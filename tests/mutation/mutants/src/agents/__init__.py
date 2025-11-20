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
from .oracle import OracleAgent
from .contractor import ContractorAgent
from .runner import RunnerAgent

__all__ = [
    "BaseAgent",
    "AgentConfig",
    "AgentState",
    "AgentFactory",
    "AgentOrchestrator",
    "create_agent_system",
    "InductorAgent",
    "OracleAgent",
    "ContractorAgent",
    "RunnerAgent",
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
