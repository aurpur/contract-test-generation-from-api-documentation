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


class AgentFactory:
    """
    Factory for creating and managing agents.
    
    Provides centralized creation and lifecycle management of all agents.
    """
    
    def __init__(
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
    
    def register_agent_class(
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
    
    def create_agent(
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
        
        # Build base parameters common to all agents
        import inspect
        base_params = {
            "config": agent_config,
            "context_manager": self.context_manager,
            "event_bus": self.event_bus,
            "task_queue": self.task_queue,
        }
        
        # Inspect agent class signature to determine parameter names
        sig = inspect.signature(agent_class.__init__)
        param_names = list(sig.parameters.keys())
        
        # Add router parameter (different agents use different names)
        if "router" in param_names:
            base_params["router"] = self.router
        elif "message_router" in param_names:
            base_params["message_router"] = self.router
        
        # Add LLM configuration if agent accepts it
        if "llm_config" in param_names and llm_config:
            base_params["llm_config"] = llm_config
        elif "llm_configs" in param_names and llm_config:
            # Oracle agent expects a list of configs for consensus
            base_params["llm_configs"] = [llm_config]
        
        # Add agent-specific parameters
        if agent_type == AgentType.RUNNER:
            # Runner agent needs project_dir
            if "project_dir" in param_names:
                base_params["project_dir"] = "./generated_tests"
        elif agent_type == AgentType.CONTRACTOR:
            # Contractor agent may need output_dir
            if "output_dir" in param_names:
                base_params["output_dir"] = "./generated_tests"
        
        # Create agent
        agent = agent_class(**base_params)
        
        # Store in registry
        self._agents[agent_type] = agent
        
        logger.info(
            f"Created agent",
            agent_type=agent_type.value,
            agent_class=agent_class.__name__,
        )
        
        return agent
    
    def get_agent(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """
        Get an existing agent instance.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(agent_type)
    
    def get_all_agents(self) -> List[BaseAgent]:
        """
        Get all active agents.
        
        Returns:
            List of all agent instances
        """
        return list(self._agents.values())
    
    async def start_agent(self, agent_type: AgentType) -> None:
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
    
    async def stop_agent(
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
    
    async def start_all_agents(self) -> None:
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
    
    async def stop_all_agents(self, timeout: float = 30.0) -> None:
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
    
    def _create_default_config(self, agent_type: AgentType) -> AgentConfig:
        """
        Create default configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Default agent configuration
        """
        # Get agent-specific settings from config
        agent_settings = self.config.agents.get(agent_type.value, None)
        
        return AgentConfig(
            agent_type=agent_type,
            max_concurrent_tasks=agent_settings.max_retries if agent_settings and hasattr(agent_settings, 'max_retries') else 5,
            task_timeout=agent_settings.timeout if agent_settings and hasattr(agent_settings, 'timeout') else 300.0,
            message_timeout=30.0,
            retry_limit=agent_settings.max_retries if agent_settings and hasattr(agent_settings, 'max_retries') else 3,
            enable_metrics=True,
            enable_tracing=True,
            custom_config={},
        )
    
    def _get_llm_config(self, agent_type: AgentType) -> Optional[Dict]:
        """
        Get LLM configuration for an agent type.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            LLM configuration dictionary or None
        """
        # Get LLM models from config
        if not self.config.llm_models:
            return None
        
        # Try to find the first available LLM config
        # Different agents may need different models in the future
        for model_config in self.config.llm_models.values():
            if hasattr(model_config, 'model_dump'):
                return model_config.model_dump()
            elif isinstance(model_config, dict):
                return model_config
        
        return None


class AgentOrchestrator:
    """
    Orchestrates the execution of all agents.
    
    Provides high-level coordination of the multi-agent workflow.
    """
    
    def __init__(self, factory: AgentFactory):
        """
        Initialize agent orchestrator.
        
        Args:
            factory: Agent factory
        """
        self.factory = factory
        self._is_running = False
        
        logger.info("Agent orchestrator initialized")
    
    async def initialize(self) -> None:
        """Initialize all agents."""
        logger.info("Initializing agent system")
        
        # This is where we would register all agent classes
        # For now, we'll just log that we're ready
        
        logger.info("Agent system initialized")
    
    async def start(self) -> None:
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
    
    async def stop(self, timeout: float = 30.0) -> None:
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
    
    async def process_workflow(self, session_id: UUID) -> None:
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
    
    def get_system_status(self) -> Dict:
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


def create_agent_system(
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
