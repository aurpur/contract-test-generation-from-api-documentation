"""
RQ3 Quality Validation Experiments - Code Quality Assessment

Research Question 3: Quelle est la qualité du code de test généré?

This module implements experiments to evaluate the quality of generated test code
across multiple dimensions: correctness, readability, maintainability, and best practices.

Quality Dimensions:
- Correctness: Valid assertions, proper framework usage, compilation/runtime errors
- Readability: Code structure, naming conventions, complexity
- Maintainability: Code duplication, modularity, cohesion
- Best Practices: Framework patterns, test structure, coverage

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import asyncio
import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID

from src.shared_context.models import EndpointContext, GeneratedTest, Oracle
from src.validation.test_quality_analyzer import (
    TestQualityAnalyzer,
    QualityReport,
    CorrectnessMetrics,
    ReadabilityMetrics,
    MaintainabilityMetrics
)


@dataclass
class QualityExperimentConfig:
    """Configuration for RQ3 quality experiments."""
    experiment_id: str
    name: str
    description: str
    llm_models: List[str]
    num_endpoints: int
    test_frameworks: List[str] = field(default_factory=lambda: ["rest-assured", "gherkin"])
    
    # Quality thresholds
    min_correctness_score: float = 0.8
    min_readability_score: float = 0.7
    min_maintainability_score: float = 0.7
    max_cyclomatic_complexity: int = 10
    max_code_duplication: float = 0.2  # 20%
    
    output_dir: Path = Path("experiments/results/rq3")
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "llm_models": self.llm_models,
            "num_endpoints": self.num_endpoints,
            "test_frameworks": self.test_frameworks,
            "quality_thresholds": {
                "min_correctness_score": self.min_correctness_score,
                "min_readability_score": self.min_readability_score,
                "min_maintainability_score": self.min_maintainability_score,
                "max_cyclomatic_complexity": self.max_cyclomatic_complexity,
                "max_code_duplication": self.max_code_duplication
            },
            "output_dir": str(self.output_dir)
        }


@dataclass
class EndpointQualityResult:
    """Quality results for a single endpoint."""
    endpoint_id: UUID
    endpoint_name: str
    llm_model: str = ""
    
    # Quality metrics
    quality_report: Optional[QualityReport] = None
    correctness_score: float = 0.0
    readability_score: float = 0.0
    maintainability_score: float = 0.0
    overall_quality_score: float = 0.0
    
    # Specific metrics
    assertion_count: int = 0
    valid_assertions: int = 0
    lines_of_code: int = 0
    cyclomatic_complexity: float = 0.0
    code_duplication_ratio: float = 0.0
    code_smells_count: int = 0
    
    # Quality flags
    meets_quality_threshold: bool = False
    has_compilation_errors: bool = False
    has_code_smells: bool = False
    
    # Metadata
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    
    def calculate_overall_score(self):
        """Calculate overall quality score from individual dimensions."""
        if self.quality_report:
            self.correctness_score = self.quality_report.correctness_metrics.correctness_score
            self.readability_score = self.quality_report.readability_metrics.readability_score
            self.maintainability_score = self.quality_report.maintainability_metrics.maintainability_score
        
        # Weighted average: correctness 40%, readability 30%, maintainability 30%
        self.overall_quality_score = (
            self.correctness_score * 0.4 +
            self.readability_score * 0.3 +
            self.maintainability_score * 0.3
        )
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            "endpoint_id": str(self.endpoint_id),
            "endpoint_name": self.endpoint_name,
            "llm_model": self.llm_model,
            "quality_scores": {
                "correctness": self.correctness_score,
                "readability": self.readability_score,
                "maintainability": self.maintainability_score,
                "overall": self.overall_quality_score
            },
            "specific_metrics": {
                "assertion_count": self.assertion_count,
                "valid_assertions": self.valid_assertions,
                "lines_of_code": self.lines_of_code,
                "cyclomatic_complexity": self.cyclomatic_complexity,
                "code_duplication_ratio": self.code_duplication_ratio,
                "code_smells_count": self.code_smells_count
            },
            "quality_flags": {
                "meets_quality_threshold": self.meets_quality_threshold,
                "has_compilation_errors": self.has_compilation_errors,
                "has_code_smells": self.has_code_smells
            },
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message
        }


@dataclass
class QualityExperimentReport:
    """Aggregate report for RQ3 quality experiments."""
    experiment_id: str
    config: QualityExperimentConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    # Results
    endpoint_results: List[EndpointQualityResult] = field(default_factory=list)
    total_endpoints: int = 0
    successful_evaluations: Dict[str, int] = field(default_factory=dict)
    
    # Aggregate metrics per LLM
    aggregate_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # LLM rankings
    llm_rankings: Dict[str, int] = field(default_factory=dict)
    
    # Quality gates
    endpoints_meeting_threshold: Dict[str, int] = field(default_factory=dict)
    endpoints_with_errors: Dict[str, int] = field(default_factory=dict)
    endpoints_with_smells: Dict[str, int] = field(default_factory=dict)
    
    def calculate_aggregates(self):
        """Calculate aggregate metrics across all results."""
        # Group results by LLM model
        results_by_llm: Dict[str, List[EndpointQualityResult]] = {}
        for result in self.endpoint_results:
            if result.llm_model not in results_by_llm:
                results_by_llm[result.llm_model] = []
            results_by_llm[result.llm_model].append(result)
        
        # Calculate aggregates for each LLM
        for llm_model, results in results_by_llm.items():
            if not results:
                continue
            
            # Extract scores
            correctness_scores = [r.correctness_score for r in results]
            readability_scores = [r.readability_score for r in results]
            maintainability_scores = [r.maintainability_score for r in results]
            overall_scores = [r.overall_quality_score for r in results]
            
            complexities = [r.cyclomatic_complexity for r in results if r.cyclomatic_complexity > 0]
            duplications = [r.code_duplication_ratio for r in results if r.code_duplication_ratio >= 0]
            
            self.aggregate_metrics[llm_model] = {
                "correctness_mean": statistics.mean(correctness_scores),
                "correctness_std": statistics.stdev(correctness_scores) if len(correctness_scores) > 1 else 0.0,
                "readability_mean": statistics.mean(readability_scores),
                "readability_std": statistics.stdev(readability_scores) if len(readability_scores) > 1 else 0.0,
                "maintainability_mean": statistics.mean(maintainability_scores),
                "maintainability_std": statistics.stdev(maintainability_scores) if len(maintainability_scores) > 1 else 0.0,
                "overall_mean": statistics.mean(overall_scores),
                "overall_std": statistics.stdev(overall_scores) if len(overall_scores) > 1 else 0.0,
                "avg_complexity": statistics.mean(complexities) if complexities else 0.0,
                "avg_duplication": statistics.mean(duplications) if duplications else 0.0,
                "avg_code_smells": statistics.mean([r.code_smells_count for r in results]),
                "pass_rate": sum(1 for r in results if r.meets_quality_threshold) / len(results)
            }
            
            # Count quality gates
            self.successful_evaluations[llm_model] = len([r for r in results if not r.error_message])
            self.endpoints_meeting_threshold[llm_model] = sum(1 for r in results if r.meets_quality_threshold)
            self.endpoints_with_errors[llm_model] = sum(1 for r in results if r.has_compilation_errors)
            self.endpoints_with_smells[llm_model] = sum(1 for r in results if r.has_code_smells)
        
        # Calculate rankings by overall quality
        llm_scores = [(llm, metrics["overall_mean"]) for llm, metrics in self.aggregate_metrics.items()]
        llm_scores.sort(key=lambda x: x[1], reverse=True)
        self.llm_rankings = {llm: rank + 1 for rank, (llm, _) in enumerate(llm_scores)}
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "config": self.config.to_dict(),
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_endpoints": self.total_endpoints,
            "endpoint_results": [r.to_dict() for r in self.endpoint_results],
            "aggregate_metrics": self.aggregate_metrics,
            "llm_rankings": self.llm_rankings,
            "quality_gates": {
                "successful_evaluations": self.successful_evaluations,
                "endpoints_meeting_threshold": self.endpoints_meeting_threshold,
                "endpoints_with_errors": self.endpoints_with_errors,
                "endpoints_with_smells": self.endpoints_with_smells
            }
        }
    
    def save(self) -> Path:
        """Save report to JSON file."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.config.output_dir / f"rq3_report_{self.experiment_id}.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ3ExperimentRunner:
    """Main runner for RQ3 quality validation experiments."""
    
    def __init__(self, config: QualityExperimentConfig):
        """Initialize experiment runner."""
        self.config = config
        self.analyzer = TestQualityAnalyzer()
        self.report = QualityExperimentReport(
            experiment_id=config.experiment_id,
            config=config,
            started_at=datetime.utcnow()
        )
    
    async def run_experiment(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest]
    ) -> QualityExperimentReport:
        """
        Run quality validation experiment.
        
        Args:
            endpoints: List of endpoints to evaluate
            oracles: Mapping of endpoint ID to oracle
            generated_tests: Mapping of endpoint ID to generated test
        
        Returns:
            QualityExperimentReport with results
        """
        self.report.total_endpoints = len(endpoints)
        
        # Evaluate quality for each endpoint
        for endpoint in endpoints:
            oracle = oracles.get(endpoint.id)
            test = generated_tests.get(endpoint.id)
            
            if not test or not oracle:
                continue
            
            result = await self._evaluate_endpoint_quality(endpoint, oracle, test)
            self.report.endpoint_results.append(result)
        
        # Calculate aggregate metrics
        self.report.calculate_aggregates()
        self.report.completed_at = datetime.utcnow()
        
        return self.report
    
    async def _evaluate_endpoint_quality(
        self,
        endpoint: EndpointContext,
        oracle: Oracle,
        test: GeneratedTest
    ) -> EndpointQualityResult:
        """Evaluate quality for a single endpoint."""
        start_time = datetime.utcnow()
        
        result = EndpointQualityResult(
            endpoint_id=endpoint.id,
            endpoint_name=endpoint.name,
            llm_model=getattr(test, 'llm_model', 'unknown')
        )
        
        try:
            # Analyze test quality
            quality_report = self.analyzer.analyze_test_quality(
                test=test,
                oracle=oracle
            )
            
            result.quality_report = quality_report
            result.calculate_overall_score()
            
            # Extract specific metrics
            if quality_report.correctness_metrics:
                result.assertion_count = (
                    quality_report.correctness_metrics.valid_assertions +
                    quality_report.correctness_metrics.invalid_assertions
                )
                result.valid_assertions = quality_report.correctness_metrics.valid_assertions
                result.has_compilation_errors = quality_report.correctness_metrics.compilation_errors > 0
            
            if quality_report.readability_metrics:
                result.lines_of_code = quality_report.readability_metrics.lines_of_code
                result.cyclomatic_complexity = quality_report.readability_metrics.avg_method_complexity
            
            if quality_report.maintainability_metrics:
                result.code_duplication_ratio = quality_report.maintainability_metrics.duplication_percentage / 100.0
                result.code_smells_count = len(quality_report.maintainability_metrics.code_smells)
                result.has_code_smells = result.code_smells_count > 0
            
            # Check quality thresholds
            result.meets_quality_threshold = (
                result.correctness_score >= self.config.min_correctness_score and
                result.readability_score >= self.config.min_readability_score and
                result.maintainability_score >= self.config.min_maintainability_score and
                result.cyclomatic_complexity <= self.config.max_cyclomatic_complexity and
                result.code_duplication_ratio <= self.config.max_code_duplication
            )
            
        except Exception as e:
            result.error_message = str(e)
        
        end_time = datetime.utcnow()
        result.execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return result
    
    def get_summary(self) -> Dict:
        """Get summary of experiment results."""
        if not self.report.endpoint_results:
            return {"status": "No results available"}
        
        total = len(self.report.endpoint_results)
        meeting_threshold = sum(1 for r in self.report.endpoint_results if r.meets_quality_threshold)
        with_errors = sum(1 for r in self.report.endpoint_results if r.has_compilation_errors)
        with_smells = sum(1 for r in self.report.endpoint_results if r.has_code_smells)
        
        avg_quality = statistics.mean([r.overall_quality_score for r in self.report.endpoint_results])
        avg_correctness = statistics.mean([r.correctness_score for r in self.report.endpoint_results])
        avg_readability = statistics.mean([r.readability_score for r in self.report.endpoint_results])
        avg_maintainability = statistics.mean([r.maintainability_score for r in self.report.endpoint_results])
        
        return {
            "total_endpoints": total,
            "meeting_threshold": meeting_threshold,
            "pass_rate": meeting_threshold / total if total > 0 else 0.0,
            "with_compilation_errors": with_errors,
            "with_code_smells": with_smells,
            "average_scores": {
                "overall_quality": avg_quality,
                "correctness": avg_correctness,
                "readability": avg_readability,
                "maintainability": avg_maintainability
            },
            "llm_rankings": self.report.llm_rankings
        }
