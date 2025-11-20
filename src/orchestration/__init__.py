"""
Orchestration layer for multi-agent workflow.

This package provides the communication infrastructure for coordinating
agents during the test generation workflow.

Modules:
    - communication: Protocol interfaces, message routing, and event bus
    - serialization: Message serialization/deserialization
    - task_queue: Priority-based task queue for managing agent workloads

Author: Aurel IKAMA HONEY
"""

# Communication
from .communication import (
    CommunicationProtocol,
    EventBus,
    EventType,
    MessageBuilder,
    MessageHandler,
    MessageRouter,
    MessageType,
)

# Serialization
from .serialization import (
    JSONSerializer,
    MessageCodec,
    MessageSerializer,
    PickleSerializer,
    SerializerFactory,
    decode_message,
    encode_message,
)

# Task Queue
from .task_queue import (
    InMemoryTaskQueue,
    Task,
    TaskBuilder,
    TaskExecutor,
    TaskPriority,
    TaskQueue,
    TaskStatus,
)

__all__ = [
    # Communication
    "CommunicationProtocol",
    "MessageHandler",
    "MessageRouter",
    "EventBus",
    "MessageBuilder",
    "MessageType",
    "EventType",
    # Serialization
    "MessageSerializer",
    "JSONSerializer",
    "PickleSerializer",
    "SerializerFactory",
    "MessageCodec",
    "encode_message",
    "decode_message",
    # Task Queue
    "TaskQueue",
    "InMemoryTaskQueue",
    "Task",
    "TaskBuilder",
    "TaskExecutor",
    "TaskPriority",
    "TaskStatus",
]
