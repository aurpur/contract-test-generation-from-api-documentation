"""
Unit Tests for RQ2 Consistency Validation Modules

Tests for:
- rq2_consistency_validation.py (RQ2ExperimentRunner)
- rq2_orchestrator.py (RQ2Orchestrator)
- rq2_reporting.py (RQ2ReportGenerator)
- Integration with inconsistency_detector.py

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import json
import pytest
import asyncio
from pathlib import Path
from uuid import UUID, uuid4
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from experiments.rq2_consistency_validation import (
    ConsistencyExperimentConfig,
    EndpointConsistencyResult,
    ConsistencyExperimentReport,
    RQ2ExperimentRunner
)
from experiments.rq2_orchestrator import (
    BatchConsistencyConfig,
    BatchConsistencyResults,
    RQ2Orchestrator,
    InconsistencyPattern,
    ConsistencyPatternAnalysis
)
from experiments.rq2_reporting import RQ2ReportGenerator

from src.shared_context.models import (
    EndpointContext,
    Oracle,
    GeneratedTest,
    HTTPMethod,
    AuthType
)
from src.validation.inconsistency_detector import (
    InconsistencyDetector,
    InconsistencyReport,
    Inconsistency,
    InconsistencyType,
    InconsistencySeverity
)


# Helper functions for test data
def create_sample_endpoint() -> EndpointContext:
    """Create a sample endpoint for testing."""
    return EndpointContext(
        id=uuid4(),
        name="Get User",
        method=HTTPMethod.GET,
        url="/api/users/{id}",
        path_params=["id"],
        description="Retrieve user information by ID",
        documentation_completeness=1.0
    )


def create_sample_oracle(endpoint_id: UUID) -> Oracle:
    """Create a sample oracle for testing."""
    return Oracle(
        id=uuid4(),
        endpoint_id=endpoint_id,
        name="Oracle for Get User",
        description="Validates user retrieval endpoint",
        status_code=200,
        required_headers=["Content-Type: application/json"],
        response_schema={
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["id", "name", "email"]
        },
        jsonpath_assertions=[
            {"path": "$.id", "expected_type": "integer"},
            {"path": "$.name", "expected_type": "string"}
        ],
        business_rules=["User ID must be positive"],
        confidence=0.9
    )


def create_sample_generated_test(endpoint_id: UUID) -> GeneratedTest:
    """Create a sample generated test for testing."""
    java_code = '''
@Test
public void testGetUser() {
    given()
        .pathParam("id", 1)
    .when()
        .get("/api/users/{id}")
    .then()
        .statusCode(200)
        .header("Content-Type", "application/json")
        .body("id", notNullValue())
        .body("name", notNullValue());
}
'''
    
    gherkin_code = '''
Scenario: Retrieve user by ID
    Given the user ID is 1
    When I send a GET request to "/api/users/{id}"
    Then the response status code should be 200
    And the response header "Content-Type" should be "application/json"
    And the response should contain field "id"
    And the response should contain field "name"
'''
    
    return GeneratedTest(
        id=uuid4(),
        oracle_id=uuid4(),
        endpoint_id=endpoint_id,
        name="testGetUser",
        test_class_name="UserApiTest",
        test_method_name="testGetUser",
        test_code=java_code,
        java_code=java_code,
        gherkin_code=gherkin_code,
        framework="rest-assured",
        confidence=0.85
    )


class TestConsistencyExperimentConfig:
    """Tests for ConsistencyExperimentConfig dataclass."""
    
    def test_config_creation(self):
        """Test creating consistency experiment configuration."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test_001",
            name="RQ2 Test Experiment",
            description="Test consistency validation",
            llm_models=["gpt-4", "claude-3-opus"],
            num_endpoints=5,
            min_coherence_score=0.8
        )
        
        assert config.experiment_id == "rq2_test_001"
        assert len(config.llm_models) == 2
        assert config.num_endpoints == 5
        assert config.min_coherence_score == 0.8
    
    def test_config_default_values(self):
        """Test default values in configuration."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test_002",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=10
        )
        
        assert config.min_coherence_score == 0.8  # default
        assert config.max_critical_inconsistencies == 0  # default
        assert config.max_major_inconsistencies == 2  # default
        assert "rest-assured" in config.test_frameworks
        assert "gherkin" in config.test_frameworks


class TestEndpointConsistencyResult:
    """Tests for EndpointConsistencyResult dataclass."""
    
    def test_result_creation(self):
        """Test creating endpoint consistency result."""
        endpoint_id = uuid4()
        
        result = EndpointConsistencyResult(
            endpoint_id=endpoint_id,
            endpoint_name="Test Endpoint",
            llm_model="gpt-4",
            coherence_score=0.85,
            java_coverage_ratio=0.9,
            gherkin_coverage_ratio=0.8
        )
        
        assert result.endpoint_id == endpoint_id
        assert result.coherence_score == 0.85
        assert result.llm_model == "gpt-4"
    
    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        endpoint_id = uuid4()
        
        result = EndpointConsistencyResult(
            endpoint_id=endpoint_id,
            endpoint_name="Test Endpoint",
            coherence_score=0.85
        )
        
        data = result.to_dict()
        
        assert "endpoint_id" in data
        assert "coherence_score" in data
        assert data["coherence_score"] == 0.85
        assert "inconsistency_counts" in data
        assert "quality_flags" in data
    
    def test_calculate_derived_metrics(self):
        """Test calculating derived metrics from inconsistency report."""
        endpoint_id = uuid4()
        oracle = create_sample_oracle(endpoint_id)
        test = create_sample_generated_test(endpoint_id)
        
        # Create mock inconsistency report
        inconsistency_report = InconsistencyReport(
            test_id=test.id,
            oracle_id=oracle.id,
            coherence_score=0.75,
            java_coverage_ratio=0.8,
            gherkin_coverage_ratio=0.7
        )
        
        # Add some inconsistencies
        critical_inc = Inconsistency(
            type=InconsistencyType.MISSING_VALIDATION,
            severity=InconsistencySeverity.CRITICAL,
            category="status_code",
            field_name="status_code",
            recommendation="Add status code validation"
        )
        inconsistency_report.add_inconsistency(critical_inc)
        
        major_inc = Inconsistency(
            type=InconsistencyType.MISSING_VALIDATION,
            severity=InconsistencySeverity.MAJOR,
            category="header",
            field_name="Content-Type",
            recommendation="Add header validation"
        )
        inconsistency_report.add_inconsistency(major_inc)
        
        # Create result and calculate metrics
        result = EndpointConsistencyResult(
            endpoint_id=endpoint_id,
            endpoint_name="Test Endpoint",
            inconsistency_report=inconsistency_report
        )
        
        result.calculate_derived_metrics()
        
        assert result.critical_count == 1
        assert result.major_count == 1
        assert result.minor_count == 0
        assert result.missing_validations == 2
        assert result.coherence_score == 0.75
        assert result.has_critical_issues == True
        assert result.has_major_issues == True


class TestConsistencyExperimentReport:
    """Tests for ConsistencyExperimentReport dataclass."""
    
    def test_report_creation(self):
        """Test creating consistency experiment report."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=5
        )
        
        report = ConsistencyExperimentReport(
            experiment_id="rq2_test",
            config=config,
            started_at=datetime.utcnow()
        )
        
        assert report.experiment_id == "rq2_test"
        assert report.total_endpoints == 0
        assert len(report.endpoint_results) == 0
    
    def test_report_calculate_aggregates(self):
        """Test calculating aggregate metrics."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=2
        )
        
        report = ConsistencyExperimentReport(
            experiment_id="rq2_test",
            config=config,
            started_at=datetime.utcnow(),
            total_endpoints=2
        )
        
        # Add sample results
        result1 = EndpointConsistencyResult(
            endpoint_id=uuid4(),
            endpoint_name="Endpoint 1",
            llm_model="gpt-4",
            coherence_score=0.9,
            java_coverage_ratio=0.95,
            gherkin_coverage_ratio=0.85,
            critical_count=0,
            major_count=1,
            minor_count=2,
            passes_threshold=True
        )
        
        result2 = EndpointConsistencyResult(
            endpoint_id=uuid4(),
            endpoint_name="Endpoint 2",
            llm_model="gpt-4",
            coherence_score=0.85,
            java_coverage_ratio=0.9,
            gherkin_coverage_ratio=0.8,
            critical_count=1,
            major_count=0,
            minor_count=1,
            passes_threshold=False,
            has_critical_issues=True
        )
        
        report.endpoint_results = [result1, result2]
        report.calculate_aggregates()
        
        assert "gpt-4" in report.aggregate_metrics
        metrics = report.aggregate_metrics["gpt-4"]
        
        assert metrics["coherence_mean"] == 0.875  # (0.9 + 0.85) / 2
        assert metrics["java_coverage_mean"] == 0.925  # (0.95 + 0.9) / 2
        assert metrics["gherkin_coverage_mean"] == 0.825  # (0.85 + 0.8) / 2
        assert metrics["critical_avg"] == 0.5  # (0 + 1) / 2
        assert metrics["major_avg"] == 0.5  # (1 + 0) / 2
        assert metrics["pass_rate"] == 0.5  # 1 of 2 passed
        
        assert report.successful_validations["gpt-4"] == 2
        assert report.endpoints_passing_threshold["gpt-4"] == 1
        assert report.endpoints_with_critical_issues["gpt-4"] == 1
    
    def test_report_to_dict(self):
        """Test converting report to dictionary."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        report = ConsistencyExperimentReport(
            experiment_id="rq2_test",
            config=config,
            started_at=datetime.utcnow()
        )
        
        data = report.to_dict()
        
        assert data["experiment_id"] == "rq2_test"
        assert "config" in data
        assert "total_endpoints" in data
        assert "aggregate_metrics" in data
        assert "quality_gates" in data
    
    def test_report_save_to_json(self, tmp_path):
        """Test saving report to JSON file."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1,
            output_dir=tmp_path
        )
        
        report = ConsistencyExperimentReport(
            experiment_id="rq2_test",
            config=config,
            started_at=datetime.utcnow()
        )
        
        output_path = report.save()
        
        assert output_path.exists()
        assert output_path.name == "rq2_report_rq2_test.json"
        
        # Verify JSON content
        with open(output_path) as f:
            data = json.load(f)
            assert data["experiment_id"] == "rq2_test"


class TestRQ2ExperimentRunner:
    """Tests for RQ2ExperimentRunner."""
    
    def test_runner_initialization(self):
        """Test initializing RQ2 experiment runner."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        runner = RQ2ExperimentRunner(config=config)
        
        assert runner.config == config
        assert runner.detector is not None
        assert isinstance(runner.detector, InconsistencyDetector)
        assert runner.report.experiment_id == "rq2_test"
    
    @pytest.mark.asyncio
    async def test_validate_endpoint_consistency(self):
        """Test validating consistency for a single endpoint."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        runner = RQ2ExperimentRunner(config=config)
        
        endpoint = create_sample_endpoint()
        oracle = create_sample_oracle(endpoint.id)
        test = create_sample_generated_test(endpoint.id)
        
        result = await runner._validate_endpoint_consistency(
            endpoint=endpoint,
            oracle=oracle,
            test=test
        )
        
        assert result is not None
        assert result.endpoint_id == endpoint.id
        assert result.endpoint_name == endpoint.name
        assert result.inconsistency_report is not None
        assert result.coherence_score >= 0.0
        assert result.coherence_score <= 1.0
    
    @pytest.mark.asyncio
    async def test_run_experiment_empty_data(self):
        """Test running experiment with empty data."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=0
        )
        
        runner = RQ2ExperimentRunner(config=config)
        
        report = await runner.run_experiment(
            endpoints=[],
            oracles={},
            generated_tests={}
        )
        
        assert report.total_endpoints == 0
        assert len(report.endpoint_results) == 0
    
    def test_get_summary(self):
        """Test getting experiment summary."""
        config = ConsistencyExperimentConfig(
            experiment_id="rq2_test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        runner = RQ2ExperimentRunner(config=config)
        
        summary = runner.get_summary()
        
        assert "status" in summary
        assert summary["status"] == "No results available"


class TestBatchConsistencyConfig:
    """Tests for BatchConsistencyConfig."""
    
    def test_batch_config_creation(self):
        """Test creating batch consistency configuration."""
        config = BatchConsistencyConfig(
            experiment_name="batch_test",
            description="Batch test",
            llm_models=["gpt-4", "claude-3-opus"],
            test_suites=["suite1", "suite2"],
            num_replications=3
        )
        
        assert config.experiment_name == "batch_test"
        assert len(config.llm_models) == 2
        assert len(config.test_suites) == 2
        assert config.num_replications == 3


class TestInconsistencyPattern:
    """Tests for InconsistencyPattern dataclass."""
    
    def test_pattern_creation(self):
        """Test creating inconsistency pattern."""
        pattern = InconsistencyPattern(
            pattern_type="missing_status_code_validation",
            category="status_code",
            severity=InconsistencySeverity.CRITICAL,
            occurrence_count=10,
            affected_endpoints=["endpoint1", "endpoint2"],
            affected_models=["gpt-4"],
            occurrence_rate=0.5,
            recommendation="Add status code validation"
        )
        
        assert pattern.pattern_type == "missing_status_code_validation"
        assert pattern.severity == InconsistencySeverity.CRITICAL
        assert pattern.occurrence_count == 10
        assert pattern.occurrence_rate == 0.5


class TestConsistencyPatternAnalysis:
    """Tests for ConsistencyPatternAnalysis dataclass."""
    
    def test_pattern_analysis_creation(self):
        """Test creating pattern analysis."""
        analysis = ConsistencyPatternAnalysis(
            total_experiments=5,
            total_endpoints=20
        )
        
        assert analysis.total_experiments == 5
        assert analysis.total_endpoints == 20
        assert "critical" in analysis.severity_distribution
        assert "missing_validation" in analysis.type_distribution
    
    def test_pattern_analysis_to_dict(self):
        """Test converting pattern analysis to dictionary."""
        analysis = ConsistencyPatternAnalysis(
            total_experiments=5,
            total_endpoints=20
        )
        
        pattern = InconsistencyPattern(
            pattern_type="missing_validation",
            category="status_code",
            severity=InconsistencySeverity.CRITICAL,
            occurrence_count=5,
            affected_endpoints=[],
            affected_models=["gpt-4"],
            occurrence_rate=0.25,
            recommendation="Add validation"
        )
        analysis.common_patterns.append(pattern)
        
        data = analysis.to_dict()
        
        assert data["total_experiments"] == 5
        assert data["total_endpoints"] == 20
        assert len(data["common_patterns"]) == 1
        assert data["common_patterns"][0]["pattern_type"] == "missing_validation"


class TestRQ2ReportGenerator:
    """Tests for RQ2ReportGenerator."""
    
    def test_generator_initialization(self, tmp_path):
        """Test initializing report generator."""
        generator = RQ2ReportGenerator(output_dir=tmp_path)
        
        assert generator.output_dir == tmp_path
        assert generator.output_dir.exists()
    
    def test_create_latex_table(self, tmp_path):
        """Test creating LaTeX table."""
        generator = RQ2ReportGenerator(output_dir=tmp_path)
        
        config = BatchConsistencyConfig(
            experiment_name="test",
            description="Test",
            llm_models=["gpt-4"],
            test_suites=["suite1"],
            output_dir=tmp_path
        )
        
        results = BatchConsistencyResults(
            experiment_name="test",
            config=config,
            reports=[]
        )
        
        latex_path = generator.create_latex_table(results)
        
        assert latex_path.exists()
        assert latex_path.suffix == ".tex"
        
        # Verify LaTeX content
        with open(latex_path) as f:
            content = f.read()
            assert "\\begin{table}" in content
            assert "\\begin{tabular}" in content
            assert "Coherence" in content
    
    def test_export_to_csv(self, tmp_path):
        """Test exporting to CSV."""
        generator = RQ2ReportGenerator(output_dir=tmp_path)
        
        config = BatchConsistencyConfig(
            experiment_name="test",
            description="Test",
            llm_models=["gpt-4"],
            test_suites=["suite1"],
            output_dir=tmp_path
        )
        
        # Create a report with sample data
        exp_config = ConsistencyExperimentConfig(
            experiment_id="test",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        report = ConsistencyExperimentReport(
            experiment_id="test",
            config=exp_config,
            started_at=datetime.utcnow()
        )
        
        # Add a sample endpoint result
        result = EndpointConsistencyResult(
            endpoint_id=uuid4(),
            endpoint_name="Test Endpoint",
            llm_model="gpt-4",
            coherence_score=0.85
        )
        report.endpoint_results.append(result)
        
        results = BatchConsistencyResults(
            experiment_name="test",
            config=config,
            reports=[report]
        )
        
        csv_path = generator.export_to_csv(results)
        
        assert csv_path.exists()
        assert csv_path.suffix == ".csv"
        
        # Verify CSV content
        with open(csv_path) as f:
            content = f.read()
            assert "coherence_score" in content
            assert "java_coverage" in content
            assert "gherkin_coverage" in content
    
    def test_create_markdown_summary(self, tmp_path):
        """Test creating markdown summary."""
        generator = RQ2ReportGenerator(output_dir=tmp_path)
        
        config = BatchConsistencyConfig(
            experiment_name="test",
            description="Test",
            llm_models=["gpt-4"],
            test_suites=["suite1"],
            output_dir=tmp_path
        )
        
        results = BatchConsistencyResults(
            experiment_name="test",
            config=config,
            reports=[]
        )
        
        md_path = generator.create_markdown_summary(results)
        
        assert md_path.exists()
        assert md_path.suffix == ".md"
        
        # Verify markdown content
        with open(md_path) as f:
            content = f.read()
            assert "# RQ2 Consistency Validation Summary" in content
            assert "## Overview" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
