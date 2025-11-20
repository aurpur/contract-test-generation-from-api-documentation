"""
Integration and End-to-End tests for Multi-Agent System.

Tests complete workflow: Inductor → Oracle → Contractor → Runner
Tests feedback loop: Runner → Contractor (regeneration on failures)
Tests multi-LLM consensus validation
Validates RQ1-RQ5 metrics

Author: Aurel IKAMA HONEY
"""
import asyncio
import json
import time
from pathlib import Path
from uuid import uuid4, UUID
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

import pytest
import pytest_asyncio

from agents.inductor import InductorAgent
from agents.oracle import OracleAgent
from agents.contractor import ContractorAgent
from agents.runner import RunnerAgent
from agents.base_agent import AgentConfig, AgentState
from parsers.bruno_models import (
    BrunoCollection,
    BrunoItem,
    BrunoRequest,
    BrunoHeader,
    BrunoParam,
    BrunoBody,
    BrunoAuth,
    BrunoScript,
    BrunoConfig,
)
from shared_context import (
    AgentType,
    EndpointContext,
    Oracle,
    GeneratedTest,
    TestExecutionResult,
    WorkflowSession,
    HTTPMethod,
    AuthType,
    ProcessingStatus,
    ContextManager,
)
from parsers.bruno_models import BrunoParseResult
from orchestration import (
    Task,
    TaskPriority,
    TaskStatus,
    InMemoryTaskQueue,
    MessageRouter,
    EventBus,
)


# ============================================================================
# Fixtures - System Components
# ============================================================================

@pytest.fixture
def context_manager():
    """Create context manager with mock storage for integration tests."""
    # Create a mock storage backend
    mock_storage = MagicMock()
    mock_storage.save_session = AsyncMock()
    mock_storage.get_session = AsyncMock(return_value=None)
    mock_storage.save_message = AsyncMock()
    mock_storage.get_messages = AsyncMock(return_value=[])
    mock_storage.close = AsyncMock()
    
    manager = ContextManager(mock_storage)
    # Store contexts and sessions in memory for testing
    manager._contexts = {}
    manager._sessions = {}
    manager._oracles = {}
    manager._generated_tests = {}
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
def agent_configs():
    """Create agent configurations."""
    return {
        "inductor": AgentConfig(
            agent_type=AgentType.INDUCTOR,
            max_concurrent_tasks=5,
        ),
        "oracle": AgentConfig(
            agent_type=AgentType.ORACLE,
            max_concurrent_tasks=3,
        ),
        "contractor": AgentConfig(
            agent_type=AgentType.CONTRACTOR,
            max_concurrent_tasks=3,
        ),
        "runner": AgentConfig(
            agent_type=AgentType.RUNNER,
            max_concurrent_tasks=2,
        ),
    }


@pytest_asyncio.fixture
async def multi_agent_system(
    agent_configs, context_manager, message_router, event_bus, task_queue
):
    """Create complete multi-agent system."""
    # Create agents
    inductor = InductorAgent(
        config=agent_configs["inductor"],
        context_manager=context_manager,
        router=message_router,
        event_bus=event_bus,
        task_queue=task_queue,
    )
    
    oracle = OracleAgent(
        config=agent_configs["oracle"],
        context_manager=context_manager,
        message_router=message_router,
        event_bus=event_bus,
        task_queue=task_queue,
    )
    
    contractor = ContractorAgent(
        config=agent_configs["contractor"],
        context_manager=context_manager,
        message_router=message_router,
        event_bus=event_bus,
        task_queue=task_queue,
    )
    
    runner = RunnerAgent(
        config=agent_configs["runner"],
        context_manager=context_manager,
        message_router=message_router,
        event_bus=event_bus,
        task_queue=task_queue,
        project_dir="/tmp/test-project",
    )
    
    system = {
        "inductor": inductor,
        "oracle": oracle,
        "contractor": contractor,
        "runner": runner,
        "context_manager": context_manager,
        "message_router": message_router,
        "event_bus": event_bus,
        "task_queue": task_queue,
    }
    
    yield system


# ============================================================================
# Fixtures - Test Data
# ============================================================================

@pytest.fixture
def sample_bruno_collection():
    """Create sample Bruno collection for testing."""
    return BrunoCollection(
        name="Test API",
        version="1.0.0",
        items=[
            BrunoItem(
                name="Get Users",
                type="http",
                request=BrunoRequest(
                    method="GET",
                    url="https://api.example.com/users",
                    headers=[],
                    params=[],
                    body=BrunoBody(),
                    auth=BrunoAuth(),
                    script=BrunoScript(),
                ),
            ),
            BrunoItem(
                name="Create User",
                type="http",
                request=BrunoRequest(
                    method="POST",
                    url="https://api.example.com/users",
                    headers=[
                        BrunoHeader(name="Content-Type", value="application/json", enabled=True),
                        BrunoHeader(name="Authorization", value="Bearer {{token}}", enabled=True),
                    ],
                    params=[],
                    body=BrunoBody(mode="json", json='{"name": "John Doe", "email": "john@example.com"}'),
                    auth=BrunoAuth(),
                    script=BrunoScript(),
                ),
            ),
        ],
        brunoConfig=BrunoConfig(name="Test API", version="1", type="collection"),
    )


@pytest.fixture
def sample_workflow_session():
    """Create sample workflow session."""
    return WorkflowSession(
        collection_name="Test API",
        endpoints_count=2,
        max_iterations=3,
    )


# ============================================================================
# Test Class: End-to-End Workflow
# ============================================================================

@pytest.mark.asyncio
class TestEndToEndWorkflow:
    """Test complete end-to-end workflow through all agents."""
    
    async def test_simple_workflow_inductor_to_oracle(
        self, multi_agent_system, sample_bruno_collection
    ):
        """Test workflow from Inductor to Oracle."""
        inductor = multi_agent_system["inductor"]
        oracle = multi_agent_system["oracle"]
        context_manager = multi_agent_system["context_manager"]
        
        # Step 1: Inductor extracts contexts
        task = Task(
            agent_type=AgentType.INDUCTOR,
            task_type="extract_context",
            session_id=uuid4(),
            payload={"collection": sample_bruno_collection.dict()},
        )
        
        inductor_result = await inductor.process_task(task)
        
        assert inductor_result["status"] == "success"
        assert inductor_result["contexts_extracted"] == 2
        assert len(inductor_result["context_ids"]) == 2
        
        # Verify contexts stored
        context_id = UUID(inductor_result["context_ids"][0])
        context = await context_manager.get_endpoint_context(context_id)
        assert context is not None
        assert context.method in [HTTPMethod.GET, HTTPMethod.POST]
        
        # Step 2: Oracle derives validation rules (mocked LLM)
        with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
            mock_llm.return_value = {
                "status_code": 200,
                "required_headers": ["Content-Type"],
                "response_schema": {"type": "array"},
                "confidence_score": 0.9,
            }
            
            oracle_task = Task(
                agent_type=AgentType.ORACLE,
                task_type="derive_oracle",
                session_id=uuid4(),
                payload={"context_id": str(context_id)},
            )
            
            oracle_result = await oracle.process_task(oracle_task)
            
            assert oracle_result["status"] == "success"
            assert "oracle_id" in oracle_result
            
            # Verify oracle stored
            oracle_obj = await context_manager.get_oracle(UUID(oracle_result["oracle_id"]))
            assert oracle_obj is not None
            assert oracle_obj.status_code == 200
    
    async def test_full_workflow_all_agents(
        self, multi_agent_system, sample_bruno_collection
    ):
        """Test complete workflow: Inductor → Oracle → Contractor → Runner."""
        inductor = multi_agent_system["inductor"]
        oracle = multi_agent_system["oracle"]
        contractor = multi_agent_system["contractor"]
        runner = multi_agent_system["runner"]
        context_manager = multi_agent_system["context_manager"]
        
        session_id = uuid4()
        
        # Step 1: Inductor extracts contexts
        inductor_task = Task(
            agent_type=AgentType.INDUCTOR,
            task_type="extract_context",
            session_id=session_id,
            payload={"collection": sample_bruno_collection.dict()},
        )
        
        inductor_result = await inductor.process_task(inductor_task)
        assert inductor_result["status"] == "success"
        context_id = UUID(inductor_result["context_ids"][0])
        
        # Step 2: Oracle derives validation (mocked LLM)
        with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
            mock_llm.return_value = {
                "status_code": 200,
                "required_headers": ["Content-Type"],
                "response_schema": {"type": "array", "items": {"type": "object"}},
                "json_path_assertions": [
                    {
                        "path": "$",
                        "constraint_type": "exists",
                        "expected_value": True,
                    }
                ],
                "confidence_score": 0.95,
            }
            
            oracle_task = Task(
                agent_type=AgentType.ORACLE,
                task_type="derive_oracle",
                session_id=session_id,
                payload={"context_id": str(context_id)},
            )
            
            oracle_result = await oracle.process_task(oracle_task)
            assert oracle_result["status"] == "success"
            oracle_id = UUID(oracle_result["oracle_id"])
        
        # Step 3: Contractor generates test code
        contractor_task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_single_test",
            session_id=session_id,
            payload={"oracle_id": str(oracle_id)},
        )
        
        contractor_result = await contractor.process_task(contractor_task)
        assert contractor_result["status"] == "success"
        assert "test_id" in contractor_result
        test_id = UUID(contractor_result["test_id"])
        
        # Verify generated test
        generated_test = await context_manager.get_generated_test(test_id)
        assert generated_test is not None
        assert generated_test.test_code is not None
        assert len(generated_test.test_code) > 0
        assert "RestAssured" in generated_test.test_code
        
        # Verify Gherkin scenario generated
        assert generated_test.feature_file_name is not None
        assert generated_test.feature_content is not None
        assert "Feature:" in generated_test.feature_content
        assert "Scenario:" in generated_test.feature_content
        
        # Step 4: Runner executes test (mocked Maven)
        with patch("agents.runner.MavenRunner.run_tests") as mock_maven:
            mock_maven.return_value = (
                True,
                "Tests run: 1, Failures: 0, Errors: 0, Skipped: 0",
                {"tests_run": 1, "failures": 0, "errors": 0, "tests_passed": 1},
            )
            
            with patch("agents.runner.MavenRunner.parse_junit_xml") as mock_parse:
                mock_parse.return_value = [
                    {
                        "name": generated_test.test_class_name,
                        "passed": True,
                        "time": 0.5,
                    }
                ]
                
                runner_task = Task(
                    agent_type=AgentType.RUNNER,
                    task_type="execute_single_test",
                    session_id=session_id,
                    payload={"test_id": str(test_id)},
                )
                
                runner_result = await runner.process_task(runner_task)
                assert runner_result["status"] == "success"
                assert runner_result["tests_passed"] == 1
    
    async def test_workflow_with_multiple_endpoints(
        self, multi_agent_system
    ):
        """Test workflow with multiple endpoints processed in parallel."""
        inductor = multi_agent_system["inductor"]
        context_manager = multi_agent_system["context_manager"]
        
        # Create collection with 5 endpoints
        collection = BrunoCollection(
            name="Large API",
            version="1.0.0",
            items=[
                BrunoItem(
                    name=f"Endpoint {i}",
                    request=BrunoRequest(
                        method=HTTPMethod.GET,
                        url=f"https://api.example.com/resource{i}",
                        headers={"Content-Type": "application/json"},
                    ),
                    description=f"Test endpoint {i}",
                )
                for i in range(5)
            ],
        )
        
        # Extract all contexts
        task = Task(
            agent_type=AgentType.INDUCTOR,
            task_type="extract_context",
            session_id=uuid4(),
            payload={"collection": collection.dict()},
        )
        
        result = await inductor.process_task(task)
        
        assert result["status"] == "success"
        assert result["contexts_extracted"] == 5
        assert len(result["context_ids"]) == 5
        
        # Verify all contexts stored
        for context_id_str in result["context_ids"]:
            context = await context_manager.get_endpoint_context(UUID(context_id_str))
            assert context is not None


# ============================================================================
# Test Class: Feedback Loop
# ============================================================================

@pytest.mark.asyncio
class TestFeedbackLoop:
    """Test feedback loop: failure detection → regeneration."""
    
    async def test_feedback_loop_on_test_failure(
        self, multi_agent_system, sample_bruno_collection
    ):
        """Test that Runner triggers Contractor regeneration on test failure."""
        contractor = multi_agent_system["contractor"]
        runner = multi_agent_system["runner"]
        context_manager = multi_agent_system["context_manager"]
        message_router = multi_agent_system["message_router"]
        
        session_id = uuid4()
        
        # Create mock endpoint context
        context = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="https://api.example.com/users",
            headers={"Content-Type": "application/json"},
            auth_type=AuthType.NONE,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        # Create mock oracle
        oracle = Oracle(
            endpoint_id=context.id,
            status_code=200,
            required_headers=["Content-Type"],
            response_schema={"type": "array"},
            confidence_score=0.9,
        )
        await context_manager.store_oracle(oracle)
        
        # Generate test
        generated_test = contractor._generate_test_from_oracle(context, oracle)
        await context_manager.store_generated_test(generated_test)
        
        # Mock Maven execution with failure
        with patch("agents.runner.MavenRunner.run_tests") as mock_maven:
            mock_maven.return_value = (
                False,
                "Tests run: 1, Failures: 1, Errors: 0, Skipped: 0",
                {"tests_run": 1, "failures": 1, "errors": 0, "tests_passed": 0},
            )
            
            with patch("agents.runner.MavenRunner.parse_junit_xml") as mock_parse:
                mock_parse.return_value = [
                    {
                        "name": generated_test.test_class_name,
                        "passed": False,
                        "time": 0.5,
                        "failure": {
                            "message": "Expected: 200 but was: 404",
                            "type": "AssertionError",
                            "text": "java.lang.AssertionError: Expected: 200 but was: 404",
                        },
                    }
                ]
                
                # Track regeneration messages
                regeneration_triggered = []
                
                async def capture_message(message):
                    if message.message_type == "regenerate_test":
                        regeneration_triggered.append(message)
                
                message_router.send = AsyncMock(side_effect=capture_message)
                
                # Execute test (should trigger regeneration)
                runner_task = Task(
                    agent_type=AgentType.RUNNER,
                    task_type="execute_single_test",
                    session_id=session_id,
                    payload={"test_id": str(generated_test.id)},
                )
                
                runner_result = await runner.process_task(runner_task)
                
                # Verify failure detected
                assert runner_result["tests_failed"] == 1
                
                # Verify regeneration triggered
                await asyncio.sleep(0.1)  # Allow async message sending
                assert len(regeneration_triggered) > 0
                regen_msg = regeneration_triggered[0]
                assert regen_msg.recipient == AgentType.CONTRACTOR
                assert "failure_context" in regen_msg.payload
    
    async def test_feedback_loop_max_retries(
        self, multi_agent_system
    ):
        """Test that feedback loop respects max retries."""
        runner = multi_agent_system["runner"]
        context_manager = multi_agent_system["context_manager"]
        
        # Create test with max retries
        context = EndpointContext(
            name="Flaky Test",
            method=HTTPMethod.GET,
            url="https://api.example.com/flaky",
            auth_type=AuthType.NONE,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        oracle = Oracle(
            endpoint_id=context.id,
            status_code=200,
            confidence_score=0.8,
        )
        await context_manager.store_oracle(oracle)
        
        generated_test = GeneratedTest(
            endpoint_id=context.id,
            oracle_id=oracle.id,
            test_class_name="FlakyTest",
            test_method_name="testFlaky",
            test_code="// test code",
        )
        await context_manager.store_generated_test(generated_test)
        
        # Mock repeated failures
        with patch("agents.runner.MavenRunner.run_tests") as mock_maven:
            mock_maven.return_value = (
                False,
                "Tests run: 1, Failures: 1",
                {"tests_run": 1, "failures": 1, "tests_passed": 0},
            )
            
            with patch("agents.runner.MavenRunner.parse_junit_xml") as mock_parse:
                mock_parse.return_value = [
                    {"name": "FlakyTest", "passed": False, "time": 0.5}
                ]
                
                # Execute multiple times (should stop after max_retries)
                for i in range(runner.max_retries + 2):
                    result = await runner._execute_single_test(
                        generated_test.id, uuid4()
                    )
                    
                    # Check if regeneration still triggered
                    execution_result = await context_manager.get_test_execution_result(
                        result["execution_result_id"]
                    )
                    
                    if i >= runner.max_retries:
                        # Should not trigger after max retries
                        assert execution_result.retry_count >= runner.max_retries


# ============================================================================
# Test Class: Multi-LLM Consensus
# ============================================================================

@pytest.mark.asyncio
class TestMultiLLMConsensus:
    """Test multi-LLM consensus validation in OracleAgent."""
    
    async def test_consensus_with_agreement(
        self, multi_agent_system
    ):
        """Test oracle generation with LLM consensus (all agree)."""
        oracle = multi_agent_system["oracle"]
        context_manager = multi_agent_system["context_manager"]
        
        # Create endpoint context
        context = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="https://api.example.com/users",
            auth_type=AuthType.NONE,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        # Mock multiple LLM responses (all agree)
        llm_responses = [
            {
                "status_code": 200,
                "required_headers": ["Content-Type"],
                "response_schema": {"type": "array"},
                "confidence_score": 0.9,
            },
            {
                "status_code": 200,
                "required_headers": ["Content-Type"],
                "response_schema": {"type": "array"},
                "confidence_score": 0.95,
            },
            {
                "status_code": 200,
                "required_headers": ["Content-Type"],
                "response_schema": {"type": "array"},
                "confidence_score": 0.92,
            },
        ]
        
        with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
            mock_llm.side_effect = llm_responses
            
            task = Task(
                agent_type=AgentType.ORACLE,
                task_type="derive_oracle",
                session_id=uuid4(),
                payload={
                    "context_id": str(context.id),
                    "use_consensus": True,
                    "llm_models": ["gpt-4", "claude-3", "gemini-pro"],
                },
            )
            
            result = await oracle.process_task(task)
            
            assert result["status"] == "success"
            assert "oracle_id" in result
            assert result.get("consensus_achieved") == True
            
            # Verify oracle has high confidence due to consensus
            oracle_obj = await context_manager.get_oracle(UUID(result["oracle_id"]))
            assert oracle_obj.confidence_score >= 0.9
    
    async def test_consensus_with_disagreement(
        self, multi_agent_system
    ):
        """Test oracle generation with LLM disagreement."""
        oracle = multi_agent_system["oracle"]
        context_manager = multi_agent_system["context_manager"]
        
        context = EndpointContext(
            name="Ambiguous Endpoint",
            method=HTTPMethod.POST,
            url="https://api.example.com/action",
            auth_type=AuthType.BEARER,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        # Mock LLM responses with disagreement
        llm_responses = [
            {"status_code": 200, "confidence_score": 0.7},
            {"status_code": 201, "confidence_score": 0.8},
            {"status_code": 200, "confidence_score": 0.6},
        ]
        
        with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
            mock_llm.side_effect = llm_responses
            
            task = Task(
                agent_type=AgentType.ORACLE,
                task_type="derive_oracle",
                session_id=uuid4(),
                payload={
                    "context_id": str(context.id),
                    "use_consensus": True,
                    "llm_models": ["gpt-4", "claude-3", "gemini-pro"],
                },
            )
            
            result = await oracle.process_task(task)
            
            # Should still generate oracle but with lower confidence
            assert result["status"] == "success"
            assert result.get("consensus_achieved") == False
            
            oracle_obj = await context_manager.get_oracle(UUID(result["oracle_id"]))
            # Confidence should reflect disagreement
            assert oracle_obj.confidence_score < 0.8


# ============================================================================
# Test Class: Performance Benchmarking
# ============================================================================

@pytest.mark.asyncio
class TestPerformanceBenchmarking:
    """Test system performance and scalability."""
    
    async def test_throughput_inductor(
        self, multi_agent_system
    ):
        """Benchmark Inductor throughput (contexts/second)."""
        inductor = multi_agent_system["inductor"]
        
        # Create large collection (50 endpoints)
        collection = BrunoCollection(
            name="Large Collection",
            version="1.0.0",
            items=[
                BrunoItem(
                    name=f"Endpoint {i}",
                    request=BrunoRequest(
                        method=HTTPMethod.GET,
                        url=f"https://api.example.com/resource{i}",
                    ),
                )
                for i in range(50)
            ],
        )
        
        start_time = time.time()
        
        task = Task(
            agent_type=AgentType.INDUCTOR,
            task_type="extract_context",
            session_id=uuid4(),
            payload={"collection": collection.dict()},
        )
        
        result = await inductor.process_task(task)
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = result["contexts_extracted"] / duration
        
        # Benchmark: should process at least 10 contexts/second
        assert throughput >= 10.0
        assert result["contexts_extracted"] == 50
    
    async def test_end_to_end_latency(
        self, multi_agent_system
    ):
        """Measure end-to-end latency for complete workflow."""
        inductor = multi_agent_system["inductor"]
        oracle = multi_agent_system["oracle"]
        contractor = multi_agent_system["contractor"]
        
        collection = BrunoCollection(
            name="Single Endpoint",
            version="1.0.0",
            items=[
                BrunoItem(
                    name="Test Endpoint",
                    request=BrunoRequest(
                        method=HTTPMethod.GET,
                        url="https://api.example.com/test",
                    ),
                )
            ],
        )
        
        session_id = uuid4()
        start_time = time.time()
        
        # Step 1: Extract context
        inductor_task = Task(
            agent_type=AgentType.INDUCTOR,
            task_type="extract_context",
            session_id=session_id,
            payload={"collection": collection.dict()},
        )
        inductor_result = await inductor.process_task(inductor_task)
        context_id = UUID(inductor_result["context_ids"][0])
        
        # Step 2: Derive oracle (mocked)
        with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
            mock_llm.return_value = {
                "status_code": 200,
                "confidence_score": 0.9,
            }
            
            oracle_task = Task(
                agent_type=AgentType.ORACLE,
                task_type="derive_oracle",
                session_id=session_id,
                payload={"context_id": str(context_id)},
            )
            oracle_result = await oracle.process_task(oracle_task)
            oracle_id = UUID(oracle_result["oracle_id"])
        
        # Step 3: Generate test
        contractor_task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_single_test",
            session_id=session_id,
            payload={"oracle_id": str(oracle_id)},
        )
        await contractor.process_task(contractor_task)
        
        end_time = time.time()
        latency = end_time - start_time
        
        # Benchmark: end-to-end should complete within 5 seconds (mocked LLM)
        assert latency < 5.0
    
    async def test_concurrent_processing(
        self, multi_agent_system
    ):
        """Test concurrent processing of multiple tasks."""
        inductor = multi_agent_system["inductor"]
        
        # Create 10 collections to process concurrently
        collections = [
            BrunoCollection(
                name=f"Collection {i}",
                version="1.0.0",
                items=[
                    BrunoItem(
                        name=f"Endpoint {j}",
                        request=BrunoRequest(
                            method=HTTPMethod.GET,
                            url=f"https://api{i}.example.com/resource{j}",
                        ),
                    )
                    for j in range(5)
                ],
            )
            for i in range(10)
        ]
        
        start_time = time.time()
        
        # Process all collections concurrently
        tasks = [
            inductor.process_task(
                Task(
                    agent_type=AgentType.INDUCTOR,
                    task_type="extract_context",
                    session_id=uuid4(),
                    payload={"collection": collection.dict()},
                )
            )
            for collection in collections
        ]
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Verify all succeeded
        assert all(r["status"] == "success" for r in results)
        assert sum(r["contexts_extracted"] for r in results) == 50
        
        # Concurrent should be faster than sequential
        # (rough estimate: should complete in less than 2x sequential time)
        assert duration < 10.0


# ============================================================================
# Test Class: RQ Validation (Preliminary)
# ============================================================================

@pytest.mark.asyncio
class TestRQValidation:
    """Preliminary validation of Research Questions (RQ1-RQ5)."""
    
    async def test_rq1_oracle_precision_basic(
        self, multi_agent_system
    ):
        """Test RQ1: Basic oracle precision measurement."""
        oracle = multi_agent_system["oracle"]
        context_manager = multi_agent_system["context_manager"]
        
        # Create endpoint with known expected oracle
        context = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="https://api.example.com/users",
            description="Returns list of users",
            auth_type=AuthType.NONE,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        # Expected oracle (ground truth)
        expected_status = 200
        expected_headers = ["Content-Type"]
        
        # Generate oracle
        with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
            mock_llm.return_value = {
                "status_code": 200,
                "required_headers": ["Content-Type"],
                "response_schema": {"type": "array"},
                "confidence_score": 0.9,
            }
            
            task = Task(
                agent_type=AgentType.ORACLE,
                task_type="derive_oracle",
                session_id=uuid4(),
                payload={"context_id": str(context.id)},
            )
            
            result = await oracle.process_task(task)
            oracle_obj = await context_manager.get_oracle(UUID(result["oracle_id"]))
        
        # Measure precision (simplified)
        status_correct = oracle_obj.status_code == expected_status
        headers_correct = set(oracle_obj.required_headers) == set(expected_headers)
        
        precision = (status_correct + headers_correct) / 2
        
        # Should achieve high precision
        assert precision >= 0.8
    
    async def test_rq2_coherence_oracle_code(
        self, multi_agent_system
    ):
        """Test RQ2: Coherence between oracle and generated code."""
        contractor = multi_agent_system["contractor"]
        context_manager = multi_agent_system["context_manager"]
        
        # Create context and oracle
        context = EndpointContext(
            name="Create User",
            method=HTTPMethod.POST,
            url="https://api.example.com/users",
            auth_type=AuthType.BEARER,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        oracle = Oracle(
            endpoint_id=context.id,
            status_code=201,
            required_headers=["Location", "Content-Type"],
            response_schema={"type": "object", "properties": {"id": {"type": "string"}}},
            confidence_score=0.95,
        )
        await context_manager.store_oracle(oracle)
        
        # Generate test
        task = Task(
            agent_type=AgentType.CONTRACTOR,
            task_type="generate_single_test",
            session_id=uuid4(),
            payload={"oracle_id": str(oracle.id)},
        )
        
        result = await contractor.process_task(task)
        generated_test = await context_manager.get_generated_test(
            UUID(result["test_id"])
        )
        
        # Check coherence: code should contain oracle assertions
        test_code = generated_test.test_code
        assert "201" in test_code  # Status code
        assert "Location" in test_code  # Required header
        assert "Content-Type" in test_code
        
        # Check Gherkin coherence
        feature_content = generated_test.feature_content
        assert "201" in feature_content
        assert "Location" in feature_content or "Content-Type" in feature_content
    
    async def test_rq3_code_quality_metrics(
        self, multi_agent_system
    ):
        """Test RQ3: Generated code quality metrics."""
        contractor = multi_agent_system["contractor"]
        context_manager = multi_agent_system["context_manager"]
        
        context = EndpointContext(
            name="Get User",
            method=HTTPMethod.GET,
            url="https://api.example.com/users/{id}",
            auth_type=AuthType.NONE,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        oracle = Oracle(
            endpoint_id=context.id,
            status_code=200,
            required_headers=["Content-Type"],
            response_schema={"type": "object"},
            json_path_assertions=[
                {"path": "$.id", "constraint_type": "exists", "expected_value": True},
                {"path": "$.name", "constraint_type": "type", "expected_value": "string"},
            ],
            confidence_score=0.9,
        )
        await context_manager.store_oracle(oracle)
        
        # Generate test
        generated_test = contractor._generate_test_from_oracle(context, oracle)
        
        # Quality metrics
        lines_of_code = len(generated_test.test_code.split("\n"))
        assertions_count = contractor._count_assertions(generated_test.test_code)
        
        # Quality criteria
        assert lines_of_code > 20  # Should be substantial
        assert lines_of_code < 200  # Should not be too verbose
        assert assertions_count >= 3  # Should have multiple assertions
        assert "RestAssured" in generated_test.test_code  # Should use correct framework
        assert "@Test" in generated_test.test_code  # Should have test annotation
    
    async def test_rq4_llm_comparison_basic(
        self, multi_agent_system
    ):
        """Test RQ4: Basic LLM comparison (mocked)."""
        oracle = multi_agent_system["oracle"]
        context_manager = multi_agent_system["context_manager"]
        
        context = EndpointContext(
            name="Test Endpoint",
            method=HTTPMethod.GET,
            url="https://api.example.com/test",
            auth_type=AuthType.NONE,
        )
        await context_manager.add_endpoint(session_id=session_id, endpoint=context)
        
        # Simulate different LLM responses
        llm_results = {}
        
        for llm_name, response in [
            ("gpt-4", {"status_code": 200, "confidence_score": 0.95}),
            ("claude-3", {"status_code": 200, "confidence_score": 0.92}),
            ("gemini-pro", {"status_code": 200, "confidence_score": 0.88}),
        ]:
            with patch("agents.oracle.OracleAgent._call_llm") as mock_llm:
                mock_llm.return_value = response
                
                task = Task(
                    agent_type=AgentType.ORACLE,
                    task_type="derive_oracle",
                    session_id=uuid4(),
                    payload={
                        "context_id": str(context.id),
                        "llm_model": llm_name,
                    },
                )
                
                result = await oracle.process_task(task)
                oracle_obj = await context_manager.get_oracle(UUID(result["oracle_id"]))
                
                llm_results[llm_name] = {
                    "confidence": oracle_obj.confidence_score,
                    "status_code": oracle_obj.status_code,
                }
        
        # All LLMs should produce results
        assert len(llm_results) == 3
        
        # Compare confidence scores
        confidences = [r["confidence"] for r in llm_results.values()]
        assert all(c > 0.8 for c in confidences)
    
    async def test_rq5_completeness_impact(
        self, multi_agent_system
    ):
        """Test RQ5: Impact of documentation completeness."""
        inductor = multi_agent_system["inductor"]
        
        # Complete documentation
        complete_item = BrunoItem(
            name="Complete Endpoint",
            request=BrunoRequest(
                method=HTTPMethod.GET,
                url="https://api.example.com/complete",
                headers={"Content-Type": "application/json"},
                params={"limit": "10"},
            ),
            description="Well-documented endpoint with full details",
        )
        
        # Incomplete documentation
        incomplete_item = BrunoItem(
            name="Incomplete Endpoint",
            request=BrunoRequest(
                method=HTTPMethod.GET,
                url="https://api.example.com/incomplete",
            ),
            description=None,
        )
        
        # Extract contexts
        complete_collection = BrunoCollection(
            name="Complete", version="1.0.0", items=[complete_item]
        )
        incomplete_collection = BrunoCollection(
            name="Incomplete", version="1.0.0", items=[incomplete_item]
        )
        
        complete_result = await inductor.process_task(
            Task(
                agent_type=AgentType.INDUCTOR,
                task_type="extract_context",
                session_id=uuid4(),
                payload={"collection": complete_collection.dict()},
            )
        )
        
        incomplete_result = await inductor.process_task(
            Task(
                agent_type=AgentType.INDUCTOR,
                task_type="extract_context",
                session_id=uuid4(),
                payload={"collection": incomplete_collection.dict()},
            )
        )
        
        # Both should succeed but with different quality metrics
        assert complete_result["status"] == "success"
        assert incomplete_result["status"] == "success"
        
        # Complete should have more extracted information
        # (This is a simplified check; full RQ5 needs more metrics)
        assert complete_result["contexts_extracted"] == 1
        assert incomplete_result["contexts_extracted"] == 1
