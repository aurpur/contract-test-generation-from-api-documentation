"""
RQ1 Oracle Validation Experiment Runner

This module orchestrates experiments to validate Research Question 1:
"Quelle est la précision et la complétude des oracles générés automatiquement?"

It performs comprehensive validation of oracle generation accuracy by:
1. Creating/loading ground truth oracles
2. Running oracle generation with different LLM models
3. Comparing generated oracles against ground truth
4. Computing precision, recall, F1-score, and completeness metrics
5. Generating detailed reports and visualizations

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import asyncio
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
import statistics

from src.shared_context.models import EndpointContext, Oracle, HTTPMethod
from src.agents.oracle import OracleAgent
from src.validation.oracle_metrics import (
    OracleMetricsCalculator,
    GroundTruth,
    OraclePrecisionMetrics
)


@dataclass
class ExperimentConfig:
    """Configuration for RQ1 validation experiments."""
    experiment_id: str
    name: str
    description: str
    llm_models: List[str]  # e.g., ["gpt-4", "claude-3-opus", "gemini-pro"]
    num_endpoints: int
    include_real_api_calls: bool = False
    max_retries: int = 2
    timeout_seconds: int = 30
    output_dir: Path = Path("experiments/results")
    
    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class EndpointExperimentResult:
    """Results for a single endpoint in RQ1 experiment."""
    endpoint_id: UUID
    endpoint_name: str
    ground_truth: GroundTruth
    generated_oracles: Dict[str, Oracle] = field(default_factory=dict)  # llm_model -> Oracle
    metrics: Dict[str, OraclePrecisionMetrics] = field(default_factory=dict)  # llm_model -> metrics
    errors: Dict[str, str] = field(default_factory=dict)  # llm_model -> error message
    execution_times: Dict[str, float] = field(default_factory=dict)  # llm_model -> seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "endpoint_id": str(self.endpoint_id),
            "endpoint_name": self.endpoint_name,
            "ground_truth": {
                "endpoint_id": str(self.ground_truth.endpoint_id),
                "status_code": self.ground_truth.status_code,
                "required_headers": self.ground_truth.required_headers,
                "optional_headers": self.ground_truth.optional_headers,
                "response_schema": self.ground_truth.response_schema,
                "business_rules": self.ground_truth.business_rules,
                "source": self.ground_truth.source,
                "confidence": self.ground_truth.confidence
            },
            "generated_oracles": {
                model: {
                    "oracle_id": str(oracle.id),
                    "name": oracle.name,
                    "status_code": oracle.status_code,
                    "required_headers": oracle.required_headers,
                    "response_schema": oracle.response_schema,
                    "confidence": oracle.confidence
                }
                for model, oracle in self.generated_oracles.items()
            },
            "metrics": {
                model: {
                    "precision": m.precision,
                    "recall": m.recall,
                    "f1_score": m.f1_score,
                    "completeness_score": m.completeness_score,
                    "true_positives": m.true_positives,
                    "false_positives": m.false_positives,
                    "false_negatives": m.false_negatives
                }
                for model, m in self.metrics.items()
            },
            "errors": self.errors,
            "execution_times": self.execution_times
        }


@dataclass
class ExperimentReport:
    """Aggregate report for entire RQ1 experiment."""
    experiment_id: str
    config: ExperimentConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    endpoint_results: List[EndpointExperimentResult] = field(default_factory=list)
    
    # Aggregate metrics per LLM
    aggregate_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Rankings
    llm_rankings: Dict[str, int] = field(default_factory=dict)  # model -> rank (1-based)
    
    # Statistics
    total_endpoints: int = 0
    successful_generations: Dict[str, int] = field(default_factory=dict)  # model -> count
    failed_generations: Dict[str, int] = field(default_factory=dict)  # model -> count
    
    def calculate_aggregates(self):
        """Calculate aggregate metrics across all endpoints."""
        for model in self.config.llm_models:
            model_metrics = [
                result.metrics[model]
                for result in self.endpoint_results
                if model in result.metrics
            ]
            
            if not model_metrics:
                continue
            
            self.aggregate_metrics[model] = {
                "precision_mean": statistics.mean(m.precision for m in model_metrics),
                "precision_std": statistics.stdev(m.precision for m in model_metrics) if len(model_metrics) > 1 else 0.0,
                "recall_mean": statistics.mean(m.recall for m in model_metrics),
                "recall_std": statistics.stdev(m.recall for m in model_metrics) if len(model_metrics) > 1 else 0.0,
                "f1_mean": statistics.mean(m.f1_score for m in model_metrics),
                "f1_std": statistics.stdev(m.f1_score for m in model_metrics) if len(model_metrics) > 1 else 0.0,
                "completeness_mean": statistics.mean(m.completeness_score for m in model_metrics),
                "completeness_std": statistics.stdev(m.completeness_score for m in model_metrics) if len(model_metrics) > 1 else 0.0,
            }
            
            self.successful_generations[model] = len(model_metrics)
            self.failed_generations[model] = self.total_endpoints - len(model_metrics)
        
        # Rank models by F1 score
        if self.aggregate_metrics:
            sorted_models = sorted(
                self.aggregate_metrics.items(),
                key=lambda x: x[1]["f1_mean"],
                reverse=True
            )
            for rank, (model, _) in enumerate(sorted_models, 1):
                self.llm_rankings[model] = rank
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "experiment_id": self.experiment_id,
            "config": {
                "experiment_id": self.config.experiment_id,
                "name": self.config.name,
                "description": self.config.description,
                "llm_models": self.config.llm_models,
                "num_endpoints": self.config.num_endpoints,
                "include_real_api_calls": self.config.include_real_api_calls
            },
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_endpoints": self.total_endpoints,
            "endpoint_results": [r.to_dict() for r in self.endpoint_results],
            "aggregate_metrics": self.aggregate_metrics,
            "llm_rankings": self.llm_rankings,
            "successful_generations": self.successful_generations,
            "failed_generations": self.failed_generations
        }
    
    def save(self, output_path: Optional[Path] = None):
        """Save report to JSON file."""
        if output_path is None:
            output_path = self.config.output_dir / f"rq1_report_{self.experiment_id}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ1ExperimentRunner:
    """
    Orchestrates RQ1 validation experiments.
    
    Runs experiments to measure oracle generation precision and completeness
    across different LLM models.
    """
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.calculator = OracleMetricsCalculator()
        self.oracle_agents: Dict[str, OracleAgent] = {}
        
        # Initialize Oracle agents for each LLM model
        for model in config.llm_models:
            self.oracle_agents[model] = OracleAgent(
                llm_model=model,
                enable_real_api_calls=config.include_real_api_calls
            )
    
    async def run_experiment(
        self,
        endpoints: List[EndpointContext],
        ground_truths: Dict[UUID, GroundTruth]
    ) -> ExperimentReport:
        """
        Run complete RQ1 experiment.
        
        Args:
            endpoints: List of endpoint contexts to test
            ground_truths: Ground truth oracles for each endpoint
            
        Returns:
            ExperimentReport with results and metrics
        """
        report = ExperimentReport(
            experiment_id=self.config.experiment_id,
            config=self.config,
            started_at=datetime.utcnow(),
            total_endpoints=len(endpoints)
        )
        
        # Run experiments for each endpoint
        for endpoint in endpoints:
            if endpoint.id not in ground_truths:
                print(f"⚠️  Skipping {endpoint.name}: no ground truth available")
                continue
            
            result = await self._run_endpoint_experiment(
                endpoint,
                ground_truths[endpoint.id]
            )
            report.endpoint_results.append(result)
        
        # Calculate aggregate metrics
        report.completed_at = datetime.utcnow()
        report.calculate_aggregates()
        
        # Save report
        report.save()
        
        return report
    
    async def _run_endpoint_experiment(
        self,
        endpoint: EndpointContext,
        ground_truth: GroundTruth
    ) -> EndpointExperimentResult:
        """Run experiment for a single endpoint across all LLM models."""
        result = EndpointExperimentResult(
            endpoint_id=endpoint.id,
            endpoint_name=endpoint.name,
            ground_truth=ground_truth
        )
        
        # Generate oracles with each LLM model
        for model in self.config.llm_models:
            try:
                start_time = datetime.utcnow()
                
                # Generate oracle
                oracle = await self._generate_oracle(
                    model,
                    endpoint
                )
                
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Store results
                result.generated_oracles[model] = oracle
                result.execution_times[model] = execution_time
                
                # Calculate metrics
                metrics = self.calculator.calculate_metrics(
                    oracle=oracle,
                    endpoint=endpoint,
                    ground_truth=ground_truth
                )
                result.metrics[model] = metrics
                
                print(f"✓ {endpoint.name} with {model}: P={metrics.precision:.2f}, R={metrics.recall:.2f}, F1={metrics.f1_score:.2f}")
                
            except Exception as e:
                result.errors[model] = str(e)
                print(f"✗ {endpoint.name} with {model}: {e}")
        
        return result
    
    async def _generate_oracle(
        self,
        model: str,
        endpoint: EndpointContext
    ) -> Oracle:
        """Generate oracle using specified LLM model."""
        agent = self.oracle_agents[model]
        
        # Create task for oracle generation
        from src.shared_context.models import Task
        task = Task(
            task_type="derive_oracles",
            payload={"contexts": [endpoint]}
        )
        
        # Execute task
        result = await agent.process_task(task)
        
        # Extract oracle from result
        oracles = result.get("oracles", [])
        if not oracles:
            raise ValueError(f"No oracle generated by {model}")
        
        return oracles[0]


def create_sample_endpoints() -> List[EndpointContext]:
    """Create sample endpoint contexts for testing."""
    return [
        EndpointContext(
            name="Get User by ID",
            method=HTTPMethod.GET,
            url="/api/users/{id}",
            description="Retrieve a user by their unique identifier",
            parameters=[
                {"name": "id", "type": "path", "required": True, "description": "User ID"}
            ],
            documentation_completeness=1.0
        ),
        EndpointContext(
            name="Create User",
            method=HTTPMethod.POST,
            url="/api/users",
            description="Create a new user",
            request_body={
                "type": "object",
                "required": ["email", "name"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "name": {"type": "string", "minLength": 1}
                }
            },
            documentation_completeness=1.0
        ),
        EndpointContext(
            name="List Users",
            method=HTTPMethod.GET,
            url="/api/users",
            description="Get a paginated list of users",
            parameters=[
                {"name": "page", "type": "query", "required": False, "description": "Page number"},
                {"name": "limit", "type": "query", "required": False, "description": "Items per page"}
            ],
            documentation_completeness=0.8
        )
    ]


def create_sample_ground_truths(endpoints: List[EndpointContext]) -> Dict[UUID, GroundTruth]:
    """Create sample ground truth oracles for testing."""
    ground_truths = {}
    
    for endpoint in endpoints:
        if "Get User by ID" in endpoint.name:
            ground_truths[endpoint.id] = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=200,
                required_headers={
                    "Content-Type": "application/json"
                },
                optional_headers={
                    "Cache-Control": "max-age=3600"
                },
                response_schema={
                    "type": "object",
                    "required": ["id", "email", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string"},
                        "name": {"type": "string"},
                        "created_at": {"type": "string"}
                    }
                },
                business_rules=[
                    "User ID must be positive integer",
                    "Email must be unique",
                    "Created_at must be ISO8601 timestamp"
                ],
                source="manual_annotation",
                confidence=1.0
            )
        
        elif "Create User" in endpoint.name:
            ground_truths[endpoint.id] = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=201,
                required_headers={
                    "Content-Type": "application/json",
                    "Location": "/api/users/{id}"
                },
                optional_headers={},
                response_schema={
                    "type": "object",
                    "required": ["id", "email", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string"},
                        "name": {"type": "string"}
                    }
                },
                business_rules=[
                    "Returns 409 if email already exists",
                    "Returns 400 if email format invalid"
                ],
                source="manual_annotation",
                confidence=1.0
            )
        
        elif "List Users" in endpoint.name:
            ground_truths[endpoint.id] = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=200,
                required_headers={
                    "Content-Type": "application/json"
                },
                optional_headers={
                    "X-Total-Count": "integer"
                },
                response_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "email": {"type": "string"},
                            "name": {"type": "string"}
                        }
                    }
                },
                business_rules=[
                    "Default page=1, limit=10",
                    "Maximum limit=100"
                ],
                source="manual_annotation",
                confidence=1.0
            )
    
    return ground_truths


async def run_sample_experiment():
    """Run a sample RQ1 experiment."""
    # Configuration
    config = ExperimentConfig(
        experiment_id=f"rq1_sample_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        name="RQ1 Sample Validation",
        description="Sample experiment to validate oracle precision and completeness",
        llm_models=["gpt-4", "claude-3-opus"],  # Add more as needed
        num_endpoints=3,
        include_real_api_calls=False,
        output_dir=Path("experiments/results/rq1")
    )
    
    # Create test data
    endpoints = create_sample_endpoints()
    ground_truths = create_sample_ground_truths(endpoints)
    
    # Run experiment
    runner = RQ1ExperimentRunner(config)
    report = await runner.run_experiment(endpoints, ground_truths)
    
    # Print summary
    print("\n" + "="*80)
    print(f"RQ1 Experiment Complete: {config.experiment_id}")
    print("="*80)
    print(f"Total Endpoints: {report.total_endpoints}")
    print(f"Duration: {(report.completed_at - report.started_at).total_seconds():.2f}s")
    print("\nAggregate Metrics by LLM:")
    print("-"*80)
    
    for model, metrics in sorted(
        report.aggregate_metrics.items(),
        key=lambda x: x[1]["f1_mean"],
        reverse=True
    ):
        rank = report.llm_rankings[model]
        print(f"\n{rank}. {model}")
        print(f"   Precision: {metrics['precision_mean']:.3f} (±{metrics['precision_std']:.3f})")
        print(f"   Recall:    {metrics['recall_mean']:.3f} (±{metrics['recall_std']:.3f})")
        print(f"   F1 Score:  {metrics['f1_mean']:.3f} (±{metrics['f1_std']:.3f})")
        print(f"   Complete:  {metrics['completeness_mean']:.3f} (±{metrics['completeness_std']:.3f})")
        print(f"   Success:   {report.successful_generations[model]}/{report.total_endpoints}")
    
    print("\n" + "="*80)
    print(f"Report saved to: experiments/results/rq1/rq1_report_{config.experiment_id}.json")
    print("="*80)
    
    return report


if __name__ == "__main__":
    # Run sample experiment
    asyncio.run(run_sample_experiment())
