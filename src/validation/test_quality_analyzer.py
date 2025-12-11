"""
Test Quality Analyzer Module (RQ3 - Qualité du Code Généré)

This module analyzes the quality of generated test code across multiple dimensions:
correctness, readability, maintainability, and adherence to best practices.

Research Question 3: Quelle est la qualité du code de test généré?

Metrics:
- Correctness: Valid assertions, proper framework usage
- Readability: Code structure, naming, comments
- Maintainability: Duplication, complexity, modularity
- Best Practices: Rest-Assured patterns, JUnit conventions

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import UUID
import re

from ..shared_context.models import GeneratedTest, Oracle
from ..utils.java_code_analyzer import JavaCodeAnalyzer, JavaCodeSmell


@dataclass
class CorrectnessMetrics:
    """Metrics for test correctness."""
    valid_assertions: int
    invalid_assertions: int
    proper_matchers: int
    improper_matchers: int
    correct_framework_usage: bool
    compilation_errors: int
    runtime_errors: int
    
    correctness_score: float = 0.0  # 0.0 to 1.0
    
    def calculate_score(self) -> float:
        """Calculate overall correctness score."""
        total_assertions = self.valid_assertions + self.invalid_assertions
        if total_assertions == 0:
            return 0.0
        
        assertion_accuracy = self.valid_assertions / total_assertions
        matcher_accuracy = self.proper_matchers / (self.proper_matchers + self.improper_matchers) if (self.proper_matchers + self.improper_matchers) > 0 else 1.0
        
        score = (assertion_accuracy * 0.5 + matcher_accuracy * 0.3)
        
        if self.correct_framework_usage:
            score += 0.1
        
        # Penalize errors
        score -= self.compilation_errors * 0.1
        score -= self.runtime_errors * 0.05
        
        self.correctness_score = max(0.0, min(1.0, score))
        return self.correctness_score


@dataclass
class ReadabilityMetrics:
    """Metrics for code readability."""
    lines_of_code: int
    comment_lines: int
    blank_lines: int
    avg_line_length: float
    max_line_length: int
    
    # Naming quality
    descriptive_names: int
    unclear_names: int
    
    # Structure
    logical_sections: int
    proper_indentation: bool
    consistent_formatting: bool
    
    # Documentation
    has_javadoc: bool
    has_inline_comments: bool
    
    readability_score: float = 0.0  # 0.0 to 1.0
    
    def calculate_score(self) -> float:
        """Calculate overall readability score."""
        score = 0.0
        
        # Comment ratio (10-20% is good)
        total_lines = self.lines_of_code + self.comment_lines + self.blank_lines
        if total_lines > 0:
            comment_ratio = self.comment_lines / total_lines
            if 0.1 <= comment_ratio <= 0.2:
                score += 0.2
            elif comment_ratio > 0:
                score += 0.1
        
        # Line length (< 120 is good)
        if self.max_line_length <= 120:
            score += 0.15
        elif self.max_line_length <= 150:
            score += 0.1
        
        # Naming quality
        total_names = self.descriptive_names + self.unclear_names
        if total_names > 0:
            naming_quality = self.descriptive_names / total_names
            score += naming_quality * 0.2
        
        # Structure
        if self.proper_indentation:
            score += 0.15
        if self.consistent_formatting:
            score += 0.15
        
        # Documentation
        if self.has_javadoc:
            score += 0.1
        if self.has_inline_comments:
            score += 0.05
        
        self.readability_score = min(1.0, score)
        return self.readability_score


@dataclass
class MaintainabilityMetrics:
    """Metrics for code maintainability."""
    cyclomatic_complexity: int
    code_duplication_ratio: float
    number_of_methods: int
    avg_method_length: float
    max_method_length: int
    
    # Modularity
    proper_setup_teardown: bool
    reusable_helpers: int
    hardcoded_values: int
    
    # Smells and anti-patterns (as dicts from JavaCodeAnalyzer)
    code_smells: List[Dict[str, Any]] = field(default_factory=list)
    test_smells: List[Dict[str, Any]] = field(default_factory=list)
    anti_patterns: List[Dict[str, Any]] = field(default_factory=list)
    
    maintainability_score: float = 0.0  # 0.0 to 1.0
    
    def calculate_score(self) -> float:
        """Calculate overall maintainability score."""
        score = 1.0
        
        # Cyclomatic complexity (< 10 is good)
        if self.cyclomatic_complexity <= 10:
            score += 0.2
        elif self.cyclomatic_complexity <= 20:
            score += 0.1
        else:
            score -= 0.1
        
        # Code duplication (< 5% is good)
        if self.code_duplication_ratio < 0.05:
            score += 0.15
        elif self.code_duplication_ratio < 0.1:
            score += 0.1
        else:
            score -= self.code_duplication_ratio * 0.5
        
        # Method length (< 50 lines is good)
        if self.avg_method_length <= 50:
            score += 0.15
        elif self.avg_method_length <= 100:
            score += 0.05
        else:
            score -= 0.1
        
        # Modularity
        if self.proper_setup_teardown:
            score += 0.1
        score += min(0.1, self.reusable_helpers * 0.02)
        score -= self.hardcoded_values * 0.02
        
        # Penalties for smells/anti-patterns
        score -= len([s for s in self.code_smells if s.severity == "critical"]) * 0.1
        score -= len([s for s in self.code_smells if s.severity == "high"]) * 0.05
        score -= len([s for s in self.test_smells if s.severity == "high"]) * 0.05
        score -= len([a for a in self.anti_patterns if a.severity == "critical"]) * 0.15
        
        self.maintainability_score = max(0.0, min(1.0, score))
        return self.maintainability_score


@dataclass
class BestPracticesMetrics:
    """Metrics for adherence to best practices."""
    follows_aaa_pattern: bool  # Arrange-Act-Assert
    proper_test_naming: bool
    single_assertion_principle: bool
    proper_error_handling: bool
    uses_test_data_builders: bool
    
    # Rest-Assured specific
    proper_given_when_then: bool
    correct_matcher_usage: bool
    proper_authentication: bool
    
    # JUnit specific
    proper_annotations: bool
    proper_assertions: bool
    
    best_practices_score: float = 0.0  # 0.0 to 1.0
    
    def calculate_score(self) -> float:
        """Calculate overall best practices score."""
        score = 0.0
        
        if self.follows_aaa_pattern:
            score += 0.15
        if self.proper_test_naming:
            score += 0.1
        if self.single_assertion_principle:
            score += 0.1
        if self.proper_error_handling:
            score += 0.1
        if self.uses_test_data_builders:
            score += 0.05
        
        # Rest-Assured
        if self.proper_given_when_then:
            score += 0.15
        if self.correct_matcher_usage:
            score += 0.15
        if self.proper_authentication:
            score += 0.1
        
        # JUnit
        if self.proper_annotations:
            score += 0.05
        if self.proper_assertions:
            score += 0.05
        
        self.best_practices_score = min(1.0, score)
        return self.best_practices_score


@dataclass
class TestQualityReport:
    """Comprehensive quality report for a test."""
    test_id: UUID
    
    # Dimension scores
    correctness_metrics: CorrectnessMetrics
    readability_metrics: ReadabilityMetrics
    maintainability_metrics: MaintainabilityMetrics
    best_practices_metrics: BestPracticesMetrics
    
    # Overall quality score (weighted average)
    overall_quality_score: float = 0.0
    
    # Alignment with oracle (from CodeQualityAgent)
    oracle_alignment_score: float = 0.0
    oracle_coverage_ratio: float = 0.0
    missing_oracle_validations: List[str] = field(default_factory=list)
    
    # Recommendations
    critical_issues: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    analyzer_version: str = "1.0"
    
    def calculate_overall_score(self) -> float:
        """
        Calculate overall quality score as weighted average.
        
        Weights:
        - Correctness: 40%
        - Readability: 20%
        - Maintainability: 25%
        - Best Practices: 15%
        """
        self.overall_quality_score = (
            self.correctness_metrics.correctness_score * 0.40 +
            self.readability_metrics.readability_score * 0.20 +
            self.maintainability_metrics.maintainability_score * 0.25 +
            self.best_practices_metrics.best_practices_score * 0.15
        )
        return self.overall_quality_score


class CodeQualityAnalyzer:
    """
    Analyzes quality of generated test code (RQ3).
    
    Evaluates correctness, readability, maintainability, and best practices.
    Integrates with JavaCodeAnalyzer for smell detection.
    """
    
    def __init__(self):
        self.java_analyzer = JavaCodeAnalyzer()
        
        # Pattern matchers
        self.assertion_pattern = re.compile(r'assert(?:That|True|False|Equals|NotNull)')
        self.hamcrest_matcher_pattern = re.compile(r'(?:equalTo|notNullValue|hasSize|greaterThan|lessThan|containsString)')
        self.given_when_then_pattern = re.compile(r'(given\(\)|when\(\)|then\(\))')
        self.test_annotation_pattern = re.compile(r'@Test')
    
    def analyze_test_quality(
        self,
        test: GeneratedTest,
        oracle: Optional[Oracle] = None
    ) -> TestQualityReport:
        """
        Perform comprehensive quality analysis on a test.
        
        Args:
            test: The generated test to analyze
            oracle: Optional oracle for alignment checking
        
        Returns:
            TestQualityReport with all quality metrics
        """
        # Analyze with JavaCodeAnalyzer
        java_analysis = self.java_analyzer.analyze(test.test_code)
        
        # Calculate dimension metrics
        correctness = self._analyze_correctness(test, java_analysis)
        readability = self._analyze_readability(test, java_analysis)
        maintainability = self._analyze_maintainability(test, java_analysis)
        best_practices = self._analyze_best_practices(test, java_analysis)
        
        # Create report
        report = TestQualityReport(
            test_id=test.id,
            correctness_metrics=correctness,
            readability_metrics=readability,
            maintainability_metrics=maintainability,
            best_practices_metrics=best_practices
        )
        
        # Calculate scores
        correctness.calculate_score()
        readability.calculate_score()
        maintainability.calculate_score()
        best_practices.calculate_score()
        report.calculate_overall_score()
        
        # Add oracle alignment if available
        if oracle:
            report.oracle_alignment_score = self._calculate_oracle_alignment(test, oracle)
            report.oracle_coverage_ratio = test.assertion_count / self._count_oracle_assertions(oracle) if self._count_oracle_assertions(oracle) > 0 else 0.0
        
        # Generate recommendations
        report.critical_issues = self._identify_critical_issues(report, java_analysis)
        report.improvement_suggestions = self._generate_improvement_suggestions(report, java_analysis)
        
        return report
    
    def analyze_multiple_tests(
        self,
        tests: List[GeneratedTest],
        oracles: Optional[Dict[UUID, Oracle]] = None
    ) -> Dict[str, Any]:
        """
        Analyze multiple tests and provide aggregate statistics.
        
        Args:
            tests: List of tests to analyze
            oracles: Optional dict mapping endpoint_id to oracle
        
        Returns:
            Dictionary with aggregate statistics
        """
        reports = []
        for test in tests:
            oracle = oracles.get(test.endpoint_id) if oracles else None
            report = self.analyze_test_quality(test, oracle)
            reports.append(report)
        
        if not reports:
            return {}
        
        n = len(reports)
        
        return {
            "total_tests": n,
            
            # Overall quality
            "avg_overall_quality": sum(r.overall_quality_score for r in reports) / n,
            "min_quality": min(r.overall_quality_score for r in reports),
            "max_quality": max(r.overall_quality_score for r in reports),
            
            # By dimension
            "avg_correctness": sum(r.correctness_metrics.correctness_score for r in reports) / n,
            "avg_readability": sum(r.readability_metrics.readability_score for r in reports) / n,
            "avg_maintainability": sum(r.maintainability_metrics.maintainability_score for r in reports) / n,
            "avg_best_practices": sum(r.best_practices_metrics.best_practices_score for r in reports) / n,
            
            # Oracle alignment
            "avg_oracle_alignment": sum(r.oracle_alignment_score for r in reports if r.oracle_alignment_score > 0) / max(1, sum(1 for r in reports if r.oracle_alignment_score > 0)),
            "avg_oracle_coverage": sum(r.oracle_coverage_ratio for r in reports if r.oracle_coverage_ratio > 0) / max(1, sum(1 for r in reports if r.oracle_coverage_ratio > 0)),
            
            # Quality categories
            "high_quality_tests": sum(1 for r in reports if r.overall_quality_score >= 0.8),
            "medium_quality_tests": sum(1 for r in reports if 0.5 <= r.overall_quality_score < 0.8),
            "low_quality_tests": sum(1 for r in reports if r.overall_quality_score < 0.5),
            
            # Issues
            "tests_with_critical_issues": sum(1 for r in reports if r.critical_issues),
            "total_critical_issues": sum(len(r.critical_issues) for r in reports),
            "total_improvement_suggestions": sum(len(r.improvement_suggestions) for r in reports),
        }
    
    def compare_llm_quality(
        self,
        tests_by_model: Dict[str, List[GeneratedTest]],
        oracles_by_endpoint: Optional[Dict[UUID, Oracle]] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare test quality across different LLM models.
        
        Args:
            tests_by_model: Dict mapping model name to list of tests
            oracles_by_endpoint: Optional dict of oracles for alignment
        
        Returns:
            Dict with comparison results per model
        """
        results = {}
        
        for model, tests in tests_by_model.items():
            results[model] = self.analyze_multiple_tests(tests, oracles_by_endpoint)
        
        return results
    
    # Private helper methods
    
    def _analyze_correctness(
        self,
        test: GeneratedTest,
        java_analysis: Dict[str, Any]
    ) -> CorrectnessMetrics:
        """Analyze correctness dimension."""
        code = test.test_code
        
        # Count assertions
        assertions = self.assertion_pattern.findall(code)
        valid_assertions = test.assertion_count
        invalid_assertions = max(0, len(assertions) - valid_assertions)
        
        # Check matcher usage
        matchers = self.hamcrest_matcher_pattern.findall(code)
        proper_matchers = len(matchers)
        improper_matchers = max(0, valid_assertions - proper_matchers)
        
        # Check framework usage
        has_given_when_then = bool(self.given_when_then_pattern.search(code))
        
        return CorrectnessMetrics(
            valid_assertions=valid_assertions,
            invalid_assertions=invalid_assertions,
            proper_matchers=proper_matchers,
            improper_matchers=improper_matchers,
            correct_framework_usage=has_given_when_then,
            compilation_errors=0,  # Would need actual compilation
            runtime_errors=0  # Would need actual execution
        )
    
    def _analyze_readability(
        self,
        test: GeneratedTest,
        java_analysis: Dict[str, Any]
    ) -> ReadabilityMetrics:
        """Analyze readability dimension."""
        code = test.test_code
        lines = code.split('\n')
        
        # Line counts
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('//')]
        comment_lines = [l for l in lines if l.strip().startswith('//')]
        blank_lines = [l for l in lines if not l.strip()]
        
        # Line lengths
        line_lengths = [len(l) for l in lines]
        avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
        max_line_length = max(line_lengths) if line_lengths else 0
        
        # Naming quality (simple heuristic from code)
        # Check for single-letter or very short variable names (poor naming)
        single_letter_vars = len(re.findall(r'\b[a-z]\s*=', code))
        method_names = re.findall(r'void\s+(\w+)\s*\(', code)
        descriptive_method_names = sum(1 for name in method_names if len(name) > 4)
        
        descriptive_names = descriptive_method_names
        unclear_names = single_letter_vars
        
        # Structure
        proper_indentation = max_line_length <= 150
        consistent_formatting = True  # Simplified
        
        # Documentation
        has_javadoc = "/**" in code
        has_inline_comments = len(comment_lines) > 0
        
        return ReadabilityMetrics(
            lines_of_code=len(code_lines),
            comment_lines=len(comment_lines),
            blank_lines=len(blank_lines),
            avg_line_length=avg_line_length,
            max_line_length=max_line_length,
            descriptive_names=descriptive_names,
            unclear_names=unclear_names,
            logical_sections=3,  # Setup, Act, Assert
            proper_indentation=proper_indentation,
            consistent_formatting=consistent_formatting,
            has_javadoc=has_javadoc,
            has_inline_comments=has_inline_comments
        )
    
    def _analyze_maintainability(
        self,
        test: GeneratedTest,
        java_analysis: Dict[str, Any]
    ) -> MaintainabilityMetrics:
        """Analyze maintainability dimension."""
        code = test.test_code
        lines = code.split('\n')
        
        # Calculate cyclomatic complexity (simplified: count decision points)
        complexity = 1  # Base complexity
        complexity += code.count('if ')
        complexity += code.count('for ')
        complexity += code.count('while ')
        complexity += code.count('case ')
        complexity += code.count('&&')
        complexity += code.count('||')
        
        # Code duplication (simplified: look for repeated patterns)
        duplication_ratio = 0.0  # Would need more sophisticated analysis
        
        # Method counts
        methods = re.findall(r'(public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)', code)
        number_of_methods = len(methods)
        
        # Method lengths
        method_lengths = []
        for match in re.finditer(r'(public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)\s*\{', code):
            # Simplified: just count lines in methods
            method_lengths.append(len(lines))
        
        avg_method_length = sum(method_lengths) / len(method_lengths) if method_lengths else len(lines)
        max_method_length = max(method_lengths) if method_lengths else len(lines)
        
        # Setup/teardown
        proper_setup_teardown = '@Before' in code or '@BeforeEach' in code or '@After' in code
        
        # Helpers and hardcoded values
        reusable_helpers = len(re.findall(r'private\s+\w+\s+\w+\s*\(', code))
        hardcoded_values = len(re.findall(r'"[^"]{10,}"', code))  # Long string literals
        
        return MaintainabilityMetrics(
            cyclomatic_complexity=complexity,
            code_duplication_ratio=duplication_ratio,
            number_of_methods=number_of_methods,
            avg_method_length=avg_method_length,
            max_method_length=max_method_length,
            proper_setup_teardown=proper_setup_teardown,
            reusable_helpers=reusable_helpers,
            hardcoded_values=hardcoded_values,
            code_smells=java_analysis.get("by_type", {}).get("code_smell", []),
            test_smells=java_analysis.get("by_type", {}).get("test_smell", []),
            anti_patterns=java_analysis.get("by_type", {}).get("antipattern", [])
        )
    
    def _analyze_best_practices(
        self,
        test: GeneratedTest,
        java_analysis: Dict[str, Any]
    ) -> BestPracticesMetrics:
        """Analyze best practices adherence."""
        code = test.test_code
        
        # AAA pattern (Arrange-Act-Assert)
        follows_aaa = bool(re.search(r'//.*Arrange|//.*Act|//.*Assert', code, re.IGNORECASE))
        
        # Test naming
        proper_naming = test.test_method_name.startswith("test") or "should" in test.test_method_name.lower()
        
        # Single assertion (relaxed for integration tests)
        single_assertion = test.assertion_count <= 5
        
        # Rest-Assured patterns
        has_given_when_then = bool(self.given_when_then_pattern.search(code))
        has_matchers = bool(self.hamcrest_matcher_pattern.search(code))
        has_auth = "header(" in code and ("Authorization" in code or "auth()" in code)
        
        # JUnit annotations
        has_test_annotation = bool(self.test_annotation_pattern.search(code))
        has_assertions = test.assertion_count > 0
        
        return BestPracticesMetrics(
            follows_aaa_pattern=follows_aaa,
            proper_test_naming=proper_naming,
            single_assertion_principle=single_assertion,
            proper_error_handling=True,  # Simplified
            uses_test_data_builders=False,  # Not implemented yet
            proper_given_when_then=has_given_when_then,
            correct_matcher_usage=has_matchers,
            proper_authentication=has_auth,
            proper_annotations=has_test_annotation,
            proper_assertions=has_assertions
        )
    
    def _calculate_oracle_alignment(self, test: GeneratedTest, oracle: Oracle) -> float:
        """Calculate alignment score between test and oracle."""
        # Simple heuristic: ratio of assertions to expected validations
        expected_assertions = self._count_oracle_assertions(oracle)
        if expected_assertions == 0:
            return 1.0
        
        return min(1.0, test.assertion_count / expected_assertions)
    
    def _count_oracle_assertions(self, oracle: Oracle) -> int:
        """Count total expected assertions from oracle."""
        count = 1  # Status code
        count += len(oracle.required_headers)
        
        if oracle.response_schema:
            count += self._count_schema_fields(oracle.response_schema)
        
        count += len(oracle.json_path_assertions)
        
        return count
    
    def _count_schema_fields(self, schema: Dict[str, Any]) -> int:
        """Recursively count fields in schema."""
        count = 0
        
        if "properties" in schema:
            count += len(schema["properties"])
            for field_schema in schema["properties"].values():
                if isinstance(field_schema, dict) and field_schema.get("type") == "object":
                    count += self._count_schema_fields(field_schema)
        
        return count
    
    def _identify_critical_issues(
        self,
        report: TestQualityReport,
        java_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify critical issues that must be fixed."""
        issues = []
        
        # Correctness
        if report.correctness_metrics.invalid_assertions > 0:
            issues.append(f"Test has {report.correctness_metrics.invalid_assertions} invalid assertions")
        
        if not report.correctness_metrics.correct_framework_usage:
            issues.append("Test does not use proper Rest-Assured given-when-then pattern")
        
        # Maintainability
        if report.maintainability_metrics.cyclomatic_complexity > 20:
            issues.append(f"Test has high cyclomatic complexity ({report.maintainability_metrics.cyclomatic_complexity})")
        
        # Critical smells/anti-patterns
        for smell in report.maintainability_metrics.code_smells:
            if smell.severity == "critical":
                issues.append(f"Critical code smell: {smell.type}")
        
        for anti_pattern in report.maintainability_metrics.anti_patterns:
            if anti_pattern.severity == "critical":
                issues.append(f"Critical anti-pattern: {anti_pattern.type}")
        
        return issues
    
    def _generate_improvement_suggestions(
        self,
        report: TestQualityReport,
        java_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate suggestions for improving test quality."""
        suggestions = []
        
        # Readability
        if report.readability_metrics.max_line_length > 120:
            suggestions.append("Break long lines (>120 chars) for better readability")
        
        if not report.readability_metrics.has_javadoc:
            suggestions.append("Add JavaDoc comments to describe test purpose")
        
        # Maintainability
        if report.maintainability_metrics.hardcoded_values > 3:
            suggestions.append("Extract hardcoded values into constants or configuration")
        
        if report.maintainability_metrics.code_duplication_ratio > 0.1:
            suggestions.append("Reduce code duplication by extracting common code into helper methods")
        
        # Best Practices
        if not report.best_practices_metrics.follows_aaa_pattern:
            suggestions.append("Structure test using Arrange-Act-Assert pattern")
        
        if not report.best_practices_metrics.proper_test_naming:
            suggestions.append("Use descriptive test method names (e.g., testGetUserReturns200)")
        
        return suggestions
