"""
Contractor Agent - Generates Java Rest-Assured test code from oracles.

This agent generates executable Java test code using Rest-Assured framework,
injecting oracle assertions and handling authentication, headers, and request/response validation.

Author: Aurel IKAMA HONEY
"""
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from jinja2 import Environment, FileSystemLoader, Template

from agents.base_agent import BaseAgent, AgentConfig
from shared_context import (
    ContextManager,
    EndpointContext,
    Oracle,
    GeneratedTest,
    AgentType,
    HTTPMethod,
    AuthType,
)
from orchestration import Task, MessageBuilder
from utils.logging import logger


class ContractorAgent(BaseAgent):
    """
    Contractor Agent generates Java Rest-Assured test code.
    
    Workflow:
    1. Retrieve endpoint context and oracle from ContextManager
    2. Build template variables from context and oracle
    3. Render Jinja2 template with variables
    4. Format generated Java code
    5. Store GeneratedTest in ContextManager
    6. Optionally generate pom.xml for Maven
    
    Features:
    - Rest-Assured test generation
    - Oracle assertions injection
    - Authentication handling (Basic, Bearer, API Key)
    - Request/response validation
    - Header and query parameter handling
    - JSONPath assertions
    - Business rules as comments
    - Java code formatting
    - pom.xml generation
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        message_router,
        event_bus,
        task_queue,
        templates_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        base_package: str = "generated",
    ):
        """
        Initialize Contractor Agent.
        
        Args:
            config: Agent configuration
            context_manager: Shared context manager
            message_router: Message router for inter-agent communication
            event_bus: Event bus for publishing events
            task_queue: Task queue for processing
            templates_dir: Directory containing Jinja2 templates
            output_dir: Directory for generated test files
            base_package: Base Java package name
        """
        super().__init__(
            config=config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Setup templates
        if templates_dir is None:
            templates_dir = str(Path(__file__).parent.parent / "code_generation" / "templates")
        
        self.templates_dir = templates_dir
        self.output_dir = output_dir or "./generated_tests"
        self.base_package = base_package
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Metrics
        self.metrics["tests_generated"] = 0
        self.metrics["lines_of_code"] = 0
        self.metrics["assertions_count"] = 0
        self.metrics["pom_generated"] = 0
    
    def register_handlers(self) -> None:
        """Register message handlers for code generation."""
        self.message_router.register(
            agent_type=AgentType.CONTRACTOR,
            message_type="generate_tests",
            handler=self._handle_generate_tests_message,
        )
        
        self.message_router.register(
            agent_type=AgentType.CONTRACTOR,
            message_type="generate_single_test",
            handler=self._handle_generate_single_test_message,
        )
        
        self.message_router.register(
            agent_type=AgentType.CONTRACTOR,
            message_type="generate_pom",
            handler=self._handle_generate_pom_message,
        )
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process code generation tasks.
        
        Args:
            task: Task to process
            
        Returns:
            Task result dictionary
        """
        task_type = task.task_type
        
        if task_type == "generate_tests":
            return await self._generate_tests_from_oracles(task)
        elif task_type == "generate_single_test":
            return await self._generate_single_test(task)
        elif task_type == "generate_pom":
            return await self._generate_pom_xml(task)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    async def _generate_tests_from_oracles(self, task: Task) -> Dict[str, Any]:
        """
        Generate tests for multiple oracles.
        
        Args:
            task: Task with oracle_ids in payload
            
        Returns:
            Result with test_ids and statistics
        """
        oracle_ids = task.payload.get("oracle_ids", [])
        session_id = task.payload.get("session_id")
        
        if not oracle_ids:
            logger.warning("No oracle IDs provided for test generation")
            return {"status": "error", "error": "No oracle IDs provided"}
        
        logger.info(f"Generating tests for {len(oracle_ids)} oracles")
        
        test_ids = []
        failed_oracles = []
        total_lines = 0
        total_assertions = 0
        
        for oracle_id in oracle_ids:
            try:
                # Retrieve oracle
                oracle = await self.context_manager.get_oracle(
                    oracle_id=UUID(oracle_id) if isinstance(oracle_id, str) else oracle_id
                )
                
                if not oracle:
                    logger.warning(f"Oracle not found: {oracle_id}")
                    failed_oracles.append(oracle_id)
                    continue
                
                # Retrieve endpoint context
                context = await self.context_manager.get_endpoint_context(
                    context_id=oracle.endpoint_id
                )
                
                if not context:
                    logger.warning(f"Context not found for oracle: {oracle_id}")
                    failed_oracles.append(oracle_id)
                    continue
                
                # Generate test
                generated_test = await self._generate_test_from_oracle(context, oracle)
                
                if generated_test:
                    # Store test
                    await self.context_manager.store_generated_test(generated_test)
                    test_ids.append(str(generated_test.id))
                    
                    # Update metrics
                    lines = len(generated_test.test_code.split('\n'))
                    assertions = self._count_assertions(generated_test.test_code)
                    
                    total_lines += lines
                    total_assertions += assertions
                    
                    self.metrics["tests_generated"] += 1
                    self.metrics["lines_of_code"] += lines
                    self.metrics["assertions_count"] += assertions
                    
                    logger.info(
                        f"Test generated for {context.name}: "
                        f"{lines} lines, {assertions} assertions"
                    )
                else:
                    failed_oracles.append(oracle_id)
                    
            except Exception as e:
                logger.error(f"Error generating test for oracle {oracle_id}: {e}")
                failed_oracles.append(oracle_id)
        
        # Publish event
        if test_ids and session_id:
            await self.event_bus.publish(
                event_type="tests_generated",
                data={
                    "session_id": str(session_id),
                    "test_ids": test_ids,
                    "tests_count": len(test_ids),
                    "total_lines": total_lines,
                    "total_assertions": total_assertions,
                    "failed_count": len(failed_oracles),
                },
            )
        
        return {
            "status": "success",
            "tests_generated": len(test_ids),
            "test_ids": test_ids,
            "total_lines": total_lines,
            "total_assertions": total_assertions,
            "failed_oracles": failed_oracles,
        }
    
    async def _generate_single_test(self, task: Task) -> Dict[str, Any]:
        """
        Generate test for a single oracle.
        
        Args:
            task: Task with oracle_id in payload
            
        Returns:
            Result with test_id
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
        
        # Retrieve context
        context = await self.context_manager.get_endpoint_context(
            context_id=oracle.endpoint_id
        )
        
        if not context:
            return {"status": "error", "error": f"Context not found for oracle"}
        
        # Generate test
        generated_test = await self._generate_test_from_oracle(context, oracle)
        
        if not generated_test:
            return {"status": "error", "error": "Failed to generate test"}
        
        # Store test
        await self.context_manager.store_generated_test(generated_test)
        
        lines = len(generated_test.test_code.split('\n'))
        assertions = self._count_assertions(generated_test.test_code)
        
        self.metrics["tests_generated"] += 1
        self.metrics["lines_of_code"] += lines
        self.metrics["assertions_count"] += assertions
        
        return {
            "status": "success",
            "test_id": str(generated_test.id),
            "lines_of_code": lines,
            "assertions_count": assertions,
        }
    
    async def _generate_pom_xml(self, task: Task) -> Dict[str, Any]:
        """
        Generate pom.xml for Maven.
        
        Args:
            task: Task with project configuration
            
        Returns:
            Result with pom.xml content
        """
        payload = task.payload
        
        template_vars = {
            "group_id": payload.get("group_id", "com.generated"),
            "artifact_id": payload.get("artifact_id", "api-tests"),
            "version": payload.get("version", "1.0.0"),
            "project_name": payload.get("project_name", "Generated API Tests"),
            "project_description": payload.get(
                "project_description", 
                "Auto-generated REST API tests"
            ),
            "java_version": payload.get("java_version", "11"),
            "additional_dependencies": payload.get("additional_dependencies", []),
        }
        
        # Render pom.xml template
        template = self.jinja_env.get_template("pom.xml.j2")
        pom_content = template.render(**template_vars)
        
        self.metrics["pom_generated"] += 1
        
        return {
            "status": "success",
            "pom_content": pom_content,
        }
    
    async def _generate_test_from_oracle(
        self, context: EndpointContext, oracle: Oracle
    ) -> Optional[GeneratedTest]:
        """
        Generate Java test code from endpoint context and oracle.
        
        Args:
            context: Endpoint context
            oracle: Oracle with validations
            
        Returns:
            GeneratedTest object or None
        """
        try:
            # Build template variables
            template_vars = self._build_template_variables(context, oracle)
            
            # Render template
            template = self.jinja_env.get_template("rest_assured_test.java.j2")
            test_code = template.render(**template_vars)
            
            # Format code
            formatted_code = self._format_java_code(test_code)
            
            # Generate Gherkin scenario
            feature_file_name, feature_content = self._generate_gherkin_scenario(
                context, oracle, template_vars
            )
            
            # Create GeneratedTest
            generated_test = GeneratedTest(
                endpoint_id=context.id,
                oracle_id=oracle.id,
                test_class_name=template_vars["class_name"],
                test_method_name=template_vars["method_name"],
                test_code=formatted_code,
                feature_file_name=feature_file_name,
                feature_content=feature_content,
                setup_code=None,
                teardown_code=None,
                dependencies=["io.rest-assured:rest-assured:5.3.2"],
                generated_at=datetime.utcnow(),
                llm_model=oracle.llm_model,
                template_version="1.0.0",
            )
            
            return generated_test
            
        except Exception as e:
            logger.error(f"Failed to generate test: {e}")
            return None
    
    def _build_template_variables(
        self, context: EndpointContext, oracle: Oracle
    ) -> Dict[str, Any]:
        """
        Build template variables from context and oracle.
        
        Args:
            context: Endpoint context
            oracle: Oracle
            
        Returns:
            Dictionary of template variables
        """
        # Generate class and method names
        class_name = self._generate_class_name(context)
        method_name = self._generate_method_name(context)
        
        # Extract base URL and path
        base_url, endpoint_path = self._split_url(context.url)
        
        # Build template variables
        template_vars = {
            # Meta
            "package_name": self.base_package,
            "class_name": class_name,
            "method_name": method_name,
            "endpoint_name": context.name,
            "http_method": context.method.value,
            "endpoint_path": endpoint_path,
            "base_url": base_url or "http://localhost:8080",
            "generation_timestamp": datetime.utcnow().isoformat(),
            "llm_model": oracle.llm_model,
            
            # Test metadata
            "test_name": f"test{class_name}",
            "test_description": context.description,
            "test_display_name": f"Test {context.method.value} {context.name}",
            "test_order": 1,
            
            # Request
            "headers": context.headers,
            "query_params": context.query_params,
            "path_params": self._build_path_params(context),
            "request_body": context.body,
            
            # Authentication
            "auth_type": context.auth_type.value,
            **self._build_auth_variables(context),
            
            # Oracle assertions
            "expected_status": oracle.status_code,
            "required_headers": oracle.required_headers,
            "header_constraints": oracle.header_constraints,
            "response_schema": oracle.response_schema,
            "json_path_assertions": oracle.json_path_assertions,
            "business_rules": oracle.business_rules,
            
            # Setup/teardown
            "setup_code": None,
            "teardown_code": None,
            "custom_assertions": None,
        }
        
        return template_vars
    
    def _generate_class_name(self, context: EndpointContext) -> str:
        """Generate Java class name from endpoint context."""
        # Convert endpoint name to PascalCase
        name = context.name.replace("-", " ").replace("_", " ")
        name = "".join(word.capitalize() for word in name.split())
        
        # Add method prefix
        method_prefix = context.method.value.capitalize()
        
        # Add Test suffix
        class_name = f"{method_prefix}{name}Test"
        
        # Remove invalid characters
        class_name = re.sub(r'[^a-zA-Z0-9]', '', class_name)
        
        return class_name
    
    def _generate_method_name(self, context: EndpointContext) -> str:
        """Generate Java method name from endpoint context."""
        # Convert to camelCase
        name = context.name.replace("-", " ").replace("_", " ")
        words = name.split()
        
        if not words:
            method_name = "testEndpoint"
        else:
            method_name = "test" + "".join(word.capitalize() for word in words)
        
        # Remove invalid characters
        method_name = re.sub(r'[^a-zA-Z0-9]', '', method_name)
        
        return method_name
    
    def _split_url(self, url: str) -> tuple[str, str]:
        """
        Split URL into base URL and path.
        
        Args:
            url: Full URL or path
            
        Returns:
            Tuple of (base_url, path)
        """
        if url.startswith("http://") or url.startswith("https://"):
            # Full URL
            parts = url.split("/", 3)
            if len(parts) >= 4:
                base_url = "/".join(parts[:3])
                path = "/" + parts[3]
            else:
                base_url = url
                path = "/"
        else:
            # Relative path
            base_url = ""
            path = url if url.startswith("/") else "/" + url
        
        return base_url, path
    
    def _build_path_params(self, context: EndpointContext) -> Dict[str, str]:
        """
        Build path parameters dictionary.
        
        Args:
            context: Endpoint context
            
        Returns:
            Dictionary of path parameters
        """
        path_params = {}
        
        for param in context.path_params:
            # Use placeholder values
            path_params[param] = f"{{{{ {param} }}}}"
        
        return path_params
    
    def _build_auth_variables(self, context: EndpointContext) -> Dict[str, Any]:
        """
        Build authentication variables.
        
        Args:
            context: Endpoint context
            
        Returns:
            Dictionary of auth variables
        """
        auth_vars = {}
        
        if context.auth_type == AuthType.BEARER:
            auth_vars["auth_token"] = context.auth_config.get("token", "YOUR_TOKEN")
        elif context.auth_type == AuthType.BASIC:
            auth_vars["auth_username"] = context.auth_config.get("username", "user")
            auth_vars["auth_password"] = context.auth_config.get("password", "pass")
        elif context.auth_type == AuthType.API_KEY:
            auth_vars["auth_header_name"] = context.auth_config.get(
                "header_name", "X-API-Key"
            )
            auth_vars["auth_api_key"] = context.auth_config.get("key", "YOUR_API_KEY")
        
        return auth_vars
    
    def _format_java_code(self, code: str) -> str:
        """
        Format Java code (basic formatting).
        
        Args:
            code: Unformatted Java code
            
        Returns:
            Formatted Java code
        """
        # Remove excessive blank lines
        lines = code.split('\n')
        formatted_lines = []
        prev_blank = False
        
        for line in lines:
            is_blank = not line.strip()
            
            if is_blank:
                if not prev_blank:
                    formatted_lines.append(line)
                prev_blank = True
            else:
                formatted_lines.append(line)
                prev_blank = False
        
        return '\n'.join(formatted_lines)
    
    def _count_assertions(self, code: str) -> int:
        """
        Count assertions in test code.
        
        Args:
            code: Java test code
            
        Returns:
            Number of assertions
        """
        assertion_patterns = [
            r'assertEquals\(',
            r'assertNotNull\(',
            r'assertTrue\(',
            r'assertFalse\(',
            r'\.body\(',
            r'\.then\(\)',
        ]
        
        count = 0
        for pattern in assertion_patterns:
            count += len(re.findall(pattern, code))
        
        return count
    
    def _generate_gherkin_scenario(
        self, context: EndpointContext, oracle: Oracle, template_vars: Dict[str, Any]
    ) -> tuple[str, str]:
        """
        Generate Gherkin feature file from endpoint context and oracle.
        
        Args:
            context: Endpoint context
            oracle: Oracle with validations
            template_vars: Template variables (reused from Java generation)
            
        Returns:
            Tuple of (feature_file_name, feature_content)
        """
        try:
            # Build Gherkin-specific template variables
            gherkin_vars = {
                **template_vars,
                "feature_title": self._generate_feature_title(context),
                "feature_description": self._generate_feature_description(context, oracle),
                "scenario_title": self._generate_scenario_title(context),
                "scenario_description": context.description or "",
                "expected_status_code": oracle.status_code,
                "expected_response_time_ms": oracle.expected_response_time_ms,
                "oracle_confidence": oracle.confidence_score,
            }
            
            # Render Gherkin template
            template = self.jinja_env.get_template("gherkin_scenario.feature.j2")
            feature_content = template.render(**gherkin_vars)
            
            # Generate feature file name
            feature_file_name = self._generate_feature_file_name(context)
            
            return feature_file_name, feature_content
            
        except Exception as e:
            logger.error(f"Failed to generate Gherkin scenario: {e}")
            return None, None
    
    def _generate_feature_title(self, context: EndpointContext) -> str:
        """
        Generate feature title for Gherkin scenario.
        
        Args:
            context: Endpoint context
            
        Returns:
            Feature title
        """
        method = context.method.value
        name = context.name.replace('_', ' ').title()
        return f"{method} {name} API"
    
    def _generate_feature_description(self, context: EndpointContext, oracle: Oracle) -> str:
        """
        Generate feature description for Gherkin scenario.
        
        Args:
            context: Endpoint context
            oracle: Oracle
            
        Returns:
            Feature description
        """
        description = context.description or f"Test {context.method.value} {context.name} endpoint"
        
        # Add oracle metadata
        if oracle.llm_model:
            description += f"\n  Generated using {oracle.llm_model}"
        if oracle.confidence_score:
            description += f" (confidence: {oracle.confidence_score:.2f})"
        
        return description
    
    def _generate_scenario_title(self, context: EndpointContext) -> str:
        """
        Generate scenario title for Gherkin scenario.
        
        Args:
            context: Endpoint context
            
        Returns:
            Scenario title
        """
        method = context.method.value
        name = context.name.replace('_', ' ').title()
        return f"Successfully {method.lower()} {name}"
    
    def _generate_feature_file_name(self, context: EndpointContext) -> str:
        """
        Generate feature file name for Gherkin scenario.
        
        Args:
            context: Endpoint context
            
        Returns:
            Feature file name (e.g., "get-users.feature")
        """
        method = context.method.value.lower()
        name = context.name.lower().replace('_', '-')
        return f"{method}-{name}.feature"
    
    # Message handlers
    
    async def _handle_generate_tests_message(self, message) -> None:
        """Handle generate_tests message."""
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_tests",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    async def _handle_generate_single_test_message(self, message) -> None:
        """Handle generate_single_test message."""
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_single_test",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    async def _handle_generate_pom_message(self, message) -> None:
        """Handle generate_pom message."""
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_pom",
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
            f"ContractorAgent(state={self.state.value}, "
            f"active_tasks={len(self.active_tasks)}, "
            f"tests_generated={self.metrics['tests_generated']})"
        )
