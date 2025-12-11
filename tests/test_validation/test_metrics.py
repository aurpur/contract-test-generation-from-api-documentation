"""
Unit tests for validation metrics modules (RQ1-RQ5).

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import pytest
from datetime import datetime
from uuid import uuid4

from src.shared_context.models import (
    Oracle, EndpointContext, GeneratedTest, HTTPMethod, AuthType
)
from src.validation.oracle_metrics import (
    OracleMetricsCalculator, GroundTruth, ValidationAspect
)
from src.validation.inconsistency_detector import (
    InconsistencyDetector, InconsistencyType, InconsistencySeverity
)
from src.validation.test_quality_analyzer import TestQualityAnalyzer
from src.validation.llm_comparator import LLMComparator
from src.validation.completeness_analyzer import CompletenessAnalyzer


class TestOracleMetrics:
    """Tests for OracleMetricsCalculator (RQ1)."""
    
    def test_calculate_metrics_perfect_match(self):
        """Test metrics calculation with perfect oracle."""
        calculator = OracleMetricsCalculator()
        
        # Create endpoint
        endpoint = EndpointContext(
            name="Get User",
            method=HTTPMethod.GET,
            url="/api/users/1",
            documentation_completeness=1.0
        )
        
        # Create oracle
        oracle = Oracle(
            name="Get User Oracle",
            endpoint_id=endpoint.id,
            status_code=200,
            required_headers=["Content-Type"],
            response_schema={"type": "object", "properties": {"id": {"type": "integer"}}}
        )
        
        # Create ground truth (same as oracle)
        ground_truth = GroundTruth(
            endpoint_id=endpoint.id,
            status_code=200,
            required_headers={"Content-Type": "application/json"},
            optional_headers={},
            response_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            business_rules=[],
            source="manual"
        )
        
        # Calculate metrics
        metrics = calculator.calculate_metrics(oracle, endpoint, ground_truth=ground_truth)
        
        # Assertions
        assert metrics.precision == 1.0
        assert metrics.recall == 1.0
        assert metrics.f1_score == 1.0
        assert metrics.status_code_correct is True
        assert metrics.completeness_score == 1.0
    
    def test_calculate_metrics_with_missing_validations(self):
        """Test metrics with incomplete oracle."""
        calculator = OracleMetricsCalculator()
        
        endpoint = EndpointContext(
            name="Get User",
            method=HTTPMethod.GET,
            url="/api/users/1",
            documentation_completeness=0.5
        )
        
        # Oracle missing some validations
        oracle = Oracle(
            name="Get User Oracle",
            endpoint_id=endpoint.id,
            status_code=200,
            required_headers=[]  # Missing headers
        )
        
        # Complete ground truth
        ground_truth = GroundTruth(
            endpoint_id=endpoint.id,
            status_code=200,
            required_headers={"Content-Type": "application/json", "Cache-Control": "no-cache"},
            optional_headers={},
            response_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            business_rules=[],
            source="manual"
        )
        
        metrics = calculator.calculate_metrics(oracle, endpoint, ground_truth=ground_truth)
        
        # Should have low recall (missing validations)
        assert metrics.recall < 0.5
        assert len(metrics.missing_validations) > 0
    
    def test_aggregate_metrics(self):
        """Test aggregate metrics calculation."""
        calculator = OracleMetricsCalculator()
        
        # Create mock metrics
        from src.validation.oracle_metrics import OraclePrecisionMetrics
        metrics_list = [
            OraclePrecisionMetrics(
                oracle_id=uuid4(),
                endpoint_id=uuid4(),
                precision=0.9,
                recall=0.8,
                f1_score=0.85,
                true_positives=9,
                false_positives=1,
                false_negatives=2,
                true_negatives=0,
                status_code_correct=True,
                headers_precision=0.9,
                schema_precision=0.85,
                business_rules_precision=1.0,
                completeness_score=0.8,
                missing_validations=[],
                extra_validations=[],
                predicted_confidence=0.9,
                actual_accuracy=0.9,
                confidence_calibration_error=0.0,
                llm_model="gpt-4",
                evaluated_at=datetime.utcnow()
            )
            for _ in range(5)
        ]
        
        aggregate = calculator.calculate_aggregate_metrics(metrics_list)
        
        assert aggregate["avg_precision"] == 0.9
        assert aggregate["avg_recall"] == 0.8
        assert aggregate["avg_f1_score"] == 0.85
        assert aggregate["total_oracles"] == 5


class TestInconsistencyDetector:
    """Tests for InconsistencyDetector (RQ2)."""
    
    def test_detect_missing_status_code(self):
        """Test detection of missing status code validation."""
        detector = InconsistencyDetector()
        
        oracle = Oracle(
            name="Test Oracle",
            endpoint_id=uuid4(),
            status_code=200
        )
        
        # Test code missing status code assertion
        test = GeneratedTest(
            endpoint_id=oracle.endpoint_id,
            oracle_id=oracle.id,
            test_class_name="GetUserTest",
            test_method_name="testGetUser",
            test_code="@Test\npublic void testGetUser() {\n  // Missing statusCode assertion\n}",
            line_count=3,
            assertion_count=0
        )
        
        report = detector.detect_inconsistencies(oracle, test)
        
        # Should detect missing status code
        assert report.total_missing_validations >= 1
        assert any(inc.category == "status_code" for inc in report.critical)
    
    def test_detect_incorrect_status_code(self):
        """Test detection of incorrect status code."""
        detector = InconsistencyDetector()
        
        oracle = Oracle(
            name="Test Oracle",
            endpoint_id=uuid4(),
            status_code=200
        )
        
        # Test with wrong status code
        test = GeneratedTest(
            endpoint_id=oracle.endpoint_id,
            oracle_id=oracle.id,
            test_class_name="GetUserTest",
            test_method_name="testGetUser",
            test_code="@Test\npublic void testGetUser() {\n  .statusCode(404)\n}",
            line_count=3,
            assertion_count=1
        )
        
        report = detector.detect_inconsistencies(oracle, test)
        
        # Should detect incorrect value
        assert report.total_incorrect_implementations >= 1
        assert any(inc.type == InconsistencyType.INCORRECT_VALUE for inc in report.critical)
    
    def test_coherence_score_calculation(self):
        """Test coherence score calculation."""
        detector = InconsistencyDetector()
        
        oracle = Oracle(
            name="Test Oracle",
            endpoint_id=uuid4(),
            status_code=200,
            required_headers=["Content-Type"]
        )
        
        # Perfect test
        test = GeneratedTest(
            endpoint_id=oracle.endpoint_id,
            oracle_id=oracle.id,
            test_class_name="GetUserTest",
            test_method_name="testGetUser",
            test_code='@Test\npublic void testGetUser() {\n  .statusCode(200)\n  .header("Content-Type", equalTo("application/json"))\n}',
            line_count=4,
            assertion_count=2
        )
        
        report = detector.detect_inconsistencies(oracle, test)
        
        # Should have high coherence
        assert report.coherence_score > 0.8


class TestTestQualityAnalyzer:
    """Tests for TestQualityAnalyzer (RQ3)."""
    
    def test_analyze_high_quality_test(self):
        """Test analysis of a high-quality test."""
        analyzer = TestQualityAnalyzer()
        
        test = GeneratedTest(
            endpoint_id=uuid4(),
            oracle_id=uuid4(),
            test_class_name="GetUserTest",
            test_method_name="testGetUserReturns200",
            test_code="""
@Test
public void testGetUserReturns200() {
    // Arrange
    String userId = "123";
    
    // Act & Assert
    given()
        .pathParam("id", userId)
    .when()
        .get("/api/users/{id}")
    .then()
        .statusCode(200)
        .body("id", equalTo(123))
        .body("name", notNullValue());
}
""",
            line_count=15,
            assertion_count=3
        )
        
        report = analyzer.analyze_test_quality(test)
        
        # Should have good scores
        assert report.overall_quality_score > 0.6
        assert report.correctness_metrics.correctness_score > 0.5
        assert report.best_practices_metrics.proper_given_when_then is True
    
    def test_detect_code_smells(self):
        """Test detection of code smells."""
        analyzer = TestQualityAnalyzer()
        
        # Test with magic numbers
        test = GeneratedTest(
            endpoint_id=uuid4(),
            oracle_id=uuid4(),
            test_class_name="Test",
            test_method_name="test",
            test_code="@Test\npublic void test() { int x = 42; int y = 100; }",
            line_count=1,
            assertion_count=0
        )
        
        report = analyzer.analyze_test_quality(test)
        
        # Should detect issues
        assert len(report.critical_issues) > 0 or len(report.improvement_suggestions) > 0


class TestLLMComparator:
    """Tests for LLMComparator (RQ4)."""
    
    def test_add_and_compare_models(self):
        """Test adding metrics and comparing models."""
        comparator = LLMComparator()
        
        from src.validation.oracle_metrics import OraclePrecisionMetrics
        
        # Add metrics for two models
        gpt4_metrics = [
            OraclePrecisionMetrics(
                oracle_id=uuid4(),
                endpoint_id=uuid4(),
                precision=0.9,
                recall=0.85,
                f1_score=0.875,
                true_positives=9,
                false_positives=1,
                false_negatives=2,
                true_negatives=0,
                status_code_correct=True,
                headers_precision=0.9,
                schema_precision=0.9,
                business_rules_precision=0.9,
                completeness_score=0.85,
                missing_validations=[],
                extra_validations=[],
                predicted_confidence=0.9,
                actual_accuracy=0.9,
                confidence_calibration_error=0.0,
                llm_model="gpt-4",
                evaluated_at=datetime.utcnow()
            )
        ]
        
        claude_metrics = [
            OraclePrecisionMetrics(
                oracle_id=uuid4(),
                endpoint_id=uuid4(),
                precision=0.85,
                recall=0.80,
                f1_score=0.825,
                true_positives=8,
                false_positives=2,
                false_negatives=2,
                true_negatives=0,
                status_code_correct=True,
                headers_precision=0.85,
                schema_precision=0.85,
                business_rules_precision=0.85,
                completeness_score=0.80,
                missing_validations=[],
                extra_validations=[],
                predicted_confidence=0.85,
                actual_accuracy=0.85,
                confidence_calibration_error=0.0,
                llm_model="claude-3",
                evaluated_at=datetime.utcnow()
            )
        ]
        
        comparator.add_oracle_metrics("gpt-4", gpt4_metrics)
        comparator.add_oracle_metrics("claude-3", claude_metrics)
        
        comparison = comparator.compare_models()
        
        # GPT-4 should rank higher
        assert comparison.oracle_quality_ranking["gpt-4"] < comparison.oracle_quality_ranking["claude-3"]
        assert comparison.best_for_oracle_quality == "gpt-4"
    
    def test_generate_comparison_report(self):
        """Test report generation."""
        comparator = LLMComparator()
        
        from src.validation.oracle_metrics import OraclePrecisionMetrics
        
        metrics = [
            OraclePrecisionMetrics(
                oracle_id=uuid4(),
                endpoint_id=uuid4(),
                precision=0.9,
                recall=0.85,
                f1_score=0.875,
                true_positives=9,
                false_positives=1,
                false_negatives=2,
                true_negatives=0,
                status_code_correct=True,
                headers_precision=0.9,
                schema_precision=0.9,
                business_rules_precision=0.9,
                completeness_score=0.85,
                missing_validations=[],
                extra_validations=[],
                predicted_confidence=0.9,
                actual_accuracy=0.9,
                confidence_calibration_error=0.0,
                llm_model="gpt-4",
                evaluated_at=datetime.utcnow()
            )
        ]
        
        comparator.add_oracle_metrics("gpt-4", metrics)
        comparison = comparator.compare_models()
        
        report = comparator.generate_comparison_report(comparison)
        
        assert "LLM COMPARISON REPORT" in report
        assert "gpt-4" in report


class TestCompletenessAnalyzer:
    """Tests for CompletenessAnalyzer (RQ5)."""
    
    def test_completeness_correlation(self):
        """Test correlation calculation."""
        analyzer = CompletenessAnalyzer()
        
        from src.validation.oracle_metrics import OraclePrecisionMetrics
        from src.validation.test_quality_analyzer import (
            TestQualityReport, CorrectnessMetrics, ReadabilityMetrics,
            MaintainabilityMetrics, BestPracticesMetrics
        )
        
        # Add endpoints with varying completeness
        for completeness in [1.0, 0.8, 0.6, 0.4, 0.2]:
            endpoint = EndpointContext(
                name=f"Endpoint {completeness}",
                method=HTTPMethod.GET,
                url="/api/test",
                documentation_completeness=completeness
            )
            
            oracle = Oracle(
                name="Test Oracle",
                endpoint_id=endpoint.id,
                status_code=200,
                confidence_score=completeness
            )
            
            oracle_metrics = OraclePrecisionMetrics(
                oracle_id=oracle.id,
                endpoint_id=endpoint.id,
                precision=completeness * 0.9,  # Correlated with completeness
                recall=completeness * 0.85,
                f1_score=completeness * 0.875,
                true_positives=int(completeness * 10),
                false_positives=1,
                false_negatives=2,
                true_negatives=0,
                status_code_correct=True,
                headers_precision=completeness,
                schema_precision=completeness,
                business_rules_precision=completeness,
                completeness_score=completeness,
                missing_validations=[],
                extra_validations=[],
                predicted_confidence=completeness,
                actual_accuracy=completeness * 0.9,
                confidence_calibration_error=0.0,
                llm_model="gpt-4",
                evaluated_at=datetime.utcnow()
            )
            
            test = GeneratedTest(
                endpoint_id=endpoint.id,
                oracle_id=oracle.id,
                test_class_name="Test",
                test_method_name="test",
                test_code="@Test\npublic void test() {}",
                line_count=1,
                assertion_count=int(completeness * 5)
            )
            
            quality_report = TestQualityReport(
                test_id=test.id,
                correctness_metrics=CorrectnessMetrics(
                    valid_assertions=int(completeness * 5),
                    invalid_assertions=0,
                    proper_matchers=int(completeness * 5),
                    improper_matchers=0,
                    correct_framework_usage=True,
                    compilation_errors=0,
                    runtime_errors=0,
                    correctness_score=completeness * 0.9
                ),
                readability_metrics=ReadabilityMetrics(
                    lines_of_code=10,
                    comment_lines=2,
                    blank_lines=1,
                    avg_line_length=50.0,
                    max_line_length=80,
                    descriptive_names=5,
                    unclear_names=0,
                    logical_sections=3,
                    proper_indentation=True,
                    consistent_formatting=True,
                    has_javadoc=True,
                    has_inline_comments=True,
                    readability_score=completeness
                ),
                maintainability_metrics=MaintainabilityMetrics(
                    cyclomatic_complexity=5,
                    code_duplication_ratio=0.0,
                    number_of_methods=1,
                    avg_method_length=10.0,
                    max_method_length=10,
                    proper_setup_teardown=True,
                    reusable_helpers=0,
                    hardcoded_values=0,
                    maintainability_score=completeness
                ),
                best_practices_metrics=BestPracticesMetrics(
                    follows_aaa_pattern=True,
                    proper_test_naming=True,
                    single_assertion_principle=True,
                    proper_error_handling=True,
                    uses_test_data_builders=False,
                    proper_given_when_then=True,
                    correct_matcher_usage=True,
                    proper_authentication=True,
                    proper_annotations=True,
                    proper_assertions=True,
                    best_practices_score=completeness
                ),
                overall_quality_score=completeness * 0.9
            )
            
            analyzer.add_endpoint_metrics(endpoint, oracle, oracle_metrics, test, quality_report)
        
        report = analyzer.analyze()
        
        # Should show positive correlation
        assert report.completeness_precision_correlation > 0.7
        assert report.completeness_quality_correlation > 0.7
    
    def test_categorization(self):
        """Test completeness categorization."""
        analyzer = CompletenessAnalyzer()
        
        # Test private method
        assert analyzer._categorize_completeness(0.9) == "complete"
        assert analyzer._categorize_completeness(0.7) == "mostly_complete"
        assert analyzer._categorize_completeness(0.5) == "partial"
        assert analyzer._categorize_completeness(0.3) == "incomplete"
        assert analyzer._categorize_completeness(0.1) == "minimal"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
