"""
Data models for the shared context between agents.

These models define the structure of data passed between agents
(Inductor, Oracle, Contractor, Runner) during the test generation workflow.

Author: Aurel IKAMA HONEY
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator
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


class AgentType(str, Enum):
    """Types of agents in the system."""
    INDUCTOR = "inductor"
    ORACLE = "oracle"
    CONTRACTOR = "contractor"
    RUNNER = "runner"


class ProcessingStatus(str, Enum):
    """Status of processing for a context."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


class HTTPMethod(str, Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AuthType(str, Enum):
    """Authentication types."""
    NONE = "none"
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "apikey"
    OAUTH2 = "oauth2"


class EndpointContext(BaseModel):
    """Context for a single API endpoint."""
    
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Endpoint name")
    method: HTTPMethod = Field(..., description="HTTP method")
    url: str = Field(..., description="Endpoint URL/path")
    
    # Request details
    headers: Dict[str, str] = Field(default_factory=dict)
    query_params: Dict[str, Any] = Field(default_factory=dict)
    path_params: List[str] = Field(default_factory=list)
    body: Optional[Dict[str, Any]] = Field(default=None)
    body_schema: Optional[Dict[str, Any]] = Field(default=None)
    
    # Authentication
    auth_type: AuthType = Field(default=AuthType.NONE)
    auth_config: Dict[str, Any] = Field(default_factory=dict)
    
    # Expected response (from documentation)
    expected_status: Optional[int] = Field(default=None)
    expected_headers: Dict[str, str] = Field(default_factory=dict)
    expected_response_schema: Optional[Dict[str, Any]] = Field(default=None)
    
    # Metadata
    description: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)
    documentation_completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class Oracle(BaseModel):
    """Validation rule/oracle for an endpoint."""
    
    id: UUID = Field(default_factory=uuid4)
    endpoint_id: UUID = Field(..., description="Associated endpoint ID")
    
    # Validation rules
    status_code: int = Field(..., description="Expected status code")
    status_code_range: Optional[tuple[int, int]] = Field(default=None)
    
    # Header validations
    required_headers: List[str] = Field(default_factory=list)
    header_constraints: Dict[str, Any] = Field(default_factory=dict)
    
    # Body validations
    response_schema: Optional[Dict[str, Any]] = Field(default=None)
    json_path_assertions: Dict[str, Any] = Field(default_factory=dict)
    
    # Domain constraints
    value_constraints: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    business_rules: List[str] = Field(default_factory=list)
    
    # Metadata
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    rationale: Optional[str] = Field(default=None)
    llm_model: Optional[str] = Field(default=None)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class GeneratedTest(BaseModel):
    """Generated test code for an endpoint."""
    
    id: UUID = Field(default_factory=uuid4)
    endpoint_id: UUID = Field(..., description="Associated endpoint ID")
    oracle_id: UUID = Field(..., description="Associated oracle ID")
    
    # Test code
    test_class_name: str = Field(..., description="Java test class name")
    test_method_name: str = Field(..., description="Java test method name")
    test_code: str = Field(..., description="Complete Java test code")
    
    # Gherkin feature
    feature_file_name: Optional[str] = Field(default=None, description="Gherkin feature file name")
    feature_content: Optional[str] = Field(default=None, description="Complete Gherkin feature content")
    
    # Test configuration
    setup_code: Optional[str] = Field(default=None)
    teardown_code: Optional[str] = Field(default=None)
    dependencies: List[str] = Field(default_factory=list)
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    llm_model: Optional[str] = Field(default=None)
    template_version: Optional[str] = Field(default=None)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class TestExecutionResult(BaseModel):
    """Result of executing a generated test."""
    
    id: UUID = Field(default_factory=uuid4)
    test_id: UUID = Field(..., description="Associated test ID")
    
    # Execution results
    passed: bool = Field(..., description="Test passed or failed")
    execution_time_ms: float = Field(..., description="Execution time in milliseconds")
    
    # Failure details
    error_message: Optional[str] = Field(default=None)
    stack_trace: Optional[str] = Field(default=None)
    assertion_failures: List[str] = Field(default_factory=list)
    
    # Actual vs Expected
    actual_status_code: Optional[int] = Field(default=None)
    actual_headers: Dict[str, str] = Field(default_factory=dict)
    actual_body: Optional[str] = Field(default=None)
    
    # Metadata
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    maven_output: Optional[str] = Field(default=None)
    retry_count: int = Field(default=0)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class AgentMessage(BaseModel):
    """Message passed between agents."""
    
    id: UUID = Field(default_factory=uuid4)
    from_agent: AgentType = Field(..., description="Sender agent")
    to_agent: AgentType = Field(..., description="Receiver agent")
    
    message_type: str = Field(..., description="Type of message")
    payload: Dict[str, Any] = Field(..., description="Message payload")
    
    # Context
    session_id: UUID = Field(..., description="Workflow session ID")
    parent_message_id: Optional[UUID] = Field(default=None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    priority: int = Field(default=0)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class WorkflowSession(BaseModel):
    """A workflow session tracking the entire test generation process."""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Source
    collection_name: str = Field(..., description="Bruno collection name")
    collection_path: str = Field(..., description="Path to collection")
    
    # Status
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING)
    current_agent: Optional[AgentType] = Field(default=None)
    
    # Progress
    total_endpoints: int = Field(default=0)
    processed_endpoints: int = Field(default=0)
    successful_tests: int = Field(default=0)
    failed_tests: int = Field(default=0)
    
    # Agent outputs
    endpoints: List[EndpointContext] = Field(default_factory=list)
    oracles: List[Oracle] = Field(default_factory=list)
    tests: List[GeneratedTest] = Field(default_factory=list)
    execution_results: List[TestExecutionResult] = Field(default_factory=list)
    
    # Iteration tracking (for feedback loop)
    iteration: int = Field(default=0)
    max_iterations: int = Field(default=3)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Configuration
    llm_models: Dict[AgentType, str] = Field(default_factory=dict)
    config: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
    
    @field_validator('updated_at', mode='before')
    @classmethod
    def set_updated_at(cls, v):
        """Always update the updated_at timestamp."""
        return datetime.utcnow()


class InconsistencyReport(BaseModel):
    """Report of inconsistencies detected between oracle and test (RQ2)."""
    
    id: UUID = Field(default_factory=uuid4)
    session_id: UUID = Field(..., description="Associated session ID")
    oracle_id: UUID = Field(..., description="Oracle ID")
    test_id: UUID = Field(..., description="Test ID")
    
    # Inconsistency details
    inconsistency_type: str = Field(..., description="Type of inconsistency")
    severity: str = Field(..., description="Severity: critical, major, minor")
    description: str = Field(..., description="Description of inconsistency")
    
    # Context
    oracle_expectation: Dict[str, Any] = Field(default_factory=dict)
    test_implementation: Dict[str, Any] = Field(default_factory=dict)
    
    # Resolution
    resolved: bool = Field(default=False)
    resolution_notes: Optional[str] = Field(default=None)
    
    # Metadata
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    detected_by: str = Field(..., description="Detection method/tool")
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class QualityMetrics(BaseModel):
    """Quality metrics for generated tests (RQ3)."""
    
    id: UUID = Field(default_factory=uuid4)
    session_id: UUID = Field(..., description="Associated session ID")
    test_id: Optional[UUID] = Field(default=None)
    
    # Correctness metrics
    assertion_count: int = Field(default=0)
    valid_assertions: int = Field(default=0)
    assertion_coverage: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Readability metrics
    cyclomatic_complexity: Optional[int] = Field(default=None)
    lines_of_code: int = Field(default=0)
    comment_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Maintainability metrics
    code_duplication: float = Field(default=0.0, ge=0.0, le=1.0)
    method_count: int = Field(default=0)
    max_method_length: int = Field(default=0)
    
    # Overall score
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Metadata
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    tool_version: Optional[str] = Field(default=None)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class LLMPerformanceMetrics(BaseModel):
    """Performance metrics for LLM models (RQ4)."""
    
    id: UUID = Field(default_factory=uuid4)
    session_id: UUID = Field(..., description="Associated session ID")
    
    # Model info
    model_name: str = Field(..., description="LLM model name")
    agent_type: AgentType = Field(..., description="Agent using the model")
    
    # Performance metrics
    total_requests: int = Field(default=0)
    successful_requests: int = Field(default=0)
    failed_requests: int = Field(default=0)
    
    # Timing
    avg_response_time_ms: float = Field(default=0.0)
    total_tokens: int = Field(default=0)
    
    # Quality
    avg_confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    hallucination_count: int = Field(default=0)
    
    # Cost
    total_cost_usd: float = Field(default=0.0)
    
    # Metadata
    measured_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class CompletenessAnalysis(BaseModel):
    """Analysis of documentation completeness impact (RQ5)."""
    
    id: UUID = Field(default_factory=uuid4)
    session_id: UUID = Field(..., description="Associated session ID")
    
    # Completeness scores
    documentation_completeness: float = Field(..., ge=0.0, le=1.0)
    endpoint_completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    request_completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    response_completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Missing elements
    missing_elements: List[str] = Field(default_factory=list)
    inferred_elements: List[str] = Field(default_factory=list)
    
    # Impact on quality
    oracle_precision: float = Field(default=0.0, ge=0.0, le=1.0)
    oracle_recall: float = Field(default=0.0, ge=0.0, le=1.0)
    test_success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
