"""
Oracle Metrics Module (RQ1 - Précision des Oracles)

This module measures the precision and completeness of generated oracles
by comparing them against ground truth and actual API responses.

Research Question 1: Quelle est la précision des oracles générés par les LLMs?

Metrics:
- Precision: How many generated validations are correct?
- Recall: How many actual validations were captured?
- F1-Score: Harmonic mean of precision and recall
- Completeness: Coverage of all validation aspects
- Confidence Accuracy: How well confidence scores predict correctness

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

from ..shared_context.models import Oracle, EndpointContext, TestExecutionResult


@dataclass
class ValidationAspect:
    """A specific aspect of validation (status, header, schema field, etc.)"""
    category: str  # "status_code", "header", "schema_field", "business_rule"
    name: str  # e.g., "Content-Type", "user.email", "status_code"
    expected_value: Any
    actual_value: Optional[Any] = None
    is_correct: Optional[bool] = None


@dataclass
class OraclePrecisionMetrics:
    """Metrics for oracle precision (RQ1)"""
    oracle_id: UUID
    endpoint_id: UUID
    
    # Core metrics
    precision: float  # TP / (TP + FP)
    recall: float  # TP / (TP + FN)
    f1_score: float  # 2 * (precision * recall) / (precision + recall)
    
    # Detailed counts
    true_positives: int  # Correct validations present
    false_positives: int  # Incorrect validations present
    false_negatives: int  # Missing validations
    true_negatives: int  # Correctly absent validations
    
    # By category
    status_code_correct: bool
    headers_precision: float
    schema_precision: float
    business_rules_precision: float
    
    # Completeness
    completeness_score: float  # % of expected validations covered
    missing_validations: List[str]
    extra_validations: List[str]
    
    # Confidence analysis
    predicted_confidence: float
    actual_accuracy: float
    confidence_calibration_error: float
    
    # Metadata
    llm_model: Optional[str]
    evaluated_at: datetime
    execution_result_id: Optional[UUID] = None


@dataclass
class GroundTruth:
    """Ground truth for an endpoint (manual annotations or real API data)"""
    endpoint_id: UUID
    
    # Expected validations
    status_code: int
    required_headers: Dict[str, str]
    optional_headers: Dict[str, str]
    response_schema: Dict[str, Any]
    business_rules: List[str]
    
    # Metadata
    source: str  # "manual", "api_call", "documentation"
    confidence: float
    annotator: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class OracleMetricsCalculator:
    """
    Calculates precision and completeness metrics for oracles (RQ1).
    
    Compares generated oracles against:
    1. Ground truth (manual annotations)
    2. Actual API responses
    3. Documentation specifications
    """
    
    def __init__(self):
        self.ground_truths: Dict[UUID, GroundTruth] = {}
    
    def add_ground_truth(self, ground_truth: GroundTruth) -> None:
        """Add ground truth for an endpoint."""
        self.ground_truths[ground_truth.endpoint_id] = ground_truth
    
    def calculate_metrics(
        self,
        oracle: Oracle,
        endpoint: EndpointContext,
        execution_result: Optional[TestExecutionResult] = None,
        ground_truth: Optional[GroundTruth] = None
    ) -> OraclePrecisionMetrics:
        """
        Calculate comprehensive precision metrics for an oracle.
        
        Args:
            oracle: The generated oracle to evaluate
            endpoint: The endpoint context
            execution_result: Optional execution result with actual values
            ground_truth: Optional ground truth, otherwise uses stored ground truth
        
        Returns:
            OraclePrecisionMetrics with all calculated metrics
        """
        # Get ground truth
        if ground_truth is None:
            ground_truth = self.ground_truths.get(endpoint.id)
        
        if ground_truth is None:
            raise ValueError(f"No ground truth found for endpoint {endpoint.id}")
        
        # Extract validation aspects
        generated_aspects = self._extract_oracle_aspects(oracle)
        expected_aspects = self._extract_ground_truth_aspects(ground_truth)
        
        # Compare with actual execution if available
        if execution_result:
            self._update_aspects_with_actual(generated_aspects, execution_result)
        
        # Calculate confusion matrix
        tp, fp, fn, tn = self._calculate_confusion_matrix(
            generated_aspects, expected_aspects
        )
        
        # Calculate core metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        
        # Calculate by category
        status_correct = self._check_status_code(oracle, ground_truth, execution_result)
        headers_prec = self._calculate_headers_precision(oracle, ground_truth)
        schema_prec = self._calculate_schema_precision(oracle, ground_truth)
        business_prec = self._calculate_business_rules_precision(oracle, ground_truth)
        
        # Calculate completeness
        completeness, missing, extra = self._calculate_completeness(
            generated_aspects, expected_aspects
        )
        
        # Confidence calibration
        conf_calibration = abs(oracle.confidence_score - precision)
        
        return OraclePrecisionMetrics(
            oracle_id=oracle.id,
            endpoint_id=endpoint.id,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            true_positives=tp,
            false_positives=fp,
            false_negatives=fn,
            true_negatives=tn,
            status_code_correct=status_correct,
            headers_precision=headers_prec,
            schema_precision=schema_prec,
            business_rules_precision=business_prec,
            completeness_score=completeness,
            missing_validations=missing,
            extra_validations=extra,
            predicted_confidence=oracle.confidence_score,
            actual_accuracy=precision,
            confidence_calibration_error=conf_calibration,
            llm_model=oracle.llm_model,
            evaluated_at=datetime.utcnow(),
            execution_result_id=execution_result.id if execution_result else None
        )
    
    def calculate_aggregate_metrics(
        self,
        metrics_list: List[OraclePrecisionMetrics]
    ) -> Dict[str, float]:
        """
        Calculate aggregate metrics across multiple oracles.
        
        Args:
            metrics_list: List of individual oracle metrics
        
        Returns:
            Dictionary with aggregate statistics
        """
        if not metrics_list:
            return {}
        
        n = len(metrics_list)
        
        return {
            # Averages
            "avg_precision": sum(m.precision for m in metrics_list) / n,
            "avg_recall": sum(m.recall for m in metrics_list) / n,
            "avg_f1_score": sum(m.f1_score for m in metrics_list) / n,
            "avg_completeness": sum(m.completeness_score for m in metrics_list) / n,
            
            # By category
            "avg_headers_precision": sum(m.headers_precision for m in metrics_list) / n,
            "avg_schema_precision": sum(m.schema_precision for m in metrics_list) / n,
            "avg_business_rules_precision": sum(m.business_rules_precision for m in metrics_list) / n,
            
            # Status code accuracy
            "status_code_accuracy": sum(1 for m in metrics_list if m.status_code_correct) / n,
            
            # Confidence calibration
            "avg_confidence_calibration_error": sum(m.confidence_calibration_error for m in metrics_list) / n,
            "avg_predicted_confidence": sum(m.predicted_confidence for m in metrics_list) / n,
            "avg_actual_accuracy": sum(m.actual_accuracy for m in metrics_list) / n,
            
            # Counts
            "total_oracles": n,
            "total_tp": sum(m.true_positives for m in metrics_list),
            "total_fp": sum(m.false_positives for m in metrics_list),
            "total_fn": sum(m.false_negatives for m in metrics_list),
            "total_tn": sum(m.true_negatives for m in metrics_list),
        }
    
    def compare_llm_models(
        self,
        metrics_by_model: Dict[str, List[OraclePrecisionMetrics]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare metrics across different LLM models.
        
        Args:
            metrics_by_model: Dictionary mapping model name to list of metrics
        
        Returns:
            Dictionary with comparison results per model
        """
        results = {}
        
        for model, metrics in metrics_by_model.items():
            results[model] = self.calculate_aggregate_metrics(metrics)
        
        return results
    
    # Private helper methods
    
    def _extract_oracle_aspects(self, oracle: Oracle) -> List[ValidationAspect]:
        """Extract all validation aspects from an oracle."""
        aspects = []
        
        # Status code
        aspects.append(ValidationAspect(
            category="status_code",
            name="status_code",
            expected_value=oracle.status_code
        ))
        
        # Headers
        for header in oracle.required_headers:
            constraint = oracle.header_constraints.get(header, {})
            aspects.append(ValidationAspect(
                category="header",
                name=header,
                expected_value=constraint
            ))
        
        # Schema fields (flatten nested structure)
        if oracle.response_schema:
            schema_aspects = self._flatten_schema(oracle.response_schema, "")
            aspects.extend(schema_aspects)
        
        # JSONPath assertions
        for path, assertion in oracle.json_path_assertions.items():
            aspects.append(ValidationAspect(
                category="jsonpath",
                name=path,
                expected_value=assertion
            ))
        
        # Business rules
        for i, rule in enumerate(oracle.business_rules):
            aspects.append(ValidationAspect(
                category="business_rule",
                name=f"rule_{i}",
                expected_value=rule
            ))
        
        return aspects
    
    def _extract_ground_truth_aspects(self, ground_truth: GroundTruth) -> List[ValidationAspect]:
        """Extract all validation aspects from ground truth."""
        aspects = []
        
        # Status code
        aspects.append(ValidationAspect(
            category="status_code",
            name="status_code",
            expected_value=ground_truth.status_code
        ))
        
        # Headers
        for header, value in ground_truth.required_headers.items():
            aspects.append(ValidationAspect(
                category="header",
                name=header,
                expected_value=value
            ))
        
        # Schema fields
        if ground_truth.response_schema:
            schema_aspects = self._flatten_schema(ground_truth.response_schema, "")
            aspects.extend(schema_aspects)
        
        # Business rules
        for i, rule in enumerate(ground_truth.business_rules):
            aspects.append(ValidationAspect(
                category="business_rule",
                name=f"rule_{i}",
                expected_value=rule
            ))
        
        return aspects
    
    def _coerce_schema_dict(self, schema: Any) -> Optional[Dict[str, Any]]:
        """Best-effort coercion of a schema payload to a dictionary.

        Some pipelines may bypass Pydantic validation (e.g., model_construct) and
        store `response_schema` as a JSON string. Metrics should be robust to that.
        """

        if schema is None:
            return None
        if isinstance(schema, dict):
            return schema
        if isinstance(schema, str):
            raw = schema.strip()
            if not raw:
                return None
            try:
                parsed = json.loads(raw)
            except Exception:
                return None
            return parsed if isinstance(parsed, dict) else None
        return None

    def _flatten_schema(self, schema: Any, prefix: str) -> List[ValidationAspect]:
        """Flatten nested schema into validation aspects."""
        aspects = []

        schema_dict = self._coerce_schema_dict(schema)
        if not schema_dict:
            return aspects

        properties = schema_dict.get("properties")
        if isinstance(properties, dict):
            for field, field_schema in properties.items():
                field_name = f"{prefix}.{field}" if prefix else field

                # Some schemas may encode a field schema as a simple type string
                if isinstance(field_schema, str):
                    field_schema = {"type": field_schema}
                if not isinstance(field_schema, dict):
                    continue
                
                # Type validation
                if "type" in field_schema:
                    aspects.append(ValidationAspect(
                        category="schema_field",
                        name=f"{field_name}.type",
                        expected_value=field_schema["type"]
                    ))
                
                # Nested object
                if field_schema.get("type") == "object" and "properties" in field_schema:
                    nested = self._flatten_schema(field_schema, field_name)
                    aspects.extend(nested)
        
        return aspects
    
    def _update_aspects_with_actual(
        self,
        aspects: List[ValidationAspect],
        execution_result: TestExecutionResult
    ) -> None:
        """Update aspects with actual values from execution."""
        for aspect in aspects:
            if aspect.category == "status_code":
                aspect.actual_value = execution_result.actual_status_code
                aspect.is_correct = (aspect.expected_value == aspect.actual_value)
            
            elif aspect.category == "header":
                actual_header = execution_result.actual_headers.get(aspect.name)
                aspect.actual_value = actual_header
                aspect.is_correct = self._compare_header_values(
                    aspect.expected_value, actual_header
                )
    
    def _compare_header_values(self, expected: Any, actual: Any) -> bool:
        """Compare header values with flexible matching."""
        if isinstance(expected, dict):
            # Constraint-based comparison
            if "pattern" in expected:
                import re
                return bool(re.match(expected["pattern"], str(actual)))
            if "value" in expected:
                return str(expected["value"]).lower() == str(actual).lower()
        
        return str(expected).lower() == str(actual).lower()
    
    def _calculate_confusion_matrix(
        self,
        generated: List[ValidationAspect],
        expected: List[ValidationAspect]
    ) -> Tuple[int, int, int, int]:
        """Calculate TP, FP, FN, TN."""
        generated_set = {(a.category, a.name) for a in generated}
        expected_set = {(a.category, a.name) for a in expected}
        
        tp = len(generated_set & expected_set)  # Present in both
        fp = len(generated_set - expected_set)  # In generated, not in expected
        fn = len(expected_set - generated_set)  # In expected, not in generated
        tn = 0  # Hard to define for validation rules
        
        return tp, fp, fn, tn
    
    def _check_status_code(
        self,
        oracle: Oracle,
        ground_truth: GroundTruth,
        execution_result: Optional[TestExecutionResult]
    ) -> bool:
        """Check if status code is correct."""
        if execution_result:
            return oracle.status_code == execution_result.actual_status_code
        return oracle.status_code == ground_truth.status_code
    
    def _calculate_headers_precision(
        self,
        oracle: Oracle,
        ground_truth: GroundTruth
    ) -> float:
        """Calculate precision for header validations."""
        if not ground_truth.required_headers:
            return 1.0
        
        generated_headers = set(oracle.required_headers)
        expected_headers = set(ground_truth.required_headers.keys())
        
        if not generated_headers:
            return 0.0
        
        correct = len(generated_headers & expected_headers)
        return correct / len(generated_headers)
    
    def _calculate_schema_precision(
        self,
        oracle: Oracle,
        ground_truth: GroundTruth
    ) -> float:
        """Calculate precision for schema validations."""
        if not ground_truth.response_schema:
            return 1.0
        
        if not oracle.response_schema:
            return 0.0
        
        generated_fields = self._get_schema_fields(oracle.response_schema)
        expected_fields = self._get_schema_fields(ground_truth.response_schema)
        
        if not generated_fields:
            return 0.0
        
        correct = len(generated_fields & expected_fields)
        return correct / len(generated_fields)
    
    def _get_schema_fields(self, schema: Any) -> Set[str]:
        """Extract all field paths from schema."""
        fields = set()

        schema_dict = self._coerce_schema_dict(schema)
        if not schema_dict:
            return fields

        def traverse(obj: Dict[str, Any], prefix: str = ""):
            props = obj.get("properties")
            if isinstance(props, dict):
                for key, value in props.items():
                    field_path = f"{prefix}.{key}" if prefix else key
                    fields.add(field_path)
                    if isinstance(value, dict) and value.get("type") == "object":
                        traverse(value, field_path)
        
        traverse(schema_dict)
        return fields
    
    def _calculate_business_rules_precision(
        self,
        oracle: Oracle,
        ground_truth: GroundTruth
    ) -> float:
        """Calculate precision for business rules."""
        if not ground_truth.business_rules:
            return 1.0
        
        if not oracle.business_rules:
            return 0.0
        
        # Simple exact match for now (could use semantic similarity)
        generated_rules = set(oracle.business_rules)
        expected_rules = set(ground_truth.business_rules)
        
        correct = len(generated_rules & expected_rules)
        return correct / len(generated_rules) if generated_rules else 0.0
    
    def _calculate_completeness(
        self,
        generated: List[ValidationAspect],
        expected: List[ValidationAspect]
    ) -> Tuple[float, List[str], List[str]]:
        """Calculate completeness score and identify missing/extra validations."""
        generated_set = {(a.category, a.name) for a in generated}
        expected_set = {(a.category, a.name) for a in expected}
        
        if not expected_set:
            return 1.0, [], []
        
        covered = len(generated_set & expected_set)
        completeness = covered / len(expected_set)
        
        missing = [f"{cat}:{name}" for cat, name in (expected_set - generated_set)]
        extra = [f"{cat}:{name}" for cat, name in (generated_set - expected_set)]
        
        return completeness, missing, extra
