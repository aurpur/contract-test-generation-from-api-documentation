"""
Unit Tests for RQ1 Validation Modules

Tests for:
- rq1_oracle_validation.py (ExperimentRunner)
- ground_truth_manager.py (GroundTruthManager)
- rq1_orchestrator.py (RQ1Orchestrator)
- rq1_reporting.py (RQ1ReportGenerator)
- create_datasets.py (RQ1DatasetCreator)

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

from experiments.rq1_oracle_validation import (
    ExperimentConfig,
    EndpointExperimentResult,
    ExperimentReport,
    RQ1ExperimentRunner,
    create_sample_endpoints,
    create_sample_ground_truths
)
from experiments.ground_truth_manager import GroundTruthManager
from experiments.rq1_orchestrator import (
    BatchExperimentConfig,
    BatchExperimentResults,
    RQ1Orchestrator
)
from experiments.rq1_reporting import RQ1ReportGenerator
from experiments.create_datasets import RQ1DatasetCreator, DatasetMetadata

from src.shared_context.models import EndpointContext
from src.validation.oracle_metrics import GroundTruth


class TestExperimentConfig:
    """Tests for ExperimentConfig dataclass."""
    
    def test_experiment_config_creation(self):
        """Test creating experiment configuration."""
        endpoints = create_sample_endpoints()
        ground_truths = create_sample_ground_truths(endpoints)
        
        config = ExperimentConfig(
            experiment_id="test_exp_001",
            name="test_experiment",
            description="Test experiment description",
            llm_models=["gpt-4", "gpt-3.5-turbo"],
            num_endpoints=len(endpoints),
            output_dir=Path("/tmp/test_output")
        )
        
        assert config.name == "test_experiment"
        assert len(config.llm_models) == 2
        assert config.num_endpoints == 3
    
    def test_experiment_config_default_values(self):
        """Test default values in ExperimentConfig."""
        endpoints = create_sample_endpoints()
        ground_truths = create_sample_ground_truths(endpoints)
        
        config = ExperimentConfig(
            experiment_id="test_exp_002",
            name="test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=10
        )
        
        # Should use defaults
        assert config.include_real_api_calls == False  # default
        assert config.output_dir == Path("experiments/results")


class TestExperimentReport:
    """Tests for ExperimentReport dataclass."""
    
    def test_experiment_report_creation(self):
        """Test creating experiment report."""
        config = ExperimentConfig(
            experiment_id="test_exp",
            name="Test Experiment",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        report = ExperimentReport(
            experiment_id="test_exp",
            config=config,
            started_at=datetime.utcnow(),
            aggregate_metrics={
                "gpt-4": {
                    "precision_mean": 0.95,
                    "recall_mean": 0.90,
                    "f1_mean": 0.925
                }
            }
        )
        
        assert report.experiment_id == "test_exp"
        assert "gpt-4" in report.aggregate_metrics
        assert report.aggregate_metrics["gpt-4"]["precision_mean"] == 0.95
    
    def test_experiment_report_to_json(self):
        """Test converting report to JSON."""
        config = ExperimentConfig(
            experiment_id="test_exp",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        report = ExperimentReport(
            experiment_id="test_exp",
            config=config,
            started_at=datetime.utcnow()
        )
        
        json_data = report.to_dict()
        
        assert json_data["experiment_id"] == "test_exp"
        assert "config" in json_data
        assert "started_at" in json_data
        assert isinstance(json_data["started_at"], str)
    
    def test_experiment_report_save_to_json(self, tmp_path):
        """Test saving report to JSON file."""
        config = ExperimentConfig(
            experiment_id="test_exp",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1,
            output_dir=tmp_path
        )
        
        report = ExperimentReport(
            experiment_id="test_exp",
            config=config,
            started_at=datetime.utcnow()
        )
        
        output_path = report.save()
        
        assert output_path.exists()
        
        # Verify content
        with open(output_path, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data["experiment_id"] == "test_exp"


class TestGroundTruthManager:
    """Tests for GroundTruthManager."""
    
    def test_ground_truth_manager_creation(self, tmp_path):
        """Test creating ground truth manager."""
        manager = GroundTruthManager(storage_dir=tmp_path)
        
        assert manager.storage_dir == tmp_path
        assert len(manager.ground_truths) == 0
    
    def test_add_ground_truth(self, tmp_path):
        """Test adding ground truth."""
        manager = GroundTruthManager(storage_dir=tmp_path)
        
        endpoint_id = uuid4()
        gt = manager.add_ground_truth(
            endpoint_id=endpoint_id,
            status_code=200,
            required_headers={"Content-Type": "application/json"},
            response_schema={"type": "object"},
            business_rules=["Returns 404 if not found"],
            source="manual",
            confidence=1.0,
            annotator="Test User"
        )
        
        assert gt.endpoint_id == endpoint_id
        assert gt.status_code == 200
        assert gt.source == "manual"
        assert len(manager.ground_truths) == 1
    
    def test_import_from_api_response(self, tmp_path):
        """Test importing ground truth from API response."""
        manager = GroundTruthManager(storage_dir=tmp_path)
        
        endpoint_id = uuid4()
        response_data = {
            "status": 200,
            "headers": {
                "Content-Type": "application/json",
                "X-Custom": "value"
            },
            "body": {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com"
            }
        }
        
        gt = manager.import_from_api_response(
            endpoint_id=endpoint_id,
            response_data=response_data,
            annotator="Test User"
        )
        
        assert gt.endpoint_id == endpoint_id
        assert gt.status_code == 200
        assert gt.source == "api_response"
        assert gt.confidence == 0.9
        assert "Content-Type" in gt.required_headers
    
    def test_save_and_load_ground_truths(self, tmp_path):
        """Test saving and loading ground truths."""
        manager = GroundTruthManager(storage_dir=tmp_path)
        
        # Add ground truths
        endpoint_id1 = uuid4()
        endpoint_id2 = uuid4()
        
        manager.add_ground_truth(
            endpoint_id=endpoint_id1,
            status_code=200,
            required_headers={"Content-Type": "application/json"},
            response_schema={"type": "object"},
            confidence=1.0
        )
        
        manager.add_ground_truth(
            endpoint_id=endpoint_id2,
            status_code=201,
            required_headers={"Content-Type": "application/json", "Location": "/users/1"},
            response_schema={"type": "object"},
            confidence=0.95
        )
        
        # Save
        filename = "test_ground_truths.json"
        manager.save_to_file(filename)
        
        # Load in new manager
        manager2 = GroundTruthManager(storage_dir=tmp_path)
        count = manager2.load_from_file(filename)
        
        assert count == 2
        assert len(manager2.ground_truths) == 2
        assert endpoint_id1 in manager2.ground_truths
        assert endpoint_id2 in manager2.ground_truths
    
    def test_validate_ground_truth(self, tmp_path):
        """Test ground truth validation."""
        manager = GroundTruthManager(storage_dir=tmp_path)
        
        # Valid ground truth
        valid_gt = GroundTruth(
            endpoint_id=uuid4(),
            status_code=200,
            required_headers={"Content-Type": "application/json"},
            optional_headers={},
            response_schema={"type": "object"},
            business_rules=[],
            source="manual",
            confidence=1.0
        )
        
        errors = manager.validate_ground_truth(valid_gt)
        assert len(errors) == 0
        
        # Invalid ground truth (bad status code)
        invalid_gt = GroundTruth(
            endpoint_id=uuid4(),
            status_code=999,  # Invalid
            required_headers={},  # Missing Content-Type
            optional_headers={},
            response_schema={},  # Missing type
            business_rules=[],
            source="manual",
            confidence=1.5  # Invalid
        )
        
        errors = manager.validate_ground_truth(invalid_gt)
        assert len(errors) > 0
        assert any("status code" in e.lower() for e in errors)
        assert any("content-type" in e.lower() for e in errors)
        assert any("confidence" in e.lower() for e in errors)
    
    def test_get_statistics(self, tmp_path):
        """Test getting statistics."""
        manager = GroundTruthManager(storage_dir=tmp_path)
        
        # Add ground truths with different sources
        manager.add_ground_truth(
            endpoint_id=uuid4(),
            status_code=200,
            required_headers={"Content-Type": "application/json"},
            response_schema={"type": "object"},
            source="manual",
            confidence=1.0
        )
        
        manager.add_ground_truth(
            endpoint_id=uuid4(),
            status_code=200,
            required_headers={"Content-Type": "application/json"},
            response_schema={"type": "object"},
            source="api_response",
            confidence=0.9
        )
        
        stats = manager.get_statistics()
        
        assert stats["count"] == 2
        assert "manual" in stats["sources"]
        assert "api_response" in stats["sources"]
        assert stats["sources"]["manual"] == 1
        assert stats["sources"]["api_response"] == 1
        assert 0.9 < stats["avg_confidence"] < 1.0


class TestBatchExperimentConfig:
    """Tests for BatchExperimentConfig."""
    
    def test_batch_config_creation(self):
        """Test creating batch experiment config."""
        config = BatchExperimentConfig(
            experiment_name="batch_test",
            description="Test batch experiment",
            llm_models=["gpt-4", "gpt-3.5-turbo"],
            datasets=["dataset1.json", "dataset2.json"],
            completeness_levels=[1.0, 0.75, 0.5],
            num_replications=3
        )
        
        assert config.experiment_name == "batch_test"
        assert len(config.llm_models) == 2
        assert len(config.datasets) == 2
        assert len(config.completeness_levels) == 3
        assert config.num_replications == 3


class TestRQ1ReportGenerator:
    """Tests for RQ1ReportGenerator."""
    
    def test_report_generator_creation(self, tmp_path):
        """Test creating report generator."""
        generator = RQ1ReportGenerator(output_dir=tmp_path)
        
        assert generator.output_dir == tmp_path
        assert tmp_path.exists()
    
    def test_create_latex_table(self, tmp_path):
        """Test creating LaTeX table."""
        generator = RQ1ReportGenerator(output_dir=tmp_path)
        
        # Create mock batch results
        config = BatchExperimentConfig(
            experiment_name="test",
            description="Test",
            llm_models=["gpt-4", "gpt-3.5-turbo"],
            datasets=["test.json"]
        )
        
        results = BatchExperimentResults(
            experiment_name="test",
            config=config,
            reports=[],
            statistical_results={
                "llm_statistics": {
                    "gpt-4": {
                        "precision": {"mean": 0.95, "stdev": 0.02, "min": 0.93, "max": 0.97},
                        "recall": {"mean": 0.90, "stdev": 0.03, "min": 0.87, "max": 0.93},
                        "f1_score": {"mean": 0.925, "stdev": 0.02, "min": 0.91, "max": 0.94}
                    },
                    "gpt-3.5-turbo": {
                        "precision": {"mean": 0.88, "stdev": 0.04, "min": 0.84, "max": 0.92},
                        "recall": {"mean": 0.85, "stdev": 0.03, "min": 0.82, "max": 0.88},
                        "f1_score": {"mean": 0.865, "stdev": 0.03, "min": 0.84, "max": 0.89}
                    }
                },
                "pairwise_comparisons": {},
                "sample_sizes": {}
            }
        )
        
        latex_path = generator.create_latex_table(results, filename="test_table.tex")
        
        assert latex_path.exists()
        
        # Verify content
        with open(latex_path, 'r') as f:
            content = f.read()
        
        assert "\\begin{table}" in content
        assert "\\begin{tabular}" in content
        assert "gpt-4" in content
        assert "gpt-3.5-turbo" in content
    
    def test_export_to_csv(self, tmp_path):
        """Test exporting to CSV."""
        generator = RQ1ReportGenerator(output_dir=tmp_path)
        
        # Create mock report
        config = ExperimentConfig(
            experiment_id="test_exp_c100_r1",
            name="Test",
            description="Test",
            llm_models=["gpt-4"],
            num_endpoints=1
        )
        
        report = ExperimentReport(
            experiment_id="test_exp_c100_r1",
            config=config,
            started_at=datetime.utcnow(),
            aggregate_metrics={
                "gpt-4": {"precision_mean": 0.95, "recall_mean": 0.90, "f1_mean": 0.925}
            },
            llm_rankings={"gpt-4": 1}
        )
        
        config = BatchExperimentConfig(
            experiment_name="test",
            description="Test",
            llm_models=["gpt-4"],
            datasets=["test.json"]
        )
        
        results = BatchExperimentResults(
            experiment_name="test",
            config=config,
            reports=[report],
            statistical_results=None
        )
        
        csv_path = generator.export_to_csv(results, filename="test_results.csv")
        
        assert csv_path.exists()
        
        # Verify content
        with open(csv_path, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) >= 2  # Header + at least one data row
        assert "experiment,llm_model,precision,recall,f1_score" in lines[0]
        assert "gpt-4" in lines[1]


class TestRQ1DatasetCreator:
    """Tests for RQ1DatasetCreator."""
    
    def test_dataset_creator_creation(self, tmp_path):
        """Test creating dataset creator."""
        creator = RQ1DatasetCreator(
            collections_dir=tmp_path / "collections",
            output_dir=tmp_path / "datasets"
        )
        
        assert creator.collections_dir == tmp_path / "collections"
        assert creator.output_dir == tmp_path / "datasets"
    
    def test_infer_status_code(self, tmp_path):
        """Test status code inference."""
        creator = RQ1DatasetCreator(output_dir=tmp_path)
        
        assert creator._infer_status_code("GET") == 200
        assert creator._infer_status_code("POST") == 201
        assert creator._infer_status_code("DELETE") == 204
        assert creator._infer_status_code("PUT") == 200
    
    def test_infer_response_schema(self, tmp_path):
        """Test response schema inference."""
        creator = RQ1DatasetCreator(output_dir=tmp_path)
        
        # List endpoint
        list_endpoint = EndpointContext(
            id=uuid4(),
            name="List Users",
            method="GET",
            url="/users",
            description="Get all users",
            documentation_completeness=1.0
        )
        
        schema = creator._infer_response_schema(list_endpoint)
        assert schema["type"] == "array"
        assert "items" in schema
        
        # Single resource endpoint
        get_endpoint = EndpointContext(
            id=uuid4(),
            name="Get User",
            method="GET",
            url="/users/{id}",
            description="Get user by ID",
            documentation_completeness=1.0
        )
        
        schema = creator._infer_response_schema(get_endpoint)
        assert schema["type"] == "object"
        assert "properties" in schema
    
    def test_reduce_completeness(self, tmp_path):
        """Test reducing endpoint completeness."""
        creator = RQ1DatasetCreator(output_dir=tmp_path)
        
        endpoints = [
            EndpointContext(
                id=uuid4(),
                name="Test Endpoint",
                method="GET",
                url="/test",
                description="This is a long description with multiple sentences. It provides detailed information.",
                documentation_completeness=1.0
            )
        ]
        
        # Reduce to 75%
        modified_75 = creator._reduce_completeness(endpoints, 0.75)
        assert len(modified_75[0].description) > 0
        
        # Reduce to 50%
        modified_50 = creator._reduce_completeness(endpoints, 0.5)
        assert len(modified_50[0].description) < len(endpoints[0].description)
        
        # Reduce to 25%
        modified_25 = creator._reduce_completeness(endpoints, 0.25)
        assert len(modified_25[0].description) < len(modified_50[0].description)
        
        # Reduce to 0%
        modified_0 = creator._reduce_completeness(endpoints, 0.0)
        assert modified_0[0].description == ""
    
    def test_identify_domains(self, tmp_path):
        """Test domain identification."""
        creator = RQ1DatasetCreator(output_dir=tmp_path)
        
        endpoints = [
            EndpointContext(
                id=uuid4(),
                name="Get Users",
                method="GET",
                url="/users",
                description="Get all users",
                documentation_completeness=1.0
            ),
            EndpointContext(
                id=uuid4(),
                name="Login",
                method="POST",
                url="/auth/login",
                description="User login",
                documentation_completeness=1.0
            ),
            EndpointContext(
                id=uuid4(),
                name="List Products",
                method="GET",
                url="/products",
                description="Get all products",
                documentation_completeness=1.0
            )
        ]
        
        domains = creator._identify_domains(endpoints)
        
        assert "user_management" in domains
        assert "authentication" in domains
        assert "product_catalog" in domains
        assert "rest_crud" in domains


@pytest.mark.asyncio
@pytest.mark.skip(reason="RQ1ExperimentRunner requires full agent framework (Phase 5.5 Action 1.1)")
async def test_rq1_experiment_runner_initialization():
    """Test RQ1ExperimentRunner initialization."""
    endpoints = create_sample_endpoints()
    ground_truths = create_sample_ground_truths(endpoints)
    
    config = ExperimentConfig(
        experiment_id="test_exp",
        name="test",
        description="Test experiment",
        llm_models=["gpt-4"],
        num_endpoints=3
    )
    
    # TODO Phase 5.5: Create LightweightOracleRunner for experiments
    # runner = RQ1ExperimentRunner(config)
    
    assert runner.config == config
    assert runner.metrics_calculator is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
