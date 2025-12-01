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


class ContextManager:
    """
    Manages the shared context between agents.
    
    Provides high-level operations for:
    - Creating and managing workflow sessions
    - Storing and retrieving agent outputs
    - Managing messages between agents
    - Tracking metrics and analytics
    """
    
    def __init__(self, storage: StorageBackend):
        """
        Initialize the context manager.
        
        Args:
            storage: Storage backend (PostgreSQL + Redis)
        """
        self.storage = storage
        logger.info("ContextManager initialized")
    
    # ==================== Session Management ====================
    
    async def create_session(
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
    
    async def get_session(self, session_id: UUID) -> Optional[WorkflowSession]:
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
    
    async def update_session(self, session: WorkflowSession) -> None:
        """
        Update a workflow session.
        
        Args:
            session: Updated session object
        """
        session.updated_at = datetime.utcnow()
        await self.storage.save_session(session)
        logger.debug(f"Updated session {session.id}")
    
    async def update_session_status(
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
    
    # ==================== Endpoint Management ====================
    
    async def add_endpoint(
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
    
    async def get_endpoints(
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
    
    async def get_endpoint(
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
    
    # ==================== Oracle Management ====================
    
    async def add_oracle(
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
    
    async def get_oracles(
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
    
    async def get_oracle_by_id(
        self,
        session_id: UUID,
        oracle_id: UUID,
    ) -> Optional[Oracle]:
        """
        Get a specific oracle by ID.
        
        Args:
            session_id: Session UUID
            oracle_id: Oracle UUID
            
        Returns:
            Oracle if found, None otherwise
        """
        oracles = await self.get_oracles(session_id)
        for oracle in oracles:
            if oracle.id == oracle_id:
                return oracle
        return None
    
    # ==================== Test Management ====================
    
    async def add_test(
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
    
    async def update_test(
        self,
        test: GeneratedTest,
        session_id: UUID,
    ) -> None:
        """
        Update an existing test in a session.
        
        Args:
            test: Generated test with updated content
            session_id: Session UUID containing the test
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Find and update the test
        for i, existing_test in enumerate(session.tests):
            if existing_test.id == test.id:
                session.tests[i] = test
                await self.update_session(session)
                logger.debug(f"Updated test '{test.test_method_name}' in session {session_id}")
                return
        
        logger.warning(f"Test {test.id} not found in session {session_id}")
    
    async def get_tests(
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
    
    async def get_test_by_id(
        self,
        session_id: UUID,
        test_id: UUID,
    ) -> Optional[GeneratedTest]:
        """
        Get a specific test by ID.
        
        Args:
            session_id: Session UUID
            test_id: Test UUID
            
        Returns:
            GeneratedTest if found, None otherwise
        """
        tests = await self.get_tests(session_id)
        for test in tests:
            if test.id == test_id:
                return test
        return None
    
    async def get_generated_tests(
        self,
        session_id: UUID,
        endpoint_id: Optional[UUID] = None,
    ) -> List[GeneratedTest]:
        """
        Alias for get_tests() for backward compatibility.
        
        Args:
            session_id: Session UUID
            endpoint_id: Optional endpoint UUID to filter by
            
        Returns:
            List of generated tests
        """
        return await self.get_tests(session_id=session_id, endpoint_id=endpoint_id)
    
    # ==================== Execution Results ====================
    
    async def add_execution_result(
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
    
    async def get_execution_results(
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
    
    # ==================== Message Passing ====================
    
    async def send_message(
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
    
    async def get_messages(
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
    
    # ==================== Metrics & Analytics ====================
    
    async def add_inconsistency_report(
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
    
    async def get_inconsistency_reports(
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
    
    async def add_quality_metrics(
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
    
    async def get_quality_metrics(
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
    
    async def add_llm_performance_metrics(
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
    
    async def get_llm_performance_metrics(
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
    
    async def add_completeness_analysis(
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
    
    async def get_completeness_analysis(
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
    
    # ==================== Iteration Management ====================
    
    async def increment_iteration(
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
    
    async def should_retry(
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
    
    # ==================== Cleanup ====================
    
    async def delete_session(
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
    
    async def close(self) -> None:
        """Close the storage backend."""
        await self.storage.close()
        logger.info("ContextManager closed")
