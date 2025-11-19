"""
Unit tests for InductorAgent.

Author: Aurel IKAMA HONEY
"""
import asyncio
import json
from pathlib import Path
from uuid import uuid4, UUID
from unittest.mock import Mock, AsyncMock, patch, MagicMock

import pytest

from agents.inductor import InductorAgent
from agents.base_agent import AgentConfig, AgentState
from shared_context import (
    AgentType,
    EndpointContext,
    HTTPMethod,
    AuthType,
    ProcessingStatus,
)
from orchestration import (
    Task,
    TaskPriority,
    TaskStatus,
    InMemoryTaskQueue,
    MessageRouter,
    EventBus,
)
from parsers.bruno_models import (
    BrunoCollection,
    BrunoItem,
    BrunoRequest,
    BrunoParseResult,
)


@pytest.fixture
def context_manager():
    """Mock context manager."""
    manager = AsyncMock()
    manager.store_endpoint_context = AsyncMock(return_value=True)
    manager.get_endpoint_context = AsyncMock()
    manager.update_endpoint_context = AsyncMock(return_value=True)
    return manager


@pytest.fixture
def message_router():
    """Create message router."""
    return MessageRouter()


@pytest.fixture
def event_bus():
    """Create event bus."""
    return EventBus()


@pytest.fixture
def task_queue():
    """Create task queue."""
    return InMemoryTaskQueue()


@pytest.fixture
def agent_config():
    """Create agent configuration."""
    return AgentConfig(
        agent_type=AgentType.INDUCTOR,
        max_concurrent_tasks=3,
        task_timeout=60.0,
        retry_limit=2,
    )


@pytest.fixture
def llm_config():
    """LLM configuration."""
    return {
        "provider": "ollama",
        "model": "llama3.1:70b",
        "temperature": 0.2,
        "max_tokens": 2048,
    }


@pytest.fixture
async def inductor_agent(agent_config, context_manager, message_router, event_bus, task_queue, llm_config):
    """Create InductorAgent instance."""
    agent = InductorAgent(
        config=agent_config,
        context_manager=context_manager,
        router=message_router,
        event_bus=event_bus,
        task_queue=task_queue,
        llm_config=llm_config,
    )
    
    yield agent
    
    # Cleanup
    if agent.state == AgentState.RUNNING:
        await agent.stop()


@pytest.fixture
def sample_bruno_request():
    """Create a sample Bruno request."""
    return BrunoRequest(
        method="GET",
        url="https://api.example.com/users/{{userId}}",
        headers=[],
        params=[],
        body=None,
        auth=None,
        script=None,
    )


@pytest.fixture
def sample_parse_result(sample_bruno_request):
    """Create a sample parse result."""
    item = BrunoItem(
        name="Get User",
        type="http-request",
        request=sample_bruno_request,
        items=[],
    )
    
    collection = BrunoCollection(
        name="Test API",
        version="1.0.0",
        items=[item],
        type="collection",
    )
    
    return BrunoParseResult(
        collection=collection,
        total_requests=1,
        total_folders=0,
        endpoints=["https://api.example.com/users/{{userId}}"],
        methods=["GET"],
        has_authentication=False,
        has_documentation=False,
    )


class TestInductorAgentInitialization:
    """Test InductorAgent initialization."""
    
    def test_agent_initialization(self, inductor_agent):
        """Test that agent initializes correctly."""
        assert inductor_agent.agent_type == AgentType.INDUCTOR
        assert inductor_agent.state == AgentState.IDLE
        assert inductor_agent.parser is not None
    
    def test_agent_with_llm_config(self, agent_config, context_manager, message_router, event_bus, task_queue):
        """Test agent initialization with LLM config."""
        llm_config = {
            "provider": "ollama",
            "model": "llama3.1:70b",
        }
        
        with patch('agents.inductor.LLMClientFactory.create') as mock_create:
            mock_client = Mock()
            mock_create.return_value = mock_client
            
            agent = InductorAgent(
                config=agent_config,
                context_manager=context_manager,
                router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                llm_config=llm_config,
            )
            
            assert agent.llm_client == mock_client
            mock_create.assert_called_once()
    
    def test_agent_without_llm_config(self, agent_config, context_manager, message_router, event_bus, task_queue):
        """Test agent initialization without LLM."""
        agent = InductorAgent(
            config=agent_config,
            context_manager=context_manager,
            router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_config=None,
        )
        
        assert agent.llm_client is None


class TestEndpointExtraction:
    """Test endpoint extraction from Bruno collections."""
    
    @pytest.mark.asyncio
    async def test_extract_endpoints_from_parse_result(self, inductor_agent, sample_parse_result):
        """Test extracting endpoints from parse result."""
        endpoints = inductor_agent._extract_endpoints_from_parse_result(sample_parse_result)
        
        assert len(endpoints) == 1
        assert isinstance(endpoints[0], EndpointContext)
        assert endpoints[0].name == "Get User"
        assert endpoints[0].method == HTTPMethod.GET
        assert endpoints[0].url == "https://api.example.com/users/{{userId}}"
    
    def test_bruno_request_to_endpoint_context(self, inductor_agent, sample_bruno_request):
        """Test converting Bruno request to endpoint context."""
        endpoint = inductor_agent._bruno_request_to_endpoint_context(
            sample_bruno_request,
            "Get User"
        )
        
        assert endpoint.name == "Get User"
        assert endpoint.method == HTTPMethod.GET
        assert endpoint.url == "https://api.example.com/users/{{userId}}"
        assert endpoint.auth_type == AuthType.NONE
    
    def test_extract_headers(self, inductor_agent):
        """Test extracting headers from request."""
        from parsers.bruno_models import BrunoHeader
        
        request = BrunoRequest(
            method="GET",
            url="https://api.example.com/data",
            headers=[
                BrunoHeader(name="Authorization", value="Bearer token123", enabled=True),
                BrunoHeader(name="Content-Type", value="application/json", enabled=True),
                BrunoHeader(name="X-Disabled", value="value", enabled=False),
            ],
            params=[],
            body=None,
            auth=None,
            script=None,
        )
        
        endpoint = inductor_agent._bruno_request_to_endpoint_context(request, "Test")
        
        assert len(endpoint.headers) == 2
        assert endpoint.headers["Authorization"] == "Bearer token123"
        assert endpoint.headers["Content-Type"] == "application/json"
        assert "X-Disabled" not in endpoint.headers
    
    def test_extract_query_params(self, inductor_agent):
        """Test extracting query parameters."""
        from parsers.bruno_models import BrunoParam
        
        request = BrunoRequest(
            method="GET",
            url="https://api.example.com/search",
            headers=[],
            params=[
                BrunoParam(name="q", value="test", enabled=True),
                BrunoParam(name="limit", value="10", enabled=True),
                BrunoParam(name="disabled", value="value", enabled=False),
            ],
            body=None,
            auth=None,
            script=None,
        )
        
        endpoint = inductor_agent._bruno_request_to_endpoint_context(request, "Search")
        
        assert len(endpoint.query_params) == 2
        assert endpoint.query_params["q"] == "test"
        assert endpoint.query_params["limit"] == "10"
        assert "disabled" not in endpoint.query_params
    
    def test_extract_json_body(self, inductor_agent):
        """Test extracting JSON body."""
        from parsers.bruno_models import BrunoBody
        
        json_body = {"name": "John", "age": 30}
        
        request = BrunoRequest(
            method="POST",
            url="https://api.example.com/users",
            headers=[],
            params=[],
            body=BrunoBody(json=json_body),
            auth=None,
            script=None,
        )
        
        endpoint = inductor_agent._bruno_request_to_endpoint_context(request, "Create User")
        
        assert endpoint.body == json_body
        assert endpoint.body_schema is not None
        assert endpoint.body_schema["type"] == "object"


class TestAuthentication:
    """Test authentication extraction."""
    
    def test_extract_basic_auth(self, inductor_agent):
        """Test extracting basic authentication."""
        from parsers.bruno_models import BrunoAuth, BrunoBasicAuth
        
        request = BrunoRequest(
            method="GET",
            url="https://api.example.com/secure",
            headers=[],
            params=[],
            body=None,
            auth=BrunoAuth(
                mode="basic",
                basic=BrunoBasicAuth(username="user", password="pass"),
            ),
            script=None,
        )
        
        endpoint = inductor_agent._bruno_request_to_endpoint_context(request, "Secure")
        
        assert endpoint.auth_type == AuthType.BASIC
        assert "username" in endpoint.auth_config
    
    def test_extract_bearer_auth(self, inductor_agent):
        """Test extracting bearer token authentication."""
        from parsers.bruno_models import BrunoAuth, BrunoBearerAuth
        
        request = BrunoRequest(
            method="GET",
            url="https://api.example.com/secure",
            headers=[],
            params=[],
            body=None,
            auth=BrunoAuth(
                mode="bearer",
                bearer=BrunoBearerAuth(token="secret-token"),
            ),
            script=None,
        )
        
        endpoint = inductor_agent._bruno_request_to_endpoint_context(request, "Secure")
        
        assert endpoint.auth_type == AuthType.BEARER
        assert "token" in endpoint.auth_config


class TestDocumentationCompleteness:
    """Test documentation completeness calculation."""
    
    def test_completeness_minimal(self, inductor_agent):
        """Test completeness for minimal documentation."""
        request = BrunoRequest(
            method="GET",
            url="https://api.example.com/test",
            headers=[],
            params=[],
            body=None,
            auth=None,
            script=None,
        )
        
        completeness = inductor_agent._calculate_documentation_completeness(request)
        
        # Only URL present
        assert 0.0 < completeness < 1.0
    
    def test_completeness_full(self, inductor_agent):
        """Test completeness for full documentation."""
        from parsers.bruno_models import (
            BrunoHeader,
            BrunoBody,
            BrunoAuth,
            BrunoBasicAuth,
            BrunoScript,
        )
        
        request = BrunoRequest(
            method="POST",
            url="https://api.example.com/users",
            headers=[BrunoHeader(name="Content-Type", value="application/json", enabled=True)],
            params=[],
            body=BrunoBody(json={"name": "test"}),
            auth=BrunoAuth(mode="basic", basic=BrunoBasicAuth(username="user", password="pass")),
            script=BrunoScript(pre_request="console.log('test');", tests="pm.test('test', () => {});"),
        )
        
        completeness = inductor_agent._calculate_documentation_completeness(request)
        
        # All fields present
        assert completeness == 1.0


class TestTaskProcessing:
    """Test task processing."""
    
    @pytest.mark.asyncio
    async def test_process_extract_context_task(self, inductor_agent, context_manager, tmp_path):
        """Test processing extract_context task."""
        # Create a temporary Bruno collection file
        collection_data = {
            "name": "Test API",
            "version": "1.0.0",
            "type": "collection",
            "items": [
                {
                    "name": "Get User",
                    "type": "http-request",
                    "request": {
                        "method": "GET",
                        "url": "https://api.example.com/users/1",
                        "headers": [],
                        "params": [],
                    }
                }
            ]
        }
        
        collection_file = tmp_path / "test_collection.json"
        with open(collection_file, 'w') as f:
            json.dump(collection_data, f)
        
        session_id = str(uuid4())
        
        task = Task(
            task_id=uuid4(),
            task_type="extract_context",
            priority=TaskPriority.NORMAL,
            data={
                "collection_path": str(collection_file),
                "session_id": session_id,
                "enrich_with_llm": False,
            }
        )
        
        result = await inductor_agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["endpoints_extracted"] == 1
        assert result["contexts_stored"] == 1
        
        # Verify context was stored
        context_manager.store_endpoint_context.assert_called()
    
    @pytest.mark.asyncio
    async def test_process_parse_collection_task(self, inductor_agent, tmp_path):
        """Test processing parse_collection task."""
        collection_data = {
            "name": "Test API",
            "version": "1.0.0",
            "type": "collection",
            "items": []
        }
        
        collection_file = tmp_path / "test_collection.json"
        with open(collection_file, 'w') as f:
            json.dump(collection_data, f)
        
        task = Task(
            task_id=uuid4(),
            task_type="parse_collection",
            priority=TaskPriority.NORMAL,
            data={"collection_path": str(collection_file)}
        )
        
        result = await inductor_agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["collection_name"] == "Test API"
        assert result["total_requests"] == 0
    
    @pytest.mark.asyncio
    async def test_process_unsupported_task(self, inductor_agent):
        """Test processing unsupported task type."""
        task = Task(
            task_id=uuid4(),
            task_type="unsupported_task",
            priority=TaskPriority.NORMAL,
            data={}
        )
        
        with pytest.raises(ValueError, match="Unsupported task type"):
            await inductor_agent.process_task(task)


class TestLLMEnrichment:
    """Test LLM enrichment functionality."""
    
    @pytest.mark.asyncio
    async def test_enrich_endpoint_without_llm(self, agent_config, context_manager, message_router, event_bus, task_queue):
        """Test enrichment when LLM is not available."""
        agent = InductorAgent(
            config=agent_config,
            context_manager=context_manager,
            router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_config=None,
        )
        
        endpoint = EndpointContext(
            name="Test",
            method=HTTPMethod.GET,
            url="https://api.example.com/test",
        )
        
        enriched = await agent._enrich_endpoint_with_llm(endpoint)
        
        # Should return unchanged endpoint
        assert enriched == endpoint
        assert enriched.description is None
    
    @pytest.mark.asyncio
    async def test_enrich_endpoint_with_llm(self, inductor_agent):
        """Test enrichment with LLM."""
        # Mock LLM client
        mock_llm = Mock()
        mock_llm.generate = Mock(return_value='{"description": "Test endpoint", "expected_status": 200, "expected_headers": {"Content-Type": "application/json"}, "tags": ["test"]}')
        inductor_agent.llm_client = mock_llm
        
        endpoint = EndpointContext(
            name="Test",
            method=HTTPMethod.GET,
            url="https://api.example.com/test",
        )
        
        enriched = await inductor_agent._enrich_endpoint_with_llm(endpoint)
        
        assert enriched.description == "Test endpoint"
        assert enriched.expected_status == 200
        assert enriched.tags == ["test"]
        
        mock_llm.generate.assert_called_once()
    
    def test_build_enrichment_prompt(self, inductor_agent):
        """Test building enrichment prompt."""
        endpoint = EndpointContext(
            name="Get User",
            method=HTTPMethod.GET,
            url="https://api.example.com/users/1",
            headers={"Authorization": "Bearer token"},
        )
        
        prompt = inductor_agent._build_enrichment_prompt(endpoint)
        
        assert "Get User" in prompt
        assert "GET" in prompt
        assert "https://api.example.com/users/1" in prompt
        assert "Authorization" in prompt
    
    def test_parse_llm_response_json(self, inductor_agent):
        """Test parsing JSON response from LLM."""
        response = '{"description": "Test", "expected_status": 200}'
        
        result = inductor_agent._parse_llm_enrichment_response(response)
        
        assert result["description"] == "Test"
        assert result["expected_status"] == 200
    
    def test_parse_llm_response_markdown(self, inductor_agent):
        """Test parsing JSON in markdown code block."""
        response = '```json\n{"description": "Test", "expected_status": 200}\n```'
        
        result = inductor_agent._parse_llm_enrichment_response(response)
        
        assert result["description"] == "Test"
        assert result["expected_status"] == 200


class TestSchemaInference:
    """Test JSON schema inference."""
    
    def test_infer_object_schema(self, inductor_agent):
        """Test inferring schema from object."""
        data = {"name": "John", "age": 30}
        
        schema = inductor_agent._infer_schema_from_json(data)
        
        assert schema["type"] == "object"
        assert "properties" in schema
        assert schema["properties"]["name"]["type"] == "string"
        assert schema["properties"]["age"]["type"] == "number"
    
    def test_infer_array_schema(self, inductor_agent):
        """Test inferring schema from array."""
        data = [{"id": 1}, {"id": 2}]
        
        schema = inductor_agent._infer_schema_from_json(data)
        
        assert schema["type"] == "array"
        assert "items" in schema
        assert schema["items"]["type"] == "object"
    
    def test_infer_nested_schema(self, inductor_agent):
        """Test inferring nested schema."""
        data = {
            "user": {
                "name": "John",
                "address": {
                    "city": "NYC"
                }
            }
        }
        
        schema = inductor_agent._infer_schema_from_json(data)
        
        assert schema["type"] == "object"
        assert schema["properties"]["user"]["type"] == "object"
        assert schema["properties"]["user"]["properties"]["address"]["type"] == "object"


class TestAgentRepr:
    """Test agent string representation."""
    
    def test_agent_repr(self, inductor_agent):
        """Test agent __repr__."""
        repr_str = repr(inductor_agent)
        
        assert "InductorAgent" in repr_str
        assert "state=" in repr_str
        assert "active_tasks=" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
