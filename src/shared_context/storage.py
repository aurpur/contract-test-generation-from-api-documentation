"""
Storage backend for shared context.

Provides persistence layer using:
- PostgreSQL for durable storage
- Redis for caching and fast access

Author: Aurel IKAMA HONEY
"""
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

import redis
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.config import get_config
from utils.logging import logger
from .models import (
    AgentMessage,
    AgentType,
    CompletenessAnalysis,
    InconsistencyReport,
    LLMPerformanceMetrics,
    QualityMetrics,
    WorkflowSession,
)

Base = declarative_base()


# ==================== SQLAlchemy Models ====================


class SessionModel(Base):
    """SQLAlchemy model for WorkflowSession."""
    
    __tablename__ = "workflow_sessions"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    collection_name = Column(String(255), nullable=False)
    collection_path = Column(String(512), nullable=False)
    status = Column(String(50), nullable=False)
    current_agent = Column(String(50), nullable=True)
    total_endpoints = Column(Integer, default=0)
    processed_endpoints = Column(Integer, default=0)
    successful_tests = Column(Integer, default=0)
    failed_tests = Column(Integer, default=0)
    iteration = Column(Integer, default=0)
    max_iterations = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    llm_models = Column(JSON, default={})
    config = Column(JSON, default={})
    
    # Store lists as JSON
    endpoints = Column(JSON, default=[])
    oracles = Column(JSON, default=[])
    tests = Column(JSON, default=[])
    execution_results = Column(JSON, default=[])


class MessageModel(Base):
    """SQLAlchemy model for AgentMessage."""
    
    __tablename__ = "agent_messages"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    from_agent = Column(String(50), nullable=False)
    to_agent = Column(String(50), nullable=False)
    message_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    session_id = Column(PGUUID(as_uuid=True), ForeignKey("workflow_sessions.id"))
    parent_message_id = Column(PGUUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=0)


class InconsistencyReportModel(Base):
    """SQLAlchemy model for InconsistencyReport."""
    
    __tablename__ = "inconsistency_reports"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    session_id = Column(PGUUID(as_uuid=True), ForeignKey("workflow_sessions.id"))
    oracle_id = Column(PGUUID(as_uuid=True), nullable=False)
    test_id = Column(PGUUID(as_uuid=True), nullable=False)
    inconsistency_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    oracle_expectation = Column(JSON, default={})
    test_implementation = Column(JSON, default={})
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    detected_by = Column(String(100), nullable=False)


class QualityMetricsModel(Base):
    """SQLAlchemy model for QualityMetrics."""
    
    __tablename__ = "quality_metrics"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    session_id = Column(PGUUID(as_uuid=True), ForeignKey("workflow_sessions.id"))
    test_id = Column(PGUUID(as_uuid=True), nullable=True)
    assertion_count = Column(Integer, default=0)
    valid_assertions = Column(Integer, default=0)
    assertion_coverage = Column(Float, default=0.0)
    cyclomatic_complexity = Column(Integer, nullable=True)
    lines_of_code = Column(Integer, default=0)
    comment_ratio = Column(Float, default=0.0)
    code_duplication = Column(Float, default=0.0)
    method_count = Column(Integer, default=0)
    max_method_length = Column(Integer, default=0)
    quality_score = Column(Float, default=0.0)
    computed_at = Column(DateTime, default=datetime.utcnow)
    tool_version = Column(String(50), nullable=True)


class LLMPerformanceMetricsModel(Base):
    """SQLAlchemy model for LLMPerformanceMetrics."""
    
    __tablename__ = "llm_performance_metrics"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    session_id = Column(PGUUID(as_uuid=True), ForeignKey("workflow_sessions.id"))
    model_name = Column(String(100), nullable=False)
    agent_type = Column(String(50), nullable=False)
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_response_time_ms = Column(Float, default=0.0)
    total_tokens = Column(Integer, default=0)
    avg_confidence_score = Column(Float, default=0.0)
    hallucination_count = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    measured_at = Column(DateTime, default=datetime.utcnow)


class CompletenessAnalysisModel(Base):
    """SQLAlchemy model for CompletenessAnalysis."""
    
    __tablename__ = "completeness_analysis"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    session_id = Column(PGUUID(as_uuid=True), ForeignKey("workflow_sessions.id"))
    documentation_completeness = Column(Float, nullable=False)
    endpoint_completeness = Column(Float, default=0.0)
    request_completeness = Column(Float, default=0.0)
    response_completeness = Column(Float, default=0.0)
    missing_elements = Column(JSON, default=[])
    inferred_elements = Column(JSON, default=[])
    oracle_precision = Column(Float, default=0.0)
    oracle_recall = Column(Float, default=0.0)
    test_success_rate = Column(Float, default=0.0)
    analyzed_at = Column(DateTime, default=datetime.utcnow)


# ==================== Storage Backend Abstract Class ====================


class StorageBackend(ABC):
    """Abstract storage backend."""
    
    @abstractmethod
    async def save_session(self, session: WorkflowSession) -> None:
        """Save a workflow session."""
        pass
    
    @abstractmethod
    async def get_session(self, session_id: UUID) -> Optional[WorkflowSession]:
        """Retrieve a workflow session."""
        pass
    
    @abstractmethod
    async def delete_session(self, session_id: UUID) -> None:
        """Delete a workflow session."""
        pass
    
    @abstractmethod
    async def save_message(self, message: AgentMessage) -> None:
        """Save an agent message."""
        pass
    
    @abstractmethod
    async def get_messages(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """Get messages for a session."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close connections."""
        pass


# ==================== PostgreSQL + Redis Storage ====================


class PostgreSQLRedisStorage(StorageBackend):
    """
    Storage backend using PostgreSQL for persistence and Redis for caching.
    """
    
    def __init__(
        self,
        postgres_url: str,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        cache_ttl: int = 3600,
    ):
        """
        Initialize storage backend.
        
        Args:
            postgres_url: PostgreSQL connection URL
            redis_host: Redis host
            redis_port: Redis port
            redis_db: Redis database number
            cache_ttl: Cache TTL in seconds
        """
        # PostgreSQL setup
        self.engine = create_async_engine(postgres_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        
        # Redis setup
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True,
        )
        self.cache_ttl = cache_ttl
        
        logger.info(
            f"Storage backend initialized (PostgreSQL + Redis, TTL={cache_ttl}s)"
        )
    
    async def initialize(self) -> None:
        """Initialize database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized")
    
    def _get_cache_key(self, prefix: str, id: UUID) -> str:
        """Generate Redis cache key."""
        return f"{prefix}:{str(id)}"
    
    def _cache_get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache."""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def _cache_set(self, key: str, value: Dict[str, Any]) -> None:
        """Set value in cache."""
        self.redis_client.setex(
            key,
            self.cache_ttl,
            json.dumps(value, default=str),
        )
    
    def _cache_delete(self, key: str) -> None:
        """Delete value from cache."""
        self.redis_client.delete(key)
    
    # ==================== Session Operations ====================
    
    async def save_session(self, session: WorkflowSession) -> None:
        """Save a workflow session."""
        async with self.async_session() as db_session:
            # Convert Pydantic model to dict for SQLAlchemy
            session_dict = session.model_dump(mode='json')
            
            # Check if session exists
            result = await db_session.get(SessionModel, session.id)
            
            if result:
                # Update existing
                for key, value in session_dict.items():
                    setattr(result, key, value)
            else:
                # Create new
                db_model = SessionModel(**session_dict)
                db_session.add(db_model)
            
            await db_session.commit()
        
        # Update cache
        cache_key = self._get_cache_key("session", session.id)
        self._cache_set(cache_key, session_dict)
    
    async def get_session(self, session_id: UUID) -> Optional[WorkflowSession]:
        """Retrieve a workflow session."""
        # Try cache first
        cache_key = self._get_cache_key("session", session_id)
        cached = self._cache_get(cache_key)
        
        if cached:
            return WorkflowSession(**cached)
        
        # Fetch from database
        async with self.async_session() as db_session:
            result = await db_session.get(SessionModel, session_id)
            
            if not result:
                return None
            
            # Convert to dict
            session_dict = {
                column.name: getattr(result, column.name)
                for column in result.__table__.columns
            }
            
            # Cache it
            self._cache_set(cache_key, session_dict)
            
            return WorkflowSession(**session_dict)
    
    async def delete_session(self, session_id: UUID) -> None:
        """Delete a workflow session."""
        async with self.async_session() as db_session:
            result = await db_session.get(SessionModel, session_id)
            if result:
                await db_session.delete(result)
                await db_session.commit()
        
        # Delete from cache
        cache_key = self._get_cache_key("session", session_id)
        self._cache_delete(cache_key)
    
    # ==================== Message Operations ====================
    
    async def save_message(self, message: AgentMessage) -> None:
        """Save an agent message."""
        async with self.async_session() as db_session:
            message_dict = message.model_dump(mode='json')
            db_model = MessageModel(**message_dict)
            db_session.add(db_model)
            await db_session.commit()
    
    async def get_messages(
        self,
        session_id: UUID,
        to_agent: Optional[AgentType] = None,
        from_agent: Optional[AgentType] = None,
    ) -> List[AgentMessage]:
        """Get messages for a session."""
        async with self.async_session() as db_session:
            from sqlalchemy import select
            
            query = select(MessageModel).where(MessageModel.session_id == session_id)
            
            if to_agent:
                query = query.where(MessageModel.to_agent == to_agent.value)
            
            if from_agent:
                query = query.where(MessageModel.from_agent == from_agent.value)
            
            result = await db_session.execute(query)
            messages = result.scalars().all()
            
            return [
                AgentMessage(
                    **{
                        column.name: getattr(msg, column.name)
                        for column in msg.__table__.columns
                    }
                )
                for msg in messages
            ]
    
    # ==================== Metrics Operations ====================
    
    async def save_inconsistency_report(self, report: InconsistencyReport) -> None:
        """Save an inconsistency report."""
        async with self.async_session() as db_session:
            report_dict = report.model_dump(mode='json')
            db_model = InconsistencyReportModel(**report_dict)
            db_session.add(db_model)
            await db_session.commit()
    
    async def get_inconsistency_reports(
        self, session_id: UUID
    ) -> List[InconsistencyReport]:
        """Get inconsistency reports for a session."""
        async with self.async_session() as db_session:
            from sqlalchemy import select
            
            query = select(InconsistencyReportModel).where(
                InconsistencyReportModel.session_id == session_id
            )
            result = await db_session.execute(query)
            reports = result.scalars().all()
            
            return [
                InconsistencyReport(
                    **{
                        column.name: getattr(report, column.name)
                        for column in report.__table__.columns
                    }
                )
                for report in reports
            ]
    
    async def save_quality_metrics(self, metrics: QualityMetrics) -> None:
        """Save quality metrics."""
        async with self.async_session() as db_session:
            metrics_dict = metrics.model_dump(mode='json')
            db_model = QualityMetricsModel(**metrics_dict)
            db_session.add(db_model)
            await db_session.commit()
    
    async def get_quality_metrics(self, session_id: UUID) -> List[QualityMetrics]:
        """Get quality metrics for a session."""
        async with self.async_session() as db_session:
            from sqlalchemy import select
            
            query = select(QualityMetricsModel).where(
                QualityMetricsModel.session_id == session_id
            )
            result = await db_session.execute(query)
            metrics_list = result.scalars().all()
            
            return [
                QualityMetrics(
                    **{
                        column.name: getattr(metrics, column.name)
                        for column in metrics.__table__.columns
                    }
                )
                for metrics in metrics_list
            ]
    
    async def save_llm_performance_metrics(
        self, metrics: LLMPerformanceMetrics
    ) -> None:
        """Save LLM performance metrics."""
        async with self.async_session() as db_session:
            metrics_dict = metrics.model_dump(mode='json')
            db_model = LLMPerformanceMetricsModel(**metrics_dict)
            db_session.add(db_model)
            await db_session.commit()
    
    async def get_llm_performance_metrics(
        self,
        session_id: UUID,
        agent_type: Optional[AgentType] = None,
    ) -> List[LLMPerformanceMetrics]:
        """Get LLM performance metrics for a session."""
        async with self.async_session() as db_session:
            from sqlalchemy import select
            
            query = select(LLMPerformanceMetricsModel).where(
                LLMPerformanceMetricsModel.session_id == session_id
            )
            
            if agent_type:
                query = query.where(
                    LLMPerformanceMetricsModel.agent_type == agent_type.value
                )
            
            result = await db_session.execute(query)
            metrics_list = result.scalars().all()
            
            return [
                LLMPerformanceMetrics(
                    **{
                        column.name: getattr(metrics, column.name)
                        for column in metrics.__table__.columns
                    }
                )
                for metrics in metrics_list
            ]
    
    async def save_completeness_analysis(
        self, analysis: CompletenessAnalysis
    ) -> None:
        """Save completeness analysis."""
        async with self.async_session() as db_session:
            analysis_dict = analysis.model_dump(mode='json')
            db_model = CompletenessAnalysisModel(**analysis_dict)
            db_session.add(db_model)
            await db_session.commit()
    
    async def get_completeness_analysis(
        self, session_id: UUID
    ) -> Optional[CompletenessAnalysis]:
        """Get completeness analysis for a session."""
        async with self.async_session() as db_session:
            from sqlalchemy import select
            
            query = select(CompletenessAnalysisModel).where(
                CompletenessAnalysisModel.session_id == session_id
            )
            result = await db_session.execute(query)
            analysis = result.scalars().first()
            
            if not analysis:
                return None
            
            return CompletenessAnalysis(
                **{
                    column.name: getattr(analysis, column.name)
                    for column in analysis.__table__.columns
                }
            )
    
    async def close(self) -> None:
        """Close connections."""
        await self.engine.dispose()
        self.redis_client.close()
        logger.info("Storage backend closed")


# ==================== Factory Function ====================


async def create_storage_backend() -> PostgreSQLRedisStorage:
    """
    Create and initialize storage backend from configuration.
    
    Returns:
        Initialized storage backend
    """
    config = get_config()
    
    # Get database configuration
    db_config = config.config.get("database", {})
    postgres_url = db_config.get(
        "postgres_url",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/contract_tests"
    )
    
    redis_config = config.config.get("redis", {})
    redis_host = redis_config.get("host", "localhost")
    redis_port = redis_config.get("port", 6379)
    redis_db = redis_config.get("db", 0)
    cache_ttl = redis_config.get("cache_ttl", 3600)
    
    # Create storage
    storage = PostgreSQLRedisStorage(
        postgres_url=postgres_url,
        redis_host=redis_host,
        redis_port=redis_port,
        redis_db=redis_db,
        cache_ttl=cache_ttl,
    )
    
    # Initialize tables
    await storage.initialize()
    
    return storage
