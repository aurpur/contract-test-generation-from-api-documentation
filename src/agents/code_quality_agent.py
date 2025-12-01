"""
Code Quality Agent - Validates generated test code quality and oracle-code alignment.

This agent analyzes generated Java/Gherkin test code for quality metrics,
code smells, antipatterns, and measures the gap between oracles and generated code.

Author: Aurel IKAMA HONEY
"""
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from agents.base_agent import BaseAgent, AgentConfig
from shared_context import (
    ContextManager,
    Oracle,
    GeneratedTest,
    AgentType,
    ProcessingStatus,
)
from orchestration import Task, MessageBuilder
from utils.logging import logger


class CodeQualityAgent(BaseAgent):
    """
    Code Quality Agent validates generated test code.
    
    Performs comprehensive quality analysis including:
    1. Code quality metrics (LOC, complexity, duplication)
    2. Code smells detection (long methods, magic numbers, etc.)
    3. Antipatterns detection (poor naming, missing assertions, etc.)
    4. Oracle-code alignment (measures gap between oracle and generated code)
    5. Test completeness (all oracle assertions present in code)
    
    Quality dimensions:
    - Correctness: Assertions match oracle expectations
    - Completeness: All oracle validations are tested
    - Maintainability: Code is clean and well-structured
    - Readability: Code is clear and understandable
    - Consistency: Naming and style are consistent
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        message_router,
        event_bus,
        task_queue,
        min_quality_score: float = 0.7,
    ):
        """
        Initialize Code Quality Agent.
        
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
        self.metrics["tests_analyzed"] = 0
        self.metrics["quality_issues_found"] = 0
        self.metrics["smells_detected"] = 0
        self.metrics["antipatterns_detected"] = 0
        self.metrics["oracle_gaps_found"] = 0
    
    def register_handlers(self) -> None:
        """Register message handlers for code quality validation."""
        pass
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process code quality validation tasks.
        
        Args:
            task: Task to process
            
        Returns:
            Task result dictionary
        """
        task_type = task.task_type
        
        if task_type == "analyze_test_quality":
            return await self._analyze_single_test(task)
        elif task_type == "analyze_multiple_tests":
            return await self._analyze_multiple_tests(task)
        elif task_type == "measure_oracle_code_gap":
            return await self._measure_oracle_code_gap(task)
        elif task_type == "detect_smells_antipatterns":
            return await self._detect_smells_and_antipatterns(task)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    async def _analyze_single_test(self, task: Task) -> Dict[str, Any]:
        """
        Analyze quality of a single generated test.
        
        Args:
            task: Task with test_id in payload
            
        Returns:
            Quality analysis results
        """
        test_id = task.payload.get("test_id")
        
        if not test_id:
            return {"status": "error", "error": "No test_id provided"}
        
        # Retrieve test
        session_id = task.session_id
        test = await self._retrieve_test(test_id, session_id)
        
        if not test:
            return {"status": "error", "error": f"Test not found: {test_id}"}
        
        # Retrieve associated oracle
        oracle = await self.context_manager.get_oracle_by_id(
            session_id=session_id,
            oracle_id=test.oracle_id
        )
        
        if not oracle:
            logger.warning(f"Oracle not found for test: {test_id}")
            oracle = None
        
        # Perform quality analysis
        quality_result = await self._perform_quality_analysis(test, oracle)
        
        self.metrics["tests_analyzed"] += 1
        self.metrics["quality_issues_found"] += len(quality_result["issues"])
        self.metrics["smells_detected"] += len(quality_result["code_smells"])
        self.metrics["antipatterns_detected"] += len(quality_result["antipatterns"])
        
        if oracle:
            self.metrics["oracle_gaps_found"] += len(quality_result["oracle_gaps"])
        
        # Publish event
        await self.event_bus.publish(
            event_type="test_quality_analyzed",
            event_data={
                "session_id": str(task.session_id),
                "test_id": str(test.id),
                "quality_score": quality_result["quality_score"],
                "issues_count": len(quality_result["issues"]),
            },
        )
        
        return {
            "status": "success",
            "test_id": str(test.id),
            "quality_result": quality_result,
        }
    
    async def _analyze_multiple_tests(self, task: Task) -> Dict[str, Any]:
        """
        Analyze quality of multiple tests.
        
        Args:
            task: Task with test_ids in payload
            
        Returns:
            Aggregate quality analysis results
        """
        test_ids = task.payload.get("test_ids", [])
        
        if not test_ids:
            return {"status": "error", "error": "No test_ids provided"}
        
        logger.info(f"Analyzing quality of {len(test_ids)} tests")
        
        session_id = task.session_id
        analysis_results = []
        
        for test_id in test_ids:
            try:
                test = await self._retrieve_test(test_id, session_id)
                
                if not test:
                    logger.warning(f"Test not found: {test_id}")
                    continue
                
                oracle = await self.context_manager.get_oracle_by_id(
                    session_id=session_id,
                    oracle_id=test.oracle_id
                )
                
                quality_result = await self._perform_quality_analysis(test, oracle)
                analysis_results.append({
                    "test_id": str(test.id),
                    "test_name": test.test_class_name,
                    **quality_result
                })
                
                self.metrics["tests_analyzed"] += 1
                self.metrics["quality_issues_found"] += len(quality_result["issues"])
                
            except Exception as e:
                logger.error(f"Error analyzing test {test_id}: {e}")
        
        # Calculate aggregate metrics
        if analysis_results:
            avg_quality_score = sum(r["quality_score"] for r in analysis_results) / len(analysis_results)
            total_issues = sum(len(r["issues"]) for r in analysis_results)
            total_smells = sum(len(r["code_smells"]) for r in analysis_results)
            total_antipatterns = sum(len(r["antipatterns"]) for r in analysis_results)
        else:
            avg_quality_score = 0.0
            total_issues = 0
            total_smells = 0
            total_antipatterns = 0
        
        # Publish aggregate event
        await self.event_bus.publish(
            event_type="multiple_tests_analyzed",
            event_data={
                "session_id": str(task.session_id),
                "total_tests": len(analysis_results),
                "avg_quality_score": avg_quality_score,
                "total_issues": total_issues,
            },
        )
        
        return {
            "status": "success",
            "analysis_results": analysis_results,
            "summary": {
                "total_tests": len(analysis_results),
                "avg_quality_score": avg_quality_score,
                "total_issues": total_issues,
                "total_smells": total_smells,
                "total_antipatterns": total_antipatterns,
            }
        }
    
    async def _measure_oracle_code_gap(self, task: Task) -> Dict[str, Any]:
        """
        Measure gap between oracle and generated code.
        
        Args:
            task: Task with test_id and oracle_id in payload
            
        Returns:
            Gap analysis results
        """
        test_id = task.payload.get("test_id")
        oracle_id = task.payload.get("oracle_id")
        session_id = task.session_id
        
        if not test_id or not oracle_id:
            return {"status": "error", "error": "Missing test_id or oracle_id"}
        
        test = await self._retrieve_test(test_id, session_id)
        oracle = await self.context_manager.get_oracle_by_id(
            session_id=session_id,
            oracle_id=UUID(oracle_id) if isinstance(oracle_id, str) else oracle_id
        )
        
        if not test or not oracle:
            return {"status": "error", "error": "Test or oracle not found"}
        
        # Measure gap
        gap_analysis = self._analyze_oracle_code_gap(test, oracle)
        
        return {
            "status": "success",
            "test_id": str(test.id),
            "oracle_id": str(oracle.id),
            "gap_analysis": gap_analysis,
        }
    
    async def _detect_smells_and_antipatterns(self, task: Task) -> Dict[str, Any]:
        """
        Detect code smells and antipatterns in test code.
        
        Args:
            task: Task with test_code in payload
            
        Returns:
            Detected smells and antipatterns
        """
        test_code = task.payload.get("test_code")
        
        if not test_code:
            return {"status": "error", "error": "No test_code provided"}
        
        # Detect smells and antipatterns
        smells = self._detect_code_smells(test_code)
        antipatterns = self._detect_antipatterns(test_code)
        
        return {
            "status": "success",
            "code_smells": smells,
            "antipatterns": antipatterns,
            "total_issues": len(smells) + len(antipatterns),
        }
    
    async def _perform_quality_analysis(
        self, test: GeneratedTest, oracle: Optional[Oracle]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive quality analysis on a test.
        
        Args:
            test: Generated test
            oracle: Associated oracle (optional)
            
        Returns:
            Quality analysis result
        """
        issues = []
        scores = {}
        
        # 1. Code metrics
        metrics_score, metrics_issues = self._analyze_code_metrics(test)
        scores["code_metrics"] = metrics_score
        issues.extend(metrics_issues)
        
        # 2. Code smells
        code_smells = self._detect_code_smells(test.test_code)
        if code_smells:
            scores["code_smells"] = max(0.0, 1.0 - len(code_smells) * 0.1)
            issues.extend([f"Code smell: {smell['type']}" for smell in code_smells])
        else:
            scores["code_smells"] = 1.0
        
        # 3. Antipatterns
        antipatterns = self._detect_antipatterns(test.test_code)
        if antipatterns:
            scores["antipatterns"] = max(0.0, 1.0 - len(antipatterns) * 0.15)
            issues.extend([f"Antipattern: {ap['type']}" for ap in antipatterns])
        else:
            scores["antipatterns"] = 1.0
        
        # 4. Oracle-code alignment (if oracle available)
        oracle_gaps = []
        if oracle:
            alignment_score, oracle_gaps = self._analyze_oracle_code_alignment(test, oracle)
            scores["oracle_alignment"] = alignment_score
            issues.extend([f"Oracle gap: {gap}" for gap in oracle_gaps])
        
        # 5. Test completeness
        completeness_score, completeness_issues = self._analyze_test_completeness(test)
        scores["completeness"] = completeness_score
        issues.extend(completeness_issues)
        
        # Calculate overall quality score
        quality_score = sum(scores.values()) / len(scores) if scores else 0.0
        
        # Generate recommendations
        recommendations = self._generate_quality_recommendations(test, issues, scores)
        
        return {
            "quality_score": quality_score,
            "component_scores": scores,
            "issues": issues,
            "code_smells": code_smells,
            "antipatterns": antipatterns,
            "oracle_gaps": oracle_gaps,
            "recommendations": recommendations,
            "analyzed_at": datetime.utcnow().isoformat(),
        }
    
    def _analyze_code_metrics(self, test: GeneratedTest) -> Tuple[float, List[str]]:
        """Analyze code metrics."""
        issues = []
        score = 1.0
        
        # Lines of code
        loc = len(test.test_code.split('\n'))
        if loc > 200:
            issues.append(f"Test code too long: {loc} lines (recommend < 200)")
            score *= 0.8
        
        # Number of assertions
        assertions_count = test.test_code.count("assertThat(") + test.test_code.count("assertEquals")
        if assertions_count == 0:
            issues.append("No assertions found in test code")
            score *= 0.5
        elif assertions_count > 20:
            issues.append(f"Too many assertions: {assertions_count} (recommend < 20)")
            score *= 0.9
        
        return score, issues
    
    def _detect_code_smells(self, test_code: str) -> List[Dict[str, Any]]:
        """
        Detect code smells in Java test code.
        
        Returns list of detected smells with details.
        """
        smells = []
        
        # 1. Magic numbers
        magic_numbers = re.findall(r'\b\d{3,}\b', test_code)
        if magic_numbers:
            smells.append({
                "type": "magic_numbers",
                "severity": "low",
                "description": f"Found magic numbers: {', '.join(set(magic_numbers))}",
                "suggestion": "Extract magic numbers to named constants"
            })
        
        # 2. Long method names
        method_names = re.findall(r'public void (\w+)\(', test_code)
        for method_name in method_names:
            if len(method_name) > 50:
                smells.append({
                    "type": "long_method_name",
                    "severity": "low",
                    "description": f"Method name too long: {method_name}",
                    "suggestion": "Shorten method name while keeping it descriptive"
                })
        
        # 3. Duplicate code (simplified check)
        lines = test_code.split('\n')
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('//'):
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        duplicates = [line for line, count in line_counts.items() if count > 3]
        if duplicates:
            smells.append({
                "type": "duplicate_code",
                "severity": "medium",
                "description": f"Found {len(duplicates)} duplicate lines",
                "suggestion": "Extract duplicate code to helper methods"
            })
        
        # 4. Missing comments
        comment_lines = sum(1 for line in lines if line.strip().startswith('//'))
        if comment_lines == 0 and len(lines) > 50:
            smells.append({
                "type": "missing_comments",
                "severity": "low",
                "description": "No comments found in long test method",
                "suggestion": "Add comments to explain complex test logic"
            })
        
        # 5. Deep nesting
        max_indent = max((len(line) - len(line.lstrip()) for line in lines if line.strip()), default=0)
        if max_indent > 16:  # More than 4 levels (assuming 4 spaces per level)
            smells.append({
                "type": "deep_nesting",
                "severity": "medium",
                "description": f"Deep nesting detected (max indent: {max_indent})",
                "suggestion": "Refactor to reduce nesting levels"
            })
        
        return smells
    
    def _detect_antipatterns(self, test_code: str) -> List[Dict[str, Any]]:
        """
        Detect antipatterns in test code.
        
        Returns list of detected antipatterns with details.
        """
        antipatterns = []
        
        # 1. Empty catch blocks
        if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', test_code):
            antipatterns.append({
                "type": "empty_catch_block",
                "severity": "high",
                "description": "Empty catch block found",
                "suggestion": "Handle exceptions properly or at least log them"
            })
        
        # 2. Hardcoded URLs/credentials
        if re.search(r'http://|https://|localhost:\d+', test_code):
            antipatterns.append({
                "type": "hardcoded_url",
                "severity": "medium",
                "description": "Hardcoded URL found in test",
                "suggestion": "Extract URLs to configuration or constants"
            })
        
        # 3. Thread.sleep() usage
        if 'Thread.sleep(' in test_code:
            antipatterns.append({
                "type": "thread_sleep",
                "severity": "medium",
                "description": "Thread.sleep() usage detected",
                "suggestion": "Use proper wait conditions instead of sleep"
            })
        
        # 4. System.out.println() usage
        if 'System.out.println(' in test_code:
            antipatterns.append({
                "type": "system_out_print",
                "severity": "low",
                "description": "System.out.println() usage in test",
                "suggestion": "Use proper logging framework instead"
            })
        
        # 5. Missing test name convention
        if not re.search(r'public void test\w+|public void should\w+', test_code):
            antipatterns.append({
                "type": "poor_test_naming",
                "severity": "low",
                "description": "Test method doesn't follow naming convention",
                "suggestion": "Use 'test*' or 'should*' naming convention"
            })
        
        # 6. Assertion without message
        assertions_without_msg = len(re.findall(r'assert\w+\([^,)]+\);', test_code))
        if assertions_without_msg > 0:
            antipatterns.append({
                "type": "assertion_without_message",
                "severity": "low",
                "description": f"{assertions_without_msg} assertions without failure messages",
                "suggestion": "Add descriptive messages to assertions for better debugging"
            })
        
        return antipatterns
    
    def _analyze_oracle_code_alignment(
        self, test: GeneratedTest, oracle: Oracle
    ) -> Tuple[float, List[str]]:
        """
        Analyze alignment between oracle and generated code.
        
        Measures the gap between oracle expectations and code assertions.
        
        Returns:
            (alignment_score, list_of_gaps)
        """
        gaps = []
        score = 1.0
        
        # Check status code assertion
        if oracle.status_code:
            status_assertion = f"statusCode({oracle.status_code})"
            if status_assertion not in test.test_code:
                gaps.append(f"Missing status code assertion: {oracle.status_code}")
                score *= 0.8
        
        # Check required headers
        if oracle.required_headers:
            for header in oracle.required_headers:
                header_check = f'header("{header}"'
                if header_check not in test.test_code:
                    gaps.append(f"Missing header validation: {header}")
                    score *= 0.9
        
        # Check response schema (simplified)
        if oracle.response_schema:
            # Check if schema validation is present
            if "body(" not in test.test_code and "jsonPath(" not in test.test_code:
                gaps.append("Missing response body/schema validation")
                score *= 0.7
        
        # Check JSONPath assertions
        if oracle.json_path_assertions:
            for path in oracle.json_path_assertions.keys():
                path_pattern = path.replace("$.", "")
                if path_pattern not in test.test_code:
                    gaps.append(f"Missing JSONPath assertion: {path}")
                    score *= 0.9
        
        # Check business rules (as comments or assertions)
        if oracle.business_rules:
            missing_rules = 0
            for rule in oracle.business_rules:
                # Check if rule is mentioned in comments or code
                rule_keywords = rule.split()[:3]  # First 3 words
                if not any(keyword.lower() in test.test_code.lower() for keyword in rule_keywords):
                    missing_rules += 1
            
            if missing_rules > 0:
                gaps.append(f"{missing_rules} business rules not reflected in test")
                score *= 0.95
        
        return score, gaps
    
    def _analyze_oracle_code_gap(
        self, test: GeneratedTest, oracle: Oracle
    ) -> Dict[str, Any]:
        """
        Detailed gap analysis between oracle and code.
        
        Returns:
            Detailed gap analysis with metrics
        """
        alignment_score, gaps = self._analyze_oracle_code_alignment(test, oracle)
        
        # Calculate coverage
        total_validations = 0
        implemented_validations = 0
        
        # Status code
        total_validations += 1
        if oracle.status_code and f"statusCode({oracle.status_code})" in test.test_code:
            implemented_validations += 1
        
        # Headers
        if oracle.required_headers:
            total_validations += len(oracle.required_headers)
            for header in oracle.required_headers:
                if f'header("{header}"' in test.test_code:
                    implemented_validations += 1
        
        # JSONPath assertions
        if oracle.json_path_assertions:
            total_validations += len(oracle.json_path_assertions)
            for path in oracle.json_path_assertions.keys():
                if path.replace("$.", "") in test.test_code:
                    implemented_validations += 1
        
        coverage_ratio = implemented_validations / total_validations if total_validations > 0 else 0.0
        
        return {
            "alignment_score": alignment_score,
            "coverage_ratio": coverage_ratio,
            "total_validations": total_validations,
            "implemented_validations": implemented_validations,
            "missing_validations": total_validations - implemented_validations,
            "gaps": gaps,
            "recommendations": [
                f"Implement missing validation: {gap}" for gap in gaps
            ]
        }
    
    def _analyze_test_completeness(self, test: GeneratedTest) -> Tuple[float, List[str]]:
        """Analyze test completeness."""
        issues = []
        score = 1.0
        
        # Check for basic test structure
        if "@Test" not in test.test_code:
            issues.append("Missing @Test annotation")
            score *= 0.7
        
        # Check for setup/teardown
        has_setup = "@Before" in test.test_code or "@BeforeEach" in test.test_code
        has_teardown = "@After" in test.test_code or "@AfterEach" in test.test_code
        
        # Not required, but good practice for complex tests
        if len(test.test_code.split('\n')) > 100 and not (has_setup or has_teardown):
            issues.append("Consider adding setup/teardown methods for complex test")
            score *= 0.95
        
        return score, issues
    
    def _generate_quality_recommendations(
        self, test: GeneratedTest, issues: List[str], scores: Dict[str, float]
    ) -> List[str]:
        """Generate actionable quality recommendations."""
        recommendations = []
        
        # Identify weakest aspect
        if scores:
            min_score_aspect = min(scores, key=scores.get)
            min_score = scores[min_score_aspect]
            
            if min_score < 0.7:
                recommendations.append(
                    f"Priority: Improve '{min_score_aspect}' (score: {min_score:.2f})"
                )
        
        # Specific recommendations
        if any("assertion" in issue.lower() for issue in issues):
            recommendations.append(
                "Add more assertions to validate all expected behaviors"
            )
        
        if any("smell" in issue.lower() or "antipattern" in issue.lower() for issue in issues):
            recommendations.append(
                "Refactor code to eliminate smells and antipatterns"
            )
        
        if any("oracle gap" in issue.lower() for issue in issues):
            recommendations.append(
                "Ensure all oracle validations are implemented in test code"
            )
        
        recommendations.append(
            "Consider peer review to catch additional quality issues"
        )
        
        return recommendations
    
    async def _retrieve_test(self, test_id: Any, session_id: Optional[UUID] = None) -> Optional[GeneratedTest]:
        """
        Retrieve a generated test from context manager.
        
        Args:
            test_id: Test ID (UUID or string)
            session_id: Session ID (required for retrieval)
            
        Returns:
            Generated test or None
        """
        try:
            if not session_id:
                logger.error("Session ID required to retrieve test")
                return None
            
            test = await self.context_manager.get_test_by_id(
                session_id=session_id,
                test_id=UUID(test_id) if isinstance(test_id, str) else test_id
            )
            return test
        except Exception as e:
            logger.error(f"Error retrieving test {test_id}: {e}")
            return None
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"CodeQualityAgent(state={self.state.value}, "
            f"active_tasks={len(self._active_tasks)}, "
            f"min_quality_score={self.min_quality_score})"
        )
