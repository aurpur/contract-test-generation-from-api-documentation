"""
RQ2 Consistency Validation Experiment Runner

This module orchestrates experiments to validate Research Question 2:
"Le code généré est-il cohérent avec les oracles dérivés?"

It performs comprehensive consistency validation by:
1. Generating oracles for test endpoints
2. Generating test code (Java + Gherkin) from oracles
3. Detecting inconsistencies between oracles and generated code
4. Computing coherence scores and consistency metrics
5. Identifying missing, extra, or incorrect validations
6. Generating detailed reports and visualizations

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import asyncio
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from uuid import UUID, uuid4
import statistics

from src.shared_context.models import (
    EndpointContext, 
    Oracle, 
    GeneratedTest,
    HTTPMethod,
    AuthType
)
from src.validation.inconsistency_detector import (
    InconsistencyDetector,
    InconsistencyReport,
    InconsistencySeverity,
    InconsistencyType
)


@dataclass
class ConsistencyExperimentConfig:
    """Configuration for RQ2 consistency validation experiments."""
    experiment_id: str
    name: str
    description: str
    llm_models: List[str]  # e.g., ["gpt-4", "claude-3-opus", "gemini-pro"]
    num_endpoints: int
    test_frameworks: List[str] = field(default_factory=lambda: ["rest-assured", "gherkin"])
    
    # Thresholds
    min_coherence_score: float = 0.8  # Minimum acceptable coherence
    max_critical_inconsistencies: int = 0  # Max critical issues allowed
    max_major_inconsistencies: int = 2  # Max major issues allowed
    
    # Execution settings
    max_retries: int = 2
    timeout_seconds: int = 30
    output_dir: Path = Path("experiments/results/rq2")
    
    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class EndpointConsistencyResult:
    """Consistency validation results for a single endpoint."""
    endpoint_id: UUID
    endpoint_name: str
    oracle: Optional[Oracle] = None
    generated_test: Optional[GeneratedTest] = None
    
    # Inconsistency analysis
    inconsistency_report: Optional[InconsistencyReport] = None
    
    # Per-LLM results (if comparing multiple models)
    llm_model: str = ""
    
    # Metrics
    coherence_score: float = 0.0  # 0.0 (incoherent) to 1.0 (fully coherent)
    java_coverage_ratio: float = 0.0  # Ratio of oracle validations in Java code
    gherkin_coverage_ratio: float = 0.0  # Ratio of oracle validations in Gherkin
    
    # Inconsistency counts by severity
    critical_count: int = 0
    major_count: int = 0
    minor_count: int = 0
    info_count: int = 0
    
    # Inconsistency counts by type
    missing_validations: int = 0
    extra_validations: int = 0
    incorrect_implementations: int = 0
    
    # Quality flags
    passes_threshold: bool = False  # coherence_score >= min_coherence_score
    has_critical_issues: bool = False
    has_major_issues: bool = False
    
    # Execution metadata
    generation_time_seconds: float = 0.0
    validation_time_seconds: float = 0.0
    error_message: Optional[str] = None
    
    def calculate_derived_metrics(self):
        """Calculate derived metrics from inconsistency report."""
        if self.inconsistency_report:
            report = self.inconsistency_report
            
            # Extract counts
            self.critical_count = len(report.critical)
            self.major_count = len(report.major)
            self.minor_count = len(report.minor)
            self.info_count = len(report.info)
            
            self.missing_validations = report.total_missing_validations
            self.extra_validations = report.total_extra_validations
            self.incorrect_implementations = report.total_incorrect_implementations
            
            # Extract scores
            self.coherence_score = report.coherence_score
            self.java_coverage_ratio = report.java_coverage_ratio
            self.gherkin_coverage_ratio = report.gherkin_coverage_ratio
            
            # Quality flags
            self.has_critical_issues = self.critical_count > 0
            self.has_major_issues = self.major_count > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "endpoint_id": str(self.endpoint_id),
            "endpoint_name": self.endpoint_name,
            "llm_model": self.llm_model,
            "coherence_score": self.coherence_score,
            "java_coverage_ratio": self.java_coverage_ratio,
            "gherkin_coverage_ratio": self.gherkin_coverage_ratio,
            "inconsistency_counts": {
                "critical": self.critical_count,
                "major": self.major_count,
                "minor": self.minor_count,
                "info": self.info_count,
                "missing_validations": self.missing_validations,
                "extra_validations": self.extra_validations,
                "incorrect_implementations": self.incorrect_implementations
            },
            "quality_flags": {
                "passes_threshold": self.passes_threshold,
                "has_critical_issues": self.has_critical_issues,
                "has_major_issues": self.has_major_issues
            },
            "execution_metadata": {
                "generation_time_seconds": self.generation_time_seconds,
                "validation_time_seconds": self.validation_time_seconds,
                "error_message": self.error_message
            }
        }
        
        # Add detailed inconsistency report if available
        if self.inconsistency_report:
            result["inconsistencies"] = {
                "critical": [self._inconsistency_to_dict(i) for i in self.inconsistency_report.critical],
                "major": [self._inconsistency_to_dict(i) for i in self.inconsistency_report.major],
                "minor": [self._inconsistency_to_dict(i) for i in self.inconsistency_report.minor],
                "info": [self._inconsistency_to_dict(i) for i in self.inconsistency_report.info]
            }
        
        return result
    
    def _inconsistency_to_dict(self, inconsistency) -> Dict[str, Any]:
        """Convert inconsistency to dictionary."""
        return {
            "type": inconsistency.type.value,
            "severity": inconsistency.severity.value,
            "category": inconsistency.category,
            "field_name": inconsistency.field_name,
            "oracle_expectation": str(inconsistency.oracle_expectation),
            "code_implementation": str(inconsistency.code_implementation),
            "recommendation": inconsistency.recommendation
        }


@dataclass
class ConsistencyExperimentReport:
    """Aggregate report for entire RQ2 consistency experiment."""
    experiment_id: str
    config: ConsistencyExperimentConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    # Results per endpoint
    endpoint_results: List[EndpointConsistencyResult] = field(default_factory=list)
    
    # Aggregate metrics per LLM
    aggregate_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Rankings by coherence
    llm_rankings: Dict[str, int] = field(default_factory=dict)  # model -> rank (1-based)
    
    # Overall statistics
    total_endpoints: int = 0
    successful_validations: Dict[str, int] = field(default_factory=dict)  # model -> count
    failed_validations: Dict[str, int] = field(default_factory=dict)  # model -> count
    
    # Quality gates
    endpoints_passing_threshold: Dict[str, int] = field(default_factory=dict)  # model -> count
    endpoints_with_critical_issues: Dict[str, int] = field(default_factory=dict)
    endpoints_with_major_issues: Dict[str, int] = field(default_factory=dict)
    
    def calculate_aggregates(self):
        """Calculate aggregate metrics across all endpoints."""
        # Group results by LLM model
        results_by_model: Dict[str, List[EndpointConsistencyResult]] = {}
        for result in self.endpoint_results:
            if result.llm_model not in results_by_model:
                results_by_model[result.llm_model] = []
            results_by_model[result.llm_model].append(result)
        
        # Calculate aggregates for each model
        for model, results in results_by_model.items():
            # Filter successful validations (no errors)
            successful_results = [r for r in results if r.error_message is None]
            
            if not successful_results:
                continue
            
            # Basic counts
            self.successful_validations[model] = len(successful_results)
            self.failed_validations[model] = len(results) - len(successful_results)
            
            # Quality gate counts
            self.endpoints_passing_threshold[model] = sum(1 for r in successful_results if r.passes_threshold)
            self.endpoints_with_critical_issues[model] = sum(1 for r in successful_results if r.has_critical_issues)
            self.endpoints_with_major_issues[model] = sum(1 for r in successful_results if r.has_major_issues)
            
            # Aggregate metrics
            self.aggregate_metrics[model] = {
                # Coherence
                "coherence_mean": statistics.mean(r.coherence_score for r in successful_results),
                "coherence_std": statistics.stdev(r.coherence_score for r in successful_results) if len(successful_results) > 1 else 0.0,
                "coherence_min": min(r.coherence_score for r in successful_results),
                "coherence_max": max(r.coherence_score for r in successful_results),
                
                # Coverage
                "java_coverage_mean": statistics.mean(r.java_coverage_ratio for r in successful_results),
                "gherkin_coverage_mean": statistics.mean(r.gherkin_coverage_ratio for r in successful_results),
                
                # Inconsistency counts (averages)
                "critical_avg": statistics.mean(r.critical_count for r in successful_results),
                "major_avg": statistics.mean(r.major_count for r in successful_results),
                "minor_avg": statistics.mean(r.minor_count for r in successful_results),
                "missing_validations_avg": statistics.mean(r.missing_validations for r in successful_results),
                "extra_validations_avg": statistics.mean(r.extra_validations for r in successful_results),
                "incorrect_implementations_avg": statistics.mean(r.incorrect_implementations for r in successful_results),
                
                # Quality rates
                "pass_rate": self.endpoints_passing_threshold[model] / len(successful_results),
                "critical_issue_rate": self.endpoints_with_critical_issues[model] / len(successful_results),
                "major_issue_rate": self.endpoints_with_major_issues[model] / len(successful_results),
                
                # Execution times
                "generation_time_avg": statistics.mean(r.generation_time_seconds for r in successful_results),
                "validation_time_avg": statistics.mean(r.validation_time_seconds for r in successful_results),
            }
        
        # Rank models by coherence score (descending)
        if self.aggregate_metrics:
            sorted_models = sorted(
                self.aggregate_metrics.items(),
                key=lambda x: x[1]["coherence_mean"],
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
                "test_frameworks": self.config.test_frameworks,
                "thresholds": {
                    "min_coherence_score": self.config.min_coherence_score,
                    "max_critical_inconsistencies": self.config.max_critical_inconsistencies,
                    "max_major_inconsistencies": self.config.max_major_inconsistencies
                }
            },
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_endpoints": self.total_endpoints,
            "endpoint_results": [r.to_dict() for r in self.endpoint_results],
            "aggregate_metrics": self.aggregate_metrics,
            "llm_rankings": self.llm_rankings,
            "successful_validations": self.successful_validations,
            "failed_validations": self.failed_validations,
            "quality_gates": {
                "endpoints_passing_threshold": self.endpoints_passing_threshold,
                "endpoints_with_critical_issues": self.endpoints_with_critical_issues,
                "endpoints_with_major_issues": self.endpoints_with_major_issues
            }
        }
    
    def save(self, output_path: Optional[Path] = None):
        """Save report to JSON file."""
        if output_path is None:
            output_path = self.config.output_dir / f"rq2_report_{self.experiment_id}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ2ExperimentRunner:
    """
    Orchestrates RQ2 consistency validation experiments.
    
    Runs experiments to measure coherence between generated oracles
    and generated test code (Java + Gherkin).
    """
    
    def __init__(
        self,
        config: ConsistencyExperimentConfig,
        inconsistency_detector: Optional[InconsistencyDetector] = None
    ):
        """
        Initialize RQ2 experiment runner.
        
        Args:
            config: Experiment configuration
            inconsistency_detector: Detector for inconsistencies (created if None)
        """
        self.config = config
        self.detector = inconsistency_detector or InconsistencyDetector()
        
        # Initialize report
        self.report = ConsistencyExperimentReport(
            experiment_id=config.experiment_id,
            config=config,
            started_at=datetime.utcnow()
        )
    
    async def run_experiment(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest]
    ) -> ConsistencyExperimentReport:
        """
        Run consistency validation experiment on provided data.
        
        Args:
            endpoints: List of API endpoints
            oracles: Mapping of endpoint_id -> generated Oracle
            generated_tests: Mapping of endpoint_id -> GeneratedTest
        
        Returns:
            ConsistencyExperimentReport with results
        """
        self.report.total_endpoints = len(endpoints)
        
        # Validate each endpoint
        for endpoint in endpoints:
            if endpoint.id not in oracles or endpoint.id not in generated_tests:
                # Skip if oracle or test missing
                result = EndpointConsistencyResult(
                    endpoint_id=endpoint.id,
                    endpoint_name=endpoint.name,
                    error_message="Missing oracle or generated test"
                )
                self.report.endpoint_results.append(result)
                continue
            
            oracle = oracles[endpoint.id]
            test = generated_tests[endpoint.id]
            
            # Validate consistency
            result = await self._validate_endpoint_consistency(
                endpoint=endpoint,
                oracle=oracle,
                test=test
            )
            
            self.report.endpoint_results.append(result)
        
        # Calculate aggregates
        self.report.completed_at = datetime.utcnow()
        self.report.calculate_aggregates()
        
        # Save report
        self.report.save()
        
        return self.report
    
    async def _validate_endpoint_consistency(
        self,
        endpoint: EndpointContext,
        oracle: Oracle,
        test: GeneratedTest
    ) -> EndpointConsistencyResult:
        """
        Validate consistency for a single endpoint.
        
        Args:
            endpoint: Endpoint context
            oracle: Generated oracle
            test: Generated test code
        
        Returns:
            EndpointConsistencyResult with validation results
        """
        start_time = datetime.utcnow()
        
        result = EndpointConsistencyResult(
            endpoint_id=endpoint.id,
            endpoint_name=endpoint.name,
            oracle=oracle,
            generated_test=test,
            llm_model=test.llm_model if hasattr(test, 'llm_model') else "unknown"
        )
        
        try:
            # Detect inconsistencies
            validation_start = datetime.utcnow()
            inconsistency_report = self.detector.detect_inconsistencies(
                oracle=oracle,
                test=test
            )
            validation_time = (datetime.utcnow() - validation_start).total_seconds()
            
            result.inconsistency_report = inconsistency_report
            result.validation_time_seconds = validation_time
            
            # Calculate derived metrics
            result.calculate_derived_metrics()
            
            # Check quality gates
            result.passes_threshold = (
                result.coherence_score >= self.config.min_coherence_score and
                result.critical_count <= self.config.max_critical_inconsistencies and
                result.major_count <= self.config.max_major_inconsistencies
            )
            
        except Exception as e:
            result.error_message = str(e)
        
        # Total execution time
        total_time = (datetime.utcnow() - start_time).total_seconds()
        result.generation_time_seconds = total_time - result.validation_time_seconds
        
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get human-readable summary of experiment results.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.report.aggregate_metrics:
            return {"status": "No results available"}
        
        summary = {
            "experiment_id": self.config.experiment_id,
            "total_endpoints": self.report.total_endpoints,
            "llm_models": self.config.llm_models,
            "results_by_model": {}
        }
        
        for model, metrics in self.report.aggregate_metrics.items():
            summary["results_by_model"][model] = {
                "rank": self.report.llm_rankings.get(model, 0),
                "coherence_score": f"{metrics['coherence_mean']:.3f} ± {metrics['coherence_std']:.3f}",
                "java_coverage": f"{metrics['java_coverage_mean']:.1%}",
                "gherkin_coverage": f"{metrics['gherkin_coverage_mean']:.1%}",
                "pass_rate": f"{metrics['pass_rate']:.1%}",
                "critical_issues": f"{metrics['critical_avg']:.1f} avg",
                "major_issues": f"{metrics['major_avg']:.1f} avg",
                "successful": self.report.successful_validations.get(model, 0),
                "failed": self.report.failed_validations.get(model, 0)
            }
        
        return summary


async def main():
    """Example usage of RQ2 experiment runner."""
    # Example configuration
    config = ConsistencyExperimentConfig(
        experiment_id="rq2_example_001",
        name="RQ2 Consistency Validation Example",
        description="Example experiment to test oracle-code consistency",
        llm_models=["gpt-4", "claude-3-opus"],
        num_endpoints=5,
        min_coherence_score=0.8
    )
    
    # Create runner
    runner = RQ2ExperimentRunner(config=config)
    
    # Note: In real usage, you would:
    # 1. Generate oracles for test endpoints
    # 2. Generate test code from those oracles
    # 3. Pass them to runner.run_experiment()
    
    print(f"RQ2 Experiment Runner initialized: {config.experiment_id}")
    print(f"Configuration: {config.num_endpoints} endpoints, {len(config.llm_models)} models")
    print(f"Output directory: {config.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
