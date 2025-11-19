"""
Unit tests for ContractorAgent.

Tests code generation from oracles, template rendering,
variable mapping, Java formatting, and pom.xml generation.
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from agents.contractor import ContractorAgent
from agents.base_agent import AgentConfig
from shared_context import (
    ContextManager,
    EndpointContext,
    Oracle,
    GeneratedTest,
    AgentType,
    HTTPMethod,
    AuthType,
)
from orchestration import Task


@pytest.fixture
def context_manager():
    """Mock context manager."""
    return MagicMock(spec=ContextManager)


@pytest.fixture
def message_router():
    """Mock message router."""
    router = MagicMock()
    router.register = MagicMock()
    router.send = AsyncMock()
    return router


@pytest.fixture
def event_bus():
    """Mock event bus."""
    bus = MagicMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture
def task_queue():
    """Mock task queue."""
    queue = MagicMock()
    queue.submit = AsyncMock()
    return queue


@pytest.fixture
def agent_config():
    """Agent configuration."""
    return AgentConfig(
        agent_id=uuid4(),
        agent_type=AgentType.CONTRACTOR,
        name="contractor-agent",
        version="1.0.0",
        capabilities=["code_generation"],
        config={},
    )


@pytest.fixture
def sample_endpoint_context():
    """Sample endpoint context."""
    return EndpointContext(
        id=uuid4(),
        name="get-users",
        url="https://api.example.com/api/v1/users",
        method=HTTPMethod.GET,
        description="Get list of users",
        headers={"Content-Type": "application/json"},
        query_params={"limit": "10"},
        path_params=[],
        body=None,
        auth_type=AuthType.BEARER,
        auth_config={"token": "test_token"},
        response_examples=[
            {
                "status": 200,
                "body": {"users": [{"id": 1, "name": "John"}]},
            }
        ],
        tags=["users", "read"],
        extracted_at=datetime.utcnow(),
        extractor_agent="inductor-agent",
    )


@pytest.fixture
def sample_oracle():
    """Sample oracle."""
    return Oracle(
        id=uuid4(),
        endpoint_id=uuid4(),
        status_code=200,
        required_headers=["Content-Type"],
        header_constraints={"Content-Type": "application/json"},
        response_schema={
            "type": "object",
            "properties": {
                "users": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                        },
                    },
                },
            },
        },
        json_path_assertions=[
            {
                "path": "$.users",
                "type": "array",
                "constraints": {"minimum": 1},
            }
        ],
        business_rules=["Users array must not be empty"],
        confidence_score=0.9,
        quality_score=0.85,
        derived_at=datetime.utcnow(),
        llm_model="gpt-4",
        consensus_votes=3,
    )


class TestContractorAgentInitialization:
    """Test ContractorAgent initialization."""
    
    def test_initialization_with_defaults(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test agent initialization with default parameters."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        assert agent.agent_type == AgentType.CONTRACTOR
        assert agent.base_package == "generated"
        assert agent.output_dir == "./generated_tests"
        assert agent.jinja_env is not None
        assert agent.metrics["tests_generated"] == 0
        assert agent.metrics["lines_of_code"] == 0
        assert agent.metrics["assertions_count"] == 0
    
    def test_initialization_with_custom_params(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test agent initialization with custom parameters."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            templates_dir="/custom/templates",
            output_dir="/custom/output",
            base_package="com.custom.tests",
        )
        
        assert agent.templates_dir == "/custom/templates"
        assert agent.output_dir == "/custom/output"
        assert agent.base_package == "com.custom.tests"


class TestTemplateVariableBuilding:
    """Test template variable building."""
    
    def test_build_template_variables(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        sample_endpoint_context,
        sample_oracle,
    ):
        """Test building template variables from context and oracle."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Link oracle to context
        sample_oracle.endpoint_id = sample_endpoint_context.id
        
        variables = agent._build_template_variables(
            sample_endpoint_context, sample_oracle
        )
        
        # Check basic variables
        assert variables["package_name"] == "generated"
        assert "GetUsersTest" in variables["class_name"]
        assert "test" in variables["method_name"].lower()
        assert variables["http_method"] == "GET"
        assert variables["base_url"] == "https://api.example.com"
        assert "/api/v1/users" in variables["endpoint_path"]
        
        # Check oracle data
        assert variables["expected_status"] == 200
        assert variables["required_headers"] == ["Content-Type"]
        assert variables["response_schema"] == sample_oracle.response_schema
        assert variables["json_path_assertions"] == sample_oracle.json_path_assertions
        assert variables["business_rules"] == sample_oracle.business_rules
        
        # Check auth
        assert variables["auth_type"] == "bearer"
        assert "auth_token" in variables
    
    def test_generate_class_name(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        sample_endpoint_context,
    ):
        """Test Java class name generation."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        class_name = agent._generate_class_name(sample_endpoint_context)
        
        assert class_name.endswith("Test")
        assert "Get" in class_name
        assert "Users" in class_name
        assert class_name[0].isupper()
    
    def test_generate_method_name(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        sample_endpoint_context,
    ):
        """Test Java method name generation."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        method_name = agent._generate_method_name(sample_endpoint_context)
        
        assert method_name.startswith("test")
        assert method_name[0].islower()
        assert "users" in method_name.lower()


class TestURLSplitting:
    """Test URL splitting."""
    
    def test_split_full_url(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test splitting full URL."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        base_url, path = agent._split_url("https://api.example.com/api/v1/users")
        
        assert base_url == "https://api.example.com"
        assert path == "/api/v1/users"
    
    def test_split_relative_path(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test splitting relative path."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        base_url, path = agent._split_url("/api/v1/users")
        
        assert base_url == ""
        assert path == "/api/v1/users"


class TestAuthVariables:
    """Test authentication variables building."""
    
    def test_bearer_auth_variables(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test Bearer auth variables."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        context = EndpointContext(
            id=uuid4(),
            name="test",
            url="/test",
            method=HTTPMethod.GET,
            auth_type=AuthType.BEARER,
            auth_config={"token": "abc123"},
            extracted_at=datetime.utcnow(),
        )
        
        auth_vars = agent._build_auth_variables(context)
        
        assert "auth_token" in auth_vars
        assert auth_vars["auth_token"] == "abc123"
    
    def test_basic_auth_variables(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test Basic auth variables."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        context = EndpointContext(
            id=uuid4(),
            name="test",
            url="/test",
            method=HTTPMethod.GET,
            auth_type=AuthType.BASIC,
            auth_config={"username": "user", "password": "pass"},
            extracted_at=datetime.utcnow(),
        )
        
        auth_vars = agent._build_auth_variables(context)
        
        assert "auth_username" in auth_vars
        assert "auth_password" in auth_vars
        assert auth_vars["auth_username"] == "user"
        assert auth_vars["auth_password"] == "pass"
    
    def test_api_key_auth_variables(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test API Key auth variables."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        context = EndpointContext(
            id=uuid4(),
            name="test",
            url="/test",
            method=HTTPMethod.GET,
            auth_type=AuthType.API_KEY,
            auth_config={"header_name": "X-API-Key", "key": "secret"},
            extracted_at=datetime.utcnow(),
        )
        
        auth_vars = agent._build_auth_variables(context)
        
        assert "auth_header_name" in auth_vars
        assert "auth_api_key" in auth_vars
        assert auth_vars["auth_header_name"] == "X-API-Key"
        assert auth_vars["auth_api_key"] == "secret"


class TestJavaFormatting:
    """Test Java code formatting."""
    
    def test_format_removes_excessive_blank_lines(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test that formatting removes excessive blank lines."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        code = "line1\n\n\n\nline2\n\n\nline3"
        formatted = agent._format_java_code(code)
        
        # Should reduce to single blank lines
        assert "\n\n\n" not in formatted
        assert formatted.count("line1") == 1
        assert formatted.count("line2") == 1
        assert formatted.count("line3") == 1


class TestAssertionCounting:
    """Test assertion counting."""
    
    def test_count_assertions(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test counting assertions in test code."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        code = """
        assertEquals(200, response.statusCode());
        assertNotNull(response.body());
        assertTrue(users.size() > 0);
        response.then().body("users", notNullValue());
        """
        
        count = agent._count_assertions(code)
        
        assert count >= 4


@pytest.mark.asyncio
class TestCodeGeneration:
    """Test code generation from oracles."""
    
    async def test_generate_test_from_oracle(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        sample_endpoint_context,
        sample_oracle,
    ):
        """Test generating test from oracle."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Link oracle to context
        sample_oracle.endpoint_id = sample_endpoint_context.id
        
        generated_test = await agent._generate_test_from_oracle(
            sample_endpoint_context, sample_oracle
        )
        
        assert generated_test is not None
        assert isinstance(generated_test, GeneratedTest)
        assert generated_test.endpoint_id == sample_endpoint_context.id
        assert generated_test.oracle_id == sample_oracle.id
        assert len(generated_test.test_code) > 0
        assert "RestAssured" in generated_test.test_code or "import" in generated_test.test_code
        assert generated_test.test_class_name.endswith("Test")
    
    async def test_generate_single_test_task(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        sample_endpoint_context,
        sample_oracle,
    ):
        """Test generate_single_test task processing."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Link oracle
        sample_oracle.endpoint_id = sample_endpoint_context.id
        
        # Mock context manager methods
        context_manager.get_oracle = AsyncMock(return_value=sample_oracle)
        context_manager.get_endpoint_context = AsyncMock(
            return_value=sample_endpoint_context
        )
        context_manager.store_generated_test = AsyncMock()
        
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_single_test",
            session_id=uuid4(),
            payload={"oracle_id": str(sample_oracle.id)},
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "test_id" in result
        assert result["lines_of_code"] > 0
        assert result["assertions_count"] > 0
    
    async def test_generate_tests_from_multiple_oracles(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        sample_endpoint_context,
        sample_oracle,
    ):
        """Test generating tests from multiple oracles."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Create multiple oracles
        oracle1 = sample_oracle
        oracle1.endpoint_id = sample_endpoint_context.id
        
        oracle2 = Oracle(
            id=uuid4(),
            endpoint_id=sample_endpoint_context.id,
            status_code=404,
            required_headers=[],
            header_constraints={},
            response_schema={},
            json_path_assertions=[],
            business_rules=[],
            confidence_score=0.8,
            quality_score=0.75,
            derived_at=datetime.utcnow(),
        )
        
        # Mock context manager
        async def get_oracle_mock(oracle_id):
            if oracle_id == oracle1.id:
                return oracle1
            elif oracle_id == oracle2.id:
                return oracle2
            return None
        
        context_manager.get_oracle = AsyncMock(side_effect=get_oracle_mock)
        context_manager.get_endpoint_context = AsyncMock(
            return_value=sample_endpoint_context
        )
        context_manager.store_generated_test = AsyncMock()
        
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_tests",
            session_id=uuid4(),
            payload={
                "oracle_ids": [str(oracle1.id), str(oracle2.id)],
                "session_id": str(uuid4()),
            },
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["tests_generated"] == 2
        assert len(result["test_ids"]) == 2
        assert result["total_lines"] > 0
        assert result["total_assertions"] > 0


@pytest.mark.asyncio
class TestPomGeneration:
    """Test pom.xml generation."""
    
    async def test_generate_pom_with_defaults(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test pom.xml generation with default values."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_pom",
            session_id=uuid4(),
            payload={},
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "pom_content" in result
        assert "<groupId>com.generated</groupId>" in result["pom_content"]
        assert "<artifactId>api-tests</artifactId>" in result["pom_content"]
        assert "rest-assured" in result["pom_content"]
    
    async def test_generate_pom_with_custom_values(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test pom.xml generation with custom values."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_pom",
            session_id=uuid4(),
            payload={
                "group_id": "com.custom",
                "artifact_id": "custom-tests",
                "version": "2.0.0",
                "java_version": "17",
            },
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "<groupId>com.custom</groupId>" in result["pom_content"]
        assert "<artifactId>custom-tests</artifactId>" in result["pom_content"]
        assert "<version>2.0.0</version>" in result["pom_content"]


@pytest.mark.asyncio
class TestMessageHandlers:
    """Test message handlers."""
    
    async def test_handle_generate_tests_message(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test generate_tests message handler."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        message = MagicMock()
        message.session_id = uuid4()
        message.payload = {"oracle_ids": [str(uuid4())]}
        
        await agent._handle_generate_tests_message(message)
        
        task_queue.submit.assert_called_once()
        message_router.send.assert_called_once()


class TestAgentRepr:
    """Test agent string representation."""
    
    def test_repr(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test string representation."""
        agent = ContractorAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        repr_str = repr(agent)
        
        assert "ContractorAgent" in repr_str
        assert "state=" in repr_str
        assert "tests_generated=" in repr_str
