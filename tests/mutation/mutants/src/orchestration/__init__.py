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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result
