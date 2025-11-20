"""
Base agent class for all agents in the system.

This module provides the abstract base class that all agents
(Inductor, Oracle, Contractor, Runner) must inherit from.

Author: Aurel IKAMA HONEY
"""
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import UUID

from shared_context import (
    AgentMessage,
    AgentType,
    ContextManager,
    ProcessingStatus,
)
from orchestration import (
    MessageRouter,
    EventBus,
    TaskQueue,
    Task,
    TaskPriority,
    TaskStatus,
    MessageBuilder,
)
from utils.logging import logger
from utils.config import Config


class AgentState(str, Enum):
    """Agent execution state."""
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class AgentConfig:
    """Configuration for an agent."""
    
    def __init__(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 5,
        task_timeout: float = 300.0,  # 5 minutes
        message_timeout: float = 30.0,
        retry_limit: int = 3,
        enable_metrics: bool = True,
        enable_tracing: bool = True,
        custom_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize agent configuration.
        
        Args:
            agent_type: Type of agent
            max_concurrent_tasks: Maximum tasks to process concurrently
            task_timeout: Timeout for task execution (seconds)
            message_timeout: Timeout for message handling (seconds)
            retry_limit: Maximum retry attempts for failed tasks
            enable_metrics: Enable metrics collection
            enable_tracing: Enable execution tracing
            custom_config: Agent-specific configuration
        """
        self.agent_type = agent_type
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_timeout = task_timeout
        self.message_timeout = message_timeout
        self.retry_limit = retry_limit
        self.enable_metrics = enable_metrics
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        return self.custom_config.get(key, default)


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    Provides common functionality for:
    - Lifecycle management (start, stop, pause, resume)
    - Message handling (send, receive, route)
    - Task processing (queue, execute, retry)
    - Error handling and recovery
    - Metrics and tracing
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        llm_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize base agent.
        
        Args:
            config: Agent configuration
            context_manager: Shared context manager
            router: Message router for inter-agent communication
            event_bus: Event bus for pub-sub messaging
            task_queue: Task queue for workload management
            llm_config: LLM configuration (if agent uses LLMs)
        """
        self.config = config
        self.agent_type = config.agent_type
        self.context_manager = context_manager
        self.router = router
        self.message_router = router  # Alias for compatibility
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = AgentState.IDLE
        self._state_lock = asyncio.Lock()
        
        # Task management
        self._active_tasks: Set[UUID] = set()
        self._task_semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
        self._task_handlers: Dict[str, Callable] = {}
        
        # Message management
        self._message_handlers: Dict[str, Callable] = {}
        self._pending_responses: Dict[UUID, asyncio.Future] = {}
        
        # Event subscriptions
        self._event_subscriptions: Dict[str, Callable] = {}
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics (expose as public property for subclasses)
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        # Public metrics property for subclass access
        self.metrics = self._metrics
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    # ========================================================================
    # Abstract Methods - Must be implemented by subclasses
    # ========================================================================
    
    @abstractmethod
    async def process_task(self, task: Task) -> Any:
        """
        Process a task assigned to this agent.
        
        This is the main work method that each agent must implement.
        
        Args:
            task: Task to process
            
        Returns:
            Task result
            
        Raises:
            Exception: If task processing fails
        """
        pass
    
    @abstractmethod
    def register_handlers(self) -> None:
        """
        Register task and message handlers.
        
        Subclasses should implement this to register their specific
        handlers for different task types and message types.
        """
        pass
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def start(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state in (AgentState.RUNNING, AgentState.STARTING):
                logger.warning(
                    f"{self.agent_type.value} agent already running",
                    agent_type=self.agent_type.value,
                )
                return
            
            self.state = AgentState.STARTING
            logger.info(
                f"Starting {self.agent_type.value} agent",
                agent_type=self.agent_type.value,
            )
        
        try:
            # Register handlers
            self.register_handlers()
            
            # Subscribe to events
            await self._subscribe_to_events()
            
            # Start task processing loop
            task_loop = asyncio.create_task(self._task_processing_loop())
            self._running_tasks.append(task_loop)
            
            # Update state
            async with self._state_lock:
                self.state = AgentState.RUNNING
            
            logger.info(
                f"{self.agent_type.value} agent started successfully",
                agent_type=self.agent_type.value,
            )
            
        except Exception as e:
            async with self._state_lock:
                self.state = AgentState.ERROR
            logger.error(
                f"Failed to start {self.agent_type.value} agent",
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    async def stop(self, timeout: float = 30.0) -> None:
        """
        Stop the agent gracefully.
        
        Args:
            timeout: Maximum time to wait for graceful shutdown (seconds)
        """
        async with self._state_lock:
            if self.state in (AgentState.STOPPED, AgentState.STOPPING):
                logger.warning(
                    f"{self.agent_type.value} agent already stopped",
                    agent_type=self.agent_type.value,
                )
                return
            
            self.state = AgentState.STOPPING
            logger.info(
                f"Stopping {self.agent_type.value} agent",
                agent_type=self.agent_type.value,
            )
        
        try:
            # Signal stop
            self._stop_event.set()
            
            # Wait for active tasks to complete
            if self._active_tasks:
                logger.info(
                    f"Waiting for {len(self._active_tasks)} active tasks to complete",
                    agent_type=self.agent_type.value,
                    active_tasks=len(self._active_tasks),
                )
                
                try:
                    await asyncio.wait_for(
                        self._wait_for_active_tasks(),
                        timeout=timeout,
                    )
                except asyncio.TimeoutError:
                    logger.warning(
                        f"Timeout waiting for active tasks, forcing shutdown",
                        agent_type=self.agent_type.value,
                    )
            
            # Cancel running tasks
            for task in self._running_tasks:
                if not task.done():
                    task.cancel()
            
            # Wait for task cancellation
            if self._running_tasks:
                await asyncio.gather(*self._running_tasks, return_exceptions=True)
            
            # Unsubscribe from events
            await self._unsubscribe_from_events()
            
            # Update state
            async with self._state_lock:
                self.state = AgentState.STOPPED
            
            logger.info(
                f"{self.agent_type.value} agent stopped successfully",
                agent_type=self.agent_type.value,
                metrics=self._metrics,
            )
            
        except Exception as e:
            async with self._state_lock:
                self.state = AgentState.ERROR
            logger.error(
                f"Error stopping {self.agent_type.value} agent",
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    async def pause(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    f"{self.agent_type.value} agent paused",
                    agent_type=self.agent_type.value,
                )
    
    async def resume(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    f"{self.agent_type.value} agent resumed",
                    agent_type=self.agent_type.value,
                )
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def send_message(
        self,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        session_id: UUID,
        priority: int = 1,
        parent_message_id: Optional[UUID] = None,
    ) -> AgentMessage:
        """
        Send a message to another agent.
        
        Args:
            to_agent: Target agent type
            message_type: Type of message
            payload: Message payload
            session_id: Session ID
            priority: Message priority (0=low, 1=normal, 2=high, 3=urgent)
            parent_message_id: ID of parent message (for threading)
            
        Returns:
            Sent message
        """
        builder = MessageBuilder()\
            .from_agent(self.agent_type)\
            .to_agent(to_agent)\
            .with_type(message_type)\
            .with_payload(payload)\
            .for_session(session_id)
        
        if parent_message_id:
            builder = builder.in_reply_to(parent_message_id)
        
        message = builder.build()
        
        await self.router.route_message(message)
        
        self._metrics["messages_sent"] += 1
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    async def handle_message(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
            f"{self.agent_type.value} received message",
            agent_type=self.agent_type.value,
            message_type=message.message_type,
            from_agent=message.from_agent.value,
        )
        
        try:
            # Find handler for message type
            handler = self._message_handlers.get(message.message_type)
            
            if handler:
                # Execute handler with timeout
                await asyncio.wait_for(
                    handler(message),
                    timeout=self.config.message_timeout,
                )
            else:
                logger.warning(
                    f"No handler for message type: {message.message_type}",
                    agent_type=self.agent_type.value,
                    message_type=message.message_type,
                )
            
        except asyncio.TimeoutError:
            logger.error(
                f"Message handling timeout",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
            )
            self._metrics["errors"] += 1
            
        except Exception as e:
            logger.error(
                f"Error handling message",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    def register_message_handler(
        self,
        message_type: str,
        handler: Callable[[AgentMessage], Any],
    ) -> None:
        """
        Register a handler for a message type.
        
        Args:
            message_type: Type of message to handle
            handler: Handler function
        """
        self._message_handlers[message_type] = handler
        logger.debug(
            f"Registered message handler",
            agent_type=self.agent_type.value,
            message_type=message_type,
        )
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def submit_task(
        self,
        task_type: str,
        session_id: UUID,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout: Optional[float] = None,
    ) -> Task:
        """
        Submit a task to the task queue.
        
        Args:
            task_type: Type of task
            session_id: Session ID
            payload: Task payload
            priority: Task priority
            timeout: Task timeout (seconds)
            
        Returns:
            Created task
        """
        task = Task(
            agent_type=self.agent_type,
            task_type=task_type,
            session_id=session_id,
            payload=payload,
            priority=priority,
            timeout_seconds=timeout or self.config.task_timeout,
            max_retries=self.config.retry_limit,
        )
        
        await self.task_queue.enqueue(task)
        
        logger.debug(
            f"Task submitted",
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    async def _task_processing_loop(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
            agent_type=self.agent_type.value,
        )
        
        while not self._stop_event.is_set():
            try:
                # Skip if paused
                if self.state == AgentState.PAUSED:
                    await asyncio.sleep(1.0)
                    continue
                
                # Get next task for this agent
                task = await asyncio.wait_for(
                    self.task_queue.dequeue(agent_type=self.agent_type),
                    timeout=1.0,
                )
                
                if task:
                    # Process task with concurrency limit
                    asyncio.create_task(self._process_task_with_limit(task))
                
            except asyncio.TimeoutError:
                # No task available, continue
                continue
                
            except Exception as e:
                logger.error(
                    f"Error in task processing loop",
                    agent_type=self.agent_type.value,
                    error=str(e),
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def _process_task_with_limit(self, task: Task) -> None:
        """
        Process a task with concurrency limit.
        
        Args:
            task: Task to process
        """
        async with self._task_semaphore:
            await self._execute_task(task)
    
    async def _execute_task(self, task: Task) -> None:
        """
        Execute a task with retry logic.
        
        Args:
            task: Task to execute
        """
        task_id = task.id
        self._active_tasks.add(task_id)
        
        try:
            # Update task status
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.utcnow()
            
            logger.info(
                f"Executing task",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
            )
            
            # Execute task with timeout
            result = await asyncio.wait_for(
                self.process_task(task),
                timeout=task.timeout_seconds,
            )
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            self._metrics["tasks_processed"] += 1
            self._metrics["tasks_succeeded"] += 1
            
            logger.info(
                f"Task completed successfully",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
            )
            
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.completed_at = datetime.utcnow()
            task.error = f"Task timeout after {task.timeout_seconds}s"
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task timeout",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                timeout=task.timeout_seconds,
            )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed: {str(e)}",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
            )
            logger.exception(e)  # Log full traceback
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def publish_event(
        self,
        event_type: str,
        payload: Dict[str, Any],
        session_id: UUID,
    ) -> None:
        """
        Publish an event to the event bus.
        
        Args:
            event_type: Type of event
            payload: Event payload
            session_id: Session ID
        """
        event_data = {
            **payload,
            "session_id": str(session_id),
            "agent_type": self.agent_type.value,
        }
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def subscribe_to_event(
        self,
        event_type: str,
        handler: Callable[[Dict[str, Any]], Any],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Handler function
        """
        self.event_bus.subscribe(event_type, handler)
        self._event_subscriptions[event_type] = handler
        
        logger.debug(
            f"Subscribed to event",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def _subscribe_to_events(self) -> None:
        """Subscribe to relevant events (to be overridden by subclasses)."""
        pass
    
    async def _unsubscribe_from_events(self) -> None:
        """Unsubscribe from all events."""
        for event_type, handler in self._event_subscriptions.items():
            self.event_bus.unsubscribe(event_type, handler)
        
        self._event_subscriptions.clear()
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    async def _wait_for_active_tasks(self) -> None:
        """Wait for all active tasks to complete."""
        while self._active_tasks:
            await asyncio.sleep(0.1)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self._metrics,
            "state": self.state.value,
            "active_tasks": len(self._active_tasks),
        }
    
    def is_running(self) -> bool:
        """Check if agent is running."""
        return self.state == AgentState.RUNNING
    
    def is_stopped(self) -> bool:
        """Check if agent is stopped."""
        return self.state == AgentState.STOPPED
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<{self.__class__.__name__} "
            f"type={self.agent_type.value} "
            f"state={self.state.value}>"
        )
