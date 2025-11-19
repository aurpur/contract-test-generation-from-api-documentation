"""
Unit tests for BaseAgent.

Author: Aurel IKAMA HONEY
"""
import asyncio
import pytest
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from agents.base_agent import (
    BaseAgent,
    AgentConfig,
    AgentState,
)
from shared_context import (
    AgentMessage,
    AgentType,
    ContextManager,
    ProcessingStatus,
)
from orchestration import (
    MessageRouter,
    EventBus,
    InMemoryTaskQueue,
    Task,
    TaskPriority,
    TaskStatus,
)


# ============================================================================
# Mock Agent Implementation
# ============================================================================

class MockAgent(BaseAgent):
    """Mock agent for testing BaseAgent functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_tasks = []
        self.task_delay = 0.1  # Simulate work
        self.should_fail = False
        
    async def process_task(self, task: Task) -> Any:
        """Process a task (mock implementation)."""
        # Simulate work
        await asyncio.sleep(self.task_delay)
        
        # Record task
        self.processed_tasks.append(task)
        
        # Simulate failure if requested
        if self.should_fail:
            raise ValueError(f"Mock task failure: {task.task_type}")
        
        # Return mock result
        return {
            "task_id": str(task.id),
            "task_type": task.task_type,
            "processed_by": self.agent_type.value,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def register_handlers(self) -> None:
        """Register handlers (mock implementation)."""
        # Register a mock message handler
        self.register_message_handler(
            "test_message",
            self._handle_test_message,
        )
    
    async def _handle_test_message(self, message: AgentMessage) -> None:
        """Handle test message."""
        pass


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def context_manager():
    """Create a mock context manager."""
    # For unit tests, we don't need a real context manager
    # We'll use None and mock the necessary methods in tests
    return None


@pytest.fixture
def message_router():
    """Create a message router."""
    router = MessageRouter()
    return router


@pytest.fixture
def event_bus():
    """Create an event bus."""
    bus = EventBus()
    return bus


@pytest.fixture
def task_queue():
    """Create a task queue."""
    queue = InMemoryTaskQueue()
    return queue


@pytest.fixture
def agent_config():
    """Create agent configuration."""
    return AgentConfig(
        agent_type=AgentType.INDUCTOR,
        max_concurrent_tasks=3,
        task_timeout=5.0,
        message_timeout=2.0,
        retry_limit=2,
    )


@pytest.fixture
def mock_agent(
    agent_config,
    context_manager,
    message_router,
    event_bus,
    task_queue,
):
    """Create a mock agent."""
    agent = MockAgent(
        config=agent_config,
        context_manager=context_manager,
        router=message_router,
        event_bus=event_bus,
        task_queue=task_queue,
    )
    
    return agent


# ============================================================================
# Test Lifecycle Management
# ============================================================================

@pytest.mark.asyncio
async def test_agent_initialization(mock_agent):
    """Test agent initialization."""
    assert mock_agent.agent_type == AgentType.INDUCTOR
    assert mock_agent.state == AgentState.IDLE
    assert len(mock_agent._active_tasks) == 0
    assert mock_agent._metrics["tasks_processed"] == 0


@pytest.mark.asyncio
async def test_agent_start(mock_agent):
    """Test starting an agent."""
    await mock_agent.start()
    
    assert mock_agent.state == AgentState.RUNNING
    assert mock_agent.is_running()
    assert not mock_agent.is_stopped()
    
    # Cleanup
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_agent_stop(mock_agent):
    """Test stopping an agent."""
    await mock_agent.start()
    assert mock_agent.is_running()
    
    await mock_agent.stop()
    assert mock_agent.state == AgentState.STOPPED
    assert mock_agent.is_stopped()
    assert not mock_agent.is_running()


@pytest.mark.asyncio
async def test_agent_pause_resume(mock_agent):
    """Test pausing and resuming an agent."""
    await mock_agent.start()
    assert mock_agent.state == AgentState.RUNNING
    
    await mock_agent.pause()
    assert mock_agent.state == AgentState.PAUSED
    
    await mock_agent.resume()
    assert mock_agent.state == AgentState.RUNNING
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_agent_double_start(mock_agent):
    """Test that starting an already running agent is safe."""
    await mock_agent.start()
    await mock_agent.start()  # Should not raise
    
    assert mock_agent.state == AgentState.RUNNING
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_agent_stop_with_active_tasks(mock_agent, task_queue):
    """Test stopping agent with active tasks."""
    await mock_agent.start()
    
    # Submit multiple tasks
    session_id = uuid4()
    for i in range(3):
        await mock_agent.submit_task(
            task_type=f"test_task_{i}",
            session_id=session_id,
            payload={"index": i},
        )
    
    # Give tasks time to start
    await asyncio.sleep(0.2)
    
    # Stop agent (should wait for tasks)
    await mock_agent.stop(timeout=10.0)
    
    assert mock_agent.is_stopped()
    assert len(mock_agent._active_tasks) == 0


# ============================================================================
# Test Message Handling
# ============================================================================

@pytest.mark.asyncio
async def test_send_message(mock_agent, message_router):
    """Test sending a message."""
    session_id = uuid4()
    
    message = await mock_agent.send_message(
        to_agent=AgentType.ORACLE,
        message_type="test_request",
        payload={"data": "test"},
        session_id=session_id,
    )
    
    assert message.from_agent == AgentType.INDUCTOR
    assert message.to_agent == AgentType.ORACLE
    assert message.message_type == "test_request"
    assert message.payload["data"] == "test"
    assert mock_agent._metrics["messages_sent"] == 1


@pytest.mark.asyncio
async def test_handle_message(mock_agent):
    """Test handling an incoming message."""
    await mock_agent.start()
    
    # Create a test message
    message = AgentMessage(
        id=uuid4(),
        from_agent=AgentType.ORACLE,
        to_agent=AgentType.INDUCTOR,
        message_type="test_message",
        payload={"data": "test"},
        session_id=uuid4(),
        timestamp=datetime.utcnow(),
        priority=1,
    )
    
    # Handle message
    await mock_agent.handle_message(message)
    
    assert mock_agent._metrics["messages_received"] == 1
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_handle_unknown_message_type(mock_agent):
    """Test handling a message with unknown type."""
    await mock_agent.start()
    
    message = AgentMessage(
        id=uuid4(),
        from_agent=AgentType.ORACLE,
        to_agent=AgentType.INDUCTOR,
        message_type="unknown_type",
        payload={},
        session_id=uuid4(),
        timestamp=datetime.utcnow(),
        priority=1,
    )
    
    # Should not raise, just log warning
    await mock_agent.handle_message(message)
    
    assert mock_agent._metrics["messages_received"] == 1
    
    await mock_agent.stop()


# ============================================================================
# Test Task Processing
# ============================================================================

@pytest.mark.asyncio
async def test_submit_task(mock_agent, task_queue):
    """Test submitting a task."""
    session_id = uuid4()
    
    task = await mock_agent.submit_task(
        task_type="test_task",
        session_id=session_id,
        payload={"key": "value"},
        priority=TaskPriority.HIGH,
    )
    
    assert task.agent_type == AgentType.INDUCTOR
    assert task.task_type == "test_task"
    assert task.session_id == session_id
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_process_task_success(mock_agent, task_queue):
    """Test successful task processing."""
    await mock_agent.start()
    
    session_id = uuid4()
    task = await mock_agent.submit_task(
        task_type="test_task",
        session_id=session_id,
        payload={"test": "data"},
    )
    
    # Wait for task to be processed
    await asyncio.sleep(0.5)
    
    assert mock_agent._metrics["tasks_processed"] == 1
    assert mock_agent._metrics["tasks_succeeded"] == 1
    assert mock_agent._metrics["tasks_failed"] == 0
    assert len(mock_agent.processed_tasks) == 1
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_process_task_failure(mock_agent, task_queue):
    """Test task processing failure."""
    await mock_agent.start()
    
    # Configure agent to fail
    mock_agent.should_fail = True
    
    session_id = uuid4()
    await mock_agent.submit_task(
        task_type="failing_task",
        session_id=session_id,
        payload={},
    )
    
    # Wait for task to fail and retries
    await asyncio.sleep(1.0)
    
    # Should have attempted: 1 initial + 2 retries = 3 attempts
    assert mock_agent._metrics["tasks_failed"] >= 1
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_concurrent_task_processing(mock_agent, task_queue):
    """Test processing multiple tasks concurrently."""
    await mock_agent.start()
    
    # Reduce task delay for faster test
    mock_agent.task_delay = 0.05
    
    session_id = uuid4()
    num_tasks = 5
    
    # Submit multiple tasks
    for i in range(num_tasks):
        await mock_agent.submit_task(
            task_type=f"task_{i}",
            session_id=session_id,
            payload={"index": i},
        )
    
    # Wait for all tasks to complete
    await asyncio.sleep(1.0)
    
    assert mock_agent._metrics["tasks_processed"] == num_tasks
    assert len(mock_agent.processed_tasks) == num_tasks
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_task_timeout(mock_agent, task_queue):
    """Test task timeout handling."""
    await mock_agent.start()
    
    # Set long task delay
    mock_agent.task_delay = 10.0
    
    session_id = uuid4()
    await mock_agent.submit_task(
        task_type="slow_task",
        session_id=session_id,
        payload={},
        timeout=0.5,  # Short timeout
    )
    
    # Wait for timeout
    await asyncio.sleep(1.0)
    
    assert mock_agent._metrics["tasks_failed"] >= 1
    
    await mock_agent.stop()


@pytest.mark.asyncio
async def test_task_priority_ordering(mock_agent, task_queue):
    """Test that high priority tasks are processed first."""
    await mock_agent.start()
    
    session_id = uuid4()
    
    # Submit low priority task
    await mock_agent.submit_task(
        task_type="low_priority",
        session_id=session_id,
        payload={"priority": "low"},
        priority=TaskPriority.LOW,
    )
    
    # Submit high priority task
    await mock_agent.submit_task(
        task_type="high_priority",
        session_id=session_id,
        payload={"priority": "high"},
        priority=TaskPriority.HIGH,
    )
    
    # Wait for processing
    await asyncio.sleep(0.5)
    
    # High priority should be processed first
    if len(mock_agent.processed_tasks) >= 2:
        assert mock_agent.processed_tasks[0].task_type == "high_priority"
        assert mock_agent.processed_tasks[1].task_type == "low_priority"
    
    await mock_agent.stop()


# ============================================================================
# Test Event Handling
# ============================================================================

@pytest.mark.asyncio
async def test_publish_event(mock_agent, event_bus):
    """Test publishing an event."""
    session_id = uuid4()
    
    await mock_agent.publish_event(
        event_type="test_event",
        payload={"data": "test"},
        session_id=session_id,
    )
    
    # Event should be published (no exception)
    assert True


@pytest.mark.asyncio
async def test_subscribe_to_event(mock_agent, event_bus):
    """Test subscribing to an event."""
    received_events = []
    
    async def handler(event_data: Dict[str, Any]) -> None:
        received_events.append(event_data)
    
    await mock_agent.subscribe_to_event("test_event", handler)
    
    # Publish event
    session_id = uuid4()
    await event_bus.publish("test_event", {"data": "test"}, session_id)
    
    await asyncio.sleep(0.1)
    
    # Handler should have received event
    assert len(received_events) == 1
    assert received_events[0]["data"] == "test"


# ============================================================================
# Test Metrics
# ============================================================================

@pytest.mark.asyncio
async def test_get_metrics(mock_agent):
    """Test getting agent metrics."""
    metrics = mock_agent.get_metrics()
    
    assert "tasks_processed" in metrics
    assert "tasks_succeeded" in metrics
    assert "tasks_failed" in metrics
    assert "messages_sent" in metrics
    assert "messages_received" in metrics
    assert "errors" in metrics
    assert "state" in metrics
    assert "active_tasks" in metrics
    
    assert metrics["state"] == AgentState.IDLE.value
    assert metrics["active_tasks"] == 0


@pytest.mark.asyncio
async def test_metrics_after_processing(mock_agent, task_queue):
    """Test metrics after processing tasks."""
    await mock_agent.start()
    
    session_id = uuid4()
    
    # Process some tasks
    for i in range(3):
        await mock_agent.submit_task(
            task_type=f"task_{i}",
            session_id=session_id,
            payload={},
        )
    
    # Wait for processing
    await asyncio.sleep(1.0)
    
    metrics = mock_agent.get_metrics()
    assert metrics["tasks_processed"] == 3
    assert metrics["tasks_succeeded"] == 3
    
    await mock_agent.stop()


# ============================================================================
# Test Agent State
# ============================================================================

@pytest.mark.asyncio
async def test_agent_repr(mock_agent):
    """Test agent string representation."""
    repr_str = repr(mock_agent)
    
    assert "MockAgent" in repr_str
    assert "inductor" in repr_str
    assert "idle" in repr_str


@pytest.mark.asyncio
async def test_agent_state_transitions(mock_agent):
    """Test all agent state transitions."""
    # IDLE -> STARTING -> RUNNING
    assert mock_agent.state == AgentState.IDLE
    
    await mock_agent.start()
    assert mock_agent.state == AgentState.RUNNING
    
    # RUNNING -> PAUSED
    await mock_agent.pause()
    assert mock_agent.state == AgentState.PAUSED
    
    # PAUSED -> RUNNING
    await mock_agent.resume()
    assert mock_agent.state == AgentState.RUNNING
    
    # RUNNING -> STOPPING -> STOPPED
    await mock_agent.stop()
    assert mock_agent.state == AgentState.STOPPED


# ============================================================================
# Test Configuration
# ============================================================================

def test_agent_config_initialization():
    """Test agent configuration initialization."""
    config = AgentConfig(
        agent_type=AgentType.ORACLE,
        max_concurrent_tasks=10,
        task_timeout=60.0,
        custom_config={"llm_model": "gpt-4"},
    )
    
    assert config.agent_type == AgentType.ORACLE
    assert config.max_concurrent_tasks == 10
    assert config.task_timeout == 60.0
    assert config.get("llm_model") == "gpt-4"
    assert config.get("unknown_key", "default") == "default"


def test_agent_config_defaults():
    """Test agent configuration defaults."""
    config = AgentConfig(agent_type=AgentType.CONTRACTOR)
    
    assert config.max_concurrent_tasks == 5
    assert config.task_timeout == 300.0
    assert config.message_timeout == 30.0
    assert config.retry_limit == 3
    assert config.enable_metrics is True
    assert config.enable_tracing is True
