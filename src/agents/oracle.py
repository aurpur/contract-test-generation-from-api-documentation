"""
Oracle Agent - Derives validation rules (oracles) from endpoint contexts.

This agent uses multi-LLM consensus to generate high-quality test oracles
including status codes, headers validation, response schema validation,
and business rules.

Author: Aurel IKAMA HONEY
"""
import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from agents.base_agent import BaseAgent, AgentConfig
from shared_context import (
    ContextManager,
    EndpointContext,
    Oracle,
    AgentType,
    ProcessingStatus,
)
from orchestration import Task, MessageBuilder
from utils.llm_client import BaseLLMClient, LLMClientFactory
from utils.logging import logger


class OracleAgent(BaseAgent):
    """
    Oracle Agent derives validation rules from endpoint contexts.
    
    Uses multi-LLM consensus to generate reliable oracles:
    1. Query multiple LLM models with same prompt
    2. Collect responses and parse oracles
    3. Vote on each assertion (status code, headers, schema)
    4. Select oracle elements with consensus >= threshold
    5. Store final oracle in ContextManager
    
    Supports:
    - Status code validation
    - Response header validation
    - Response schema validation
    - JSONPath assertions
    - Business rule extraction
    - Multi-LLM consensus mechanism
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        message_router,
        event_bus,
        task_queue,
        llm_configs: Optional[List[Dict[str, Any]]] = None,
        consensus_threshold: float = 0.7,
    ):
        """
        Initialize Oracle Agent.
        
        Args:
            config: Agent configuration
            context_manager: Shared context manager
            message_router: Message router for inter-agent communication
            event_bus: Event bus for publishing events
            task_queue: Task queue for processing
            llm_configs: List of LLM configurations for consensus
            consensus_threshold: Minimum agreement ratio (0.0-1.0)
        """
        super().__init__(
            config=config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Initialize LLM clients for consensus
        self.llm_clients: List[BaseLLMClient] = []
        if llm_configs:
            for llm_config in llm_configs:
                try:
                    client = LLMClientFactory.create_client(llm_config)
                    self.llm_clients.append(client)
                    logger.info(
                        f"Initialized LLM client: {llm_config.get('provider')} "
                        f"({llm_config.get('model')})"
                    )
                except Exception as e:
                    logger.error(f"Failed to initialize LLM client: {e}")
        
        self.consensus_threshold = consensus_threshold
        
        # Metrics
        self.metrics["oracles_generated"] = 0
        self.metrics["consensus_votes"] = 0
        self.metrics["llm_calls"] = 0
        self.metrics["low_confidence_oracles"] = 0
    
    def register_handlers(self) -> None:
        """Register message handlers for oracle derivation."""
        self.message_router.register(
            agent_type=AgentType.ORACLE,
            message_type="derive_oracles",
            handler=self._handle_derive_oracles_message,
        )
        
        self.message_router.register(
            agent_type=AgentType.ORACLE,
            message_type="derive_single_oracle",
            handler=self._handle_derive_single_oracle_message,
        )
        
        self.message_router.register(
            agent_type=AgentType.ORACLE,
            message_type="validate_oracle_quality",
            handler=self._handle_validate_oracle_quality_message,
        )
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process oracle derivation tasks.
        
        Args:
            task: Task to process
            
        Returns:
            Task result dictionary
        """
        task_type = task.task_type
        
        if task_type == "derive_oracles":
            return await self._derive_oracles_from_contexts(task)
        elif task_type == "derive_single_oracle":
            return await self._derive_single_oracle(task)
        elif task_type == "validate_oracle_quality":
            return await self._validate_oracle_quality(task)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    async def _derive_oracles_from_contexts(self, task: Task) -> Dict[str, Any]:
        """
        Derive oracles for multiple endpoint contexts.
        
        Args:
            task: Task with context_ids in payload
            
        Returns:
            Result with oracle_ids and statistics
        """
        context_ids = task.payload.get("context_ids", [])
        session_id = task.payload.get("session_id")
        
        if not context_ids:
            logger.warning("No context IDs provided for oracle derivation")
            return {
                "status": "error",
                "error": "No context IDs provided"
            }
        
        logger.info(f"Deriving oracles for {len(context_ids)} contexts")
        
        oracle_ids = []
        failed_contexts = []
        
        for context_id in context_ids:
            try:
                # Retrieve endpoint context
                context = await self.context_manager.get_endpoint_context(
                    context_id=UUID(context_id) if isinstance(context_id, str) else context_id
                )
                
                if not context:
                    logger.warning(f"Context not found: {context_id}")
                    failed_contexts.append(context_id)
                    continue
                
                # Derive oracle using multi-LLM consensus
                oracle = await self._derive_oracle_with_consensus(context)
                
                if oracle:
                    # Store oracle
                    await self.context_manager.store_oracle(oracle)
                    oracle_ids.append(str(oracle.id))
                    
                    self.metrics["oracles_generated"] += 1
                    logger.info(
                        f"Oracle generated for {context.name}: "
                        f"confidence={oracle.confidence_score:.2f}"
                    )
                else:
                    failed_contexts.append(context_id)
                    logger.warning(f"Failed to derive oracle for context: {context_id}")
                    
            except Exception as e:
                logger.error(f"Error deriving oracle for context {context_id}: {e}")
                failed_contexts.append(context_id)
        
        # Publish event
        if oracle_ids and session_id:
            await self.event_bus.publish(
                event_type="oracles_derived",
                data={
                    "session_id": str(session_id),
                    "oracle_ids": oracle_ids,
                    "oracles_count": len(oracle_ids),
                    "failed_count": len(failed_contexts),
                    "consensus_threshold": self.consensus_threshold,
                },
            )
        
        return {
            "status": "success",
            "oracles_generated": len(oracle_ids),
            "oracle_ids": oracle_ids,
            "failed_contexts": failed_contexts,
        }
    
    async def _derive_single_oracle(self, task: Task) -> Dict[str, Any]:
        """
        Derive oracle for a single endpoint context.
        
        Args:
            task: Task with context_id in payload
            
        Returns:
            Result with oracle_id
        """
        context_id = task.payload.get("context_id")
        
        if not context_id:
            return {"status": "error", "error": "No context_id provided"}
        
        # Retrieve context
        context = await self.context_manager.get_endpoint_context(
            context_id=UUID(context_id) if isinstance(context_id, str) else context_id
        )
        
        if not context:
            return {"status": "error", "error": f"Context not found: {context_id}"}
        
        # Derive oracle
        oracle = await self._derive_oracle_with_consensus(context)
        
        if not oracle:
            return {"status": "error", "error": "Failed to derive oracle"}
        
        # Store oracle
        await self.context_manager.store_oracle(oracle)
        
        self.metrics["oracles_generated"] += 1
        
        return {
            "status": "success",
            "oracle_id": str(oracle.id),
            "confidence_score": oracle.confidence_score,
        }
    
    async def _validate_oracle_quality(self, task: Task) -> Dict[str, Any]:
        """
        Validate quality of a generated oracle.
        
        Args:
            task: Task with oracle_id in payload
            
        Returns:
            Validation results
        """
        oracle_id = task.payload.get("oracle_id")
        
        if not oracle_id:
            return {"status": "error", "error": "No oracle_id provided"}
        
        # Retrieve oracle
        oracle = await self.context_manager.get_oracle(
            oracle_id=UUID(oracle_id) if isinstance(oracle_id, str) else oracle_id
        )
        
        if not oracle:
            return {"status": "error", "error": f"Oracle not found: {oracle_id}"}
        
        # Validate oracle quality
        quality_score, issues = self._calculate_oracle_quality(oracle)
        
        return {
            "status": "success",
            "oracle_id": str(oracle.id),
            "quality_score": quality_score,
            "issues": issues,
            "is_valid": quality_score >= 0.6,
        }
    
    async def _derive_oracle_with_consensus(
        self, context: EndpointContext
    ) -> Optional[Oracle]:
        """
        Derive oracle using multi-LLM consensus.
        
        Args:
            context: Endpoint context
            
        Returns:
            Oracle with consensus-based validations or None
        """
        if not self.llm_clients:
            logger.warning("No LLM clients configured, using fallback oracle generation")
            return self._generate_fallback_oracle(context)
        
        # Generate prompt
        prompt = self._build_oracle_prompt(context)
        
        # Query all LLM models
        responses = await self._query_all_llms(prompt)
        
        if not responses:
            logger.warning("No LLM responses received, using fallback")
            return self._generate_fallback_oracle(context)
        
        # Parse oracle proposals from responses
        oracle_proposals = []
        for response, model_name in responses:
            try:
                oracle_data = self._parse_llm_oracle_response(response)
                if oracle_data:
                    oracle_proposals.append((oracle_data, model_name))
            except Exception as e:
                logger.error(f"Failed to parse oracle from {model_name}: {e}")
        
        if not oracle_proposals:
            logger.warning("No valid oracle proposals, using fallback")
            return self._generate_fallback_oracle(context)
        
        # Apply consensus mechanism
        consensus_oracle = self._apply_consensus(oracle_proposals, context)
        
        return consensus_oracle
    
    async def _query_all_llms(self, prompt: str) -> List[Tuple[str, str]]:
        """
        Query all configured LLM models in parallel.
        
        Args:
            prompt: Oracle generation prompt
            
        Returns:
            List of (response, model_name) tuples
        """
        tasks = []
        for client in self.llm_clients:
            tasks.append(self._query_llm_with_timeout(client, prompt))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"LLM query failed: {result}")
                continue
            
            if result:
                model_name = getattr(self.llm_clients[i], "model", f"llm_{i}")
                responses.append((result, model_name))
                self.metrics["llm_calls"] += 1
        
        return responses
    
    async def _query_llm_with_timeout(
        self, client: BaseLLMClient, prompt: str, timeout: float = 30.0
    ) -> Optional[str]:
        """
        Query LLM with timeout protection.
        
        Args:
            client: LLM client
            prompt: Prompt to send
            timeout: Timeout in seconds
            
        Returns:
            LLM response or None
        """
        try:
            response = await asyncio.wait_for(
                client.generate(prompt),
                timeout=timeout
            )
            return response
        except asyncio.TimeoutError:
            logger.warning(f"LLM query timeout after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"LLM query error: {e}")
            return None
    
    def _build_oracle_prompt(self, context: EndpointContext) -> str:
        """
        Build prompt for oracle generation.
        
        Args:
            context: Endpoint context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Generate test oracle (validation rules) for the following API endpoint.

**Endpoint Information:**
- Name: {context.name}
- Method: {context.method.value}
- URL: {context.url}
- Description: {context.description or "N/A"}

**Request Details:**
"""
        
        if context.headers:
            prompt += f"- Headers: {json.dumps(context.headers, indent=2)}\n"
        
        if context.query_params:
            prompt += f"- Query Parameters: {json.dumps(context.query_params, indent=2)}\n"
        
        if context.body:
            prompt += f"- Request Body: {json.dumps(context.body, indent=2)}\n"
        
        if context.auth_type.value != "none":
            prompt += f"- Authentication: {context.auth_type.value}\n"
        
        if context.expected_status:
            prompt += f"\n**Expected Response:**\n"
            prompt += f"- Status Code: {context.expected_status}\n"
        
        if context.expected_headers:
            prompt += f"- Headers: {json.dumps(context.expected_headers, indent=2)}\n"
        
        if context.expected_response_schema:
            prompt += f"- Response Schema: {json.dumps(context.expected_response_schema, indent=2)}\n"
        
        prompt += """
**Task:**
Generate a comprehensive test oracle with the following validations:

1. **Status Code Validation:**
   - Expected HTTP status code
   - Acceptable status code range (if applicable)

2. **Response Header Validation:**
   - Required headers (e.g., Content-Type, Authorization)
   - Header value constraints

3. **Response Body Validation:**
   - JSON schema for response structure
   - JSONPath assertions for specific fields
   - Value constraints (e.g., id > 0, email format)

4. **Business Rules:**
   - Domain-specific validation rules
   - Data consistency rules

**Output Format (JSON):**
{
  "status_code": 200,
  "status_code_range": [200, 299],
  "required_headers": ["Content-Type", "X-Request-ID"],
  "header_constraints": {
    "Content-Type": "application/json"
  },
  "response_schema": {
    "type": "object",
    "properties": {...}
  },
  "json_path_assertions": {
    "$.id": {"type": "integer", "minimum": 1},
    "$.email": {"type": "string", "format": "email"}
  },
  "value_constraints": {
    "id": {"type": "integer", "minimum": 1},
    "created_at": {"type": "string", "format": "date-time"}
  },
  "business_rules": [
    "Response must include user ID",
    "Email must be valid format"
  ],
  "rationale": "Explanation of validation choices"
}

Generate the oracle now:
"""
        
        return prompt
    
    def _parse_llm_oracle_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse LLM response to extract oracle data.
        
        Args:
            response: LLM response text
            
        Returns:
            Parsed oracle data or None
        """
        # Try to extract JSON from response
        # Handle markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            json_str = response[start:end].strip()
        else:
            json_str = response.strip()
        
        try:
            oracle_data = json.loads(json_str)
            return oracle_data
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from LLM response")
            return None
    
    def _apply_consensus(
        self, oracle_proposals: List[Tuple[Dict[str, Any], str]], context: EndpointContext
    ) -> Oracle:
        """
        Apply consensus mechanism to oracle proposals.
        
        Votes on each oracle element and selects those with agreement >= threshold.
        
        Args:
            oracle_proposals: List of (oracle_data, model_name) tuples
            context: Endpoint context
            
        Returns:
            Consensus oracle
        """
        num_models = len(oracle_proposals)
        self.metrics["consensus_votes"] += 1
        
        # Vote on status code
        status_codes = [p[0].get("status_code") for p in oracle_proposals if p[0].get("status_code")]
        consensus_status_code = self._vote_on_value(status_codes, num_models)
        
        # Vote on required headers
        all_headers = []
        for proposal, _ in oracle_proposals:
            headers = proposal.get("required_headers", [])
            all_headers.extend(headers)
        consensus_headers = self._vote_on_list(all_headers, num_models)
        
        # Merge header constraints
        header_constraints = {}
        for proposal, _ in oracle_proposals:
            constraints = proposal.get("header_constraints", {})
            for key, value in constraints.items():
                if key not in header_constraints:
                    header_constraints[key] = []
                header_constraints[key].append(value)
        
        # Select most common constraint value for each header
        consensus_header_constraints = {}
        for key, values in header_constraints.items():
            consensus_value = self._vote_on_value(values, num_models)
            if consensus_value:
                consensus_header_constraints[key] = consensus_value
        
        # Merge response schemas (take most complete)
        response_schemas = [
            p[0].get("response_schema") for p in oracle_proposals
            if p[0].get("response_schema")
        ]
        consensus_schema = self._select_most_complete_schema(response_schemas)
        
        # Merge JSONPath assertions
        json_path_assertions = {}
        for proposal, _ in oracle_proposals:
            assertions = proposal.get("json_path_assertions", {})
            for path, constraint in assertions.items():
                if path not in json_path_assertions:
                    json_path_assertions[path] = []
                json_path_assertions[path].append(constraint)
        
        consensus_json_path = {}
        for path, constraints in json_path_assertions.items():
            # Take most common constraint
            if constraints:
                consensus_json_path[path] = constraints[0]  # Simplified: take first
        
        # Merge business rules
        all_business_rules = []
        for proposal, _ in oracle_proposals:
            rules = proposal.get("business_rules", [])
            all_business_rules.extend(rules)
        consensus_business_rules = self._vote_on_list(all_business_rules, num_models)
        
        # Calculate confidence score based on consensus
        confidence_score = self._calculate_consensus_confidence(
            oracle_proposals, num_models
        )
        
        if confidence_score < 0.6:
            self.metrics["low_confidence_oracles"] += 1
        
        # Collect rationales
        rationales = [p[0].get("rationale", "") for p in oracle_proposals if p[0].get("rationale")]
        combined_rationale = " | ".join(rationales) if rationales else None
        
        # Build consensus oracle
        oracle = Oracle(
            endpoint_id=context.id,
            status_code=consensus_status_code or context.expected_status or 200,
            status_code_range=None,  # Could be derived from proposals
            required_headers=consensus_headers,
            header_constraints=consensus_header_constraints,
            response_schema=consensus_schema,
            json_path_assertions=consensus_json_path,
            value_constraints={},  # Could be extracted from proposals
            business_rules=consensus_business_rules,
            confidence_score=confidence_score,
            rationale=combined_rationale,
            llm_model=f"consensus_{num_models}_models",
            generated_at=datetime.utcnow(),
        )
        
        return oracle
    
    def _vote_on_value(self, values: List[Any], num_models: int) -> Optional[Any]:
        """
        Vote on a single value - select most common if above threshold.
        
        Args:
            values: List of values from different models
            num_models: Total number of models
            
        Returns:
            Consensus value or None
        """
        if not values:
            return None
        
        # Count occurrences
        from collections import Counter
        counter = Counter(values)
        most_common_value, count = counter.most_common(1)[0]
        
        # Check if above threshold
        agreement_ratio = count / num_models
        if agreement_ratio >= self.consensus_threshold:
            return most_common_value
        
        return None
    
    def _vote_on_list(self, items: List[Any], num_models: int) -> List[Any]:
        """
        Vote on list items - include items above threshold.
        
        Args:
            items: List of items from all models
            num_models: Total number of models
            
        Returns:
            List of consensus items
        """
        from collections import Counter
        counter = Counter(items)
        
        consensus_items = []
        for item, count in counter.items():
            agreement_ratio = count / num_models
            if agreement_ratio >= self.consensus_threshold:
                consensus_items.append(item)
        
        return consensus_items
    
    def _select_most_complete_schema(
        self, schemas: List[Optional[Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        """
        Select most complete schema from proposals.
        
        Args:
            schemas: List of schema proposals
            
        Returns:
            Most complete schema
        """
        if not schemas:
            return None
        
        # Score schemas by number of properties
        def score_schema(schema: Optional[Dict[str, Any]]) -> int:
            if not schema:
                return 0
            
            score = 0
            if "properties" in schema:
                score += len(schema["properties"])
            if "required" in schema:
                score += len(schema["required"])
            
            return score
        
        scored_schemas = [(schema, score_schema(schema)) for schema in schemas]
        scored_schemas.sort(key=lambda x: x[1], reverse=True)
        
        return scored_schemas[0][0] if scored_schemas else None
    
    def _calculate_consensus_confidence(
        self, oracle_proposals: List[Tuple[Dict[str, Any], str]], num_models: int
    ) -> float:
        """
        Calculate confidence score based on consensus level.
        
        Args:
            oracle_proposals: List of oracle proposals
            num_models: Number of models
            
        Returns:
            Confidence score (0.0-1.0)
        """
        if num_models == 1:
            return 0.7  # Single model has moderate confidence
        
        # Calculate agreement on key fields
        agreements = []
        
        # Status code agreement
        status_codes = [p[0].get("status_code") for p in oracle_proposals]
        if status_codes:
            from collections import Counter
            most_common_count = Counter(status_codes).most_common(1)[0][1]
            agreements.append(most_common_count / num_models)
        
        # Headers agreement
        all_headers_sets = [
            set(p[0].get("required_headers", [])) for p in oracle_proposals
        ]
        if all_headers_sets:
            # Jaccard similarity
            intersection = set.intersection(*all_headers_sets)
            union = set.union(*all_headers_sets)
            if union:
                agreements.append(len(intersection) / len(union))
        
        # Average agreement
        if agreements:
            return sum(agreements) / len(agreements)
        
        return 0.5  # Default moderate confidence
    
    def _generate_fallback_oracle(self, context: EndpointContext) -> Oracle:
        """
        Generate basic oracle without LLM (fallback).
        
        Args:
            context: Endpoint context
            
        Returns:
            Basic oracle derived from context
        """
        logger.info(f"Generating fallback oracle for {context.name}")
        
        # Extract basic validations from context
        status_code = context.expected_status or 200
        
        required_headers = []
        if context.expected_headers:
            required_headers = list(context.expected_headers.keys())
        
        oracle = Oracle(
            endpoint_id=context.id,
            status_code=status_code,
            required_headers=required_headers,
            header_constraints=context.expected_headers.copy() if context.expected_headers else {},
            response_schema=context.expected_response_schema,
            json_path_assertions={},
            value_constraints={},
            business_rules=[],
            confidence_score=0.5,  # Low confidence for fallback
            rationale="Generated without LLM (fallback)",
            llm_model="fallback",
            generated_at=datetime.utcnow(),
        )
        
        return oracle
    
    def _calculate_oracle_quality(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """
        Calculate quality score for an oracle.
        
        Args:
            oracle: Oracle to validate
            
        Returns:
            Tuple of (quality_score, list_of_issues)
        """
        score = 1.0
        issues = []
        
        # Check status code
        if not oracle.status_code or oracle.status_code < 100 or oracle.status_code > 599:
            score -= 0.2
            issues.append("Invalid status code")
        
        # Check required headers
        if not oracle.required_headers:
            score -= 0.1
            issues.append("No required headers specified")
        
        # Check response schema
        if not oracle.response_schema:
            score -= 0.15
            issues.append("No response schema specified")
        
        # Check confidence
        if oracle.confidence_score < 0.6:
            score -= 0.1
            issues.append("Low confidence score")
        
        # Check completeness
        if not oracle.json_path_assertions and not oracle.business_rules:
            score -= 0.15
            issues.append("No assertions or business rules")
        
        return max(0.0, score), issues
    
    # Message handlers
    
    async def _handle_derive_oracles_message(self, message) -> None:
        """Handle derive_oracles message."""
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="derive_oracles",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        # Send acknowledgment
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    async def _handle_derive_single_oracle_message(self, message) -> None:
        """Handle derive_single_oracle message."""
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="derive_single_oracle",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    async def _handle_validate_oracle_quality_message(self, message) -> None:
        """Handle validate_oracle_quality message."""
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="validate_oracle_quality",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"OracleAgent(state={self.state.value}, "
            f"active_tasks={len(self.active_tasks)}, "
            f"llm_clients={len(self.llm_clients)}, "
            f"consensus_threshold={self.consensus_threshold})"
        )
