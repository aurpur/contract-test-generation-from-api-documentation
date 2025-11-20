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
    
    def xǁAgentConfigǁ__init____mutmut_orig(
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
    
    def xǁAgentConfigǁ__init____mutmut_1(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 6,
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
    
    def xǁAgentConfigǁ__init____mutmut_2(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 5,
        task_timeout: float = 301.0,  # 5 minutes
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
    
    def xǁAgentConfigǁ__init____mutmut_3(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 5,
        task_timeout: float = 300.0,  # 5 minutes
        message_timeout: float = 31.0,
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
    
    def xǁAgentConfigǁ__init____mutmut_4(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 5,
        task_timeout: float = 300.0,  # 5 minutes
        message_timeout: float = 30.0,
        retry_limit: int = 4,
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
    
    def xǁAgentConfigǁ__init____mutmut_5(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 5,
        task_timeout: float = 300.0,  # 5 minutes
        message_timeout: float = 30.0,
        retry_limit: int = 3,
        enable_metrics: bool = False,
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
    
    def xǁAgentConfigǁ__init____mutmut_6(
        self,
        agent_type: AgentType,
        max_concurrent_tasks: int = 5,
        task_timeout: float = 300.0,  # 5 minutes
        message_timeout: float = 30.0,
        retry_limit: int = 3,
        enable_metrics: bool = True,
        enable_tracing: bool = False,
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
    
    def xǁAgentConfigǁ__init____mutmut_7(
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
        self.agent_type = None
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_timeout = task_timeout
        self.message_timeout = message_timeout
        self.retry_limit = retry_limit
        self.enable_metrics = enable_metrics
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_8(
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
        self.max_concurrent_tasks = None
        self.task_timeout = task_timeout
        self.message_timeout = message_timeout
        self.retry_limit = retry_limit
        self.enable_metrics = enable_metrics
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_9(
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
        self.task_timeout = None
        self.message_timeout = message_timeout
        self.retry_limit = retry_limit
        self.enable_metrics = enable_metrics
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_10(
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
        self.message_timeout = None
        self.retry_limit = retry_limit
        self.enable_metrics = enable_metrics
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_11(
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
        self.retry_limit = None
        self.enable_metrics = enable_metrics
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_12(
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
        self.enable_metrics = None
        self.enable_tracing = enable_tracing
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_13(
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
        self.enable_tracing = None
        self.custom_config = custom_config or {}
    
    def xǁAgentConfigǁ__init____mutmut_14(
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
        self.custom_config = None
    
    def xǁAgentConfigǁ__init____mutmut_15(
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
        self.custom_config = custom_config and {}
    
    xǁAgentConfigǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentConfigǁ__init____mutmut_1': xǁAgentConfigǁ__init____mutmut_1, 
        'xǁAgentConfigǁ__init____mutmut_2': xǁAgentConfigǁ__init____mutmut_2, 
        'xǁAgentConfigǁ__init____mutmut_3': xǁAgentConfigǁ__init____mutmut_3, 
        'xǁAgentConfigǁ__init____mutmut_4': xǁAgentConfigǁ__init____mutmut_4, 
        'xǁAgentConfigǁ__init____mutmut_5': xǁAgentConfigǁ__init____mutmut_5, 
        'xǁAgentConfigǁ__init____mutmut_6': xǁAgentConfigǁ__init____mutmut_6, 
        'xǁAgentConfigǁ__init____mutmut_7': xǁAgentConfigǁ__init____mutmut_7, 
        'xǁAgentConfigǁ__init____mutmut_8': xǁAgentConfigǁ__init____mutmut_8, 
        'xǁAgentConfigǁ__init____mutmut_9': xǁAgentConfigǁ__init____mutmut_9, 
        'xǁAgentConfigǁ__init____mutmut_10': xǁAgentConfigǁ__init____mutmut_10, 
        'xǁAgentConfigǁ__init____mutmut_11': xǁAgentConfigǁ__init____mutmut_11, 
        'xǁAgentConfigǁ__init____mutmut_12': xǁAgentConfigǁ__init____mutmut_12, 
        'xǁAgentConfigǁ__init____mutmut_13': xǁAgentConfigǁ__init____mutmut_13, 
        'xǁAgentConfigǁ__init____mutmut_14': xǁAgentConfigǁ__init____mutmut_14, 
        'xǁAgentConfigǁ__init____mutmut_15': xǁAgentConfigǁ__init____mutmut_15
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentConfigǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentConfigǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentConfigǁ__init____mutmut_orig)
    xǁAgentConfigǁ__init____mutmut_orig.__name__ = 'xǁAgentConfigǁ__init__'
    
    def xǁAgentConfigǁget__mutmut_orig(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        return self.custom_config.get(key, default)
    
    def xǁAgentConfigǁget__mutmut_1(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        return self.custom_config.get(None, default)
    
    def xǁAgentConfigǁget__mutmut_2(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        return self.custom_config.get(key, None)
    
    def xǁAgentConfigǁget__mutmut_3(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        return self.custom_config.get(default)
    
    def xǁAgentConfigǁget__mutmut_4(self, key: str, default: Any = None) -> Any:
        """Get custom configuration value."""
        return self.custom_config.get(key, )
    
    xǁAgentConfigǁget__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentConfigǁget__mutmut_1': xǁAgentConfigǁget__mutmut_1, 
        'xǁAgentConfigǁget__mutmut_2': xǁAgentConfigǁget__mutmut_2, 
        'xǁAgentConfigǁget__mutmut_3': xǁAgentConfigǁget__mutmut_3, 
        'xǁAgentConfigǁget__mutmut_4': xǁAgentConfigǁget__mutmut_4
    }
    
    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentConfigǁget__mutmut_orig"), object.__getattribute__(self, "xǁAgentConfigǁget__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get.__signature__ = _mutmut_signature(xǁAgentConfigǁget__mutmut_orig)
    xǁAgentConfigǁget__mutmut_orig.__name__ = 'xǁAgentConfigǁget'


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
    
    def xǁBaseAgentǁ__init____mutmut_orig(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_1(
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
        self.config = None
        self.agent_type = config.agent_type
        self.context_manager = context_manager
        self.router = router
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_2(
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
        self.agent_type = None
        self.context_manager = context_manager
        self.router = router
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_3(
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
        self.context_manager = None
        self.router = router
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_4(
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
        self.router = None
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_5(
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
        self.event_bus = None
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_6(
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
        self.event_bus = event_bus
        self.task_queue = None
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_7(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = None
        
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_8(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config and {}
        
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_9(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = None
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_10(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = AgentState.IDLE
        self._state_lock = None
        
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_11(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = AgentState.IDLE
        self._state_lock = asyncio.Lock()
        
        # Task management
        self._active_tasks: Set[UUID] = None
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_12(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = AgentState.IDLE
        self._state_lock = asyncio.Lock()
        
        # Task management
        self._active_tasks: Set[UUID] = set()
        self._task_semaphore = None
        self._task_handlers: Dict[str, Callable] = {}
        
        # Message management
        self._message_handlers: Dict[str, Callable] = {}
        self._pending_responses: Dict[UUID, asyncio.Future] = {}
        
        # Event subscriptions
        self._event_subscriptions: Dict[str, Callable] = {}
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_13(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = AgentState.IDLE
        self._state_lock = asyncio.Lock()
        
        # Task management
        self._active_tasks: Set[UUID] = set()
        self._task_semaphore = asyncio.Semaphore(None)
        self._task_handlers: Dict[str, Callable] = {}
        
        # Message management
        self._message_handlers: Dict[str, Callable] = {}
        self._pending_responses: Dict[UUID, asyncio.Future] = {}
        
        # Event subscriptions
        self._event_subscriptions: Dict[str, Callable] = {}
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_14(
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
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.llm_config = llm_config or {}
        
        # State management
        self.state = AgentState.IDLE
        self._state_lock = asyncio.Lock()
        
        # Task management
        self._active_tasks: Set[UUID] = set()
        self._task_semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
        self._task_handlers: Dict[str, Callable] = None
        
        # Message management
        self._message_handlers: Dict[str, Callable] = {}
        self._pending_responses: Dict[UUID, asyncio.Future] = {}
        
        # Event subscriptions
        self._event_subscriptions: Dict[str, Callable] = {}
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_15(
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
        self._message_handlers: Dict[str, Callable] = None
        self._pending_responses: Dict[UUID, asyncio.Future] = {}
        
        # Event subscriptions
        self._event_subscriptions: Dict[str, Callable] = {}
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_16(
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
        self._pending_responses: Dict[UUID, asyncio.Future] = None
        
        # Event subscriptions
        self._event_subscriptions: Dict[str, Callable] = {}
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_17(
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
        self._event_subscriptions: Dict[str, Callable] = None
        
        # Lifecycle control
        self._stop_event = asyncio.Event()
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_18(
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
        self._stop_event = None
        self._running_tasks: List[asyncio.Task] = []
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_19(
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
        self._running_tasks: List[asyncio.Task] = None
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_20(
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
        
        # Metrics
        self._metrics = None
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_21(
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
        
        # Metrics
        self._metrics = {
            "XXtasks_processedXX": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_22(
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
        
        # Metrics
        self._metrics = {
            "TASKS_PROCESSED": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_23(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 1,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_24(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "XXtasks_succeededXX": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_25(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "TASKS_SUCCEEDED": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_26(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 1,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_27(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "XXtasks_failedXX": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_28(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "TASKS_FAILED": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_29(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 1,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_30(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "XXmessages_sentXX": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_31(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "MESSAGES_SENT": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_32(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 1,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_33(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "XXmessages_receivedXX": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_34(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "MESSAGES_RECEIVED": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_35(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 1,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_36(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "XXerrorsXX": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_37(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "ERRORS": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_38(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 1,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_39(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(None, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_40(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, None)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_41(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_42(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, )
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_43(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            None,
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_44(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=None,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_45(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            max_concurrent_tasks=None,
        )
    
    def xǁBaseAgentǁ__init____mutmut_46(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            agent_type=self.agent_type.value,
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_47(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            max_concurrent_tasks=config.max_concurrent_tasks,
        )
    
    def xǁBaseAgentǁ__init____mutmut_48(
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
        
        # Metrics
        self._metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
        }
        
        # Register with router
        self.router.register_handler(self.agent_type, self.handle_message)
        
        logger.info(
            f"{self.agent_type.value} agent initialized",
            agent_type=self.agent_type.value,
            )
    
    xǁBaseAgentǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁ__init____mutmut_1': xǁBaseAgentǁ__init____mutmut_1, 
        'xǁBaseAgentǁ__init____mutmut_2': xǁBaseAgentǁ__init____mutmut_2, 
        'xǁBaseAgentǁ__init____mutmut_3': xǁBaseAgentǁ__init____mutmut_3, 
        'xǁBaseAgentǁ__init____mutmut_4': xǁBaseAgentǁ__init____mutmut_4, 
        'xǁBaseAgentǁ__init____mutmut_5': xǁBaseAgentǁ__init____mutmut_5, 
        'xǁBaseAgentǁ__init____mutmut_6': xǁBaseAgentǁ__init____mutmut_6, 
        'xǁBaseAgentǁ__init____mutmut_7': xǁBaseAgentǁ__init____mutmut_7, 
        'xǁBaseAgentǁ__init____mutmut_8': xǁBaseAgentǁ__init____mutmut_8, 
        'xǁBaseAgentǁ__init____mutmut_9': xǁBaseAgentǁ__init____mutmut_9, 
        'xǁBaseAgentǁ__init____mutmut_10': xǁBaseAgentǁ__init____mutmut_10, 
        'xǁBaseAgentǁ__init____mutmut_11': xǁBaseAgentǁ__init____mutmut_11, 
        'xǁBaseAgentǁ__init____mutmut_12': xǁBaseAgentǁ__init____mutmut_12, 
        'xǁBaseAgentǁ__init____mutmut_13': xǁBaseAgentǁ__init____mutmut_13, 
        'xǁBaseAgentǁ__init____mutmut_14': xǁBaseAgentǁ__init____mutmut_14, 
        'xǁBaseAgentǁ__init____mutmut_15': xǁBaseAgentǁ__init____mutmut_15, 
        'xǁBaseAgentǁ__init____mutmut_16': xǁBaseAgentǁ__init____mutmut_16, 
        'xǁBaseAgentǁ__init____mutmut_17': xǁBaseAgentǁ__init____mutmut_17, 
        'xǁBaseAgentǁ__init____mutmut_18': xǁBaseAgentǁ__init____mutmut_18, 
        'xǁBaseAgentǁ__init____mutmut_19': xǁBaseAgentǁ__init____mutmut_19, 
        'xǁBaseAgentǁ__init____mutmut_20': xǁBaseAgentǁ__init____mutmut_20, 
        'xǁBaseAgentǁ__init____mutmut_21': xǁBaseAgentǁ__init____mutmut_21, 
        'xǁBaseAgentǁ__init____mutmut_22': xǁBaseAgentǁ__init____mutmut_22, 
        'xǁBaseAgentǁ__init____mutmut_23': xǁBaseAgentǁ__init____mutmut_23, 
        'xǁBaseAgentǁ__init____mutmut_24': xǁBaseAgentǁ__init____mutmut_24, 
        'xǁBaseAgentǁ__init____mutmut_25': xǁBaseAgentǁ__init____mutmut_25, 
        'xǁBaseAgentǁ__init____mutmut_26': xǁBaseAgentǁ__init____mutmut_26, 
        'xǁBaseAgentǁ__init____mutmut_27': xǁBaseAgentǁ__init____mutmut_27, 
        'xǁBaseAgentǁ__init____mutmut_28': xǁBaseAgentǁ__init____mutmut_28, 
        'xǁBaseAgentǁ__init____mutmut_29': xǁBaseAgentǁ__init____mutmut_29, 
        'xǁBaseAgentǁ__init____mutmut_30': xǁBaseAgentǁ__init____mutmut_30, 
        'xǁBaseAgentǁ__init____mutmut_31': xǁBaseAgentǁ__init____mutmut_31, 
        'xǁBaseAgentǁ__init____mutmut_32': xǁBaseAgentǁ__init____mutmut_32, 
        'xǁBaseAgentǁ__init____mutmut_33': xǁBaseAgentǁ__init____mutmut_33, 
        'xǁBaseAgentǁ__init____mutmut_34': xǁBaseAgentǁ__init____mutmut_34, 
        'xǁBaseAgentǁ__init____mutmut_35': xǁBaseAgentǁ__init____mutmut_35, 
        'xǁBaseAgentǁ__init____mutmut_36': xǁBaseAgentǁ__init____mutmut_36, 
        'xǁBaseAgentǁ__init____mutmut_37': xǁBaseAgentǁ__init____mutmut_37, 
        'xǁBaseAgentǁ__init____mutmut_38': xǁBaseAgentǁ__init____mutmut_38, 
        'xǁBaseAgentǁ__init____mutmut_39': xǁBaseAgentǁ__init____mutmut_39, 
        'xǁBaseAgentǁ__init____mutmut_40': xǁBaseAgentǁ__init____mutmut_40, 
        'xǁBaseAgentǁ__init____mutmut_41': xǁBaseAgentǁ__init____mutmut_41, 
        'xǁBaseAgentǁ__init____mutmut_42': xǁBaseAgentǁ__init____mutmut_42, 
        'xǁBaseAgentǁ__init____mutmut_43': xǁBaseAgentǁ__init____mutmut_43, 
        'xǁBaseAgentǁ__init____mutmut_44': xǁBaseAgentǁ__init____mutmut_44, 
        'xǁBaseAgentǁ__init____mutmut_45': xǁBaseAgentǁ__init____mutmut_45, 
        'xǁBaseAgentǁ__init____mutmut_46': xǁBaseAgentǁ__init____mutmut_46, 
        'xǁBaseAgentǁ__init____mutmut_47': xǁBaseAgentǁ__init____mutmut_47, 
        'xǁBaseAgentǁ__init____mutmut_48': xǁBaseAgentǁ__init____mutmut_48
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBaseAgentǁ__init____mutmut_orig)
    xǁBaseAgentǁ__init____mutmut_orig.__name__ = 'xǁBaseAgentǁ__init__'
    
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
    
    async def xǁBaseAgentǁstart__mutmut_orig(self) -> None:
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_1(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state not in (AgentState.RUNNING, AgentState.STARTING):
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_2(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state in (AgentState.RUNNING, AgentState.STARTING):
                logger.warning(
                    None,
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_3(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state in (AgentState.RUNNING, AgentState.STARTING):
                logger.warning(
                    f"{self.agent_type.value} agent already running",
                    agent_type=None,
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_4(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state in (AgentState.RUNNING, AgentState.STARTING):
                logger.warning(
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_5(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state in (AgentState.RUNNING, AgentState.STARTING):
                logger.warning(
                    f"{self.agent_type.value} agent already running",
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_6(self) -> None:
        """Start the agent."""
        async with self._state_lock:
            if self.state in (AgentState.RUNNING, AgentState.STARTING):
                logger.warning(
                    f"{self.agent_type.value} agent already running",
                    agent_type=self.agent_type.value,
                )
                return
            
            self.state = None
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_7(self) -> None:
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
                None,
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_8(self) -> None:
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
                agent_type=None,
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_9(self) -> None:
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_10(self) -> None:
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_11(self) -> None:
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
            task_loop = None
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_12(self) -> None:
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
            task_loop = asyncio.create_task(None)
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_13(self) -> None:
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
            self._running_tasks.append(None)
            
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_14(self) -> None:
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
                self.state = None
            
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_15(self) -> None:
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
                None,
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_16(self) -> None:
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
                agent_type=None,
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_17(self) -> None:
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_18(self) -> None:
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
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_19(self) -> None:
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
                self.state = None
            logger.error(
                f"Failed to start {self.agent_type.value} agent",
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_20(self) -> None:
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
                None,
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_21(self) -> None:
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
                agent_type=None,
                error=str(e),
            )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_22(self) -> None:
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
                error=None,
            )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_23(self) -> None:
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
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_24(self) -> None:
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
                error=str(e),
            )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_25(self) -> None:
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
                )
            raise
    
    # ========================================================================
    # Lifecycle Management
    # ========================================================================
    
    async def xǁBaseAgentǁstart__mutmut_26(self) -> None:
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
                error=str(None),
            )
            raise
    
    xǁBaseAgentǁstart__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁstart__mutmut_1': xǁBaseAgentǁstart__mutmut_1, 
        'xǁBaseAgentǁstart__mutmut_2': xǁBaseAgentǁstart__mutmut_2, 
        'xǁBaseAgentǁstart__mutmut_3': xǁBaseAgentǁstart__mutmut_3, 
        'xǁBaseAgentǁstart__mutmut_4': xǁBaseAgentǁstart__mutmut_4, 
        'xǁBaseAgentǁstart__mutmut_5': xǁBaseAgentǁstart__mutmut_5, 
        'xǁBaseAgentǁstart__mutmut_6': xǁBaseAgentǁstart__mutmut_6, 
        'xǁBaseAgentǁstart__mutmut_7': xǁBaseAgentǁstart__mutmut_7, 
        'xǁBaseAgentǁstart__mutmut_8': xǁBaseAgentǁstart__mutmut_8, 
        'xǁBaseAgentǁstart__mutmut_9': xǁBaseAgentǁstart__mutmut_9, 
        'xǁBaseAgentǁstart__mutmut_10': xǁBaseAgentǁstart__mutmut_10, 
        'xǁBaseAgentǁstart__mutmut_11': xǁBaseAgentǁstart__mutmut_11, 
        'xǁBaseAgentǁstart__mutmut_12': xǁBaseAgentǁstart__mutmut_12, 
        'xǁBaseAgentǁstart__mutmut_13': xǁBaseAgentǁstart__mutmut_13, 
        'xǁBaseAgentǁstart__mutmut_14': xǁBaseAgentǁstart__mutmut_14, 
        'xǁBaseAgentǁstart__mutmut_15': xǁBaseAgentǁstart__mutmut_15, 
        'xǁBaseAgentǁstart__mutmut_16': xǁBaseAgentǁstart__mutmut_16, 
        'xǁBaseAgentǁstart__mutmut_17': xǁBaseAgentǁstart__mutmut_17, 
        'xǁBaseAgentǁstart__mutmut_18': xǁBaseAgentǁstart__mutmut_18, 
        'xǁBaseAgentǁstart__mutmut_19': xǁBaseAgentǁstart__mutmut_19, 
        'xǁBaseAgentǁstart__mutmut_20': xǁBaseAgentǁstart__mutmut_20, 
        'xǁBaseAgentǁstart__mutmut_21': xǁBaseAgentǁstart__mutmut_21, 
        'xǁBaseAgentǁstart__mutmut_22': xǁBaseAgentǁstart__mutmut_22, 
        'xǁBaseAgentǁstart__mutmut_23': xǁBaseAgentǁstart__mutmut_23, 
        'xǁBaseAgentǁstart__mutmut_24': xǁBaseAgentǁstart__mutmut_24, 
        'xǁBaseAgentǁstart__mutmut_25': xǁBaseAgentǁstart__mutmut_25, 
        'xǁBaseAgentǁstart__mutmut_26': xǁBaseAgentǁstart__mutmut_26
    }
    
    def start(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁstart__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁstart__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start.__signature__ = _mutmut_signature(xǁBaseAgentǁstart__mutmut_orig)
    xǁBaseAgentǁstart__mutmut_orig.__name__ = 'xǁBaseAgentǁstart'
    
    async def xǁBaseAgentǁstop__mutmut_orig(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_1(self, timeout: float = 31.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_2(self, timeout: float = 30.0) -> None:
        """
        Stop the agent gracefully.
        
        Args:
            timeout: Maximum time to wait for graceful shutdown (seconds)
        """
        async with self._state_lock:
            if self.state not in (AgentState.STOPPED, AgentState.STOPPING):
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
    
    async def xǁBaseAgentǁstop__mutmut_3(self, timeout: float = 30.0) -> None:
        """
        Stop the agent gracefully.
        
        Args:
            timeout: Maximum time to wait for graceful shutdown (seconds)
        """
        async with self._state_lock:
            if self.state in (AgentState.STOPPED, AgentState.STOPPING):
                logger.warning(
                    None,
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
    
    async def xǁBaseAgentǁstop__mutmut_4(self, timeout: float = 30.0) -> None:
        """
        Stop the agent gracefully.
        
        Args:
            timeout: Maximum time to wait for graceful shutdown (seconds)
        """
        async with self._state_lock:
            if self.state in (AgentState.STOPPED, AgentState.STOPPING):
                logger.warning(
                    f"{self.agent_type.value} agent already stopped",
                    agent_type=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_5(self, timeout: float = 30.0) -> None:
        """
        Stop the agent gracefully.
        
        Args:
            timeout: Maximum time to wait for graceful shutdown (seconds)
        """
        async with self._state_lock:
            if self.state in (AgentState.STOPPED, AgentState.STOPPING):
                logger.warning(
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
    
    async def xǁBaseAgentǁstop__mutmut_6(self, timeout: float = 30.0) -> None:
        """
        Stop the agent gracefully.
        
        Args:
            timeout: Maximum time to wait for graceful shutdown (seconds)
        """
        async with self._state_lock:
            if self.state in (AgentState.STOPPED, AgentState.STOPPING):
                logger.warning(
                    f"{self.agent_type.value} agent already stopped",
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
    
    async def xǁBaseAgentǁstop__mutmut_7(self, timeout: float = 30.0) -> None:
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
            
            self.state = None
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
    
    async def xǁBaseAgentǁstop__mutmut_8(self, timeout: float = 30.0) -> None:
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
                None,
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
    
    async def xǁBaseAgentǁstop__mutmut_9(self, timeout: float = 30.0) -> None:
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
                agent_type=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_10(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_11(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_12(self, timeout: float = 30.0) -> None:
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
                    None,
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
    
    async def xǁBaseAgentǁstop__mutmut_13(self, timeout: float = 30.0) -> None:
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
                    agent_type=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_14(self, timeout: float = 30.0) -> None:
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
                    active_tasks=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_15(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_16(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_17(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_18(self, timeout: float = 30.0) -> None:
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
                        None,
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
    
    async def xǁBaseAgentǁstop__mutmut_19(self, timeout: float = 30.0) -> None:
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
                        timeout=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_20(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_21(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_22(self, timeout: float = 30.0) -> None:
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
                        None,
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
    
    async def xǁBaseAgentǁstop__mutmut_23(self, timeout: float = 30.0) -> None:
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
                        agent_type=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_24(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_25(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_26(self, timeout: float = 30.0) -> None:
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
                if task.done():
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
    
    async def xǁBaseAgentǁstop__mutmut_27(self, timeout: float = 30.0) -> None:
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
                await asyncio.gather(*self._running_tasks, return_exceptions=None)
            
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
    
    async def xǁBaseAgentǁstop__mutmut_28(self, timeout: float = 30.0) -> None:
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
                await asyncio.gather(return_exceptions=True)
            
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
    
    async def xǁBaseAgentǁstop__mutmut_29(self, timeout: float = 30.0) -> None:
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
                await asyncio.gather(*self._running_tasks, )
            
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
    
    async def xǁBaseAgentǁstop__mutmut_30(self, timeout: float = 30.0) -> None:
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
                await asyncio.gather(*self._running_tasks, return_exceptions=False)
            
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
    
    async def xǁBaseAgentǁstop__mutmut_31(self, timeout: float = 30.0) -> None:
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
                self.state = None
            
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
    
    async def xǁBaseAgentǁstop__mutmut_32(self, timeout: float = 30.0) -> None:
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
                None,
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
    
    async def xǁBaseAgentǁstop__mutmut_33(self, timeout: float = 30.0) -> None:
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
                agent_type=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_34(self, timeout: float = 30.0) -> None:
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
                metrics=None,
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
    
    async def xǁBaseAgentǁstop__mutmut_35(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_36(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_37(self, timeout: float = 30.0) -> None:
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
    
    async def xǁBaseAgentǁstop__mutmut_38(self, timeout: float = 30.0) -> None:
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
                self.state = None
            logger.error(
                f"Error stopping {self.agent_type.value} agent",
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_39(self, timeout: float = 30.0) -> None:
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
                None,
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_40(self, timeout: float = 30.0) -> None:
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
                agent_type=None,
                error=str(e),
            )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_41(self, timeout: float = 30.0) -> None:
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
                error=None,
            )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_42(self, timeout: float = 30.0) -> None:
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
                agent_type=self.agent_type.value,
                error=str(e),
            )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_43(self, timeout: float = 30.0) -> None:
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
                error=str(e),
            )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_44(self, timeout: float = 30.0) -> None:
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
                )
            raise
    
    async def xǁBaseAgentǁstop__mutmut_45(self, timeout: float = 30.0) -> None:
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
                error=str(None),
            )
            raise
    
    xǁBaseAgentǁstop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁstop__mutmut_1': xǁBaseAgentǁstop__mutmut_1, 
        'xǁBaseAgentǁstop__mutmut_2': xǁBaseAgentǁstop__mutmut_2, 
        'xǁBaseAgentǁstop__mutmut_3': xǁBaseAgentǁstop__mutmut_3, 
        'xǁBaseAgentǁstop__mutmut_4': xǁBaseAgentǁstop__mutmut_4, 
        'xǁBaseAgentǁstop__mutmut_5': xǁBaseAgentǁstop__mutmut_5, 
        'xǁBaseAgentǁstop__mutmut_6': xǁBaseAgentǁstop__mutmut_6, 
        'xǁBaseAgentǁstop__mutmut_7': xǁBaseAgentǁstop__mutmut_7, 
        'xǁBaseAgentǁstop__mutmut_8': xǁBaseAgentǁstop__mutmut_8, 
        'xǁBaseAgentǁstop__mutmut_9': xǁBaseAgentǁstop__mutmut_9, 
        'xǁBaseAgentǁstop__mutmut_10': xǁBaseAgentǁstop__mutmut_10, 
        'xǁBaseAgentǁstop__mutmut_11': xǁBaseAgentǁstop__mutmut_11, 
        'xǁBaseAgentǁstop__mutmut_12': xǁBaseAgentǁstop__mutmut_12, 
        'xǁBaseAgentǁstop__mutmut_13': xǁBaseAgentǁstop__mutmut_13, 
        'xǁBaseAgentǁstop__mutmut_14': xǁBaseAgentǁstop__mutmut_14, 
        'xǁBaseAgentǁstop__mutmut_15': xǁBaseAgentǁstop__mutmut_15, 
        'xǁBaseAgentǁstop__mutmut_16': xǁBaseAgentǁstop__mutmut_16, 
        'xǁBaseAgentǁstop__mutmut_17': xǁBaseAgentǁstop__mutmut_17, 
        'xǁBaseAgentǁstop__mutmut_18': xǁBaseAgentǁstop__mutmut_18, 
        'xǁBaseAgentǁstop__mutmut_19': xǁBaseAgentǁstop__mutmut_19, 
        'xǁBaseAgentǁstop__mutmut_20': xǁBaseAgentǁstop__mutmut_20, 
        'xǁBaseAgentǁstop__mutmut_21': xǁBaseAgentǁstop__mutmut_21, 
        'xǁBaseAgentǁstop__mutmut_22': xǁBaseAgentǁstop__mutmut_22, 
        'xǁBaseAgentǁstop__mutmut_23': xǁBaseAgentǁstop__mutmut_23, 
        'xǁBaseAgentǁstop__mutmut_24': xǁBaseAgentǁstop__mutmut_24, 
        'xǁBaseAgentǁstop__mutmut_25': xǁBaseAgentǁstop__mutmut_25, 
        'xǁBaseAgentǁstop__mutmut_26': xǁBaseAgentǁstop__mutmut_26, 
        'xǁBaseAgentǁstop__mutmut_27': xǁBaseAgentǁstop__mutmut_27, 
        'xǁBaseAgentǁstop__mutmut_28': xǁBaseAgentǁstop__mutmut_28, 
        'xǁBaseAgentǁstop__mutmut_29': xǁBaseAgentǁstop__mutmut_29, 
        'xǁBaseAgentǁstop__mutmut_30': xǁBaseAgentǁstop__mutmut_30, 
        'xǁBaseAgentǁstop__mutmut_31': xǁBaseAgentǁstop__mutmut_31, 
        'xǁBaseAgentǁstop__mutmut_32': xǁBaseAgentǁstop__mutmut_32, 
        'xǁBaseAgentǁstop__mutmut_33': xǁBaseAgentǁstop__mutmut_33, 
        'xǁBaseAgentǁstop__mutmut_34': xǁBaseAgentǁstop__mutmut_34, 
        'xǁBaseAgentǁstop__mutmut_35': xǁBaseAgentǁstop__mutmut_35, 
        'xǁBaseAgentǁstop__mutmut_36': xǁBaseAgentǁstop__mutmut_36, 
        'xǁBaseAgentǁstop__mutmut_37': xǁBaseAgentǁstop__mutmut_37, 
        'xǁBaseAgentǁstop__mutmut_38': xǁBaseAgentǁstop__mutmut_38, 
        'xǁBaseAgentǁstop__mutmut_39': xǁBaseAgentǁstop__mutmut_39, 
        'xǁBaseAgentǁstop__mutmut_40': xǁBaseAgentǁstop__mutmut_40, 
        'xǁBaseAgentǁstop__mutmut_41': xǁBaseAgentǁstop__mutmut_41, 
        'xǁBaseAgentǁstop__mutmut_42': xǁBaseAgentǁstop__mutmut_42, 
        'xǁBaseAgentǁstop__mutmut_43': xǁBaseAgentǁstop__mutmut_43, 
        'xǁBaseAgentǁstop__mutmut_44': xǁBaseAgentǁstop__mutmut_44, 
        'xǁBaseAgentǁstop__mutmut_45': xǁBaseAgentǁstop__mutmut_45
    }
    
    def stop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁstop__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁstop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop.__signature__ = _mutmut_signature(xǁBaseAgentǁstop__mutmut_orig)
    xǁBaseAgentǁstop__mutmut_orig.__name__ = 'xǁBaseAgentǁstop'
    
    async def xǁBaseAgentǁpause__mutmut_orig(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    f"{self.agent_type.value} agent paused",
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁpause__mutmut_1(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state != AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    f"{self.agent_type.value} agent paused",
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁpause__mutmut_2(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = None
                logger.info(
                    f"{self.agent_type.value} agent paused",
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁpause__mutmut_3(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    None,
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁpause__mutmut_4(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    f"{self.agent_type.value} agent paused",
                    agent_type=None,
                )
    
    async def xǁBaseAgentǁpause__mutmut_5(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁpause__mutmut_6(self) -> None:
        """Pause the agent (stop processing new tasks)."""
        async with self._state_lock:
            if self.state == AgentState.RUNNING:
                self.state = AgentState.PAUSED
                logger.info(
                    f"{self.agent_type.value} agent paused",
                    )
    
    xǁBaseAgentǁpause__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁpause__mutmut_1': xǁBaseAgentǁpause__mutmut_1, 
        'xǁBaseAgentǁpause__mutmut_2': xǁBaseAgentǁpause__mutmut_2, 
        'xǁBaseAgentǁpause__mutmut_3': xǁBaseAgentǁpause__mutmut_3, 
        'xǁBaseAgentǁpause__mutmut_4': xǁBaseAgentǁpause__mutmut_4, 
        'xǁBaseAgentǁpause__mutmut_5': xǁBaseAgentǁpause__mutmut_5, 
        'xǁBaseAgentǁpause__mutmut_6': xǁBaseAgentǁpause__mutmut_6
    }
    
    def pause(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁpause__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁpause__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pause.__signature__ = _mutmut_signature(xǁBaseAgentǁpause__mutmut_orig)
    xǁBaseAgentǁpause__mutmut_orig.__name__ = 'xǁBaseAgentǁpause'
    
    async def xǁBaseAgentǁresume__mutmut_orig(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    f"{self.agent_type.value} agent resumed",
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁresume__mutmut_1(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state != AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    f"{self.agent_type.value} agent resumed",
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁresume__mutmut_2(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = None
                logger.info(
                    f"{self.agent_type.value} agent resumed",
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁresume__mutmut_3(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    None,
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁresume__mutmut_4(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    f"{self.agent_type.value} agent resumed",
                    agent_type=None,
                )
    
    async def xǁBaseAgentǁresume__mutmut_5(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    agent_type=self.agent_type.value,
                )
    
    async def xǁBaseAgentǁresume__mutmut_6(self) -> None:
        """Resume the agent (continue processing tasks)."""
        async with self._state_lock:
            if self.state == AgentState.PAUSED:
                self.state = AgentState.RUNNING
                logger.info(
                    f"{self.agent_type.value} agent resumed",
                    )
    
    xǁBaseAgentǁresume__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁresume__mutmut_1': xǁBaseAgentǁresume__mutmut_1, 
        'xǁBaseAgentǁresume__mutmut_2': xǁBaseAgentǁresume__mutmut_2, 
        'xǁBaseAgentǁresume__mutmut_3': xǁBaseAgentǁresume__mutmut_3, 
        'xǁBaseAgentǁresume__mutmut_4': xǁBaseAgentǁresume__mutmut_4, 
        'xǁBaseAgentǁresume__mutmut_5': xǁBaseAgentǁresume__mutmut_5, 
        'xǁBaseAgentǁresume__mutmut_6': xǁBaseAgentǁresume__mutmut_6
    }
    
    def resume(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁresume__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁresume__mutmut_mutants"), args, kwargs, self)
        return result 
    
    resume.__signature__ = _mutmut_signature(xǁBaseAgentǁresume__mutmut_orig)
    xǁBaseAgentǁresume__mutmut_orig.__name__ = 'xǁBaseAgentǁresume'
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_orig(
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_1(
        self,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        session_id: UUID,
        priority: int = 2,
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_2(
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
        builder = None
        
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_3(
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
            .for_session(None)
        
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_4(
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
            .with_payload(None)\
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_5(
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
            .with_type(None)\
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_6(
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
            .to_agent(None)\
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_7(
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
            .from_agent(None)\
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_8(
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
            builder = None
        
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_9(
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
            builder = builder.in_reply_to(None)
        
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_10(
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
        
        message = None
        
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
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_11(
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
        
        await self.router.route_message(None)
        
        self._metrics["messages_sent"] += 1
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_12(
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
        
        self._metrics["messages_sent"] = 1
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_13(
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
        
        self._metrics["messages_sent"] -= 1
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_14(
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
        
        self._metrics["XXmessages_sentXX"] += 1
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_15(
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
        
        self._metrics["MESSAGES_SENT"] += 1
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_16(
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
        
        self._metrics["messages_sent"] += 2
        
        logger.debug(
            f"{self.agent_type.value} sent message to {to_agent.value}",
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_17(
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
            None,
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_18(
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
            from_agent=None,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_19(
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
            to_agent=None,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_20(
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
            message_type=None,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_21(
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
            message_id=None,
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_22(
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
            from_agent=self.agent_type.value,
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_23(
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
            to_agent=to_agent.value,
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_24(
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
            message_type=message_type,
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_25(
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
            message_id=str(message.id),
        )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_26(
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
            )
        
        return message
    
    # ========================================================================
    # Message Handling
    # ========================================================================
    
    async def xǁBaseAgentǁsend_message__mutmut_27(
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
            message_id=str(None),
        )
        
        return message
    
    xǁBaseAgentǁsend_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁsend_message__mutmut_1': xǁBaseAgentǁsend_message__mutmut_1, 
        'xǁBaseAgentǁsend_message__mutmut_2': xǁBaseAgentǁsend_message__mutmut_2, 
        'xǁBaseAgentǁsend_message__mutmut_3': xǁBaseAgentǁsend_message__mutmut_3, 
        'xǁBaseAgentǁsend_message__mutmut_4': xǁBaseAgentǁsend_message__mutmut_4, 
        'xǁBaseAgentǁsend_message__mutmut_5': xǁBaseAgentǁsend_message__mutmut_5, 
        'xǁBaseAgentǁsend_message__mutmut_6': xǁBaseAgentǁsend_message__mutmut_6, 
        'xǁBaseAgentǁsend_message__mutmut_7': xǁBaseAgentǁsend_message__mutmut_7, 
        'xǁBaseAgentǁsend_message__mutmut_8': xǁBaseAgentǁsend_message__mutmut_8, 
        'xǁBaseAgentǁsend_message__mutmut_9': xǁBaseAgentǁsend_message__mutmut_9, 
        'xǁBaseAgentǁsend_message__mutmut_10': xǁBaseAgentǁsend_message__mutmut_10, 
        'xǁBaseAgentǁsend_message__mutmut_11': xǁBaseAgentǁsend_message__mutmut_11, 
        'xǁBaseAgentǁsend_message__mutmut_12': xǁBaseAgentǁsend_message__mutmut_12, 
        'xǁBaseAgentǁsend_message__mutmut_13': xǁBaseAgentǁsend_message__mutmut_13, 
        'xǁBaseAgentǁsend_message__mutmut_14': xǁBaseAgentǁsend_message__mutmut_14, 
        'xǁBaseAgentǁsend_message__mutmut_15': xǁBaseAgentǁsend_message__mutmut_15, 
        'xǁBaseAgentǁsend_message__mutmut_16': xǁBaseAgentǁsend_message__mutmut_16, 
        'xǁBaseAgentǁsend_message__mutmut_17': xǁBaseAgentǁsend_message__mutmut_17, 
        'xǁBaseAgentǁsend_message__mutmut_18': xǁBaseAgentǁsend_message__mutmut_18, 
        'xǁBaseAgentǁsend_message__mutmut_19': xǁBaseAgentǁsend_message__mutmut_19, 
        'xǁBaseAgentǁsend_message__mutmut_20': xǁBaseAgentǁsend_message__mutmut_20, 
        'xǁBaseAgentǁsend_message__mutmut_21': xǁBaseAgentǁsend_message__mutmut_21, 
        'xǁBaseAgentǁsend_message__mutmut_22': xǁBaseAgentǁsend_message__mutmut_22, 
        'xǁBaseAgentǁsend_message__mutmut_23': xǁBaseAgentǁsend_message__mutmut_23, 
        'xǁBaseAgentǁsend_message__mutmut_24': xǁBaseAgentǁsend_message__mutmut_24, 
        'xǁBaseAgentǁsend_message__mutmut_25': xǁBaseAgentǁsend_message__mutmut_25, 
        'xǁBaseAgentǁsend_message__mutmut_26': xǁBaseAgentǁsend_message__mutmut_26, 
        'xǁBaseAgentǁsend_message__mutmut_27': xǁBaseAgentǁsend_message__mutmut_27
    }
    
    def send_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁsend_message__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁsend_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    send_message.__signature__ = _mutmut_signature(xǁBaseAgentǁsend_message__mutmut_orig)
    xǁBaseAgentǁsend_message__mutmut_orig.__name__ = 'xǁBaseAgentǁsend_message'
    
    async def xǁBaseAgentǁhandle_message__mutmut_orig(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_1(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] = 1
        
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_2(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] -= 1
        
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_3(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["XXmessages_receivedXX"] += 1
        
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_4(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["MESSAGES_RECEIVED"] += 1
        
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_5(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 2
        
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_6(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
            None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_7(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
            f"{self.agent_type.value} received message",
            agent_type=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_8(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
            f"{self.agent_type.value} received message",
            agent_type=self.agent_type.value,
            message_type=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_9(self, message: AgentMessage) -> None:
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
            from_agent=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_10(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_11(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
            f"{self.agent_type.value} received message",
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_12(self, message: AgentMessage) -> None:
        """
        Handle an incoming message.
        
        Args:
            message: Message to handle
        """
        self._metrics["messages_received"] += 1
        
        logger.debug(
            f"{self.agent_type.value} received message",
            agent_type=self.agent_type.value,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_13(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_14(self, message: AgentMessage) -> None:
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
            handler = None
            
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_15(self, message: AgentMessage) -> None:
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
            handler = self._message_handlers.get(None)
            
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_16(self, message: AgentMessage) -> None:
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
                    None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_17(self, message: AgentMessage) -> None:
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
                    timeout=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_18(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_19(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_20(self, message: AgentMessage) -> None:
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
                    handler(None),
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_21(self, message: AgentMessage) -> None:
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
                    None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_22(self, message: AgentMessage) -> None:
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
                    agent_type=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_23(self, message: AgentMessage) -> None:
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
                    message_type=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_24(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_25(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_26(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_27(self, message: AgentMessage) -> None:
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
                None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_28(self, message: AgentMessage) -> None:
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
                agent_type=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_29(self, message: AgentMessage) -> None:
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
                message_type=None,
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_30(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_31(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_32(self, message: AgentMessage) -> None:
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
    
    async def xǁBaseAgentǁhandle_message__mutmut_33(self, message: AgentMessage) -> None:
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
            self._metrics["errors"] = 1
            
        except Exception as e:
            logger.error(
                f"Error handling message",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_34(self, message: AgentMessage) -> None:
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
            self._metrics["errors"] -= 1
            
        except Exception as e:
            logger.error(
                f"Error handling message",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_35(self, message: AgentMessage) -> None:
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
            self._metrics["XXerrorsXX"] += 1
            
        except Exception as e:
            logger.error(
                f"Error handling message",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_36(self, message: AgentMessage) -> None:
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
            self._metrics["ERRORS"] += 1
            
        except Exception as e:
            logger.error(
                f"Error handling message",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_37(self, message: AgentMessage) -> None:
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
            self._metrics["errors"] += 2
            
        except Exception as e:
            logger.error(
                f"Error handling message",
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_38(self, message: AgentMessage) -> None:
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
                None,
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_39(self, message: AgentMessage) -> None:
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
                agent_type=None,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_40(self, message: AgentMessage) -> None:
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
                message_type=None,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_41(self, message: AgentMessage) -> None:
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
                error=None,
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_42(self, message: AgentMessage) -> None:
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
                agent_type=self.agent_type.value,
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_43(self, message: AgentMessage) -> None:
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
                message_type=message.message_type,
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_44(self, message: AgentMessage) -> None:
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
                error=str(e),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_45(self, message: AgentMessage) -> None:
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
                )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_46(self, message: AgentMessage) -> None:
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
                error=str(None),
            )
            self._metrics["errors"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_47(self, message: AgentMessage) -> None:
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
            self._metrics["errors"] = 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_48(self, message: AgentMessage) -> None:
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
            self._metrics["errors"] -= 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_49(self, message: AgentMessage) -> None:
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
            self._metrics["XXerrorsXX"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_50(self, message: AgentMessage) -> None:
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
            self._metrics["ERRORS"] += 1
    
    async def xǁBaseAgentǁhandle_message__mutmut_51(self, message: AgentMessage) -> None:
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
            self._metrics["errors"] += 2
    
    xǁBaseAgentǁhandle_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁhandle_message__mutmut_1': xǁBaseAgentǁhandle_message__mutmut_1, 
        'xǁBaseAgentǁhandle_message__mutmut_2': xǁBaseAgentǁhandle_message__mutmut_2, 
        'xǁBaseAgentǁhandle_message__mutmut_3': xǁBaseAgentǁhandle_message__mutmut_3, 
        'xǁBaseAgentǁhandle_message__mutmut_4': xǁBaseAgentǁhandle_message__mutmut_4, 
        'xǁBaseAgentǁhandle_message__mutmut_5': xǁBaseAgentǁhandle_message__mutmut_5, 
        'xǁBaseAgentǁhandle_message__mutmut_6': xǁBaseAgentǁhandle_message__mutmut_6, 
        'xǁBaseAgentǁhandle_message__mutmut_7': xǁBaseAgentǁhandle_message__mutmut_7, 
        'xǁBaseAgentǁhandle_message__mutmut_8': xǁBaseAgentǁhandle_message__mutmut_8, 
        'xǁBaseAgentǁhandle_message__mutmut_9': xǁBaseAgentǁhandle_message__mutmut_9, 
        'xǁBaseAgentǁhandle_message__mutmut_10': xǁBaseAgentǁhandle_message__mutmut_10, 
        'xǁBaseAgentǁhandle_message__mutmut_11': xǁBaseAgentǁhandle_message__mutmut_11, 
        'xǁBaseAgentǁhandle_message__mutmut_12': xǁBaseAgentǁhandle_message__mutmut_12, 
        'xǁBaseAgentǁhandle_message__mutmut_13': xǁBaseAgentǁhandle_message__mutmut_13, 
        'xǁBaseAgentǁhandle_message__mutmut_14': xǁBaseAgentǁhandle_message__mutmut_14, 
        'xǁBaseAgentǁhandle_message__mutmut_15': xǁBaseAgentǁhandle_message__mutmut_15, 
        'xǁBaseAgentǁhandle_message__mutmut_16': xǁBaseAgentǁhandle_message__mutmut_16, 
        'xǁBaseAgentǁhandle_message__mutmut_17': xǁBaseAgentǁhandle_message__mutmut_17, 
        'xǁBaseAgentǁhandle_message__mutmut_18': xǁBaseAgentǁhandle_message__mutmut_18, 
        'xǁBaseAgentǁhandle_message__mutmut_19': xǁBaseAgentǁhandle_message__mutmut_19, 
        'xǁBaseAgentǁhandle_message__mutmut_20': xǁBaseAgentǁhandle_message__mutmut_20, 
        'xǁBaseAgentǁhandle_message__mutmut_21': xǁBaseAgentǁhandle_message__mutmut_21, 
        'xǁBaseAgentǁhandle_message__mutmut_22': xǁBaseAgentǁhandle_message__mutmut_22, 
        'xǁBaseAgentǁhandle_message__mutmut_23': xǁBaseAgentǁhandle_message__mutmut_23, 
        'xǁBaseAgentǁhandle_message__mutmut_24': xǁBaseAgentǁhandle_message__mutmut_24, 
        'xǁBaseAgentǁhandle_message__mutmut_25': xǁBaseAgentǁhandle_message__mutmut_25, 
        'xǁBaseAgentǁhandle_message__mutmut_26': xǁBaseAgentǁhandle_message__mutmut_26, 
        'xǁBaseAgentǁhandle_message__mutmut_27': xǁBaseAgentǁhandle_message__mutmut_27, 
        'xǁBaseAgentǁhandle_message__mutmut_28': xǁBaseAgentǁhandle_message__mutmut_28, 
        'xǁBaseAgentǁhandle_message__mutmut_29': xǁBaseAgentǁhandle_message__mutmut_29, 
        'xǁBaseAgentǁhandle_message__mutmut_30': xǁBaseAgentǁhandle_message__mutmut_30, 
        'xǁBaseAgentǁhandle_message__mutmut_31': xǁBaseAgentǁhandle_message__mutmut_31, 
        'xǁBaseAgentǁhandle_message__mutmut_32': xǁBaseAgentǁhandle_message__mutmut_32, 
        'xǁBaseAgentǁhandle_message__mutmut_33': xǁBaseAgentǁhandle_message__mutmut_33, 
        'xǁBaseAgentǁhandle_message__mutmut_34': xǁBaseAgentǁhandle_message__mutmut_34, 
        'xǁBaseAgentǁhandle_message__mutmut_35': xǁBaseAgentǁhandle_message__mutmut_35, 
        'xǁBaseAgentǁhandle_message__mutmut_36': xǁBaseAgentǁhandle_message__mutmut_36, 
        'xǁBaseAgentǁhandle_message__mutmut_37': xǁBaseAgentǁhandle_message__mutmut_37, 
        'xǁBaseAgentǁhandle_message__mutmut_38': xǁBaseAgentǁhandle_message__mutmut_38, 
        'xǁBaseAgentǁhandle_message__mutmut_39': xǁBaseAgentǁhandle_message__mutmut_39, 
        'xǁBaseAgentǁhandle_message__mutmut_40': xǁBaseAgentǁhandle_message__mutmut_40, 
        'xǁBaseAgentǁhandle_message__mutmut_41': xǁBaseAgentǁhandle_message__mutmut_41, 
        'xǁBaseAgentǁhandle_message__mutmut_42': xǁBaseAgentǁhandle_message__mutmut_42, 
        'xǁBaseAgentǁhandle_message__mutmut_43': xǁBaseAgentǁhandle_message__mutmut_43, 
        'xǁBaseAgentǁhandle_message__mutmut_44': xǁBaseAgentǁhandle_message__mutmut_44, 
        'xǁBaseAgentǁhandle_message__mutmut_45': xǁBaseAgentǁhandle_message__mutmut_45, 
        'xǁBaseAgentǁhandle_message__mutmut_46': xǁBaseAgentǁhandle_message__mutmut_46, 
        'xǁBaseAgentǁhandle_message__mutmut_47': xǁBaseAgentǁhandle_message__mutmut_47, 
        'xǁBaseAgentǁhandle_message__mutmut_48': xǁBaseAgentǁhandle_message__mutmut_48, 
        'xǁBaseAgentǁhandle_message__mutmut_49': xǁBaseAgentǁhandle_message__mutmut_49, 
        'xǁBaseAgentǁhandle_message__mutmut_50': xǁBaseAgentǁhandle_message__mutmut_50, 
        'xǁBaseAgentǁhandle_message__mutmut_51': xǁBaseAgentǁhandle_message__mutmut_51
    }
    
    def handle_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁhandle_message__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁhandle_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    handle_message.__signature__ = _mutmut_signature(xǁBaseAgentǁhandle_message__mutmut_orig)
    xǁBaseAgentǁhandle_message__mutmut_orig.__name__ = 'xǁBaseAgentǁhandle_message'
    
    def xǁBaseAgentǁregister_message_handler__mutmut_orig(
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
    
    def xǁBaseAgentǁregister_message_handler__mutmut_1(
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
        self._message_handlers[message_type] = None
        logger.debug(
            f"Registered message handler",
            agent_type=self.agent_type.value,
            message_type=message_type,
        )
    
    def xǁBaseAgentǁregister_message_handler__mutmut_2(
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
            None,
            agent_type=self.agent_type.value,
            message_type=message_type,
        )
    
    def xǁBaseAgentǁregister_message_handler__mutmut_3(
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
            agent_type=None,
            message_type=message_type,
        )
    
    def xǁBaseAgentǁregister_message_handler__mutmut_4(
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
            message_type=None,
        )
    
    def xǁBaseAgentǁregister_message_handler__mutmut_5(
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
            agent_type=self.agent_type.value,
            message_type=message_type,
        )
    
    def xǁBaseAgentǁregister_message_handler__mutmut_6(
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
            message_type=message_type,
        )
    
    def xǁBaseAgentǁregister_message_handler__mutmut_7(
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
            )
    
    xǁBaseAgentǁregister_message_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁregister_message_handler__mutmut_1': xǁBaseAgentǁregister_message_handler__mutmut_1, 
        'xǁBaseAgentǁregister_message_handler__mutmut_2': xǁBaseAgentǁregister_message_handler__mutmut_2, 
        'xǁBaseAgentǁregister_message_handler__mutmut_3': xǁBaseAgentǁregister_message_handler__mutmut_3, 
        'xǁBaseAgentǁregister_message_handler__mutmut_4': xǁBaseAgentǁregister_message_handler__mutmut_4, 
        'xǁBaseAgentǁregister_message_handler__mutmut_5': xǁBaseAgentǁregister_message_handler__mutmut_5, 
        'xǁBaseAgentǁregister_message_handler__mutmut_6': xǁBaseAgentǁregister_message_handler__mutmut_6, 
        'xǁBaseAgentǁregister_message_handler__mutmut_7': xǁBaseAgentǁregister_message_handler__mutmut_7
    }
    
    def register_message_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁregister_message_handler__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁregister_message_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_message_handler.__signature__ = _mutmut_signature(xǁBaseAgentǁregister_message_handler__mutmut_orig)
    xǁBaseAgentǁregister_message_handler__mutmut_orig.__name__ = 'xǁBaseAgentǁregister_message_handler'
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_orig(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_1(
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
        task = None
        
        await self.task_queue.enqueue(task)
        
        logger.debug(
            f"Task submitted",
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_2(
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
            agent_type=None,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_3(
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
            task_type=None,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_4(
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
            session_id=None,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_5(
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
            payload=None,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_6(
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
            priority=None,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_7(
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
            timeout_seconds=None,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_8(
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
            max_retries=None,
        )
        
        await self.task_queue.enqueue(task)
        
        logger.debug(
            f"Task submitted",
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_9(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_10(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_11(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_12(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_13(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_14(
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_15(
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
            )
        
        await self.task_queue.enqueue(task)
        
        logger.debug(
            f"Task submitted",
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_16(
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
            timeout_seconds=timeout and self.config.task_timeout,
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
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_17(
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
        
        await self.task_queue.enqueue(None)
        
        logger.debug(
            f"Task submitted",
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_18(
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
            None,
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_19(
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
            agent_type=None,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_20(
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
            task_type=None,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_21(
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
            task_id=None,
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_22(
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
            agent_type=self.agent_type.value,
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_23(
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
            task_type=task_type,
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_24(
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
            task_id=str(task.id),
        )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_25(
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
            )
        
        return task
    
    # ========================================================================
    # Task Processing
    # ========================================================================
    
    async def xǁBaseAgentǁsubmit_task__mutmut_26(
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
            task_id=str(None),
        )
        
        return task
    
    xǁBaseAgentǁsubmit_task__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁsubmit_task__mutmut_1': xǁBaseAgentǁsubmit_task__mutmut_1, 
        'xǁBaseAgentǁsubmit_task__mutmut_2': xǁBaseAgentǁsubmit_task__mutmut_2, 
        'xǁBaseAgentǁsubmit_task__mutmut_3': xǁBaseAgentǁsubmit_task__mutmut_3, 
        'xǁBaseAgentǁsubmit_task__mutmut_4': xǁBaseAgentǁsubmit_task__mutmut_4, 
        'xǁBaseAgentǁsubmit_task__mutmut_5': xǁBaseAgentǁsubmit_task__mutmut_5, 
        'xǁBaseAgentǁsubmit_task__mutmut_6': xǁBaseAgentǁsubmit_task__mutmut_6, 
        'xǁBaseAgentǁsubmit_task__mutmut_7': xǁBaseAgentǁsubmit_task__mutmut_7, 
        'xǁBaseAgentǁsubmit_task__mutmut_8': xǁBaseAgentǁsubmit_task__mutmut_8, 
        'xǁBaseAgentǁsubmit_task__mutmut_9': xǁBaseAgentǁsubmit_task__mutmut_9, 
        'xǁBaseAgentǁsubmit_task__mutmut_10': xǁBaseAgentǁsubmit_task__mutmut_10, 
        'xǁBaseAgentǁsubmit_task__mutmut_11': xǁBaseAgentǁsubmit_task__mutmut_11, 
        'xǁBaseAgentǁsubmit_task__mutmut_12': xǁBaseAgentǁsubmit_task__mutmut_12, 
        'xǁBaseAgentǁsubmit_task__mutmut_13': xǁBaseAgentǁsubmit_task__mutmut_13, 
        'xǁBaseAgentǁsubmit_task__mutmut_14': xǁBaseAgentǁsubmit_task__mutmut_14, 
        'xǁBaseAgentǁsubmit_task__mutmut_15': xǁBaseAgentǁsubmit_task__mutmut_15, 
        'xǁBaseAgentǁsubmit_task__mutmut_16': xǁBaseAgentǁsubmit_task__mutmut_16, 
        'xǁBaseAgentǁsubmit_task__mutmut_17': xǁBaseAgentǁsubmit_task__mutmut_17, 
        'xǁBaseAgentǁsubmit_task__mutmut_18': xǁBaseAgentǁsubmit_task__mutmut_18, 
        'xǁBaseAgentǁsubmit_task__mutmut_19': xǁBaseAgentǁsubmit_task__mutmut_19, 
        'xǁBaseAgentǁsubmit_task__mutmut_20': xǁBaseAgentǁsubmit_task__mutmut_20, 
        'xǁBaseAgentǁsubmit_task__mutmut_21': xǁBaseAgentǁsubmit_task__mutmut_21, 
        'xǁBaseAgentǁsubmit_task__mutmut_22': xǁBaseAgentǁsubmit_task__mutmut_22, 
        'xǁBaseAgentǁsubmit_task__mutmut_23': xǁBaseAgentǁsubmit_task__mutmut_23, 
        'xǁBaseAgentǁsubmit_task__mutmut_24': xǁBaseAgentǁsubmit_task__mutmut_24, 
        'xǁBaseAgentǁsubmit_task__mutmut_25': xǁBaseAgentǁsubmit_task__mutmut_25, 
        'xǁBaseAgentǁsubmit_task__mutmut_26': xǁBaseAgentǁsubmit_task__mutmut_26
    }
    
    def submit_task(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁsubmit_task__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁsubmit_task__mutmut_mutants"), args, kwargs, self)
        return result 
    
    submit_task.__signature__ = _mutmut_signature(xǁBaseAgentǁsubmit_task__mutmut_orig)
    xǁBaseAgentǁsubmit_task__mutmut_orig.__name__ = 'xǁBaseAgentǁsubmit_task'
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_orig(self) -> None:
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_1(self) -> None:
        """Main task processing loop."""
        logger.info(
            None,
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_2(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
            agent_type=None,
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_3(self) -> None:
        """Main task processing loop."""
        logger.info(
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_4(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_5(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
            agent_type=self.agent_type.value,
        )
        
        while self._stop_event.is_set():
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_6(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
            agent_type=self.agent_type.value,
        )
        
        while not self._stop_event.is_set():
            try:
                # Skip if paused
                if self.state != AgentState.PAUSED:
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_7(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
            agent_type=self.agent_type.value,
        )
        
        while not self._stop_event.is_set():
            try:
                # Skip if paused
                if self.state == AgentState.PAUSED:
                    await asyncio.sleep(None)
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_8(self) -> None:
        """Main task processing loop."""
        logger.info(
            f"Task processing loop started",
            agent_type=self.agent_type.value,
        )
        
        while not self._stop_event.is_set():
            try:
                # Skip if paused
                if self.state == AgentState.PAUSED:
                    await asyncio.sleep(2.0)
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_9(self) -> None:
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
                    break
                
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_10(self) -> None:
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
                task = None
                
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_11(self) -> None:
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
                    None,
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_12(self) -> None:
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
                    timeout=None,
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_13(self) -> None:
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_14(self) -> None:
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_15(self) -> None:
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
                    self.task_queue.dequeue(agent_type=None),
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_16(self) -> None:
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
                    timeout=2.0,
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_17(self) -> None:
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
                    asyncio.create_task(None)
                
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_18(self) -> None:
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
                    asyncio.create_task(self._process_task_with_limit(None))
                
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_19(self) -> None:
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
                break
                
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
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_20(self) -> None:
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
                    None,
                    agent_type=self.agent_type.value,
                    error=str(e),
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_21(self) -> None:
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
                    agent_type=None,
                    error=str(e),
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_22(self) -> None:
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
                    error=None,
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_23(self) -> None:
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
                    agent_type=self.agent_type.value,
                    error=str(e),
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_24(self) -> None:
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
                    error=str(e),
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_25(self) -> None:
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
                    )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_26(self) -> None:
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
                    error=str(None),
                )
                await asyncio.sleep(1.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_27(self) -> None:
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
                await asyncio.sleep(None)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_28(self) -> None:
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
                await asyncio.sleep(2.0)
        
        logger.info(
            f"Task processing loop stopped",
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_29(self) -> None:
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
            None,
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_30(self) -> None:
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
            agent_type=None,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_31(self) -> None:
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
            agent_type=self.agent_type.value,
        )
    
    async def xǁBaseAgentǁ_task_processing_loop__mutmut_32(self) -> None:
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
            )
    
    xǁBaseAgentǁ_task_processing_loop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁ_task_processing_loop__mutmut_1': xǁBaseAgentǁ_task_processing_loop__mutmut_1, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_2': xǁBaseAgentǁ_task_processing_loop__mutmut_2, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_3': xǁBaseAgentǁ_task_processing_loop__mutmut_3, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_4': xǁBaseAgentǁ_task_processing_loop__mutmut_4, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_5': xǁBaseAgentǁ_task_processing_loop__mutmut_5, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_6': xǁBaseAgentǁ_task_processing_loop__mutmut_6, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_7': xǁBaseAgentǁ_task_processing_loop__mutmut_7, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_8': xǁBaseAgentǁ_task_processing_loop__mutmut_8, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_9': xǁBaseAgentǁ_task_processing_loop__mutmut_9, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_10': xǁBaseAgentǁ_task_processing_loop__mutmut_10, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_11': xǁBaseAgentǁ_task_processing_loop__mutmut_11, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_12': xǁBaseAgentǁ_task_processing_loop__mutmut_12, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_13': xǁBaseAgentǁ_task_processing_loop__mutmut_13, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_14': xǁBaseAgentǁ_task_processing_loop__mutmut_14, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_15': xǁBaseAgentǁ_task_processing_loop__mutmut_15, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_16': xǁBaseAgentǁ_task_processing_loop__mutmut_16, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_17': xǁBaseAgentǁ_task_processing_loop__mutmut_17, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_18': xǁBaseAgentǁ_task_processing_loop__mutmut_18, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_19': xǁBaseAgentǁ_task_processing_loop__mutmut_19, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_20': xǁBaseAgentǁ_task_processing_loop__mutmut_20, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_21': xǁBaseAgentǁ_task_processing_loop__mutmut_21, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_22': xǁBaseAgentǁ_task_processing_loop__mutmut_22, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_23': xǁBaseAgentǁ_task_processing_loop__mutmut_23, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_24': xǁBaseAgentǁ_task_processing_loop__mutmut_24, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_25': xǁBaseAgentǁ_task_processing_loop__mutmut_25, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_26': xǁBaseAgentǁ_task_processing_loop__mutmut_26, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_27': xǁBaseAgentǁ_task_processing_loop__mutmut_27, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_28': xǁBaseAgentǁ_task_processing_loop__mutmut_28, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_29': xǁBaseAgentǁ_task_processing_loop__mutmut_29, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_30': xǁBaseAgentǁ_task_processing_loop__mutmut_30, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_31': xǁBaseAgentǁ_task_processing_loop__mutmut_31, 
        'xǁBaseAgentǁ_task_processing_loop__mutmut_32': xǁBaseAgentǁ_task_processing_loop__mutmut_32
    }
    
    def _task_processing_loop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁ_task_processing_loop__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁ_task_processing_loop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _task_processing_loop.__signature__ = _mutmut_signature(xǁBaseAgentǁ_task_processing_loop__mutmut_orig)
    xǁBaseAgentǁ_task_processing_loop__mutmut_orig.__name__ = 'xǁBaseAgentǁ_task_processing_loop'
    
    async def xǁBaseAgentǁ_process_task_with_limit__mutmut_orig(self, task: Task) -> None:
        """
        Process a task with concurrency limit.
        
        Args:
            task: Task to process
        """
        async with self._task_semaphore:
            await self._execute_task(task)
    
    async def xǁBaseAgentǁ_process_task_with_limit__mutmut_1(self, task: Task) -> None:
        """
        Process a task with concurrency limit.
        
        Args:
            task: Task to process
        """
        async with self._task_semaphore:
            await self._execute_task(None)
    
    xǁBaseAgentǁ_process_task_with_limit__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁ_process_task_with_limit__mutmut_1': xǁBaseAgentǁ_process_task_with_limit__mutmut_1
    }
    
    def _process_task_with_limit(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁ_process_task_with_limit__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁ_process_task_with_limit__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _process_task_with_limit.__signature__ = _mutmut_signature(xǁBaseAgentǁ_process_task_with_limit__mutmut_orig)
    xǁBaseAgentǁ_process_task_with_limit__mutmut_orig.__name__ = 'xǁBaseAgentǁ_process_task_with_limit'
    
    async def xǁBaseAgentǁ_execute_task__mutmut_orig(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_1(self, task: Task) -> None:
        """
        Execute a task with retry logic.
        
        Args:
            task: Task to execute
        """
        task_id = None
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_2(self, task: Task) -> None:
        """
        Execute a task with retry logic.
        
        Args:
            task: Task to execute
        """
        task_id = task.id
        self._active_tasks.add(None)
        
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_3(self, task: Task) -> None:
        """
        Execute a task with retry logic.
        
        Args:
            task: Task to execute
        """
        task_id = task.id
        self._active_tasks.add(task_id)
        
        try:
            # Update task status
            task.status = None
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_4(self, task: Task) -> None:
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
            task.started_at = None
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_5(self, task: Task) -> None:
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
                None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_6(self, task: Task) -> None:
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
                agent_type=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_7(self, task: Task) -> None:
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
                task_type=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_8(self, task: Task) -> None:
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
                task_id=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_9(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_10(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_11(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_12(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_13(self, task: Task) -> None:
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
                task_id=str(None),
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_14(self, task: Task) -> None:
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
            result = None
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_15(self, task: Task) -> None:
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
                None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_16(self, task: Task) -> None:
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
                timeout=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_17(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_18(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_19(self, task: Task) -> None:
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
                self.process_task(None),
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_20(self, task: Task) -> None:
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
            task.status = None
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_21(self, task: Task) -> None:
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
            task.completed_at = None
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_22(self, task: Task) -> None:
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
            task.result = None
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_23(self, task: Task) -> None:
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
            
            self._metrics["tasks_processed"] = 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_24(self, task: Task) -> None:
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
            
            self._metrics["tasks_processed"] -= 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_25(self, task: Task) -> None:
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
            
            self._metrics["XXtasks_processedXX"] += 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_26(self, task: Task) -> None:
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
            
            self._metrics["TASKS_PROCESSED"] += 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_27(self, task: Task) -> None:
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
            
            self._metrics["tasks_processed"] += 2
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_28(self, task: Task) -> None:
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
            self._metrics["tasks_succeeded"] = 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_29(self, task: Task) -> None:
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
            self._metrics["tasks_succeeded"] -= 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_30(self, task: Task) -> None:
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
            self._metrics["XXtasks_succeededXX"] += 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_31(self, task: Task) -> None:
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
            self._metrics["TASKS_SUCCEEDED"] += 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_32(self, task: Task) -> None:
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
            self._metrics["tasks_succeeded"] += 2
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_33(self, task: Task) -> None:
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
                None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_34(self, task: Task) -> None:
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
                agent_type=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_35(self, task: Task) -> None:
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
                task_type=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_36(self, task: Task) -> None:
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
                task_id=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_37(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_38(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_39(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_40(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_41(self, task: Task) -> None:
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
                task_id=str(None),
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_42(self, task: Task) -> None:
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
            task.status = None
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_43(self, task: Task) -> None:
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
            task.completed_at = None
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_44(self, task: Task) -> None:
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
            task.error = None
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_45(self, task: Task) -> None:
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
            
            self._metrics["tasks_failed"] = 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_46(self, task: Task) -> None:
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
            
            self._metrics["tasks_failed"] -= 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_47(self, task: Task) -> None:
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
            
            self._metrics["XXtasks_failedXX"] += 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_48(self, task: Task) -> None:
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
            
            self._metrics["TASKS_FAILED"] += 1
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_49(self, task: Task) -> None:
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
            
            self._metrics["tasks_failed"] += 2
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_50(self, task: Task) -> None:
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
            self._metrics["errors"] = 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_51(self, task: Task) -> None:
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
            self._metrics["errors"] -= 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_52(self, task: Task) -> None:
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
            self._metrics["XXerrorsXX"] += 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_53(self, task: Task) -> None:
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
            self._metrics["ERRORS"] += 1
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_54(self, task: Task) -> None:
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
            self._metrics["errors"] += 2
            
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_55(self, task: Task) -> None:
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
                None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_56(self, task: Task) -> None:
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
                agent_type=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_57(self, task: Task) -> None:
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
                task_type=None,
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_58(self, task: Task) -> None:
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
                task_id=None,
                timeout=task.timeout_seconds,
            )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_59(self, task: Task) -> None:
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
                timeout=None,
            )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_60(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_61(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_62(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_63(self, task: Task) -> None:
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
                timeout=task.timeout_seconds,
            )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_64(self, task: Task) -> None:
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
                )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_65(self, task: Task) -> None:
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
                task_id=str(None),
                timeout=task.timeout_seconds,
            )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_66(self, task: Task) -> None:
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
            task.status = None
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_67(self, task: Task) -> None:
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
            task.completed_at = None
            task.error = str(e)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_68(self, task: Task) -> None:
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
            task.error = None
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_69(self, task: Task) -> None:
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
            task.error = str(None)
            
            self._metrics["tasks_failed"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_70(self, task: Task) -> None:
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
            
            self._metrics["tasks_failed"] = 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_71(self, task: Task) -> None:
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
            
            self._metrics["tasks_failed"] -= 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_72(self, task: Task) -> None:
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
            
            self._metrics["XXtasks_failedXX"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_73(self, task: Task) -> None:
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
            
            self._metrics["TASKS_FAILED"] += 1
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_74(self, task: Task) -> None:
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
            
            self._metrics["tasks_failed"] += 2
            self._metrics["errors"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_75(self, task: Task) -> None:
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
            self._metrics["errors"] = 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_76(self, task: Task) -> None:
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
            self._metrics["errors"] -= 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_77(self, task: Task) -> None:
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
            self._metrics["XXerrorsXX"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_78(self, task: Task) -> None:
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
            self._metrics["ERRORS"] += 1
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_79(self, task: Task) -> None:
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
            self._metrics["errors"] += 2
            
            logger.error(
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_80(self, task: Task) -> None:
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
                None,
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_81(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=None,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_82(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=None,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_83(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=None,
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_84(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=None,
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_85(self, task: Task) -> None:
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
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_86(self, task: Task) -> None:
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
                f"Task failed",
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_87(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_id=str(task_id),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_88(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_89(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_90(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(None),
                error=str(e),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_91(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(None),
            )
            
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_92(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count <= task.max_retries:
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_93(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count = 1
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_94(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count -= 1
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_95(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 2
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
    
    async def xǁBaseAgentǁ_execute_task__mutmut_96(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = None
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_97(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(None)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_98(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    None,
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_99(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=None,
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_100(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=None,
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_101(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    retry_count=None,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_102(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_103(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    task_id=str(task_id),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_104(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_105(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=str(task_id),
                    )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_106(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                await self.task_queue.enqueue(task)
                
                logger.info(
                    f"Task requeued for retry",
                    agent_type=self.agent_type.value,
                    task_id=str(None),
                    retry_count=task.retry_count,
                )
        
        finally:
            self._active_tasks.remove(task_id)
    
    async def xǁBaseAgentǁ_execute_task__mutmut_107(self, task: Task) -> None:
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
                f"Task failed",
                agent_type=self.agent_type.value,
                task_type=task.task_type,
                task_id=str(task_id),
                error=str(e),
            )
            
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
            self._active_tasks.remove(None)
    
    xǁBaseAgentǁ_execute_task__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁ_execute_task__mutmut_1': xǁBaseAgentǁ_execute_task__mutmut_1, 
        'xǁBaseAgentǁ_execute_task__mutmut_2': xǁBaseAgentǁ_execute_task__mutmut_2, 
        'xǁBaseAgentǁ_execute_task__mutmut_3': xǁBaseAgentǁ_execute_task__mutmut_3, 
        'xǁBaseAgentǁ_execute_task__mutmut_4': xǁBaseAgentǁ_execute_task__mutmut_4, 
        'xǁBaseAgentǁ_execute_task__mutmut_5': xǁBaseAgentǁ_execute_task__mutmut_5, 
        'xǁBaseAgentǁ_execute_task__mutmut_6': xǁBaseAgentǁ_execute_task__mutmut_6, 
        'xǁBaseAgentǁ_execute_task__mutmut_7': xǁBaseAgentǁ_execute_task__mutmut_7, 
        'xǁBaseAgentǁ_execute_task__mutmut_8': xǁBaseAgentǁ_execute_task__mutmut_8, 
        'xǁBaseAgentǁ_execute_task__mutmut_9': xǁBaseAgentǁ_execute_task__mutmut_9, 
        'xǁBaseAgentǁ_execute_task__mutmut_10': xǁBaseAgentǁ_execute_task__mutmut_10, 
        'xǁBaseAgentǁ_execute_task__mutmut_11': xǁBaseAgentǁ_execute_task__mutmut_11, 
        'xǁBaseAgentǁ_execute_task__mutmut_12': xǁBaseAgentǁ_execute_task__mutmut_12, 
        'xǁBaseAgentǁ_execute_task__mutmut_13': xǁBaseAgentǁ_execute_task__mutmut_13, 
        'xǁBaseAgentǁ_execute_task__mutmut_14': xǁBaseAgentǁ_execute_task__mutmut_14, 
        'xǁBaseAgentǁ_execute_task__mutmut_15': xǁBaseAgentǁ_execute_task__mutmut_15, 
        'xǁBaseAgentǁ_execute_task__mutmut_16': xǁBaseAgentǁ_execute_task__mutmut_16, 
        'xǁBaseAgentǁ_execute_task__mutmut_17': xǁBaseAgentǁ_execute_task__mutmut_17, 
        'xǁBaseAgentǁ_execute_task__mutmut_18': xǁBaseAgentǁ_execute_task__mutmut_18, 
        'xǁBaseAgentǁ_execute_task__mutmut_19': xǁBaseAgentǁ_execute_task__mutmut_19, 
        'xǁBaseAgentǁ_execute_task__mutmut_20': xǁBaseAgentǁ_execute_task__mutmut_20, 
        'xǁBaseAgentǁ_execute_task__mutmut_21': xǁBaseAgentǁ_execute_task__mutmut_21, 
        'xǁBaseAgentǁ_execute_task__mutmut_22': xǁBaseAgentǁ_execute_task__mutmut_22, 
        'xǁBaseAgentǁ_execute_task__mutmut_23': xǁBaseAgentǁ_execute_task__mutmut_23, 
        'xǁBaseAgentǁ_execute_task__mutmut_24': xǁBaseAgentǁ_execute_task__mutmut_24, 
        'xǁBaseAgentǁ_execute_task__mutmut_25': xǁBaseAgentǁ_execute_task__mutmut_25, 
        'xǁBaseAgentǁ_execute_task__mutmut_26': xǁBaseAgentǁ_execute_task__mutmut_26, 
        'xǁBaseAgentǁ_execute_task__mutmut_27': xǁBaseAgentǁ_execute_task__mutmut_27, 
        'xǁBaseAgentǁ_execute_task__mutmut_28': xǁBaseAgentǁ_execute_task__mutmut_28, 
        'xǁBaseAgentǁ_execute_task__mutmut_29': xǁBaseAgentǁ_execute_task__mutmut_29, 
        'xǁBaseAgentǁ_execute_task__mutmut_30': xǁBaseAgentǁ_execute_task__mutmut_30, 
        'xǁBaseAgentǁ_execute_task__mutmut_31': xǁBaseAgentǁ_execute_task__mutmut_31, 
        'xǁBaseAgentǁ_execute_task__mutmut_32': xǁBaseAgentǁ_execute_task__mutmut_32, 
        'xǁBaseAgentǁ_execute_task__mutmut_33': xǁBaseAgentǁ_execute_task__mutmut_33, 
        'xǁBaseAgentǁ_execute_task__mutmut_34': xǁBaseAgentǁ_execute_task__mutmut_34, 
        'xǁBaseAgentǁ_execute_task__mutmut_35': xǁBaseAgentǁ_execute_task__mutmut_35, 
        'xǁBaseAgentǁ_execute_task__mutmut_36': xǁBaseAgentǁ_execute_task__mutmut_36, 
        'xǁBaseAgentǁ_execute_task__mutmut_37': xǁBaseAgentǁ_execute_task__mutmut_37, 
        'xǁBaseAgentǁ_execute_task__mutmut_38': xǁBaseAgentǁ_execute_task__mutmut_38, 
        'xǁBaseAgentǁ_execute_task__mutmut_39': xǁBaseAgentǁ_execute_task__mutmut_39, 
        'xǁBaseAgentǁ_execute_task__mutmut_40': xǁBaseAgentǁ_execute_task__mutmut_40, 
        'xǁBaseAgentǁ_execute_task__mutmut_41': xǁBaseAgentǁ_execute_task__mutmut_41, 
        'xǁBaseAgentǁ_execute_task__mutmut_42': xǁBaseAgentǁ_execute_task__mutmut_42, 
        'xǁBaseAgentǁ_execute_task__mutmut_43': xǁBaseAgentǁ_execute_task__mutmut_43, 
        'xǁBaseAgentǁ_execute_task__mutmut_44': xǁBaseAgentǁ_execute_task__mutmut_44, 
        'xǁBaseAgentǁ_execute_task__mutmut_45': xǁBaseAgentǁ_execute_task__mutmut_45, 
        'xǁBaseAgentǁ_execute_task__mutmut_46': xǁBaseAgentǁ_execute_task__mutmut_46, 
        'xǁBaseAgentǁ_execute_task__mutmut_47': xǁBaseAgentǁ_execute_task__mutmut_47, 
        'xǁBaseAgentǁ_execute_task__mutmut_48': xǁBaseAgentǁ_execute_task__mutmut_48, 
        'xǁBaseAgentǁ_execute_task__mutmut_49': xǁBaseAgentǁ_execute_task__mutmut_49, 
        'xǁBaseAgentǁ_execute_task__mutmut_50': xǁBaseAgentǁ_execute_task__mutmut_50, 
        'xǁBaseAgentǁ_execute_task__mutmut_51': xǁBaseAgentǁ_execute_task__mutmut_51, 
        'xǁBaseAgentǁ_execute_task__mutmut_52': xǁBaseAgentǁ_execute_task__mutmut_52, 
        'xǁBaseAgentǁ_execute_task__mutmut_53': xǁBaseAgentǁ_execute_task__mutmut_53, 
        'xǁBaseAgentǁ_execute_task__mutmut_54': xǁBaseAgentǁ_execute_task__mutmut_54, 
        'xǁBaseAgentǁ_execute_task__mutmut_55': xǁBaseAgentǁ_execute_task__mutmut_55, 
        'xǁBaseAgentǁ_execute_task__mutmut_56': xǁBaseAgentǁ_execute_task__mutmut_56, 
        'xǁBaseAgentǁ_execute_task__mutmut_57': xǁBaseAgentǁ_execute_task__mutmut_57, 
        'xǁBaseAgentǁ_execute_task__mutmut_58': xǁBaseAgentǁ_execute_task__mutmut_58, 
        'xǁBaseAgentǁ_execute_task__mutmut_59': xǁBaseAgentǁ_execute_task__mutmut_59, 
        'xǁBaseAgentǁ_execute_task__mutmut_60': xǁBaseAgentǁ_execute_task__mutmut_60, 
        'xǁBaseAgentǁ_execute_task__mutmut_61': xǁBaseAgentǁ_execute_task__mutmut_61, 
        'xǁBaseAgentǁ_execute_task__mutmut_62': xǁBaseAgentǁ_execute_task__mutmut_62, 
        'xǁBaseAgentǁ_execute_task__mutmut_63': xǁBaseAgentǁ_execute_task__mutmut_63, 
        'xǁBaseAgentǁ_execute_task__mutmut_64': xǁBaseAgentǁ_execute_task__mutmut_64, 
        'xǁBaseAgentǁ_execute_task__mutmut_65': xǁBaseAgentǁ_execute_task__mutmut_65, 
        'xǁBaseAgentǁ_execute_task__mutmut_66': xǁBaseAgentǁ_execute_task__mutmut_66, 
        'xǁBaseAgentǁ_execute_task__mutmut_67': xǁBaseAgentǁ_execute_task__mutmut_67, 
        'xǁBaseAgentǁ_execute_task__mutmut_68': xǁBaseAgentǁ_execute_task__mutmut_68, 
        'xǁBaseAgentǁ_execute_task__mutmut_69': xǁBaseAgentǁ_execute_task__mutmut_69, 
        'xǁBaseAgentǁ_execute_task__mutmut_70': xǁBaseAgentǁ_execute_task__mutmut_70, 
        'xǁBaseAgentǁ_execute_task__mutmut_71': xǁBaseAgentǁ_execute_task__mutmut_71, 
        'xǁBaseAgentǁ_execute_task__mutmut_72': xǁBaseAgentǁ_execute_task__mutmut_72, 
        'xǁBaseAgentǁ_execute_task__mutmut_73': xǁBaseAgentǁ_execute_task__mutmut_73, 
        'xǁBaseAgentǁ_execute_task__mutmut_74': xǁBaseAgentǁ_execute_task__mutmut_74, 
        'xǁBaseAgentǁ_execute_task__mutmut_75': xǁBaseAgentǁ_execute_task__mutmut_75, 
        'xǁBaseAgentǁ_execute_task__mutmut_76': xǁBaseAgentǁ_execute_task__mutmut_76, 
        'xǁBaseAgentǁ_execute_task__mutmut_77': xǁBaseAgentǁ_execute_task__mutmut_77, 
        'xǁBaseAgentǁ_execute_task__mutmut_78': xǁBaseAgentǁ_execute_task__mutmut_78, 
        'xǁBaseAgentǁ_execute_task__mutmut_79': xǁBaseAgentǁ_execute_task__mutmut_79, 
        'xǁBaseAgentǁ_execute_task__mutmut_80': xǁBaseAgentǁ_execute_task__mutmut_80, 
        'xǁBaseAgentǁ_execute_task__mutmut_81': xǁBaseAgentǁ_execute_task__mutmut_81, 
        'xǁBaseAgentǁ_execute_task__mutmut_82': xǁBaseAgentǁ_execute_task__mutmut_82, 
        'xǁBaseAgentǁ_execute_task__mutmut_83': xǁBaseAgentǁ_execute_task__mutmut_83, 
        'xǁBaseAgentǁ_execute_task__mutmut_84': xǁBaseAgentǁ_execute_task__mutmut_84, 
        'xǁBaseAgentǁ_execute_task__mutmut_85': xǁBaseAgentǁ_execute_task__mutmut_85, 
        'xǁBaseAgentǁ_execute_task__mutmut_86': xǁBaseAgentǁ_execute_task__mutmut_86, 
        'xǁBaseAgentǁ_execute_task__mutmut_87': xǁBaseAgentǁ_execute_task__mutmut_87, 
        'xǁBaseAgentǁ_execute_task__mutmut_88': xǁBaseAgentǁ_execute_task__mutmut_88, 
        'xǁBaseAgentǁ_execute_task__mutmut_89': xǁBaseAgentǁ_execute_task__mutmut_89, 
        'xǁBaseAgentǁ_execute_task__mutmut_90': xǁBaseAgentǁ_execute_task__mutmut_90, 
        'xǁBaseAgentǁ_execute_task__mutmut_91': xǁBaseAgentǁ_execute_task__mutmut_91, 
        'xǁBaseAgentǁ_execute_task__mutmut_92': xǁBaseAgentǁ_execute_task__mutmut_92, 
        'xǁBaseAgentǁ_execute_task__mutmut_93': xǁBaseAgentǁ_execute_task__mutmut_93, 
        'xǁBaseAgentǁ_execute_task__mutmut_94': xǁBaseAgentǁ_execute_task__mutmut_94, 
        'xǁBaseAgentǁ_execute_task__mutmut_95': xǁBaseAgentǁ_execute_task__mutmut_95, 
        'xǁBaseAgentǁ_execute_task__mutmut_96': xǁBaseAgentǁ_execute_task__mutmut_96, 
        'xǁBaseAgentǁ_execute_task__mutmut_97': xǁBaseAgentǁ_execute_task__mutmut_97, 
        'xǁBaseAgentǁ_execute_task__mutmut_98': xǁBaseAgentǁ_execute_task__mutmut_98, 
        'xǁBaseAgentǁ_execute_task__mutmut_99': xǁBaseAgentǁ_execute_task__mutmut_99, 
        'xǁBaseAgentǁ_execute_task__mutmut_100': xǁBaseAgentǁ_execute_task__mutmut_100, 
        'xǁBaseAgentǁ_execute_task__mutmut_101': xǁBaseAgentǁ_execute_task__mutmut_101, 
        'xǁBaseAgentǁ_execute_task__mutmut_102': xǁBaseAgentǁ_execute_task__mutmut_102, 
        'xǁBaseAgentǁ_execute_task__mutmut_103': xǁBaseAgentǁ_execute_task__mutmut_103, 
        'xǁBaseAgentǁ_execute_task__mutmut_104': xǁBaseAgentǁ_execute_task__mutmut_104, 
        'xǁBaseAgentǁ_execute_task__mutmut_105': xǁBaseAgentǁ_execute_task__mutmut_105, 
        'xǁBaseAgentǁ_execute_task__mutmut_106': xǁBaseAgentǁ_execute_task__mutmut_106, 
        'xǁBaseAgentǁ_execute_task__mutmut_107': xǁBaseAgentǁ_execute_task__mutmut_107
    }
    
    def _execute_task(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁ_execute_task__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁ_execute_task__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _execute_task.__signature__ = _mutmut_signature(xǁBaseAgentǁ_execute_task__mutmut_orig)
    xǁBaseAgentǁ_execute_task__mutmut_orig.__name__ = 'xǁBaseAgentǁ_execute_task'
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_orig(
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
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_1(
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
        event_data = None
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_2(
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
            "XXsession_idXX": str(session_id),
            "agent_type": self.agent_type.value,
        }
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_3(
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
            "SESSION_ID": str(session_id),
            "agent_type": self.agent_type.value,
        }
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_4(
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
            "session_id": str(None),
            "agent_type": self.agent_type.value,
        }
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_5(
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
            "XXagent_typeXX": self.agent_type.value,
        }
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_6(
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
            "AGENT_TYPE": self.agent_type.value,
        }
        await self.event_bus.publish(event_type, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_7(
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
        await self.event_bus.publish(None, event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_8(
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
        await self.event_bus.publish(event_type, None)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_9(
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
        await self.event_bus.publish(event_data)
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_10(
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
        await self.event_bus.publish(event_type, )
        
        logger.debug(
            f"Event published",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_11(
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
            None,
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_12(
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
            agent_type=None,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_13(
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
            event_type=None,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_14(
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
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_15(
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
            event_type=event_type,
        )
    
    # ========================================================================
    # Event Handling
    # ========================================================================
    
    async def xǁBaseAgentǁpublish_event__mutmut_16(
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
            )
    
    xǁBaseAgentǁpublish_event__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁpublish_event__mutmut_1': xǁBaseAgentǁpublish_event__mutmut_1, 
        'xǁBaseAgentǁpublish_event__mutmut_2': xǁBaseAgentǁpublish_event__mutmut_2, 
        'xǁBaseAgentǁpublish_event__mutmut_3': xǁBaseAgentǁpublish_event__mutmut_3, 
        'xǁBaseAgentǁpublish_event__mutmut_4': xǁBaseAgentǁpublish_event__mutmut_4, 
        'xǁBaseAgentǁpublish_event__mutmut_5': xǁBaseAgentǁpublish_event__mutmut_5, 
        'xǁBaseAgentǁpublish_event__mutmut_6': xǁBaseAgentǁpublish_event__mutmut_6, 
        'xǁBaseAgentǁpublish_event__mutmut_7': xǁBaseAgentǁpublish_event__mutmut_7, 
        'xǁBaseAgentǁpublish_event__mutmut_8': xǁBaseAgentǁpublish_event__mutmut_8, 
        'xǁBaseAgentǁpublish_event__mutmut_9': xǁBaseAgentǁpublish_event__mutmut_9, 
        'xǁBaseAgentǁpublish_event__mutmut_10': xǁBaseAgentǁpublish_event__mutmut_10, 
        'xǁBaseAgentǁpublish_event__mutmut_11': xǁBaseAgentǁpublish_event__mutmut_11, 
        'xǁBaseAgentǁpublish_event__mutmut_12': xǁBaseAgentǁpublish_event__mutmut_12, 
        'xǁBaseAgentǁpublish_event__mutmut_13': xǁBaseAgentǁpublish_event__mutmut_13, 
        'xǁBaseAgentǁpublish_event__mutmut_14': xǁBaseAgentǁpublish_event__mutmut_14, 
        'xǁBaseAgentǁpublish_event__mutmut_15': xǁBaseAgentǁpublish_event__mutmut_15, 
        'xǁBaseAgentǁpublish_event__mutmut_16': xǁBaseAgentǁpublish_event__mutmut_16
    }
    
    def publish_event(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁpublish_event__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁpublish_event__mutmut_mutants"), args, kwargs, self)
        return result 
    
    publish_event.__signature__ = _mutmut_signature(xǁBaseAgentǁpublish_event__mutmut_orig)
    xǁBaseAgentǁpublish_event__mutmut_orig.__name__ = 'xǁBaseAgentǁpublish_event'
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_orig(
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
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_1(
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
        self.event_bus.subscribe(None, handler)
        self._event_subscriptions[event_type] = handler
        
        logger.debug(
            f"Subscribed to event",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_2(
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
        self.event_bus.subscribe(event_type, None)
        self._event_subscriptions[event_type] = handler
        
        logger.debug(
            f"Subscribed to event",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_3(
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
        self.event_bus.subscribe(handler)
        self._event_subscriptions[event_type] = handler
        
        logger.debug(
            f"Subscribed to event",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_4(
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
        self.event_bus.subscribe(event_type, )
        self._event_subscriptions[event_type] = handler
        
        logger.debug(
            f"Subscribed to event",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_5(
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
        self._event_subscriptions[event_type] = None
        
        logger.debug(
            f"Subscribed to event",
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_6(
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
            None,
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_7(
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
            agent_type=None,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_8(
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
            event_type=None,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_9(
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
            agent_type=self.agent_type.value,
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_10(
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
            event_type=event_type,
        )
    
    async def xǁBaseAgentǁsubscribe_to_event__mutmut_11(
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
            )
    
    xǁBaseAgentǁsubscribe_to_event__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁsubscribe_to_event__mutmut_1': xǁBaseAgentǁsubscribe_to_event__mutmut_1, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_2': xǁBaseAgentǁsubscribe_to_event__mutmut_2, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_3': xǁBaseAgentǁsubscribe_to_event__mutmut_3, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_4': xǁBaseAgentǁsubscribe_to_event__mutmut_4, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_5': xǁBaseAgentǁsubscribe_to_event__mutmut_5, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_6': xǁBaseAgentǁsubscribe_to_event__mutmut_6, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_7': xǁBaseAgentǁsubscribe_to_event__mutmut_7, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_8': xǁBaseAgentǁsubscribe_to_event__mutmut_8, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_9': xǁBaseAgentǁsubscribe_to_event__mutmut_9, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_10': xǁBaseAgentǁsubscribe_to_event__mutmut_10, 
        'xǁBaseAgentǁsubscribe_to_event__mutmut_11': xǁBaseAgentǁsubscribe_to_event__mutmut_11
    }
    
    def subscribe_to_event(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁsubscribe_to_event__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁsubscribe_to_event__mutmut_mutants"), args, kwargs, self)
        return result 
    
    subscribe_to_event.__signature__ = _mutmut_signature(xǁBaseAgentǁsubscribe_to_event__mutmut_orig)
    xǁBaseAgentǁsubscribe_to_event__mutmut_orig.__name__ = 'xǁBaseAgentǁsubscribe_to_event'
    
    async def _subscribe_to_events(self) -> None:
        """Subscribe to relevant events (to be overridden by subclasses)."""
        pass
    
    async def xǁBaseAgentǁ_unsubscribe_from_events__mutmut_orig(self) -> None:
        """Unsubscribe from all events."""
        for event_type, handler in self._event_subscriptions.items():
            self.event_bus.unsubscribe(event_type, handler)
        
        self._event_subscriptions.clear()
    
    async def xǁBaseAgentǁ_unsubscribe_from_events__mutmut_1(self) -> None:
        """Unsubscribe from all events."""
        for event_type, handler in self._event_subscriptions.items():
            self.event_bus.unsubscribe(None, handler)
        
        self._event_subscriptions.clear()
    
    async def xǁBaseAgentǁ_unsubscribe_from_events__mutmut_2(self) -> None:
        """Unsubscribe from all events."""
        for event_type, handler in self._event_subscriptions.items():
            self.event_bus.unsubscribe(event_type, None)
        
        self._event_subscriptions.clear()
    
    async def xǁBaseAgentǁ_unsubscribe_from_events__mutmut_3(self) -> None:
        """Unsubscribe from all events."""
        for event_type, handler in self._event_subscriptions.items():
            self.event_bus.unsubscribe(handler)
        
        self._event_subscriptions.clear()
    
    async def xǁBaseAgentǁ_unsubscribe_from_events__mutmut_4(self) -> None:
        """Unsubscribe from all events."""
        for event_type, handler in self._event_subscriptions.items():
            self.event_bus.unsubscribe(event_type, )
        
        self._event_subscriptions.clear()
    
    xǁBaseAgentǁ_unsubscribe_from_events__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁ_unsubscribe_from_events__mutmut_1': xǁBaseAgentǁ_unsubscribe_from_events__mutmut_1, 
        'xǁBaseAgentǁ_unsubscribe_from_events__mutmut_2': xǁBaseAgentǁ_unsubscribe_from_events__mutmut_2, 
        'xǁBaseAgentǁ_unsubscribe_from_events__mutmut_3': xǁBaseAgentǁ_unsubscribe_from_events__mutmut_3, 
        'xǁBaseAgentǁ_unsubscribe_from_events__mutmut_4': xǁBaseAgentǁ_unsubscribe_from_events__mutmut_4
    }
    
    def _unsubscribe_from_events(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁ_unsubscribe_from_events__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁ_unsubscribe_from_events__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _unsubscribe_from_events.__signature__ = _mutmut_signature(xǁBaseAgentǁ_unsubscribe_from_events__mutmut_orig)
    xǁBaseAgentǁ_unsubscribe_from_events__mutmut_orig.__name__ = 'xǁBaseAgentǁ_unsubscribe_from_events'
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    async def xǁBaseAgentǁ_wait_for_active_tasks__mutmut_orig(self) -> None:
        """Wait for all active tasks to complete."""
        while self._active_tasks:
            await asyncio.sleep(0.1)
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    async def xǁBaseAgentǁ_wait_for_active_tasks__mutmut_1(self) -> None:
        """Wait for all active tasks to complete."""
        while self._active_tasks:
            await asyncio.sleep(None)
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    async def xǁBaseAgentǁ_wait_for_active_tasks__mutmut_2(self) -> None:
        """Wait for all active tasks to complete."""
        while self._active_tasks:
            await asyncio.sleep(1.1)
    
    xǁBaseAgentǁ_wait_for_active_tasks__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁ_wait_for_active_tasks__mutmut_1': xǁBaseAgentǁ_wait_for_active_tasks__mutmut_1, 
        'xǁBaseAgentǁ_wait_for_active_tasks__mutmut_2': xǁBaseAgentǁ_wait_for_active_tasks__mutmut_2
    }
    
    def _wait_for_active_tasks(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁ_wait_for_active_tasks__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁ_wait_for_active_tasks__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _wait_for_active_tasks.__signature__ = _mutmut_signature(xǁBaseAgentǁ_wait_for_active_tasks__mutmut_orig)
    xǁBaseAgentǁ_wait_for_active_tasks__mutmut_orig.__name__ = 'xǁBaseAgentǁ_wait_for_active_tasks'
    
    def xǁBaseAgentǁget_metrics__mutmut_orig(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self._metrics,
            "state": self.state.value,
            "active_tasks": len(self._active_tasks),
        }
    
    def xǁBaseAgentǁget_metrics__mutmut_1(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self._metrics,
            "XXstateXX": self.state.value,
            "active_tasks": len(self._active_tasks),
        }
    
    def xǁBaseAgentǁget_metrics__mutmut_2(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self._metrics,
            "STATE": self.state.value,
            "active_tasks": len(self._active_tasks),
        }
    
    def xǁBaseAgentǁget_metrics__mutmut_3(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self._metrics,
            "state": self.state.value,
            "XXactive_tasksXX": len(self._active_tasks),
        }
    
    def xǁBaseAgentǁget_metrics__mutmut_4(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self._metrics,
            "state": self.state.value,
            "ACTIVE_TASKS": len(self._active_tasks),
        }
    
    xǁBaseAgentǁget_metrics__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁget_metrics__mutmut_1': xǁBaseAgentǁget_metrics__mutmut_1, 
        'xǁBaseAgentǁget_metrics__mutmut_2': xǁBaseAgentǁget_metrics__mutmut_2, 
        'xǁBaseAgentǁget_metrics__mutmut_3': xǁBaseAgentǁget_metrics__mutmut_3, 
        'xǁBaseAgentǁget_metrics__mutmut_4': xǁBaseAgentǁget_metrics__mutmut_4
    }
    
    def get_metrics(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁget_metrics__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁget_metrics__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_metrics.__signature__ = _mutmut_signature(xǁBaseAgentǁget_metrics__mutmut_orig)
    xǁBaseAgentǁget_metrics__mutmut_orig.__name__ = 'xǁBaseAgentǁget_metrics'
    
    def xǁBaseAgentǁis_running__mutmut_orig(self) -> bool:
        """Check if agent is running."""
        return self.state == AgentState.RUNNING
    
    def xǁBaseAgentǁis_running__mutmut_1(self) -> bool:
        """Check if agent is running."""
        return self.state != AgentState.RUNNING
    
    xǁBaseAgentǁis_running__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁis_running__mutmut_1': xǁBaseAgentǁis_running__mutmut_1
    }
    
    def is_running(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁis_running__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁis_running__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_running.__signature__ = _mutmut_signature(xǁBaseAgentǁis_running__mutmut_orig)
    xǁBaseAgentǁis_running__mutmut_orig.__name__ = 'xǁBaseAgentǁis_running'
    
    def xǁBaseAgentǁis_stopped__mutmut_orig(self) -> bool:
        """Check if agent is stopped."""
        return self.state == AgentState.STOPPED
    
    def xǁBaseAgentǁis_stopped__mutmut_1(self) -> bool:
        """Check if agent is stopped."""
        return self.state != AgentState.STOPPED
    
    xǁBaseAgentǁis_stopped__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseAgentǁis_stopped__mutmut_1': xǁBaseAgentǁis_stopped__mutmut_1
    }
    
    def is_stopped(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseAgentǁis_stopped__mutmut_orig"), object.__getattribute__(self, "xǁBaseAgentǁis_stopped__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_stopped.__signature__ = _mutmut_signature(xǁBaseAgentǁis_stopped__mutmut_orig)
    xǁBaseAgentǁis_stopped__mutmut_orig.__name__ = 'xǁBaseAgentǁis_stopped'
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<{self.__class__.__name__} "
            f"type={self.agent_type.value} "
            f"state={self.state.value}>"
        )
