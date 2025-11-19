"""
Unit tests for OracleAgent.

Tests oracle derivation, multi-LLM consensus, quality validation,
and message handling.

Author: Aurel IKAMA HONEY
"""
import asyncio
import json
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from agents.oracle import OracleAgent
from agents.base_agent import AgentConfig
from shared_context import (
    AgentType,
    EndpointContext,
    HTTPMethod,
    AuthType,
    Oracle,
)
from orchestration import Task


@pytest.fixture
def context_manager():
    """Mock context manager."""
    manager = AsyncMock()
    manager.get_endpoint_context = AsyncMock()
    manager.store_oracle = AsyncMock()
    manager.get_oracle = AsyncMock()
    return manager


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
    bus = AsyncMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture
def task_queue():
    """Mock task queue."""
    queue = AsyncMock()
    queue.submit = AsyncMock()
    return queue


@pytest.fixture
def agent_config():
    """Agent configuration."""
    return AgentConfig(
        agent_type=AgentType.ORACLE,
        max_concurrent_tasks=3,
        task_timeout=180.0,
    )


@pytest.fixture
def llm_configs():
    """LLM configurations for consensus."""
    return [
        {
            "provider": "ollama",
            "model": "mistral",
            "base_url": "http://localhost:11434",
        },
        {
            "provider": "ollama",
            "model": "llama2",
            "base_url": "http://localhost:11434",
        },
    ]


@pytest.fixture
def sample_endpoint_context():
    """Sample endpoint context."""
    return EndpointContext(
        id=uuid4(),
        name="Get User",
        method=HTTPMethod.GET,
        url="/api/users/{id}",
        headers={"Accept": "application/json"},
        query_params={},
        path_params=["id"],
        body=None,
        auth_type=AuthType.BEARER,
        auth_config={"token": "test_token"},
        expected_status=200,
        expected_headers={"Content-Type": "application/json"},
        expected_response_schema={
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["id", "name", "email"]
        },
        description="Retrieve user by ID",
        tags=["users"],
        documentation_completeness=0.9,
    )


@pytest.fixture
def sample_oracle():
    """Sample oracle."""
    endpoint_id = uuid4()
    return Oracle(
        id=uuid4(),
        endpoint_id=endpoint_id,
        status_code=200,
        required_headers=["Content-Type", "X-Request-ID"],
        header_constraints={"Content-Type": "application/json"},
        response_schema={
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            }
        },
        json_path_assertions={
            "$.id": {"type": "integer", "minimum": 1}
        },
        business_rules=["User ID must be positive"],
        confidence_score=0.85,
        rationale="High agreement across models",
        llm_model="consensus_2_models",
    )


class TestOracleAgentInitialization:
    """Test OracleAgent initialization."""
    
    @patch("agents.oracle.LLMClientFactory")
    def test_agent_initialization_with_llm_configs(
        self, mock_factory, agent_config, context_manager, 
        message_router, event_bus, task_queue, llm_configs
    ):
        """Test agent initializes with LLM configurations."""
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        mock_factory.create_client.side_effect = [mock_client1, mock_client2]
        
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_configs=llm_configs,
            consensus_threshold=0.7,
        )
        
        assert agent.agent_type == AgentType.ORACLE
        assert len(agent.llm_clients) == 2
        assert agent.consensus_threshold == 0.7
        assert agent.metrics["oracles_generated"] == 0
    
    def test_agent_initialization_without_llm(
        self, agent_config, context_manager, message_router, event_bus, task_queue
    ):
        """Test agent initializes without LLM configs (fallback mode)."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_configs=None,
        )
        
        assert len(agent.llm_clients) == 0
        assert agent.consensus_threshold == 0.7  # Default


class TestOracleDerivation:
    """Test oracle derivation from endpoint contexts."""
    
    @pytest.mark.asyncio
    async def test_derive_oracles_from_contexts(
        self, agent_config, context_manager, message_router, 
        event_bus, task_queue, sample_endpoint_context
    ):
        """Test deriving oracles for multiple contexts."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_configs=None,  # Use fallback
        )
        
        # Mock context retrieval
        context_manager.get_endpoint_context.return_value = sample_endpoint_context
        
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="derive_oracles",
            session_id=uuid4(),
            payload={
                "context_ids": [str(sample_endpoint_context.id)],
                "session_id": str(uuid4()),
            }
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["oracles_generated"] == 1
        assert len(result["oracle_ids"]) == 1
        assert context_manager.store_oracle.called
        assert event_bus.publish.called
    
    @pytest.mark.asyncio
    async def test_derive_single_oracle(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue, sample_endpoint_context
    ):
        """Test deriving oracle for single context."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_configs=None,
        )
        
        context_manager.get_endpoint_context.return_value = sample_endpoint_context
        
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="derive_single_oracle",
            session_id=uuid4(),
            payload={"context_id": str(sample_endpoint_context.id)}
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "oracle_id" in result
        assert "confidence_score" in result
        assert context_manager.store_oracle.called
    
    @pytest.mark.asyncio
    async def test_derive_oracles_missing_context(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test handling missing context during oracle derivation."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        context_manager.get_endpoint_context.return_value = None
        
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="derive_oracles",
            session_id=uuid4(),
            payload={
                "context_ids": [str(uuid4())],
                "session_id": str(uuid4()),
            }
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["oracles_generated"] == 0
        assert len(result["failed_contexts"]) == 1


class TestMultiLLMConsensus:
    """Test multi-LLM consensus mechanism."""
    
    @pytest.mark.asyncio
    @patch("agents.oracle.LLMClientFactory")
    async def test_consensus_with_multiple_llms(
        self, mock_factory, agent_config, context_manager,
        message_router, event_bus, task_queue, 
        llm_configs, sample_endpoint_context
    ):
        """Test consensus mechanism with multiple LLM responses."""
        # Mock LLM clients
        mock_client1 = AsyncMock()
        mock_client2 = AsyncMock()
        
        llm_response_1 = """```json
{
  "status_code": 200,
  "required_headers": ["Content-Type", "X-Request-ID"],
  "header_constraints": {"Content-Type": "application/json"},
  "response_schema": {"type": "object"},
  "business_rules": ["User ID must be positive"],
  "rationale": "Standard REST response"
}
```"""
        
        llm_response_2 = """```json
{
  "status_code": 200,
  "required_headers": ["Content-Type"],
  "header_constraints": {"Content-Type": "application/json"},
  "response_schema": {"type": "object"},
  "business_rules": ["User ID must be positive"],
  "rationale": "Basic validation"
}
```"""
        
        mock_client1.generate = AsyncMock(return_value=llm_response_1)
        mock_client2.generate = AsyncMock(return_value=llm_response_2)
        
        mock_factory.create_client.side_effect = [mock_client1, mock_client2]
        
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_configs=llm_configs,
            consensus_threshold=0.5,  # 50% agreement
        )
        
        oracle = await agent._derive_oracle_with_consensus(sample_endpoint_context)
        
        assert oracle is not None
        assert oracle.status_code == 200  # Both agreed
        assert "Content-Type" in oracle.required_headers  # Both agreed
        assert oracle.confidence_score > 0.0
        assert agent.metrics["llm_calls"] == 2
    
    def test_vote_on_value(
        self, agent_config, context_manager, message_router, 
        event_bus, task_queue
    ):
        """Test voting on single value."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            consensus_threshold=0.6,
        )
        
        # Test with clear majority (>60%)
        values = [200, 200, 201]
        result = agent._vote_on_value(values, num_models=3)
        assert result == 200
        
        # Test without majority
        values = [200, 201, 202]
        result = agent._vote_on_value(values, num_models=3)
        assert result is None
    
    def test_vote_on_list(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test voting on list items."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            consensus_threshold=0.5,
        )
        
        items = ["Content-Type", "Content-Type", "X-Request-ID", "X-API-Key"]
        result = agent._vote_on_list(items, num_models=2)
        
        # Content-Type appears 2/2 = 100% (above threshold)
        assert "Content-Type" in result
        # Others appear 1/2 = 50% (at threshold)
        assert "X-Request-ID" in result


class TestPromptGeneration:
    """Test LLM prompt generation."""
    
    def test_build_oracle_prompt(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue, sample_endpoint_context
    ):
        """Test building oracle generation prompt."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        prompt = agent._build_oracle_prompt(sample_endpoint_context)
        
        assert "Get User" in prompt
        assert "GET" in prompt
        assert "/api/users/{id}" in prompt
        assert "application/json" in prompt
        assert "Status Code Validation" in prompt
        assert "Response Header Validation" in prompt
        assert "Business Rules" in prompt
    
    def test_parse_llm_oracle_response_json(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test parsing JSON oracle from LLM response."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        response = """```json
{
  "status_code": 200,
  "required_headers": ["Content-Type"],
  "business_rules": ["ID must be positive"]
}
```"""
        
        oracle_data = agent._parse_llm_oracle_response(response)
        
        assert oracle_data is not None
        assert oracle_data["status_code"] == 200
        assert "Content-Type" in oracle_data["required_headers"]
    
    def test_parse_llm_oracle_response_plain_json(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test parsing plain JSON (no markdown)."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        response = '{"status_code": 201, "required_headers": []}'
        
        oracle_data = agent._parse_llm_oracle_response(response)
        
        assert oracle_data is not None
        assert oracle_data["status_code"] == 201


class TestOracleQuality:
    """Test oracle quality validation."""
    
    @pytest.mark.asyncio
    async def test_validate_oracle_quality(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue, sample_oracle
    ):
        """Test validating oracle quality."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        context_manager.get_oracle.return_value = sample_oracle
        
        task = Task(
            agent_type=AgentType.ORACLE,
            task_type="validate_oracle_quality",
            session_id=uuid4(),
            payload={"oracle_id": str(sample_oracle.id)}
        )
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "quality_score" in result
        assert "is_valid" in result
        assert result["quality_score"] > 0.6
    
    def test_calculate_oracle_quality_high_quality(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue, sample_oracle
    ):
        """Test calculating quality for high-quality oracle."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        quality_score, issues = agent._calculate_oracle_quality(sample_oracle)
        
        assert quality_score > 0.7
        assert len(issues) == 0
    
    def test_calculate_oracle_quality_low_quality(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test calculating quality for low-quality oracle."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        # Create incomplete oracle
        incomplete_oracle = Oracle(
            endpoint_id=uuid4(),
            status_code=999,  # Invalid
            required_headers=[],
            response_schema=None,
            confidence_score=0.3,
        )
        
        quality_score, issues = agent._calculate_oracle_quality(incomplete_oracle)
        
        assert quality_score < 0.6
        assert len(issues) > 0
        assert "Invalid status code" in issues


class TestFallbackOracle:
    """Test fallback oracle generation."""
    
    def test_generate_fallback_oracle(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue, sample_endpoint_context
    ):
        """Test generating fallback oracle without LLM."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        oracle = agent._generate_fallback_oracle(sample_endpoint_context)
        
        assert oracle is not None
        assert oracle.endpoint_id == sample_endpoint_context.id
        assert oracle.status_code == 200
        assert oracle.confidence_score == 0.5  # Low confidence
        assert oracle.llm_model == "fallback"


class TestMessageHandlers:
    """Test message handling."""
    
    @pytest.mark.asyncio
    async def test_handle_derive_oracles_message(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test handling derive_oracles message."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        message = MagicMock()
        message.session_id = uuid4()
        message.payload = {"context_ids": [str(uuid4())]}
        
        await agent._handle_derive_oracles_message(message)
        
        assert task_queue.submit.called
        assert message_router.send.called


class TestAgentRepr:
    """Test agent string representation."""
    
    def test_agent_repr(
        self, agent_config, context_manager, message_router,
        event_bus, task_queue
    ):
        """Test agent __repr__."""
        agent = OracleAgent(
            config=agent_config,
            context_manager=context_manager,
            message_router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
            consensus_threshold=0.8,
        )
        
        repr_str = repr(agent)
        
        assert "OracleAgent" in repr_str
        assert "0.8" in repr_str
