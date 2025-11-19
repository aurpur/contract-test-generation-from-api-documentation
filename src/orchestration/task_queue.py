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
    
    def __init__(self, maxsize: int = 0):
        """
        Initialize in-memory task queue.
        
        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self.tasks: Dict[UUID, Task] = {}
        self.lock = asyncio.Lock()
        logger.info(f"InMemoryTaskQueue initialized (maxsize={maxsize})")
    
    async def enqueue(self, task: Task) -> None:
        """Add a task to the queue."""
        async with self.lock:
            self.tasks[task.id] = task
            await self.queue.put(task)
            logger.debug(
                f"Enqueued task {task.id} for {task.agent_type.value} "
                f"(priority={-task.priority.value}, type={task.task_type})"
            )
    
    async def dequeue(
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
    
    async def peek(
        self,
        agent_type: Optional[AgentType] = None,
    ) -> Optional[Task]:
        """View the highest priority task without removing it."""
        task = await self.dequeue(agent_type)
        if task:
            await self.enqueue(task)
        return task
    
    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get a specific task by ID."""
        async with self.lock:
            return self.tasks.get(task_id)
    
    async def cancel_task(self, task_id: UUID) -> bool:
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
    
    async def size(self, agent_type: Optional[AgentType] = None) -> int:
        """Get the number of pending tasks."""
        async with self.lock:
            if agent_type is None:
                return self.queue.qsize()
            
            # Count tasks for specific agent
            return sum(
                1 for task in self.tasks.values()
                if task.agent_type == agent_type and task.status == TaskStatus.PENDING
            )
    
    async def clear(self) -> None:
        """Clear all pending tasks."""
        async with self.lock:
            # Create new queue
            maxsize = self.queue.maxsize
            self.queue = asyncio.PriorityQueue(maxsize=maxsize)
            self.tasks.clear()
            logger.info("Cleared task queue")


class TaskExecutor:
    """
    Executes tasks from a queue.
    
    Manages task execution, retries, timeouts, and result collection.
    """
    
    def __init__(
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
    
    def register_handler(
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
    
    async def execute_task(self, task: Task) -> Any:
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
    
    async def _call_handler(self, handler: Callable, task: Task) -> Any:
        """Call handler, supporting both sync and async."""
        result = handler(task)
        
        # If result is awaitable, await it
        if hasattr(result, '__await__'):
            return await result
        
        return result
    
    async def start(self) -> None:
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
    
    def _cleanup_completed_tasks(self) -> None:
        """Remove completed tasks from running_tasks dict."""
        completed = [
            task_id
            for task_id, async_task in self.running_tasks.items()
            if async_task.done()
        ]
        
        for task_id in completed:
            del self.running_tasks[task_id]
    
    async def stop(self) -> None:
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
    
    def get_statistics(self) -> Dict[str, Any]:
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


class TaskBuilder:
    """
    Builder pattern for constructing tasks.
    
    Provides a fluent interface for creating tasks.
    """
    
    def __init__(self):
        """Initialize task builder."""
        self._agent_type: Optional[AgentType] = None
        self._task_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: TaskPriority = TaskPriority.NORMAL
        self._max_retries: int = 3
        self._timeout_seconds: Optional[float] = None
        self._message_id: Optional[UUID] = None
    
    def for_agent(self, agent: AgentType) -> 'TaskBuilder':
        """Set the target agent."""
        self._agent_type = agent
        return self
    
    def of_type(self, task_type: str) -> 'TaskBuilder':
        """Set the task type."""
        self._task_type = task_type
        return self
    
    def with_payload(self, payload: Dict[str, Any]) -> 'TaskBuilder':
        """Set the payload."""
        self._payload = payload
        return self
    
    def add_to_payload(self, key: str, value: Any) -> 'TaskBuilder':
        """Add a key-value pair to the payload."""
        self._payload[key] = value
        return self
    
    def for_session(self, session_id: UUID) -> 'TaskBuilder':
        """Set the session ID."""
        self._session_id = session_id
        return self
    
    def with_priority(self, priority: TaskPriority) -> 'TaskBuilder':
        """Set the priority."""
        self._priority = priority
        return self
    
    def with_retries(self, max_retries: int) -> 'TaskBuilder':
        """Set maximum retries."""
        self._max_retries = max_retries
        return self
    
    def with_timeout(self, timeout_seconds: float) -> 'TaskBuilder':
        """Set timeout in seconds."""
        self._timeout_seconds = timeout_seconds
        return self
    
    def from_message(self, message: AgentMessage) -> 'TaskBuilder':
        """Create task from a message."""
        self._agent_type = message.to_agent
        self._task_type = message.message_type
        self._payload = message.payload
        self._session_id = message.session_id
        self._priority = TaskPriority(message.priority)
        self._message_id = message.id
        return self
    
    def build(self) -> Task:
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
    
    def reset(self) -> 'TaskBuilder':
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
