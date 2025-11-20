"""
Task queue system for managing agent workloads.

This module implements a priority-based task queue for distributing
work among agents during the test generation workflow.

Author: Aurel IKAMA HONEY
"""
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID, uuid4

from shared_context import AgentMessage, AgentType
from utils.logging import logger
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


class TaskPriority(int, Enum):
    """Task priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


@dataclass(order=True)
class Task:
    """
    Represents a task to be executed by an agent.
    
    Tasks are ordered by priority (higher first) and then by creation time.
    Python's heapq is a min-heap, so we use negative priority for max-heap behavior.
    """
    
    # Required task details (no defaults)
    agent_type: AgentType = field(compare=False)
    task_type: str = field(compare=False)
    session_id: UUID = field(compare=False)
    
    # Fields for ordering (with defaults)
    # Use negative priority for max-heap behavior in min-heap
    priority: TaskPriority = field(default=TaskPriority.NORMAL, compare=False)
    _sort_priority: int = field(init=False, compare=True)
    created_at: datetime = field(default_factory=datetime.utcnow, compare=True)
    
    # Optional task details (with defaults)
    id: UUID = field(default_factory=uuid4, compare=False)
    payload: Dict[str, Any] = field(default_factory=dict, compare=False)
    
    # Execution
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)
    started_at: Optional[datetime] = field(default=None, compare=False)
    completed_at: Optional[datetime] = field(default=None, compare=False)
    result: Optional[Any] = field(default=None, compare=False)
    error: Optional[str] = field(default=None, compare=False)
    
    # Retry logic
    max_retries: int = field(default=3, compare=False)
    retry_count: int = field(default=0, compare=False)
    
    # Timeout
    timeout_seconds: Optional[float] = field(default=None, compare=False)
    
    # Related message
    message_id: Optional[UUID] = field(default=None, compare=False)
    
    def __post_init__(self):
        """Initialize sort priority (negative for max-heap)."""
        # Invert priority for max-heap behavior
        object.__setattr__(self, '_sort_priority', -self.priority.value)


class TaskQueue(ABC):
    """
    Abstract base class for task queues.
    
    Defines the interface for managing task queues.
    """
    
    @abstractmethod
    async def enqueue(self, task: Task) -> None:
        """
        Add a task to the queue.
        
        Args:
            task: Task to enqueue
        """
        pass
    
    @abstractmethod
    async def dequeue(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """
        Remove and return the highest priority task.
        
        Args:
            agent_type: Optional filter by agent type
            
        Returns:
            Task or None if queue is empty
        """
        pass
    
    @abstractmethod
    async def peek(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """
        View the highest priority task without removing it.
        
        Args:
            agent_type: Optional filter by agent type
            
        Returns:
            Task or None if queue is empty
        """
        pass
    
    @abstractmethod
    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: Task UUID
            
        Returns:
            Task or None if not found
        """
        pass
    
    @abstractmethod
    async def cancel_task(self, task_id: UUID) -> bool:
        """
        Cancel a pending task.
        
        Args:
            task_id: Task UUID
            
        Returns:
            True if cancelled, False if not found or already running
        """
        pass
    
    @abstractmethod
    async def size(self, agent_type: Optional[AgentType] = None) -> int:
        """
        Get the number of pending tasks.
        
        Args:
            agent_type: Optional filter by agent type
            
        Returns:
            Number of pending tasks
        """
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all pending tasks."""
        pass


class InMemoryTaskQueue(TaskQueue):
    """
    In-memory priority-based task queue.
    
    Uses asyncio.PriorityQueue for task management.
    Suitable for single-process deployments.
    """
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_orig(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self.tasks: Dict[UUID, Task] = {}
        self.lock = asyncio.Lock()
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_1(self, maxsize: int = 1):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self.tasks: Dict[UUID, Task] = {}
        self.lock = asyncio.Lock()
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_2(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = None
        self.tasks: Dict[UUID, Task] = {}
        self.lock = asyncio.Lock()
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_3(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=None)
        self.tasks: Dict[UUID, Task] = {}
        self.lock = asyncio.Lock()
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_4(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self.tasks: Dict[UUID, Task] = None
        self.lock = asyncio.Lock()
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_5(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self.tasks: Dict[UUID, Task] = {}
        self.lock = None
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    def xǁInMemoryTaskQueueǁ__init____mutmut_6(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self.tasks: Dict[UUID, Task] = {}
        self.lock = asyncio.Lock()
        logger.info(None)
    
    xǁInMemoryTaskQueueǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁ__init____mutmut_1': xǁInMemoryTaskQueueǁ__init____mutmut_1, 
        'xǁInMemoryTaskQueueǁ__init____mutmut_2': xǁInMemoryTaskQueueǁ__init____mutmut_2, 
        'xǁInMemoryTaskQueueǁ__init____mutmut_3': xǁInMemoryTaskQueueǁ__init____mutmut_3, 
        'xǁInMemoryTaskQueueǁ__init____mutmut_4': xǁInMemoryTaskQueueǁ__init____mutmut_4, 
        'xǁInMemoryTaskQueueǁ__init____mutmut_5': xǁInMemoryTaskQueueǁ__init____mutmut_5, 
        'xǁInMemoryTaskQueueǁ__init____mutmut_6': xǁInMemoryTaskQueueǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁ__init____mutmut_orig)
    xǁInMemoryTaskQueueǁ__init____mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁ__init__'
    
    async def xǁInMemoryTaskQueueǁenqueue__mutmut_orig(self, task: Task) -> None:
        """Add a task to the queue."""
        async with self.lock:
            self.tasks[task.id] = task
            await self.queue.put(task)
            logger.debug(
                f"Enqueued task {task.id} for {task.agent_type.value} "
                f"(priority={-task.priority.value}, type={task.task_type})"
            )
    
    async def xǁInMemoryTaskQueueǁenqueue__mutmut_1(self, task: Task) -> None:
        """Add a task to the queue."""
        async with self.lock:
            self.tasks[task.id] = None
            await self.queue.put(task)
            logger.debug(
                f"Enqueued task {task.id} for {task.agent_type.value} "
                f"(priority={-task.priority.value}, type={task.task_type})"
            )
    
    async def xǁInMemoryTaskQueueǁenqueue__mutmut_2(self, task: Task) -> None:
        """Add a task to the queue."""
        async with self.lock:
            self.tasks[task.id] = task
            await self.queue.put(None)
            logger.debug(
                f"Enqueued task {task.id} for {task.agent_type.value} "
                f"(priority={-task.priority.value}, type={task.task_type})"
            )
    
    async def xǁInMemoryTaskQueueǁenqueue__mutmut_3(self, task: Task) -> None:
        """Add a task to the queue."""
        async with self.lock:
            self.tasks[task.id] = task
            await self.queue.put(task)
            logger.debug(
                None
            )
    
    async def xǁInMemoryTaskQueueǁenqueue__mutmut_4(self, task: Task) -> None:
        """Add a task to the queue."""
        async with self.lock:
            self.tasks[task.id] = task
            await self.queue.put(task)
            logger.debug(
                f"Enqueued task {task.id} for {task.agent_type.value} "
                f"(priority={+task.priority.value}, type={task.task_type})"
            )
    
    xǁInMemoryTaskQueueǁenqueue__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁenqueue__mutmut_1': xǁInMemoryTaskQueueǁenqueue__mutmut_1, 
        'xǁInMemoryTaskQueueǁenqueue__mutmut_2': xǁInMemoryTaskQueueǁenqueue__mutmut_2, 
        'xǁInMemoryTaskQueueǁenqueue__mutmut_3': xǁInMemoryTaskQueueǁenqueue__mutmut_3, 
        'xǁInMemoryTaskQueueǁenqueue__mutmut_4': xǁInMemoryTaskQueueǁenqueue__mutmut_4
    }
    
    def enqueue(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁenqueue__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁenqueue__mutmut_mutants"), args, kwargs, self)
        return result 
    
    enqueue.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁenqueue__mutmut_orig)
    xǁInMemoryTaskQueueǁenqueue__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁenqueue'
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_orig(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_1(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is not None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_2(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = None
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_3(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(None, timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_4(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=None)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_5(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_6(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), )
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_7(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=1.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_8(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    None
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_9(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = None
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_10(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = ""
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_11(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_12(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = None
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_13(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(None, timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_14(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=None)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_15(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_16(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), )
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_17(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=1.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_18(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type or not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_19(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type != agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_20(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_21(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = None
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_22(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(None)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_23(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    return
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_24(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(None)
            
            if found_task:
                logger.debug(
                    f"Dequeued task {found_task.id} for {agent_type.value}"
                )
            
            return found_task
    
    async def xǁInMemoryTaskQueueǁdequeue__mutmut_25(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """Remove and return the highest priority task."""
        if agent_type is None:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                logger.debug(
                    f"Dequeued task {task.id} for {task.agent_type.value}"
                )
                return task
            except asyncio.TimeoutError:
                return None
        
        # Filter by agent type
        async with self.lock:
            # This is inefficient but works for in-memory queue
            # For production, use a proper queue per agent type
            temp_tasks = []
            found_task = None
            
            while not self.queue.empty():
                try:
                    task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    if task.agent_type == agent_type and not found_task:
                        found_task = task
                    else:
                        temp_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            # Re-enqueue temp tasks
            for task in temp_tasks:
                await self.queue.put(task)
            
            if found_task:
                logger.debug(
                    None
                )
            
            return found_task
    
    xǁInMemoryTaskQueueǁdequeue__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁdequeue__mutmut_1': xǁInMemoryTaskQueueǁdequeue__mutmut_1, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_2': xǁInMemoryTaskQueueǁdequeue__mutmut_2, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_3': xǁInMemoryTaskQueueǁdequeue__mutmut_3, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_4': xǁInMemoryTaskQueueǁdequeue__mutmut_4, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_5': xǁInMemoryTaskQueueǁdequeue__mutmut_5, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_6': xǁInMemoryTaskQueueǁdequeue__mutmut_6, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_7': xǁInMemoryTaskQueueǁdequeue__mutmut_7, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_8': xǁInMemoryTaskQueueǁdequeue__mutmut_8, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_9': xǁInMemoryTaskQueueǁdequeue__mutmut_9, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_10': xǁInMemoryTaskQueueǁdequeue__mutmut_10, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_11': xǁInMemoryTaskQueueǁdequeue__mutmut_11, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_12': xǁInMemoryTaskQueueǁdequeue__mutmut_12, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_13': xǁInMemoryTaskQueueǁdequeue__mutmut_13, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_14': xǁInMemoryTaskQueueǁdequeue__mutmut_14, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_15': xǁInMemoryTaskQueueǁdequeue__mutmut_15, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_16': xǁInMemoryTaskQueueǁdequeue__mutmut_16, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_17': xǁInMemoryTaskQueueǁdequeue__mutmut_17, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_18': xǁInMemoryTaskQueueǁdequeue__mutmut_18, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_19': xǁInMemoryTaskQueueǁdequeue__mutmut_19, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_20': xǁInMemoryTaskQueueǁdequeue__mutmut_20, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_21': xǁInMemoryTaskQueueǁdequeue__mutmut_21, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_22': xǁInMemoryTaskQueueǁdequeue__mutmut_22, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_23': xǁInMemoryTaskQueueǁdequeue__mutmut_23, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_24': xǁInMemoryTaskQueueǁdequeue__mutmut_24, 
        'xǁInMemoryTaskQueueǁdequeue__mutmut_25': xǁInMemoryTaskQueueǁdequeue__mutmut_25
    }
    
    def dequeue(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁdequeue__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁdequeue__mutmut_mutants"), args, kwargs, self)
        return result 
    
    dequeue.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁdequeue__mutmut_orig)
    xǁInMemoryTaskQueueǁdequeue__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁdequeue'
    
    async def xǁInMemoryTaskQueueǁpeek__mutmut_orig(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """View the highest priority task without removing it."""
        task = await self.dequeue(agent_type)
        if task:
            await self.enqueue(task)
        return task
    
    async def xǁInMemoryTaskQueueǁpeek__mutmut_1(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """View the highest priority task without removing it."""
        task = None
        if task:
            await self.enqueue(task)
        return task
    
    async def xǁInMemoryTaskQueueǁpeek__mutmut_2(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """View the highest priority task without removing it."""
        task = await self.dequeue(None)
        if task:
            await self.enqueue(task)
        return task
    
    async def xǁInMemoryTaskQueueǁpeek__mutmut_3(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """View the highest priority task without removing it."""
        task = await self.dequeue(agent_type)
        if task:
            await self.enqueue(None)
        return task
    
    xǁInMemoryTaskQueueǁpeek__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁpeek__mutmut_1': xǁInMemoryTaskQueueǁpeek__mutmut_1, 
        'xǁInMemoryTaskQueueǁpeek__mutmut_2': xǁInMemoryTaskQueueǁpeek__mutmut_2, 
        'xǁInMemoryTaskQueueǁpeek__mutmut_3': xǁInMemoryTaskQueueǁpeek__mutmut_3
    }
    
    def peek(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁpeek__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁpeek__mutmut_mutants"), args, kwargs, self)
        return result 
    
    peek.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁpeek__mutmut_orig)
    xǁInMemoryTaskQueueǁpeek__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁpeek'
    
    async def xǁInMemoryTaskQueueǁget_task__mutmut_orig(self, task_id: UUID) -> Optional[Task]:
        """Get a specific task by ID."""
        async with self.lock:
            return self.tasks.get(task_id)
    
    async def xǁInMemoryTaskQueueǁget_task__mutmut_1(self, task_id: UUID) -> Optional[Task]:
        """Get a specific task by ID."""
        async with self.lock:
            return self.tasks.get(None)
    
    xǁInMemoryTaskQueueǁget_task__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁget_task__mutmut_1': xǁInMemoryTaskQueueǁget_task__mutmut_1
    }
    
    def get_task(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁget_task__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁget_task__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_task.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁget_task__mutmut_orig)
    xǁInMemoryTaskQueueǁget_task__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁget_task'
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_orig(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_1(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = None
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_2(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(None)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_3(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_4(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return True
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_5(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status == TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_6(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    None
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_7(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return True
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_8(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = None
            logger.info(f"Cancelled task {task_id}")
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_9(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(None)
            return True
    
    async def xǁInMemoryTaskQueueǁcancel_task__mutmut_10(self, task_id: UUID) -> bool:
        """Cancel a pending task."""
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status != TaskStatus.PENDING:
                logger.warning(
                    f"Cannot cancel task {task_id}: status is {task.status}"
                )
                return False
            
            task.status = TaskStatus.CANCELLED
            logger.info(f"Cancelled task {task_id}")
            return False
    
    xǁInMemoryTaskQueueǁcancel_task__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁcancel_task__mutmut_1': xǁInMemoryTaskQueueǁcancel_task__mutmut_1, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_2': xǁInMemoryTaskQueueǁcancel_task__mutmut_2, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_3': xǁInMemoryTaskQueueǁcancel_task__mutmut_3, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_4': xǁInMemoryTaskQueueǁcancel_task__mutmut_4, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_5': xǁInMemoryTaskQueueǁcancel_task__mutmut_5, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_6': xǁInMemoryTaskQueueǁcancel_task__mutmut_6, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_7': xǁInMemoryTaskQueueǁcancel_task__mutmut_7, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_8': xǁInMemoryTaskQueueǁcancel_task__mutmut_8, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_9': xǁInMemoryTaskQueueǁcancel_task__mutmut_9, 
        'xǁInMemoryTaskQueueǁcancel_task__mutmut_10': xǁInMemoryTaskQueueǁcancel_task__mutmut_10
    }
    
    def cancel_task(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁcancel_task__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁcancel_task__mutmut_mutants"), args, kwargs, self)
        return result 
    
    cancel_task.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁcancel_task__mutmut_orig)
    xǁInMemoryTaskQueueǁcancel_task__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁcancel_task'
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_orig(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                1 for task in self.tasks.values()
                if task.agent_type == agent_type and task.status == TaskStatus.PENDING
            )
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_1(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is not None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                1 for task in self.tasks.values()
                if task.agent_type == agent_type and task.status == TaskStatus.PENDING
            )
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_2(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                None
            )
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_3(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                2 for task in self.tasks.values()
                if task.agent_type == agent_type and task.status == TaskStatus.PENDING
            )
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_4(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                1 for task in self.tasks.values()
                if task.agent_type == agent_type or task.status == TaskStatus.PENDING
            )
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_5(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                1 for task in self.tasks.values()
                if task.agent_type != agent_type and task.status == TaskStatus.PENDING
            )
    
    async def xǁInMemoryTaskQueueǁsize__mutmut_6(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                1 for task in self.tasks.values()
                if task.agent_type == agent_type and task.status != TaskStatus.PENDING
            )
    
    xǁInMemoryTaskQueueǁsize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁsize__mutmut_1': xǁInMemoryTaskQueueǁsize__mutmut_1, 
        'xǁInMemoryTaskQueueǁsize__mutmut_2': xǁInMemoryTaskQueueǁsize__mutmut_2, 
        'xǁInMemoryTaskQueueǁsize__mutmut_3': xǁInMemoryTaskQueueǁsize__mutmut_3, 
        'xǁInMemoryTaskQueueǁsize__mutmut_4': xǁInMemoryTaskQueueǁsize__mutmut_4, 
        'xǁInMemoryTaskQueueǁsize__mutmut_5': xǁInMemoryTaskQueueǁsize__mutmut_5, 
        'xǁInMemoryTaskQueueǁsize__mutmut_6': xǁInMemoryTaskQueueǁsize__mutmut_6
    }
    
    def size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁsize__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁsize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    size.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁsize__mutmut_orig)
    xǁInMemoryTaskQueueǁsize__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁsize'
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_orig(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info("Cleared task queue")
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_1(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = None
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info("Cleared task queue")
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_2(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = None
            self.tasks.clear()
            logger.info("Cleared task queue")
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_3(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=None)
            self.tasks.clear()
            logger.info("Cleared task queue")
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_4(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info(None)
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_5(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info("XXCleared task queueXX")
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_6(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info("cleared task queue")
    
    async def xǁInMemoryTaskQueueǁclear__mutmut_7(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info("CLEARED TASK QUEUE")
    
    xǁInMemoryTaskQueueǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInMemoryTaskQueueǁclear__mutmut_1': xǁInMemoryTaskQueueǁclear__mutmut_1, 
        'xǁInMemoryTaskQueueǁclear__mutmut_2': xǁInMemoryTaskQueueǁclear__mutmut_2, 
        'xǁInMemoryTaskQueueǁclear__mutmut_3': xǁInMemoryTaskQueueǁclear__mutmut_3, 
        'xǁInMemoryTaskQueueǁclear__mutmut_4': xǁInMemoryTaskQueueǁclear__mutmut_4, 
        'xǁInMemoryTaskQueueǁclear__mutmut_5': xǁInMemoryTaskQueueǁclear__mutmut_5, 
        'xǁInMemoryTaskQueueǁclear__mutmut_6': xǁInMemoryTaskQueueǁclear__mutmut_6, 
        'xǁInMemoryTaskQueueǁclear__mutmut_7': xǁInMemoryTaskQueueǁclear__mutmut_7
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInMemoryTaskQueueǁclear__mutmut_orig"), object.__getattribute__(self, "xǁInMemoryTaskQueueǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁInMemoryTaskQueueǁclear__mutmut_orig)
    xǁInMemoryTaskQueueǁclear__mutmut_orig.__name__ = 'xǁInMemoryTaskQueueǁclear'


class TaskExecutor:
    """
    Executes tasks from a queue.
    
    Manages task execution, retries, timeouts, and result collection.
    """
    
    def xǁTaskExecutorǁ__init____mutmut_orig(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_1(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 11,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_2(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = None
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_3(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = None
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_4(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = None
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_5(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = None
        self.is_running = False
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_6(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = None
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_7(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = True
        logger.info(
            f"TaskExecutor initialized (max_concurrent={max_concurrent_tasks})"
        )
    
    def xǁTaskExecutorǁ__init____mutmut_8(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 10,
    ):
        """
        Initialize task executor.
        
        Args:
            queue: Task queue to pull from
            max_concurrent_tasks: Maximum concurrent task executions
        """
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[UUID, asyncio.Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
        logger.info(
            None
        )
    
    xǁTaskExecutorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁ__init____mutmut_1': xǁTaskExecutorǁ__init____mutmut_1, 
        'xǁTaskExecutorǁ__init____mutmut_2': xǁTaskExecutorǁ__init____mutmut_2, 
        'xǁTaskExecutorǁ__init____mutmut_3': xǁTaskExecutorǁ__init____mutmut_3, 
        'xǁTaskExecutorǁ__init____mutmut_4': xǁTaskExecutorǁ__init____mutmut_4, 
        'xǁTaskExecutorǁ__init____mutmut_5': xǁTaskExecutorǁ__init____mutmut_5, 
        'xǁTaskExecutorǁ__init____mutmut_6': xǁTaskExecutorǁ__init____mutmut_6, 
        'xǁTaskExecutorǁ__init____mutmut_7': xǁTaskExecutorǁ__init____mutmut_7, 
        'xǁTaskExecutorǁ__init____mutmut_8': xǁTaskExecutorǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTaskExecutorǁ__init____mutmut_orig)
    xǁTaskExecutorǁ__init____mutmut_orig.__name__ = 'xǁTaskExecutorǁ__init__'
    
    def xǁTaskExecutorǁregister_handler__mutmut_orig(
        self,
        task_type: str,
        handler: Callable[[Task], Any],
    ) -> None:
        """
        Register a handler for a task type.
        
        Args:
            task_type: Type of task to handle
            handler: Handler function (can be async)
        """
        self.handlers[task_type] = handler
        logger.debug(f"Registered handler for task type: {task_type}")
    
    def xǁTaskExecutorǁregister_handler__mutmut_1(
        self,
        task_type: str,
        handler: Callable[[Task], Any],
    ) -> None:
        """
        Register a handler for a task type.
        
        Args:
            task_type: Type of task to handle
            handler: Handler function (can be async)
        """
        self.handlers[task_type] = None
        logger.debug(f"Registered handler for task type: {task_type}")
    
    def xǁTaskExecutorǁregister_handler__mutmut_2(
        self,
        task_type: str,
        handler: Callable[[Task], Any],
    ) -> None:
        """
        Register a handler for a task type.
        
        Args:
            task_type: Type of task to handle
            handler: Handler function (can be async)
        """
        self.handlers[task_type] = handler
        logger.debug(None)
    
    xǁTaskExecutorǁregister_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁregister_handler__mutmut_1': xǁTaskExecutorǁregister_handler__mutmut_1, 
        'xǁTaskExecutorǁregister_handler__mutmut_2': xǁTaskExecutorǁregister_handler__mutmut_2
    }
    
    def register_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁregister_handler__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁregister_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_handler.__signature__ = _mutmut_signature(xǁTaskExecutorǁregister_handler__mutmut_orig)
    xǁTaskExecutorǁregister_handler__mutmut_orig.__name__ = 'xǁTaskExecutorǁregister_handler'
    
    async def xǁTaskExecutorǁexecute_task__mutmut_orig(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_1(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_2(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(None)
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_3(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = None
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_4(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = None
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_5(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = None
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_6(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            None
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_7(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = None
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_8(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    None,
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_9(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=None,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_10(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_11(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_12(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(None, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_13(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, None),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_14(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_15(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, ),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_16(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = None
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_17(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(None, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_18(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, None)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_19(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_20(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, )
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_21(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = None
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_22(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = None
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_23(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = None
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_24(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(None)
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_25(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = None
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_26(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = None
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_27(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(None)
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_28(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = None
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_29(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = None
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_30(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(None)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_31(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count = 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_32(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count -= 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_33(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 2
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_34(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                None,
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_35(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=None,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_36(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_37(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_38(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=False,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_39(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count <= task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_40(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    None
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_41(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = None
                await self.queue.enqueue(task)
            
            raise
    
    async def xǁTaskExecutorǁexecute_task__mutmut_42(self, task: Task) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
            
        Raises:
            ValueError: If no handler for task type
            Exception: If task execution fails
        """
        if task.task_type not in self.handlers:
            raise ValueError(f"No handler for task type: {task.task_type}")
        
        handler = self.handlers[task.task_type]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info(
            f"Executing task {task.id} ({task.task_type}) "
            f"for {task.agent_type.value}"
        )
        
        try:
            # Execute with timeout if specified
            if task.timeout_seconds:
                result = await asyncio.wait_for(
                    self._call_handler(handler, task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = await self._call_handler(handler, task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            logger.info(f"Task {task.id} completed successfully")
            
            return result
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Task timed out after {task.timeout_seconds}s"
            logger.error(f"Task {task.id} timed out")
            raise
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error(
                f"Task {task.id} failed (attempt {task.retry_count}): {e}",
                exc_info=True,
            )
            
            # Retry if within limit
            if task.retry_count < task.max_retries:
                logger.info(
                    f"Retrying task {task.id} "
                    f"({task.retry_count}/{task.max_retries})"
                )
                task.status = TaskStatus.PENDING
                await self.queue.enqueue(None)
            
            raise
    
    xǁTaskExecutorǁexecute_task__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁexecute_task__mutmut_1': xǁTaskExecutorǁexecute_task__mutmut_1, 
        'xǁTaskExecutorǁexecute_task__mutmut_2': xǁTaskExecutorǁexecute_task__mutmut_2, 
        'xǁTaskExecutorǁexecute_task__mutmut_3': xǁTaskExecutorǁexecute_task__mutmut_3, 
        'xǁTaskExecutorǁexecute_task__mutmut_4': xǁTaskExecutorǁexecute_task__mutmut_4, 
        'xǁTaskExecutorǁexecute_task__mutmut_5': xǁTaskExecutorǁexecute_task__mutmut_5, 
        'xǁTaskExecutorǁexecute_task__mutmut_6': xǁTaskExecutorǁexecute_task__mutmut_6, 
        'xǁTaskExecutorǁexecute_task__mutmut_7': xǁTaskExecutorǁexecute_task__mutmut_7, 
        'xǁTaskExecutorǁexecute_task__mutmut_8': xǁTaskExecutorǁexecute_task__mutmut_8, 
        'xǁTaskExecutorǁexecute_task__mutmut_9': xǁTaskExecutorǁexecute_task__mutmut_9, 
        'xǁTaskExecutorǁexecute_task__mutmut_10': xǁTaskExecutorǁexecute_task__mutmut_10, 
        'xǁTaskExecutorǁexecute_task__mutmut_11': xǁTaskExecutorǁexecute_task__mutmut_11, 
        'xǁTaskExecutorǁexecute_task__mutmut_12': xǁTaskExecutorǁexecute_task__mutmut_12, 
        'xǁTaskExecutorǁexecute_task__mutmut_13': xǁTaskExecutorǁexecute_task__mutmut_13, 
        'xǁTaskExecutorǁexecute_task__mutmut_14': xǁTaskExecutorǁexecute_task__mutmut_14, 
        'xǁTaskExecutorǁexecute_task__mutmut_15': xǁTaskExecutorǁexecute_task__mutmut_15, 
        'xǁTaskExecutorǁexecute_task__mutmut_16': xǁTaskExecutorǁexecute_task__mutmut_16, 
        'xǁTaskExecutorǁexecute_task__mutmut_17': xǁTaskExecutorǁexecute_task__mutmut_17, 
        'xǁTaskExecutorǁexecute_task__mutmut_18': xǁTaskExecutorǁexecute_task__mutmut_18, 
        'xǁTaskExecutorǁexecute_task__mutmut_19': xǁTaskExecutorǁexecute_task__mutmut_19, 
        'xǁTaskExecutorǁexecute_task__mutmut_20': xǁTaskExecutorǁexecute_task__mutmut_20, 
        'xǁTaskExecutorǁexecute_task__mutmut_21': xǁTaskExecutorǁexecute_task__mutmut_21, 
        'xǁTaskExecutorǁexecute_task__mutmut_22': xǁTaskExecutorǁexecute_task__mutmut_22, 
        'xǁTaskExecutorǁexecute_task__mutmut_23': xǁTaskExecutorǁexecute_task__mutmut_23, 
        'xǁTaskExecutorǁexecute_task__mutmut_24': xǁTaskExecutorǁexecute_task__mutmut_24, 
        'xǁTaskExecutorǁexecute_task__mutmut_25': xǁTaskExecutorǁexecute_task__mutmut_25, 
        'xǁTaskExecutorǁexecute_task__mutmut_26': xǁTaskExecutorǁexecute_task__mutmut_26, 
        'xǁTaskExecutorǁexecute_task__mutmut_27': xǁTaskExecutorǁexecute_task__mutmut_27, 
        'xǁTaskExecutorǁexecute_task__mutmut_28': xǁTaskExecutorǁexecute_task__mutmut_28, 
        'xǁTaskExecutorǁexecute_task__mutmut_29': xǁTaskExecutorǁexecute_task__mutmut_29, 
        'xǁTaskExecutorǁexecute_task__mutmut_30': xǁTaskExecutorǁexecute_task__mutmut_30, 
        'xǁTaskExecutorǁexecute_task__mutmut_31': xǁTaskExecutorǁexecute_task__mutmut_31, 
        'xǁTaskExecutorǁexecute_task__mutmut_32': xǁTaskExecutorǁexecute_task__mutmut_32, 
        'xǁTaskExecutorǁexecute_task__mutmut_33': xǁTaskExecutorǁexecute_task__mutmut_33, 
        'xǁTaskExecutorǁexecute_task__mutmut_34': xǁTaskExecutorǁexecute_task__mutmut_34, 
        'xǁTaskExecutorǁexecute_task__mutmut_35': xǁTaskExecutorǁexecute_task__mutmut_35, 
        'xǁTaskExecutorǁexecute_task__mutmut_36': xǁTaskExecutorǁexecute_task__mutmut_36, 
        'xǁTaskExecutorǁexecute_task__mutmut_37': xǁTaskExecutorǁexecute_task__mutmut_37, 
        'xǁTaskExecutorǁexecute_task__mutmut_38': xǁTaskExecutorǁexecute_task__mutmut_38, 
        'xǁTaskExecutorǁexecute_task__mutmut_39': xǁTaskExecutorǁexecute_task__mutmut_39, 
        'xǁTaskExecutorǁexecute_task__mutmut_40': xǁTaskExecutorǁexecute_task__mutmut_40, 
        'xǁTaskExecutorǁexecute_task__mutmut_41': xǁTaskExecutorǁexecute_task__mutmut_41, 
        'xǁTaskExecutorǁexecute_task__mutmut_42': xǁTaskExecutorǁexecute_task__mutmut_42
    }
    
    def execute_task(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁexecute_task__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁexecute_task__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute_task.__signature__ = _mutmut_signature(xǁTaskExecutorǁexecute_task__mutmut_orig)
    xǁTaskExecutorǁexecute_task__mutmut_orig.__name__ = 'xǁTaskExecutorǁexecute_task'
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_orig(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(result, '__await__'):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_1(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = None
        
        # If result is awaitable, await it
        if hasattr(result, '__await__'):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_2(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(None)
        
        # If result is awaitable, await it
        if hasattr(result, '__await__'):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_3(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(None, '__await__'):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_4(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(result, None):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_5(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr('__await__'):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_6(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(result, ):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_7(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(result, 'XX__await__XX'):
            return await result
        
        return result
    
    async def xǁTaskExecutorǁ_call_handler__mutmut_8(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(result, '__AWAIT__'):
            return await result
        
        return result
    
    xǁTaskExecutorǁ_call_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁ_call_handler__mutmut_1': xǁTaskExecutorǁ_call_handler__mutmut_1, 
        'xǁTaskExecutorǁ_call_handler__mutmut_2': xǁTaskExecutorǁ_call_handler__mutmut_2, 
        'xǁTaskExecutorǁ_call_handler__mutmut_3': xǁTaskExecutorǁ_call_handler__mutmut_3, 
        'xǁTaskExecutorǁ_call_handler__mutmut_4': xǁTaskExecutorǁ_call_handler__mutmut_4, 
        'xǁTaskExecutorǁ_call_handler__mutmut_5': xǁTaskExecutorǁ_call_handler__mutmut_5, 
        'xǁTaskExecutorǁ_call_handler__mutmut_6': xǁTaskExecutorǁ_call_handler__mutmut_6, 
        'xǁTaskExecutorǁ_call_handler__mutmut_7': xǁTaskExecutorǁ_call_handler__mutmut_7, 
        'xǁTaskExecutorǁ_call_handler__mutmut_8': xǁTaskExecutorǁ_call_handler__mutmut_8
    }
    
    def _call_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁ_call_handler__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁ_call_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _call_handler.__signature__ = _mutmut_signature(xǁTaskExecutorǁ_call_handler__mutmut_orig)
    xǁTaskExecutorǁ_call_handler__mutmut_orig.__name__ = 'xǁTaskExecutorǁ_call_handler'
    
    async def xǁTaskExecutorǁstart__mutmut_orig(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_1(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning(None)
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_2(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("XXTaskExecutor already runningXX")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_3(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("taskexecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_4(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TASKEXECUTOR ALREADY RUNNING")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_5(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = None
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_6(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = False
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_7(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info(None)
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_8(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("XXTaskExecutor startedXX")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_9(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("taskexecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_10(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TASKEXECUTOR STARTED")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_11(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) > self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_12(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(None)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_13(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(1.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_14(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    break
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_15(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = None
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_16(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_17(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(None)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_18(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(1.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_19(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    break
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_20(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = None
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_21(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(None)
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_22(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(None))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_23(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = None
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_24(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(None, exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_25(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=None)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_26(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(exc_info=True)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_27(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", )
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_28(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=False)
                await asyncio.sleep(1)
    
    async def xǁTaskExecutorǁstart__mutmut_29(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(None)
    
    async def xǁTaskExecutorǁstart__mutmut_30(self) -> None:
        """Start processing tasks from the queue."""
        if self.is_running:
            logger.warning("TaskExecutor already running")
            return
        
        self.is_running = True
        logger.info("TaskExecutor started")
        
        while self.is_running:
            try:
                # Check if we can accept more tasks
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue
                
                # Get next task
                task = await self.queue.dequeue()
                
                if not task:
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute task in background
                async_task = asyncio.create_task(self.execute_task(task))
                self.running_tasks[task.id] = async_task
                
                # Clean up completed tasks
                self._cleanup_completed_tasks()
            
            except Exception as e:
                logger.error(f"Error in task executor loop: {e}", exc_info=True)
                await asyncio.sleep(2)
    
    xǁTaskExecutorǁstart__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁstart__mutmut_1': xǁTaskExecutorǁstart__mutmut_1, 
        'xǁTaskExecutorǁstart__mutmut_2': xǁTaskExecutorǁstart__mutmut_2, 
        'xǁTaskExecutorǁstart__mutmut_3': xǁTaskExecutorǁstart__mutmut_3, 
        'xǁTaskExecutorǁstart__mutmut_4': xǁTaskExecutorǁstart__mutmut_4, 
        'xǁTaskExecutorǁstart__mutmut_5': xǁTaskExecutorǁstart__mutmut_5, 
        'xǁTaskExecutorǁstart__mutmut_6': xǁTaskExecutorǁstart__mutmut_6, 
        'xǁTaskExecutorǁstart__mutmut_7': xǁTaskExecutorǁstart__mutmut_7, 
        'xǁTaskExecutorǁstart__mutmut_8': xǁTaskExecutorǁstart__mutmut_8, 
        'xǁTaskExecutorǁstart__mutmut_9': xǁTaskExecutorǁstart__mutmut_9, 
        'xǁTaskExecutorǁstart__mutmut_10': xǁTaskExecutorǁstart__mutmut_10, 
        'xǁTaskExecutorǁstart__mutmut_11': xǁTaskExecutorǁstart__mutmut_11, 
        'xǁTaskExecutorǁstart__mutmut_12': xǁTaskExecutorǁstart__mutmut_12, 
        'xǁTaskExecutorǁstart__mutmut_13': xǁTaskExecutorǁstart__mutmut_13, 
        'xǁTaskExecutorǁstart__mutmut_14': xǁTaskExecutorǁstart__mutmut_14, 
        'xǁTaskExecutorǁstart__mutmut_15': xǁTaskExecutorǁstart__mutmut_15, 
        'xǁTaskExecutorǁstart__mutmut_16': xǁTaskExecutorǁstart__mutmut_16, 
        'xǁTaskExecutorǁstart__mutmut_17': xǁTaskExecutorǁstart__mutmut_17, 
        'xǁTaskExecutorǁstart__mutmut_18': xǁTaskExecutorǁstart__mutmut_18, 
        'xǁTaskExecutorǁstart__mutmut_19': xǁTaskExecutorǁstart__mutmut_19, 
        'xǁTaskExecutorǁstart__mutmut_20': xǁTaskExecutorǁstart__mutmut_20, 
        'xǁTaskExecutorǁstart__mutmut_21': xǁTaskExecutorǁstart__mutmut_21, 
        'xǁTaskExecutorǁstart__mutmut_22': xǁTaskExecutorǁstart__mutmut_22, 
        'xǁTaskExecutorǁstart__mutmut_23': xǁTaskExecutorǁstart__mutmut_23, 
        'xǁTaskExecutorǁstart__mutmut_24': xǁTaskExecutorǁstart__mutmut_24, 
        'xǁTaskExecutorǁstart__mutmut_25': xǁTaskExecutorǁstart__mutmut_25, 
        'xǁTaskExecutorǁstart__mutmut_26': xǁTaskExecutorǁstart__mutmut_26, 
        'xǁTaskExecutorǁstart__mutmut_27': xǁTaskExecutorǁstart__mutmut_27, 
        'xǁTaskExecutorǁstart__mutmut_28': xǁTaskExecutorǁstart__mutmut_28, 
        'xǁTaskExecutorǁstart__mutmut_29': xǁTaskExecutorǁstart__mutmut_29, 
        'xǁTaskExecutorǁstart__mutmut_30': xǁTaskExecutorǁstart__mutmut_30
    }
    
    def start(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁstart__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁstart__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start.__signature__ = _mutmut_signature(xǁTaskExecutorǁstart__mutmut_orig)
    xǁTaskExecutorǁstart__mutmut_orig.__name__ = 'xǁTaskExecutorǁstart'
    
    def xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_orig(self) -> None:
        """Remove completed tasks from running_tasks dict."""
        completed = [
            task_id
            for task_id, async_task in self.running_tasks.items()
            if async_task.done()
        ]
        
        for task_id in completed:
            del self.running_tasks[task_id]
    
    def xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_1(self) -> None:
        """Remove completed tasks from running_tasks dict."""
        completed = None
        
        for task_id in completed:
            del self.running_tasks[task_id]
    
    xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_1': xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_1
    }
    
    def _cleanup_completed_tasks(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _cleanup_completed_tasks.__signature__ = _mutmut_signature(xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_orig)
    xǁTaskExecutorǁ_cleanup_completed_tasks__mutmut_orig.__name__ = 'xǁTaskExecutorǁ_cleanup_completed_tasks'
    
    async def xǁTaskExecutorǁstop__mutmut_orig(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_1(self) -> None:
        """Stop processing tasks."""
        if self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_2(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = None
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_3(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = True
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_4(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                None
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_5(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=None,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_6(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                return_exceptions=True,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_7(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_8(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=False,
            )
        
        logger.info("TaskExecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_9(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info(None)
    
    async def xǁTaskExecutorǁstop__mutmut_10(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("XXTaskExecutor stoppedXX")
    
    async def xǁTaskExecutorǁstop__mutmut_11(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("taskexecutor stopped")
    
    async def xǁTaskExecutorǁstop__mutmut_12(self) -> None:
        """Stop processing tasks."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            logger.info(
                f"Waiting for {len(self.running_tasks)} tasks to complete..."
            )
            await asyncio.gather(
                *self.running_tasks.values(),
                return_exceptions=True,
            )
        
        logger.info("TASKEXECUTOR STOPPED")
    
    xǁTaskExecutorǁstop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁstop__mutmut_1': xǁTaskExecutorǁstop__mutmut_1, 
        'xǁTaskExecutorǁstop__mutmut_2': xǁTaskExecutorǁstop__mutmut_2, 
        'xǁTaskExecutorǁstop__mutmut_3': xǁTaskExecutorǁstop__mutmut_3, 
        'xǁTaskExecutorǁstop__mutmut_4': xǁTaskExecutorǁstop__mutmut_4, 
        'xǁTaskExecutorǁstop__mutmut_5': xǁTaskExecutorǁstop__mutmut_5, 
        'xǁTaskExecutorǁstop__mutmut_6': xǁTaskExecutorǁstop__mutmut_6, 
        'xǁTaskExecutorǁstop__mutmut_7': xǁTaskExecutorǁstop__mutmut_7, 
        'xǁTaskExecutorǁstop__mutmut_8': xǁTaskExecutorǁstop__mutmut_8, 
        'xǁTaskExecutorǁstop__mutmut_9': xǁTaskExecutorǁstop__mutmut_9, 
        'xǁTaskExecutorǁstop__mutmut_10': xǁTaskExecutorǁstop__mutmut_10, 
        'xǁTaskExecutorǁstop__mutmut_11': xǁTaskExecutorǁstop__mutmut_11, 
        'xǁTaskExecutorǁstop__mutmut_12': xǁTaskExecutorǁstop__mutmut_12
    }
    
    def stop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁstop__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁstop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop.__signature__ = _mutmut_signature(xǁTaskExecutorǁstop__mutmut_orig)
    xǁTaskExecutorǁstop__mutmut_orig.__name__ = 'xǁTaskExecutorǁstop'
    
    def xǁTaskExecutorǁget_statistics__mutmut_orig(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "running_tasks": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_1(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "XXis_runningXX": self.is_running,
            "running_tasks": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_2(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "IS_RUNNING": self.is_running,
            "running_tasks": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_3(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "XXrunning_tasksXX": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_4(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "RUNNING_TASKS": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_5(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "running_tasks": len(self.running_tasks),
            "XXmax_concurrent_tasksXX": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_6(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "running_tasks": len(self.running_tasks),
            "MAX_CONCURRENT_TASKS": self.max_concurrent_tasks,
            "registered_handlers": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_7(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "running_tasks": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "XXregistered_handlersXX": len(self.handlers),
        }
    
    def xǁTaskExecutorǁget_statistics__mutmut_8(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "is_running": self.is_running,
            "running_tasks": len(self.running_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "REGISTERED_HANDLERS": len(self.handlers),
        }
    
    xǁTaskExecutorǁget_statistics__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskExecutorǁget_statistics__mutmut_1': xǁTaskExecutorǁget_statistics__mutmut_1, 
        'xǁTaskExecutorǁget_statistics__mutmut_2': xǁTaskExecutorǁget_statistics__mutmut_2, 
        'xǁTaskExecutorǁget_statistics__mutmut_3': xǁTaskExecutorǁget_statistics__mutmut_3, 
        'xǁTaskExecutorǁget_statistics__mutmut_4': xǁTaskExecutorǁget_statistics__mutmut_4, 
        'xǁTaskExecutorǁget_statistics__mutmut_5': xǁTaskExecutorǁget_statistics__mutmut_5, 
        'xǁTaskExecutorǁget_statistics__mutmut_6': xǁTaskExecutorǁget_statistics__mutmut_6, 
        'xǁTaskExecutorǁget_statistics__mutmut_7': xǁTaskExecutorǁget_statistics__mutmut_7, 
        'xǁTaskExecutorǁget_statistics__mutmut_8': xǁTaskExecutorǁget_statistics__mutmut_8
    }
    
    def get_statistics(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskExecutorǁget_statistics__mutmut_orig"), object.__getattribute__(self, "xǁTaskExecutorǁget_statistics__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_statistics.__signature__ = _mutmut_signature(xǁTaskExecutorǁget_statistics__mutmut_orig)
    xǁTaskExecutorǁget_statistics__mutmut_orig.__name__ = 'xǁTaskExecutorǁget_statistics'


class TaskBuilder:
    """
    Builder pattern for constructing tasks.
    
    Provides a fluent interface for creating tasks.
    """
    
    def xǁTaskBuilderǁ__init____mutmut_orig(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_1(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = ""
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_2(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = ""
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_3(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = None
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_4(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = ""
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_5(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = None
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_6(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = None
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_7(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 4
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_8(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = ""
        self._message_id: Optional[UUID] = None
    
    def xǁTaskBuilderǁ__init____mutmut_9(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = ""
    
    xǁTaskBuilderǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁ__init____mutmut_1': xǁTaskBuilderǁ__init____mutmut_1, 
        'xǁTaskBuilderǁ__init____mutmut_2': xǁTaskBuilderǁ__init____mutmut_2, 
        'xǁTaskBuilderǁ__init____mutmut_3': xǁTaskBuilderǁ__init____mutmut_3, 
        'xǁTaskBuilderǁ__init____mutmut_4': xǁTaskBuilderǁ__init____mutmut_4, 
        'xǁTaskBuilderǁ__init____mutmut_5': xǁTaskBuilderǁ__init____mutmut_5, 
        'xǁTaskBuilderǁ__init____mutmut_6': xǁTaskBuilderǁ__init____mutmut_6, 
        'xǁTaskBuilderǁ__init____mutmut_7': xǁTaskBuilderǁ__init____mutmut_7, 
        'xǁTaskBuilderǁ__init____mutmut_8': xǁTaskBuilderǁ__init____mutmut_8, 
        'xǁTaskBuilderǁ__init____mutmut_9': xǁTaskBuilderǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTaskBuilderǁ__init____mutmut_orig)
    xǁTaskBuilderǁ__init____mutmut_orig.__name__ = 'xǁTaskBuilderǁ__init__'
    
    def xǁTaskBuilderǁfor_agent__mutmut_orig(self, agent: AgentType) -> 'TaskBuilder':
        """Set the target agent."""
        self._agent_type = agent
        return self
    
    def xǁTaskBuilderǁfor_agent__mutmut_1(self, agent: AgentType) -> 'TaskBuilder':
        """Set the target agent."""
        self._agent_type = None
        return self
    
    xǁTaskBuilderǁfor_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁfor_agent__mutmut_1': xǁTaskBuilderǁfor_agent__mutmut_1
    }
    
    def for_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁfor_agent__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁfor_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    for_agent.__signature__ = _mutmut_signature(xǁTaskBuilderǁfor_agent__mutmut_orig)
    xǁTaskBuilderǁfor_agent__mutmut_orig.__name__ = 'xǁTaskBuilderǁfor_agent'
    
    def xǁTaskBuilderǁof_type__mutmut_orig(self, task_type: str) -> 'TaskBuilder':
        """Set the task type."""
        self._task_type = task_type
        return self
    
    def xǁTaskBuilderǁof_type__mutmut_1(self, task_type: str) -> 'TaskBuilder':
        """Set the task type."""
        self._task_type = None
        return self
    
    xǁTaskBuilderǁof_type__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁof_type__mutmut_1': xǁTaskBuilderǁof_type__mutmut_1
    }
    
    def of_type(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁof_type__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁof_type__mutmut_mutants"), args, kwargs, self)
        return result 
    
    of_type.__signature__ = _mutmut_signature(xǁTaskBuilderǁof_type__mutmut_orig)
    xǁTaskBuilderǁof_type__mutmut_orig.__name__ = 'xǁTaskBuilderǁof_type'
    
    def xǁTaskBuilderǁwith_payload__mutmut_orig(self, payload: Dict[str, Any]) -> 'TaskBuilder':
        """Set the payload."""
        self._payload = payload
        return self
    
    def xǁTaskBuilderǁwith_payload__mutmut_1(self, payload: Dict[str, Any]) -> 'TaskBuilder':
        """Set the payload."""
        self._payload = None
        return self
    
    xǁTaskBuilderǁwith_payload__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁwith_payload__mutmut_1': xǁTaskBuilderǁwith_payload__mutmut_1
    }
    
    def with_payload(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁwith_payload__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁwith_payload__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_payload.__signature__ = _mutmut_signature(xǁTaskBuilderǁwith_payload__mutmut_orig)
    xǁTaskBuilderǁwith_payload__mutmut_orig.__name__ = 'xǁTaskBuilderǁwith_payload'
    
    def xǁTaskBuilderǁadd_to_payload__mutmut_orig(self, key: str, value: Any) -> 'TaskBuilder':
        """Add a key-value pair to the payload."""
        self._payload[key] = value
        return self
    
    def xǁTaskBuilderǁadd_to_payload__mutmut_1(self, key: str, value: Any) -> 'TaskBuilder':
        """Add a key-value pair to the payload."""
        self._payload[key] = None
        return self
    
    xǁTaskBuilderǁadd_to_payload__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁadd_to_payload__mutmut_1': xǁTaskBuilderǁadd_to_payload__mutmut_1
    }
    
    def add_to_payload(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁadd_to_payload__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁadd_to_payload__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_to_payload.__signature__ = _mutmut_signature(xǁTaskBuilderǁadd_to_payload__mutmut_orig)
    xǁTaskBuilderǁadd_to_payload__mutmut_orig.__name__ = 'xǁTaskBuilderǁadd_to_payload'
    
    def xǁTaskBuilderǁfor_session__mutmut_orig(self, session_id: UUID) -> 'TaskBuilder':
        """Set the session ID."""
        self._session_id = session_id
        return self
    
    def xǁTaskBuilderǁfor_session__mutmut_1(self, session_id: UUID) -> 'TaskBuilder':
        """Set the session ID."""
        self._session_id = None
        return self
    
    xǁTaskBuilderǁfor_session__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁfor_session__mutmut_1': xǁTaskBuilderǁfor_session__mutmut_1
    }
    
    def for_session(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁfor_session__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁfor_session__mutmut_mutants"), args, kwargs, self)
        return result 
    
    for_session.__signature__ = _mutmut_signature(xǁTaskBuilderǁfor_session__mutmut_orig)
    xǁTaskBuilderǁfor_session__mutmut_orig.__name__ = 'xǁTaskBuilderǁfor_session'
    
    def xǁTaskBuilderǁwith_priority__mutmut_orig(self, priority: TaskPriority) -> 'TaskBuilder':
        """Set the priority."""
        self._priority = priority
        return self
    
    def xǁTaskBuilderǁwith_priority__mutmut_1(self, priority: TaskPriority) -> 'TaskBuilder':
        """Set the priority."""
        self._priority = None
        return self
    
    xǁTaskBuilderǁwith_priority__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁwith_priority__mutmut_1': xǁTaskBuilderǁwith_priority__mutmut_1
    }
    
    def with_priority(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁwith_priority__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁwith_priority__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_priority.__signature__ = _mutmut_signature(xǁTaskBuilderǁwith_priority__mutmut_orig)
    xǁTaskBuilderǁwith_priority__mutmut_orig.__name__ = 'xǁTaskBuilderǁwith_priority'
    
    def xǁTaskBuilderǁwith_retries__mutmut_orig(self, max_retries: int) -> 'TaskBuilder':
        """Set maximum retries."""
        self._max_retries = max_retries
        return self
    
    def xǁTaskBuilderǁwith_retries__mutmut_1(self, max_retries: int) -> 'TaskBuilder':
        """Set maximum retries."""
        self._max_retries = None
        return self
    
    xǁTaskBuilderǁwith_retries__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁwith_retries__mutmut_1': xǁTaskBuilderǁwith_retries__mutmut_1
    }
    
    def with_retries(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁwith_retries__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁwith_retries__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_retries.__signature__ = _mutmut_signature(xǁTaskBuilderǁwith_retries__mutmut_orig)
    xǁTaskBuilderǁwith_retries__mutmut_orig.__name__ = 'xǁTaskBuilderǁwith_retries'
    
    def xǁTaskBuilderǁwith_timeout__mutmut_orig(self, timeout_seconds: float) -> 'TaskBuilder':
        """Set timeout in seconds."""
        self._timeout_seconds = timeout_seconds
        return self
    
    def xǁTaskBuilderǁwith_timeout__mutmut_1(self, timeout_seconds: float) -> 'TaskBuilder':
        """Set timeout in seconds."""
        self._timeout_seconds = None
        return self
    
    xǁTaskBuilderǁwith_timeout__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁwith_timeout__mutmut_1': xǁTaskBuilderǁwith_timeout__mutmut_1
    }
    
    def with_timeout(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁwith_timeout__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁwith_timeout__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_timeout.__signature__ = _mutmut_signature(xǁTaskBuilderǁwith_timeout__mutmut_orig)
    xǁTaskBuilderǁwith_timeout__mutmut_orig.__name__ = 'xǁTaskBuilderǁwith_timeout'
    
    def xǁTaskBuilderǁfrom_message__mutmut_orig(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = TaskPriority(message.priority)
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_1(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = None
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = TaskPriority(message.priority)
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_2(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = None
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = TaskPriority(message.priority)
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_3(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = None
        self._session_id = message.session_id
        self._priority = TaskPriority(message.priority)
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_4(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = None
        self._priority = TaskPriority(message.priority)
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_5(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = None
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_6(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = TaskPriority(None)
        self._message_id = message.id
        return self
    
    def xǁTaskBuilderǁfrom_message__mutmut_7(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = TaskPriority(message.priority)
        self._message_id = None
        return self
    
    xǁTaskBuilderǁfrom_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁfrom_message__mutmut_1': xǁTaskBuilderǁfrom_message__mutmut_1, 
        'xǁTaskBuilderǁfrom_message__mutmut_2': xǁTaskBuilderǁfrom_message__mutmut_2, 
        'xǁTaskBuilderǁfrom_message__mutmut_3': xǁTaskBuilderǁfrom_message__mutmut_3, 
        'xǁTaskBuilderǁfrom_message__mutmut_4': xǁTaskBuilderǁfrom_message__mutmut_4, 
        'xǁTaskBuilderǁfrom_message__mutmut_5': xǁTaskBuilderǁfrom_message__mutmut_5, 
        'xǁTaskBuilderǁfrom_message__mutmut_6': xǁTaskBuilderǁfrom_message__mutmut_6, 
        'xǁTaskBuilderǁfrom_message__mutmut_7': xǁTaskBuilderǁfrom_message__mutmut_7
    }
    
    def from_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁfrom_message__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁfrom_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    from_message.__signature__ = _mutmut_signature(xǁTaskBuilderǁfrom_message__mutmut_orig)
    xǁTaskBuilderǁfrom_message__mutmut_orig.__name__ = 'xǁTaskBuilderǁfrom_message'
    
    def xǁTaskBuilderǁbuild__mutmut_orig(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_1(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_2(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError(None)
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_3(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("XXagent_type is requiredXX")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_4(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("AGENT_TYPE IS REQUIRED")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_5(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_6(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError(None)
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_7(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("XXtask_type is requiredXX")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_8(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("TASK_TYPE IS REQUIRED")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_9(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_10(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError(None)
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_11(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("XXsession_id is requiredXX")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_12(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("SESSION_ID IS REQUIRED")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_13(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=None,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_14(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=None,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_15(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=None,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_16(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=None,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_17(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=None,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_18(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=None,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_19(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=None,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_20(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=None,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_21(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_22(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_23(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_24(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_25(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_26(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            timeout_seconds=self._timeout_seconds,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_27(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            message_id=self._message_id,
        )
    
    def xǁTaskBuilderǁbuild__mutmut_28(self) -> Task:
        """
        Build the task.
        
        Returns:
            Constructed task
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._agent_type:
            raise ValueError("agent_type is required")
        if not self._task_type:
            raise ValueError("task_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return Task(
            agent_type=self._agent_type,
            task_type=self._task_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            max_retries=self._max_retries,
            timeout_seconds=self._timeout_seconds,
            )
    
    xǁTaskBuilderǁbuild__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁbuild__mutmut_1': xǁTaskBuilderǁbuild__mutmut_1, 
        'xǁTaskBuilderǁbuild__mutmut_2': xǁTaskBuilderǁbuild__mutmut_2, 
        'xǁTaskBuilderǁbuild__mutmut_3': xǁTaskBuilderǁbuild__mutmut_3, 
        'xǁTaskBuilderǁbuild__mutmut_4': xǁTaskBuilderǁbuild__mutmut_4, 
        'xǁTaskBuilderǁbuild__mutmut_5': xǁTaskBuilderǁbuild__mutmut_5, 
        'xǁTaskBuilderǁbuild__mutmut_6': xǁTaskBuilderǁbuild__mutmut_6, 
        'xǁTaskBuilderǁbuild__mutmut_7': xǁTaskBuilderǁbuild__mutmut_7, 
        'xǁTaskBuilderǁbuild__mutmut_8': xǁTaskBuilderǁbuild__mutmut_8, 
        'xǁTaskBuilderǁbuild__mutmut_9': xǁTaskBuilderǁbuild__mutmut_9, 
        'xǁTaskBuilderǁbuild__mutmut_10': xǁTaskBuilderǁbuild__mutmut_10, 
        'xǁTaskBuilderǁbuild__mutmut_11': xǁTaskBuilderǁbuild__mutmut_11, 
        'xǁTaskBuilderǁbuild__mutmut_12': xǁTaskBuilderǁbuild__mutmut_12, 
        'xǁTaskBuilderǁbuild__mutmut_13': xǁTaskBuilderǁbuild__mutmut_13, 
        'xǁTaskBuilderǁbuild__mutmut_14': xǁTaskBuilderǁbuild__mutmut_14, 
        'xǁTaskBuilderǁbuild__mutmut_15': xǁTaskBuilderǁbuild__mutmut_15, 
        'xǁTaskBuilderǁbuild__mutmut_16': xǁTaskBuilderǁbuild__mutmut_16, 
        'xǁTaskBuilderǁbuild__mutmut_17': xǁTaskBuilderǁbuild__mutmut_17, 
        'xǁTaskBuilderǁbuild__mutmut_18': xǁTaskBuilderǁbuild__mutmut_18, 
        'xǁTaskBuilderǁbuild__mutmut_19': xǁTaskBuilderǁbuild__mutmut_19, 
        'xǁTaskBuilderǁbuild__mutmut_20': xǁTaskBuilderǁbuild__mutmut_20, 
        'xǁTaskBuilderǁbuild__mutmut_21': xǁTaskBuilderǁbuild__mutmut_21, 
        'xǁTaskBuilderǁbuild__mutmut_22': xǁTaskBuilderǁbuild__mutmut_22, 
        'xǁTaskBuilderǁbuild__mutmut_23': xǁTaskBuilderǁbuild__mutmut_23, 
        'xǁTaskBuilderǁbuild__mutmut_24': xǁTaskBuilderǁbuild__mutmut_24, 
        'xǁTaskBuilderǁbuild__mutmut_25': xǁTaskBuilderǁbuild__mutmut_25, 
        'xǁTaskBuilderǁbuild__mutmut_26': xǁTaskBuilderǁbuild__mutmut_26, 
        'xǁTaskBuilderǁbuild__mutmut_27': xǁTaskBuilderǁbuild__mutmut_27, 
        'xǁTaskBuilderǁbuild__mutmut_28': xǁTaskBuilderǁbuild__mutmut_28
    }
    
    def build(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁbuild__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁbuild__mutmut_mutants"), args, kwargs, self)
        return result 
    
    build.__signature__ = _mutmut_signature(xǁTaskBuilderǁbuild__mutmut_orig)
    xǁTaskBuilderǁbuild__mutmut_orig.__name__ = 'xǁTaskBuilderǁbuild'
    
    def xǁTaskBuilderǁreset__mutmut_orig(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_1(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = ""
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_2(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = ""
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_3(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = None
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_4(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = ""
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_5(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = None
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_6(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = None
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_7(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 4
        self._timeout_seconds = None
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_8(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = ""
        self._message_id = None
        return self
    
    def xǁTaskBuilderǁreset__mutmut_9(self) -> 'TaskBuilder':
        """Reset the builder to initial state."""
        self._agent_type = None
        self._task_type = None
        self._payload = {}
        self._session_id = None
        self._priority = TaskPriority.NORMAL
        self._max_retries = 3
        self._timeout_seconds = None
        self._message_id = ""
        return self
    
    xǁTaskBuilderǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskBuilderǁreset__mutmut_1': xǁTaskBuilderǁreset__mutmut_1, 
        'xǁTaskBuilderǁreset__mutmut_2': xǁTaskBuilderǁreset__mutmut_2, 
        'xǁTaskBuilderǁreset__mutmut_3': xǁTaskBuilderǁreset__mutmut_3, 
        'xǁTaskBuilderǁreset__mutmut_4': xǁTaskBuilderǁreset__mutmut_4, 
        'xǁTaskBuilderǁreset__mutmut_5': xǁTaskBuilderǁreset__mutmut_5, 
        'xǁTaskBuilderǁreset__mutmut_6': xǁTaskBuilderǁreset__mutmut_6, 
        'xǁTaskBuilderǁreset__mutmut_7': xǁTaskBuilderǁreset__mutmut_7, 
        'xǁTaskBuilderǁreset__mutmut_8': xǁTaskBuilderǁreset__mutmut_8, 
        'xǁTaskBuilderǁreset__mutmut_9': xǁTaskBuilderǁreset__mutmut_9
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskBuilderǁreset__mutmut_orig"), object.__getattribute__(self, "xǁTaskBuilderǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁTaskBuilderǁreset__mutmut_orig)
    xǁTaskBuilderǁreset__mutmut_orig.__name__ = 'xǁTaskBuilderǁreset'
