"""
Tests for RQ3, RQ4, RQ5 Experiments

Tests cover:
- RQ3: Quality validation experiments
- RQ4: LLM comparison experiments
- RQ5: Completeness impact experiments
- RQ345: Orchestrator and reporting

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import asyncio
import pytest
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from experiments.rq3_quality_validation import (
    QualityExperimentConfig,
    EndpointQualityResult,
    QualityExperimentReport,
    RQ3ExperimentRunner
)
from experiments.rq4_llm_comparison import (
    LLMComparisonConfig,
    ModelPerformanceResult,
    LLMComparisonExperimentReport,
    RQ4ExperimentRunner
)
from experiments.rq5_completeness_impact import (
    CompletenessExperimentConfig,
    CompletenessLevelResult,
    ModelCompletenessResult,
    CompletenessExperimentReport,
    RQ5ExperimentRunner
)
from experiments.rq345_orchestrator import (
    RQ345BatchConfig,
    RQ345Results,
    CrossRQAnalysis,
    RQ345BatchReport,
    RQ345Orchestrator
)
from experiments.rq345_reporting import (
    ReportConfig,
    RQ345ReportGenerator
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_endpoint_id():
    """Sample endpoint UUID."""
    return uuid4()


@pytest.fixture
def sample_quality_config():
    """Sample quality experiment configuration."""
    return QualityExperimentConfig(
        experiment_id="test_rq3",
        name="Test RQ3 Experiment",
        description="Test code quality assessment",
        llm_models=["gpt-4", "claude-3-sonnet"],
        num_endpoints=5
    )


@pytest.fixture
def sample_comparison_config():
    """Sample LLM comparison configuration."""
    return LLMComparisonConfig(
        experiment_id="test_rq4",
        name="Test RQ4 Experiment",
        description="Test LLM comparison",
        llm_models=["gpt-4", "claude-3-sonnet"]
    )


@pytest.fixture
def sample_completeness_config():
    """Sample completeness impact configuration."""
    return CompletenessExperimentConfig(
        experiment_id="test_rq5",
        name="Test RQ5 Experiment",
        description="Test completeness impact",
        llm_models=["gpt-4", "claude-3-sonnet"]
    )


@pytest.fixture
def sample_batch_config(sample_quality_config, sample_comparison_config, sample_completeness_config):
    """Sample batch configuration."""
    return RQ345BatchConfig(
        experiment_id="test_rq345",
        name="Test RQ345 Batch",
        description="Test unified experiments",
        llm_models=["gpt-4", "claude-3-sonnet"],
        num_endpoints=5,
        rq3_config=sample_quality_config,
        rq4_config=sample_comparison_config,
        rq5_config=sample_completeness_config
    )


@pytest.fixture
def sample_endpoint_quality_result(sample_endpoint_id):
    """Sample endpoint quality result."""
    result = EndpointQualityResult(
        endpoint_id=sample_endpoint_id,
        endpoint_name="POST /api/users",
        llm_model="gpt-4",
        correctness_score=0.85,
        readability_score=0.75,
        maintainability_score=0.70,
        assertion_count=10,
        valid_assertions=9,
        lines_of_code=50,
        cyclomatic_complexity=5.0,
        code_duplication_ratio=0.15,
        code_smells_count=2
    )
    result.calculate_overall_score()
    return result


@pytest.fixture
def sample_model_performance_result():
    """Sample model performance result."""
    result = ModelPerformanceResult(
        llm_model="gpt-4",
        oracle_precision=0.85,
        oracle_recall=0.80,
        oracle_f1=0.82,
        code_correctness=0.85,
        code_readability=0.75,
        code_maintainability=0.70,
        code_overall_quality=0.77,
        coherence_score=0.90,
        java_coverage_ratio=0.95,
        gherkin_coverage_ratio=0.92,
        avg_generation_time_ms=2500.0,
        avg_input_tokens=1500.0,
        avg_output_tokens=800.0,
        total_cost_usd=0.15,
        robustness_score=0.85
    )
    result.calculate_overall_score()
    return result


@pytest.fixture
def sample_completeness_level_result():
    """Sample completeness level result."""
    result = CompletenessLevelResult(
        completeness_level=0.75,
        completeness_category="mostly_complete",
        endpoint_count=5,
        avg_oracle_precision=0.82,
        avg_oracle_recall=0.78,
        avg_oracle_f1=0.80,
        avg_code_correctness=0.81,
        avg_code_readability=0.72,
        avg_code_maintainability=0.68,
        avg_coherence_score=0.87
    )
    result.calculate_overall_quality()
    return result


# ============================================================================
# RQ3 Quality Validation Tests
# ============================================================================

class TestQualityExperimentConfig:
    """Tests for QualityExperimentConfig."""
    
    def test_config_creation(self, sample_quality_config):
        """Test configuration creation."""
        assert sample_quality_config.experiment_id == "test_rq3"
        assert len(sample_quality_config.llm_models) == 2
        assert sample_quality_config.min_correctness_score == 0.8
    
    def test_config_to_dict(self, sample_quality_config):
        """Test configuration serialization."""
        config_dict = sample_quality_config.to_dict()
        assert config_dict["experiment_id"] == "test_rq3"
        assert "llm_models" in config_dict
        assert "thresholds" in config_dict


class TestEndpointQualityResult:
    """Tests for EndpointQualityResult."""
    
    def test_result_creation(self, sample_endpoint_quality_result):
        """Test quality result creation."""
        assert sample_endpoint_quality_result.llm_model == "gpt-4"
        assert sample_endpoint_quality_result.correctness_score == 0.85
    
    def test_overall_score_calculation(self, sample_endpoint_quality_result):
        """Test overall quality score calculation."""
        # Overall = 0.4*correctness + 0.3*readability + 0.3*maintainability
        expected = 0.4 * 0.85 + 0.3 * 0.75 + 0.3 * 0.70
        assert abs(sample_endpoint_quality_result.overall_quality_score - expected) < 0.001
    
    def test_quality_threshold_check(self, sample_endpoint_quality_result):
        """Test quality threshold checking."""
        sample_endpoint_quality_result.check_quality_threshold(
            min_correctness=0.8,
            min_readability=0.7,
            min_maintainability=0.7
        )
        assert sample_endpoint_quality_result.meets_quality_threshold
    
    def test_result_to_dict(self, sample_endpoint_quality_result):
        """Test result serialization."""
        result_dict = sample_endpoint_quality_result.to_dict()
        assert result_dict["llm_model"] == "gpt-4"
        assert "correctness_score" in result_dict
        assert "overall_quality_score" in result_dict


class TestQualityExperimentReport:
    """Tests for QualityExperimentReport."""
    
    def test_report_creation(self, sample_quality_config):
        """Test report creation."""
        report = QualityExperimentReport(
            experiment_id="test_rq3",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        assert report.experiment_id == "test_rq3"
        assert report.endpoint_results == []
    
    def test_aggregate_metrics_calculation(self, sample_quality_config, sample_endpoint_quality_result):
        """Test aggregate metrics calculation."""
        report = QualityExperimentReport(
            experiment_id="test_rq3",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        
        # Add multiple results
        report.endpoint_results.append(sample_endpoint_quality_result)
        result2 = EndpointQualityResult(
            endpoint_id=uuid4(),
            endpoint_name="GET /api/users",
            llm_model="gpt-4",
            correctness_score=0.90,
            readability_score=0.80,
            maintainability_score=0.75,
            overall_quality_score=0.82
        )
        report.endpoint_results.append(result2)
        
        report.calculate_aggregate_metrics()
        
        assert "gpt-4" in report.aggregate_metrics
        metrics = report.aggregate_metrics["gpt-4"]
        assert "mean_correctness_score" in metrics
        assert metrics["mean_correctness_score"] > 0.8
    
    def test_report_to_dict(self, sample_quality_config):
        """Test report serialization."""
        report = QualityExperimentReport(
            experiment_id="test_rq3",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        report_dict = report.to_dict()
        assert report_dict["experiment_id"] == "test_rq3"
        assert "config" in report_dict


# ============================================================================
# RQ4 LLM Comparison Tests
# ============================================================================

class TestLLMComparisonConfig:
    """Tests for LLMComparisonConfig."""
    
    def test_config_creation(self, sample_comparison_config):
        """Test configuration creation."""
        assert sample_comparison_config.experiment_id == "test_rq4"
        assert sample_comparison_config.compare_oracle_quality
        assert sample_comparison_config.compare_code_quality
    
    def test_token_costs(self, sample_comparison_config):
        """Test token cost configuration."""
        assert "gpt-4" in sample_comparison_config.token_costs
        assert len(sample_comparison_config.token_costs["gpt-4"]) == 2  # input, output
    
    def test_config_to_dict(self, sample_comparison_config):
        """Test configuration serialization."""
        config_dict = sample_comparison_config.to_dict()
        assert "comparison_dimensions" in config_dict
        assert "token_costs" in config_dict


class TestModelPerformanceResult:
    """Tests for ModelPerformanceResult."""
    
    def test_result_creation(self, sample_model_performance_result):
        """Test performance result creation."""
        assert sample_model_performance_result.llm_model == "gpt-4"
        assert sample_model_performance_result.oracle_f1 == 0.82
    
    def test_overall_score_calculation(self, sample_model_performance_result):
        """Test overall score calculation."""
        # Should be weighted average
        assert sample_model_performance_result.overall_score > 0.0
        assert sample_model_performance_result.overall_score <= 1.0
    
    def test_normalized_metrics(self, sample_model_performance_result):
        """Test normalized metric calculations."""
        perf_score = sample_model_performance_result.calculate_normalized_performance()
        cost_score = sample_model_performance_result.calculate_normalized_cost()
        
        assert 0.0 <= perf_score <= 1.0
        assert 0.0 <= cost_score <= 1.0
    
    def test_result_to_dict(self, sample_model_performance_result):
        """Test result serialization."""
        result_dict = sample_model_performance_result.to_dict()
        assert result_dict["llm_model"] == "gpt-4"
        assert "oracle_metrics" in result_dict
        assert "overall_score" in result_dict


class TestLLMComparisonReport:
    """Tests for LLMComparisonExperimentReport."""
    
    def test_report_creation(self, sample_comparison_config):
        """Test report creation."""
        report = LLMComparisonExperimentReport(
            experiment_id="test_rq4",
            config=sample_comparison_config,
            started_at=datetime.utcnow()
        )
        assert report.experiment_id == "test_rq4"
    
    def test_rankings_calculation(self, sample_comparison_config, sample_model_performance_result):
        """Test ranking calculations."""
        report = LLMComparisonExperimentReport(
            experiment_id="test_rq4",
            config=sample_comparison_config,
            started_at=datetime.utcnow()
        )
        
        report.model_results.append(sample_model_performance_result)
        result2 = ModelPerformanceResult(
            llm_model="claude-3-sonnet",
            oracle_precision=0.80,
            oracle_recall=0.75,
            oracle_f1=0.77,
            code_overall_quality=0.70,
            coherence_score=0.85,
            avg_generation_time_ms=3000.0,
            total_cost_usd=0.10,
            robustness_score=0.80
        )
        result2.calculate_overall_score()
        report.model_results.append(result2)
        
        report.calculate_rankings()
        
        assert len(report.overall_rankings) == 2
        assert report.best_overall != ""


# ============================================================================
# RQ5 Completeness Impact Tests
# ============================================================================

class TestCompletenessExperimentConfig:
    """Tests for CompletenessExperimentConfig."""
    
    def test_config_creation(self, sample_completeness_config):
        """Test configuration creation."""
        assert sample_completeness_config.experiment_id == "test_rq5"
        assert len(sample_completeness_config.completeness_levels) > 0
    
    def test_default_completeness_levels(self, sample_completeness_config):
        """Test default completeness levels."""
        assert 1.0 in sample_completeness_config.completeness_levels
        assert 0.5 in sample_completeness_config.completeness_levels


class TestCompletenessLevelResult:
    """Tests for CompletenessLevelResult."""
    
    def test_result_creation(self, sample_completeness_level_result):
        """Test level result creation."""
        assert sample_completeness_level_result.completeness_level == 0.75
        assert sample_completeness_level_result.completeness_category == "mostly_complete"
    
    def test_overall_quality_calculation(self, sample_completeness_level_result):
        """Test overall quality calculation."""
        # Should be weighted average of oracle, code, consistency
        assert sample_completeness_level_result.avg_overall_quality > 0.0
        assert sample_completeness_level_result.avg_overall_quality <= 1.0


class TestModelCompletenessResult:
    """Tests for ModelCompletenessResult."""
    
    def test_result_creation(self):
        """Test completeness result creation."""
        result = ModelCompletenessResult(llm_model="gpt-4")
        assert result.llm_model == "gpt-4"
        assert result.level_results == []
    
    def test_correlation_calculation(self, sample_completeness_level_result):
        """Test correlation coefficient calculation."""
        result = ModelCompletenessResult(llm_model="gpt-4")
        
        # Add multiple level results
        result.level_results.append(sample_completeness_level_result)
        level2 = CompletenessLevelResult(
            completeness_level=0.5,
            completeness_category="partial",
            avg_overall_quality=0.70
        )
        result.level_results.append(level2)
        
        result.calculate_correlations()
        
        # Correlation should be calculated
        assert result.completeness_quality_correlation != 0.0
    
    def test_degradation_rate_calculation(self, sample_completeness_level_result):
        """Test degradation rate calculation."""
        result = ModelCompletenessResult(llm_model="gpt-4")
        
        result.level_results.append(sample_completeness_level_result)
        level2 = CompletenessLevelResult(
            completeness_level=0.5,
            completeness_category="partial",
            avg_overall_quality=0.70
        )
        result.level_results.append(level2)
        
        result.calculate_degradation_rates()
        
        # Degradation rate should be positive
        assert result.quality_degradation_rate >= 0.0
    
    def test_threshold_identification(self, sample_completeness_level_result):
        """Test threshold identification."""
        result = ModelCompletenessResult(llm_model="gpt-4")
        
        # Add result with quality >= 0.8
        high_quality = CompletenessLevelResult(
            completeness_level=0.8,
            completeness_category="complete",
            avg_overall_quality=0.85
        )
        result.level_results.append(high_quality)
        
        result.identify_thresholds()
        
        # Should identify threshold
        assert result.min_completeness_for_quality_80 > 0.0
    
    def test_robustness_calculation(self, sample_completeness_level_result):
        """Test robustness score calculation."""
        result = ModelCompletenessResult(llm_model="gpt-4")
        
        # Add complete and partial results
        complete = CompletenessLevelResult(
            completeness_level=1.0,
            completeness_category="complete",
            avg_overall_quality=0.85
        )
        partial = CompletenessLevelResult(
            completeness_level=0.5,
            completeness_category="partial",
            avg_overall_quality=0.70
        )
        result.level_results.extend([complete, partial])
        
        result.calculate_robustness()
        
        # Robustness should be quality retention ratio
        assert 0.0 <= result.robustness_score <= 1.0


# ============================================================================
# RQ345 Orchestrator Tests
# ============================================================================

class TestRQ345BatchConfig:
    """Tests for RQ345BatchConfig."""
    
    def test_config_creation(self, sample_batch_config):
        """Test batch configuration creation."""
        assert sample_batch_config.experiment_id == "test_rq345"
        assert sample_batch_config.run_rq3
        assert sample_batch_config.run_rq4
        assert sample_batch_config.run_rq5
    
    def test_config_to_dict(self, sample_batch_config):
        """Test configuration serialization."""
        config_dict = sample_batch_config.to_dict()
        assert "enabled_rqs" in config_dict
        assert config_dict["enabled_rqs"]["rq3_code_quality"]


class TestRQ345Results:
    """Tests for RQ345Results."""
    
    def test_results_creation(self):
        """Test results container creation."""
        results = RQ345Results()
        assert results.rq3_report is None
        assert results.rq4_report is None
        assert results.rq5_report is None
    
    def test_has_results(self, sample_quality_config):
        """Test results availability check."""
        results = RQ345Results()
        assert not results.has_results()
        
        results.rq3_report = QualityExperimentReport(
            experiment_id="test",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        assert results.has_results()
    
    def test_get_llm_models(self, sample_quality_config):
        """Test LLM model extraction."""
        results = RQ345Results()
        results.rq3_report = QualityExperimentReport(
            experiment_id="test",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        results.rq3_report.aggregate_metrics = {
            "gpt-4": {},
            "claude-3-sonnet": {}
        }
        
        models = results.get_llm_models()
        assert len(models) == 2
        assert "gpt-4" in models


class TestCrossRQAnalysis:
    """Tests for CrossRQAnalysis."""
    
    def test_analysis_creation(self):
        """Test cross-RQ analysis creation."""
        analysis = CrossRQAnalysis()
        assert analysis.quality_leaders == []
        assert analysis.cost_effective_models == []
        assert analysis.robust_performers == []
    
    def test_analysis_to_dict(self):
        """Test analysis serialization."""
        analysis = CrossRQAnalysis()
        analysis.quality_leaders = ["gpt-4"]
        analysis.key_findings = ["Test finding"]
        
        analysis_dict = analysis.to_dict()
        assert "patterns" in analysis_dict
        assert "key_findings" in analysis_dict


class TestRQ345BatchReport:
    """Tests for RQ345BatchReport."""
    
    def test_report_creation(self, sample_batch_config):
        """Test batch report creation."""
        report = RQ345BatchReport(
            experiment_id="test_rq345",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        assert report.experiment_id == "test_rq345"
        assert report.total_endpoints_analyzed == 0
    
    def test_overall_rankings_generation(self, sample_batch_config, sample_quality_config):
        """Test overall rankings generation."""
        report = RQ345BatchReport(
            experiment_id="test_rq345",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        
        # Add RQ3 results
        report.results.rq3_report = QualityExperimentReport(
            experiment_id="test",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        report.results.rq3_report.llm_rankings = {
            "gpt-4": 1,
            "claude-3-sonnet": 2
        }
        
        report.generate_overall_rankings()
        
        assert len(report.overall_model_rankings) > 0
    
    def test_recommendations_generation(self, sample_batch_config):
        """Test recommendations generation."""
        report = RQ345BatchReport(
            experiment_id="test_rq345",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        
        report.best_overall_model = "gpt-4"
        report.generate_recommendations()
        
        assert len(report.recommendations) > 0


# ============================================================================
# RQ345 Reporting Tests
# ============================================================================

class TestReportConfig:
    """Tests for ReportConfig."""
    
    def test_config_creation(self):
        """Test report config creation."""
        config = ReportConfig()
        assert config.generate_latex
        assert config.generate_csv
        assert config.generate_markdown
    
    def test_config_to_dict(self):
        """Test config serialization."""
        config = ReportConfig()
        config_dict = config.to_dict()
        assert "output_formats" in config_dict
        assert "chart_config" in config_dict


class TestRQ345ReportGenerator:
    """Tests for RQ345ReportGenerator."""
    
    def test_generator_creation(self, tmp_path):
        """Test report generator creation."""
        config = ReportConfig(output_dir=tmp_path / "reports")
        generator = RQ345ReportGenerator(config)
        assert generator.config.output_dir.exists()
    
    def test_latex_report_generation(self, tmp_path, sample_batch_config):
        """Test LaTeX report generation."""
        config = ReportConfig(output_dir=tmp_path / "reports")
        generator = RQ345ReportGenerator(config)
        
        report = RQ345BatchReport(
            experiment_id="test",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        report.completed_at = datetime.utcnow()
        
        latex_path = generator._generate_latex_report(report)
        assert latex_path.exists()
        assert latex_path.suffix == ".tex"
        
        # Check content
        content = latex_path.read_text()
        assert "\\documentclass" in content
        assert "\\begin{document}" in content
    
    def test_csv_report_generation(self, tmp_path, sample_batch_config, sample_quality_config):
        """Test CSV report generation."""
        config = ReportConfig(output_dir=tmp_path / "reports")
        generator = RQ345ReportGenerator(config)
        
        report = RQ345BatchReport(
            experiment_id="test",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        
        # Add RQ3 results
        report.results.rq3_report = QualityExperimentReport(
            experiment_id="test",
            config=sample_quality_config,
            started_at=datetime.utcnow()
        )
        report.results.rq3_report.aggregate_metrics = {
            "gpt-4": {
                "mean_correctness_score": 0.85,
                "mean_readability_score": 0.75,
                "mean_maintainability_score": 0.70,
                "mean_overall_quality": 0.77
            }
        }
        
        csv_files = generator._generate_csv_reports(report)
        assert "rq3_csv" in csv_files
        assert csv_files["rq3_csv"].exists()
    
    def test_markdown_report_generation(self, tmp_path, sample_batch_config):
        """Test Markdown report generation."""
        config = ReportConfig(output_dir=tmp_path / "reports")
        generator = RQ345ReportGenerator(config)
        
        report = RQ345BatchReport(
            experiment_id="test",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        report.completed_at = datetime.utcnow()
        
        md_path = generator._generate_markdown_report(report)
        assert md_path.exists()
        assert md_path.suffix == ".md"
        
        # Check content
        content = md_path.read_text()
        assert "# RQ3/4/5" in content
    
    def test_html_dashboard_generation(self, tmp_path, sample_batch_config):
        """Test HTML dashboard generation."""
        config = ReportConfig(output_dir=tmp_path / "reports")
        generator = RQ345ReportGenerator(config)
        
        report = RQ345BatchReport(
            experiment_id="test",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        report.completed_at = datetime.utcnow()
        
        html_path = generator._generate_html_dashboard(report)
        assert html_path.exists()
        assert html_path.suffix == ".html"
        
        # Check content
        content = html_path.read_text()
        assert "<!DOCTYPE html>" in content
        assert "<html>" in content


# ============================================================================
# Integration Tests
# ============================================================================

class TestRQ345Integration:
    """Integration tests for complete RQ345 workflow."""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, tmp_path, sample_batch_config):
        """Test complete RQ345 workflow."""
        # Setup
        sample_batch_config.output_dir = tmp_path / "results"
        orchestrator = RQ345Orchestrator(sample_batch_config)
        
        # Mock data
        endpoints = []
        oracles = {}
        generated_tests = {}
        
        # Note: This is a minimal test - full integration would require real data
        assert orchestrator.config.experiment_id == "test_rq345"
    
    def test_report_generation_workflow(self, tmp_path, sample_batch_config):
        """Test report generation workflow."""
        # Create report
        report = RQ345BatchReport(
            experiment_id="test",
            config=sample_batch_config,
            started_at=datetime.utcnow()
        )
        report.completed_at = datetime.utcnow()
        report.best_overall_model = "gpt-4"
        report.total_endpoints_analyzed = 10
        report.total_tests_generated = 50
        
        # Generate reports
        config = ReportConfig(
            output_dir=tmp_path / "reports",
            generate_charts=False  # Skip charts for faster testing
        )
        generator = RQ345ReportGenerator(config)
        
        output_files = generator.generate_full_report(report)
        
        # Verify outputs
        assert "latex" in output_files
        assert "markdown" in output_files
        assert output_files["latex"].exists()
        assert output_files["markdown"].exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
