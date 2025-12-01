"""
Unit tests for ValidationAgent.

Author: Aurel IKAMA HONEY
"""
import pytest
from datetime import datetime
from uuid import uuid4

from agents.validation_agent import ValidationAgent
from agents.base_agent import AgentConfig
from shared_context import Oracle, AgentType


@pytest.fixture
def validation_agent(mock_context_manager, mock_message_router, mock_event_bus, mock_task_queue):
    """Create a ValidationAgent instance for testing."""
    config = AgentConfig(
        agent_id="validation-agent-1",
        agent_type=AgentType.VALIDATOR,
        name="TestValidationAgent",
    )
    
    agent = ValidationAgent(
        config=config,
        context_manager=mock_context_manager,
        message_router=mock_message_router,
        event_bus=mock_event_bus,
        task_queue=mock_task_queue,
        min_quality_score=0.6,
    )
    
    return agent


@pytest.fixture
def valid_oracle():
    """Create a valid oracle for testing."""
    return Oracle(
        name="Test Oracle",
        endpoint_id=uuid4(),
        status_code=200,
        required_headers=["Content-Type", "X-Request-ID"],
        header_constraints={"Content-Type": "application/json"},
        response_schema={
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        },
        json_path_assertions={
            "$.id": {"type": "integer", "minimum": 1}
        },
        business_rules=["ID must be positive", "Name must not be empty"],
        confidence_score=0.85,
        rationale="Test oracle",
        llm_model="test-model",
        generated_at=datetime.utcnow(),
    )


@pytest.fixture
def invalid_oracle():
    """Create an invalid oracle for testing."""
    return Oracle(
        name="Invalid Oracle",
        endpoint_id=uuid4(),
        status_code=999,  # Invalid status code
        required_headers=[],
        header_constraints={},
        response_schema=None,  # Missing schema
        json_path_assertions={},
        business_rules=[],
        confidence_score=0.3,  # Low confidence
        rationale="Test oracle",
        llm_model="test-model",
        generated_at=datetime.utcnow(),
    )


class TestValidationAgent:
    """Test suite for ValidationAgent."""
    
    def test_initialization(self, validation_agent):
        """Test agent initialization."""
        assert validation_agent.config.agent_type == AgentType.VALIDATOR
        assert validation_agent.min_quality_score == 0.6
        assert validation_agent.metrics["oracles_validated"] == 0
    
    def test_validate_status_code_valid(self, validation_agent, valid_oracle):
        """Test status code validation with valid code."""
        score, issues = validation_agent._validate_status_code(valid_oracle)
        
        assert score == 1.0
        assert len(issues) == 0
    
    def test_validate_status_code_invalid(self, validation_agent, invalid_oracle):
        """Test status code validation with invalid code."""
        score, issues = validation_agent._validate_status_code(invalid_oracle)
        
        assert score < 1.0
        assert len(issues) > 0
        assert any("out of valid range" in issue for issue in issues)
    
    def test_validate_headers_with_headers(self, validation_agent, valid_oracle):
        """Test header validation with valid headers."""
        score, issues = validation_agent._validate_headers(valid_oracle)
        
        assert score >= 0.5
        # May have suggestions but no critical issues
    
    def test_validate_headers_without_headers(self, validation_agent, invalid_oracle):
        """Test header validation without headers."""
        score, issues = validation_agent._validate_headers(invalid_oracle)
        
        assert score < 1.0
        assert len(issues) > 0
    
    def test_validate_response_schema_valid(self, validation_agent, valid_oracle):
        """Test response schema validation with valid schema."""
        score, issues = validation_agent._validate_response_schema(valid_oracle)
        
        assert score >= 0.8
    
    def test_validate_response_schema_missing(self, validation_agent, invalid_oracle):
        """Test response schema validation with missing schema."""
        score, issues = validation_agent._validate_response_schema(invalid_oracle)
        
        assert score < 0.5
        assert any("No response schema" in issue for issue in issues)
    
    def test_validate_confidence_valid(self, validation_agent, valid_oracle):
        """Test confidence validation with valid confidence."""
        score, issues = validation_agent._validate_confidence(valid_oracle)
        
        assert score == 1.0
        assert len(issues) == 0
    
    def test_validate_confidence_low(self, validation_agent, invalid_oracle):
        """Test confidence validation with low confidence."""
        score, issues = validation_agent._validate_confidence(invalid_oracle)
        
        assert score < 1.0
        assert any("Low confidence" in issue for issue in issues)
    
    @pytest.mark.asyncio
    async def test_perform_validation_valid_oracle(self, validation_agent, valid_oracle):
        """Test full validation on valid oracle."""
        result = await validation_agent._perform_validation(valid_oracle)
        
        assert "is_valid" in result
        assert "quality_score" in result
        assert "component_scores" in result
        assert "issues" in result
        assert "recommendations" in result
        
        assert result["quality_score"] > 0.7
    
    @pytest.mark.asyncio
    async def test_perform_validation_invalid_oracle(self, validation_agent, invalid_oracle):
        """Test full validation on invalid oracle."""
        result = await validation_agent._perform_validation(invalid_oracle)
        
        assert result["is_valid"] is False
        assert result["quality_score"] < 0.6
        assert len(result["issues"]) > 0
    
    def test_generate_recommendations(self, validation_agent, invalid_oracle):
        """Test recommendation generation."""
        issues = [
            "Missing response schema",
            "Low confidence score",
            "No header validations"
        ]
        scores = {
            "status_code": 0.2,
            "headers": 0.5,
            "response_schema": 0.3,
        }
        
        recommendations = validation_agent._generate_recommendations(
            invalid_oracle, issues, scores
        )
        
        assert len(recommendations) > 0
        assert any("status_code" in rec for rec in recommendations)
    
    def test_analyze_improvement(self, validation_agent):
        """Test improvement analysis."""
        previous = {
            "quality_score": 0.5,
            "issues": ["issue1", "issue2", "issue3"]
        }
        current = {
            "quality_score": 0.8,
            "issues": ["issue1"]
        }
        
        improvement = validation_agent._analyze_improvement(previous, current)
        
        assert improvement["quality_improved"] is True
        assert improvement["quality_score_delta"] == 0.3
        assert improvement["issues_resolved"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
