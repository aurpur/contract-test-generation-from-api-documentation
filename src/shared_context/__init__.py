"""
Shared context management between agents.

This module provides the infrastructure for agents to share state,
communicate via messages, and persist data during the test generation workflow.

Author: Aurel IKAMA HONEY
"""
from .context_manager import ContextManager
from .models import (
    AgentMessage,
    AgentType,
    AuthType,
    CompletenessAnalysis,
    EndpointContext,
    GeneratedTest,
    HTTPMethod,
    InconsistencyReport,
    LLMPerformanceMetrics,
    Oracle,
    ProcessingStatus,
    QualityMetrics,
    TestExecutionResult,
    WorkflowSession,
)
from .storage import PostgreSQLRedisStorage, StorageBackend, create_storage_backend

__all__ = [
    # Context Manager
    "ContextManager",
    
    # Storage
    "StorageBackend",
    "PostgreSQLRedisStorage",
    "create_storage_backend",
    
    # Models
    "WorkflowSession",
    "EndpointContext",
    "Oracle",
    "GeneratedTest",
    "TestExecutionResult",
    "AgentMessage",
    "InconsistencyReport",
    "QualityMetrics",
    "LLMPerformanceMetrics",
    "CompletenessAnalysis",
    
    # Enums
    "AgentType",
    "ProcessingStatus",
    "HTTPMethod",
    "AuthType",
]
