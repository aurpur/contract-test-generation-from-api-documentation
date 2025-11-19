"""
Multi-agent system for test generation.

This module provides the multi-agent system for automated contract test generation:
- BaseAgent: Abstract base class for all agents
- AgentConfig: Configuration for agents
- AgentState: Agent execution state
- AgentFactory: Factory for creating and managing agents
- AgentOrchestrator: High-level workflow coordination

Author: Aurel IKAMA HONEY
"""

from .base_agent import BaseAgent, AgentConfig, AgentState
from .factory import AgentFactory, AgentOrchestrator, create_agent_system
from .inductor import InductorAgent

__all__ = [
    "BaseAgent",
    "AgentConfig",
    "AgentState",
    "AgentFactory",
    "AgentOrchestrator",
    "create_agent_system",
    "InductorAgent",
]
