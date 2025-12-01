"""
Validation Agent - Validates generated oracles for quality and correctness.

This agent performs validation on generated oracles to ensure they meet
quality standards and are suitable for test generation.

Author: Aurel IKAMA HONEY
"""
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from agents.base_agent import BaseAgent, AgentConfig
from shared_context import (
    ContextManager,
    Oracle,
    AgentType,
    ProcessingStatus,
)
from orchestration import Task, MessageBuilder
from utils.logging import logger


class ValidationAgent(BaseAgent):
    """
    Validation Agent validates generated oracles.
    
    Performs comprehensive validation including:
    1. Schema validation (correct structure)
    2. Completeness check (all required fields present)
    3. Consistency check (no contradictions)
    4. Quality scoring (overall oracle quality)
    5. Actionable feedback generation
    
    Validation criteria:
    - Status code validity (100-599)
    - Header constraints validity
    - Response schema validity (JSON Schema spec)
    - JSONPath assertions syntax
    - Business rules clarity
    - Confidence score reasonability
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        message_router,
        event_bus,
        task_queue,
        min_quality_score: float = 0.6,
    ):
        """
        Initialize Validation Agent.
        
        Args:
            config: Agent configuration
            context_manager: Shared context manager
            message_router: Message router for inter-agent communication
            event_bus: Event bus for publishing events
            task_queue: Task queue for processing
            min_quality_score: Minimum acceptable quality score
        """
        super().__init__(
            config=config,
            context_manager=context_manager,
            router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        self.min_quality_score = min_quality_score
        
        # Metrics
        self.metrics["oracles_validated"] = 0
        self.metrics["oracles_passed"] = 0
        self.metrics["oracles_failed"] = 0
        self.metrics["validation_issues_found"] = 0
    
    def register_handlers(self) -> None:
        """Register message handlers for validation."""
        pass
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process validation tasks.
        
        Args:
            task: Task to process
            
        Returns:
            Task result dictionary
        """
        task_type = task.task_type
        
        if task_type == "validate_oracle":
            return await self._validate_single_oracle(task)
        elif task_type == "validate_multiple_oracles":
            return await self._validate_multiple_oracles(task)
        elif task_type == "revalidate_after_improvement":
            return await self._revalidate_oracle(task)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    async def _validate_single_oracle(self, task: Task) -> Dict[str, Any]:
        """
        Validate a single oracle.
        
        Args:
            task: Task with oracle_id in payload
            
        Returns:
            Validation results
        """
        oracle_id = task.payload.get("oracle_id")
        
        if not oracle_id:
            return {"status": "error", "error": "No oracle_id provided"}
        
        # Retrieve oracle
        original_oracle = await self.context_manager.get_oracle_by_id(
            session_id=task.session_id,
            oracle_id=UUID(oracle_id) if isinstance(oracle_id, str) else oracle_id
        )
        
        if not original_oracle:
            return {"status": "error", "error": f"Oracle not found: {oracle_id}"}
        
        # Perform validation
        validation_result = await self._perform_validation(original_oracle)
        
        self.metrics["oracles_validated"] += 1
        
        if validation_result["is_valid"]:
            self.metrics["oracles_passed"] += 1
        else:
            self.metrics["oracles_failed"] += 1
            self.metrics["validation_issues_found"] += len(validation_result["issues"])
        
        # Publish event
        await self.event_bus.publish(
            event_type="oracle_validated",
            event_data={
                "session_id": str(task.session_id),
                "oracle_id": str(oracle.id),
                "is_valid": validation_result["is_valid"],
                "quality_score": validation_result["quality_score"],
                "issues_count": len(validation_result["issues"]),
            },
        )
        
        return {
            "status": "success",
            "oracle_id": str(oracle.id),
            "validation_result": validation_result,
        }
    
    async def _validate_multiple_oracles(self, task: Task) -> Dict[str, Any]:
        """
        Validate multiple oracles.
        
        Args:
            task: Task with oracle_ids in payload
            
        Returns:
            Validation results for all oracles
        """
        oracle_ids = task.payload.get("oracle_ids", [])
        
        if not oracle_ids:
            return {"status": "error", "error": "No oracle_ids provided"}
        
        session_id = task.session_id
        logger.info(f"Validating {len(oracle_ids)} oracles")
        
        validation_results = []
        
        for oracle_id in oracle_ids:
            try:
                oracle = await self.context_manager.get_oracle_by_id(
                    session_id=session_id,
                    oracle_id=UUID(oracle_id) if isinstance(oracle_id, str) else oracle_id
                )
                
                if not oracle:
                    logger.warning(f"Oracle not found: {oracle_id}")
                    continue
                
                validation_result = await self._perform_validation(oracle)
                validation_results.append({
                    "oracle_id": str(oracle.id),
                    "oracle_name": oracle.name,
                    **validation_result
                })
                
                self.metrics["oracles_validated"] += 1
                
                if validation_result["is_valid"]:
                    self.metrics["oracles_passed"] += 1
                else:
                    self.metrics["oracles_failed"] += 1
                    self.metrics["validation_issues_found"] += len(validation_result["issues"])
                
            except Exception as e:
                logger.error(f"Error validating oracle {oracle_id}: {e}")
        
        # Publish aggregate event
        passed = sum(1 for r in validation_results if r["is_valid"])
        failed = len(validation_results) - passed
        
        await self.event_bus.publish(
            event_type="multiple_oracles_validated",
            event_data={
                "session_id": str(task.session_id),
                "total_oracles": len(validation_results),
                "passed": passed,
                "failed": failed,
            },
        )
        
        return {
            "status": "success",
            "validation_results": validation_results,
            "summary": {
                "total": len(validation_results),
                "passed": passed,
                "failed": failed,
            }
        }
    
    async def _revalidate_oracle(self, task: Task) -> Dict[str, Any]:
        """
        Revalidate an oracle after improvements.
        
        Args:
            task: Task with oracle_id in payload
            
        Returns:
            Revalidation results with comparison to previous validation
        """
        oracle_id = task.payload.get("oracle_id")
        previous_validation = task.payload.get("previous_validation")
        
        if not oracle_id:
            return {"status": "error", "error": "No oracle_id provided"}
        
        # Retrieve oracle
        oracle = await self.context_manager.get_oracle(
            oracle_id=UUID(oracle_id) if isinstance(oracle_id, str) else oracle_id
        )
        
        if not oracle:
            return {"status": "error", "error": f"Oracle not found: {oracle_id}"}
        
        # Perform revalidation
        validation_result = await self._perform_validation(oracle)
        
        # Compare with previous validation
        improvement_analysis = None
        if previous_validation:
            improvement_analysis = self._analyze_improvement(
                previous_validation, validation_result
            )
        
        return {
            "status": "success",
            "oracle_id": str(oracle.id),
            "validation_result": validation_result,
            "improvement_analysis": improvement_analysis,
        }
    
    async def _perform_validation(self, oracle: Oracle) -> Dict[str, Any]:
        """
        Perform comprehensive validation on an oracle.
        
        Args:
            oracle: Oracle to validate
            
        Returns:
            Validation result with quality score and issues
        """
        issues = []
        scores = {}
        
        # 1. Validate status code
        status_score, status_issues = self._validate_status_code(oracle)
        scores["status_code"] = status_score
        issues.extend(status_issues)
        
        # 2. Validate headers
        headers_score, headers_issues = self._validate_headers(oracle)
        scores["headers"] = headers_score
        issues.extend(headers_issues)
        
        # 3. Validate response schema
        schema_score, schema_issues = self._validate_response_schema(oracle)
        scores["response_schema"] = schema_score
        issues.extend(schema_issues)
        
        # 4. Validate JSONPath assertions
        jsonpath_score, jsonpath_issues = self._validate_jsonpath_assertions(oracle)
        scores["jsonpath_assertions"] = jsonpath_score
        issues.extend(jsonpath_issues)
        
        # 5. Validate business rules
        rules_score, rules_issues = self._validate_business_rules(oracle)
        scores["business_rules"] = rules_score
        issues.extend(rules_issues)
        
        # 6. Check confidence score
        confidence_score, confidence_issues = self._validate_confidence(oracle)
        scores["confidence"] = confidence_score
        issues.extend(confidence_issues)
        
        # Calculate overall quality score
        quality_score = sum(scores.values()) / len(scores)
        
        # Determine if valid
        is_valid = quality_score >= self.min_quality_score and len(issues) == 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(oracle, issues, scores)
        
        return {
            "is_valid": is_valid,
            "quality_score": quality_score,
            "component_scores": scores,
            "issues": issues,
            "recommendations": recommendations,
            "validated_at": datetime.utcnow().isoformat(),
        }
    
    def _validate_status_code(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """Validate status code."""
        issues = []
        
        if not oracle.status_code:
            issues.append("Status code is missing")
            return 0.0, issues
        
        if oracle.status_code < 100 or oracle.status_code > 599:
            issues.append(f"Status code {oracle.status_code} is out of valid range (100-599)")
            return 0.2, issues
        
        # Check if status code is reasonable for the endpoint
        if oracle.status_code >= 500:
            issues.append(f"Status code {oracle.status_code} indicates server error - verify this is expected")
            return 0.7, issues
        
        return 1.0, issues
    
    def _validate_headers(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """Validate header validations."""
        issues = []
        score = 1.0
        
        if not oracle.required_headers and not oracle.header_constraints:
            issues.append("No header validations specified - consider adding common headers like Content-Type")
            score = 0.5
        
        # Check for common required headers
        common_headers = ["Content-Type"]
        if oracle.required_headers:
            missing_common = [h for h in common_headers if h not in oracle.required_headers]
            if missing_common:
                issues.append(f"Consider adding common headers: {', '.join(missing_common)}")
                score *= 0.9
        
        # Validate header constraints format
        if oracle.header_constraints:
            for header, value in oracle.header_constraints.items():
                if not isinstance(value, str):
                    issues.append(f"Header constraint '{header}' has non-string value")
                    score *= 0.8
        
        return score, issues
    
    def _validate_response_schema(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """Validate response schema."""
        issues = []
        score = 1.0
        
        if not oracle.response_schema:
            issues.append("No response schema specified - consider adding schema validation")
            return 0.3, issues
        
        schema = oracle.response_schema
        
        # Check required fields
        if "type" not in schema:
            issues.append("Response schema missing 'type' field")
            score *= 0.7
        
        # Validate object schemas
        if schema.get("type") == "object":
            if "properties" not in schema:
                issues.append("Object schema should define 'properties'")
                score *= 0.8
            
            if "required" in schema and "properties" in schema:
                # Check that required fields exist in properties
                for req_field in schema.get("required", []):
                    if req_field not in schema.get("properties", {}):
                        issues.append(f"Required field '{req_field}' not defined in properties")
                        score *= 0.9
        
        # Validate array schemas
        if schema.get("type") == "array":
            if "items" not in schema:
                issues.append("Array schema should define 'items'")
                score *= 0.8
        
        return score, issues
    
    def _validate_jsonpath_assertions(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """Validate JSONPath assertions."""
        issues = []
        score = 1.0
        
        if not oracle.json_path_assertions:
            # Not required, but recommended
            return 0.8, issues
        
        for path, constraint in oracle.json_path_assertions.items():
            # Validate JSONPath syntax (basic check)
            if not path.startswith("$."):
                issues.append(f"JSONPath '{path}' should start with '$.'")
                score *= 0.9
            
            # Validate constraint structure
            if not isinstance(constraint, dict):
                issues.append(f"JSONPath constraint for '{path}' should be a dictionary")
                score *= 0.8
        
        return score, issues
    
    def _validate_business_rules(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """Validate business rules."""
        issues = []
        score = 1.0
        
        if not oracle.business_rules:
            # Not critical, but useful
            return 0.7, issues
        
        for rule in oracle.business_rules:
            if not rule or len(rule.strip()) < 10:
                issues.append(f"Business rule too short or empty: '{rule}'")
                score *= 0.9
        
        return score, issues
    
    def _validate_confidence(self, oracle: Oracle) -> Tuple[float, List[str]]:
        """Validate confidence score."""
        issues = []
        
        if not oracle.confidence_score:
            issues.append("Confidence score is missing")
            return 0.0, issues
        
        if oracle.confidence_score < 0.0 or oracle.confidence_score > 1.0:
            issues.append(f"Confidence score {oracle.confidence_score} out of range (0.0-1.0)")
            return 0.0, issues
        
        if oracle.confidence_score < 0.5:
            issues.append(f"Low confidence score ({oracle.confidence_score:.2f}) - oracle may be unreliable")
            return 0.5, issues
        
        return 1.0, issues
    
    def _generate_recommendations(
        self, oracle: Oracle, issues: List[str], scores: Dict[str, float]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Identify weakest components
        if scores:
            min_score_component = min(scores, key=scores.get)
            min_score = scores[min_score_component]
            
            if min_score < 0.7:
                recommendations.append(
                    f"Focus on improving '{min_score_component}' validation (current score: {min_score:.2f})"
                )
        
        # Specific recommendations based on issues
        if any("schema" in issue.lower() for issue in issues):
            recommendations.append(
                "Consider using real API responses to infer accurate response schemas"
            )
        
        if any("header" in issue.lower() for issue in issues):
            recommendations.append(
                "Add standard HTTP headers like Content-Type, Cache-Control, Authorization"
            )
        
        if any("confidence" in issue.lower() for issue in issues):
            recommendations.append(
                "Try collecting real API data to improve oracle confidence"
            )
        
        if not oracle.json_path_assertions:
            recommendations.append(
                "Add JSONPath assertions to validate specific response fields"
            )
        
        if not oracle.business_rules:
            recommendations.append(
                "Consider adding business rules to capture domain-specific validations"
            )
        
        return recommendations
    
    def _analyze_improvement(
        self, previous: Dict[str, Any], current: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze improvement between two validations."""
        prev_score = previous.get("quality_score", 0.0)
        curr_score = current.get("quality_score", 0.0)
        
        prev_issues = len(previous.get("issues", []))
        curr_issues = len(current.get("issues", []))
        
        return {
            "quality_score_delta": curr_score - prev_score,
            "quality_improved": curr_score > prev_score,
            "issues_resolved": prev_issues - curr_issues,
            "previous_quality_score": prev_score,
            "current_quality_score": curr_score,
            "previous_issues_count": prev_issues,
            "current_issues_count": curr_issues,
        }
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ValidationAgent(state={self.state.value}, "
            f"active_tasks={len(self._active_tasks)}, "
            f"min_quality_score={self.min_quality_score})"
        )
