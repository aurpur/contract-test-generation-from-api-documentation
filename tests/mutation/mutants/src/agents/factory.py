"""
Agent factory for creating and managing agents.

This module provides factory functions and utilities for creating
and configuring agents in the system.

Author: Aurel IKAMA HONEY
"""
from typing import Dict, List, Optional, Type
from uuid import UUID

from .base_agent import BaseAgent, AgentConfig, AgentState
from shared_context import AgentType, ContextManager
from orchestration import MessageRouter, EventBus, TaskQueue
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


class AgentFactory:
    """
    Factory for creating and managing agents.
    
    Provides centralized creation and lifecycle management of all agents.
    """
    
    def xǁAgentFactoryǁ__init____mutmut_orig(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_1(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = None
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_2(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = None
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_3(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = None
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_4(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = None
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_5(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = None
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_6(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = None
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_7(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = None
        
        logger.info("Agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_8(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info(None)
    
    def xǁAgentFactoryǁ__init____mutmut_9(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("XXAgent factory initializedXX")
    
    def xǁAgentFactoryǁ__init____mutmut_10(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("agent factory initialized")
    
    def xǁAgentFactoryǁ__init____mutmut_11(
        self,
        context_manager: ContextManager,
        router: MessageRouter,
        event_bus: EventBus,
        task_queue: TaskQueue,
        config: Config,
    ):
        """
        Initialize agent factory.
        
        Args:
            context_manager: Shared context manager
            router: Message router
            event_bus: Event bus
            task_queue: Task queue
            config: System configuration
        """
        self.context_manager = context_manager
        self.router = router
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.config = config
        
        # Registry of agent types
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        
        # Active agents
        self._agents: Dict[AgentType, BaseAgent] = {}
        
        logger.info("AGENT FACTORY INITIALIZED")
    
    xǁAgentFactoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁ__init____mutmut_1': xǁAgentFactoryǁ__init____mutmut_1, 
        'xǁAgentFactoryǁ__init____mutmut_2': xǁAgentFactoryǁ__init____mutmut_2, 
        'xǁAgentFactoryǁ__init____mutmut_3': xǁAgentFactoryǁ__init____mutmut_3, 
        'xǁAgentFactoryǁ__init____mutmut_4': xǁAgentFactoryǁ__init____mutmut_4, 
        'xǁAgentFactoryǁ__init____mutmut_5': xǁAgentFactoryǁ__init____mutmut_5, 
        'xǁAgentFactoryǁ__init____mutmut_6': xǁAgentFactoryǁ__init____mutmut_6, 
        'xǁAgentFactoryǁ__init____mutmut_7': xǁAgentFactoryǁ__init____mutmut_7, 
        'xǁAgentFactoryǁ__init____mutmut_8': xǁAgentFactoryǁ__init____mutmut_8, 
        'xǁAgentFactoryǁ__init____mutmut_9': xǁAgentFactoryǁ__init____mutmut_9, 
        'xǁAgentFactoryǁ__init____mutmut_10': xǁAgentFactoryǁ__init____mutmut_10, 
        'xǁAgentFactoryǁ__init____mutmut_11': xǁAgentFactoryǁ__init____mutmut_11
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentFactoryǁ__init____mutmut_orig)
    xǁAgentFactoryǁ__init____mutmut_orig.__name__ = 'xǁAgentFactoryǁ__init__'
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_orig(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_1(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_2(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(None, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_3(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, None):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_4(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_5(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, ):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_6(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                None
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_7(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = None
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_8(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            None,
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_9(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=None,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_10(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            agent_class=None,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_11(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_12(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_class=agent_class.__name__,
        )
    
    def xǁAgentFactoryǁregister_agent_class__mutmut_13(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class for a specific agent type.
        
        Args:
            agent_type: Type of agent
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(
                f"Agent class must inherit from BaseAgent: {agent_class}"
            )
        
        self._agent_classes[agent_type] = agent_class
        
        logger.info(
            f"Registered agent class",
            agent_type=agent_type.value,
            )
    
    xǁAgentFactoryǁregister_agent_class__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁregister_agent_class__mutmut_1': xǁAgentFactoryǁregister_agent_class__mutmut_1, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_2': xǁAgentFactoryǁregister_agent_class__mutmut_2, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_3': xǁAgentFactoryǁregister_agent_class__mutmut_3, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_4': xǁAgentFactoryǁregister_agent_class__mutmut_4, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_5': xǁAgentFactoryǁregister_agent_class__mutmut_5, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_6': xǁAgentFactoryǁregister_agent_class__mutmut_6, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_7': xǁAgentFactoryǁregister_agent_class__mutmut_7, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_8': xǁAgentFactoryǁregister_agent_class__mutmut_8, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_9': xǁAgentFactoryǁregister_agent_class__mutmut_9, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_10': xǁAgentFactoryǁregister_agent_class__mutmut_10, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_11': xǁAgentFactoryǁregister_agent_class__mutmut_11, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_12': xǁAgentFactoryǁregister_agent_class__mutmut_12, 
        'xǁAgentFactoryǁregister_agent_class__mutmut_13': xǁAgentFactoryǁregister_agent_class__mutmut_13
    }
    
    def register_agent_class(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁregister_agent_class__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁregister_agent_class__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_agent_class.__signature__ = _mutmut_signature(xǁAgentFactoryǁregister_agent_class__mutmut_orig)
    xǁAgentFactoryǁregister_agent_class__mutmut_orig.__name__ = 'xǁAgentFactoryǁregister_agent_class'
    
    def xǁAgentFactoryǁcreate_agent__mutmut_orig(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_1(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_2(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                None
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_3(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = None
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_4(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is not None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_5(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = None
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_6(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(None)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_7(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is not None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_8(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = None
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_9(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(None)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_10(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = None
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_11(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=None,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_12(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=None,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_13(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=None,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_14(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=None,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_15(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=None,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_16(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=None,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_17(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_18(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_19(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_20(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_21(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_22(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_23(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = None
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_24(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            None,
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_25(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=None,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_26(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=None,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_27(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_28(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def xǁAgentFactoryǁcreate_agent__mutmut_29(
        self,
        agent_type: AgentType,
        agent_config: Optional[AgentConfig] = None,
        llm_config: Optional[Dict] = None,
    ) -> BaseAgent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_config: Agent configuration (uses defaults if not provided)
            llm_config: LLM configuration for the agent
            
        Returns:
            Created agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        # Check if agent class is registered
        if agent_type not in self._agent_classes:
            raise ValueError(
                f"No agent class registered for type: {agent_type.value}"
            )
        
        # Get agent class
        agent_class = self._agent_classes[agent_type]
        
        # Create config if not provided
        if agent_config is None:
            agent_config = self._create_default_config(agent_type)
        
        # Get LLM config
        if llm_config is None:
            llm_config = self._get_llm_config(agent_type)
        
        # Create agent
        agent = agent_class(
            config=agent_config,
            context_manager=self.context_manager,
            router=self.router,
            event_bus=self.event_bus,
            task_queue=self.task_queue,
            llm_config=llm_config,
        )
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            )
        
        return agent
    
    xǁAgentFactoryǁcreate_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁcreate_agent__mutmut_1': xǁAgentFactoryǁcreate_agent__mutmut_1, 
        'xǁAgentFactoryǁcreate_agent__mutmut_2': xǁAgentFactoryǁcreate_agent__mutmut_2, 
        'xǁAgentFactoryǁcreate_agent__mutmut_3': xǁAgentFactoryǁcreate_agent__mutmut_3, 
        'xǁAgentFactoryǁcreate_agent__mutmut_4': xǁAgentFactoryǁcreate_agent__mutmut_4, 
        'xǁAgentFactoryǁcreate_agent__mutmut_5': xǁAgentFactoryǁcreate_agent__mutmut_5, 
        'xǁAgentFactoryǁcreate_agent__mutmut_6': xǁAgentFactoryǁcreate_agent__mutmut_6, 
        'xǁAgentFactoryǁcreate_agent__mutmut_7': xǁAgentFactoryǁcreate_agent__mutmut_7, 
        'xǁAgentFactoryǁcreate_agent__mutmut_8': xǁAgentFactoryǁcreate_agent__mutmut_8, 
        'xǁAgentFactoryǁcreate_agent__mutmut_9': xǁAgentFactoryǁcreate_agent__mutmut_9, 
        'xǁAgentFactoryǁcreate_agent__mutmut_10': xǁAgentFactoryǁcreate_agent__mutmut_10, 
        'xǁAgentFactoryǁcreate_agent__mutmut_11': xǁAgentFactoryǁcreate_agent__mutmut_11, 
        'xǁAgentFactoryǁcreate_agent__mutmut_12': xǁAgentFactoryǁcreate_agent__mutmut_12, 
        'xǁAgentFactoryǁcreate_agent__mutmut_13': xǁAgentFactoryǁcreate_agent__mutmut_13, 
        'xǁAgentFactoryǁcreate_agent__mutmut_14': xǁAgentFactoryǁcreate_agent__mutmut_14, 
        'xǁAgentFactoryǁcreate_agent__mutmut_15': xǁAgentFactoryǁcreate_agent__mutmut_15, 
        'xǁAgentFactoryǁcreate_agent__mutmut_16': xǁAgentFactoryǁcreate_agent__mutmut_16, 
        'xǁAgentFactoryǁcreate_agent__mutmut_17': xǁAgentFactoryǁcreate_agent__mutmut_17, 
        'xǁAgentFactoryǁcreate_agent__mutmut_18': xǁAgentFactoryǁcreate_agent__mutmut_18, 
        'xǁAgentFactoryǁcreate_agent__mutmut_19': xǁAgentFactoryǁcreate_agent__mutmut_19, 
        'xǁAgentFactoryǁcreate_agent__mutmut_20': xǁAgentFactoryǁcreate_agent__mutmut_20, 
        'xǁAgentFactoryǁcreate_agent__mutmut_21': xǁAgentFactoryǁcreate_agent__mutmut_21, 
        'xǁAgentFactoryǁcreate_agent__mutmut_22': xǁAgentFactoryǁcreate_agent__mutmut_22, 
        'xǁAgentFactoryǁcreate_agent__mutmut_23': xǁAgentFactoryǁcreate_agent__mutmut_23, 
        'xǁAgentFactoryǁcreate_agent__mutmut_24': xǁAgentFactoryǁcreate_agent__mutmut_24, 
        'xǁAgentFactoryǁcreate_agent__mutmut_25': xǁAgentFactoryǁcreate_agent__mutmut_25, 
        'xǁAgentFactoryǁcreate_agent__mutmut_26': xǁAgentFactoryǁcreate_agent__mutmut_26, 
        'xǁAgentFactoryǁcreate_agent__mutmut_27': xǁAgentFactoryǁcreate_agent__mutmut_27, 
        'xǁAgentFactoryǁcreate_agent__mutmut_28': xǁAgentFactoryǁcreate_agent__mutmut_28, 
        'xǁAgentFactoryǁcreate_agent__mutmut_29': xǁAgentFactoryǁcreate_agent__mutmut_29
    }
    
    def create_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁcreate_agent__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁcreate_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_agent.__signature__ = _mutmut_signature(xǁAgentFactoryǁcreate_agent__mutmut_orig)
    xǁAgentFactoryǁcreate_agent__mutmut_orig.__name__ = 'xǁAgentFactoryǁcreate_agent'
    
    def xǁAgentFactoryǁget_agent__mutmut_orig(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """
        Get an existing agent instance.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(agent_type)
    
    def xǁAgentFactoryǁget_agent__mutmut_1(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """
        Get an existing agent instance.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(None)
    
    xǁAgentFactoryǁget_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁget_agent__mutmut_1': xǁAgentFactoryǁget_agent__mutmut_1
    }
    
    def get_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁget_agent__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁget_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_agent.__signature__ = _mutmut_signature(xǁAgentFactoryǁget_agent__mutmut_orig)
    xǁAgentFactoryǁget_agent__mutmut_orig.__name__ = 'xǁAgentFactoryǁget_agent'
    
    def xǁAgentFactoryǁget_all_agents__mutmut_orig(self) -> List[BaseAgent]:
        """
        Get all active agents.
        
        Returns:
            List of all agent instances
        """
        return list(self._agents.values())
    
    def xǁAgentFactoryǁget_all_agents__mutmut_1(self) -> List[BaseAgent]:
        """
        Get all active agents.
        
        Returns:
            List of all agent instances
        """
        return list(None)
    
    xǁAgentFactoryǁget_all_agents__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁget_all_agents__mutmut_1': xǁAgentFactoryǁget_all_agents__mutmut_1
    }
    
    def get_all_agents(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁget_all_agents__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁget_all_agents__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_all_agents.__signature__ = _mutmut_signature(xǁAgentFactoryǁget_all_agents__mutmut_orig)
    xǁAgentFactoryǁget_all_agents__mutmut_orig.__name__ = 'xǁAgentFactoryǁget_all_agents'
    
    async def xǁAgentFactoryǁstart_agent__mutmut_orig(self, agent_type: AgentType) -> None:
        """
        Start a specific agent.
        
        Args:
            agent_type: Type of agent to start
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.start()
    
    async def xǁAgentFactoryǁstart_agent__mutmut_1(self, agent_type: AgentType) -> None:
        """
        Start a specific agent.
        
        Args:
            agent_type: Type of agent to start
            
        Raises:
            ValueError: If agent not found
        """
        agent = None
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.start()
    
    async def xǁAgentFactoryǁstart_agent__mutmut_2(self, agent_type: AgentType) -> None:
        """
        Start a specific agent.
        
        Args:
            agent_type: Type of agent to start
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(None)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.start()
    
    async def xǁAgentFactoryǁstart_agent__mutmut_3(self, agent_type: AgentType) -> None:
        """
        Start a specific agent.
        
        Args:
            agent_type: Type of agent to start
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is not None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.start()
    
    async def xǁAgentFactoryǁstart_agent__mutmut_4(self, agent_type: AgentType) -> None:
        """
        Start a specific agent.
        
        Args:
            agent_type: Type of agent to start
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is None:
            raise ValueError(None)
        
        await agent.start()
    
    xǁAgentFactoryǁstart_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁstart_agent__mutmut_1': xǁAgentFactoryǁstart_agent__mutmut_1, 
        'xǁAgentFactoryǁstart_agent__mutmut_2': xǁAgentFactoryǁstart_agent__mutmut_2, 
        'xǁAgentFactoryǁstart_agent__mutmut_3': xǁAgentFactoryǁstart_agent__mutmut_3, 
        'xǁAgentFactoryǁstart_agent__mutmut_4': xǁAgentFactoryǁstart_agent__mutmut_4
    }
    
    def start_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁstart_agent__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁstart_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start_agent.__signature__ = _mutmut_signature(xǁAgentFactoryǁstart_agent__mutmut_orig)
    xǁAgentFactoryǁstart_agent__mutmut_orig.__name__ = 'xǁAgentFactoryǁstart_agent'
    
    async def xǁAgentFactoryǁstop_agent__mutmut_orig(
        self,
        agent_type: AgentType,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.stop(timeout=timeout)
    
    async def xǁAgentFactoryǁstop_agent__mutmut_1(
        self,
        agent_type: AgentType,
        timeout: float = 31.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.stop(timeout=timeout)
    
    async def xǁAgentFactoryǁstop_agent__mutmut_2(
        self,
        agent_type: AgentType,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = None
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.stop(timeout=timeout)
    
    async def xǁAgentFactoryǁstop_agent__mutmut_3(
        self,
        agent_type: AgentType,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(None)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.stop(timeout=timeout)
    
    async def xǁAgentFactoryǁstop_agent__mutmut_4(
        self,
        agent_type: AgentType,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is not None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.stop(timeout=timeout)
    
    async def xǁAgentFactoryǁstop_agent__mutmut_5(
        self,
        agent_type: AgentType,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is None:
            raise ValueError(None)
        
        await agent.stop(timeout=timeout)
    
    async def xǁAgentFactoryǁstop_agent__mutmut_6(
        self,
        agent_type: AgentType,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop a specific agent.
        
        Args:
            agent_type: Type of agent to stop
            timeout: Shutdown timeout (seconds)
            
        Raises:
            ValueError: If agent not found
        """
        agent = self.get_agent(agent_type)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_type.value}")
        
        await agent.stop(timeout=None)
    
    xǁAgentFactoryǁstop_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁstop_agent__mutmut_1': xǁAgentFactoryǁstop_agent__mutmut_1, 
        'xǁAgentFactoryǁstop_agent__mutmut_2': xǁAgentFactoryǁstop_agent__mutmut_2, 
        'xǁAgentFactoryǁstop_agent__mutmut_3': xǁAgentFactoryǁstop_agent__mutmut_3, 
        'xǁAgentFactoryǁstop_agent__mutmut_4': xǁAgentFactoryǁstop_agent__mutmut_4, 
        'xǁAgentFactoryǁstop_agent__mutmut_5': xǁAgentFactoryǁstop_agent__mutmut_5, 
        'xǁAgentFactoryǁstop_agent__mutmut_6': xǁAgentFactoryǁstop_agent__mutmut_6
    }
    
    def stop_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁstop_agent__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁstop_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop_agent.__signature__ = _mutmut_signature(xǁAgentFactoryǁstop_agent__mutmut_orig)
    xǁAgentFactoryǁstop_agent__mutmut_orig.__name__ = 'xǁAgentFactoryǁstop_agent'
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_orig(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_1(self) -> None:
        """Start all registered agents."""
        logger.info(None)
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_2(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    None,
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_3(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=None,
                    error=str(e),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_4(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=None,
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_5(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_6(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    error=str(e),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_7(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_8(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(None),
                )
                raise
        
        logger.info("All agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_9(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info(None)
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_10(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("XXAll agents started successfullyXX")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_11(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("all agents started successfully")
    
    async def xǁAgentFactoryǁstart_all_agents__mutmut_12(self) -> None:
        """Start all registered agents."""
        logger.info(f"Starting {len(self._agents)} agents")
        
        for agent_type, agent in self._agents.items():
            try:
                await agent.start()
            except Exception as e:
                logger.error(
                    f"Failed to start agent",
                    agent_type=agent_type.value,
                    error=str(e),
                )
                raise
        
        logger.info("ALL AGENTS STARTED SUCCESSFULLY")
    
    xǁAgentFactoryǁstart_all_agents__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁstart_all_agents__mutmut_1': xǁAgentFactoryǁstart_all_agents__mutmut_1, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_2': xǁAgentFactoryǁstart_all_agents__mutmut_2, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_3': xǁAgentFactoryǁstart_all_agents__mutmut_3, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_4': xǁAgentFactoryǁstart_all_agents__mutmut_4, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_5': xǁAgentFactoryǁstart_all_agents__mutmut_5, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_6': xǁAgentFactoryǁstart_all_agents__mutmut_6, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_7': xǁAgentFactoryǁstart_all_agents__mutmut_7, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_8': xǁAgentFactoryǁstart_all_agents__mutmut_8, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_9': xǁAgentFactoryǁstart_all_agents__mutmut_9, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_10': xǁAgentFactoryǁstart_all_agents__mutmut_10, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_11': xǁAgentFactoryǁstart_all_agents__mutmut_11, 
        'xǁAgentFactoryǁstart_all_agents__mutmut_12': xǁAgentFactoryǁstart_all_agents__mutmut_12
    }
    
    def start_all_agents(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁstart_all_agents__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁstart_all_agents__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start_all_agents.__signature__ = _mutmut_signature(xǁAgentFactoryǁstart_all_agents__mutmut_orig)
    xǁAgentFactoryǁstart_all_agents__mutmut_orig.__name__ = 'xǁAgentFactoryǁstart_all_agents'
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_orig(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_1(self, timeout: float = 31.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_2(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(None)
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_3(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = None
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_4(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = None
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_5(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(None)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_6(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent or agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_7(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=None)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_8(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        None,
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_9(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=None,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_10(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=None,
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_11(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_12(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        error=str(e),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_13(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_14(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(None),
                    )
        
        logger.info("All agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_15(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info(None)
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_16(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("XXAll agents stoppedXX")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_17(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("all agents stopped")
    
    async def xǁAgentFactoryǁstop_all_agents__mutmut_18(self, timeout: float = 30.0) -> None:
        """
        Stop all registered agents.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        logger.info(f"Stopping {len(self._agents)} agents")
        
        # Stop in reverse order (Runner -> Contractor -> Oracle -> Inductor)
        agent_types = [
            AgentType.RUNNER,
            AgentType.CONTRACTOR,
            AgentType.ORACLE,
            AgentType.INDUCTOR,
        ]
        
        for agent_type in agent_types:
            agent = self.get_agent(agent_type)
            if agent and agent.is_running():
                try:
                    await agent.stop(timeout=timeout)
                except Exception as e:
                    logger.error(
                        f"Error stopping agent",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
        
        logger.info("ALL AGENTS STOPPED")
    
    xǁAgentFactoryǁstop_all_agents__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁstop_all_agents__mutmut_1': xǁAgentFactoryǁstop_all_agents__mutmut_1, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_2': xǁAgentFactoryǁstop_all_agents__mutmut_2, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_3': xǁAgentFactoryǁstop_all_agents__mutmut_3, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_4': xǁAgentFactoryǁstop_all_agents__mutmut_4, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_5': xǁAgentFactoryǁstop_all_agents__mutmut_5, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_6': xǁAgentFactoryǁstop_all_agents__mutmut_6, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_7': xǁAgentFactoryǁstop_all_agents__mutmut_7, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_8': xǁAgentFactoryǁstop_all_agents__mutmut_8, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_9': xǁAgentFactoryǁstop_all_agents__mutmut_9, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_10': xǁAgentFactoryǁstop_all_agents__mutmut_10, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_11': xǁAgentFactoryǁstop_all_agents__mutmut_11, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_12': xǁAgentFactoryǁstop_all_agents__mutmut_12, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_13': xǁAgentFactoryǁstop_all_agents__mutmut_13, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_14': xǁAgentFactoryǁstop_all_agents__mutmut_14, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_15': xǁAgentFactoryǁstop_all_agents__mutmut_15, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_16': xǁAgentFactoryǁstop_all_agents__mutmut_16, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_17': xǁAgentFactoryǁstop_all_agents__mutmut_17, 
        'xǁAgentFactoryǁstop_all_agents__mutmut_18': xǁAgentFactoryǁstop_all_agents__mutmut_18
    }
    
    def stop_all_agents(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁstop_all_agents__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁstop_all_agents__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop_all_agents.__signature__ = _mutmut_signature(xǁAgentFactoryǁstop_all_agents__mutmut_orig)
    xǁAgentFactoryǁstop_all_agents__mutmut_orig.__name__ = 'xǁAgentFactoryǁstop_all_agents'
    
    def get_agent_metrics(self) -> Dict[str, Dict]:
        """
        Get metrics from all agents.
        
        Returns:
            Dictionary mapping agent types to their metrics
        """
        return {
            agent_type.value: agent.get_metrics()
            for agent_type, agent in self._agents.items()
        }
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_orig(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_1(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = None
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_2(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            None,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_3(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            None,
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_4(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_5(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_6(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get(None, {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_7(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", None).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_8(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get({}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_9(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", ).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_10(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("XXagentsXX", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_11(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("AGENTS", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_12(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=None,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_13(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=None,
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_14(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=None,
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_15(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=None,
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_16(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=None,
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_17(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=None,
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_18(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=None,
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_19(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=None,
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_20(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_21(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_22(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_23(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_24(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_25(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_26(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_27(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_28(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get(None, 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_29(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", None),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_30(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get(5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_31(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", ),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_32(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("XXmax_concurrent_tasksXX", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_33(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("MAX_CONCURRENT_TASKS", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_34(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 6),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_35(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get(None, 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_36(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", None),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_37(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get(300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_38(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", ),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_39(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("XXtask_timeoutXX", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_40(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("TASK_TIMEOUT", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_41(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 301.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_42(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get(None, 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_43(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", None),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_44(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get(30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_45(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", ),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_46(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("XXmessage_timeoutXX", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_47(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("MESSAGE_TIMEOUT", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_48(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 31.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_49(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get(None, 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_50(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", None),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_51(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get(3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_52(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", ),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_53(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("XXretry_limitXX", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_54(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("RETRY_LIMIT", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_55(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 4),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_56(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get(None, True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_57(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", None),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_58(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get(True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_59(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", ),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_60(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("XXenable_metricsXX", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_61(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("ENABLE_METRICS", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_62(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", False),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_63(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get(None, True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_64(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", None),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_65(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get(True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_66(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", ),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_67(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("XXenable_tracingXX", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_68(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("ENABLE_TRACING", True),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_69(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", False),
            custom_config=agent_settings.get("config", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_70(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get(None, {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_71(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", None),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_72(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get({}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_73(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("config", ),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_74(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("XXconfigXX", {}),
        )
    
    def xǁAgentFactoryǁ_create_default_config__mutmut_75(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        )
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.get("max_concurrent_tasks", 5),
            task_timeout=agent_settings.get("task_timeout", 300.0),
            message_timeout=agent_settings.get("message_timeout", 30.0),
            retry_limit=agent_settings.get("retry_limit", 3),
            enable_metrics=agent_settings.get("enable_metrics", True),
            enable_tracing=agent_settings.get("enable_tracing", True),
            custom_config=agent_settings.get("CONFIG", {}),
        )
    
    xǁAgentFactoryǁ_create_default_config__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁ_create_default_config__mutmut_1': xǁAgentFactoryǁ_create_default_config__mutmut_1, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_2': xǁAgentFactoryǁ_create_default_config__mutmut_2, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_3': xǁAgentFactoryǁ_create_default_config__mutmut_3, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_4': xǁAgentFactoryǁ_create_default_config__mutmut_4, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_5': xǁAgentFactoryǁ_create_default_config__mutmut_5, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_6': xǁAgentFactoryǁ_create_default_config__mutmut_6, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_7': xǁAgentFactoryǁ_create_default_config__mutmut_7, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_8': xǁAgentFactoryǁ_create_default_config__mutmut_8, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_9': xǁAgentFactoryǁ_create_default_config__mutmut_9, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_10': xǁAgentFactoryǁ_create_default_config__mutmut_10, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_11': xǁAgentFactoryǁ_create_default_config__mutmut_11, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_12': xǁAgentFactoryǁ_create_default_config__mutmut_12, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_13': xǁAgentFactoryǁ_create_default_config__mutmut_13, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_14': xǁAgentFactoryǁ_create_default_config__mutmut_14, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_15': xǁAgentFactoryǁ_create_default_config__mutmut_15, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_16': xǁAgentFactoryǁ_create_default_config__mutmut_16, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_17': xǁAgentFactoryǁ_create_default_config__mutmut_17, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_18': xǁAgentFactoryǁ_create_default_config__mutmut_18, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_19': xǁAgentFactoryǁ_create_default_config__mutmut_19, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_20': xǁAgentFactoryǁ_create_default_config__mutmut_20, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_21': xǁAgentFactoryǁ_create_default_config__mutmut_21, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_22': xǁAgentFactoryǁ_create_default_config__mutmut_22, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_23': xǁAgentFactoryǁ_create_default_config__mutmut_23, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_24': xǁAgentFactoryǁ_create_default_config__mutmut_24, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_25': xǁAgentFactoryǁ_create_default_config__mutmut_25, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_26': xǁAgentFactoryǁ_create_default_config__mutmut_26, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_27': xǁAgentFactoryǁ_create_default_config__mutmut_27, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_28': xǁAgentFactoryǁ_create_default_config__mutmut_28, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_29': xǁAgentFactoryǁ_create_default_config__mutmut_29, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_30': xǁAgentFactoryǁ_create_default_config__mutmut_30, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_31': xǁAgentFactoryǁ_create_default_config__mutmut_31, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_32': xǁAgentFactoryǁ_create_default_config__mutmut_32, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_33': xǁAgentFactoryǁ_create_default_config__mutmut_33, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_34': xǁAgentFactoryǁ_create_default_config__mutmut_34, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_35': xǁAgentFactoryǁ_create_default_config__mutmut_35, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_36': xǁAgentFactoryǁ_create_default_config__mutmut_36, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_37': xǁAgentFactoryǁ_create_default_config__mutmut_37, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_38': xǁAgentFactoryǁ_create_default_config__mutmut_38, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_39': xǁAgentFactoryǁ_create_default_config__mutmut_39, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_40': xǁAgentFactoryǁ_create_default_config__mutmut_40, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_41': xǁAgentFactoryǁ_create_default_config__mutmut_41, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_42': xǁAgentFactoryǁ_create_default_config__mutmut_42, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_43': xǁAgentFactoryǁ_create_default_config__mutmut_43, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_44': xǁAgentFactoryǁ_create_default_config__mutmut_44, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_45': xǁAgentFactoryǁ_create_default_config__mutmut_45, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_46': xǁAgentFactoryǁ_create_default_config__mutmut_46, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_47': xǁAgentFactoryǁ_create_default_config__mutmut_47, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_48': xǁAgentFactoryǁ_create_default_config__mutmut_48, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_49': xǁAgentFactoryǁ_create_default_config__mutmut_49, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_50': xǁAgentFactoryǁ_create_default_config__mutmut_50, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_51': xǁAgentFactoryǁ_create_default_config__mutmut_51, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_52': xǁAgentFactoryǁ_create_default_config__mutmut_52, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_53': xǁAgentFactoryǁ_create_default_config__mutmut_53, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_54': xǁAgentFactoryǁ_create_default_config__mutmut_54, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_55': xǁAgentFactoryǁ_create_default_config__mutmut_55, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_56': xǁAgentFactoryǁ_create_default_config__mutmut_56, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_57': xǁAgentFactoryǁ_create_default_config__mutmut_57, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_58': xǁAgentFactoryǁ_create_default_config__mutmut_58, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_59': xǁAgentFactoryǁ_create_default_config__mutmut_59, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_60': xǁAgentFactoryǁ_create_default_config__mutmut_60, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_61': xǁAgentFactoryǁ_create_default_config__mutmut_61, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_62': xǁAgentFactoryǁ_create_default_config__mutmut_62, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_63': xǁAgentFactoryǁ_create_default_config__mutmut_63, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_64': xǁAgentFactoryǁ_create_default_config__mutmut_64, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_65': xǁAgentFactoryǁ_create_default_config__mutmut_65, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_66': xǁAgentFactoryǁ_create_default_config__mutmut_66, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_67': xǁAgentFactoryǁ_create_default_config__mutmut_67, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_68': xǁAgentFactoryǁ_create_default_config__mutmut_68, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_69': xǁAgentFactoryǁ_create_default_config__mutmut_69, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_70': xǁAgentFactoryǁ_create_default_config__mutmut_70, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_71': xǁAgentFactoryǁ_create_default_config__mutmut_71, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_72': xǁAgentFactoryǁ_create_default_config__mutmut_72, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_73': xǁAgentFactoryǁ_create_default_config__mutmut_73, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_74': xǁAgentFactoryǁ_create_default_config__mutmut_74, 
        'xǁAgentFactoryǁ_create_default_config__mutmut_75': xǁAgentFactoryǁ_create_default_config__mutmut_75
    }
    
    def _create_default_config(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁ_create_default_config__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁ_create_default_config__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _create_default_config.__signature__ = _mutmut_signature(xǁAgentFactoryǁ_create_default_config__mutmut_orig)
    xǁAgentFactoryǁ_create_default_config__mutmut_orig.__name__ = 'xǁAgentFactoryǁ_create_default_config'
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_orig(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_1(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = None
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_2(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get(None, {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_3(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", None)
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_4(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get({})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_5(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", )
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_6(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("XXllmXX", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_7(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("LLM", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_8(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = None
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_9(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get(None, {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_10(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", None)
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_11(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get({})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_12(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("llm", )
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_13(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            None,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_14(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            None,
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_15(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_16(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_17(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get(None, {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_18(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", None).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_19(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get({}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_20(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", ).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_21(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("XXagentsXX", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_22(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("AGENTS", {}).get(
            agent_type.value,
            {},
        ).get("llm", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_23(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("XXllmXX", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    def xǁAgentFactoryǁ_get_llm_config__mutmut_24(self, agent_type: AgentType) -> Dict:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration
        """
        llm_config = self.config.get("llm", {})
        
        # Get agent-specific LLM settings if available
        agent_llm = self.config.get("agents", {}).get(
            agent_type.value,
            {},
        ).get("LLM", {})
        
        # Merge with defaults
        return {
            **llm_config,
            **agent_llm,
        }
    
    xǁAgentFactoryǁ_get_llm_config__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentFactoryǁ_get_llm_config__mutmut_1': xǁAgentFactoryǁ_get_llm_config__mutmut_1, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_2': xǁAgentFactoryǁ_get_llm_config__mutmut_2, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_3': xǁAgentFactoryǁ_get_llm_config__mutmut_3, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_4': xǁAgentFactoryǁ_get_llm_config__mutmut_4, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_5': xǁAgentFactoryǁ_get_llm_config__mutmut_5, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_6': xǁAgentFactoryǁ_get_llm_config__mutmut_6, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_7': xǁAgentFactoryǁ_get_llm_config__mutmut_7, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_8': xǁAgentFactoryǁ_get_llm_config__mutmut_8, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_9': xǁAgentFactoryǁ_get_llm_config__mutmut_9, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_10': xǁAgentFactoryǁ_get_llm_config__mutmut_10, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_11': xǁAgentFactoryǁ_get_llm_config__mutmut_11, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_12': xǁAgentFactoryǁ_get_llm_config__mutmut_12, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_13': xǁAgentFactoryǁ_get_llm_config__mutmut_13, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_14': xǁAgentFactoryǁ_get_llm_config__mutmut_14, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_15': xǁAgentFactoryǁ_get_llm_config__mutmut_15, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_16': xǁAgentFactoryǁ_get_llm_config__mutmut_16, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_17': xǁAgentFactoryǁ_get_llm_config__mutmut_17, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_18': xǁAgentFactoryǁ_get_llm_config__mutmut_18, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_19': xǁAgentFactoryǁ_get_llm_config__mutmut_19, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_20': xǁAgentFactoryǁ_get_llm_config__mutmut_20, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_21': xǁAgentFactoryǁ_get_llm_config__mutmut_21, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_22': xǁAgentFactoryǁ_get_llm_config__mutmut_22, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_23': xǁAgentFactoryǁ_get_llm_config__mutmut_23, 
        'xǁAgentFactoryǁ_get_llm_config__mutmut_24': xǁAgentFactoryǁ_get_llm_config__mutmut_24
    }
    
    def _get_llm_config(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentFactoryǁ_get_llm_config__mutmut_orig"), object.__getattribute__(self, "xǁAgentFactoryǁ_get_llm_config__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_llm_config.__signature__ = _mutmut_signature(xǁAgentFactoryǁ_get_llm_config__mutmut_orig)
    xǁAgentFactoryǁ_get_llm_config__mutmut_orig.__name__ = 'xǁAgentFactoryǁ_get_llm_config'


class AgentOrchestrator:
    """
    Orchestrates the execution of all agents.
    
    Provides high-level coordination of the multi-agent workflow.
    """
    
    def xǁAgentOrchestratorǁ__init____mutmut_orig(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = False
        
        logger.info("Agent orchestrator initialized")
    
    def xǁAgentOrchestratorǁ__init____mutmut_1(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = None
        self._is_running = False
        
        logger.info("Agent orchestrator initialized")
    
    def xǁAgentOrchestratorǁ__init____mutmut_2(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = None
        
        logger.info("Agent orchestrator initialized")
    
    def xǁAgentOrchestratorǁ__init____mutmut_3(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = True
        
        logger.info("Agent orchestrator initialized")
    
    def xǁAgentOrchestratorǁ__init____mutmut_4(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = False
        
        logger.info(None)
    
    def xǁAgentOrchestratorǁ__init____mutmut_5(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = False
        
        logger.info("XXAgent orchestrator initializedXX")
    
    def xǁAgentOrchestratorǁ__init____mutmut_6(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = False
        
        logger.info("agent orchestrator initialized")
    
    def xǁAgentOrchestratorǁ__init____mutmut_7(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = False
        
        logger.info("AGENT ORCHESTRATOR INITIALIZED")
    
    xǁAgentOrchestratorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentOrchestratorǁ__init____mutmut_1': xǁAgentOrchestratorǁ__init____mutmut_1, 
        'xǁAgentOrchestratorǁ__init____mutmut_2': xǁAgentOrchestratorǁ__init____mutmut_2, 
        'xǁAgentOrchestratorǁ__init____mutmut_3': xǁAgentOrchestratorǁ__init____mutmut_3, 
        'xǁAgentOrchestratorǁ__init____mutmut_4': xǁAgentOrchestratorǁ__init____mutmut_4, 
        'xǁAgentOrchestratorǁ__init____mutmut_5': xǁAgentOrchestratorǁ__init____mutmut_5, 
        'xǁAgentOrchestratorǁ__init____mutmut_6': xǁAgentOrchestratorǁ__init____mutmut_6, 
        'xǁAgentOrchestratorǁ__init____mutmut_7': xǁAgentOrchestratorǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentOrchestratorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentOrchestratorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentOrchestratorǁ__init____mutmut_orig)
    xǁAgentOrchestratorǁ__init____mutmut_orig.__name__ = 'xǁAgentOrchestratorǁ__init__'
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_orig(self) -> None:
        """Initialize all agents."""
        logger.info("Initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("Agent system initialized")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_1(self) -> None:
        """Initialize all agents."""
        logger.info(None)
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("Agent system initialized")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_2(self) -> None:
        """Initialize all agents."""
        logger.info("XXInitializing agent systemXX")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("Agent system initialized")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_3(self) -> None:
        """Initialize all agents."""
        logger.info("initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("Agent system initialized")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_4(self) -> None:
        """Initialize all agents."""
        logger.info("INITIALIZING AGENT SYSTEM")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("Agent system initialized")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_5(self) -> None:
        """Initialize all agents."""
        logger.info("Initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info(None)
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_6(self) -> None:
        """Initialize all agents."""
        logger.info("Initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("XXAgent system initializedXX")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_7(self) -> None:
        """Initialize all agents."""
        logger.info("Initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("agent system initialized")
    
    async def xǁAgentOrchestratorǁinitialize__mutmut_8(self) -> None:
        """Initialize all agents."""
        logger.info("Initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("AGENT SYSTEM INITIALIZED")
    
    xǁAgentOrchestratorǁinitialize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentOrchestratorǁinitialize__mutmut_1': xǁAgentOrchestratorǁinitialize__mutmut_1, 
        'xǁAgentOrchestratorǁinitialize__mutmut_2': xǁAgentOrchestratorǁinitialize__mutmut_2, 
        'xǁAgentOrchestratorǁinitialize__mutmut_3': xǁAgentOrchestratorǁinitialize__mutmut_3, 
        'xǁAgentOrchestratorǁinitialize__mutmut_4': xǁAgentOrchestratorǁinitialize__mutmut_4, 
        'xǁAgentOrchestratorǁinitialize__mutmut_5': xǁAgentOrchestratorǁinitialize__mutmut_5, 
        'xǁAgentOrchestratorǁinitialize__mutmut_6': xǁAgentOrchestratorǁinitialize__mutmut_6, 
        'xǁAgentOrchestratorǁinitialize__mutmut_7': xǁAgentOrchestratorǁinitialize__mutmut_7, 
        'xǁAgentOrchestratorǁinitialize__mutmut_8': xǁAgentOrchestratorǁinitialize__mutmut_8
    }
    
    def initialize(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentOrchestratorǁinitialize__mutmut_orig"), object.__getattribute__(self, "xǁAgentOrchestratorǁinitialize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    initialize.__signature__ = _mutmut_signature(xǁAgentOrchestratorǁinitialize__mutmut_orig)
    xǁAgentOrchestratorǁinitialize__mutmut_orig.__name__ = 'xǁAgentOrchestratorǁinitialize'
    
    async def xǁAgentOrchestratorǁstart__mutmut_orig(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_1(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning(None)
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_2(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("XXAgent system already runningXX")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_3(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_4(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("AGENT SYSTEM ALREADY RUNNING")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_5(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info(None)
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_6(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("XXStarting agent systemXX")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_7(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_8(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("STARTING AGENT SYSTEM")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_9(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = None
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_10(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = False
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_11(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info(None)
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_12(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("XXAgent system started successfullyXX")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_13(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_14(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("AGENT SYSTEM STARTED SUCCESSFULLY")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_15(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(None, error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_16(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=None)
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_17(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(error=str(e))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_18(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", )
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    async def xǁAgentOrchestratorǁstart__mutmut_19(self) -> None:
        """Start the agent system."""
        if self._is_running:
            logger.warning("Agent system already running")
            return
        
        logger.info("Starting agent system")
        
        try:
            await self.factory.start_all_agents()
            self._is_running = True
            
            logger.info("Agent system started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agent system", error=str(None))
            # Try to stop any agents that were started
            await self.factory.stop_all_agents()
            raise
    
    xǁAgentOrchestratorǁstart__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentOrchestratorǁstart__mutmut_1': xǁAgentOrchestratorǁstart__mutmut_1, 
        'xǁAgentOrchestratorǁstart__mutmut_2': xǁAgentOrchestratorǁstart__mutmut_2, 
        'xǁAgentOrchestratorǁstart__mutmut_3': xǁAgentOrchestratorǁstart__mutmut_3, 
        'xǁAgentOrchestratorǁstart__mutmut_4': xǁAgentOrchestratorǁstart__mutmut_4, 
        'xǁAgentOrchestratorǁstart__mutmut_5': xǁAgentOrchestratorǁstart__mutmut_5, 
        'xǁAgentOrchestratorǁstart__mutmut_6': xǁAgentOrchestratorǁstart__mutmut_6, 
        'xǁAgentOrchestratorǁstart__mutmut_7': xǁAgentOrchestratorǁstart__mutmut_7, 
        'xǁAgentOrchestratorǁstart__mutmut_8': xǁAgentOrchestratorǁstart__mutmut_8, 
        'xǁAgentOrchestratorǁstart__mutmut_9': xǁAgentOrchestratorǁstart__mutmut_9, 
        'xǁAgentOrchestratorǁstart__mutmut_10': xǁAgentOrchestratorǁstart__mutmut_10, 
        'xǁAgentOrchestratorǁstart__mutmut_11': xǁAgentOrchestratorǁstart__mutmut_11, 
        'xǁAgentOrchestratorǁstart__mutmut_12': xǁAgentOrchestratorǁstart__mutmut_12, 
        'xǁAgentOrchestratorǁstart__mutmut_13': xǁAgentOrchestratorǁstart__mutmut_13, 
        'xǁAgentOrchestratorǁstart__mutmut_14': xǁAgentOrchestratorǁstart__mutmut_14, 
        'xǁAgentOrchestratorǁstart__mutmut_15': xǁAgentOrchestratorǁstart__mutmut_15, 
        'xǁAgentOrchestratorǁstart__mutmut_16': xǁAgentOrchestratorǁstart__mutmut_16, 
        'xǁAgentOrchestratorǁstart__mutmut_17': xǁAgentOrchestratorǁstart__mutmut_17, 
        'xǁAgentOrchestratorǁstart__mutmut_18': xǁAgentOrchestratorǁstart__mutmut_18, 
        'xǁAgentOrchestratorǁstart__mutmut_19': xǁAgentOrchestratorǁstart__mutmut_19
    }
    
    def start(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentOrchestratorǁstart__mutmut_orig"), object.__getattribute__(self, "xǁAgentOrchestratorǁstart__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start.__signature__ = _mutmut_signature(xǁAgentOrchestratorǁstart__mutmut_orig)
    xǁAgentOrchestratorǁstart__mutmut_orig.__name__ = 'xǁAgentOrchestratorǁstart'
    
    async def xǁAgentOrchestratorǁstop__mutmut_orig(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_1(self, timeout: float = 31.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_2(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_3(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning(None)
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_4(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("XXAgent system not runningXX")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_5(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_6(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("AGENT SYSTEM NOT RUNNING")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_7(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info(None)
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_8(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("XXStopping agent systemXX")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_9(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_10(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("STOPPING AGENT SYSTEM")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_11(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=None)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_12(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = None
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_13(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = True
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_14(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info(None)
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_15(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("XXAgent system stopped successfullyXX")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_16(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_17(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("AGENT SYSTEM STOPPED SUCCESSFULLY")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_18(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(None, error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_19(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=None)
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_20(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(error=str(e))
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_21(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", )
            raise
    
    async def xǁAgentOrchestratorǁstop__mutmut_22(self, timeout: float = 30.0) -> None:
        """
        Stop the agent system.
        
        Args:
            timeout: Shutdown timeout per agent (seconds)
        """
        if not self._is_running:
            logger.warning("Agent system not running")
            return
        
        logger.info("Stopping agent system")
        
        try:
            await self.factory.stop_all_agents(timeout=timeout)
            self._is_running = False
            
            logger.info("Agent system stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agent system", error=str(None))
            raise
    
    xǁAgentOrchestratorǁstop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentOrchestratorǁstop__mutmut_1': xǁAgentOrchestratorǁstop__mutmut_1, 
        'xǁAgentOrchestratorǁstop__mutmut_2': xǁAgentOrchestratorǁstop__mutmut_2, 
        'xǁAgentOrchestratorǁstop__mutmut_3': xǁAgentOrchestratorǁstop__mutmut_3, 
        'xǁAgentOrchestratorǁstop__mutmut_4': xǁAgentOrchestratorǁstop__mutmut_4, 
        'xǁAgentOrchestratorǁstop__mutmut_5': xǁAgentOrchestratorǁstop__mutmut_5, 
        'xǁAgentOrchestratorǁstop__mutmut_6': xǁAgentOrchestratorǁstop__mutmut_6, 
        'xǁAgentOrchestratorǁstop__mutmut_7': xǁAgentOrchestratorǁstop__mutmut_7, 
        'xǁAgentOrchestratorǁstop__mutmut_8': xǁAgentOrchestratorǁstop__mutmut_8, 
        'xǁAgentOrchestratorǁstop__mutmut_9': xǁAgentOrchestratorǁstop__mutmut_9, 
        'xǁAgentOrchestratorǁstop__mutmut_10': xǁAgentOrchestratorǁstop__mutmut_10, 
        'xǁAgentOrchestratorǁstop__mutmut_11': xǁAgentOrchestratorǁstop__mutmut_11, 
        'xǁAgentOrchestratorǁstop__mutmut_12': xǁAgentOrchestratorǁstop__mutmut_12, 
        'xǁAgentOrchestratorǁstop__mutmut_13': xǁAgentOrchestratorǁstop__mutmut_13, 
        'xǁAgentOrchestratorǁstop__mutmut_14': xǁAgentOrchestratorǁstop__mutmut_14, 
        'xǁAgentOrchestratorǁstop__mutmut_15': xǁAgentOrchestratorǁstop__mutmut_15, 
        'xǁAgentOrchestratorǁstop__mutmut_16': xǁAgentOrchestratorǁstop__mutmut_16, 
        'xǁAgentOrchestratorǁstop__mutmut_17': xǁAgentOrchestratorǁstop__mutmut_17, 
        'xǁAgentOrchestratorǁstop__mutmut_18': xǁAgentOrchestratorǁstop__mutmut_18, 
        'xǁAgentOrchestratorǁstop__mutmut_19': xǁAgentOrchestratorǁstop__mutmut_19, 
        'xǁAgentOrchestratorǁstop__mutmut_20': xǁAgentOrchestratorǁstop__mutmut_20, 
        'xǁAgentOrchestratorǁstop__mutmut_21': xǁAgentOrchestratorǁstop__mutmut_21, 
        'xǁAgentOrchestratorǁstop__mutmut_22': xǁAgentOrchestratorǁstop__mutmut_22
    }
    
    def stop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentOrchestratorǁstop__mutmut_orig"), object.__getattribute__(self, "xǁAgentOrchestratorǁstop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop.__signature__ = _mutmut_signature(xǁAgentOrchestratorǁstop__mutmut_orig)
    xǁAgentOrchestratorǁstop__mutmut_orig.__name__ = 'xǁAgentOrchestratorǁstop'
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_orig(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_1(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            None,
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_2(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=None,
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_3(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_4(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_5(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(None),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_6(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            None,
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_7(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=None,
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_8(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            session_id=str(session_id),
        )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_9(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            )
    
    async def xǁAgentOrchestratorǁprocess_workflow__mutmut_10(self, session_id: UUID) -> None:
        """
        Process a complete workflow for a session.
        
        This coordinates the execution of all agents in the correct order:
        1. Inductor: Extract API context
        2. Oracle: Generate test oracles
        3. Contractor: Generate test code
        4. Runner: Execute tests and collect results
        
        Args:
            session_id: Session ID for the workflow
        """
        logger.info(
            f"Starting workflow execution",
            session_id=str(session_id),
        )
        
        # For now, this is a placeholder
        # The actual workflow will be implemented in Phase 4.6
        
        logger.info(
            f"Workflow execution completed",
            session_id=str(None),
        )
    
    xǁAgentOrchestratorǁprocess_workflow__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentOrchestratorǁprocess_workflow__mutmut_1': xǁAgentOrchestratorǁprocess_workflow__mutmut_1, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_2': xǁAgentOrchestratorǁprocess_workflow__mutmut_2, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_3': xǁAgentOrchestratorǁprocess_workflow__mutmut_3, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_4': xǁAgentOrchestratorǁprocess_workflow__mutmut_4, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_5': xǁAgentOrchestratorǁprocess_workflow__mutmut_5, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_6': xǁAgentOrchestratorǁprocess_workflow__mutmut_6, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_7': xǁAgentOrchestratorǁprocess_workflow__mutmut_7, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_8': xǁAgentOrchestratorǁprocess_workflow__mutmut_8, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_9': xǁAgentOrchestratorǁprocess_workflow__mutmut_9, 
        'xǁAgentOrchestratorǁprocess_workflow__mutmut_10': xǁAgentOrchestratorǁprocess_workflow__mutmut_10
    }
    
    def process_workflow(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentOrchestratorǁprocess_workflow__mutmut_orig"), object.__getattribute__(self, "xǁAgentOrchestratorǁprocess_workflow__mutmut_mutants"), args, kwargs, self)
        return result 
    
    process_workflow.__signature__ = _mutmut_signature(xǁAgentOrchestratorǁprocess_workflow__mutmut_orig)
    xǁAgentOrchestratorǁprocess_workflow__mutmut_orig.__name__ = 'xǁAgentOrchestratorǁprocess_workflow'
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_orig(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_1(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = None
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_2(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "XXis_runningXX": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_3(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "IS_RUNNING": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_4(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "XXtotal_agentsXX": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_5(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "TOTAL_AGENTS": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_6(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "XXrunning_agentsXX": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_7(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "RUNNING_AGENTS": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_8(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(None),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_9(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(2 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_10(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "XXstopped_agentsXX": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_11(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "STOPPED_AGENTS": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_12(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(None),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_13(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(2 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_14(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "XXagent_statesXX": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_15(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "AGENT_STATES": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "metrics": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_16(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "XXmetricsXX": self.factory.get_agent_metrics(),
        }
    
    def xǁAgentOrchestratorǁget_system_status__mutmut_17(self) -> Dict:
        """
        Get status of the entire agent system.
        
        Returns:
            Dictionary with system status
        """
        agents = self.factory.get_all_agents()
        
        return {
            "is_running": self._is_running,
            "total_agents": len(agents),
            "running_agents": sum(1 for a in agents if a.is_running()),
            "stopped_agents": sum(1 for a in agents if a.is_stopped()),
            "agent_states": {
                a.agent_type.value: a.state.value
                for a in agents
            },
            "METRICS": self.factory.get_agent_metrics(),
        }
    
    xǁAgentOrchestratorǁget_system_status__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentOrchestratorǁget_system_status__mutmut_1': xǁAgentOrchestratorǁget_system_status__mutmut_1, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_2': xǁAgentOrchestratorǁget_system_status__mutmut_2, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_3': xǁAgentOrchestratorǁget_system_status__mutmut_3, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_4': xǁAgentOrchestratorǁget_system_status__mutmut_4, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_5': xǁAgentOrchestratorǁget_system_status__mutmut_5, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_6': xǁAgentOrchestratorǁget_system_status__mutmut_6, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_7': xǁAgentOrchestratorǁget_system_status__mutmut_7, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_8': xǁAgentOrchestratorǁget_system_status__mutmut_8, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_9': xǁAgentOrchestratorǁget_system_status__mutmut_9, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_10': xǁAgentOrchestratorǁget_system_status__mutmut_10, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_11': xǁAgentOrchestratorǁget_system_status__mutmut_11, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_12': xǁAgentOrchestratorǁget_system_status__mutmut_12, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_13': xǁAgentOrchestratorǁget_system_status__mutmut_13, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_14': xǁAgentOrchestratorǁget_system_status__mutmut_14, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_15': xǁAgentOrchestratorǁget_system_status__mutmut_15, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_16': xǁAgentOrchestratorǁget_system_status__mutmut_16, 
        'xǁAgentOrchestratorǁget_system_status__mutmut_17': xǁAgentOrchestratorǁget_system_status__mutmut_17
    }
    
    def get_system_status(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentOrchestratorǁget_system_status__mutmut_orig"), object.__getattribute__(self, "xǁAgentOrchestratorǁget_system_status__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_system_status.__signature__ = _mutmut_signature(xǁAgentOrchestratorǁget_system_status__mutmut_orig)
    xǁAgentOrchestratorǁget_system_status__mutmut_orig.__name__ = 'xǁAgentOrchestratorǁget_system_status'


def x_create_agent_system__mutmut_orig(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_1(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = None
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_2(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=None,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_3(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=None,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_4(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=None,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_5(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=None,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_6(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=None,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_7(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_8(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_9(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_10(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_11(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_12(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = None
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_13(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(None)
    
    logger.info("Agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_14(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info(None)
    
    return orchestrator


def x_create_agent_system__mutmut_15(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("XXAgent system createdXX")
    
    return orchestrator


def x_create_agent_system__mutmut_16(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("agent system created")
    
    return orchestrator


def x_create_agent_system__mutmut_17(
    context_manager: ContextManager,
    router: MessageRouter,
    event_bus: EventBus,
    task_queue: TaskQueue,
    config: Config,
) -> AgentOrchestrator:
    """
    Create a complete agent system with all components.
    
    Args:
        context_manager: Shared context manager
        router: Message router
        event_bus: Event bus
        task_queue: Task queue
        config: System configuration
        
    Returns:
        Configured agent orchestrator
    """
    # Create factory
    factory = AgentFactory(
        context_manager=context_manager,
        router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        config=config,
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(factory)
    
    logger.info("AGENT SYSTEM CREATED")
    
    return orchestrator

x_create_agent_system__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_agent_system__mutmut_1': x_create_agent_system__mutmut_1, 
    'x_create_agent_system__mutmut_2': x_create_agent_system__mutmut_2, 
    'x_create_agent_system__mutmut_3': x_create_agent_system__mutmut_3, 
    'x_create_agent_system__mutmut_4': x_create_agent_system__mutmut_4, 
    'x_create_agent_system__mutmut_5': x_create_agent_system__mutmut_5, 
    'x_create_agent_system__mutmut_6': x_create_agent_system__mutmut_6, 
    'x_create_agent_system__mutmut_7': x_create_agent_system__mutmut_7, 
    'x_create_agent_system__mutmut_8': x_create_agent_system__mutmut_8, 
    'x_create_agent_system__mutmut_9': x_create_agent_system__mutmut_9, 
    'x_create_agent_system__mutmut_10': x_create_agent_system__mutmut_10, 
    'x_create_agent_system__mutmut_11': x_create_agent_system__mutmut_11, 
    'x_create_agent_system__mutmut_12': x_create_agent_system__mutmut_12, 
    'x_create_agent_system__mutmut_13': x_create_agent_system__mutmut_13, 
    'x_create_agent_system__mutmut_14': x_create_agent_system__mutmut_14, 
    'x_create_agent_system__mutmut_15': x_create_agent_system__mutmut_15, 
    'x_create_agent_system__mutmut_16': x_create_agent_system__mutmut_16, 
    'x_create_agent_system__mutmut_17': x_create_agent_system__mutmut_17
}

def create_agent_system(*args, **kwargs):
    result = _mutmut_trampoline(x_create_agent_system__mutmut_orig, x_create_agent_system__mutmut_mutants, args, kwargs)
    return result 

create_agent_system.__signature__ = _mutmut_signature(x_create_agent_system__mutmut_orig)
x_create_agent_system__mutmut_orig.__name__ = 'x_create_agent_system'
