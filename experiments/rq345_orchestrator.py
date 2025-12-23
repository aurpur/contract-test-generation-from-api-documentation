"""
===============================================================================
RQ345 Unified Orchestrator - Combined Research Questions Analysis
===============================================================================

OBJECTIF:
    Orchestration unifiée pour les Questions de Recherche 3, 4 et 5:
    - RQ3: Évaluation de la qualité du code généré
    - RQ4: Comparaison des performances des modèles LLM
    - RQ5: Impact de la complétude de la documentation

FONCTIONNALITÉS:
    - Exécution batch sur plusieurs endpoints et modèles
    - Analyse de corrélation inter-RQ
    - Agrégation intégrée des résultats
    - Tests statistiques multi-dimensions
    - Détection de patterns comprehensive
    - Outputs prêts pour publication

MODÈLES LLM:
    Ce module utilise UNIQUEMENT des modèles Ollama locaux :
    - deepseek_r1      : Raisonnement avancé (deepseek-r1:8b)
    - deepseek_coder   : Code spécialisé (deepseek-coder-v2)
    - codellama_7b     : Meta CodeLlama 7B
    - qwen25_7b        : Qwen 2.5 généraliste
    - qwen25_coder_7b  : Qwen 2.5 code
    - llama31, llama32 : Meta Llama
    - mistral          : Mistral 7B

IMPORTANT:
    - PAS de simulation - utilise les vrais agents
    - PAS de modèles cloud (OpenAI, Anthropic, Google)

USAGE:
    python -m experiments.rq345_orchestrator

Auteur: Aurel IKAMA HONEY
Date: December 11, 2025
===============================================================================
"""
import asyncio
import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from experiments.rq3_quality_validation import (
    QualityExperimentConfig,
    QualityExperimentReport,
    RQ3ExperimentRunner
)
from experiments.rq4_llm_comparison import (
    LLMComparisonConfig,
    LLMComparisonExperimentReport,
    RQ4ExperimentRunner
)
from experiments.rq5_completeness_impact import (
    CompletenessExperimentConfig,
    CompletenessExperimentReport,
    RQ5ExperimentRunner
)
from src.shared_context.models import EndpointContext, GeneratedTest, Oracle


# ==============================================================================
# MODÈLES OLLAMA DISPONIBLES
# ==============================================================================
AVAILABLE_OLLAMA_MODELS = [
    "deepseek_r1", "deepseek_coder", "codellama_7b",
    "qwen25_7b", "qwen25_coder_7b", "llama31", "llama32", "mistral"
]


@dataclass
class RQ345BatchConfig:
    """Configuration for unified RQ3/4/5 batch experiments."""
    experiment_id: str
    name: str
    description: str
    
    # LLM models to evaluate
    llm_models: List[str]
    
    # Number of endpoints to test
    num_endpoints: int
    
    # Enable/disable individual RQs
    run_rq3: bool = True  # Code quality
    run_rq4: bool = True  # LLM comparison
    run_rq5: bool = True  # Completeness impact
    
    # Execution mode
    parallel_execution: bool = True
    
    # RQ-specific configurations
    rq3_config: Optional[QualityExperimentConfig] = None
    rq4_config: Optional[LLMComparisonConfig] = None
    rq5_config: Optional[CompletenessExperimentConfig] = None
    
    # Cross-RQ analysis options
    analyze_correlations: bool = True
    analyze_patterns: bool = True
    statistical_testing: bool = True
    
    # Output configuration
    output_dir: Path = Path("experiments/results/rq345")
    save_intermediate_results: bool = True
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "llm_models": self.llm_models,
            "num_endpoints": self.num_endpoints,
            "enabled_rqs": {
                "rq3_code_quality": self.run_rq3,
                "rq4_llm_comparison": self.run_rq4,
                "rq5_completeness_impact": self.run_rq5
            },
            "execution_mode": "parallel" if self.parallel_execution else "sequential",
            "analysis_options": {
                "correlations": self.analyze_correlations,
                "patterns": self.analyze_patterns,
                "statistical_testing": self.statistical_testing
            },
            "output_dir": str(self.output_dir)
        }


@dataclass
class RQ345Results:
    """Combined results from all three research questions."""
    rq3_report: Optional[QualityExperimentReport] = None
    rq4_report: Optional[LLMComparisonExperimentReport] = None
    rq5_report: Optional[CompletenessExperimentReport] = None
    
    def has_results(self) -> bool:
        """Check if any results are available."""
        return any([self.rq3_report, self.rq4_report, self.rq5_report])
    
    def get_llm_models(self) -> List[str]:
        """Get list of LLM models analyzed."""
        models = set()
        if self.rq3_report:
            # Prefer aggregate metrics when available, otherwise fall back to rankings.
            if getattr(self.rq3_report, "aggregate_metrics", None):
                models.update(self.rq3_report.aggregate_metrics.keys())
            if getattr(self.rq3_report, "llm_rankings", None):
                models.update(self.rq3_report.llm_rankings.keys())
        if self.rq4_report:
            if getattr(self.rq4_report, "model_results", None):
                models.update([r.llm_model for r in self.rq4_report.model_results])
            if getattr(self.rq4_report, "overall_rankings", None):
                models.update(self.rq4_report.overall_rankings.keys())
        if self.rq5_report:
            if getattr(self.rq5_report, "model_results", None):
                models.update([r.llm_model for r in self.rq5_report.model_results])
        return sorted(list(models))
    
    def to_dict(self) -> Dict:
        """Convert results to dictionary."""
        return {
            "rq3_code_quality": self.rq3_report.to_dict() if self.rq3_report else None,
            "rq4_llm_comparison": self.rq4_report.to_dict() if self.rq4_report else None,
            "rq5_completeness_impact": self.rq5_report.to_dict() if self.rq5_report else None
        }


@dataclass
class CrossRQAnalysis:
    """Cross-research question correlation and pattern analysis."""
    # Correlation matrices
    quality_vs_performance: Dict[str, float] = field(default_factory=dict)  # RQ3 vs RQ4
    quality_vs_completeness: Dict[str, float] = field(default_factory=dict)  # RQ3 vs RQ5
    performance_vs_robustness: Dict[str, float] = field(default_factory=dict)  # RQ4 vs RQ5
    
    # Pattern detection
    quality_leaders: List[str] = field(default_factory=list)  # Best for code quality
    cost_effective_models: List[str] = field(default_factory=list)  # Best quality/cost ratio
    robust_performers: List[str] = field(default_factory=list)  # Consistent across completeness
    
    # Trade-off analysis
    quality_cost_tradeoffs: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # (quality, cost)
    performance_robustness_tradeoffs: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    
    # Key findings
    key_findings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert analysis to dictionary."""
        return {
            "correlations": {
                "quality_vs_performance": self.quality_vs_performance,
                "quality_vs_completeness": self.quality_vs_completeness,
                "performance_vs_robustness": self.performance_vs_robustness
            },
            "patterns": {
                "quality_leaders": self.quality_leaders,
                "cost_effective_models": self.cost_effective_models,
                "robust_performers": self.robust_performers
            },
            "tradeoffs": {
                "quality_cost": {model: {"quality": qc[0], "cost": qc[1]} 
                               for model, qc in self.quality_cost_tradeoffs.items()},
                "performance_robustness": {model: {"performance": pr[0], "robustness": pr[1]} 
                                         for model, pr in self.performance_robustness_tradeoffs.items()}
            },
            "key_findings": self.key_findings
        }


@dataclass
class RQ345BatchReport:
    """Comprehensive report for unified RQ3/4/5 experiments."""
    experiment_id: str
    config: RQ345BatchConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    # Individual RQ results
    results: RQ345Results = field(default_factory=RQ345Results)
    
    # Cross-RQ analysis
    cross_rq_analysis: Optional[CrossRQAnalysis] = None
    
    # Execution metrics
    total_endpoints_analyzed: int = 0
    total_tests_generated: int = 0
    total_execution_time_seconds: float = 0.0
    
    # Overall rankings (across all dimensions)
    overall_model_rankings: Dict[str, int] = field(default_factory=dict)
    best_overall_model: str = ""
    
    # Recommendations
    recommendations: Dict[str, List[str]] = field(default_factory=dict)
    
    def generate_overall_rankings(self):
        """Generate overall model rankings across all RQs."""
        if not self.results.has_results():
            return
        
        models = self.results.get_llm_models()
        scores = {model: [] for model in models}
        
        # Collect scores from each RQ
        if self.results.rq3_report:
            for model in models:
                if model in self.results.rq3_report.llm_rankings:
                    rank = self.results.rq3_report.llm_rankings[model]
                    # Convert rank to normalized score (lower rank = higher score)
                    normalized_score = 1.0 - (rank - 1) / len(models)
                    scores[model].append(normalized_score * 0.33)  # 33% weight
        
        if self.results.rq4_report:
            for model in models:
                if model in self.results.rq4_report.overall_rankings:
                    rank = self.results.rq4_report.overall_rankings[model]
                    normalized_score = 1.0 - (rank - 1) / len(models)
                    scores[model].append(normalized_score * 0.33)  # 33% weight
        
        if self.results.rq5_report:
            # Use robustness score as proxy
            for result in self.results.rq5_report.model_results:
                if result.llm_model in scores:
                    scores[result.llm_model].append(result.robustness_score * 0.33)  # 33% weight
        
        # Calculate overall scores
        overall_scores = {model: sum(score_list) for model, score_list in scores.items() if score_list}
        
        # Rank models
        sorted_models = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
        self.overall_model_rankings = {model: rank + 1 for rank, (model, _) in enumerate(sorted_models)}
        self.best_overall_model = sorted_models[0][0] if sorted_models else ""
    
    def generate_recommendations(self):
        """Generate recommendations based on all RQ findings."""
        self.recommendations = {
            "code_quality": [],
            "model_selection": [],
            "documentation": [],
            "cost_optimization": []
        }
        
        # Code quality recommendations (from RQ3)
        if self.results.rq3_report:
            avg_quality = statistics.mean([
                metrics["mean_overall_quality"] 
                for metrics in self.results.rq3_report.aggregate_metrics.values()
            ])
            if avg_quality < 0.7:
                self.recommendations["code_quality"].append(
                    "Overall code quality below threshold (70%). Consider post-processing or manual review."
                )
        
        # Model selection recommendations (from RQ4)
        if self.results.rq4_report and self.best_overall_model:
            self.recommendations["model_selection"].append(
                f"Best overall model: {self.best_overall_model}. "
                f"Recommended for balanced performance across all dimensions."
            )
            
            # Cost-effective recommendation
            if self.results.rq4_report.best_for_cost:
                self.recommendations["cost_optimization"].append(
                    f"Most cost-effective: {self.results.rq4_report.best_for_cost}. "
                    f"Consider for budget-constrained projects."
                )
        
        # Documentation recommendations (from RQ5)
        if self.results.rq5_report:
            min_completeness = self.results.rq5_report.recommended_min_completeness
            if min_completeness > 0:
                self.recommendations["documentation"].append(
                    f"Maintain at least {min_completeness*100:.0f}% documentation completeness "
                    f"for acceptable test quality."
                )
            
            if self.results.rq5_report.most_robust_model:
                self.recommendations["documentation"].append(
                    f"For incomplete documentation scenarios, use {self.results.rq5_report.most_robust_model} "
                    f"(most robust to documentation gaps)."
                )
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "config": self.config.to_dict(),
            "timing": {
                "started_at": self.started_at.isoformat(),
                "completed_at": self.completed_at.isoformat() if self.completed_at else None,
                "total_execution_time_seconds": self.total_execution_time_seconds
            },
            "results": self.results.to_dict(),
            "cross_rq_analysis": self.cross_rq_analysis.to_dict() if self.cross_rq_analysis else None,
            "metrics": {
                "total_endpoints_analyzed": self.total_endpoints_analyzed,
                "total_tests_generated": self.total_tests_generated
            },
            "overall_rankings": {
                "rankings": self.overall_model_rankings,
                "best_overall": self.best_overall_model
            },
            "recommendations": self.recommendations
        }
    
    def save(self) -> Path:
        """Save report to JSON file."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.config.output_dir / f"rq345_report_{self.experiment_id}.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ345Orchestrator:
    """Unified orchestrator for RQ3, RQ4, and RQ5 experiments."""
    
    def __init__(self, config: RQ345BatchConfig):
        """Initialize orchestrator with configuration."""
        self.config = config
        self.report = RQ345BatchReport(
            experiment_id=config.experiment_id,
            config=config,
            started_at=datetime.utcnow()
        )
        
        # Initialize individual RQ runners
        self.rq3_runner = None
        self.rq4_runner = None
        self.rq5_runner = None
        
        if config.run_rq3 and config.rq3_config:
            self.rq3_runner = RQ3ExperimentRunner(config.rq3_config)
        
        if config.run_rq4 and config.rq4_config:
            self.rq4_runner = RQ4ExperimentRunner(config.rq4_config)
        
        if config.run_rq5 and config.rq5_config:
            self.rq5_runner = RQ5ExperimentRunner(config.rq5_config)
    
    async def run_batch_experiments(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest],
        rq5_data: Optional[Dict[float, Dict[str, Dict[str, any]]]] = None
    ) -> RQ345BatchReport:
        """
        Run all enabled research questions experiments.
        
        Args:
            endpoints: List of endpoint contexts
            oracles: Dictionary of oracles by endpoint UUID
            generated_tests: Dictionary of generated tests by endpoint UUID
            rq5_data: Optional RQ5 completeness data (nested dict by level and model)
        
        Returns:
            RQ345BatchReport with all results and analysis
        """
        start_time = datetime.utcnow()
        
        # Update metrics
        self.report.total_endpoints_analyzed = len(endpoints)
        self.report.total_tests_generated = len(generated_tests)
        
        # Run experiments
        if self.config.parallel_execution:
            await self._run_parallel_experiments(endpoints, oracles, generated_tests, rq5_data)
        else:
            await self._run_sequential_experiments(endpoints, oracles, generated_tests, rq5_data)
        
        # Perform cross-RQ analysis
        if self.config.analyze_correlations or self.config.analyze_patterns:
            self.report.cross_rq_analysis = await self._perform_cross_rq_analysis()
        
        # Generate overall rankings
        self.report.generate_overall_rankings()
        
        # Generate recommendations
        self.report.generate_recommendations()
        
        # Finalize report
        self.report.completed_at = datetime.utcnow()
        self.report.total_execution_time_seconds = (
            self.report.completed_at - start_time
        ).total_seconds()
        
        return self.report
    
    async def _run_parallel_experiments(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest],
        rq5_data: Optional[Dict] = None
    ):
        """Run experiments in parallel."""
        tasks = []
        
        if self.rq3_runner:
            tasks.append(self._run_rq3(endpoints, oracles, generated_tests))
        
        if self.rq4_runner:
            tasks.append(self._run_rq4(endpoints, oracles, generated_tests))
        
        if self.rq5_runner and rq5_data:
            tasks.append(self._run_rq5(rq5_data))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Experiment {i+1} failed: {result}")
    
    async def _run_sequential_experiments(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest],
        rq5_data: Optional[Dict] = None
    ):
        """Run experiments sequentially."""
        if self.rq3_runner:
            await self._run_rq3(endpoints, oracles, generated_tests)
        
        if self.rq4_runner:
            await self._run_rq4(endpoints, oracles, generated_tests)
        
        if self.rq5_runner and rq5_data:
            await self._run_rq5(rq5_data)
    
    async def _run_rq3(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest]
    ):
        """Run RQ3 code quality experiments."""
        print("Running RQ3: Code Quality Assessment...")
        self.report.results.rq3_report = await self.rq3_runner.run_experiment(
            endpoints, oracles, generated_tests
        )
        if self.config.save_intermediate_results:
            self.report.results.rq3_report.save()
        print(f"RQ3 completed: {len(self.report.results.rq3_report.endpoint_results)} endpoints analyzed")
    
    async def _run_rq4(
        self,
        endpoints: List[EndpointContext],
        oracles: Dict[UUID, Oracle],
        generated_tests: Dict[UUID, GeneratedTest]
    ):
        """Run RQ4 LLM comparison experiments."""
        print("Running RQ4: LLM Comparison...")
        self.report.results.rq4_report = await self.rq4_runner.run_experiment(
            endpoints, oracles, generated_tests
        )
        if self.config.save_intermediate_results:
            self.report.results.rq4_report.save()
        print(f"RQ4 completed: {len(self.report.results.rq4_report.model_results)} models compared")
    
    async def _run_rq5(self, rq5_data: Dict):
        """Run RQ5 completeness impact experiments."""
        print("Running RQ5: Completeness Impact Analysis...")
        self.report.results.rq5_report = await self.rq5_runner.run_experiment(rq5_data)
        if self.config.save_intermediate_results:
            self.report.results.rq5_report.save()
        print(f"RQ5 completed: {len(self.report.results.rq5_report.model_results)} models analyzed")
    
    async def _perform_cross_rq_analysis(self) -> CrossRQAnalysis:
        """Perform cross-research question analysis."""
        analysis = CrossRQAnalysis()
        
        if not self.report.results.has_results():
            return analysis
        
        models = self.report.results.get_llm_models()
        
        # Quality vs Performance correlation (RQ3 vs RQ4)
        if self.report.results.rq3_report and self.report.results.rq4_report:
            for model in models:
                rq3_metrics = self.report.results.rq3_report.aggregate_metrics.get(model, {})
                rq4_result = next(
                    (r for r in self.report.results.rq4_report.model_results if r.llm_model == model),
                    None
                )
                
                if rq3_metrics and rq4_result:
                    quality = rq3_metrics.get("mean_overall_quality", 0.0)
                    performance = 1.0 / (rq4_result.avg_generation_time_ms / 1000.0) if rq4_result.avg_generation_time_ms > 0 else 0.0
                    analysis.quality_vs_performance[model] = self._pearson_correlation(
                        [quality], [performance]
                    )
        
        # Quality vs Completeness correlation (RQ3 vs RQ5)
        if self.report.results.rq3_report and self.report.results.rq5_report:
            for model in models:
                rq5_result = next(
                    (r for r in self.report.results.rq5_report.model_results if r.llm_model == model),
                    None
                )
                if rq5_result:
                    analysis.quality_vs_completeness[model] = rq5_result.completeness_quality_correlation
        
        # Identify patterns
        self._identify_quality_leaders(analysis, models)
        self._identify_cost_effective_models(analysis, models)
        self._identify_robust_performers(analysis, models)
        
        # Analyze trade-offs
        self._analyze_quality_cost_tradeoffs(analysis, models)
        
        # Generate key findings
        self._generate_cross_rq_findings(analysis)
        
        return analysis
    
    def _identify_quality_leaders(self, analysis: CrossRQAnalysis, models: List[str]):
        """Identify models with best code quality."""
        if not self.report.results.rq3_report:
            return
        
        quality_scores = []
        for model in models:
            metrics = self.report.results.rq3_report.aggregate_metrics.get(model, {})
            if metrics:
                quality_scores.append((model, metrics.get("mean_overall_quality", 0.0)))
        
        quality_scores.sort(key=lambda x: x[1], reverse=True)
        # Top 3 or top 25%
        top_count = max(3, len(models) // 4)
        analysis.quality_leaders = [model for model, _ in quality_scores[:top_count]]
    
    def _identify_cost_effective_models(self, analysis: CrossRQAnalysis, models: List[str]):
        """Identify models with best quality/cost ratio."""
        if not self.report.results.rq4_report:
            return
        
        ratios = []
        for model in models:
            result = next(
                (r for r in self.report.results.rq4_report.model_results if r.llm_model == model),
                None
            )
            if result and result.total_cost_usd > 0:
                ratio = result.overall_score / result.total_cost_usd
                ratios.append((model, ratio))
        
        ratios.sort(key=lambda x: x[1], reverse=True)
        top_count = max(2, len(models) // 4)
        analysis.cost_effective_models = [model for model, _ in ratios[:top_count]]
    
    def _identify_robust_performers(self, analysis: CrossRQAnalysis, models: List[str]):
        """Identify models most robust to incomplete documentation."""
        if not self.report.results.rq5_report:
            return
        
        robustness_scores = []
        for result in self.report.results.rq5_report.model_results:
            robustness_scores.append((result.llm_model, result.robustness_score))
        
        robustness_scores.sort(key=lambda x: x[1], reverse=True)
        top_count = max(2, len(models) // 4)
        analysis.robust_performers = [model for model, _ in robustness_scores[:top_count]]
    
    def _analyze_quality_cost_tradeoffs(self, analysis: CrossRQAnalysis, models: List[str]):
        """Analyze quality vs cost trade-offs."""
        if not self.report.results.rq4_report:
            return
        
        for model in models:
            result = next(
                (r for r in self.report.results.rq4_report.model_results if r.llm_model == model),
                None
            )
            if result:
                analysis.quality_cost_tradeoffs[model] = (
                    result.overall_score,
                    result.total_cost_usd
                )
                analysis.performance_robustness_tradeoffs[model] = (
                    1.0 / result.avg_generation_time_ms if result.avg_generation_time_ms > 0 else 0.0,
                    0.0  # Placeholder for robustness
                )
        
        # Add robustness scores
        if self.report.results.rq5_report:
            for result in self.report.results.rq5_report.model_results:
                if result.llm_model in analysis.performance_robustness_tradeoffs:
                    perf, _ = analysis.performance_robustness_tradeoffs[result.llm_model]
                    analysis.performance_robustness_tradeoffs[result.llm_model] = (
                        perf, result.robustness_score
                    )
    
    def _generate_cross_rq_findings(self, analysis: CrossRQAnalysis):
        """Generate key findings from cross-RQ analysis."""
        if analysis.quality_leaders:
            analysis.key_findings.append(
                f"Quality leaders: {', '.join(analysis.quality_leaders[:3])} "
                f"consistently produce high-quality code across all metrics."
            )
        
        if analysis.cost_effective_models:
            analysis.key_findings.append(
                f"Most cost-effective: {', '.join(analysis.cost_effective_models[:2])} "
                f"offer best quality-to-cost ratio."
            )
        
        if analysis.robust_performers:
            analysis.key_findings.append(
                f"Most robust: {', '.join(analysis.robust_performers[:2])} "
                f"maintain quality even with incomplete documentation."
            )
    
    def _pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        try:
            mean_x = statistics.mean(x)
            mean_y = statistics.mean(y)
            
            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
            denominator_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
            denominator_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))
            
            if denominator_x == 0 or denominator_y == 0:
                return 0.0
            
            return numerator / (denominator_x * denominator_y) ** 0.5
        except Exception:
            return 0.0
    
    def get_summary(self) -> Dict:
        """Get summary of batch experiments."""
        return {
            "experiment_id": self.config.experiment_id,
            "models_evaluated": self.config.llm_models,
            "endpoints_analyzed": self.report.total_endpoints_analyzed,
            "tests_generated": self.report.total_tests_generated,
            "execution_time_seconds": self.report.total_execution_time_seconds,
            "best_overall_model": self.report.best_overall_model,
            "rq_completion": {
                "rq3_code_quality": self.report.results.rq3_report is not None,
                "rq4_llm_comparison": self.report.results.rq4_report is not None,
                "rq5_completeness_impact": self.report.results.rq5_report is not None
            },
            "cross_rq_analysis_completed": self.report.cross_rq_analysis is not None
        }
