"""
RQ4 LLM Comparison Experiments - Multi-Model Performance Analysis

Research Question 4: Comment les différents LLMs se comparent-ils dans la génération de tests?

This module implements comprehensive experiments to compare the performance of
different Large Language Models (LLMs) across all quality dimensions: oracle generation,
code generation, consistency, quality, and cost-effectiveness.

Comparison Dimensions:
- Oracle Quality: Precision, recall, F1 score
- Code Quality: Correctness, readability, maintainability
- Consistency: Oracle-code coherence
- Performance: Generation time, token usage
- Cost-Effectiveness: Quality per dollar spent
- Robustness: Performance with incomplete documentation

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import asyncio
import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from src.shared_context.models import EndpointContext, GeneratedTest, Oracle
from src.validation.llm_comparator import (
    LLMComparator,
    LLMComparisonReport,
    LLMPerformanceMetrics
)


@dataclass
class LLMComparisonConfig:
    """Configuration for RQ4 LLM comparison experiments."""
    experiment_id: str
    name: str
    description: str
    llm_models: List[str]
    num_endpoints: int = 0
    
    # Comparison dimensions
    compare_oracle_quality: bool = True
    compare_code_quality: bool = True
    compare_consistency: bool = True
    compare_performance: bool = True
    compare_cost: bool = True
    compare_robustness: bool = True
    
    # Cost per 1M tokens (USD) - approximate values
    token_costs: Dict[str, Tuple[float, float]] = field(default_factory=lambda: {
        "gpt-4": (30.0, 60.0),  # (input, output)
        "gpt-4-turbo": (10.0, 30.0),
        "claude-3-opus": (15.0, 75.0),
        "claude-3-sonnet": (3.0, 15.0),
        "gemini-pro": (0.5, 1.5),
        "mistral-large": (4.0, 12.0),
        "llama-3-70b": (0.0, 0.0),  # local/free
    })
    
    output_dir: Path = Path("experiments/results/rq4")
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "llm_models": self.llm_models,
            "num_endpoints": self.num_endpoints,
            "comparison_dimensions": {
                "oracle_quality": self.compare_oracle_quality,
                "code_quality": self.compare_code_quality,
                "consistency": self.compare_consistency,
                "performance": self.compare_performance,
                "cost": self.compare_cost,
                "robustness": self.compare_robustness
            },
            "token_costs": {
                model: {"input": costs[0], "output": costs[1]}
                for model, costs in self.token_costs.items()
            },
            "output_dir": str(self.output_dir)
        }


@dataclass
class ModelPerformanceResult:
    """Performance results for a single LLM model."""
    llm_model: str
    
    # Oracle generation metrics
    oracle_precision: float = 0.0
    oracle_recall: float = 0.0
    oracle_f1: float = 0.0
    oracle_confidence_avg: float = 0.0
    
    # Code quality metrics
    code_correctness: float = 0.0
    code_readability: float = 0.0
    code_maintainability: float = 0.0
    code_overall_quality: float = 0.0
    
    # Consistency metrics
    coherence_score: float = 0.0
    java_coverage_ratio: float = 0.0
    gherkin_coverage_ratio: float = 0.0
    inconsistency_count: int = 0
    
    # Performance metrics
    avg_generation_time_ms: float = 0.0
    avg_input_tokens: float = 0.0
    avg_output_tokens: float = 0.0
    total_generation_time_ms: float = 0.0
    
    # Cost metrics
    total_cost_usd: float = 0.0
    cost_per_endpoint_usd: float = 0.0
    cost_per_test_usd: float = 0.0
    
    # Robustness metrics (with incomplete documentation)
    robustness_score: float = 0.0
    quality_degradation_rate: float = 0.0  # Quality drop per 10% documentation loss
    
    # Success rates
    successful_generations: int = 0
    total_attempts: int = 0
    success_rate: float = 0.0
    
    # Overall ranking score
    overall_score: float = 0.0
    
    def calculate_overall_score(self):
        """
        Calculate overall ranking score as weighted average of all dimensions.
        
        Weights:
        - Oracle quality: 25%
        - Code quality: 25%
        - Consistency: 20%
        - Performance: 10%
        - Cost-effectiveness: 10%
        - Robustness: 10%
        """
        oracle_score = (self.oracle_precision + self.oracle_recall + self.oracle_f1) / 3.0
        code_score = self.code_overall_quality
        consistency_score = self.coherence_score
        
        # Normalize performance (lower is better, so invert)
        # Assume max acceptable time is 10 seconds
        performance_score = max(0.0, 1.0 - (self.avg_generation_time_ms / 10000.0))
        
        # Normalize cost (lower is better, so invert)
        # Assume max acceptable cost per endpoint is $0.50
        cost_score = max(0.0, 1.0 - (self.cost_per_endpoint_usd / 0.50))
        
        robustness_score = self.robustness_score
        
        self.overall_score = (
            oracle_score * 0.25 +
            code_score * 0.25 +
            consistency_score * 0.20 +
            performance_score * 0.10 +
            cost_score * 0.10 +
            robustness_score * 0.10
        )

    def calculate_normalized_performance(self, max_time_ms: float = 10000.0) -> float:
        """Return normalized performance score in [0,1] (higher is better)."""
        if max_time_ms <= 0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - (self.avg_generation_time_ms / max_time_ms)))

    def calculate_normalized_cost(self, max_cost_per_endpoint_usd: float = 0.50) -> float:
        """Return normalized cost score in [0,1] (higher is better)."""
        if max_cost_per_endpoint_usd <= 0:
            return 0.0

        cost_per_endpoint = self.cost_per_endpoint_usd
        if cost_per_endpoint <= 0.0 and self.total_cost_usd > 0.0:
            # Best-effort fallback when cost_per_endpoint wasn't computed.
            denom = float(self.total_attempts or self.successful_generations or 1)
            cost_per_endpoint = self.total_cost_usd / denom

        return max(0.0, min(1.0, 1.0 - (cost_per_endpoint / max_cost_per_endpoint_usd)))
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            "llm_model": self.llm_model,
            "oracle_metrics": {
                "precision": self.oracle_precision,
                "recall": self.oracle_recall,
                "f1": self.oracle_f1,
                "confidence_avg": self.oracle_confidence_avg
            },
            "code_quality_metrics": {
                "correctness": self.code_correctness,
                "readability": self.code_readability,
                "maintainability": self.code_maintainability,
                "overall": self.code_overall_quality
            },
            "consistency_metrics": {
                "coherence_score": self.coherence_score,
                "java_coverage": self.java_coverage_ratio,
                "gherkin_coverage": self.gherkin_coverage_ratio,
                "inconsistency_count": self.inconsistency_count
            },
            "performance_metrics": {
                "avg_generation_time_ms": self.avg_generation_time_ms,
                "avg_input_tokens": self.avg_input_tokens,
                "avg_output_tokens": self.avg_output_tokens,
                "total_generation_time_ms": self.total_generation_time_ms
            },
            "cost_metrics": {
                "total_cost_usd": self.total_cost_usd,
                "cost_per_endpoint_usd": self.cost_per_endpoint_usd,
                "cost_per_test_usd": self.cost_per_test_usd
            },
            "robustness_metrics": {
                "robustness_score": self.robustness_score,
                "quality_degradation_rate": self.quality_degradation_rate
            },
            "success_metrics": {
                "successful_generations": self.successful_generations,
                "total_attempts": self.total_attempts,
                "success_rate": self.success_rate
            },
            "overall_score": self.overall_score
        }


@dataclass
class LLMComparisonExperimentReport:
    """Aggregate report for RQ4 LLM comparison experiments."""
    experiment_id: str
    config: LLMComparisonConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    # Results per model
    model_results: List[ModelPerformanceResult] = field(default_factory=list)
    
    # Rankings
    overall_rankings: Dict[str, int] = field(default_factory=dict)
    oracle_quality_rankings: Dict[str, int] = field(default_factory=dict)
    code_quality_rankings: Dict[str, int] = field(default_factory=dict)
    consistency_rankings: Dict[str, int] = field(default_factory=dict)
    performance_rankings: Dict[str, int] = field(default_factory=dict)
    cost_rankings: Dict[str, int] = field(default_factory=dict)
    robustness_rankings: Dict[str, int] = field(default_factory=dict)
    
    # Statistical comparisons
    statistical_significance: Dict[str, Dict[str, bool]] = field(default_factory=dict)
    effect_sizes: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Best model per dimension
    best_for_oracle_quality: str = ""
    best_for_code_quality: str = ""
    best_for_consistency: str = ""
    best_for_performance: str = ""
    best_for_cost: str = ""
    best_for_robustness: str = ""
    best_overall: str = ""
    
    def calculate_rankings(self):
        """Calculate rankings for each dimension."""
        if not self.model_results:
            return
        
        # Overall rankings
        overall_scores = [(r.llm_model, r.overall_score) for r in self.model_results]
        overall_scores.sort(key=lambda x: x[1], reverse=True)
        self.overall_rankings = {model: rank + 1 for rank, (model, _) in enumerate(overall_scores)}
        self.best_overall = overall_scores[0][0] if overall_scores else ""
        
        # Oracle quality rankings
        oracle_scores = [(r.llm_model, r.oracle_f1) for r in self.model_results]
        oracle_scores.sort(key=lambda x: x[1], reverse=True)
        self.oracle_quality_rankings = {model: rank + 1 for rank, (model, _) in enumerate(oracle_scores)}
        self.best_for_oracle_quality = oracle_scores[0][0] if oracle_scores else ""
        
        # Code quality rankings
        code_scores = [(r.llm_model, r.code_overall_quality) for r in self.model_results]
        code_scores.sort(key=lambda x: x[1], reverse=True)
        self.code_quality_rankings = {model: rank + 1 for rank, (model, _) in enumerate(code_scores)}
        self.best_for_code_quality = code_scores[0][0] if code_scores else ""
        
        # Consistency rankings
        consistency_scores = [(r.llm_model, r.coherence_score) for r in self.model_results]
        consistency_scores.sort(key=lambda x: x[1], reverse=True)
        self.consistency_rankings = {model: rank + 1 for rank, (model, _) in enumerate(consistency_scores)}
        self.best_for_consistency = consistency_scores[0][0] if consistency_scores else ""
        
        # Performance rankings (lower time is better)
        performance_scores = [(r.llm_model, r.avg_generation_time_ms) for r in self.model_results]
        performance_scores.sort(key=lambda x: x[1])  # ascending
        self.performance_rankings = {model: rank + 1 for rank, (model, _) in enumerate(performance_scores)}
        self.best_for_performance = performance_scores[0][0] if performance_scores else ""
        
        # Cost rankings (lower cost is better)
        cost_scores = [(r.llm_model, r.cost_per_endpoint_usd) for r in self.model_results]
        cost_scores.sort(key=lambda x: x[1])  # ascending
        self.cost_rankings = {model: rank + 1 for rank, (model, _) in enumerate(cost_scores)}
        self.best_for_cost = cost_scores[0][0] if cost_scores else ""
        
        # Robustness rankings
        robustness_scores = [(r.llm_model, r.robustness_score) for r in self.model_results]
        robustness_scores.sort(key=lambda x: x[1], reverse=True)
        self.robustness_rankings = {model: rank + 1 for rank, (model, _) in enumerate(robustness_scores)}
        self.best_for_robustness = robustness_scores[0][0] if robustness_scores else ""
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        by_model = {r.llm_model: r for r in self.model_results}

        induction_best = self.best_for_oracle_quality
        generation_best = self.best_for_code_quality
        coherence_best = self.best_for_consistency

        return {
            "experiment_id": self.experiment_id,
            "config": self.config.to_dict(),
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "model_results": [r.to_dict() for r in self.model_results],
            "rq4_answer": {
                "induction": {
                    "metric": "oracle_f1",
                    "best_model": induction_best,
                    "best_score": by_model.get(induction_best).oracle_f1 if induction_best in by_model else None,
                },
                "generation": {
                    "metric": "code_overall_quality",
                    "best_model": generation_best,
                    "best_score": by_model.get(generation_best).code_overall_quality if generation_best in by_model else None,
                },
                "coherence": {
                    "metric": "coherence_score",
                    "best_model": coherence_best,
                    "best_score": by_model.get(coherence_best).coherence_score if coherence_best in by_model else None,
                },
            },
            "rankings": {
                "overall": self.overall_rankings,
                "oracle_quality": self.oracle_quality_rankings,
                "code_quality": self.code_quality_rankings,
                "consistency": self.consistency_rankings,
                "performance": self.performance_rankings,
                "cost": self.cost_rankings,
                "robustness": self.robustness_rankings
            },
            "best_models": {
                "overall": self.best_overall,
                "oracle_quality": self.best_for_oracle_quality,
                "code_quality": self.best_for_code_quality,
                "consistency": self.best_for_consistency,
                "performance": self.best_for_performance,
                "cost": self.best_for_cost,
                "robustness": self.best_for_robustness
            },
            "statistical_significance": self.statistical_significance,
            "effect_sizes": self.effect_sizes
        }
    
    def save(self) -> Path:
        """Save report to JSON file."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.config.output_dir / f"rq4_report_{self.experiment_id}.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ4ExperimentRunner:
    """Main runner for RQ4 LLM comparison experiments."""
    
    def __init__(self, config: LLMComparisonConfig):
        """Initialize experiment runner."""
        self.config = config
        self.comparator = LLMComparator()
        self.report = LLMComparisonExperimentReport(
            experiment_id=config.experiment_id,
            config=config,
            started_at=datetime.utcnow()
        )
    
    async def run_experiment(
        self,
        endpoints: List[EndpointContext],
        results_by_model: Dict[str, Dict[str, any]]
    ) -> LLMComparisonExperimentReport:
        """
        Run LLM comparison experiment.
        
        Args:
            endpoints: List of endpoints evaluated
            results_by_model: Dictionary mapping model name to its results
                Expected keys per model: 'oracles', 'tests', 'quality_reports',
                'consistency_reports', 'performance_metrics'
        
        Returns:
            LLMComparisonExperimentReport with comparative results
        """
        # Analyze each model's performance
        for model_name in self.config.llm_models:
            if model_name not in results_by_model:
                continue
            
            model_data = results_by_model[model_name]
            result = await self._analyze_model_performance(
                model_name,
                endpoints,
                model_data
            )
            self.report.model_results.append(result)
        
        # Calculate rankings
        self.report.calculate_rankings()
        self.report.completed_at = datetime.utcnow()
        
        return self.report
    
    async def _analyze_model_performance(
        self,
        model_name: str,
        endpoints: List[EndpointContext],
        model_data: Dict[str, any]
    ) -> ModelPerformanceResult:
        """Analyze performance for a single LLM model."""
        result = ModelPerformanceResult(llm_model=model_name)
        
        try:
            # Extract oracle metrics
            oracles = model_data.get('oracles', [])
            if oracles:
                precisions = [o.get('precision', 0.0) for o in oracles]
                recalls = [o.get('recall', 0.0) for o in oracles]
                f1s = [o.get('f1', 0.0) for o in oracles]
                confidences = [o.get('confidence', 0.0) for o in oracles]
                
                result.oracle_precision = statistics.mean(precisions) if precisions else 0.0
                result.oracle_recall = statistics.mean(recalls) if recalls else 0.0
                result.oracle_f1 = statistics.mean(f1s) if f1s else 0.0
                result.oracle_confidence_avg = statistics.mean(confidences) if confidences else 0.0
            
            # Extract code quality metrics
            quality_reports = model_data.get('quality_reports', [])
            if quality_reports:
                correctness = [q.get('correctness', 0.0) for q in quality_reports]
                readability = [q.get('readability', 0.0) for q in quality_reports]
                maintainability = [q.get('maintainability', 0.0) for q in quality_reports]
                overall = [q.get('overall', 0.0) for q in quality_reports]
                
                result.code_correctness = statistics.mean(correctness) if correctness else 0.0
                result.code_readability = statistics.mean(readability) if readability else 0.0
                result.code_maintainability = statistics.mean(maintainability) if maintainability else 0.0
                result.code_overall_quality = statistics.mean(overall) if overall else 0.0
            
            # Extract consistency metrics
            consistency_reports = model_data.get('consistency_reports', [])
            if consistency_reports:
                coherence = [c.get('coherence_score', 0.0) for c in consistency_reports]
                java_cov = [c.get('java_coverage', 0.0) for c in consistency_reports]
                gherkin_cov = [c.get('gherkin_coverage', 0.0) for c in consistency_reports]
                inconsistencies = [c.get('inconsistency_count', 0) for c in consistency_reports]
                
                result.coherence_score = statistics.mean(coherence) if coherence else 0.0
                result.java_coverage_ratio = statistics.mean(java_cov) if java_cov else 0.0
                result.gherkin_coverage_ratio = statistics.mean(gherkin_cov) if gherkin_cov else 0.0
                result.inconsistency_count = int(statistics.mean(inconsistencies)) if inconsistencies else 0
            
            # Extract performance metrics
            perf_metrics = model_data.get('performance_metrics', {})
            result.avg_generation_time_ms = perf_metrics.get('avg_generation_time_ms', 0.0)
            result.avg_input_tokens = perf_metrics.get('avg_input_tokens', 0.0)
            result.avg_output_tokens = perf_metrics.get('avg_output_tokens', 0.0)
            result.total_generation_time_ms = perf_metrics.get('total_generation_time_ms', 0.0)
            
            # Calculate cost metrics
            if model_name in self.config.token_costs:
                input_cost, output_cost = self.config.token_costs[model_name]
                total_input_cost = (result.avg_input_tokens * len(endpoints) * input_cost) / 1_000_000
                total_output_cost = (result.avg_output_tokens * len(endpoints) * output_cost) / 1_000_000
                result.total_cost_usd = total_input_cost + total_output_cost
                result.cost_per_endpoint_usd = result.total_cost_usd / len(endpoints) if endpoints else 0.0
                result.cost_per_test_usd = result.cost_per_endpoint_usd  # Assuming one test per endpoint
            
            # Extract robustness metrics
            robustness_data = model_data.get('robustness_metrics', {})
            result.robustness_score = robustness_data.get('robustness_score', 0.0)
            result.quality_degradation_rate = robustness_data.get('degradation_rate', 0.0)
            
            # Extract success metrics
            result.successful_generations = model_data.get('successful_generations', 0)
            result.total_attempts = len(endpoints)
            result.success_rate = result.successful_generations / result.total_attempts if result.total_attempts > 0 else 0.0
            
            # Calculate overall score
            result.calculate_overall_score()
            
        except Exception as e:
            print(f"Error analyzing {model_name}: {e}")
        
        return result
    
    def get_summary(self) -> Dict:
        """Get summary of comparison results."""
        if not self.report.model_results:
            return {"status": "No results available"}
        
        return {
            "models_compared": len(self.report.model_results),
            "best_overall": self.report.best_overall,
            "best_for_oracle_quality": self.report.best_for_oracle_quality,
            "best_for_code_quality": self.report.best_for_code_quality,
            "best_for_consistency": self.report.best_for_consistency,
            "best_for_performance": self.report.best_for_performance,
            "best_for_cost": self.report.best_for_cost,
            "best_for_robustness": self.report.best_for_robustness,
            "overall_rankings": self.report.overall_rankings
        }
