"""
LLM Comparator Module (RQ4 - Comparaison des LLMs)

This module compares the performance of different LLMs (GPT-4, Claude, Gemini, 
Mistral, Llama) across all metrics to determine which performs best for contract
test generation.

Research Question 4: Quel LLM génère les meilleurs tests de contrat?

Comparison Dimensions:
- Oracle quality (precision, completeness)
- Code quality (correctness, readability, maintainability)
- Consistency (oracle-code alignment)
- Performance (speed, cost)
- Robustness (handling incomplete documentation)

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID
import statistics

from .oracle_metrics import OraclePrecisionMetrics
from .test_quality_analyzer import TestQualityReport
from .inconsistency_detector import InconsistencyReport


@dataclass
class LLMPerformanceMetrics:
    """Performance metrics for an LLM."""
    model_name: str
    
    # Oracle quality
    avg_oracle_precision: float = 0.0
    avg_oracle_recall: float = 0.0
    avg_oracle_f1: float = 0.0
    avg_oracle_completeness: float = 0.0
    avg_confidence_calibration: float = 0.0
    
    # Code quality
    avg_test_quality: float = 0.0
    avg_correctness: float = 0.0
    avg_readability: float = 0.0
    avg_maintainability: float = 0.0
    avg_best_practices: float = 0.0
    
    # Consistency
    avg_coherence_score: float = 0.0
    avg_oracle_alignment: float = 0.0
    total_inconsistencies: int = 0
    critical_inconsistencies: int = 0
    
    # Performance
    avg_oracle_time_ms: float = 0.0
    avg_code_gen_time_ms: float = 0.0
    avg_total_time_ms: float = 0.0
    avg_cost_per_test: float = 0.0
    
    # Robustness (with incomplete documentation)
    incomplete_doc_precision: float = 0.0
    incomplete_doc_quality: float = 0.0
    
    # Sample size
    num_tests: int = 0
    num_endpoints: int = 0
    
    # Metadata
    evaluated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LLMComparison:
    """Comparison results across multiple LLMs."""
    models: List[str]
    
    # Rankings (model name -> rank, 1 is best)
    oracle_quality_ranking: Dict[str, int] = field(default_factory=dict)
    code_quality_ranking: Dict[str, int] = field(default_factory=dict)
    consistency_ranking: Dict[str, int] = field(default_factory=dict)
    performance_ranking: Dict[str, int] = field(default_factory=dict)
    cost_ranking: Dict[str, int] = field(default_factory=dict)
    robustness_ranking: Dict[str, int] = field(default_factory=dict)
    overall_ranking: Dict[str, int] = field(default_factory=dict)
    
    # Scores (normalized 0-1)
    normalized_scores: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Statistical significance
    significant_differences: List[Tuple[str, str, str]] = field(default_factory=list)  # (model1, model2, dimension)
    
    # Best model per dimension
    best_for_oracle_quality: str = ""
    best_for_code_quality: str = ""
    best_for_consistency: str = ""
    best_for_performance: str = ""
    best_for_cost: str = ""
    best_for_robustness: str = ""
    best_overall: str = ""
    
    # Metadata
    compared_at: datetime = field(default_factory=datetime.utcnow)


class LLMComparator:
    """
    Compares performance of different LLMs for contract test generation (RQ4).
    
    Aggregates metrics from OracleMetrics, TestQualityAnalyzer, and 
    InconsistencyDetector to provide comprehensive comparison.
    """
    
    def __init__(self):
        self.llm_metrics: Dict[str, LLMPerformanceMetrics] = {}
    
    def add_oracle_metrics(
        self,
        model_name: str,
        metrics: List[OraclePrecisionMetrics],
        time_ms: Optional[List[float]] = None
    ) -> None:
        """
        Add oracle metrics for an LLM.
        
        Args:
            model_name: Name of the LLM
            metrics: List of oracle precision metrics
            time_ms: Optional list of generation times in milliseconds
        """
        if model_name not in self.llm_metrics:
            self.llm_metrics[model_name] = LLMPerformanceMetrics(model_name=model_name)
        
        llm = self.llm_metrics[model_name]
        n = len(metrics)
        
        if n > 0:
            llm.avg_oracle_precision = sum(m.precision for m in metrics) / n
            llm.avg_oracle_recall = sum(m.recall for m in metrics) / n
            llm.avg_oracle_f1 = sum(m.f1_score for m in metrics) / n
            llm.avg_oracle_completeness = sum(m.completeness_score for m in metrics) / n
            llm.avg_confidence_calibration = sum(m.confidence_calibration_error for m in metrics) / n
            llm.num_endpoints = n
        
        if time_ms:
            llm.avg_oracle_time_ms = sum(time_ms) / len(time_ms)
    
    def add_quality_metrics(
        self,
        model_name: str,
        reports: List[TestQualityReport],
        time_ms: Optional[List[float]] = None
    ) -> None:
        """
        Add test quality metrics for an LLM.
        
        Args:
            model_name: Name of the LLM
            reports: List of test quality reports
            time_ms: Optional list of generation times in milliseconds
        """
        if model_name not in self.llm_metrics:
            self.llm_metrics[model_name] = LLMPerformanceMetrics(model_name=model_name)
        
        llm = self.llm_metrics[model_name]
        n = len(reports)
        
        if n > 0:
            llm.avg_test_quality = sum(r.overall_quality_score for r in reports) / n
            llm.avg_correctness = sum(r.correctness_metrics.correctness_score for r in reports) / n
            llm.avg_readability = sum(r.readability_metrics.readability_score for r in reports) / n
            llm.avg_maintainability = sum(r.maintainability_metrics.maintainability_score for r in reports) / n
            llm.avg_best_practices = sum(r.best_practices_metrics.best_practices_score for r in reports) / n
            llm.avg_oracle_alignment = sum(r.oracle_alignment_score for r in reports if r.oracle_alignment_score > 0) / max(1, sum(1 for r in reports if r.oracle_alignment_score > 0))
            llm.num_tests = n
        
        if time_ms:
            llm.avg_code_gen_time_ms = sum(time_ms) / len(time_ms)
            llm.avg_total_time_ms = llm.avg_oracle_time_ms + llm.avg_code_gen_time_ms
    
    def add_consistency_metrics(
        self,
        model_name: str,
        reports: List[InconsistencyReport]
    ) -> None:
        """
        Add consistency metrics for an LLM.
        
        Args:
            model_name: Name of the LLM
            reports: List of inconsistency reports
        """
        if model_name not in self.llm_metrics:
            self.llm_metrics[model_name] = LLMPerformanceMetrics(model_name=model_name)
        
        llm = self.llm_metrics[model_name]
        n = len(reports)
        
        if n > 0:
            llm.avg_coherence_score = sum(r.coherence_score for r in reports) / n
            llm.total_inconsistencies = sum(r.total_inconsistencies for r in reports)
            llm.critical_inconsistencies = sum(len(r.critical) for r in reports)
    
    def add_cost_metrics(
        self,
        model_name: str,
        costs: List[float]
    ) -> None:
        """
        Add cost metrics for an LLM.
        
        Args:
            model_name: Name of the LLM
            costs: List of costs per test in USD
        """
        if model_name not in self.llm_metrics:
            self.llm_metrics[model_name] = LLMPerformanceMetrics(model_name=model_name)
        
        llm = self.llm_metrics[model_name]
        if costs:
            llm.avg_cost_per_test = sum(costs) / len(costs)
    
    def add_robustness_metrics(
        self,
        model_name: str,
        incomplete_doc_precision: float,
        incomplete_doc_quality: float
    ) -> None:
        """
        Add robustness metrics (performance with incomplete documentation).
        
        Args:
            model_name: Name of the LLM
            incomplete_doc_precision: Oracle precision with incomplete docs
            incomplete_doc_quality: Test quality with incomplete docs
        """
        if model_name not in self.llm_metrics:
            self.llm_metrics[model_name] = LLMPerformanceMetrics(model_name=model_name)
        
        llm = self.llm_metrics[model_name]
        llm.incomplete_doc_precision = incomplete_doc_precision
        llm.incomplete_doc_quality = incomplete_doc_quality
    
    def compare_models(self) -> LLMComparison:
        """
        Compare all LLMs across all dimensions.
        
        Returns:
            LLMComparison with rankings and best models
        """
        models = list(self.llm_metrics.keys())
        
        if not models:
            return LLMComparison(models=[])
        
        comparison = LLMComparison(models=models)
        
        # Calculate rankings for each dimension
        comparison.oracle_quality_ranking = self._rank_by_oracle_quality()
        comparison.code_quality_ranking = self._rank_by_code_quality()
        comparison.consistency_ranking = self._rank_by_consistency()
        comparison.performance_ranking = self._rank_by_performance()
        comparison.cost_ranking = self._rank_by_cost()
        comparison.robustness_ranking = self._rank_by_robustness()
        
        # Calculate overall ranking (weighted average of ranks)
        comparison.overall_ranking = self._calculate_overall_ranking(comparison)
        
        # Normalize scores
        comparison.normalized_scores = self._normalize_scores()
        
        # Identify best models
        comparison.best_for_oracle_quality = self._get_best_model(comparison.oracle_quality_ranking)
        comparison.best_for_code_quality = self._get_best_model(comparison.code_quality_ranking)
        comparison.best_for_consistency = self._get_best_model(comparison.consistency_ranking)
        comparison.best_for_performance = self._get_best_model(comparison.performance_ranking)
        comparison.best_for_cost = self._get_best_model(comparison.cost_ranking)
        comparison.best_for_robustness = self._get_best_model(comparison.robustness_ranking)
        comparison.best_overall = self._get_best_model(comparison.overall_ranking)
        
        # Statistical significance (simplified)
        comparison.significant_differences = self._detect_significant_differences()
        
        return comparison
    
    def get_model_metrics(self, model_name: str) -> Optional[LLMPerformanceMetrics]:
        """Get metrics for a specific model."""
        return self.llm_metrics.get(model_name)
    
    def generate_comparison_report(self, comparison: LLMComparison) -> str:
        """
        Generate a human-readable comparison report.
        
        Args:
            comparison: LLMComparison object
        
        Returns:
            Formatted string report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("LLM COMPARISON REPORT (RQ4)")
        lines.append("=" * 80)
        lines.append("")
        
        # Overall rankings
        lines.append("OVERALL RANKINGS:")
        for model, rank in sorted(comparison.overall_ranking.items(), key=lambda x: x[1]):
            metrics = self.llm_metrics[model]
            lines.append(f"  {rank}. {model}")
            lines.append(f"     Tests: {metrics.num_tests}, Endpoints: {metrics.num_endpoints}")
            lines.append(f"     Oracle F1: {metrics.avg_oracle_f1:.3f}, Test Quality: {metrics.avg_test_quality:.3f}")
            lines.append(f"     Coherence: {metrics.avg_coherence_score:.3f}, Time: {metrics.avg_total_time_ms:.1f}ms")
        lines.append("")
        
        # Best models per dimension
        lines.append("BEST MODELS BY DIMENSION:")
        lines.append(f"  Oracle Quality:  {comparison.best_for_oracle_quality}")
        lines.append(f"  Code Quality:    {comparison.best_for_code_quality}")
        lines.append(f"  Consistency:     {comparison.best_for_consistency}")
        lines.append(f"  Performance:     {comparison.best_for_performance}")
        lines.append(f"  Cost:            {comparison.best_for_cost}")
        lines.append(f"  Robustness:      {comparison.best_for_robustness}")
        lines.append(f"  Overall:         {comparison.best_overall}")
        lines.append("")
        
        # Detailed metrics table
        lines.append("DETAILED METRICS:")
        lines.append(f"{'Model':<15} {'OracleF1':<10} {'TestQual':<10} {'Coherence':<10} {'Time(ms)':<10} {'Cost($)':<10}")
        lines.append("-" * 80)
        
        for model in comparison.models:
            metrics = self.llm_metrics[model]
            lines.append(
                f"{model:<15} "
                f"{metrics.avg_oracle_f1:<10.3f} "
                f"{metrics.avg_test_quality:<10.3f} "
                f"{metrics.avg_coherence_score:<10.3f} "
                f"{metrics.avg_total_time_ms:<10.1f} "
                f"{metrics.avg_cost_per_test:<10.4f}"
            )
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    # Private helper methods
    
    def _rank_by_oracle_quality(self) -> Dict[str, int]:
        """Rank models by oracle quality (F1 score)."""
        scores = {model: metrics.avg_oracle_f1 for model, metrics in self.llm_metrics.items()}
        return self._rank_dict(scores, higher_is_better=True)
    
    def _rank_by_code_quality(self) -> Dict[str, int]:
        """Rank models by code quality."""
        scores = {model: metrics.avg_test_quality for model, metrics in self.llm_metrics.items()}
        return self._rank_dict(scores, higher_is_better=True)
    
    def _rank_by_consistency(self) -> Dict[str, int]:
        """Rank models by consistency (coherence score)."""
        scores = {model: metrics.avg_coherence_score for model, metrics in self.llm_metrics.items()}
        return self._rank_dict(scores, higher_is_better=True)
    
    def _rank_by_performance(self) -> Dict[str, int]:
        """Rank models by performance (speed)."""
        scores = {model: metrics.avg_total_time_ms for model, metrics in self.llm_metrics.items()}
        return self._rank_dict(scores, higher_is_better=False)
    
    def _rank_by_cost(self) -> Dict[str, int]:
        """Rank models by cost (lower is better)."""
        scores = {model: metrics.avg_cost_per_test for model, metrics in self.llm_metrics.items()}
        return self._rank_dict(scores, higher_is_better=False)
    
    def _rank_by_robustness(self) -> Dict[str, int]:
        """Rank models by robustness (incomplete doc handling)."""
        # Combine incomplete doc precision and quality
        scores = {
            model: (metrics.incomplete_doc_precision + metrics.incomplete_doc_quality) / 2
            for model, metrics in self.llm_metrics.items()
        }
        return self._rank_dict(scores, higher_is_better=True)
    
    def _calculate_overall_ranking(self, comparison: LLMComparison) -> Dict[str, int]:
        """
        Calculate overall ranking as weighted average of dimension ranks.
        
        Weights:
        - Oracle Quality: 30%
        - Code Quality: 25%
        - Consistency: 20%
        - Performance: 10%
        - Cost: 10%
        - Robustness: 5%
        """
        weighted_scores = {}
        
        for model in comparison.models:
            score = (
                comparison.oracle_quality_ranking[model] * 0.30 +
                comparison.code_quality_ranking[model] * 0.25 +
                comparison.consistency_ranking[model] * 0.20 +
                comparison.performance_ranking[model] * 0.10 +
                comparison.cost_ranking[model] * 0.10 +
                comparison.robustness_ranking[model] * 0.05
            )
            weighted_scores[model] = score
        
        return self._rank_dict(weighted_scores, higher_is_better=False)  # Lower weighted score is better
    
    def _rank_dict(self, scores: Dict[str, float], higher_is_better: bool = True) -> Dict[str, int]:
        """
        Rank dictionary by values.
        
        Args:
            scores: Dict mapping keys to scores
            higher_is_better: If True, higher scores get better ranks
        
        Returns:
            Dict mapping keys to ranks (1 is best)
        """
        if not scores:
            return {}
        
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=higher_is_better)
        
        ranks = {}
        current_rank = 1
        prev_score = None
        
        for i, (model, score) in enumerate(sorted_items):
            if prev_score is not None and score != prev_score:
                current_rank = i + 1
            ranks[model] = current_rank
            prev_score = score
        
        return ranks
    
    def _get_best_model(self, ranking: Dict[str, int]) -> str:
        """Get the model with rank 1."""
        for model, rank in ranking.items():
            if rank == 1:
                return model
        return ""
    
    def _normalize_scores(self) -> Dict[str, Dict[str, float]]:
        """
        Normalize all scores to 0-1 range for comparison.
        
        Returns:
            Dict mapping model name to dict of normalized scores
        """
        normalized = {}
        
        for model, metrics in self.llm_metrics.items():
            normalized[model] = {
                "oracle_f1": metrics.avg_oracle_f1,
                "oracle_precision": metrics.avg_oracle_precision,
                "oracle_recall": metrics.avg_oracle_recall,
                "oracle_completeness": metrics.avg_oracle_completeness,
                "test_quality": metrics.avg_test_quality,
                "correctness": metrics.avg_correctness,
                "readability": metrics.avg_readability,
                "maintainability": metrics.avg_maintainability,
                "best_practices": metrics.avg_best_practices,
                "coherence": metrics.avg_coherence_score,
                "oracle_alignment": metrics.avg_oracle_alignment,
            }
        
        return normalized
    
    def _detect_significant_differences(self) -> List[Tuple[str, str, str]]:
        """
        Detect statistically significant differences between models.
        
        Simplified: just checks if difference is > 0.1 (10%)
        
        Returns:
            List of (model1, model2, dimension) tuples
        """
        significant = []
        models = list(self.llm_metrics.keys())
        
        for i, model1 in enumerate(models):
            for model2 in models[i+1:]:
                m1 = self.llm_metrics[model1]
                m2 = self.llm_metrics[model2]
                
                # Oracle quality
                if abs(m1.avg_oracle_f1 - m2.avg_oracle_f1) > 0.1:
                    significant.append((model1, model2, "oracle_quality"))
                
                # Test quality
                if abs(m1.avg_test_quality - m2.avg_test_quality) > 0.1:
                    significant.append((model1, model2, "test_quality"))
                
                # Consistency
                if abs(m1.avg_coherence_score - m2.avg_coherence_score) > 0.1:
                    significant.append((model1, model2, "consistency"))
        
        return significant
    
    def export_to_csv(self, filename: str) -> None:
        """Export comparison data to CSV for further analysis."""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                "Model", "NumTests", "NumEndpoints",
                "OraclePrecision", "OracleRecall", "OracleF1", "OracleCompleteness",
                "TestQuality", "Correctness", "Readability", "Maintainability", "BestPractices",
                "CoherenceScore", "OracleAlignment", "TotalInconsistencies", "CriticalInconsistencies",
                "OracleTimeMs", "CodeGenTimeMs", "TotalTimeMs", "CostPerTest",
                "IncompleteDocPrecision", "IncompleteDocQuality"
            ])
            
            # Data rows
            for model, metrics in self.llm_metrics.items():
                writer.writerow([
                    model, metrics.num_tests, metrics.num_endpoints,
                    metrics.avg_oracle_precision, metrics.avg_oracle_recall,
                    metrics.avg_oracle_f1, metrics.avg_oracle_completeness,
                    metrics.avg_test_quality, metrics.avg_correctness,
                    metrics.avg_readability, metrics.avg_maintainability,
                    metrics.avg_best_practices, metrics.avg_coherence_score,
                    metrics.avg_oracle_alignment, metrics.total_inconsistencies,
                    metrics.critical_inconsistencies, metrics.avg_oracle_time_ms,
                    metrics.avg_code_gen_time_ms, metrics.avg_total_time_ms,
                    metrics.avg_cost_per_test, metrics.incomplete_doc_precision,
                    metrics.incomplete_doc_quality
                ])
