"""
Tests for communication, serialization, and task queue modules.

Author: Aurel IKAMA HONEY
"""
import asyncio
import pickle
from datetime import datetime
from uuid import uuid4

import pytest

from shared_context import AgentMessage, AgentType
from orchestration.communication import (
    CommunicationProtocol,
    EventBus,
    EventType,
    MessageBuilder,
    MessageRouter,
    MessageType,
)
from orchestration.serialization import (
    JSONSerializer,
    MessageCodec,
    PickleSerializer,
    SerializerFactory,
    decode_message,
    encode_message,
)
from orchestration.task_queue import (
    InMemoryTaskQueue,
    Task,
    TaskBuilder,
    TaskExecutor,
    TaskPriority,
    TaskStatus,
)


# ================================
# Communication Protocol Tests
# ================================


class MockCommunicationProtocol(CommunicationProtocol):
    """Mock protocol for testing."""
    
    def __init__(self):
        self.sent_messages = []
        self.received_messages = []
    
    async def send_message(self, message: AgentMessage) -> None:
        self.sent_messages.append(message)
    
    async def receive_message(self) -> AgentMessage:
        if self.received_messages:
            return self.received_messages.pop(0)
        await asyncio.sleep(0.1)
        raise TimeoutError("No message available")
    
    async def broadcast(self, message: AgentMessage) -> None:
        self.sent_messages.append(message)


class TestMessageBuilder:
    """Test MessageBuilder."""
    
    def test_build_basic_message(self):
        """Test building a basic message."""
        session_id = uuid4()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(session_id)
            .with_payload({"test": "data"})
            .build()
        )
        
        assert message.from_agent == AgentType.INDUCTOR
        assert message.to_agent == AgentType.ORACLE
        assert message.message_type == MessageType.TASK_REQUEST
        assert message.session_id == session_id
        assert message.payload == {"test": "data"}
    
    def test_build_with_parent(self):
        """Test building a response message."""
        parent_id = uuid4()
        session_id = uuid4()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.ORACLE)
            .to_agent(AgentType.INDUCTOR)
            .of_type(MessageType.TASK_RESPONSE)
            .for_session(session_id)
            .in_reply_to(parent_id)
            .build()
        )
        
        assert message.parent_id == parent_id
    
    def test_build_with_priority(self):
        """Test building a high-priority message."""
        session_id = uuid4()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.RUNNER)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(session_id)
            .with_priority(2)
            .build()
        )
        
        assert message.priority == 2
    
    def test_build_missing_required_field(self):
        """Test building without required fields."""
        with pytest.raises(ValueError):
            MessageBuilder().from_agent(AgentType.INDUCTOR).build()
    
    def test_builder_reset(self):
        """Test resetting builder state."""
        builder = MessageBuilder()
        session_id = uuid4()
        
        builder.from_agent(AgentType.INDUCTOR).to_agent(AgentType.ORACLE)
        builder.reset()
        
        with pytest.raises(ValueError):
            builder.for_session(session_id).build()


class TestMessageRouter:
    """Test MessageRouter."""
    
    @pytest.mark.asyncio
    async def test_register_and_route_message(self):
        """Test registering handler and routing message."""
        router = MessageRouter()
        received_messages = []
        
        async def handler(message: AgentMessage):
            received_messages.append(message)
        
        router.register_handler(MessageType.TASK_REQUEST, handler)
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        await router.route_message(message)
        
        assert len(received_messages) == 1
        assert received_messages[0].id == message.id
    
    @pytest.mark.asyncio
    async def test_route_to_agent_handler(self):
        """Test routing to agent-specific handler."""
        router = MessageRouter()
        received_by_oracle = []
        
        async def oracle_handler(message: AgentMessage):
            received_by_oracle.append(message)
        
        router.register_agent_handler(AgentType.ORACLE, oracle_handler)
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        await router.route_message(message)
        
        assert len(received_by_oracle) == 1
    
    @pytest.mark.asyncio
    async def test_no_handler_registered(self):
        """Test routing when no handler is registered."""
        router = MessageRouter()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        # Should not raise, just log warning
        await router.route_message(message)
    
    @pytest.mark.asyncio
    async def test_handler_exception(self):
        """Test handling exceptions in handlers."""
        router = MessageRouter()
        
        async def failing_handler(message: AgentMessage):
            raise ValueError("Handler error")
        
        router.register_handler(MessageType.TASK_REQUEST, failing_handler)
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        # Should not raise, just log error
        await router.route_message(message)


class TestEventBus:
    """Test EventBus."""
    
    @pytest.mark.asyncio
    async def test_subscribe_and_publish(self):
        """Test subscribing and publishing events."""
        bus = EventBus()
        received_events = []
        
        async def subscriber(event_type: EventType, data: dict):
            received_events.append((event_type, data))
        
        bus.subscribe(EventType.WORKFLOW_STARTED, subscriber)
        
        await bus.publish(EventType.WORKFLOW_STARTED, {"session_id": "test"})
        
        # Give event time to process
        await asyncio.sleep(0.1)
        
        assert len(received_events) == 1
        assert received_events[0][0] == EventType.WORKFLOW_STARTED
        assert received_events[0][1]["session_id"] == "test"
    
    @pytest.mark.asyncio
    async def test_multiple_subscribers(self):
        """Test multiple subscribers to same event."""
        bus = EventBus()
        received_1 = []
        received_2 = []
        
        async def subscriber_1(event_type: EventType, data: dict):
            received_1.append(data)
        
        async def subscriber_2(event_type: EventType, data: dict):
            received_2.append(data)
        
        bus.subscribe(EventType.AGENT_STARTED, subscriber_1)
        bus.subscribe(EventType.AGENT_STARTED, subscriber_2)
        
        await bus.publish(EventType.AGENT_STARTED, {"agent": "oracle"})
        
        await asyncio.sleep(0.1)
        
        assert len(received_1) == 1
        assert len(received_2) == 1
    
    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        """Test unsubscribing from events."""
        bus = EventBus()
        received = []
        
        async def subscriber(event_type: EventType, data: dict):
            received.append(data)
        
        bus.subscribe(EventType.ITERATION_STARTED, subscriber)
        await bus.publish(EventType.ITERATION_STARTED, {"iteration": 1})
        
        await asyncio.sleep(0.1)
        
        bus.unsubscribe(EventType.ITERATION_STARTED, subscriber)
        await bus.publish(EventType.ITERATION_STARTED, {"iteration": 2})
        
        await asyncio.sleep(0.1)
        
        # Should only receive first event
        assert len(received) == 1
        assert received[0]["iteration"] == 1
    
    @pytest.mark.asyncio
    async def test_subscriber_exception(self):
        """Test handling exceptions in subscribers."""
        bus = EventBus()
        received_good = []
        
        async def failing_subscriber(event_type: EventType, data: dict):
            raise ValueError("Subscriber error")
        
        async def good_subscriber(event_type: EventType, data: dict):
            received_good.append(data)
        
        bus.subscribe(EventType.ERROR_OCCURRED, failing_subscriber)
        bus.subscribe(EventType.ERROR_OCCURRED, good_subscriber)
        
        await bus.publish(EventType.ERROR_OCCURRED, {"error": "test"})
        
        await asyncio.sleep(0.1)
        
        # Good subscriber should still receive event
        assert len(received_good) == 1


# ================================
# Serialization Tests
# ================================


class TestJSONSerializer:
    """Test JSONSerializer."""
    
    def test_serialize_deserialize(self):
        """Test JSON serialization roundtrip."""
        serializer = JSONSerializer()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .with_payload({"key": "value"})
            .build()
        )
        
        # Serialize
        data = serializer.serialize(message)
        assert isinstance(data, bytes)
        
        # Deserialize
        restored = serializer.deserialize(data)
        assert restored.id == message.id
        assert restored.from_agent == message.from_agent
        assert restored.payload == message.payload
    
    def test_serialize_with_datetime(self):
        """Test serializing message with datetime."""
        serializer = JSONSerializer()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        data = serializer.serialize(message)
        restored = serializer.deserialize(data)
        
        assert restored.created_at is not None
        assert isinstance(restored.created_at, datetime)


class TestPickleSerializer:
    """Test PickleSerializer."""
    
    def test_serialize_deserialize(self):
        """Test pickle serialization roundtrip."""
        serializer = PickleSerializer()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.ORACLE)
            .to_agent(AgentType.CONTRACTOR)
            .of_type(MessageType.TASK_RESPONSE)
            .for_session(uuid4())
            .with_payload({"complex": {"nested": "data"}})
            .build()
        )
        
        # Serialize
        data = serializer.serialize(message)
        assert isinstance(data, bytes)
        
        # Deserialize
        restored = serializer.deserialize(data)
        assert restored.id == message.id
        assert restored.payload == message.payload
    
    def test_smaller_than_json(self):
        """Test that pickle is more compact than JSON."""
        json_serializer = JSONSerializer()
        pickle_serializer = PickleSerializer()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .with_payload({"data": "x" * 1000})
            .build()
        )
        
        json_data = json_serializer.serialize(message)
        pickle_data = pickle_serializer.serialize(message)
        
        # Pickle should be smaller for large payloads
        assert len(pickle_data) < len(json_data)


class TestSerializerFactory:
    """Test SerializerFactory."""
    
    def test_create_json_serializer(self):
        """Test creating JSON serializer."""
        serializer = SerializerFactory.create("json")
        assert isinstance(serializer, JSONSerializer)
    
    def test_create_pickle_serializer(self):
        """Test creating pickle serializer."""
        serializer = SerializerFactory.create("pickle")
        assert isinstance(serializer, PickleSerializer)
    
    def test_invalid_format(self):
        """Test creating with invalid format."""
        with pytest.raises(ValueError):
            SerializerFactory.create("invalid")


class TestMessageCodec:
    """Test MessageCodec."""
    
    def test_encode_decode_json(self):
        """Test encoding/decoding with JSON."""
        codec = MessageCodec(format="json")
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        # Encode
        encoded = codec.encode(message)
        assert isinstance(encoded, bytes)
        
        # Decode
        decoded = codec.decode(encoded)
        assert decoded.id == message.id
    
    def test_encode_decode_pickle(self):
        """Test encoding/decoding with pickle."""
        codec = MessageCodec(format="pickle")
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.ORACLE)
            .to_agent(AgentType.CONTRACTOR)
            .of_type(MessageType.TASK_RESPONSE)
            .for_session(uuid4())
            .build()
        )
        
        encoded = codec.encode(message)
        decoded = codec.decode(encoded)
        
        assert decoded.id == message.id


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_encode_message(self):
        """Test encode_message function."""
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        encoded = encode_message(message)
        assert isinstance(encoded, bytes)
    
    def test_decode_message(self):
        """Test decode_message function."""
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(uuid4())
            .build()
        )
        
        encoded = encode_message(message)
        decoded = decode_message(encoded)
        
        assert decoded.id == message.id


# ================================
# Task Queue Tests
# ================================


class TestTask:
    """Test Task model."""
    
    def test_create_task(self):
        """Test creating a task."""
        session_id = uuid4()
        
        task = Task(
            priority=TaskPriority.HIGH,
            agent_type=AgentType.ORACLE,
            task_type="analyze_endpoint",
            session_id=session_id,
        )
        
        assert task.agent_type == AgentType.ORACLE
        assert task.task_type == "analyze_endpoint"
        assert task.status == TaskStatus.PENDING
        assert task.session_id == session_id
    
    def test_task_ordering(self):
        """Test task priority ordering."""
        task_low = Task(
            priority=TaskPriority.LOW,
            agent_type=AgentType.ORACLE,
            task_type="test",
            session_id=uuid4(),
        )
        
        task_high = Task(
            priority=TaskPriority.HIGH,
            agent_type=AgentType.ORACLE,
            task_type="test",
            session_id=uuid4(),
        )
        
        # Higher priority should come first (smaller when negated)
        assert task_high < task_low


class TestTaskBuilder:
    """Test TaskBuilder."""
    
    def test_build_basic_task(self):
        """Test building a basic task."""
        session_id = uuid4()
        
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("analyze_endpoint")
            .for_session(session_id)
            .with_payload({"endpoint": "/api/users"})
            .build()
        )
        
        assert task.agent_type == AgentType.ORACLE
        assert task.task_type == "analyze_endpoint"
        assert task.session_id == session_id
        assert task.payload["endpoint"] == "/api/users"
    
    def test_build_with_options(self):
        """Test building with additional options."""
        session_id = uuid4()
        
        task = (
            TaskBuilder()
            .for_agent(AgentType.CONTRACTOR)
            .of_type("generate_test")
            .for_session(session_id)
            .with_priority(TaskPriority.CRITICAL)
            .with_retries(5)
            .with_timeout(30.0)
            .build()
        )
        
        assert task.max_retries == 5
        assert task.timeout_seconds == 30.0
    
    def test_build_from_message(self):
        """Test building from AgentMessage."""
        session_id = uuid4()
        
        message = (
            MessageBuilder()
            .from_agent(AgentType.INDUCTOR)
            .to_agent(AgentType.ORACLE)
            .of_type(MessageType.TASK_REQUEST)
            .for_session(session_id)
            .with_payload({"test": "data"})
            .build()
        )
        
        task = TaskBuilder().from_message(message).build()
        
        assert task.agent_type == message.to_agent
        assert task.task_type == message.message_type
        assert task.payload == message.payload
        assert task.message_id == message.id
    
    def test_build_missing_required(self):
        """Test building without required fields."""
        with pytest.raises(ValueError):
            TaskBuilder().for_agent(AgentType.ORACLE).build()
    
    def test_builder_reset(self):
        """Test resetting builder."""
        builder = TaskBuilder()
        session_id = uuid4()
        
        builder.for_agent(AgentType.ORACLE).of_type("test")
        builder.reset()
        
        with pytest.raises(ValueError):
            builder.for_session(session_id).build()


class TestInMemoryTaskQueue:
    """Test InMemoryTaskQueue."""
    
    @pytest.mark.asyncio
    async def test_enqueue_dequeue(self):
        """Test enqueueing and dequeueing tasks."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("test_task")
            .for_session(session_id)
            .build()
        )
        
        await queue.enqueue(task)
        
        assert await queue.size() == 1
        
        dequeued = await queue.dequeue()
        
        assert dequeued.id == task.id
        assert await queue.size() == 0
    
    @pytest.mark.asyncio
    async def test_priority_ordering(self):
        """Test that tasks are dequeued by priority."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        # Enqueue in reverse priority order
        low = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("low")
            .for_session(session_id)
            .with_priority(TaskPriority.LOW)
            .build()
        )
        
        high = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("high")
            .for_session(session_id)
            .with_priority(TaskPriority.HIGH)
            .build()
        )
        
        await queue.enqueue(low)
        await queue.enqueue(high)
        
        # Should dequeue high priority first
        first = await queue.dequeue()
        assert first.id == high.id
        
        second = await queue.dequeue()
        assert second.id == low.id
    
    @pytest.mark.asyncio
    async def test_dequeue_by_agent(self):
        """Test dequeueing tasks for specific agent."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        oracle_task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("oracle_task")
            .for_session(session_id)
            .build()
        )
        
        contractor_task = (
            TaskBuilder()
            .for_agent(AgentType.CONTRACTOR)
            .of_type("contractor_task")
            .for_session(session_id)
            .build()
        )
        
        await queue.enqueue(oracle_task)
        await queue.enqueue(contractor_task)
        
        # Dequeue for Oracle
        task = await queue.dequeue(agent_type=AgentType.ORACLE)
        assert task.id == oracle_task.id
        
        # Should still have Contractor task
        assert await queue.size() == 1
    
    @pytest.mark.asyncio
    async def test_peek(self):
        """Test peeking at next task."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("test")
            .for_session(session_id)
            .build()
        )
        
        await queue.enqueue(task)
        
        peeked = await queue.peek()
        assert peeked.id == task.id
        
        # Should not remove from queue
        assert await queue.size() == 1
    
    @pytest.mark.asyncio
    async def test_get_task(self):
        """Test getting task by ID."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("test")
            .for_session(session_id)
            .build()
        )
        
        await queue.enqueue(task)
        
        retrieved = await queue.get_task(task.id)
        assert retrieved.id == task.id
    
    @pytest.mark.asyncio
    async def test_cancel_task(self):
        """Test cancelling a task."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("test")
            .for_session(session_id)
            .build()
        )
        
        await queue.enqueue(task)
        
        # Cancel
        success = await queue.cancel_task(task.id)
        assert success
        
        # Check status
        retrieved = await queue.get_task(task.id)
        assert retrieved.status == TaskStatus.CANCELLED
    
    @pytest.mark.asyncio
    async def test_clear(self):
        """Test clearing queue."""
        queue = InMemoryTaskQueue()
        session_id = uuid4()
        
        for i in range(5):
            task = (
                TaskBuilder()
                .for_agent(AgentType.ORACLE)
                .of_type(f"task_{i}")
                .for_session(session_id)
                .build()
            )
            await queue.enqueue(task)
        
        assert await queue.size() == 5
        
        await queue.clear()
        
        assert await queue.size() == 0


class TestTaskExecutor:
    """Test TaskExecutor."""
    
    @pytest.mark.asyncio
    async def test_execute_task(self):
        """Test executing a task."""
        queue = InMemoryTaskQueue()
        executor = TaskExecutor(queue)
        
        # Register handler
        results = []
        
        def handler(task: Task):
            results.append(task.payload["value"])
            return task.payload["value"] * 2
        
        executor.register_handler("test_task", handler)
        
        # Create task
        session_id = uuid4()
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("test_task")
            .for_session(session_id)
            .with_payload({"value": 42})
            .build()
        )
        
        # Execute
        result = await executor.execute_task(task)
        
        assert result == 84
        assert task.status == TaskStatus.COMPLETED
        assert len(results) == 1
    
    @pytest.mark.asyncio
    async def test_execute_async_handler(self):
        """Test executing task with async handler."""
        queue = InMemoryTaskQueue()
        executor = TaskExecutor(queue)
        
        async def async_handler(task: Task):
            await asyncio.sleep(0.1)
            return "async_result"
        
        executor.register_handler("async_task", async_handler)
        
        session_id = uuid4()
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("async_task")
            .for_session(session_id)
            .build()
        )
        
        result = await executor.execute_task(task)
        
        assert result == "async_result"
        assert task.status == TaskStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_task_timeout(self):
        """Test task timeout."""
        queue = InMemoryTaskQueue()
        executor = TaskExecutor(queue)
        
        async def slow_handler(task: Task):
            await asyncio.sleep(10)
            return "done"
        
        executor.register_handler("slow_task", slow_handler)
        
        session_id = uuid4()
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("slow_task")
            .for_session(session_id)
            .with_timeout(0.1)
            .build()
        )
        
        with pytest.raises(asyncio.TimeoutError):
            await executor.execute_task(task)
        
        assert task.status == TaskStatus.TIMEOUT
    
    @pytest.mark.asyncio
    async def test_task_retry(self):
        """Test task retry on failure."""
        queue = InMemoryTaskQueue()
        executor = TaskExecutor(queue, max_concurrent_tasks=1)
        
        call_count = [0]
        
        def failing_handler(task: Task):
            call_count[0] += 1
            if call_count[0] < 3:
                raise ValueError("Not yet")
            return "success"
        
        executor.register_handler("retry_task", failing_handler)
        
        session_id = uuid4()
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("retry_task")
            .for_session(session_id)
            .with_retries(3)
            .build()
        )
        
        # First attempt fails
        with pytest.raises(ValueError):
            await executor.execute_task(task)
        
        # Should be re-enqueued
        assert await queue.size() == 1
        assert task.retry_count == 1
    
    @pytest.mark.asyncio
    async def test_no_handler(self):
        """Test executing task without handler."""
        queue = InMemoryTaskQueue()
        executor = TaskExecutor(queue)
        
        session_id = uuid4()
        task = (
            TaskBuilder()
            .for_agent(AgentType.ORACLE)
            .of_type("unknown_task")
            .for_session(session_id)
            .build()
        )
        
        with pytest.raises(ValueError, match="No handler"):
            await executor.execute_task(task)
    
    @pytest.mark.asyncio
    async def test_executor_statistics(self):
        """Test getting executor statistics."""
        queue = InMemoryTaskQueue()
        executor = TaskExecutor(queue, max_concurrent_tasks=5)
        
        stats = executor.get_statistics()
        
        assert stats["max_concurrent_tasks"] == 5
        assert stats["running_tasks"] == 0
        assert stats["is_running"] is False
