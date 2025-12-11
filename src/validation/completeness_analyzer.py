"""
Completeness Analyzer Module (RQ5 - Impact de la Complétude de la Documentation)

This module analyzes the impact of documentation completeness on the quality
of generated oracles and test code. It correlates documentation completeness
scores with oracle precision and test quality.

Research Question 5: Comment la complétude de la documentation impacte-t-elle 
la qualité des tests générés?

Analysis:
- Correlation between documentation completeness and oracle precision
- Impact on test quality (correctness, coverage)
- Identification of critical missing information
- Degradation patterns with incomplete documentation

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID
import statistics

from ..shared_context.models import EndpointContext, Oracle, GeneratedTest
from .oracle_metrics import OraclePrecisionMetrics
from .test_quality_analyzer import TestQualityReport


class CompletenessCategory(str):
    """Categories of documentation completeness."""
    COMPLETE = "complete"  # 80-100%
    MOSTLY_COMPLETE = "mostly_complete"  # 60-79%
    PARTIAL = "partial"  # 40-59%
    INCOMPLETE = "incomplete"  # 20-39%
    MINIMAL = "minimal"  # 0-19%


@dataclass
class CompletenessImpactMetrics:
    """Metrics for impact of documentation completeness."""
    completeness_score: float  # 0.0 to 1.0
    category: str
    
    # Oracle quality impact
    oracle_precision: float
    oracle_recall: float
    oracle_f1: float
    oracle_confidence: float
    
    # Test quality impact
    test_quality_score: float
    test_correctness: float
    assertion_count: int
    
    # Missing elements impact
    missing_status_code: bool = False
    missing_headers: List[str] = field(default_factory=list)
    missing_schema: bool = False
    missing_examples: bool = False
    
    # Degradation vs complete
    precision_drop: Optional[float] = None
    quality_drop: Optional[float] = None
    
    # Metadata
    endpoint_id: UUID = None
    llm_model: str = ""


@dataclass
class CompletenessAnalysisReport:
    """Report analyzing completeness impact across multiple endpoints."""
    
    # Correlation analysis
    completeness_precision_correlation: float  # -1 to 1
    completeness_quality_correlation: float
    completeness_confidence_correlation: float
    
    # By category
    metrics_by_category: Dict[str, List[CompletenessImpactMetrics]] = field(default_factory=dict)
    avg_by_category: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Critical thresholds
    min_completeness_for_good_quality: float = 0.0  # Min completeness for quality > 0.8
    min_completeness_for_good_precision: float = 0.0  # Min completeness for precision > 0.8
    
    # Missing elements frequency
    missing_elements_frequency: Dict[str, int] = field(default_factory=dict)
    
    # Degradation analysis
    avg_precision_drop_per_10pct: float = 0.0  # Avg precision drop per 10% completeness decrease
    avg_quality_drop_per_10pct: float = 0.0
    
    # Statistical significance
    correlation_p_value: Optional[float] = None
    
    # Sample size
    total_endpoints: int = 0
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.utcnow)


class CompletenessAnalyzer:
    """
    Analyzes the impact of documentation completeness on test quality (RQ5).
    
    Correlates documentation completeness with oracle precision and test quality
    to determine minimum required documentation level for good results.
    """
    
    def __init__(self):
        self.metrics: List[CompletenessImpactMetrics] = []
        
        # Baseline (complete documentation metrics)
        self.baseline_precision: Optional[float] = None
        self.baseline_quality: Optional[float] = None
    
    def add_endpoint_metrics(
        self,
        endpoint: EndpointContext,
        oracle: Oracle,
        oracle_metrics: OraclePrecisionMetrics,
        test: GeneratedTest,
        test_quality: TestQualityReport
    ) -> None:
        """
        Add metrics for an endpoint.
        
        Args:
            endpoint: Endpoint context with completeness score
            oracle: Generated oracle
            oracle_metrics: Oracle precision metrics
            test: Generated test
            test_quality: Test quality report
        """
        # Determine category
        category = self._categorize_completeness(endpoint.documentation_completeness)
        
        # Identify missing elements
        missing_status = endpoint.expected_status is None
        missing_headers = [h for h in ["Content-Type", "Authorization"] if h not in endpoint.expected_headers]
        missing_schema = endpoint.expected_response_schema is None
        missing_examples = endpoint.body is None and endpoint.method.value in ["POST", "PUT", "PATCH"]
        
        # Create impact metrics
        impact = CompletenessImpactMetrics(
            completeness_score=endpoint.documentation_completeness,
            category=category,
            oracle_precision=oracle_metrics.precision,
            oracle_recall=oracle_metrics.recall,
            oracle_f1=oracle_metrics.f1_score,
            oracle_confidence=oracle.confidence_score,
            test_quality_score=test_quality.overall_quality_score,
            test_correctness=test_quality.correctness_metrics.correctness_score,
            assertion_count=test.assertion_count,
            missing_status_code=missing_status,
            missing_headers=missing_headers,
            missing_schema=missing_schema,
            missing_examples=missing_examples,
            endpoint_id=endpoint.id,
            llm_model=oracle.llm_model or ""
        )
        
        # Calculate degradation if baseline is set
        if self.baseline_precision is not None:
            impact.precision_drop = self.baseline_precision - oracle_metrics.precision
        if self.baseline_quality is not None:
            impact.quality_drop = self.baseline_quality - test_quality.overall_quality_score
        
        self.metrics.append(impact)
    
    def set_baseline(
        self,
        complete_endpoints: List[Tuple[EndpointContext, Oracle, OraclePrecisionMetrics, GeneratedTest, TestQualityReport]]
    ) -> None:
        """
        Set baseline metrics from endpoints with complete documentation (>0.9).
        
        Args:
            complete_endpoints: List of tuples with complete endpoint data
        """
        precisions = []
        qualities = []
        
        for endpoint, oracle, oracle_metrics, test, test_quality in complete_endpoints:
            if endpoint.documentation_completeness >= 0.9:
                precisions.append(oracle_metrics.precision)
                qualities.append(test_quality.overall_quality_score)
        
        if precisions:
            self.baseline_precision = statistics.mean(precisions)
        if qualities:
            self.baseline_quality = statistics.mean(qualities)
    
    def analyze(self) -> CompletenessAnalysisReport:
        """
        Analyze the impact of completeness across all endpoints.
        
        Returns:
            CompletenessAnalysisReport with correlation analysis
        """
        if not self.metrics:
            return CompletenessAnalysisReport(
                completeness_precision_correlation=0.0,
                completeness_quality_correlation=0.0,
                completeness_confidence_correlation=0.0,
                total_endpoints=0
            )
        
        report = CompletenessAnalysisReport(
            completeness_precision_correlation=0.0,
            completeness_quality_correlation=0.0,
            completeness_confidence_correlation=0.0,
            total_endpoints=len(self.metrics)
        )
        
        # Calculate correlations
        report.completeness_precision_correlation = self._calculate_correlation(
            [m.completeness_score for m in self.metrics],
            [m.oracle_precision for m in self.metrics]
        )
        report.completeness_quality_correlation = self._calculate_correlation(
            [m.completeness_score for m in self.metrics],
            [m.test_quality_score for m in self.metrics]
        )
        report.completeness_confidence_correlation = self._calculate_correlation(
            [m.completeness_score for m in self.metrics],
            [m.oracle_confidence for m in self.metrics]
        )
        
        # Group by category
        report.metrics_by_category = self._group_by_category()
        report.avg_by_category = self._calculate_category_averages(report.metrics_by_category)
        
        # Find thresholds
        report.min_completeness_for_good_quality = self._find_threshold(
            [m.completeness_score for m in self.metrics],
            [m.test_quality_score for m in self.metrics],
            target=0.8
        )
        report.min_completeness_for_good_precision = self._find_threshold(
            [m.completeness_score for m in self.metrics],
            [m.oracle_precision for m in self.metrics],
            target=0.8
        )
        
        # Missing elements frequency
        report.missing_elements_frequency = self._analyze_missing_elements()
        
        # Degradation analysis
        report.avg_precision_drop_per_10pct = self._calculate_degradation_rate(
            [m.completeness_score for m in self.metrics],
            [m.oracle_precision for m in self.metrics]
        )
        report.avg_quality_drop_per_10pct = self._calculate_degradation_rate(
            [m.completeness_score for m in self.metrics],
            [m.test_quality_score for m in self.metrics]
        )
        
        return report
    
    def analyze_by_llm(
        self,
        llm_model: str
    ) -> CompletenessAnalysisReport:
        """
        Analyze completeness impact for a specific LLM.
        
        Args:
            llm_model: Name of the LLM to analyze
        
        Returns:
            CompletenessAnalysisReport for that LLM
        """
        # Filter metrics for this LLM
        llm_metrics = [m for m in self.metrics if m.llm_model == llm_model]
        
        if not llm_metrics:
            return CompletenessAnalysisReport(
                completeness_precision_correlation=0.0,
                completeness_quality_correlation=0.0,
                completeness_confidence_correlation=0.0,
                total_endpoints=0
            )
        
        # Temporarily replace metrics
        original_metrics = self.metrics
        self.metrics = llm_metrics
        
        # Analyze
        report = self.analyze()
        
        # Restore original metrics
        self.metrics = original_metrics
        
        return report
    
    def compare_llms_robustness(
        self,
        llm_models: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare how different LLMs handle incomplete documentation.
        
        Args:
            llm_models: List of LLM model names
        
        Returns:
            Dict mapping model name to robustness metrics
        """
        results = {}
        
        for model in llm_models:
            llm_metrics = [m for m in self.metrics if m.llm_model == model]
            
            if not llm_metrics:
                continue
            
            # Separate by completeness level
            complete = [m for m in llm_metrics if m.completeness_score >= 0.8]
            incomplete = [m for m in llm_metrics if m.completeness_score < 0.5]
            
            if complete and incomplete:
                complete_precision = statistics.mean([m.oracle_precision for m in complete])
                incomplete_precision = statistics.mean([m.oracle_precision for m in incomplete])
                complete_quality = statistics.mean([m.test_quality_score for m in complete])
                incomplete_quality = statistics.mean([m.test_quality_score for m in incomplete])
                
                # Robustness = how well it performs with incomplete docs relative to complete
                precision_retention = incomplete_precision / complete_precision if complete_precision > 0 else 0
                quality_retention = incomplete_quality / complete_quality if complete_quality > 0 else 0
                
                results[model] = {
                    "complete_precision": complete_precision,
                    "incomplete_precision": incomplete_precision,
                    "precision_retention": precision_retention,
                    "complete_quality": complete_quality,
                    "incomplete_quality": incomplete_quality,
                    "quality_retention": quality_retention,
                    "robustness_score": (precision_retention + quality_retention) / 2
                }
        
        return results
    
    def generate_recommendations(
        self,
        report: CompletenessAnalysisReport
    ) -> List[str]:
        """
        Generate recommendations based on completeness analysis.
        
        Args:
            report: CompletenessAnalysisReport
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Correlation strength
        if report.completeness_precision_correlation > 0.7:
            recommendations.append(
                f"Strong positive correlation ({report.completeness_precision_correlation:.2f}) "
                "between documentation completeness and oracle precision. "
                "Improving documentation will significantly improve oracle quality."
            )
        elif report.completeness_precision_correlation > 0.4:
            recommendations.append(
                f"Moderate positive correlation ({report.completeness_precision_correlation:.2f}) "
                "between documentation completeness and oracle precision. "
                "Better documentation helps but other factors also matter."
            )
        
        # Minimum thresholds
        if report.min_completeness_for_good_precision > 0:
            recommendations.append(
                f"Minimum documentation completeness of {report.min_completeness_for_good_precision:.0%} "
                "is required to achieve oracle precision > 80%. "
                "Ensure documentation meets this threshold."
            )
        
        if report.min_completeness_for_good_quality > 0:
            recommendations.append(
                f"Minimum documentation completeness of {report.min_completeness_for_good_quality:.0%} "
                "is required to achieve test quality > 80%."
            )
        
        # Missing elements
        if report.missing_elements_frequency:
            most_missing = max(report.missing_elements_frequency.items(), key=lambda x: x[1])
            recommendations.append(
                f"Most frequently missing documentation element: {most_missing[0]} "
                f"({most_missing[1]} occurrences). Prioritize documenting this."
            )
        
        # Degradation rate
        if report.avg_precision_drop_per_10pct > 0.05:
            recommendations.append(
                f"Oracle precision drops by {report.avg_precision_drop_per_10pct:.1%} "
                "for every 10% decrease in documentation completeness. "
                "Documentation quality is critical."
            )
        
        return recommendations
    
    # Private helper methods
    
    def _categorize_completeness(self, score: float) -> str:
        """Categorize completeness score."""
        if score >= 0.8:
            return CompletenessCategory.COMPLETE
        elif score >= 0.6:
            return CompletenessCategory.MOSTLY_COMPLETE
        elif score >= 0.4:
            return CompletenessCategory.PARTIAL
        elif score >= 0.2:
            return CompletenessCategory.INCOMPLETE
        else:
            return CompletenessCategory.MINIMAL
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        
        sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        
        if sum_sq_x == 0 or sum_sq_y == 0:
            return 0.0
        
        denominator = (sum_sq_x * sum_sq_y) ** 0.5
        
        return numerator / denominator if denominator > 0 else 0.0
    
    def _group_by_category(self) -> Dict[str, List[CompletenessImpactMetrics]]:
        """Group metrics by completeness category."""
        grouped = {}
        
        for metric in self.metrics:
            if metric.category not in grouped:
                grouped[metric.category] = []
            grouped[metric.category].append(metric)
        
        return grouped
    
    def _calculate_category_averages(
        self,
        grouped: Dict[str, List[CompletenessImpactMetrics]]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate average metrics per category."""
        averages = {}
        
        for category, metrics_list in grouped.items():
            if not metrics_list:
                continue
            
            n = len(metrics_list)
            averages[category] = {
                "avg_completeness": sum(m.completeness_score for m in metrics_list) / n,
                "avg_precision": sum(m.oracle_precision for m in metrics_list) / n,
                "avg_recall": sum(m.oracle_recall for m in metrics_list) / n,
                "avg_f1": sum(m.oracle_f1 for m in metrics_list) / n,
                "avg_quality": sum(m.test_quality_score for m in metrics_list) / n,
                "avg_correctness": sum(m.test_correctness for m in metrics_list) / n,
                "avg_assertions": sum(m.assertion_count for m in metrics_list) / n,
                "count": n
            }
        
        return averages
    
    def _find_threshold(
        self,
        completeness_scores: List[float],
        quality_scores: List[float],
        target: float
    ) -> float:
        """
        Find minimum completeness score needed to achieve target quality.
        
        Args:
            completeness_scores: List of completeness scores
            quality_scores: List of quality scores
            target: Target quality score (e.g., 0.8)
        
        Returns:
            Minimum completeness score, or 0.0 if not achievable
        """
        # Find all samples that meet target
        meeting_target = [
            completeness_scores[i]
            for i in range(len(quality_scores))
            if quality_scores[i] >= target
        ]
        
        if not meeting_target:
            return 0.0
        
        # Return minimum completeness among those meeting target
        return min(meeting_target)
    
    def _analyze_missing_elements(self) -> Dict[str, int]:
        """Count frequency of missing documentation elements."""
        frequency = {
            "status_code": 0,
            "headers": 0,
            "schema": 0,
            "examples": 0
        }
        
        for metric in self.metrics:
            if metric.missing_status_code:
                frequency["status_code"] += 1
            if metric.missing_headers:
                frequency["headers"] += 1
            if metric.missing_schema:
                frequency["schema"] += 1
            if metric.missing_examples:
                frequency["examples"] += 1
        
        return frequency
    
    def _calculate_degradation_rate(
        self,
        completeness_scores: List[float],
        quality_scores: List[float]
    ) -> float:
        """
        Calculate average quality drop per 10% completeness decrease.
        
        Uses linear regression to estimate slope.
        """
        if len(completeness_scores) < 2:
            return 0.0
        
        # Simple linear regression
        n = len(completeness_scores)
        mean_x = statistics.mean(completeness_scores)
        mean_y = statistics.mean(quality_scores)
        
        numerator = sum(
            (completeness_scores[i] - mean_x) * (quality_scores[i] - mean_y)
            for i in range(n)
        )
        denominator = sum(
            (completeness_scores[i] - mean_x) ** 2
            for i in range(n)
        )
        
        if denominator == 0:
            return 0.0
        
        # Slope of regression line (change in quality per unit change in completeness)
        slope = numerator / denominator
        
        # Convert to "per 10% completeness"
        return abs(slope * 0.1)
    
    def export_to_csv(self, filename: str) -> None:
        """Export analysis data to CSV."""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                "EndpointID", "Completeness", "Category", "LLMModel",
                "OraclePrecision", "OracleRecall", "OracleF1", "OracleConfidence",
                "TestQuality", "TestCorrectness", "AssertionCount",
                "MissingStatusCode", "MissingHeaders", "MissingSchema", "MissingExamples",
                "PrecisionDrop", "QualityDrop"
            ])
            
            # Data rows
            for metric in self.metrics:
                writer.writerow([
                    str(metric.endpoint_id), metric.completeness_score, metric.category, metric.llm_model,
                    metric.oracle_precision, metric.oracle_recall, metric.oracle_f1, metric.oracle_confidence,
                    metric.test_quality_score, metric.test_correctness, metric.assertion_count,
                    metric.missing_status_code, ",".join(metric.missing_headers), metric.missing_schema, metric.missing_examples,
                    metric.precision_drop or 0.0, metric.quality_drop or 0.0
                ])
