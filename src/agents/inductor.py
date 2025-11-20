"""
Inductor Agent - Extracts context from API documentation.

This agent is responsible for:
- Parsing Bruno collections
- Extracting endpoint contexts
- Enriching contexts with LLM assistance
- Storing contexts in the shared context manager

Author: Aurel IKAMA HONEY
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from shared_context import (
    AgentType,
    ContextManager,
    EndpointContext,
    HTTPMethod,
    AuthType,
    ProcessingStatus,
)
from orchestration import Task, TaskStatus, MessageBuilder
from parsers.bruno_parser import BrunoParser
from parsers.bruno_models import BrunoItem, BrunoRequest, BrunoParseResult
from utils.llm_client import BaseLLMClient, LLMClientFactory
from utils.logging import logger

from .base_agent import BaseAgent, AgentConfig, AgentState


class InductorAgent(BaseAgent):
    """
    Inductor Agent extracts API context from Bruno collections.
    
    This agent:
    1. Parses Bruno collection files (.json or .bru)
    2. Extracts endpoint information
    3. Uses LLM to enrich incomplete documentation
    4. Stores EndpointContext in ContextManager
    5. Publishes "context_extracted" events
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        router,
        event_bus,
        task_queue,
        llm_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Inductor Agent.
        
        Args:
            config: Agent configuration
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            llm_config: LLM configuration for context enrichment
        """
        super().__init__(config, context_manager, router, event_bus, task_queue, llm_config)
        
        self.logger = logger.bind(agent="InductorAgent")
        self.parser = BrunoParser()
        
        # Initialize LLM client if configured
        self.llm_client: Optional[BaseLLMClient] = None
        if llm_config:
            try:
                provider = llm_config.get("provider", "ollama")
                model = llm_config.get("model", "llama3.1:70b")
                self.llm_client = LLMClientFactory.create(
                    provider=provider,
                    model=model,
                    temperature=llm_config.get("temperature", 0.2),
                    max_tokens=llm_config.get("max_tokens", 2048),
                )
                self.logger.info(f"Initialized LLM client: {provider}/{model}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize LLM client: {e}")
        
        # Register message handlers
        self.register_handlers()
        
        # Note: Event subscription will happen during start() lifecycle method
    
    def register_handlers(self):
        """Register message handlers for this agent."""
        self.register_message_handler("extract_context", self._handle_extract_context_message)
        self.register_message_handler("parse_collection", self._handle_parse_collection_message)
        self.register_message_handler("enrich_context", self._handle_enrich_context_message)
    
    async def _subscribe_to_events(self):
        """Subscribe to relevant events."""
        # Subscribe to workflow events if needed
        await self.subscribe_to_event("workflow_started", self._on_workflow_started)
    
    async def _on_workflow_started(self, event_data: Dict[str, Any]):
        """Handle workflow started event."""
        self.logger.info(f"Workflow started: {event_data.get('session_id')}")
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process a task assigned to this agent.
        
        Args:
            task: Task to process
            
        Returns:
            Task result dictionary
            
        Raises:
            ValueError: If task type is unsupported
        """
        task_type = task.task_type
        
        self.logger.info(f"Processing task: {task_type} (ID: {task.id})")
        
        if task_type == "extract_context":
            return await self._extract_context_from_collection(task)
        elif task_type == "parse_collection":
            return await self._parse_bruno_collection(task)
        elif task_type == "enrich_context":
            return await self._enrich_endpoint_context(task)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    async def _extract_context_from_collection(self, task: Task) -> Dict[str, Any]:
        """
        Extract endpoint contexts from a Bruno collection.
        
        Args:
            task: Task with collection_path in payload
            
        Returns:
            Dictionary with extracted contexts
        """
        collection_path = task.payload.get("collection_path")
        session_id = task.session_id  # Use task.session_id directly (already a UUID)
        enrich_with_llm = task.payload.get("enrich_with_llm", False)
        
        if not collection_path:
            raise ValueError("collection_path is required")
        
        self.logger.info(f"Extracting context from: {collection_path}")
        
        # Parse the Bruno collection
        parse_result = self.parser.parse_collection_from_json(collection_path)
        
        # Extract endpoints from the collection
        endpoints = self._extract_endpoints_from_parse_result(parse_result)
        
        self.logger.info(f"Extracted {len(endpoints)} endpoints from collection")
        
        # Enrich with LLM if requested and available
        if enrich_with_llm and self.llm_client:
            self.logger.info("Enriching contexts with LLM")
            enriched_endpoints = []
            for endpoint in endpoints:
                try:
                    enriched = await self._enrich_endpoint_with_llm(endpoint)
                    enriched_endpoints.append(enriched)
                except Exception as e:
                    self.logger.warning(f"Failed to enrich endpoint {endpoint.name}: {e}")
                    enriched_endpoints.append(endpoint)
            endpoints = enriched_endpoints
        
        # Store contexts in ContextManager
        stored_contexts = []
        for endpoint in endpoints:
            try:
                # Add endpoint context to session
                await self.context_manager.add_endpoint(
                    session_id=session_id,
                    endpoint=endpoint
                )
                stored_contexts.append(endpoint.id)
                self.logger.debug(f"Stored context for endpoint: {endpoint.name}")
            except Exception as e:
                self.logger.error(f"Failed to store context for {endpoint.name}: {e}")
        
        # Publish event
        await self.publish_event(
            "context_extracted",
            {
                "collection_path": collection_path,
                "endpoints_count": len(endpoints),
                "context_ids": [str(ctx_id) for ctx_id in stored_contexts],
                "agent": self.agent_type.value,
            },
            session_id=session_id  # Pass session_id as separate argument
        )
        
        return {
            "status": "success",
            "endpoints_extracted": len(endpoints),
            "contexts_stored": len(stored_contexts),
            "context_ids": [str(ctx_id) for ctx_id in stored_contexts],
        }
    
    async def _parse_bruno_collection(self, task: Task) -> Dict[str, Any]:
        """
        Parse a Bruno collection without storing contexts.
        
        Args:
            task: Task with collection_path in payload
            
        Returns:
            Dictionary with parse results
        """
        collection_path = task.payload.get("collection_path")
        
        if not collection_path:
            raise ValueError("collection_path is required")
        
        self.logger.info(f"Parsing collection: {collection_path}")
        
        parse_result = self.parser.parse_collection_from_json(collection_path)
        
        return {
            "status": "success",
            "collection_name": parse_result.collection.name,
            "total_requests": parse_result.total_requests,
            "total_folders": parse_result.total_folders,
            "endpoints": parse_result.endpoints,
            "methods": parse_result.methods,
        }
    
    async def _enrich_endpoint_context(self, task: Task) -> Dict[str, Any]:
        """
        Enrich an existing endpoint context with LLM.
        
        Args:
            task: Task with context_id in payload
            
        Returns:
            Dictionary with enrichment results
        """
        context_id = task.payload.get("context_id")
        session_id = task.session_id  # Use task.session_id directly (already a UUID)
        
        if not context_id:
            raise ValueError("context_id is required")
        
        # Retrieve context from ContextManager
        context = await self.context_manager.get_endpoint_context(
            session_id=session_id,
            context_id=UUID(context_id)
        )
        
        if not context:
            raise ValueError(f"Context not found: {context_id}")
        
        # Enrich with LLM
        enriched = await self._enrich_endpoint_with_llm(context)
        
        # Update context in ContextManager
        await self.context_manager.update_endpoint_context(
            session_id=UUID(session_id),
            context_id=UUID(context_id),
            updates=enriched.model_dump()
        )
        
        return {
            "status": "success",
            "context_id": str(context_id),
            "enriched": True,
        }
    
    def _extract_endpoints_from_parse_result(
        self, parse_result: BrunoParseResult
    ) -> List[EndpointContext]:
        """
        Extract EndpointContext objects from parsed Bruno collection.
        
        Args:
            parse_result: Parsed Bruno collection
            
        Returns:
            List of EndpointContext objects
        """
        endpoints = []
        
        # Traverse the collection tree and extract requests
        def traverse_items(items: List[BrunoItem]):
            for item in items:
                if item.request:
                    endpoint = self._bruno_request_to_endpoint_context(item.request, item.name)
                    endpoints.append(endpoint)
                
                # Recursively traverse folders
                if item.items:
                    traverse_items(item.items)
        
        traverse_items(parse_result.collection.items)
        
        return endpoints
    
    def _bruno_request_to_endpoint_context(
        self, request: BrunoRequest, name: str
    ) -> EndpointContext:
        """
        Convert a BrunoRequest to an EndpointContext.
        
        Args:
            request: Bruno request object
            name: Request name
            
        Returns:
            EndpointContext object
        """
        # Extract HTTP method
        method = HTTPMethod(request.method.upper())
        
        # Extract headers
        headers = {}
        if request.headers:
            for header in request.headers:
                if header.enabled:
                    headers[header.name] = header.value
        
        # Extract query parameters
        query_params = {}
        if request.params:
            for param in request.params:
                if param.enabled:
                    query_params[param.name] = param.value
        
        # Extract body
        body = None
        body_schema = None
        if request.body:
            if request.body.json:
                body = request.body.json
                # Try to infer schema from JSON
                try:
                    body_schema = self._infer_schema_from_json(body)
                except Exception:
                    pass
        
        # Extract authentication
        auth_type = AuthType.NONE
        auth_config = {}
        if request.auth and request.auth.mode != "none":
            auth_type_map = {
                "basic": AuthType.BASIC,
                "bearer": AuthType.BEARER,
                "apikey": AuthType.API_KEY,
                "oauth2": AuthType.OAUTH2,
            }
            auth_type = auth_type_map.get(request.auth.mode, AuthType.NONE)
            
            # Store auth configuration (sanitized)
            if auth_type == AuthType.BASIC:
                auth_config = {"username": request.auth.username or "", "password": "***"}
            elif auth_type == AuthType.BEARER:
                auth_config = {"token": "***"}
            elif auth_type == AuthType.API_KEY:
                auth_config = {"key": "apikey", "value": "***"}
        
        # Calculate documentation completeness
        completeness = self._calculate_documentation_completeness(request)
        
        return EndpointContext(
            name=name,
            method=method,
            url=request.url,
            headers=headers,
            query_params=query_params,
            body=body,
            body_schema=body_schema,
            auth_type=auth_type,
            auth_config=auth_config,
            description=None,  # Bruno doesn't have description in the current model
            documentation_completeness=completeness,
        )
    
    def _infer_schema_from_json(self, json_data: Any) -> Dict[str, Any]:
        """
        Infer a simple JSON schema from JSON data.
        
        Args:
            json_data: JSON data
            
        Returns:
            Simplified schema dictionary
        """
        if isinstance(json_data, dict):
            schema = {"type": "object", "properties": {}}
            for key, value in json_data.items():
                schema["properties"][key] = self._infer_schema_from_json(value)
            return schema
        elif isinstance(json_data, list):
            if json_data:
                return {"type": "array", "items": self._infer_schema_from_json(json_data[0])}
            return {"type": "array"}
        elif isinstance(json_data, str):
            return {"type": "string"}
        elif isinstance(json_data, (int, float)):
            return {"type": "number"}
        elif isinstance(json_data, bool):
            return {"type": "boolean"}
        else:
            return {"type": "any"}
    
    def _calculate_documentation_completeness(self, request: BrunoRequest) -> float:
        """
        Calculate documentation completeness score (0.0 to 1.0).
        
        Args:
            request: Bruno request
            
        Returns:
            Completeness score
        """
        score = 0.0
        max_score = 0.0
        
        # URL present (mandatory)
        max_score += 1.0
        if request.url:
            score += 1.0
        
        # Headers present
        max_score += 1.0
        if request.headers and len(request.headers) > 0:
            score += 1.0
        
        # Body present (for POST/PUT/PATCH)
        if request.method.upper() in ["POST", "PUT", "PATCH"]:
            max_score += 1.0
            if request.body and request.body.json:
                score += 1.0
        
        # Authentication present
        max_score += 1.0
        if request.auth and request.auth.mode != "none":
            score += 1.0
        
        # Scripts present (pre-request or post-response)
        max_score += 1.0
        if request.script:
            if request.script.req or request.script.res:
                score += 1.0
        
        return score / max_score if max_score > 0 else 0.0
    
    async def _enrich_endpoint_with_llm(self, endpoint: EndpointContext) -> EndpointContext:
        """
        Enrich an endpoint context using LLM.
        
        Args:
            endpoint: Endpoint context to enrich
            
        Returns:
            Enriched endpoint context
        """
        if not self.llm_client:
            return endpoint
        
        # Build prompt for LLM
        prompt = self._build_enrichment_prompt(endpoint)
        
        try:
            # Generate enrichment using LLM
            response = self.llm_client.generate(prompt)
            
            # Parse LLM response
            enrichment = self._parse_llm_enrichment_response(response)
            
            # Update endpoint with enrichment
            if enrichment.get("description"):
                endpoint.description = enrichment["description"]
            
            if enrichment.get("expected_status"):
                endpoint.expected_status = enrichment["expected_status"]
            
            if enrichment.get("expected_headers"):
                endpoint.expected_headers.update(enrichment["expected_headers"])
            
            if enrichment.get("tags"):
                endpoint.tags = enrichment["tags"]
            
            self.logger.debug(f"Enriched endpoint: {endpoint.name}")
            
        except Exception as e:
            self.logger.warning(f"Failed to enrich endpoint with LLM: {e}")
        
        return endpoint
    
    def _build_enrichment_prompt(self, endpoint: EndpointContext) -> str:
        """
        Build a prompt for LLM to enrich endpoint context.
        
        Args:
            endpoint: Endpoint context
            
        Returns:
            Prompt string
        """
        prompt = f"""You are an API documentation expert. Analyze this API endpoint and provide additional context.

Endpoint: {endpoint.name}
Method: {endpoint.method.value}
URL: {endpoint.url}
Headers: {json.dumps(endpoint.headers, indent=2) if endpoint.headers else "None"}
Query Parameters: {json.dumps(endpoint.query_params, indent=2) if endpoint.query_params else "None"}
Body: {json.dumps(endpoint.body, indent=2) if endpoint.body else "None"}
Authentication: {endpoint.auth_type.value}

Please provide:
1. A concise description of what this endpoint does (1-2 sentences)
2. The expected HTTP status code for a successful response
3. Expected response headers (if any)
4. Relevant tags/categories for this endpoint (e.g., "user", "authentication", "crud")

Format your response as JSON:
{{
  "description": "...",
  "expected_status": 200,
  "expected_headers": {{"Content-Type": "application/json"}},
  "tags": ["tag1", "tag2"]
}}
"""
        return prompt
    
    def _parse_llm_enrichment_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM enrichment response.
        
        Args:
            response: LLM response text
            
        Returns:
            Parsed enrichment dictionary
        """
        try:
            # Try to extract JSON from response
            # LLM might return JSON wrapped in markdown code blocks
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            enrichment = json.loads(json_str)
            return enrichment
            
        except Exception as e:
            self.logger.warning(f"Failed to parse LLM response: {e}")
            return {}
    
    async def _handle_extract_context_message(self, message):
        """Handle extract_context message."""
        # Submit task to queue
        task = Task(
            task_id=uuid4(),
            task_type="extract_context",
            priority=message.priority,
            data=message.content,
            created_at=message.timestamp,
        )
        
        await self.task_queue.submit(task)
        
        # Send acknowledgment
        response = (
            MessageBuilder()
            .of_type("acknowledgment")
            .from_agent(self.agent_type)
            .to_agent(message.source)
            .for_session(message.session_id)
            .in_reply_to(message.message_id)
            .with_content({"status": "accepted", "task_id": str(task.task_id)})
            .build()
        )
        
        await self.send_message(response)
    
    async def _handle_parse_collection_message(self, message):
        """Handle parse_collection message."""
        task = Task(
            task_id=uuid4(),
            task_type="parse_collection",
            priority=message.priority,
            data=message.content,
            created_at=message.timestamp,
        )
        
        await self.task_queue.submit(task)
        
        response = (
            MessageBuilder()
            .of_type("acknowledgment")
            .from_agent(self.agent_type)
            .to_agent(message.source)
            .for_session(message.session_id)
            .in_reply_to(message.message_id)
            .with_content({"status": "accepted", "task_id": str(task.task_id)})
            .build()
        )
        
        await self.send_message(response)
    
    async def _handle_enrich_context_message(self, message):
        """Handle enrich_context message."""
        task = Task(
            task_id=uuid4(),
            task_type="enrich_context",
            priority=message.priority,
            data=message.content,
            created_at=message.timestamp,
        )
        
        await self.task_queue.submit(task)
        
        response = (
            MessageBuilder()
            .of_type("acknowledgment")
            .from_agent(self.agent_type)
            .to_agent(message.source)
            .for_session(message.session_id)
            .in_reply_to(message.message_id)
            .with_content({"status": "accepted", "task_id": str(task.task_id)})
            .build()
        )
        
        await self.send_message(response)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"InductorAgent(state={self.state.value}, active_tasks={len(self._active_tasks)})"


__all__ = ["InductorAgent"]
