"""
===============================================================================
RQ5 Completeness Impact Experiments - Documentation Quality Analysis
===============================================================================

OBJECTIF:
    Question de Recherche 5: "Quel est l'impact de la complétude de la 
    documentation sur la qualité des tests générés?"
    
    Ce module analyse la corrélation entre la complétude de la documentation API
    et la qualité des tests générés. Il évalue comment une documentation manquante
    ou incomplète affecte la précision des oracles et la qualité du code.

DIMENSIONS D'ANALYSE:
    - Niveaux de complétude: 100%, 75%, 50%, 25%, 10% (minimal)
    - Impact qualité: Corrélation complétude ↔ scores de qualité
    - Éléments manquants: Impact des codes status, headers, schémas absents
    - Robustesse LLM: Performance des modèles avec doc incomplète
    - Dégradation qualité: Taux de perte qualité par réduction doc
    - Identification seuils: Complétude minimale pour qualité acceptable

MODÈLES LLM:
    Ce module utilise UNIQUEMENT des modèles Ollama locaux :
    - deepseek_r1, deepseek_coder, codellama_7b
    - qwen25_7b, qwen25_coder_7b, llama31, llama32, mistral

IMPORTANT:
    - PAS de simulation - utilise les vrais agents avec datasets réels
    - PAS de modèles cloud (OpenAI, Anthropic, Google)

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

from src.shared_context.models import EndpointContext, GeneratedTest, Oracle
from src.validation.completeness_analyzer import (
    CompletenessAnalyzer,
    CompletenessAnalysisReport,
    CompletenessCategory,
    CompletenessImpactMetrics
)


@dataclass
class CompletenessExperimentConfig:
    """Configuration for RQ5 completeness impact experiments."""
    experiment_id: str
    name: str
    description: str
    llm_models: List[str]
    
    # Completeness levels to test
    completeness_levels: List[float] = field(default_factory=lambda: [1.0, 0.75, 0.5, 0.25, 0.1])
    
    # Minimum thresholds
    min_acceptable_completeness: float = 0.5  # 50%
    min_acceptable_quality: float = 0.7  # 70%
    
    # Analysis options
    analyze_correlations: bool = True
    analyze_missing_elements: bool = True
    analyze_llm_robustness: bool = True
    identify_thresholds: bool = True
    
    output_dir: Path = Path("experiments/results/rq5")
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "llm_models": self.llm_models,
            "completeness_levels": self.completeness_levels,
            "thresholds": {
                "min_acceptable_completeness": self.min_acceptable_completeness,
                "min_acceptable_quality": self.min_acceptable_quality
            },
            "analysis_options": {
                "correlations": self.analyze_correlations,
                "missing_elements": self.analyze_missing_elements,
                "llm_robustness": self.analyze_llm_robustness,
                "identify_thresholds": self.identify_thresholds
            },
            "output_dir": str(self.output_dir)
        }


@dataclass
class CompletenessLevelResult:
    """Results for a specific completeness level."""
    completeness_level: float  # 0.0 to 1.0
    completeness_category: str  # e.g., "complete", "mostly_complete", "partial"
    
    # Number of endpoints
    endpoint_count: int = 0
    
    # Quality metrics at this completeness level
    avg_oracle_precision: float = 0.0
    avg_oracle_recall: float = 0.0
    avg_oracle_f1: float = 0.0
    avg_oracle_confidence: float = 0.0
    
    avg_code_correctness: float = 0.0
    avg_code_readability: float = 0.0
    avg_code_maintainability: float = 0.0
    avg_code_overall_quality: float = 0.0
    
    avg_coherence_score: float = 0.0
    avg_inconsistency_count: float = 0.0
    
    # Overall quality at this level
    avg_overall_quality: float = 0.0
    
    # Missing elements statistics
    missing_elements: Dict[str, int] = field(default_factory=dict)
    
    def calculate_overall_quality(self):
        """Calculate overall quality score."""
        oracle_quality = (self.avg_oracle_precision + self.avg_oracle_recall + self.avg_oracle_f1) / 3.0
        code_quality = self.avg_code_overall_quality
        consistency_quality = self.avg_coherence_score
        
        self.avg_overall_quality = (
            oracle_quality * 0.35 +
            code_quality * 0.35 +
            consistency_quality * 0.30
        )
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            "completeness_level": self.completeness_level,
            "completeness_category": self.completeness_category,
            "endpoint_count": self.endpoint_count,
            "oracle_metrics": {
                "precision": self.avg_oracle_precision,
                "recall": self.avg_oracle_recall,
                "f1": self.avg_oracle_f1,
                "confidence": self.avg_oracle_confidence
            },
            "code_quality_metrics": {
                "correctness": self.avg_code_correctness,
                "readability": self.avg_code_readability,
                "maintainability": self.avg_code_maintainability,
                "overall": self.avg_code_overall_quality
            },
            "consistency_metrics": {
                "coherence_score": self.avg_coherence_score,
                "avg_inconsistency_count": self.avg_inconsistency_count
            },
            "overall_quality": self.avg_overall_quality,
            "missing_elements": self.missing_elements
        }


@dataclass
class ModelCompletenessResult:
    """Completeness impact results for a single LLM model."""
    llm_model: str
    
    # Results per completeness level
    level_results: List[CompletenessLevelResult] = field(default_factory=list)
    
    # Correlation coefficients (Pearson)
    completeness_quality_correlation: float = 0.0
    completeness_precision_correlation: float = 0.0
    completeness_recall_correlation: float = 0.0
    
    # Quality degradation analysis
    quality_degradation_rate: float = 0.0  # Quality drop per 10% completeness loss
    precision_degradation_rate: float = 0.0
    recall_degradation_rate: float = 0.0
    
    # Threshold analysis
    min_completeness_for_quality_80: float = 0.0  # Minimum completeness for 80% quality
    min_completeness_for_precision_80: float = 0.0
    min_completeness_for_recall_80: float = 0.0
    
    # Robustness score
    robustness_score: float = 0.0  # How well model handles incomplete docs (0-1)
    
    def calculate_correlations(self):
        """Calculate correlation coefficients."""
        if len(self.level_results) < 2:
            return
        
        completeness_values = [r.completeness_level for r in self.level_results]
        quality_values = [r.avg_overall_quality for r in self.level_results]
        precision_values = [r.avg_oracle_precision for r in self.level_results]
        recall_values = [r.avg_oracle_recall for r in self.level_results]
        
        self.completeness_quality_correlation = self._pearson_correlation(
            completeness_values, quality_values
        )
        self.completeness_precision_correlation = self._pearson_correlation(
            completeness_values, precision_values
        )
        self.completeness_recall_correlation = self._pearson_correlation(
            completeness_values, recall_values
        )
    
    def calculate_degradation_rates(self):
        """Calculate quality degradation rates."""
        if len(self.level_results) < 2:
            return
        
        # Sort by completeness level (descending)
        sorted_results = sorted(self.level_results, key=lambda x: x.completeness_level, reverse=True)
        
        # Calculate average degradation per 10% completeness drop
        quality_drops = []
        precision_drops = []
        recall_drops = []
        
        for i in range(len(sorted_results) - 1):
            current = sorted_results[i]
            next_level = sorted_results[i + 1]
            
            completeness_drop = (current.completeness_level - next_level.completeness_level) * 100
            if completeness_drop > 0:
                quality_drop = (current.avg_overall_quality - next_level.avg_overall_quality) / (completeness_drop / 10)
                precision_drop = (current.avg_oracle_precision - next_level.avg_oracle_precision) / (completeness_drop / 10)
                recall_drop = (current.avg_oracle_recall - next_level.avg_oracle_recall) / (completeness_drop / 10)

                # Degradation rate is a magnitude; clamp negatives to 0 (no degradation).
                quality_drops.append(max(0.0, quality_drop))
                precision_drops.append(max(0.0, precision_drop))
                recall_drops.append(max(0.0, recall_drop))
        
        if quality_drops:
            self.quality_degradation_rate = statistics.mean(quality_drops)
            self.precision_degradation_rate = statistics.mean(precision_drops)
            self.recall_degradation_rate = statistics.mean(recall_drops)
    
    def identify_thresholds(self):
        """Identify minimum completeness thresholds for target quality levels."""
        # Sort by completeness level
        sorted_results = sorted(self.level_results, key=lambda x: x.completeness_level)
        
        # Find minimum completeness for 80% quality
        for result in sorted_results:
            if result.avg_overall_quality >= 0.8 and self.min_completeness_for_quality_80 == 0.0:
                self.min_completeness_for_quality_80 = result.completeness_level
            if result.avg_oracle_precision >= 0.8 and self.min_completeness_for_precision_80 == 0.0:
                self.min_completeness_for_precision_80 = result.completeness_level
            if result.avg_oracle_recall >= 0.8 and self.min_completeness_for_recall_80 == 0.0:
                self.min_completeness_for_recall_80 = result.completeness_level
    
    def calculate_robustness(self):
        """Calculate robustness score based on performance with incomplete docs."""
        if not self.level_results:
            return
        
        # Robustness = how well quality is maintained at lower completeness levels
        # Compare quality at 50% completeness to quality at 100% completeness
        
        result_50 = next((r for r in self.level_results if abs(r.completeness_level - 0.5) < 0.1), None)
        result_100 = next((r for r in self.level_results if abs(r.completeness_level - 1.0) < 0.1), None)
        
        if result_50 and result_100 and result_100.avg_overall_quality > 0:
            # Robustness = quality retention ratio
            self.robustness_score = result_50.avg_overall_quality / result_100.avg_overall_quality
        else:
            # Alternative: average quality across all incomplete levels
            incomplete_results = [r for r in self.level_results if r.completeness_level < 1.0]
            if incomplete_results:
                avg_incomplete_quality = statistics.mean([r.avg_overall_quality for r in incomplete_results])
                complete_result = next((r for r in self.level_results if r.completeness_level >= 0.9), None)
                if complete_result and complete_result.avg_overall_quality > 0:
                    self.robustness_score = avg_incomplete_quality / complete_result.avg_overall_quality
    
    def _pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        denominator_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        
        if denominator_x == 0 or denominator_y == 0:
            return 0.0
        
        return numerator / (denominator_x * denominator_y) ** 0.5
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            "llm_model": self.llm_model,
            "level_results": [r.to_dict() for r in self.level_results],
            "correlations": {
                "completeness_quality": self.completeness_quality_correlation,
                "completeness_precision": self.completeness_precision_correlation,
                "completeness_recall": self.completeness_recall_correlation
            },
            "degradation_rates": {
                "quality_per_10pct": self.quality_degradation_rate,
                "precision_per_10pct": self.precision_degradation_rate,
                "recall_per_10pct": self.recall_degradation_rate
            },
            "thresholds": {
                "min_for_quality_80": self.min_completeness_for_quality_80,
                "min_for_precision_80": self.min_completeness_for_precision_80,
                "min_for_recall_80": self.min_completeness_for_recall_80
            },
            "robustness_score": self.robustness_score
        }


@dataclass
class CompletenessExperimentReport:
    """Aggregate report for RQ5 completeness impact experiments."""
    experiment_id: str
    config: CompletenessExperimentConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    # Results per model
    model_results: List[ModelCompletenessResult] = field(default_factory=list)
    
    # Overall findings
    avg_completeness_quality_correlation: float = 0.0
    most_impactful_missing_elements: List[Tuple[str, float]] = field(default_factory=list)
    most_robust_model: str = ""
    least_robust_model: str = ""
    
    # Recommendations
    recommended_min_completeness: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    
    def calculate_overall_findings(self):
        """Calculate overall findings across all models."""
        if not self.model_results:
            return
        
        # Average correlation across models
        correlations = [r.completeness_quality_correlation for r in self.model_results]
        self.avg_completeness_quality_correlation = statistics.mean(correlations) if correlations else 0.0
        
        # Identify most robust model
        robustness_scores = [(r.llm_model, r.robustness_score) for r in self.model_results]
        robustness_scores.sort(key=lambda x: x[1], reverse=True)
        self.most_robust_model = robustness_scores[0][0] if robustness_scores else ""
        self.least_robust_model = robustness_scores[-1][0] if robustness_scores else ""
        
        # Recommended minimum completeness (average across models)
        thresholds = [r.min_completeness_for_quality_80 for r in self.model_results if r.min_completeness_for_quality_80 > 0]
        self.recommended_min_completeness = statistics.mean(thresholds) if thresholds else 0.5
        
        # Generate recommendations
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Generate actionable recommendations."""
        self.recommendations = []
        
        if self.avg_completeness_quality_correlation > 0.7:
            self.recommendations.append(
                f"Strong correlation ({self.avg_completeness_quality_correlation:.2f}) found between "
                "documentation completeness and test quality. Prioritize complete documentation."
            )
        
        if self.recommended_min_completeness > 0:
            self.recommendations.append(
                f"Maintain at least {self.recommended_min_completeness*100:.0f}% documentation "
                "completeness to achieve 80% quality threshold."
            )
        
        if self.most_robust_model:
            self.recommendations.append(
                f"For projects with incomplete documentation, consider using {self.most_robust_model} "
                f"(robustness score: {next(r.robustness_score for r in self.model_results if r.llm_model == self.most_robust_model):.2f})."
            )
        
        # Check degradation rates
        avg_degradation = statistics.mean([r.quality_degradation_rate for r in self.model_results])
        if avg_degradation > 0.05:
            self.recommendations.append(
                f"Quality degrades by {avg_degradation:.2f} points per 10% documentation loss. "
                "Even small documentation gaps can significantly impact quality."
            )
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "config": self.config.to_dict(),
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "model_results": [r.to_dict() for r in self.model_results],
            "overall_findings": {
                "avg_correlation": self.avg_completeness_quality_correlation,
                "most_robust_model": self.most_robust_model,
                "least_robust_model": self.least_robust_model,
                "recommended_min_completeness": self.recommended_min_completeness
            },
            "recommendations": self.recommendations
        }
    
    def save(self) -> Path:
        """Save report to JSON file."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.config.output_dir / f"rq5_report_{self.experiment_id}.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ5ExperimentRunner:
    """Main runner for RQ5 completeness impact experiments."""
    
    def __init__(self, config: CompletenessExperimentConfig):
        """Initialize experiment runner."""
        self.config = config
        self.analyzer = CompletenessAnalyzer()
        self.report = CompletenessExperimentReport(
            experiment_id=config.experiment_id,
            config=config,
            started_at=datetime.utcnow()
        )
    
    async def run_experiment(
        self,
        results_by_completeness_and_model: Dict[float, Dict[str, Dict[str, any]]]
    ) -> CompletenessExperimentReport:
        """
        Run completeness impact experiment.
        
        Args:
            results_by_completeness_and_model: Nested dictionary structure:
                {completeness_level: {model_name: {results_data}}}
        
        Returns:
            CompletenessExperimentReport with analysis
        """
        # Analyze each model's response to completeness variation
        for model_name in self.config.llm_models:
            result = await self._analyze_model_completeness_impact(
                model_name,
                results_by_completeness_and_model
            )
            self.report.model_results.append(result)
        
        # Calculate overall findings
        self.report.calculate_overall_findings()
        self.report.completed_at = datetime.utcnow()
        
        return self.report
    
    async def _analyze_model_completeness_impact(
        self,
        model_name: str,
        results_by_completeness: Dict[float, Dict[str, Dict[str, any]]]
    ) -> ModelCompletenessResult:
        """Analyze completeness impact for a single LLM model."""
        result = ModelCompletenessResult(llm_model=model_name)
        
        # Analyze results at each completeness level
        for completeness_level in sorted(self.config.completeness_levels, reverse=True):
            if completeness_level not in results_by_completeness:
                continue
            
            model_data = results_by_completeness[completeness_level].get(model_name, {})
            if not model_data:
                continue
            
            level_result = self._analyze_completeness_level(
                completeness_level,
                model_data
            )
            result.level_results.append(level_result)
        
        # Calculate correlations
        if self.config.analyze_correlations:
            result.calculate_correlations()
        
        # Calculate degradation rates
        result.calculate_degradation_rates()
        
        # Identify thresholds
        if self.config.identify_thresholds:
            result.identify_thresholds()
        
        # Calculate robustness
        if self.config.analyze_llm_robustness:
            result.calculate_robustness()
        
        return result
    
    def _analyze_completeness_level(
        self,
        completeness_level: float,
        model_data: Dict[str, any]
    ) -> CompletenessLevelResult:
        """Analyze results at a specific completeness level."""
        # Determine completeness category
        if completeness_level >= 0.8:
            category = "complete"
        elif completeness_level >= 0.6:
            category = "mostly_complete"
        elif completeness_level >= 0.4:
            category = "partial"
        elif completeness_level >= 0.2:
            category = "incomplete"
        else:
            category = "minimal"
        
        level_result = CompletenessLevelResult(
            completeness_level=completeness_level,
            completeness_category=category
        )
        
        # Extract metrics from model data
        oracles = model_data.get('oracles', [])
        quality_reports = model_data.get('quality_reports', [])
        consistency_reports = model_data.get('consistency_reports', [])
        
        level_result.endpoint_count = len(oracles)
        
        # Oracle metrics
        if oracles:
            level_result.avg_oracle_precision = statistics.mean([o.get('precision', 0.0) for o in oracles])
            level_result.avg_oracle_recall = statistics.mean([o.get('recall', 0.0) for o in oracles])
            level_result.avg_oracle_f1 = statistics.mean([o.get('f1', 0.0) for o in oracles])
            level_result.avg_oracle_confidence = statistics.mean([o.get('confidence', 0.0) for o in oracles])
        
        # Code quality metrics
        if quality_reports:
            level_result.avg_code_correctness = statistics.mean([q.get('correctness', 0.0) for q in quality_reports])
            level_result.avg_code_readability = statistics.mean([q.get('readability', 0.0) for q in quality_reports])
            level_result.avg_code_maintainability = statistics.mean([q.get('maintainability', 0.0) for q in quality_reports])
            level_result.avg_code_overall_quality = statistics.mean([q.get('overall', 0.0) for q in quality_reports])
        
        # Consistency metrics
        if consistency_reports:
            level_result.avg_coherence_score = statistics.mean([c.get('coherence_score', 0.0) for c in consistency_reports])
            level_result.avg_inconsistency_count = statistics.mean([c.get('inconsistency_count', 0) for c in consistency_reports])
        
        # Calculate overall quality
        level_result.calculate_overall_quality()
        
        # Extract missing elements
        level_result.missing_elements = model_data.get('missing_elements', {})
        
        return level_result
    
    def get_summary(self) -> Dict:
        """Get summary of experiment results."""
        if not self.report.model_results:
            return {"status": "No results available"}
        
        return {
            "models_analyzed": len(self.report.model_results),
            "completeness_levels_tested": len(self.config.completeness_levels),
            "avg_correlation": self.report.avg_completeness_quality_correlation,
            "most_robust_model": self.report.most_robust_model,
            "recommended_min_completeness": self.report.recommended_min_completeness,
            "key_recommendations": self.report.recommendations[:3]
        }
