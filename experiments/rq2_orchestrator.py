"""
RQ2 Consistency Experiment Orchestrator

Advanced orchestration system for running comprehensive RQ2 consistency experiments.
Supports:
- Batch consistency validation across multiple test suites
- Multi-LLM comparison for code generation quality
- Statistical analysis of consistency patterns
- Cross-validation and experiment replication
- Result aggregation and inconsistency pattern analysis

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from uuid import UUID
import statistics
from collections import Counter, defaultdict

from experiments.rq2_consistency_validation import (
    RQ2ExperimentRunner,
    ConsistencyExperimentConfig,
    ConsistencyExperimentReport,
    EndpointConsistencyResult
)
from src.shared_context.models import (
    EndpointContext,
    Oracle,
    GeneratedTest,
    HTTPMethod
)
from src.validation.inconsistency_detector import (
    InconsistencyType,
    InconsistencySeverity
)


@dataclass
class BatchConsistencyConfig:
    """Configuration for batch consistency validation experiments."""
    experiment_name: str
    description: str
    llm_models: List[str]  # Models to compare
    test_suites: List[str]  # Paths to test suite directories
    num_replications: int = 3
    output_dir: Path = Path("experiments/results/rq2")
    
    # Consistency thresholds
    min_coherence_score: float = 0.8
    max_critical_inconsistencies: int = 0
    max_major_inconsistencies: int = 2
    
    # Analysis options
    enable_pattern_analysis: bool = True
    enable_statistical_tests: bool = True
    generate_visualizations: bool = True
    
    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class InconsistencyPattern:
    """Pattern of inconsistencies across experiments."""
    pattern_type: str  # e.g., "missing_status_code_validation"
    category: str  # e.g., "status_code", "header", "schema"
    severity: InconsistencySeverity
    occurrence_count: int
    affected_endpoints: List[str]
    affected_models: List[str]
    occurrence_rate: float  # % of endpoints affected
    
    # Statistics
    avg_per_endpoint: float = 0.0
    std_per_endpoint: float = 0.0
    
    # Recommendations
    recommendation: str = ""
    impact_assessment: str = ""


@dataclass
class ConsistencyPatternAnalysis:
    """Analysis of consistency patterns across experiments."""
    total_experiments: int
    total_endpoints: int
    
    # Pattern detection
    common_patterns: List[InconsistencyPattern] = field(default_factory=list)
    model_specific_patterns: Dict[str, List[InconsistencyPattern]] = field(default_factory=dict)
    
    # Severity distribution
    severity_distribution: Dict[str, int] = field(default_factory=lambda: {
        "critical": 0,
        "major": 0,
        "minor": 0,
        "info": 0
    })
    
    # Type distribution
    type_distribution: Dict[str, int] = field(default_factory=lambda: {
        "missing_validation": 0,
        "extra_validation": 0,
        "incorrect_value": 0,
        "incorrect_type": 0,
        "incomplete_implementation": 0,
        "weak_assertion": 0,
        "missing_gherkin_step": 0
    })
    
    # Category distribution
    category_distribution: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_experiments": self.total_experiments,
            "total_endpoints": self.total_endpoints,
            "common_patterns": [
                {
                    "pattern_type": p.pattern_type,
                    "category": p.category,
                    "severity": p.severity.value,
                    "occurrence_count": p.occurrence_count,
                    "occurrence_rate": p.occurrence_rate,
                    "affected_models": p.affected_models,
                    "recommendation": p.recommendation
                }
                for p in self.common_patterns
            ],
            "severity_distribution": self.severity_distribution,
            "type_distribution": self.type_distribution,
            "category_distribution": self.category_distribution
        }


@dataclass
class BatchConsistencyResults:
    """Results from batch consistency validation experiments."""
    experiment_name: str
    config: BatchConsistencyConfig
    reports: List[ConsistencyExperimentReport]
    pattern_analysis: Optional[ConsistencyPatternAnalysis] = None
    statistical_results: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "experiment_name": self.experiment_name,
            "config": {
                "llm_models": self.config.llm_models,
                "test_suites": [str(s) for s in self.config.test_suites],
                "num_replications": self.config.num_replications,
                "thresholds": {
                    "min_coherence_score": self.config.min_coherence_score,
                    "max_critical_inconsistencies": self.config.max_critical_inconsistencies,
                    "max_major_inconsistencies": self.config.max_major_inconsistencies
                }
            },
            "created_at": self.created_at.isoformat(),
            "num_reports": len(self.reports),
            "pattern_analysis": self.pattern_analysis.to_dict() if self.pattern_analysis else None,
            "statistical_results": self.statistical_results
        }
    
    def save(self, filename: Optional[str] = None):
        """Save results to JSON file."""
        if filename is None:
            timestamp = self.created_at.strftime("%Y%m%d_%H%M%S")
            filename = f"{self.experiment_name}_{timestamp}.json"
        
        output_path = self.config.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.to_json(), f, indent=2)
        
        print(f"\n✓ Saved batch results to {output_path}")
        return output_path


class RQ2Orchestrator:
    """
    Orchestrator for comprehensive RQ2 consistency validation experiments.
    
    Manages:
    - Multiple test suites and oracle-test pairs
    - Multi-LLM consistency comparison
    - Inconsistency pattern detection and analysis
    - Experiment replication for statistical validity
    - Result aggregation and visualization
    """
    
    def __init__(self, config: BatchConsistencyConfig):
        self.config = config
        self.all_reports: List[ConsistencyExperimentReport] = []
        
    async def run_batch_experiments(self) -> BatchConsistencyResults:
        """
        Run batch consistency validation experiments.
        
        Returns:
            BatchConsistencyResults with all experiment reports
        """
        print(f"\n{'='*60}")
        print(f"BATCH CONSISTENCY EXPERIMENT: {self.config.experiment_name}")
        print(f"{'='*60}")
        print(f"Description: {self.config.description}")
        print(f"LLM Models: {', '.join(self.config.llm_models)}")
        print(f"Test Suites: {len(self.config.test_suites)}")
        print(f"Replications: {self.config.num_replications}")
        print(f"Coherence Threshold: {self.config.min_coherence_score:.2f}")
        print(f"{'='*60}\n")
        
        # Run experiments for each test suite
        for suite_path in self.config.test_suites:
            print(f"\n--- Processing Test Suite: {suite_path} ---")
            
            # Load test suite data
            suite_data = self._load_test_suite(suite_path)
            if not suite_data:
                print(f"⚠ Could not load test suite {suite_path}, skipping...")
                continue
            
            endpoints = suite_data["endpoints"]
            oracles = suite_data["oracles"]
            
            # Run experiments for each LLM model
            for model in self.config.llm_models:
                print(f"\n  Model: {model}")
                
                # Load generated tests for this model
                generated_tests = self._load_generated_tests(suite_path, model)
                
                if not generated_tests:
                    print(f"    ⚠ No generated tests found for {model}, skipping...")
                    continue
                
                # Run multiple replications
                for replication in range(1, self.config.num_replications + 1):
                    print(f"    Replication {replication}/{self.config.num_replications}")
                    
                    # Create experiment configuration
                    exp_config = ConsistencyExperimentConfig(
                        experiment_id=f"{suite_path}_{model}_rep{replication}",
                        name=f"RQ2 - {model} - Suite {suite_path}",
                        description=f"Consistency validation for {model} on {suite_path}",
                        llm_models=[model],
                        num_endpoints=len(endpoints),
                        min_coherence_score=self.config.min_coherence_score,
                        max_critical_inconsistencies=self.config.max_critical_inconsistencies,
                        max_major_inconsistencies=self.config.max_major_inconsistencies,
                        output_dir=self.config.output_dir
                    )
                    
                    # Run experiment
                    runner = RQ2ExperimentRunner(config=exp_config)
                    report = await runner.run_experiment(
                        endpoints=endpoints,
                        oracles=oracles,
                        generated_tests=generated_tests
                    )
                    
                    self.all_reports.append(report)
                    
                    # Print summary
                    self._print_report_summary(report, model)
        
        # Analyze patterns
        pattern_analysis = None
        if self.config.enable_pattern_analysis:
            print("\n--- Analyzing Inconsistency Patterns ---")
            pattern_analysis = self._analyze_inconsistency_patterns()
            self._print_pattern_analysis(pattern_analysis)
        
        # Statistical analysis
        statistical_results = None
        if self.config.enable_statistical_tests:
            print("\n--- Running Statistical Analysis ---")
            statistical_results = self._run_statistical_analysis()
        
        # Create batch results
        results = BatchConsistencyResults(
            experiment_name=self.config.experiment_name,
            config=self.config,
            reports=self.all_reports,
            pattern_analysis=pattern_analysis,
            statistical_results=statistical_results
        )
        
        # Save results
        results.save()
        
        return results
    
    def _load_test_suite(self, suite_path: str) -> Optional[Dict[str, Any]]:
        """
        Load test suite data (endpoints and oracles).
        
        Args:
            suite_path: Path to test suite directory or file
        
        Returns:
            Dictionary with endpoints and oracles, or None if failed
        """
        # This is a placeholder implementation
        # In real usage, load from actual test suite files
        print(f"    Loading test suite from {suite_path}...")
        
        # Example structure:
        # return {
        #     "endpoints": [...],
        #     "oracles": {...}
        # }
        
        # For now, return None (will be implemented with actual data)
        return None
    
    def _load_generated_tests(
        self,
        suite_path: str,
        model: str
    ) -> Optional[Dict[UUID, GeneratedTest]]:
        """
        Load generated tests for specific LLM model.
        
        Args:
            suite_path: Path to test suite
            model: LLM model name
        
        Returns:
            Mapping of endpoint_id -> GeneratedTest, or None if failed
        """
        # Placeholder implementation
        print(f"      Loading generated tests for {model}...")
        
        # In real usage, load from output directories
        # return {endpoint_id: GeneratedTest(...)}
        
        return None
    
    def _print_report_summary(self, report: ConsistencyExperimentReport, model: str):
        """Print summary of experiment report."""
        if model not in report.aggregate_metrics:
            return
        
        metrics = report.aggregate_metrics[model]
        
        print(f"      Coherence: {metrics['coherence_mean']:.3f} ± {metrics['coherence_std']:.3f}")
        print(f"      Java Coverage: {metrics['java_coverage_mean']:.1%}")
        print(f"      Gherkin Coverage: {metrics['gherkin_coverage_mean']:.1%}")
        print(f"      Pass Rate: {metrics['pass_rate']:.1%}")
        print(f"      Critical Issues: {metrics['critical_avg']:.1f} avg")
        print(f"      Major Issues: {metrics['major_avg']:.1f} avg")
    
    def _analyze_inconsistency_patterns(self) -> ConsistencyPatternAnalysis:
        """
        Analyze patterns in inconsistencies across all experiments.
        
        Returns:
            ConsistencyPatternAnalysis with detected patterns
        """
        analysis = ConsistencyPatternAnalysis(
            total_experiments=len(self.all_reports),
            total_endpoints=sum(r.total_endpoints for r in self.all_reports)
        )
        
        # Collect all inconsistencies
        all_inconsistencies = []
        for report in self.all_reports:
            for endpoint_result in report.endpoint_results:
                if endpoint_result.inconsistency_report:
                    ir = endpoint_result.inconsistency_report
                    all_inconsistencies.extend(ir.critical)
                    all_inconsistencies.extend(ir.major)
                    all_inconsistencies.extend(ir.minor)
                    all_inconsistencies.extend(ir.info)
        
        # Count by severity
        for inc in all_inconsistencies:
            analysis.severity_distribution[inc.severity.value] += 1
            analysis.type_distribution[inc.type.value] = \
                analysis.type_distribution.get(inc.type.value, 0) + 1
            analysis.category_distribution[inc.category] = \
                analysis.category_distribution.get(inc.category, 0) + 1
        
        # Detect common patterns
        pattern_counter = Counter()
        for inc in all_inconsistencies:
            pattern_key = f"{inc.type.value}_{inc.category}"
            pattern_counter[pattern_key] += 1
        
        # Create pattern objects for most common patterns
        total_endpoints = analysis.total_endpoints if analysis.total_endpoints > 0 else 1
        
        for (pattern_key, count) in pattern_counter.most_common(10):
            inc_type, category = pattern_key.split("_", 1)
            
            # Find all inconsistencies of this pattern
            pattern_incs = [
                inc for inc in all_inconsistencies
                if inc.type.value == inc_type and inc.category == category
            ]
            
            if not pattern_incs:
                continue
            
            # Determine most common severity
            severity_counts = Counter(inc.severity for inc in pattern_incs)
            common_severity = severity_counts.most_common(1)[0][0]
            
            # Collect affected endpoints and models
            affected_endpoints = list(set(
                inc.field_name for inc in pattern_incs
            ))
            affected_models = []  # Would extract from endpoint_results
            
            pattern = InconsistencyPattern(
                pattern_type=pattern_key,
                category=category,
                severity=common_severity,
                occurrence_count=count,
                affected_endpoints=affected_endpoints[:5],  # Top 5
                affected_models=affected_models,
                occurrence_rate=count / total_endpoints,
                recommendation=pattern_incs[0].recommendation if pattern_incs else ""
            )
            
            analysis.common_patterns.append(pattern)
        
        return analysis
    
    def _print_pattern_analysis(self, analysis: ConsistencyPatternAnalysis):
        """Print summary of pattern analysis."""
        print(f"\nTotal Experiments: {analysis.total_experiments}")
        print(f"Total Endpoints: {analysis.total_endpoints}")
        
        print("\nSeverity Distribution:")
        for severity, count in analysis.severity_distribution.items():
            print(f"  {severity.upper()}: {count}")
        
        print("\nTop 5 Common Patterns:")
        for i, pattern in enumerate(analysis.common_patterns[:5], 1):
            print(f"  {i}. {pattern.pattern_type}")
            print(f"     Severity: {pattern.severity.value}")
            print(f"     Occurrences: {pattern.occurrence_count} ({pattern.occurrence_rate:.1%})")
            print(f"     Category: {pattern.category}")
    
    def _run_statistical_analysis(self) -> Dict[str, Any]:
        """
        Run statistical analysis on experiment results.
        
        Returns:
            Dictionary with statistical test results
        """
        # Placeholder for statistical analysis
        # Would include:
        # - ANOVA/Kruskal-Wallis for comparing LLM models
        # - Effect sizes (Cohen's d, eta-squared)
        # - Confidence intervals
        # - Pairwise comparisons with corrections
        
        stats = {
            "comparison_method": "not_implemented",
            "note": "Statistical analysis to be implemented with scipy.stats"
        }
        
        return stats
    
    def get_comparative_summary(self) -> Dict[str, Any]:
        """
        Get comparative summary across all LLM models.
        
        Returns:
            Dictionary with model comparison
        """
        model_summaries = {}
        
        for model in self.config.llm_models:
            # Aggregate across all reports for this model
            model_reports = [
                r for r in self.all_reports
                if model in r.aggregate_metrics
            ]
            
            if not model_reports:
                continue
            
            coherence_scores = [
                r.aggregate_metrics[model]["coherence_mean"]
                for r in model_reports
            ]
            
            pass_rates = [
                r.aggregate_metrics[model]["pass_rate"]
                for r in model_reports
            ]
            
            critical_counts = [
                r.aggregate_metrics[model]["critical_avg"]
                for r in model_reports
            ]
            
            model_summaries[model] = {
                "coherence_mean": statistics.mean(coherence_scores),
                "coherence_std": statistics.stdev(coherence_scores) if len(coherence_scores) > 1 else 0.0,
                "pass_rate_mean": statistics.mean(pass_rates),
                "critical_issues_mean": statistics.mean(critical_counts),
                "num_experiments": len(model_reports)
            }
        
        return model_summaries


async def main():
    """Example usage of RQ2 orchestrator."""
    config = BatchConsistencyConfig(
        experiment_name="rq2_batch_example",
        description="Example batch consistency validation",
        llm_models=["gpt-4", "claude-3-opus", "gemini-pro"],
        test_suites=["suite1", "suite2"],
        num_replications=3,
        min_coherence_score=0.8
    )
    
    orchestrator = RQ2Orchestrator(config=config)
    
    print("RQ2 Orchestrator initialized")
    print(f"Configuration: {len(config.llm_models)} models, {len(config.test_suites)} suites")
    print(f"Output directory: {config.output_dir}")
    
    # Note: In real usage, call:
    # results = await orchestrator.run_batch_experiments()


if __name__ == "__main__":
    asyncio.run(main())
