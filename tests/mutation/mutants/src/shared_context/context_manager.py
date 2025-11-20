"""
Context Manager for shared state between agents.

This module manages the shared context that agents use to communicate
and store intermediate results during the test generation workflow.

Author: Aurel IKAMA HONEY
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from utils.logging import logger
from .models import (
    AgentMessage,
    AgentType,
    CompletenessAnalysis,
    EndpointContext,
    GeneratedTest,
    InconsistencyReport,
    LLMPerformanceMetrics,
    Oracle,
    ProcessingStatus,
    QualityMetrics,
    TestExecutionResult,
    WorkflowSession,
)
from .storage import StorageBackend
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


class ContextManager:
    """
    Manages the shared context between agents.
    
    Provides high-level operations for:
    - Creating and managing workflow sessions
    - Storing and retrieving agent outputs
    - Managing messages between agents
    - Tracking metrics and analytics
    """
    
    def xǁContextManagerǁ__init____mutmut_orig(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = storage
        logger.info("ContextManager initialized")
    
    def xǁContextManagerǁ__init____mutmut_1(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = None
        logger.info("ContextManager initialized")
    
    def xǁContextManagerǁ__init____mutmut_2(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = storage
        logger.info(None)
    
    def xǁContextManagerǁ__init____mutmut_3(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = storage
        logger.info("XXContextManager initializedXX")
    
    def xǁContextManagerǁ__init____mutmut_4(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = storage
        logger.info("contextmanager initialized")
    
    def xǁContextManagerǁ__init____mutmut_5(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = storage
        logger.info("CONTEXTMANAGER INITIALIZED")
    
    xǁContextManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁ__init____mutmut_1': xǁContextManagerǁ__init____mutmut_1, 
        'xǁContextManagerǁ__init____mutmut_2': xǁContextManagerǁ__init____mutmut_2, 
        'xǁContextManagerǁ__init____mutmut_3': xǁContextManagerǁ__init____mutmut_3, 
        'xǁContextManagerǁ__init____mutmut_4': xǁContextManagerǁ__init____mutmut_4, 
        'xǁContextManagerǁ__init____mutmut_5': xǁContextManagerǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁContextManagerǁ__init____mutmut_orig)
    xǁContextManagerǁ__init____mutmut_orig.__name__ = 'xǁContextManagerǁ__init__'
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_orig(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_1(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = None
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_2(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=None,
            collection_path=collection_path,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_3(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=None,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_4(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=None,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_5(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            config=None,
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_6(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_path=collection_path,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_7(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_8(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_9(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_10(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            config=config and {},
        )
        
        await self.storage.save_session(session)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_11(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(None)
        logger.info(f"Created session {session.id} for collection '{collection_name}'")
        
        return session
    
    # ==================== Session Management ====================
    
    async def xǁContextManagerǁcreate_session__mutmut_12(
        self,
        collection_name: str,
        collection_path: str,
        llm_models: Dict[AgentType, str],
        config: Optional[Dict[str, Any]] = None,
    ) -> WorkflowSession:
        """
        Create a new workflow session.
        
        Args:
            collection_name: Name of the Bruno collection
            collection_path: Path to the collection file
            llm_models: Mapping of agent types to LLM model names
            config: Additional configuration
            
        Returns:
            Created workflow session
        """
        session = WorkflowSession(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            config=config or {},
        )
        
        await self.storage.save_session(session)
        logger.info(None)
        
        return session
    
    xǁContextManagerǁcreate_session__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁcreate_session__mutmut_1': xǁContextManagerǁcreate_session__mutmut_1, 
        'xǁContextManagerǁcreate_session__mutmut_2': xǁContextManagerǁcreate_session__mutmut_2, 
        'xǁContextManagerǁcreate_session__mutmut_3': xǁContextManagerǁcreate_session__mutmut_3, 
        'xǁContextManagerǁcreate_session__mutmut_4': xǁContextManagerǁcreate_session__mutmut_4, 
        'xǁContextManagerǁcreate_session__mutmut_5': xǁContextManagerǁcreate_session__mutmut_5, 
        'xǁContextManagerǁcreate_session__mutmut_6': xǁContextManagerǁcreate_session__mutmut_6, 
        'xǁContextManagerǁcreate_session__mutmut_7': xǁContextManagerǁcreate_session__mutmut_7, 
        'xǁContextManagerǁcreate_session__mutmut_8': xǁContextManagerǁcreate_session__mutmut_8, 
        'xǁContextManagerǁcreate_session__mutmut_9': xǁContextManagerǁcreate_session__mutmut_9, 
        'xǁContextManagerǁcreate_session__mutmut_10': xǁContextManagerǁcreate_session__mutmut_10, 
        'xǁContextManagerǁcreate_session__mutmut_11': xǁContextManagerǁcreate_session__mutmut_11, 
        'xǁContextManagerǁcreate_session__mutmut_12': xǁContextManagerǁcreate_session__mutmut_12
    }
    
    def create_session(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁcreate_session__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁcreate_session__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_session.__signature__ = _mutmut_signature(xǁContextManagerǁcreate_session__mutmut_orig)
    xǁContextManagerǁcreate_session__mutmut_orig.__name__ = 'xǁContextManagerǁcreate_session'
    
    async def xǁContextManagerǁget_session__mutmut_orig(self, session_id: UUID) -> Optional[WorkflowSession]:
        """
        Retrieve a workflow session by ID.
        
        Args:
            session_id: Session UUID
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        session = await self.storage.get_session(session_id)
        
        if session:
            logger.debug(f"Retrieved session {session_id}")
        else:
            logger.warning(f"Session {session_id} not found")
        
        return session
    
    async def xǁContextManagerǁget_session__mutmut_1(self, session_id: UUID) -> Optional[WorkflowSession]:
        """
        Retrieve a workflow session by ID.
        
        Args:
            session_id: Session UUID
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        session = None
        
        if session:
            logger.debug(f"Retrieved session {session_id}")
        else:
            logger.warning(f"Session {session_id} not found")
        
        return session
    
    async def xǁContextManagerǁget_session__mutmut_2(self, session_id: UUID) -> Optional[WorkflowSession]:
        """
        Retrieve a workflow session by ID.
        
        Args:
            session_id: Session UUID
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        session = await self.storage.get_session(None)
        
        if session:
            logger.debug(f"Retrieved session {session_id}")
        else:
            logger.warning(f"Session {session_id} not found")
        
        return session
    
    async def xǁContextManagerǁget_session__mutmut_3(self, session_id: UUID) -> Optional[WorkflowSession]:
        """
        Retrieve a workflow session by ID.
        
        Args:
            session_id: Session UUID
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        session = await self.storage.get_session(session_id)
        
        if session:
            logger.debug(None)
        else:
            logger.warning(f"Session {session_id} not found")
        
        return session
    
    async def xǁContextManagerǁget_session__mutmut_4(self, session_id: UUID) -> Optional[WorkflowSession]:
        """
        Retrieve a workflow session by ID.
        
        Args:
            session_id: Session UUID
            
        Returns:
            WorkflowSession if found, None otherwise
        """
        session = await self.storage.get_session(session_id)
        
        if session:
            logger.debug(f"Retrieved session {session_id}")
        else:
            logger.warning(None)
        
        return session
    
    xǁContextManagerǁget_session__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_session__mutmut_1': xǁContextManagerǁget_session__mutmut_1, 
        'xǁContextManagerǁget_session__mutmut_2': xǁContextManagerǁget_session__mutmut_2, 
        'xǁContextManagerǁget_session__mutmut_3': xǁContextManagerǁget_session__mutmut_3, 
        'xǁContextManagerǁget_session__mutmut_4': xǁContextManagerǁget_session__mutmut_4
    }
    
    def get_session(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_session__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_session__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_session.__signature__ = _mutmut_signature(xǁContextManagerǁget_session__mutmut_orig)
    xǁContextManagerǁget_session__mutmut_orig.__name__ = 'xǁContextManagerǁget_session'
    
    async def xǁContextManagerǁupdate_session__mutmut_orig(self, session: WorkflowSession) -> None:
        """
        Update a workflow session.
        
        Args:
            session: Updated session object
        """
        session.updated_at = datetime.utcnow()
        await self.storage.save_session(session)
        logger.debug(f"Updated session {session.id}")
    
    async def xǁContextManagerǁupdate_session__mutmut_1(self, session: WorkflowSession) -> None:
        """
        Update a workflow session.
        
        Args:
            session: Updated session object
        """
        session.updated_at = None
        await self.storage.save_session(session)
        logger.debug(f"Updated session {session.id}")
    
    async def xǁContextManagerǁupdate_session__mutmut_2(self, session: WorkflowSession) -> None:
        """
        Update a workflow session.
        
        Args:
            session: Updated session object
        """
        session.updated_at = datetime.utcnow()
        await self.storage.save_session(None)
        logger.debug(f"Updated session {session.id}")
    
    async def xǁContextManagerǁupdate_session__mutmut_3(self, session: WorkflowSession) -> None:
        """
        Update a workflow session.
        
        Args:
            session: Updated session object
        """
        session.updated_at = datetime.utcnow()
        await self.storage.save_session(session)
        logger.debug(None)
    
    xǁContextManagerǁupdate_session__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁupdate_session__mutmut_1': xǁContextManagerǁupdate_session__mutmut_1, 
        'xǁContextManagerǁupdate_session__mutmut_2': xǁContextManagerǁupdate_session__mutmut_2, 
        'xǁContextManagerǁupdate_session__mutmut_3': xǁContextManagerǁupdate_session__mutmut_3
    }
    
    def update_session(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁupdate_session__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁupdate_session__mutmut_mutants"), args, kwargs, self)
        return result 
    
    update_session.__signature__ = _mutmut_signature(xǁContextManagerǁupdate_session__mutmut_orig)
    xǁContextManagerǁupdate_session__mutmut_orig.__name__ = 'xǁContextManagerǁupdate_session'
    
    async def xǁContextManagerǁupdate_session_status__mutmut_orig(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_1(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_2(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_3(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_4(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_5(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = None
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_6(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = None
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_7(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status != ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_8(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = None
        
        await self.update_session(session)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_9(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(None)
        logger.info(f"Session {session_id} status: {status.value}")
    
    async def xǁContextManagerǁupdate_session_status__mutmut_10(
        self,
        session_id: UUID,
        status: ProcessingStatus,
        current_agent: Optional[AgentType] = None,
    ) -> None:
        """
        Update the status of a session.
        
        Args:
            session_id: Session UUID
            status: New status
            current_agent: Current agent processing the session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = status
        if current_agent:
            session.current_agent = current_agent
        
        if status == ProcessingStatus.COMPLETED:
            session.completed_at = datetime.utcnow()
        
        await self.update_session(session)
        logger.info(None)
    
    xǁContextManagerǁupdate_session_status__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁupdate_session_status__mutmut_1': xǁContextManagerǁupdate_session_status__mutmut_1, 
        'xǁContextManagerǁupdate_session_status__mutmut_2': xǁContextManagerǁupdate_session_status__mutmut_2, 
        'xǁContextManagerǁupdate_session_status__mutmut_3': xǁContextManagerǁupdate_session_status__mutmut_3, 
        'xǁContextManagerǁupdate_session_status__mutmut_4': xǁContextManagerǁupdate_session_status__mutmut_4, 
        'xǁContextManagerǁupdate_session_status__mutmut_5': xǁContextManagerǁupdate_session_status__mutmut_5, 
        'xǁContextManagerǁupdate_session_status__mutmut_6': xǁContextManagerǁupdate_session_status__mutmut_6, 
        'xǁContextManagerǁupdate_session_status__mutmut_7': xǁContextManagerǁupdate_session_status__mutmut_7, 
        'xǁContextManagerǁupdate_session_status__mutmut_8': xǁContextManagerǁupdate_session_status__mutmut_8, 
        'xǁContextManagerǁupdate_session_status__mutmut_9': xǁContextManagerǁupdate_session_status__mutmut_9, 
        'xǁContextManagerǁupdate_session_status__mutmut_10': xǁContextManagerǁupdate_session_status__mutmut_10
    }
    
    def update_session_status(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁupdate_session_status__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁupdate_session_status__mutmut_mutants"), args, kwargs, self)
        return result 
    
    update_session_status.__signature__ = _mutmut_signature(xǁContextManagerǁupdate_session_status__mutmut_orig)
    xǁContextManagerǁupdate_session_status__mutmut_orig.__name__ = 'xǁContextManagerǁupdate_session_status'
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_orig(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_1(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_2(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_3(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_4(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_5(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(None)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_6(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = None
        
        await self.update_session(session)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_7(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(None)
        logger.debug(f"Added endpoint '{endpoint.name}' to session {session_id}")
    
    # ==================== Endpoint Management ====================
    
    async def xǁContextManagerǁadd_endpoint__mutmut_8(
        self,
        session_id: UUID,
        endpoint: EndpointContext,
    ) -> None:
        """
        Add an endpoint context to a session.
        
        Args:
            session_id: Session UUID
            endpoint: Endpoint context to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.endpoints.append(endpoint)
        session.total_endpoints = len(session.endpoints)
        
        await self.update_session(session)
        logger.debug(None)
    
    xǁContextManagerǁadd_endpoint__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_endpoint__mutmut_1': xǁContextManagerǁadd_endpoint__mutmut_1, 
        'xǁContextManagerǁadd_endpoint__mutmut_2': xǁContextManagerǁadd_endpoint__mutmut_2, 
        'xǁContextManagerǁadd_endpoint__mutmut_3': xǁContextManagerǁadd_endpoint__mutmut_3, 
        'xǁContextManagerǁadd_endpoint__mutmut_4': xǁContextManagerǁadd_endpoint__mutmut_4, 
        'xǁContextManagerǁadd_endpoint__mutmut_5': xǁContextManagerǁadd_endpoint__mutmut_5, 
        'xǁContextManagerǁadd_endpoint__mutmut_6': xǁContextManagerǁadd_endpoint__mutmut_6, 
        'xǁContextManagerǁadd_endpoint__mutmut_7': xǁContextManagerǁadd_endpoint__mutmut_7, 
        'xǁContextManagerǁadd_endpoint__mutmut_8': xǁContextManagerǁadd_endpoint__mutmut_8
    }
    
    def add_endpoint(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_endpoint__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_endpoint__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_endpoint.__signature__ = _mutmut_signature(xǁContextManagerǁadd_endpoint__mutmut_orig)
    xǁContextManagerǁadd_endpoint__mutmut_orig.__name__ = 'xǁContextManagerǁadd_endpoint'
    
    async def xǁContextManagerǁget_endpoints__mutmut_orig(
        self,
        session_id: UUID,
    ) -> List[EndpointContext]:
        """
        Get all endpoints for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of endpoint contexts
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.endpoints
    
    async def xǁContextManagerǁget_endpoints__mutmut_1(
        self,
        session_id: UUID,
    ) -> List[EndpointContext]:
        """
        Get all endpoints for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of endpoint contexts
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.endpoints
    
    async def xǁContextManagerǁget_endpoints__mutmut_2(
        self,
        session_id: UUID,
    ) -> List[EndpointContext]:
        """
        Get all endpoints for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of endpoint contexts
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.endpoints
    
    async def xǁContextManagerǁget_endpoints__mutmut_3(
        self,
        session_id: UUID,
    ) -> List[EndpointContext]:
        """
        Get all endpoints for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of endpoint contexts
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.endpoints
    
    async def xǁContextManagerǁget_endpoints__mutmut_4(
        self,
        session_id: UUID,
    ) -> List[EndpointContext]:
        """
        Get all endpoints for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of endpoint contexts
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        return session.endpoints
    
    xǁContextManagerǁget_endpoints__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_endpoints__mutmut_1': xǁContextManagerǁget_endpoints__mutmut_1, 
        'xǁContextManagerǁget_endpoints__mutmut_2': xǁContextManagerǁget_endpoints__mutmut_2, 
        'xǁContextManagerǁget_endpoints__mutmut_3': xǁContextManagerǁget_endpoints__mutmut_3, 
        'xǁContextManagerǁget_endpoints__mutmut_4': xǁContextManagerǁget_endpoints__mutmut_4
    }
    
    def get_endpoints(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_endpoints__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_endpoints__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_endpoints.__signature__ = _mutmut_signature(xǁContextManagerǁget_endpoints__mutmut_orig)
    xǁContextManagerǁget_endpoints__mutmut_orig.__name__ = 'xǁContextManagerǁget_endpoints'
    
    async def xǁContextManagerǁget_endpoint__mutmut_orig(
        self,
        session_id: UUID,
        endpoint_id: UUID,
    ) -> Optional[EndpointContext]:
        """
        Get a specific endpoint by ID.
        
        Args:
            session_id: Session UUID
            endpoint_id: Endpoint UUID
            
        Returns:
            EndpointContext if found, None otherwise
        """
        endpoints = await self.get_endpoints(session_id)
        
        for endpoint in endpoints:
            if endpoint.id == endpoint_id:
                return endpoint
        
        logger.warning(f"Endpoint {endpoint_id} not found in session {session_id}")
        return None
    
    async def xǁContextManagerǁget_endpoint__mutmut_1(
        self,
        session_id: UUID,
        endpoint_id: UUID,
    ) -> Optional[EndpointContext]:
        """
        Get a specific endpoint by ID.
        
        Args:
            session_id: Session UUID
            endpoint_id: Endpoint UUID
            
        Returns:
            EndpointContext if found, None otherwise
        """
        endpoints = None
        
        for endpoint in endpoints:
            if endpoint.id == endpoint_id:
                return endpoint
        
        logger.warning(f"Endpoint {endpoint_id} not found in session {session_id}")
        return None
    
    async def xǁContextManagerǁget_endpoint__mutmut_2(
        self,
        session_id: UUID,
        endpoint_id: UUID,
    ) -> Optional[EndpointContext]:
        """
        Get a specific endpoint by ID.
        
        Args:
            session_id: Session UUID
            endpoint_id: Endpoint UUID
            
        Returns:
            EndpointContext if found, None otherwise
        """
        endpoints = await self.get_endpoints(None)
        
        for endpoint in endpoints:
            if endpoint.id == endpoint_id:
                return endpoint
        
        logger.warning(f"Endpoint {endpoint_id} not found in session {session_id}")
        return None
    
    async def xǁContextManagerǁget_endpoint__mutmut_3(
        self,
        session_id: UUID,
        endpoint_id: UUID,
    ) -> Optional[EndpointContext]:
        """
        Get a specific endpoint by ID.
        
        Args:
            session_id: Session UUID
            endpoint_id: Endpoint UUID
            
        Returns:
            EndpointContext if found, None otherwise
        """
        endpoints = await self.get_endpoints(session_id)
        
        for endpoint in endpoints:
            if endpoint.id != endpoint_id:
                return endpoint
        
        logger.warning(f"Endpoint {endpoint_id} not found in session {session_id}")
        return None
    
    async def xǁContextManagerǁget_endpoint__mutmut_4(
        self,
        session_id: UUID,
        endpoint_id: UUID,
    ) -> Optional[EndpointContext]:
        """
        Get a specific endpoint by ID.
        
        Args:
            session_id: Session UUID
            endpoint_id: Endpoint UUID
            
        Returns:
            EndpointContext if found, None otherwise
        """
        endpoints = await self.get_endpoints(session_id)
        
        for endpoint in endpoints:
            if endpoint.id == endpoint_id:
                return endpoint
        
        logger.warning(None)
        return None
    
    xǁContextManagerǁget_endpoint__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_endpoint__mutmut_1': xǁContextManagerǁget_endpoint__mutmut_1, 
        'xǁContextManagerǁget_endpoint__mutmut_2': xǁContextManagerǁget_endpoint__mutmut_2, 
        'xǁContextManagerǁget_endpoint__mutmut_3': xǁContextManagerǁget_endpoint__mutmut_3, 
        'xǁContextManagerǁget_endpoint__mutmut_4': xǁContextManagerǁget_endpoint__mutmut_4
    }
    
    def get_endpoint(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_endpoint__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_endpoint__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_endpoint.__signature__ = _mutmut_signature(xǁContextManagerǁget_endpoint__mutmut_orig)
    xǁContextManagerǁget_endpoint__mutmut_orig.__name__ = 'xǁContextManagerǁget_endpoint'
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_orig(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(oracle)
        
        await self.update_session(session)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_1(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(oracle)
        
        await self.update_session(session)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_2(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(oracle)
        
        await self.update_session(session)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_3(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(oracle)
        
        await self.update_session(session)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_4(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        session.oracles.append(oracle)
        
        await self.update_session(session)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_5(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(None)
        
        await self.update_session(session)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_6(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(oracle)
        
        await self.update_session(None)
        logger.debug(f"Added oracle for endpoint {oracle.endpoint_id}")
    
    # ==================== Oracle Management ====================
    
    async def xǁContextManagerǁadd_oracle__mutmut_7(
        self,
        session_id: UUID,
        oracle: Oracle,
    ) -> None:
        """
        Add an oracle to a session.
        
        Args:
            session_id: Session UUID
            oracle: Oracle to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.oracles.append(oracle)
        
        await self.update_session(session)
        logger.debug(None)
    
    xǁContextManagerǁadd_oracle__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_oracle__mutmut_1': xǁContextManagerǁadd_oracle__mutmut_1, 
        'xǁContextManagerǁadd_oracle__mutmut_2': xǁContextManagerǁadd_oracle__mutmut_2, 
        'xǁContextManagerǁadd_oracle__mutmut_3': xǁContextManagerǁadd_oracle__mutmut_3, 
        'xǁContextManagerǁadd_oracle__mutmut_4': xǁContextManagerǁadd_oracle__mutmut_4, 
        'xǁContextManagerǁadd_oracle__mutmut_5': xǁContextManagerǁadd_oracle__mutmut_5, 
        'xǁContextManagerǁadd_oracle__mutmut_6': xǁContextManagerǁadd_oracle__mutmut_6, 
        'xǁContextManagerǁadd_oracle__mutmut_7': xǁContextManagerǁadd_oracle__mutmut_7
    }
    
    def add_oracle(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_oracle__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_oracle__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_oracle.__signature__ = _mutmut_signature(xǁContextManagerǁadd_oracle__mutmut_orig)
    xǁContextManagerǁadd_oracle__mutmut_orig.__name__ = 'xǁContextManagerǁadd_oracle'
    
    async def xǁContextManagerǁget_oracles__mutmut_orig(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id == endpoint_id]
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_1(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id == endpoint_id]
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_2(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id == endpoint_id]
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_3(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id == endpoint_id]
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_4(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id == endpoint_id]
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_5(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = None
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id == endpoint_id]
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_6(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = None
        
        return oracles
    
    async def xǁContextManagerǁget_oracles__mutmut_7(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[Oracle]:
        """
        Get oracles for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of oracles
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        oracles = session.oracles
        
        if endpoint_id:
            oracles = [o for o in oracles if o.endpoint_id != endpoint_id]
        
        return oracles
    
    xǁContextManagerǁget_oracles__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_oracles__mutmut_1': xǁContextManagerǁget_oracles__mutmut_1, 
        'xǁContextManagerǁget_oracles__mutmut_2': xǁContextManagerǁget_oracles__mutmut_2, 
        'xǁContextManagerǁget_oracles__mutmut_3': xǁContextManagerǁget_oracles__mutmut_3, 
        'xǁContextManagerǁget_oracles__mutmut_4': xǁContextManagerǁget_oracles__mutmut_4, 
        'xǁContextManagerǁget_oracles__mutmut_5': xǁContextManagerǁget_oracles__mutmut_5, 
        'xǁContextManagerǁget_oracles__mutmut_6': xǁContextManagerǁget_oracles__mutmut_6, 
        'xǁContextManagerǁget_oracles__mutmut_7': xǁContextManagerǁget_oracles__mutmut_7
    }
    
    def get_oracles(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_oracles__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_oracles__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_oracles.__signature__ = _mutmut_signature(xǁContextManagerǁget_oracles__mutmut_orig)
    xǁContextManagerǁget_oracles__mutmut_orig.__name__ = 'xǁContextManagerǁget_oracles'
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_orig(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(test)
        
        await self.update_session(session)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_1(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(test)
        
        await self.update_session(session)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_2(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(test)
        
        await self.update_session(session)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_3(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(test)
        
        await self.update_session(session)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_4(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        session.tests.append(test)
        
        await self.update_session(session)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_5(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(None)
        
        await self.update_session(session)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_6(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(test)
        
        await self.update_session(None)
        logger.debug(f"Added test '{test.test_method_name}' to session {session_id}")
    
    # ==================== Test Management ====================
    
    async def xǁContextManagerǁadd_test__mutmut_7(
        self,
        session_id: UUID,
        test: GeneratedTest,
    ) -> None:
        """
        Add a generated test to a session.
        
        Args:
            session_id: Session UUID
            test: Generated test to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.tests.append(test)
        
        await self.update_session(session)
        logger.debug(None)
    
    xǁContextManagerǁadd_test__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_test__mutmut_1': xǁContextManagerǁadd_test__mutmut_1, 
        'xǁContextManagerǁadd_test__mutmut_2': xǁContextManagerǁadd_test__mutmut_2, 
        'xǁContextManagerǁadd_test__mutmut_3': xǁContextManagerǁadd_test__mutmut_3, 
        'xǁContextManagerǁadd_test__mutmut_4': xǁContextManagerǁadd_test__mutmut_4, 
        'xǁContextManagerǁadd_test__mutmut_5': xǁContextManagerǁadd_test__mutmut_5, 
        'xǁContextManagerǁadd_test__mutmut_6': xǁContextManagerǁadd_test__mutmut_6, 
        'xǁContextManagerǁadd_test__mutmut_7': xǁContextManagerǁadd_test__mutmut_7
    }
    
    def add_test(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_test__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_test__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_test.__signature__ = _mutmut_signature(xǁContextManagerǁadd_test__mutmut_orig)
    xǁContextManagerǁadd_test__mutmut_orig.__name__ = 'xǁContextManagerǁadd_test'
    
    async def xǁContextManagerǁget_tests__mutmut_orig(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = session.tests
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id == endpoint_id]
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_1(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = session.tests
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id == endpoint_id]
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_2(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = session.tests
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id == endpoint_id]
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_3(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = session.tests
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id == endpoint_id]
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_4(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        tests = session.tests
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id == endpoint_id]
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_5(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = None
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id == endpoint_id]
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_6(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = session.tests
        
        if endpoint_id:
            tests = None
        
        return tests
    
    async def xǁContextManagerǁget_tests__mutmut_7(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Get tests for a session, optionally filtered by endpoint.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        tests = session.tests
        
        if endpoint_id:
            tests = [t for t in tests if t.endpoint_id != endpoint_id]
        
        return tests
    
    xǁContextManagerǁget_tests__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_tests__mutmut_1': xǁContextManagerǁget_tests__mutmut_1, 
        'xǁContextManagerǁget_tests__mutmut_2': xǁContextManagerǁget_tests__mutmut_2, 
        'xǁContextManagerǁget_tests__mutmut_3': xǁContextManagerǁget_tests__mutmut_3, 
        'xǁContextManagerǁget_tests__mutmut_4': xǁContextManagerǁget_tests__mutmut_4, 
        'xǁContextManagerǁget_tests__mutmut_5': xǁContextManagerǁget_tests__mutmut_5, 
        'xǁContextManagerǁget_tests__mutmut_6': xǁContextManagerǁget_tests__mutmut_6, 
        'xǁContextManagerǁget_tests__mutmut_7': xǁContextManagerǁget_tests__mutmut_7
    }
    
    def get_tests(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_tests__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_tests__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_tests.__signature__ = _mutmut_signature(xǁContextManagerǁget_tests__mutmut_orig)
    xǁContextManagerǁget_tests__mutmut_orig.__name__ = 'xǁContextManagerǁget_tests'
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_orig(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_1(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_2(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_3(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_4(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_5(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(None)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_6(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests = 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_7(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests -= 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_8(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 2
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_9(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests = 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_10(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests -= 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_11(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 2
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_12(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = None
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_13(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(None)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_14(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            None
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_15(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'XXpassedXX' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_16(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'PASSED' if result.passed else 'failed'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_17(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'XXfailedXX'})"
        )
    
    # ==================== Execution Results ====================
    
    async def xǁContextManagerǁadd_execution_result__mutmut_18(
        self,
        session_id: UUID,
        result: TestExecutionResult,
    ) -> None:
        """
        Add a test execution result to a session.
        
        Args:
            session_id: Session UUID
            result: Execution result to add
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.execution_results.append(result)
        
        # Update counters
        if result.passed:
            session.successful_tests += 1
        else:
            session.failed_tests += 1
        
        session.processed_endpoints = len(session.execution_results)
        
        await self.update_session(session)
        logger.debug(
            f"Added execution result for test {result.test_id} "
            f"({'passed' if result.passed else 'FAILED'})"
        )
    
    xǁContextManagerǁadd_execution_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_execution_result__mutmut_1': xǁContextManagerǁadd_execution_result__mutmut_1, 
        'xǁContextManagerǁadd_execution_result__mutmut_2': xǁContextManagerǁadd_execution_result__mutmut_2, 
        'xǁContextManagerǁadd_execution_result__mutmut_3': xǁContextManagerǁadd_execution_result__mutmut_3, 
        'xǁContextManagerǁadd_execution_result__mutmut_4': xǁContextManagerǁadd_execution_result__mutmut_4, 
        'xǁContextManagerǁadd_execution_result__mutmut_5': xǁContextManagerǁadd_execution_result__mutmut_5, 
        'xǁContextManagerǁadd_execution_result__mutmut_6': xǁContextManagerǁadd_execution_result__mutmut_6, 
        'xǁContextManagerǁadd_execution_result__mutmut_7': xǁContextManagerǁadd_execution_result__mutmut_7, 
        'xǁContextManagerǁadd_execution_result__mutmut_8': xǁContextManagerǁadd_execution_result__mutmut_8, 
        'xǁContextManagerǁadd_execution_result__mutmut_9': xǁContextManagerǁadd_execution_result__mutmut_9, 
        'xǁContextManagerǁadd_execution_result__mutmut_10': xǁContextManagerǁadd_execution_result__mutmut_10, 
        'xǁContextManagerǁadd_execution_result__mutmut_11': xǁContextManagerǁadd_execution_result__mutmut_11, 
        'xǁContextManagerǁadd_execution_result__mutmut_12': xǁContextManagerǁadd_execution_result__mutmut_12, 
        'xǁContextManagerǁadd_execution_result__mutmut_13': xǁContextManagerǁadd_execution_result__mutmut_13, 
        'xǁContextManagerǁadd_execution_result__mutmut_14': xǁContextManagerǁadd_execution_result__mutmut_14, 
        'xǁContextManagerǁadd_execution_result__mutmut_15': xǁContextManagerǁadd_execution_result__mutmut_15, 
        'xǁContextManagerǁadd_execution_result__mutmut_16': xǁContextManagerǁadd_execution_result__mutmut_16, 
        'xǁContextManagerǁadd_execution_result__mutmut_17': xǁContextManagerǁadd_execution_result__mutmut_17, 
        'xǁContextManagerǁadd_execution_result__mutmut_18': xǁContextManagerǁadd_execution_result__mutmut_18
    }
    
    def add_execution_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_execution_result__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_execution_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_execution_result.__signature__ = _mutmut_signature(xǁContextManagerǁadd_execution_result__mutmut_orig)
    xǁContextManagerǁadd_execution_result__mutmut_orig.__name__ = 'xǁContextManagerǁadd_execution_result'
    
    async def xǁContextManagerǁget_execution_results__mutmut_orig(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        results = session.execution_results
        
        if test_id:
            results = [r for r in results if r.test_id == test_id]
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_1(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        results = session.execution_results
        
        if test_id:
            results = [r for r in results if r.test_id == test_id]
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_2(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        results = session.execution_results
        
        if test_id:
            results = [r for r in results if r.test_id == test_id]
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_3(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        results = session.execution_results
        
        if test_id:
            results = [r for r in results if r.test_id == test_id]
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_4(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        results = session.execution_results
        
        if test_id:
            results = [r for r in results if r.test_id == test_id]
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_5(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        results = None
        
        if test_id:
            results = [r for r in results if r.test_id == test_id]
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_6(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        results = session.execution_results
        
        if test_id:
            results = None
        
        return results
    
    async def xǁContextManagerǁget_execution_results__mutmut_7(
        self,
        session_id: UUID,
        test_id: Optional[UUID] = None,
    ) -> List[TestExecutionResult]:
        """
        Get execution results for a session, optionally filtered by test.
        
        Args:
            session_id: Session UUID
            test_id: Optional test UUID to filter by
            
        Returns:
            List of execution results
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        results = session.execution_results
        
        if test_id:
            results = [r for r in results if r.test_id != test_id]
        
        return results
    
    xǁContextManagerǁget_execution_results__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_execution_results__mutmut_1': xǁContextManagerǁget_execution_results__mutmut_1, 
        'xǁContextManagerǁget_execution_results__mutmut_2': xǁContextManagerǁget_execution_results__mutmut_2, 
        'xǁContextManagerǁget_execution_results__mutmut_3': xǁContextManagerǁget_execution_results__mutmut_3, 
        'xǁContextManagerǁget_execution_results__mutmut_4': xǁContextManagerǁget_execution_results__mutmut_4, 
        'xǁContextManagerǁget_execution_results__mutmut_5': xǁContextManagerǁget_execution_results__mutmut_5, 
        'xǁContextManagerǁget_execution_results__mutmut_6': xǁContextManagerǁget_execution_results__mutmut_6, 
        'xǁContextManagerǁget_execution_results__mutmut_7': xǁContextManagerǁget_execution_results__mutmut_7
    }
    
    def get_execution_results(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_execution_results__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_execution_results__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_execution_results.__signature__ = _mutmut_signature(xǁContextManagerǁget_execution_results__mutmut_orig)
    xǁContextManagerǁget_execution_results__mutmut_orig.__name__ = 'xǁContextManagerǁget_execution_results'
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_orig(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_1(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 1,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_2(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = None
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_3(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=None,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_4(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=None,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_5(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=None,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_6(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=None,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_7(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=None,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_8(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=None,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_9(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=None,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_10(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_11(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_12(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_13(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_14(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_15(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_16(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            )
        
        await self.storage.save_message(message)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_17(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(None)
        logger.debug(
            f"Message {message.id}: {from_agent.value} → {to_agent.value} "
            f"[{message_type}]"
        )
        
        return message
    
    # ==================== Message Passing ====================
    
    async def xǁContextManagerǁsend_message__mutmut_18(
        self,
        session_id: UUID,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        parent_message_id: Optional[UUID] = None,
        priority: int = 0,
    ) -> AgentMessage:
        """
        Send a message between agents.
        
        Args:
            session_id: Session UUID
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            parent_message_id: Optional parent message ID
            priority: Message priority (higher = more urgent)
            
        Returns:
            Created message
        """
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            session_id=session_id,
            parent_message_id=parent_message_id,
            priority=priority,
        )
        
        await self.storage.save_message(message)
        logger.debug(
            None
        )
        
        return message
    
    xǁContextManagerǁsend_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁsend_message__mutmut_1': xǁContextManagerǁsend_message__mutmut_1, 
        'xǁContextManagerǁsend_message__mutmut_2': xǁContextManagerǁsend_message__mutmut_2, 
        'xǁContextManagerǁsend_message__mutmut_3': xǁContextManagerǁsend_message__mutmut_3, 
        'xǁContextManagerǁsend_message__mutmut_4': xǁContextManagerǁsend_message__mutmut_4, 
        'xǁContextManagerǁsend_message__mutmut_5': xǁContextManagerǁsend_message__mutmut_5, 
        'xǁContextManagerǁsend_message__mutmut_6': xǁContextManagerǁsend_message__mutmut_6, 
        'xǁContextManagerǁsend_message__mutmut_7': xǁContextManagerǁsend_message__mutmut_7, 
        'xǁContextManagerǁsend_message__mutmut_8': xǁContextManagerǁsend_message__mutmut_8, 
        'xǁContextManagerǁsend_message__mutmut_9': xǁContextManagerǁsend_message__mutmut_9, 
        'xǁContextManagerǁsend_message__mutmut_10': xǁContextManagerǁsend_message__mutmut_10, 
        'xǁContextManagerǁsend_message__mutmut_11': xǁContextManagerǁsend_message__mutmut_11, 
        'xǁContextManagerǁsend_message__mutmut_12': xǁContextManagerǁsend_message__mutmut_12, 
        'xǁContextManagerǁsend_message__mutmut_13': xǁContextManagerǁsend_message__mutmut_13, 
        'xǁContextManagerǁsend_message__mutmut_14': xǁContextManagerǁsend_message__mutmut_14, 
        'xǁContextManagerǁsend_message__mutmut_15': xǁContextManagerǁsend_message__mutmut_15, 
        'xǁContextManagerǁsend_message__mutmut_16': xǁContextManagerǁsend_message__mutmut_16, 
        'xǁContextManagerǁsend_message__mutmut_17': xǁContextManagerǁsend_message__mutmut_17, 
        'xǁContextManagerǁsend_message__mutmut_18': xǁContextManagerǁsend_message__mutmut_18
    }
    
    def send_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁsend_message__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁsend_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    send_message.__signature__ = _mutmut_signature(xǁContextManagerǁsend_message__mutmut_orig)
    xǁContextManagerǁsend_message__mutmut_orig.__name__ = 'xǁContextManagerǁsend_message'
    
    async def xǁContextManagerǁget_messages__mutmut_orig(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            session_id=session_id,
            to_agent=to_agent,
            from_agent=from_agent,
        )
    
    async def xǁContextManagerǁget_messages__mutmut_1(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            session_id=None,
            to_agent=to_agent,
            from_agent=from_agent,
        )
    
    async def xǁContextManagerǁget_messages__mutmut_2(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            session_id=session_id,
            to_agent=None,
            from_agent=from_agent,
        )
    
    async def xǁContextManagerǁget_messages__mutmut_3(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            session_id=session_id,
            to_agent=to_agent,
            from_agent=None,
        )
    
    async def xǁContextManagerǁget_messages__mutmut_4(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            to_agent=to_agent,
            from_agent=from_agent,
        )
    
    async def xǁContextManagerǁget_messages__mutmut_5(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            session_id=session_id,
            from_agent=from_agent,
        )
    
    async def xǁContextManagerǁget_messages__mutmut_6(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """
        Get messages for a session, optionally filtered.
        
        Args:
            session_id: Session UUID
            to_agent: Optional filter by receiver
            from_agent: Optional filter by sender
            
        Returns:
            List of messages
        """
        return await self.storage.get_messages(
            session_id=session_id,
            to_agent=to_agent,
            )
    
    xǁContextManagerǁget_messages__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_messages__mutmut_1': xǁContextManagerǁget_messages__mutmut_1, 
        'xǁContextManagerǁget_messages__mutmut_2': xǁContextManagerǁget_messages__mutmut_2, 
        'xǁContextManagerǁget_messages__mutmut_3': xǁContextManagerǁget_messages__mutmut_3, 
        'xǁContextManagerǁget_messages__mutmut_4': xǁContextManagerǁget_messages__mutmut_4, 
        'xǁContextManagerǁget_messages__mutmut_5': xǁContextManagerǁget_messages__mutmut_5, 
        'xǁContextManagerǁget_messages__mutmut_6': xǁContextManagerǁget_messages__mutmut_6
    }
    
    def get_messages(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_messages__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_messages__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_messages.__signature__ = _mutmut_signature(xǁContextManagerǁget_messages__mutmut_orig)
    xǁContextManagerǁget_messages__mutmut_orig.__name__ = 'xǁContextManagerǁget_messages'
    
    # ==================== Metrics & Analytics ====================
    
    async def xǁContextManagerǁadd_inconsistency_report__mutmut_orig(
        self,
        report: InconsistencyReport,
    ) -> None:
        """
        Add an inconsistency report (RQ2).
        
        Args:
            report: Inconsistency report to add
        """
        await self.storage.save_inconsistency_report(report)
        logger.info(
            f"Inconsistency detected: {report.inconsistency_type} "
            f"(severity: {report.severity})"
        )
    
    # ==================== Metrics & Analytics ====================
    
    async def xǁContextManagerǁadd_inconsistency_report__mutmut_1(
        self,
        report: InconsistencyReport,
    ) -> None:
        """
        Add an inconsistency report (RQ2).
        
        Args:
            report: Inconsistency report to add
        """
        await self.storage.save_inconsistency_report(None)
        logger.info(
            f"Inconsistency detected: {report.inconsistency_type} "
            f"(severity: {report.severity})"
        )
    
    # ==================== Metrics & Analytics ====================
    
    async def xǁContextManagerǁadd_inconsistency_report__mutmut_2(
        self,
        report: InconsistencyReport,
    ) -> None:
        """
        Add an inconsistency report (RQ2).
        
        Args:
            report: Inconsistency report to add
        """
        await self.storage.save_inconsistency_report(report)
        logger.info(
            None
        )
    
    xǁContextManagerǁadd_inconsistency_report__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_inconsistency_report__mutmut_1': xǁContextManagerǁadd_inconsistency_report__mutmut_1, 
        'xǁContextManagerǁadd_inconsistency_report__mutmut_2': xǁContextManagerǁadd_inconsistency_report__mutmut_2
    }
    
    def add_inconsistency_report(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_inconsistency_report__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_inconsistency_report__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_inconsistency_report.__signature__ = _mutmut_signature(xǁContextManagerǁadd_inconsistency_report__mutmut_orig)
    xǁContextManagerǁadd_inconsistency_report__mutmut_orig.__name__ = 'xǁContextManagerǁadd_inconsistency_report'
    
    async def xǁContextManagerǁget_inconsistency_reports__mutmut_orig(
        self,
        session_id: UUID,
    ) -> List[InconsistencyReport]:
        """
        Get inconsistency reports for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of inconsistency reports
        """
        return await self.storage.get_inconsistency_reports(session_id)
    
    async def xǁContextManagerǁget_inconsistency_reports__mutmut_1(
        self,
        session_id: UUID,
    ) -> List[InconsistencyReport]:
        """
        Get inconsistency reports for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of inconsistency reports
        """
        return await self.storage.get_inconsistency_reports(None)
    
    xǁContextManagerǁget_inconsistency_reports__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_inconsistency_reports__mutmut_1': xǁContextManagerǁget_inconsistency_reports__mutmut_1
    }
    
    def get_inconsistency_reports(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_inconsistency_reports__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_inconsistency_reports__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_inconsistency_reports.__signature__ = _mutmut_signature(xǁContextManagerǁget_inconsistency_reports__mutmut_orig)
    xǁContextManagerǁget_inconsistency_reports__mutmut_orig.__name__ = 'xǁContextManagerǁget_inconsistency_reports'
    
    async def xǁContextManagerǁadd_quality_metrics__mutmut_orig(
        self,
        metrics: QualityMetrics,
    ) -> None:
        """
        Add quality metrics (RQ3).
        
        Args:
            metrics: Quality metrics to add
        """
        await self.storage.save_quality_metrics(metrics)
        logger.debug(f"Quality metrics: score={metrics.quality_score:.2f}")
    
    async def xǁContextManagerǁadd_quality_metrics__mutmut_1(
        self,
        metrics: QualityMetrics,
    ) -> None:
        """
        Add quality metrics (RQ3).
        
        Args:
            metrics: Quality metrics to add
        """
        await self.storage.save_quality_metrics(None)
        logger.debug(f"Quality metrics: score={metrics.quality_score:.2f}")
    
    async def xǁContextManagerǁadd_quality_metrics__mutmut_2(
        self,
        metrics: QualityMetrics,
    ) -> None:
        """
        Add quality metrics (RQ3).
        
        Args:
            metrics: Quality metrics to add
        """
        await self.storage.save_quality_metrics(metrics)
        logger.debug(None)
    
    xǁContextManagerǁadd_quality_metrics__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_quality_metrics__mutmut_1': xǁContextManagerǁadd_quality_metrics__mutmut_1, 
        'xǁContextManagerǁadd_quality_metrics__mutmut_2': xǁContextManagerǁadd_quality_metrics__mutmut_2
    }
    
    def add_quality_metrics(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_quality_metrics__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_quality_metrics__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_quality_metrics.__signature__ = _mutmut_signature(xǁContextManagerǁadd_quality_metrics__mutmut_orig)
    xǁContextManagerǁadd_quality_metrics__mutmut_orig.__name__ = 'xǁContextManagerǁadd_quality_metrics'
    
    async def xǁContextManagerǁget_quality_metrics__mutmut_orig(
        self,
        session_id: UUID,
    ) -> List[QualityMetrics]:
        """
        Get quality metrics for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of quality metrics
        """
        return await self.storage.get_quality_metrics(session_id)
    
    async def xǁContextManagerǁget_quality_metrics__mutmut_1(
        self,
        session_id: UUID,
    ) -> List[QualityMetrics]:
        """
        Get quality metrics for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of quality metrics
        """
        return await self.storage.get_quality_metrics(None)
    
    xǁContextManagerǁget_quality_metrics__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_quality_metrics__mutmut_1': xǁContextManagerǁget_quality_metrics__mutmut_1
    }
    
    def get_quality_metrics(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_quality_metrics__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_quality_metrics__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_quality_metrics.__signature__ = _mutmut_signature(xǁContextManagerǁget_quality_metrics__mutmut_orig)
    xǁContextManagerǁget_quality_metrics__mutmut_orig.__name__ = 'xǁContextManagerǁget_quality_metrics'
    
    async def xǁContextManagerǁadd_llm_performance_metrics__mutmut_orig(
        self,
        metrics: LLMPerformanceMetrics,
    ) -> None:
        """
        Add LLM performance metrics (RQ4).
        
        Args:
            metrics: LLM performance metrics to add
        """
        await self.storage.save_llm_performance_metrics(metrics)
        logger.debug(
            f"LLM metrics: {metrics.model_name} "
            f"({metrics.agent_type.value}) - "
            f"{metrics.successful_requests}/{metrics.total_requests} successful"
        )
    
    async def xǁContextManagerǁadd_llm_performance_metrics__mutmut_1(
        self,
        metrics: LLMPerformanceMetrics,
    ) -> None:
        """
        Add LLM performance metrics (RQ4).
        
        Args:
            metrics: LLM performance metrics to add
        """
        await self.storage.save_llm_performance_metrics(None)
        logger.debug(
            f"LLM metrics: {metrics.model_name} "
            f"({metrics.agent_type.value}) - "
            f"{metrics.successful_requests}/{metrics.total_requests} successful"
        )
    
    async def xǁContextManagerǁadd_llm_performance_metrics__mutmut_2(
        self,
        metrics: LLMPerformanceMetrics,
    ) -> None:
        """
        Add LLM performance metrics (RQ4).
        
        Args:
            metrics: LLM performance metrics to add
        """
        await self.storage.save_llm_performance_metrics(metrics)
        logger.debug(
            None
        )
    
    xǁContextManagerǁadd_llm_performance_metrics__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_llm_performance_metrics__mutmut_1': xǁContextManagerǁadd_llm_performance_metrics__mutmut_1, 
        'xǁContextManagerǁadd_llm_performance_metrics__mutmut_2': xǁContextManagerǁadd_llm_performance_metrics__mutmut_2
    }
    
    def add_llm_performance_metrics(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_llm_performance_metrics__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_llm_performance_metrics__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_llm_performance_metrics.__signature__ = _mutmut_signature(xǁContextManagerǁadd_llm_performance_metrics__mutmut_orig)
    xǁContextManagerǁadd_llm_performance_metrics__mutmut_orig.__name__ = 'xǁContextManagerǁadd_llm_performance_metrics'
    
    async def xǁContextManagerǁget_llm_performance_metrics__mutmut_orig(
        self,
        session_id: UUID,
        agent_type: Optional[AgentType] = None,
    ) -> List[LLMPerformanceMetrics]:
        """
        Get LLM performance metrics for a session.
        
        Args:
            session_id: Session UUID
            agent_type: Optional filter by agent type
            
        Returns:
            List of LLM performance metrics
        """
        return await self.storage.get_llm_performance_metrics(
            session_id=session_id,
            agent_type=agent_type,
        )
    
    async def xǁContextManagerǁget_llm_performance_metrics__mutmut_1(
        self,
        session_id: UUID,
        agent_type: Optional[AgentType] = None,
    ) -> List[LLMPerformanceMetrics]:
        """
        Get LLM performance metrics for a session.
        
        Args:
            session_id: Session UUID
            agent_type: Optional filter by agent type
            
        Returns:
            List of LLM performance metrics
        """
        return await self.storage.get_llm_performance_metrics(
            session_id=None,
            agent_type=agent_type,
        )
    
    async def xǁContextManagerǁget_llm_performance_metrics__mutmut_2(
        self,
        session_id: UUID,
        agent_type: Optional[AgentType] = None,
    ) -> List[LLMPerformanceMetrics]:
        """
        Get LLM performance metrics for a session.
        
        Args:
            session_id: Session UUID
            agent_type: Optional filter by agent type
            
        Returns:
            List of LLM performance metrics
        """
        return await self.storage.get_llm_performance_metrics(
            session_id=session_id,
            agent_type=None,
        )
    
    async def xǁContextManagerǁget_llm_performance_metrics__mutmut_3(
        self,
        session_id: UUID,
        agent_type: Optional[AgentType] = None,
    ) -> List[LLMPerformanceMetrics]:
        """
        Get LLM performance metrics for a session.
        
        Args:
            session_id: Session UUID
            agent_type: Optional filter by agent type
            
        Returns:
            List of LLM performance metrics
        """
        return await self.storage.get_llm_performance_metrics(
            agent_type=agent_type,
        )
    
    async def xǁContextManagerǁget_llm_performance_metrics__mutmut_4(
        self,
        session_id: UUID,
        agent_type: Optional[AgentType] = None,
    ) -> List[LLMPerformanceMetrics]:
        """
        Get LLM performance metrics for a session.
        
        Args:
            session_id: Session UUID
            agent_type: Optional filter by agent type
            
        Returns:
            List of LLM performance metrics
        """
        return await self.storage.get_llm_performance_metrics(
            session_id=session_id,
            )
    
    xǁContextManagerǁget_llm_performance_metrics__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_llm_performance_metrics__mutmut_1': xǁContextManagerǁget_llm_performance_metrics__mutmut_1, 
        'xǁContextManagerǁget_llm_performance_metrics__mutmut_2': xǁContextManagerǁget_llm_performance_metrics__mutmut_2, 
        'xǁContextManagerǁget_llm_performance_metrics__mutmut_3': xǁContextManagerǁget_llm_performance_metrics__mutmut_3, 
        'xǁContextManagerǁget_llm_performance_metrics__mutmut_4': xǁContextManagerǁget_llm_performance_metrics__mutmut_4
    }
    
    def get_llm_performance_metrics(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_llm_performance_metrics__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_llm_performance_metrics__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_llm_performance_metrics.__signature__ = _mutmut_signature(xǁContextManagerǁget_llm_performance_metrics__mutmut_orig)
    xǁContextManagerǁget_llm_performance_metrics__mutmut_orig.__name__ = 'xǁContextManagerǁget_llm_performance_metrics'
    
    async def xǁContextManagerǁadd_completeness_analysis__mutmut_orig(
        self,
        analysis: CompletenessAnalysis,
    ) -> None:
        """
        Add completeness analysis (RQ5).
        
        Args:
            analysis: Completeness analysis to add
        """
        await self.storage.save_completeness_analysis(analysis)
        logger.info(
            f"Completeness analysis: "
            f"{analysis.documentation_completeness:.1%} complete"
        )
    
    async def xǁContextManagerǁadd_completeness_analysis__mutmut_1(
        self,
        analysis: CompletenessAnalysis,
    ) -> None:
        """
        Add completeness analysis (RQ5).
        
        Args:
            analysis: Completeness analysis to add
        """
        await self.storage.save_completeness_analysis(None)
        logger.info(
            f"Completeness analysis: "
            f"{analysis.documentation_completeness:.1%} complete"
        )
    
    async def xǁContextManagerǁadd_completeness_analysis__mutmut_2(
        self,
        analysis: CompletenessAnalysis,
    ) -> None:
        """
        Add completeness analysis (RQ5).
        
        Args:
            analysis: Completeness analysis to add
        """
        await self.storage.save_completeness_analysis(analysis)
        logger.info(
            None
        )
    
    xǁContextManagerǁadd_completeness_analysis__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁadd_completeness_analysis__mutmut_1': xǁContextManagerǁadd_completeness_analysis__mutmut_1, 
        'xǁContextManagerǁadd_completeness_analysis__mutmut_2': xǁContextManagerǁadd_completeness_analysis__mutmut_2
    }
    
    def add_completeness_analysis(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁadd_completeness_analysis__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁadd_completeness_analysis__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_completeness_analysis.__signature__ = _mutmut_signature(xǁContextManagerǁadd_completeness_analysis__mutmut_orig)
    xǁContextManagerǁadd_completeness_analysis__mutmut_orig.__name__ = 'xǁContextManagerǁadd_completeness_analysis'
    
    async def xǁContextManagerǁget_completeness_analysis__mutmut_orig(
        self,
        session_id: UUID,
    ) -> Optional[CompletenessAnalysis]:
        """
        Get completeness analysis for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            Completeness analysis if found
        """
        return await self.storage.get_completeness_analysis(session_id)
    
    async def xǁContextManagerǁget_completeness_analysis__mutmut_1(
        self,
        session_id: UUID,
    ) -> Optional[CompletenessAnalysis]:
        """
        Get completeness analysis for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            Completeness analysis if found
        """
        return await self.storage.get_completeness_analysis(None)
    
    xǁContextManagerǁget_completeness_analysis__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁget_completeness_analysis__mutmut_1': xǁContextManagerǁget_completeness_analysis__mutmut_1
    }
    
    def get_completeness_analysis(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁget_completeness_analysis__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁget_completeness_analysis__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_completeness_analysis.__signature__ = _mutmut_signature(xǁContextManagerǁget_completeness_analysis__mutmut_orig)
    xǁContextManagerǁget_completeness_analysis__mutmut_orig.__name__ = 'xǁContextManagerǁget_completeness_analysis'
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_orig(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_1(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_2(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_3(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_4(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        session.iteration += 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_5(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration = 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_6(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration -= 1
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_7(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 2
        await self.update_session(session)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_8(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 1
        await self.update_session(None)
        
        logger.info(
            f"Session {session_id} iteration: {session.iteration}/{session.max_iterations}"
        )
        
        return session.iteration
    
    # ==================== Iteration Management ====================
    
    async def xǁContextManagerǁincrement_iteration__mutmut_9(
        self,
        session_id: UUID,
    ) -> int:
        """
        Increment the iteration counter for a session (feedback loop).
        
        Args:
            session_id: Session UUID
            
        Returns:
            New iteration number
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.iteration += 1
        await self.update_session(session)
        
        logger.info(
            None
        )
        
        return session.iteration
    
    xǁContextManagerǁincrement_iteration__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁincrement_iteration__mutmut_1': xǁContextManagerǁincrement_iteration__mutmut_1, 
        'xǁContextManagerǁincrement_iteration__mutmut_2': xǁContextManagerǁincrement_iteration__mutmut_2, 
        'xǁContextManagerǁincrement_iteration__mutmut_3': xǁContextManagerǁincrement_iteration__mutmut_3, 
        'xǁContextManagerǁincrement_iteration__mutmut_4': xǁContextManagerǁincrement_iteration__mutmut_4, 
        'xǁContextManagerǁincrement_iteration__mutmut_5': xǁContextManagerǁincrement_iteration__mutmut_5, 
        'xǁContextManagerǁincrement_iteration__mutmut_6': xǁContextManagerǁincrement_iteration__mutmut_6, 
        'xǁContextManagerǁincrement_iteration__mutmut_7': xǁContextManagerǁincrement_iteration__mutmut_7, 
        'xǁContextManagerǁincrement_iteration__mutmut_8': xǁContextManagerǁincrement_iteration__mutmut_8, 
        'xǁContextManagerǁincrement_iteration__mutmut_9': xǁContextManagerǁincrement_iteration__mutmut_9
    }
    
    def increment_iteration(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁincrement_iteration__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁincrement_iteration__mutmut_mutants"), args, kwargs, self)
        return result 
    
    increment_iteration.__signature__ = _mutmut_signature(xǁContextManagerǁincrement_iteration__mutmut_orig)
    xǁContextManagerǁincrement_iteration__mutmut_orig.__name__ = 'xǁContextManagerǁincrement_iteration'
    
    async def xǁContextManagerǁshould_retry__mutmut_orig(
        self,
        session_id: UUID,
    ) -> bool:
        """
        Check if the session should retry (hasn't exceeded max iterations).
        
        Args:
            session_id: Session UUID
            
        Returns:
            True if should retry, False otherwise
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.iteration < session.max_iterations
    
    async def xǁContextManagerǁshould_retry__mutmut_1(
        self,
        session_id: UUID,
    ) -> bool:
        """
        Check if the session should retry (hasn't exceeded max iterations).
        
        Args:
            session_id: Session UUID
            
        Returns:
            True if should retry, False otherwise
        """
        session = None
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.iteration < session.max_iterations
    
    async def xǁContextManagerǁshould_retry__mutmut_2(
        self,
        session_id: UUID,
    ) -> bool:
        """
        Check if the session should retry (hasn't exceeded max iterations).
        
        Args:
            session_id: Session UUID
            
        Returns:
            True if should retry, False otherwise
        """
        session = await self.get_session(None)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.iteration < session.max_iterations
    
    async def xǁContextManagerǁshould_retry__mutmut_3(
        self,
        session_id: UUID,
    ) -> bool:
        """
        Check if the session should retry (hasn't exceeded max iterations).
        
        Args:
            session_id: Session UUID
            
        Returns:
            True if should retry, False otherwise
        """
        session = await self.get_session(session_id)
        if session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.iteration < session.max_iterations
    
    async def xǁContextManagerǁshould_retry__mutmut_4(
        self,
        session_id: UUID,
    ) -> bool:
        """
        Check if the session should retry (hasn't exceeded max iterations).
        
        Args:
            session_id: Session UUID
            
        Returns:
            True if should retry, False otherwise
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(None)
        
        return session.iteration < session.max_iterations
    
    async def xǁContextManagerǁshould_retry__mutmut_5(
        self,
        session_id: UUID,
    ) -> bool:
        """
        Check if the session should retry (hasn't exceeded max iterations).
        
        Args:
            session_id: Session UUID
            
        Returns:
            True if should retry, False otherwise
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session.iteration <= session.max_iterations
    
    xǁContextManagerǁshould_retry__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁshould_retry__mutmut_1': xǁContextManagerǁshould_retry__mutmut_1, 
        'xǁContextManagerǁshould_retry__mutmut_2': xǁContextManagerǁshould_retry__mutmut_2, 
        'xǁContextManagerǁshould_retry__mutmut_3': xǁContextManagerǁshould_retry__mutmut_3, 
        'xǁContextManagerǁshould_retry__mutmut_4': xǁContextManagerǁshould_retry__mutmut_4, 
        'xǁContextManagerǁshould_retry__mutmut_5': xǁContextManagerǁshould_retry__mutmut_5
    }
    
    def should_retry(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁshould_retry__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁshould_retry__mutmut_mutants"), args, kwargs, self)
        return result 
    
    should_retry.__signature__ = _mutmut_signature(xǁContextManagerǁshould_retry__mutmut_orig)
    xǁContextManagerǁshould_retry__mutmut_orig.__name__ = 'xǁContextManagerǁshould_retry'
    
    # ==================== Cleanup ====================
    
    async def xǁContextManagerǁdelete_session__mutmut_orig(
        self,
        session_id: UUID,
    ) -> None:
        """
        Delete a session and all associated data.
        
        Args:
            session_id: Session UUID
        """
        await self.storage.delete_session(session_id)
        logger.info(f"Deleted session {session_id}")
    
    # ==================== Cleanup ====================
    
    async def xǁContextManagerǁdelete_session__mutmut_1(
        self,
        session_id: UUID,
    ) -> None:
        """
        Delete a session and all associated data.
        
        Args:
            session_id: Session UUID
        """
        await self.storage.delete_session(None)
        logger.info(f"Deleted session {session_id}")
    
    # ==================== Cleanup ====================
    
    async def xǁContextManagerǁdelete_session__mutmut_2(
        self,
        session_id: UUID,
    ) -> None:
        """
        Delete a session and all associated data.
        
        Args:
            session_id: Session UUID
        """
        await self.storage.delete_session(session_id)
        logger.info(None)
    
    xǁContextManagerǁdelete_session__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁdelete_session__mutmut_1': xǁContextManagerǁdelete_session__mutmut_1, 
        'xǁContextManagerǁdelete_session__mutmut_2': xǁContextManagerǁdelete_session__mutmut_2
    }
    
    def delete_session(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁdelete_session__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁdelete_session__mutmut_mutants"), args, kwargs, self)
        return result 
    
    delete_session.__signature__ = _mutmut_signature(xǁContextManagerǁdelete_session__mutmut_orig)
    xǁContextManagerǁdelete_session__mutmut_orig.__name__ = 'xǁContextManagerǁdelete_session'
    
    async def xǁContextManagerǁclose__mutmut_orig(self) -> None:
        """Close the storage backend."""
        await self.storage.close()
        logger.info("ContextManager closed")
    
    async def xǁContextManagerǁclose__mutmut_1(self) -> None:
        """Close the storage backend."""
        await self.storage.close()
        logger.info(None)
    
    async def xǁContextManagerǁclose__mutmut_2(self) -> None:
        """Close the storage backend."""
        await self.storage.close()
        logger.info("XXContextManager closedXX")
    
    async def xǁContextManagerǁclose__mutmut_3(self) -> None:
        """Close the storage backend."""
        await self.storage.close()
        logger.info("contextmanager closed")
    
    async def xǁContextManagerǁclose__mutmut_4(self) -> None:
        """Close the storage backend."""
        await self.storage.close()
        logger.info("CONTEXTMANAGER CLOSED")
    
    xǁContextManagerǁclose__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextManagerǁclose__mutmut_1': xǁContextManagerǁclose__mutmut_1, 
        'xǁContextManagerǁclose__mutmut_2': xǁContextManagerǁclose__mutmut_2, 
        'xǁContextManagerǁclose__mutmut_3': xǁContextManagerǁclose__mutmut_3, 
        'xǁContextManagerǁclose__mutmut_4': xǁContextManagerǁclose__mutmut_4
    }
    
    def close(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextManagerǁclose__mutmut_orig"), object.__getattribute__(self, "xǁContextManagerǁclose__mutmut_mutants"), args, kwargs, self)
        return result 
    
    close.__signature__ = _mutmut_signature(xǁContextManagerǁclose__mutmut_orig)
    xǁContextManagerǁclose__mutmut_orig.__name__ = 'xǁContextManagerǁclose'
