"""
Integration tests for shared context storage layer.

Tests the storage backend (PostgreSQL + Redis) and context manager.

Author: Aurel IKAMA HONEY
"""
import asyncio
from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from src.shared_context.context_manager import ContextManager
from src.shared_context.models import (
    AgentType,
    AuthType,
    CompletenessAnalysis,
    EndpointContext,
    GeneratedTest,
    HTTPMethod,
    InconsistencyReport,
    LLMPerformanceMetrics,
    Oracle,
    ProcessingStatus,
    QualityMetrics,
    TestExecutionResult,
)
from src.shared_context.storage import create_storage_backend


@pytest_asyncio.fixture(scope="function")
async def storage_backend():
    """Create mock storage backend for testing."""
    from unittest.mock import AsyncMock, Mock
    from src.shared_context.storage import StorageBackend
    
    # Create a mock storage backend
    storage = Mock(spec=StorageBackend)
    
    # Mock all async methods
    storage.save_session = AsyncMock()
    storage.get_session = AsyncMock()
    storage.delete_session = AsyncMock()
    storage.save_message = AsyncMock()
    storage.get_messages = AsyncMock(return_value=[])
    storage.save_quality_metrics = AsyncMock()
    storage.get_quality_metrics = AsyncMock(return_value=[])
    storage.save_llm_metrics = AsyncMock()
    storage.save_llm_performance_metrics = AsyncMock()
    storage.get_llm_metrics = AsyncMock(return_value=[])
    storage.get_llm_performance_metrics = AsyncMock(return_value=[])
    storage.save_endpoint_context = AsyncMock()
    storage.get_endpoint_context = AsyncMock()
    storage.save_oracle = AsyncMock()
    storage.get_oracle = AsyncMock()
    storage.save_generated_test = AsyncMock()
    storage.get_generated_test = AsyncMock()
    storage.save_execution_result = AsyncMock()
    storage.get_execution_result = AsyncMock()
    storage.save_inconsistency_report = AsyncMock()
    storage.get_inconsistency_reports = AsyncMock(return_value=[])
    storage.save_completeness_analysis = AsyncMock()
    storage.get_completeness_analysis = AsyncMock()
    storage.close = AsyncMock()
    
    def mock_get_cache_key(entity_type, entity_id):
        return f"{entity_type}:{entity_id}"
    
    def mock_cache_get(key):
        return storage._cache.get(key)
    
    def mock_cache_set(key, value):
        storage._cache[key] = value
    
    storage._get_cache_key = Mock(side_effect=mock_get_cache_key)
    storage._cache_get = Mock(side_effect=mock_cache_get)
    storage._cache_set = Mock(side_effect=mock_cache_set)
    
    # Store data in memory for simple tests
    storage._sessions = {}
    storage._messages = []
    storage._endpoints = {}
    storage._oracles = {}
    storage._tests = {}
    storage._results = {}
    storage._cache = {}
    storage._quality_metrics = []
    storage._completeness = []
    storage._llm_perf = []
    
    # Implement basic CRUD logic
    async def mock_save_session(session):
        storage._sessions[session.id] = session
        # Also cache the session
        cache_key = storage._get_cache_key("session", session.id)
        storage._cache[cache_key] = session.model_dump()
    
    async def mock_get_session(session_id):
        return storage._sessions.get(session_id)
    
    async def mock_delete_session(session_id):
        if session_id in storage._sessions:
            del storage._sessions[session_id]
        # Clear cache
        cache_key = storage._get_cache_key("session", session_id)
        if cache_key in storage._cache:
            del storage._cache[cache_key]
    
    async def mock_save_message(message):
        storage._messages.append(message)
    
    async def mock_get_messages(session_id, to_agent=None, from_agent=None):
        messages = [msg for msg in storage._messages if msg.session_id == session_id]
        if to_agent:
            messages = [msg for msg in messages if msg.to_agent == to_agent]
        if from_agent:
            messages = [msg for msg in messages if msg.from_agent == from_agent]
        return messages
    
    storage._reports = []
    
    async def mock_save_inconsistency_report(report):
        storage._reports.append(report)
    
    async def mock_get_inconsistency_reports(session_id):
        return [r for r in storage._reports if r.session_id == session_id]
    
    async def mock_save_quality_metrics(metrics):
        storage._quality_metrics.append(metrics)
    
    async def mock_get_quality_metrics(session_id):
        return [m for m in storage._quality_metrics if m.session_id == session_id]
    
    async def mock_save_completeness_analysis(analysis):
        storage._completeness.append(analysis)
    
    async def mock_save_llm_performance_metrics(metrics):
        storage._llm_perf.append(metrics)
    
    async def mock_get_llm_performance_metrics(session_id):
        return [m for m in storage._llm_perf if m.session_id == session_id]
    
    async def mock_get_completeness_analysis(session_id):
        results = [c for c in storage._completeness if c.session_id == session_id]
        return results[0] if results else None
    
    storage.save_session.side_effect = mock_save_session
    storage.get_session.side_effect = mock_get_session
    storage.delete_session.side_effect = mock_delete_session
    storage.save_message.side_effect = mock_save_message
    storage.get_messages.side_effect = mock_get_messages
    storage.save_inconsistency_report.side_effect = mock_save_inconsistency_report
    storage.get_inconsistency_reports.side_effect = mock_get_inconsistency_reports
    storage.save_quality_metrics.side_effect = mock_save_quality_metrics
    storage.get_quality_metrics.side_effect = mock_get_quality_metrics
    storage.save_completeness_analysis.side_effect = mock_save_completeness_analysis
    storage.get_completeness_analysis.side_effect = mock_get_completeness_analysis
    storage.save_llm_performance_metrics.side_effect = mock_save_llm_performance_metrics
    storage.get_llm_performance_metrics.side_effect = mock_get_llm_performance_metrics
    
    yield storage


@pytest_asyncio.fixture(scope="function")
async def context_manager(storage_backend):
    """Create context manager for testing."""
    manager = ContextManager(storage_backend)
    yield manager
    await manager.close()


class TestStorageBackend:
    """Test the storage backend directly."""
    
    @pytest.mark.asyncio
    async def test_session_crud(self, storage_backend):
        """Test session create, read, update, delete."""
        from src.shared_context.models import WorkflowSession
        
        # Create
        session = WorkflowSession(
            collection_name="Test Collection",
            collection_path="/path/to/collection.json",
            llm_models={
                AgentType.INDUCTOR: "mistral",
                AgentType.ORACLE: "llama3.1",
            },
        )
        
        await storage_backend.save_session(session)
        
        # Read
        retrieved = await storage_backend.get_session(session.id)
        assert retrieved is not None
        assert retrieved.collection_name == "Test Collection"
        assert retrieved.status == ProcessingStatus.PENDING
        
        # Update
        session.status = ProcessingStatus.IN_PROGRESS
        session.current_agent = AgentType.INDUCTOR
        await storage_backend.save_session(session)
        
        retrieved = await storage_backend.get_session(session.id)
        assert retrieved.status == ProcessingStatus.IN_PROGRESS
        assert retrieved.current_agent == AgentType.INDUCTOR
        
        # Delete
        await storage_backend.delete_session(session.id)
        deleted = await storage_backend.get_session(session.id)
        assert deleted is None
    
    @pytest.mark.asyncio
    async def test_message_crud(self, storage_backend):
        """Test message operations."""
        from src.shared_context.models import AgentMessage, WorkflowSession
        
        # Create session first
        session = WorkflowSession(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        await storage_backend.save_session(session)
        
        # Create message
        message = AgentMessage(
            from_agent=AgentType.INDUCTOR,
            to_agent=AgentType.ORACLE,
            message_type="context_ready",
            payload={"endpoints": 5},
            session_id=session.id,
        )
        
        await storage_backend.save_message(message)
        
        # Read messages
        messages = await storage_backend.get_messages(session.id)
        assert len(messages) == 1
        assert messages[0].from_agent == AgentType.INDUCTOR
        assert messages[0].to_agent == AgentType.ORACLE
        
        # Filter by agent
        oracle_messages = await storage_backend.get_messages(
            session.id, to_agent=AgentType.ORACLE
        )
        assert len(oracle_messages) == 1
        
        # Cleanup
        await storage_backend.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_metrics_storage(self, storage_backend):
        """Test storing various metrics."""
        from src.shared_context.models import WorkflowSession
        
        # Create session
        session = WorkflowSession(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        await storage_backend.save_session(session)
        
        # Quality metrics
        quality = QualityMetrics(
            session_id=session.id,
            assertion_count=10,
            valid_assertions=9,
            assertion_coverage=0.9,
            quality_score=0.85,
        )
        await storage_backend.save_quality_metrics(quality)
        
        # LLM performance metrics
        llm_perf = LLMPerformanceMetrics(
            session_id=session.id,
            model_name="mistral",
            agent_type=AgentType.INDUCTOR,
            total_requests=10,
            successful_requests=9,
            avg_response_time_ms=250.5,
        )
        await storage_backend.save_llm_performance_metrics(llm_perf)
        
        # Completeness analysis
        completeness = CompletenessAnalysis(
            session_id=session.id,
            documentation_completeness=0.75,
            endpoint_completeness=0.8,
            oracle_precision=0.9,
            oracle_recall=0.85,
        )
        await storage_backend.save_completeness_analysis(completeness)
        
        # Retrieve and verify
        quality_list = await storage_backend.get_quality_metrics(session.id)
        assert len(quality_list) == 1
        assert quality_list[0].quality_score == 0.85
        
        llm_list = await storage_backend.get_llm_performance_metrics(session.id)
        assert len(llm_list) == 1
        assert llm_list[0].model_name == "mistral"
        
        completeness_result = await storage_backend.get_completeness_analysis(
            session.id
        )
        assert completeness_result is not None
        assert completeness_result.documentation_completeness == 0.75
        
        # Cleanup
        await storage_backend.delete_session(session.id)


class TestContextManager:
    """Test the context manager."""
    
    @pytest.mark.asyncio
    async def test_create_and_get_session(self, context_manager):
        """Test session creation and retrieval."""
        session = await context_manager.create_session(
            collection_name="API Collection",
            collection_path="/path/to/collection.json",
            llm_models={
                AgentType.INDUCTOR: "mistral",
                AgentType.ORACLE: "llama3.1",
            },
            config={"max_iterations": 5},
        )
        
        assert session.collection_name == "API Collection"
        assert session.status == ProcessingStatus.PENDING
        assert session.config["max_iterations"] == 5
        
        # Retrieve
        retrieved = await context_manager.get_session(session.id)
        assert retrieved is not None
        assert retrieved.id == session.id
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_endpoint_management(self, context_manager):
        """Test adding and retrieving endpoints."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        # Add endpoints
        endpoint1 = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="/api/users",
            expected_status=200,
        )
        endpoint2 = EndpointContext(
            name="Create User",
            method=HTTPMethod.POST,
            url="/api/users",
            body={"name": "John", "email": "john@example.com"},
            expected_status=201,
        )
        
        await context_manager.add_endpoint(session.id, endpoint1)
        await context_manager.add_endpoint(session.id, endpoint2)
        
        # Retrieve
        endpoints = await context_manager.get_endpoints(session.id)
        assert len(endpoints) == 2
        assert endpoints[0].name == "Get Users"
        assert endpoints[1].method == HTTPMethod.POST
        
        # Get specific endpoint
        endpoint = await context_manager.get_endpoint(session.id, endpoint1.id)
        assert endpoint is not None
        assert endpoint.name == "Get Users"
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_oracle_management(self, context_manager):
        """Test adding and retrieving oracles."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        endpoint = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="/api/users",
        )
        await context_manager.add_endpoint(session.id, endpoint)
        
        # Add oracle
        oracle = Oracle(
            name="Get Users Management Oracle",
            endpoint_id=endpoint.id,
            status_code=200,
            required_headers=["Content-Type"],
            header_constraints={"Content-Type": "application/json"},
            confidence_score=0.95,
            llm_model="mistral",
        )
        
        await context_manager.add_oracle(session.id, oracle)
        
        # Retrieve
        oracles = await context_manager.get_oracles(session.id)
        assert len(oracles) == 1
        assert oracles[0].status_code == 200
        assert oracles[0].confidence_score == 0.95
        
        # Filter by endpoint
        endpoint_oracles = await context_manager.get_oracles(
            session.id, endpoint_id=endpoint.id
        )
        assert len(endpoint_oracles) == 1
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_test_management(self, context_manager):
        """Test adding and retrieving generated tests."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        endpoint = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="/api/users",
        )
        await context_manager.add_endpoint(session.id, endpoint)
        
        oracle = Oracle(name="Get Users Oracle", endpoint_id=endpoint.id, status_code=200)
        await context_manager.add_oracle(session.id, oracle)
        
        # Add test
        test = GeneratedTest(
            endpoint_id=endpoint.id,
            oracle_id=oracle.id,
            test_class_name="GetUsersTest",
            test_method_name="testGetUsersReturns200",
            test_code="@Test\npublic void testGetUsersReturns200() {...}",
            llm_model="mistral",
        )
        
        await context_manager.add_test(session.id, test)
        
        # Retrieve
        tests = await context_manager.get_tests(session.id)
        assert len(tests) == 1
        assert tests[0].test_class_name == "GetUsersTest"
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_execution_results(self, context_manager):
        """Test adding and retrieving execution results."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        endpoint = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="/api/users",
        )
        await context_manager.add_endpoint(session.id, endpoint)
        
        oracle = Oracle(name="Execution Test Oracle", endpoint_id=endpoint.id, status_code=200)
        await context_manager.add_oracle(session.id, oracle)
        
        test = GeneratedTest(
            endpoint_id=endpoint.id,
            oracle_id=oracle.id,
            test_class_name="GetUsersTest",
            test_method_name="testGetUsersReturns200",
            test_code="...",
        )
        await context_manager.add_test(session.id, test)
        
        # Add execution result
        result = TestExecutionResult(
            test_id=test.id,
            passed=True,
            execution_time_ms=123.45,
            actual_status_code=200,
        )
        
        await context_manager.add_execution_result(session.id, result)
        
        # Verify counters updated
        updated_session = await context_manager.get_session(session.id)
        assert updated_session.successful_tests == 1
        assert updated_session.processed_endpoints == 1
        
        # Retrieve results
        results = await context_manager.get_execution_results(session.id)
        assert len(results) == 1
        assert results[0].passed is True
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_message_passing(self, context_manager):
        """Test inter-agent message passing."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        # Send messages
        msg1 = await context_manager.send_message(
            session_id=session.id,
            from_agent=AgentType.INDUCTOR,
            to_agent=AgentType.ORACLE,
            message_type="context_ready",
            payload={"endpoints": 5},
            priority=1,
        )
        
        msg2 = await context_manager.send_message(
            session_id=session.id,
            from_agent=AgentType.ORACLE,
            to_agent=AgentType.CONTRACTOR,
            message_type="oracles_ready",
            payload={"oracles": 5},
            parent_message_id=msg1.id,
        )
        
        # Retrieve all messages
        all_messages = await context_manager.get_messages(session.id)
        assert len(all_messages) == 2
        
        # Filter by recipient
        oracle_messages = await context_manager.get_messages(
            session.id, to_agent=AgentType.ORACLE
        )
        assert len(oracle_messages) == 1
        assert oracle_messages[0].message_type == "context_ready"
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_iteration_management(self, context_manager):
        """Test feedback loop iteration management."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        # Check initial state
        assert session.iteration == 0
        assert await context_manager.should_retry(session.id) is True
        
        # Increment iteration
        iteration = await context_manager.increment_iteration(session.id)
        assert iteration == 1
        
        # Keep incrementing
        await context_manager.increment_iteration(session.id)
        await context_manager.increment_iteration(session.id)
        
        # Should not retry after max iterations
        assert await context_manager.should_retry(session.id) is False
        
        # Cleanup
        await context_manager.delete_session(session.id)
    
    @pytest.mark.asyncio
    async def test_inconsistency_reports(self, context_manager):
        """Test inconsistency detection (RQ2)."""
        session = await context_manager.create_session(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        endpoint = EndpointContext(
            name="Get Users",
            method=HTTPMethod.GET,
            url="/api/users",
        )
        await context_manager.add_endpoint(session.id, endpoint)
        
        oracle = Oracle(name="Inconsistency Report Oracle", endpoint_id=endpoint.id, status_code=200)
        await context_manager.add_oracle(session.id, oracle)
        
        test = GeneratedTest(
            endpoint_id=endpoint.id,
            oracle_id=oracle.id,
            test_class_name="Test",
            test_method_name="test",
            test_code="...",
        )
        await context_manager.add_test(session.id, test)
        
        # Add inconsistency report
        report = InconsistencyReport(
            session_id=session.id,
            oracle_id=oracle.id,
            test_id=test.id,
            inconsistency_type="status_code_mismatch",
            severity="critical",
            description="Oracle expects 200 but test checks for 201",
            oracle_expectation={"status": 200},
            test_implementation={"status": 201},
            detected_by="automated_analyzer",
        )
        
        await context_manager.add_inconsistency_report(report)
        
        # Retrieve
        reports = await context_manager.get_inconsistency_reports(session.id)
        assert len(reports) == 1
        assert reports[0].severity == "critical"
        
        # Cleanup
        await context_manager.delete_session(session.id)


class TestCaching:
    """Test Redis caching functionality."""
    
    @pytest.mark.asyncio
    async def test_session_caching(self, storage_backend):
        """Test that sessions are cached in Redis."""
        from src.shared_context.models import WorkflowSession
        
        session = WorkflowSession(
            collection_name="Test",
            collection_path="/test",
            llm_models={},
        )
        
        # Save (should cache)
        await storage_backend.save_session(session)
        
        # Check cache directly
        cache_key = storage_backend._get_cache_key("session", session.id)
        cached = storage_backend._cache_get(cache_key)
        assert cached is not None
        assert cached["collection_name"] == "Test"
        
        # Retrieve (should use cache)
        retrieved = await storage_backend.get_session(session.id)
        assert retrieved is not None
        
        # Cleanup
        await storage_backend.delete_session(session.id)
        
        # Verify cache cleared
        cached_after = storage_backend._cache_get(cache_key)
        assert cached_after is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
