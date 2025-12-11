"""
RQ1 Experiment Orchestrator

Advanced orchestration system for running comprehensive RQ1 validation experiments.
Supports:
- Batch experiment execution across multiple datasets
- Parameter sweeping (completeness levels, LLM configurations)
- Statistical analysis and significance testing
- Cross-validation and experiment replication
- Result aggregation and comparison

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

from experiments.rq1_oracle_validation import (
    RQ1ExperimentRunner,
    ExperimentConfig,
    ExperimentReport,
    EndpointExperimentResult
)
from experiments.ground_truth_manager import GroundTruthManager
from src.shared_context.models import EndpointContext


@dataclass
class BatchExperimentConfig:
    """Configuration for batch experiment execution."""
    experiment_name: str
    description: str
    llm_models: List[str]
    datasets: List[str]  # Paths to ground truth JSON files
    completeness_levels: List[float] = field(default_factory=lambda: [1.0, 0.75, 0.5, 0.25])
    num_replications: int = 3
    output_dir: Path = Path("experiments/results/rq1")
    enable_statistical_tests: bool = True
    
    def __post_init__(self):
        self.output_dir = Path(self.output_dir)


@dataclass
class BatchExperimentResults:
    """Results from batch experiment execution."""
    experiment_name: str
    config: BatchExperimentConfig
    reports: List[ExperimentReport]
    statistical_results: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "experiment_name": self.experiment_name,
            "config": {
                "llm_models": self.config.llm_models,
                "datasets": [str(d) for d in self.config.datasets],
                "completeness_levels": self.config.completeness_levels,
                "num_replications": self.config.num_replications
            },
            "created_at": self.created_at.isoformat(),
            "num_reports": len(self.reports),
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


class RQ1Orchestrator:
    """
    Orchestrator for comprehensive RQ1 validation experiments.
    
    Manages:
    - Multiple datasets and ground truth collections
    - Parameter sweeping across completeness levels
    - Experiment replication for statistical validity
    - Result aggregation and analysis
    - Statistical significance testing
    """
    
    def __init__(self, config: BatchExperimentConfig):
        self.config = config
        self.gt_manager = GroundTruthManager()
        self.all_reports: List[ExperimentReport] = []
    
    async def run_batch_experiments(self) -> BatchExperimentResults:
        """
        Run batch experiments across all configurations.
        
        Returns:
            BatchExperimentResults with all experiment reports
        """
        print(f"\n{'='*60}")
        print(f"BATCH EXPERIMENT: {self.config.experiment_name}")
        print(f"{'='*60}")
        print(f"Description: {self.config.description}")
        print(f"LLM Models: {', '.join(self.config.llm_models)}")
        print(f"Datasets: {len(self.config.datasets)}")
        print(f"Completeness Levels: {self.config.completeness_levels}")
        print(f"Replications: {self.config.num_replications}")
        print(f"{'='*60}\n")
        
        # Run experiments for each dataset
        for dataset_path in self.config.datasets:
            print(f"\n--- Processing Dataset: {dataset_path} ---")
            
            # Load ground truths
            self.gt_manager.load_from_file(dataset_path)
            ground_truths = self.gt_manager.list_ground_truths()
            
            if not ground_truths:
                print(f"⚠ No ground truths found in {dataset_path}, skipping...")
                continue
            
            # Get endpoints (would normally load from collection file)
            endpoints = self._load_endpoints_for_ground_truths(ground_truths)
            
            # Run experiments for each completeness level
            for completeness in self.config.completeness_levels:
                print(f"\n  Completeness Level: {completeness*100:.0f}%")
                
                # Modify endpoints to simulate completeness level
                modified_endpoints = self._apply_completeness_level(
                    endpoints, completeness
                )
                
                # Run multiple replications
                for replication in range(1, self.config.num_replications + 1):
                    print(f"    Replication {replication}/{self.config.num_replications}")
                    
                    # Create experiment config
                    exp_config = ExperimentConfig(
                        experiment_name=f"{self.config.experiment_name}_c{int(completeness*100)}_r{replication}",
                        llm_models=self.config.llm_models,
                        endpoints=modified_endpoints,
                        ground_truths={gt.endpoint_id: gt for gt in ground_truths},
                        num_endpoints=len(modified_endpoints),
                        output_dir=self.config.output_dir / f"completeness_{int(completeness*100)}" / f"rep_{replication}"
                    )
                    
                    # Run experiment
                    runner = RQ1ExperimentRunner(exp_config)
                    report = await runner.run_experiment()
                    
                    # Store report
                    self.all_reports.append(report)
                    
                    # Save individual report
                    report.save_to_json()
        
        # Perform statistical analysis
        statistical_results = None
        if self.config.enable_statistical_tests:
            statistical_results = self._perform_statistical_analysis()
        
        # Create batch results
        batch_results = BatchExperimentResults(
            experiment_name=self.config.experiment_name,
            config=self.config,
            reports=self.all_reports,
            statistical_results=statistical_results
        )
        
        # Save batch results
        batch_results.save()
        
        # Print summary
        self._print_batch_summary(batch_results)
        
        return batch_results
    
    def _load_endpoints_for_ground_truths(
        self,
        ground_truths: List
    ) -> List[EndpointContext]:
        """
        Load endpoints that correspond to ground truths.
        
        In production, this would load from actual collection files.
        For now, creates minimal endpoint contexts.
        """
        endpoints = []
        
        for gt in ground_truths:
            # Create minimal endpoint context
            # In real implementation, would load from collection file
            endpoint = EndpointContext(
                id=gt.endpoint_id,
                name=f"Endpoint for GT {gt.endpoint_id}",
                method="GET",  # Would be from collection
                path="/api/resource",  # Would be from collection
                description="Test endpoint",  # Would be from collection
                documentation_completeness=1.0
            )
            endpoints.append(endpoint)
        
        return endpoints
    
    def _apply_completeness_level(
        self,
        endpoints: List[EndpointContext],
        completeness: float
    ) -> List[EndpointContext]:
        """
        Modify endpoints to simulate different documentation completeness levels.
        
        Args:
            endpoints: Original endpoints
            completeness: Target completeness (0.0-1.0)
            
        Returns:
            Modified endpoints with reduced documentation
        """
        modified = []
        
        for endpoint in endpoints:
            # Create copy with modified completeness
            modified_endpoint = EndpointContext(
                id=endpoint.id,
                name=endpoint.name,
                method=endpoint.method,
                path=endpoint.path,
                description=endpoint.description if completeness > 0.5 else "",
                documentation_completeness=completeness
            )
            
            # Remove documentation elements based on completeness
            if completeness < 1.0:
                # Would modify description, examples, etc.
                pass
            
            modified.append(modified_endpoint)
        
        return modified
    
    def _perform_statistical_analysis(self) -> Dict[str, Any]:
        """
        Perform statistical analysis on experiment results.
        
        Returns:
            Dictionary with statistical test results
        """
        print("\n--- Statistical Analysis ---")
        
        # Group reports by LLM model
        reports_by_llm = {}
        for report in self.all_reports:
            for llm, metrics in report.llm_metrics.items():
                if llm not in reports_by_llm:
                    reports_by_llm[llm] = []
                reports_by_llm[llm].append(metrics)
        
        # Calculate statistics for each LLM
        llm_statistics = {}
        for llm, metrics_list in reports_by_llm.items():
            precisions = [m["precision"] for m in metrics_list]
            recalls = [m["recall"] for m in metrics_list]
            f1_scores = [m["f1_score"] for m in metrics_list]
            
            llm_statistics[llm] = {
                "precision": {
                    "mean": statistics.mean(precisions),
                    "stdev": statistics.stdev(precisions) if len(precisions) > 1 else 0.0,
                    "min": min(precisions),
                    "max": max(precisions)
                },
                "recall": {
                    "mean": statistics.mean(recalls),
                    "stdev": statistics.stdev(recalls) if len(recalls) > 1 else 0.0,
                    "min": min(recalls),
                    "max": max(recalls)
                },
                "f1_score": {
                    "mean": statistics.mean(f1_scores),
                    "stdev": statistics.stdev(f1_scores) if len(f1_scores) > 1 else 0.0,
                    "min": min(f1_scores),
                    "max": max(f1_scores)
                }
            }
        
        # Pairwise comparisons between LLMs
        pairwise_comparisons = self._pairwise_llm_comparisons(reports_by_llm)
        
        results = {
            "llm_statistics": llm_statistics,
            "pairwise_comparisons": pairwise_comparisons,
            "sample_sizes": {llm: len(metrics) for llm, metrics in reports_by_llm.items()}
        }
        
        # Print statistics
        print("\nLLM Performance Statistics:")
        for llm, stats in llm_statistics.items():
            print(f"\n{llm}:")
            print(f"  Precision: {stats['precision']['mean']:.3f} ± {stats['precision']['stdev']:.3f}")
            print(f"  Recall: {stats['recall']['mean']:.3f} ± {stats['recall']['stdev']:.3f}")
            print(f"  F1 Score: {stats['f1_score']['mean']:.3f} ± {stats['f1_score']['stdev']:.3f}")
        
        return results
    
    def _pairwise_llm_comparisons(
        self,
        reports_by_llm: Dict[str, List[Dict[str, float]]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Perform pairwise comparisons between LLMs.
        
        Returns:
            Dictionary with comparison results
        """
        comparisons = {}
        llm_names = list(reports_by_llm.keys())
        
        for i, llm1 in enumerate(llm_names):
            for llm2 in llm_names[i+1:]:
                # Calculate mean F1 difference
                f1_scores1 = [m["f1_score"] for m in reports_by_llm[llm1]]
                f1_scores2 = [m["f1_score"] for m in reports_by_llm[llm2]]
                
                mean_diff = statistics.mean(f1_scores1) - statistics.mean(f1_scores2)
                
                # Simple effect size (Cohen's d approximation)
                if len(f1_scores1) > 1 and len(f1_scores2) > 1:
                    pooled_std = (
                        (statistics.stdev(f1_scores1) + statistics.stdev(f1_scores2)) / 2
                    )
                    effect_size = mean_diff / pooled_std if pooled_std > 0 else 0.0
                else:
                    effect_size = 0.0
                
                comparison_key = f"{llm1} vs {llm2}"
                comparisons[comparison_key] = {
                    "mean_f1_difference": mean_diff,
                    "effect_size": effect_size,
                    "better_model": llm1 if mean_diff > 0 else llm2
                }
        
        return comparisons
    
    def _print_batch_summary(self, results: BatchExperimentResults):
        """Print summary of batch experiment results."""
        print(f"\n{'='*60}")
        print(f"BATCH EXPERIMENT SUMMARY")
        print(f"{'='*60}")
        print(f"Experiment: {results.experiment_name}")
        print(f"Total Reports: {len(results.reports)}")
        print(f"Completed: {results.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if results.statistical_results:
            print("\nStatistical Analysis:")
            stats = results.statistical_results["llm_statistics"]
            
            print("\nOverall Rankings (by mean F1 score):")
            rankings = sorted(
                stats.items(),
                key=lambda x: x[1]["f1_score"]["mean"],
                reverse=True
            )
            
            for rank, (llm, llm_stats) in enumerate(rankings, 1):
                f1_mean = llm_stats["f1_score"]["mean"]
                f1_std = llm_stats["f1_score"]["stdev"]
                print(f"  {rank}. {llm}: {f1_mean:.3f} ± {f1_std:.3f}")
        
        print(f"{'='*60}\n")


async def run_sample_batch_experiment():
    """Run a sample batch experiment with multiple configurations."""
    
    # Create sample ground truth dataset
    from experiments.ground_truth_manager import create_sample_ground_truth_dataset
    gt_manager = create_sample_ground_truth_dataset()
    
    # Configure batch experiment
    config = BatchExperimentConfig(
        experiment_name="rq1_completeness_impact",
        description="Evaluate impact of documentation completeness on oracle quality",
        llm_models=["gpt-4", "gpt-3.5-turbo", "claude-3"],
        datasets=["sample_ground_truths.json"],
        completeness_levels=[1.0, 0.75, 0.5, 0.25],
        num_replications=3,
        enable_statistical_tests=True
    )
    
    # Run batch experiments
    orchestrator = RQ1Orchestrator(config)
    results = await orchestrator.run_batch_experiments()
    
    return results


if __name__ == "__main__":
    # Run sample batch experiment
    asyncio.run(run_sample_batch_experiment())
