"""
Validation and metrics for research questions (RQ1-RQ5).

This package contains modules for evaluating the quality of generated oracles
and test code, addressing the five research questions:

RQ1: Quelle est la précision des oracles générés par les LLMs?
RQ2: Le code généré est-il cohérent avec les oracles dérivés?
RQ3: Quelle est la qualité du code de test généré?
RQ4: Quel LLM génère les meilleurs tests de contrat?
RQ5: Comment la complétude de la documentation impacte-t-elle la qualité?

Modules:
- oracle_metrics: Oracle precision and completeness metrics (RQ1)
- inconsistency_detector: Oracle-code consistency checks (RQ2)
- test_quality_analyzer: Test code quality analysis (RQ3)
- llm_comparator: LLM performance comparison (RQ4)
- completeness_analyzer: Documentation completeness impact (RQ5)

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""

from .oracle_metrics import (
    OracleMetricsCalculator,
    OraclePrecisionMetrics,
    GroundTruth,
    ValidationAspect
)
from .inconsistency_detector import (
    InconsistencyDetector,
    InconsistencyReport,
    Inconsistency,
    InconsistencyType,
    InconsistencySeverity
)
from .test_quality_analyzer import (
    TestQualityAnalyzer,
    TestQualityReport,
    CorrectnessMetrics,
    ReadabilityMetrics,
    MaintainabilityMetrics,
    BestPracticesMetrics
)
from .llm_comparator import (
    LLMComparator,
    LLMComparison,
    LLMPerformanceMetrics
)
from .completeness_analyzer import (
    CompletenessAnalyzer,
    CompletenessAnalysisReport,
    CompletenessImpactMetrics,
    CompletenessCategory
)

__all__ = [
    # RQ1 - Oracle Metrics
    "OracleMetricsCalculator",
    "OraclePrecisionMetrics",
    "GroundTruth",
    "ValidationAspect",
    
    # RQ2 - Inconsistency Detection
    "InconsistencyDetector",
    "InconsistencyReport",
    "Inconsistency",
    "InconsistencyType",
    "InconsistencySeverity",
    
    # RQ3 - Test Quality
    "TestQualityAnalyzer",
    "TestQualityReport",
    "CorrectnessMetrics",
    "ReadabilityMetrics",
    "MaintainabilityMetrics",
    "BestPracticesMetrics",
    
    # RQ4 - LLM Comparison
    "LLMComparator",
    "LLMComparison",
    "LLMPerformanceMetrics",
    
    # RQ5 - Completeness Impact
    "CompletenessAnalyzer",
    "CompletenessAnalysisReport",
    "CompletenessImpactMetrics",
    "CompletenessCategory",
]
