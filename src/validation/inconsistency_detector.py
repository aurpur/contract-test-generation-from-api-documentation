"""
Inconsistency Detector Module (RQ2 - Cohérence Oracles/Code)

This module detects inconsistencies between oracles and generated test code
to ensure that all oracle validations are properly implemented in tests.

Research Question 2: Le code généré est-il cohérent avec les oracles dérivés?

Detects:
- Missing validations (oracle present, not in code)
- Extra validations (in code, not in oracle)
- Incorrect implementations (wrong assertion type/value)
- Incomplete implementations (partial validation)

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID
import re

from ..shared_context.models import Oracle, GeneratedTest


class InconsistencyType(str, Enum):
    """Types of inconsistencies between oracle and code."""
    MISSING_VALIDATION = "missing_validation"  # Oracle has it, code doesn't
    EXTRA_VALIDATION = "extra_validation"  # Code has it, oracle doesn't
    INCORRECT_VALUE = "incorrect_value"  # Wrong expected value
    INCORRECT_TYPE = "incorrect_type"  # Wrong assertion type
    INCOMPLETE_IMPLEMENTATION = "incomplete_implementation"  # Partial validation
    WEAK_ASSERTION = "weak_assertion"  # Too lenient assertion
    MISSING_GHERKIN_STEP = "missing_gherkin_step"  # Oracle validation not in Gherkin


class InconsistencySeverity(str, Enum):
    """Severity levels for inconsistencies."""
    CRITICAL = "critical"  # Core validations missing (status code, required fields)
    MAJOR = "major"  # Important validations missing (headers, schema types)
    MINOR = "minor"  # Optional validations missing (business rules, descriptions)
    INFO = "info"  # Extra validations or improvements


@dataclass
class Inconsistency:
    """A detected inconsistency between oracle and code."""
    type: InconsistencyType
    severity: InconsistencySeverity
    category: str  # "status_code", "header", "schema", "business_rule"
    field_name: str
    
    # Details
    oracle_expectation: Optional[Any] = None
    code_implementation: Optional[Any] = None
    gherkin_implementation: Optional[Any] = None
    
    # Location in code
    code_line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    gherkin_line_number: Optional[int] = None
    
    # Recommendation
    recommendation: str = ""
    suggested_fix: Optional[str] = None


@dataclass
class InconsistencyReport:
    """Report of all inconsistencies for a test."""
    test_id: UUID
    oracle_id: UUID
    
    # Inconsistencies by severity
    critical: List[Inconsistency] = field(default_factory=list)
    major: List[Inconsistency] = field(default_factory=list)
    minor: List[Inconsistency] = field(default_factory=list)
    info: List[Inconsistency] = field(default_factory=list)
    
    # Summary counts
    total_inconsistencies: int = 0
    total_missing_validations: int = 0
    total_extra_validations: int = 0
    total_incorrect_implementations: int = 0
    
    # Coherence score
    coherence_score: float = 0.0  # 0.0 (incoherent) to 1.0 (fully coherent)
    
    # Java code analysis
    java_assertions_found: int = 0
    java_assertions_expected: int = 0
    java_coverage_ratio: float = 0.0
    
    # Gherkin analysis
    gherkin_steps_found: int = 0
    gherkin_steps_expected: int = 0
    gherkin_coverage_ratio: float = 0.0
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_inconsistency(self, inconsistency: Inconsistency) -> None:
        """Add an inconsistency to the appropriate severity list."""
        if inconsistency.severity == InconsistencySeverity.CRITICAL:
            self.critical.append(inconsistency)
        elif inconsistency.severity == InconsistencySeverity.MAJOR:
            self.major.append(inconsistency)
        elif inconsistency.severity == InconsistencySeverity.MINOR:
            self.minor.append(inconsistency)
        else:
            self.info.append(inconsistency)
        
        self.total_inconsistencies += 1
        
        if inconsistency.type == InconsistencyType.MISSING_VALIDATION:
            self.total_missing_validations += 1
        elif inconsistency.type == InconsistencyType.EXTRA_VALIDATION:
            self.total_extra_validations += 1
        elif inconsistency.type in (InconsistencyType.INCORRECT_VALUE, InconsistencyType.INCORRECT_TYPE):
            self.total_incorrect_implementations += 1


class InconsistencyDetector:
    """
    Detects inconsistencies between oracles and generated test code (RQ2).
    
    Analyzes both Java test code and Gherkin scenarios to ensure
    all oracle validations are properly implemented.
    """
    
    def __init__(self):
        # Assertion pattern matchers (Rest-Assured)
        self.status_code_pattern = re.compile(r'\.statusCode\((\d+)\)')
        self.header_pattern = re.compile(r'\.header\(["\']([^"\']+)["\'],\s*([^)]+)\)')
        self.body_pattern = re.compile(r'\.body\(["\']([^"\']+)["\'],\s*([^)]+)\)')
        self.jsonpath_pattern = re.compile(r'assertThat\([^,]+,\s*([^)]+)\)')
        
        # Gherkin step patterns
        self.gherkin_status_pattern = re.compile(r'status code (?:should be|is) (\d+)')
        self.gherkin_header_pattern = re.compile(r'header "([^"]+)" should (?:be|contain) "([^"]+)"')
        self.gherkin_field_pattern = re.compile(r'field "([^"]+)" should (?:be|exist|contain)')
    
    def detect_inconsistencies(
        self,
        oracle: Oracle,
        test: GeneratedTest
    ) -> InconsistencyReport:
        """
        Detect all inconsistencies between oracle and generated test.
        
        Args:
            oracle: The oracle with expected validations
            test: The generated test code
        
        Returns:
            InconsistencyReport with all detected issues
        """
        report = InconsistencyReport(
            test_id=test.id,
            oracle_id=oracle.id
        )
        
        # Parse Java code for assertions
        java_assertions = self._parse_java_assertions(test.test_code)
        
        # Parse Gherkin if available
        gherkin_steps = {}
        if test.feature_content:
            gherkin_steps = self._parse_gherkin_steps(test.feature_content)
        
        # Check status code
        self._check_status_code(oracle, java_assertions, gherkin_steps, report)
        
        # Check headers
        self._check_headers(oracle, java_assertions, gherkin_steps, report)
        
        # Check response schema
        self._check_response_schema(oracle, java_assertions, gherkin_steps, report)
        
        # Check JSONPath assertions
        self._check_jsonpath_assertions(oracle, java_assertions, report)
        
        # Check business rules
        self._check_business_rules(oracle, test.test_code, test.feature_content, report)
        
        # Calculate coherence score
        report.coherence_score = self._calculate_coherence_score(report)
        
        # Calculate coverage ratios
        report.java_assertions_expected = self._count_expected_assertions(oracle)
        report.java_assertions_found = len(java_assertions)
        report.java_coverage_ratio = (
            report.java_assertions_found / report.java_assertions_expected
            if report.java_assertions_expected > 0 else 0.0
        )
        
        if test.feature_content:
            report.gherkin_steps_expected = self._count_expected_gherkin_steps(oracle)
            report.gherkin_steps_found = len(gherkin_steps)
            report.gherkin_coverage_ratio = (
                report.gherkin_steps_found / report.gherkin_steps_expected
                if report.gherkin_steps_expected > 0 else 0.0
            )
        
        return report
    
    def analyze_multiple_tests(
        self,
        oracle_test_pairs: List[Tuple[Oracle, GeneratedTest]]
    ) -> Dict[str, Any]:
        """
        Analyze multiple oracle-test pairs and provide aggregate statistics.
        
        Args:
            oracle_test_pairs: List of (oracle, test) tuples
        
        Returns:
            Dictionary with aggregate statistics
        """
        reports = [self.detect_inconsistencies(oracle, test) for oracle, test in oracle_test_pairs]
        
        if not reports:
            return {}
        
        n = len(reports)
        
        return {
            "total_tests": n,
            "avg_coherence_score": sum(r.coherence_score for r in reports) / n,
            "avg_inconsistencies": sum(r.total_inconsistencies for r in reports) / n,
            
            # By severity
            "total_critical": sum(len(r.critical) for r in reports),
            "total_major": sum(len(r.major) for r in reports),
            "total_minor": sum(len(r.minor) for r in reports),
            "total_info": sum(len(r.info) for r in reports),
            
            # By type
            "total_missing_validations": sum(r.total_missing_validations for r in reports),
            "total_extra_validations": sum(r.total_extra_validations for r in reports),
            "total_incorrect_implementations": sum(r.total_incorrect_implementations for r in reports),
            
            # Coverage
            "avg_java_coverage": sum(r.java_coverage_ratio for r in reports) / n,
            "avg_gherkin_coverage": sum(r.gherkin_coverage_ratio for r in reports if r.gherkin_coverage_ratio > 0) / max(1, sum(1 for r in reports if r.gherkin_coverage_ratio > 0)),
            
            # Quality metrics
            "tests_with_critical_issues": sum(1 for r in reports if r.critical),
            "tests_with_no_issues": sum(1 for r in reports if r.total_inconsistencies == 0),
            "fully_coherent_ratio": sum(1 for r in reports if r.coherence_score >= 0.95) / n,
        }
    
    # Private helper methods
    
    def _parse_java_assertions(self, java_code: str) -> Dict[str, List[Dict[str, Any]]]:
        """Parse all assertions from Java test code."""
        assertions = {
            "status_code": [],
            "headers": [],
            "body": [],
            "jsonpath": []
        }
        
        lines = java_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Status code
            match = self.status_code_pattern.search(line)
            if match:
                assertions["status_code"].append({
                    "value": int(match.group(1)),
                    "line": line_num,
                    "code": line.strip()
                })
            
            # Headers
            match = self.header_pattern.search(line)
            if match:
                assertions["headers"].append({
                    "name": match.group(1),
                    "matcher": match.group(2),
                    "line": line_num,
                    "code": line.strip()
                })
            
            # Body fields
            match = self.body_pattern.search(line)
            if match:
                assertions["body"].append({
                    "path": match.group(1),
                    "matcher": match.group(2),
                    "line": line_num,
                    "code": line.strip()
                })
            
            # JSONPath with assertThat
            match = self.jsonpath_pattern.search(line)
            if match:
                assertions["jsonpath"].append({
                    "matcher": match.group(1),
                    "line": line_num,
                    "code": line.strip()
                })
        
        return assertions
    
    def _parse_gherkin_steps(self, gherkin_content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Parse validation steps from Gherkin feature."""
        steps = {
            "status_code": [],
            "headers": [],
            "fields": []
        }
        
        lines = gherkin_content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Status code
            match = self.gherkin_status_pattern.search(stripped.lower())
            if match:
                steps["status_code"].append({
                    "value": int(match.group(1)),
                    "line": line_num,
                    "text": stripped
                })
            
            # Headers
            match = self.gherkin_header_pattern.search(stripped.lower())
            if match:
                steps["headers"].append({
                    "name": match.group(1),
                    "value": match.group(2),
                    "line": line_num,
                    "text": stripped
                })
            
            # Fields
            match = self.gherkin_field_pattern.search(stripped.lower())
            if match:
                steps["fields"].append({
                    "name": match.group(1),
                    "line": line_num,
                    "text": stripped
                })
        
        return steps
    
    def _check_status_code(
        self,
        oracle: Oracle,
        java_assertions: Dict,
        gherkin_steps: Dict,
        report: InconsistencyReport
    ) -> None:
        """Check status code validation consistency."""
        expected_status = oracle.status_code
        
        # Check Java
        java_status = java_assertions.get("status_code", [])
        if not java_status:
            report.add_inconsistency(Inconsistency(
                type=InconsistencyType.MISSING_VALIDATION,
                severity=InconsistencySeverity.CRITICAL,
                category="status_code",
                field_name="status_code",
                oracle_expectation=expected_status,
                code_implementation=None,
                recommendation=f"Add .statusCode({expected_status}) to the test",
                suggested_fix=f".statusCode({expected_status})"
            ))
        else:
            actual_status = java_status[0]["value"]
            if actual_status != expected_status:
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.INCORRECT_VALUE,
                    severity=InconsistencySeverity.CRITICAL,
                    category="status_code",
                    field_name="status_code",
                    oracle_expectation=expected_status,
                    code_implementation=actual_status,
                    code_line_number=java_status[0]["line"],
                    code_snippet=java_status[0]["code"],
                    recommendation=f"Change status code from {actual_status} to {expected_status}",
                    suggested_fix=f".statusCode({expected_status})"
                ))
        
        # Check Gherkin if available
        if gherkin_steps:
            gherkin_status = gherkin_steps.get("status_code", [])
            if not gherkin_status:
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.MISSING_GHERKIN_STEP,
                    severity=InconsistencySeverity.MAJOR,
                    category="status_code",
                    field_name="status_code",
                    oracle_expectation=expected_status,
                    gherkin_implementation=None,
                    recommendation=f"Add Gherkin step: Then the status code should be {expected_status}",
                    suggested_fix=f"Then the status code should be {expected_status}"
                ))
    
    def _check_headers(
        self,
        oracle: Oracle,
        java_assertions: Dict,
        gherkin_steps: Dict,
        report: InconsistencyReport
    ) -> None:
        """Check header validation consistency."""
        java_headers = {h["name"]: h for h in java_assertions.get("headers", [])}
        gherkin_headers = {h["name"]: h for h in gherkin_steps.get("headers", [])}
        
        for required_header in oracle.required_headers:
            # Check Java
            if required_header not in java_headers:
                severity = InconsistencySeverity.MAJOR if required_header.lower() in ["content-type", "authorization"] else InconsistencySeverity.MINOR
                
                constraint = oracle.header_constraints.get(required_header, {})
                expected_value = constraint.get("value", "any")
                
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.MISSING_VALIDATION,
                    severity=severity,
                    category="header",
                    field_name=required_header,
                    oracle_expectation=constraint,
                    code_implementation=None,
                    recommendation=f"Add header validation for '{required_header}'",
                    suggested_fix=f'.header("{required_header}", equalTo("{expected_value}"))'
                ))
            
            # Check Gherkin
            if gherkin_steps and required_header not in gherkin_headers:
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.MISSING_GHERKIN_STEP,
                    severity=InconsistencySeverity.MINOR,
                    category="header",
                    field_name=required_header,
                    oracle_expectation=required_header,
                    gherkin_implementation=None,
                    recommendation=f"Add Gherkin step for header '{required_header}'",
                    suggested_fix=f'And the header "{required_header}" should be present'
                ))
    
    def _check_response_schema(
        self,
        oracle: Oracle,
        java_assertions: Dict,
        gherkin_steps: Dict,
        report: InconsistencyReport
    ) -> None:
        """Check response schema validation consistency."""
        if not oracle.response_schema:
            return
        
        # Extract expected fields from schema
        expected_fields = self._extract_schema_fields(oracle.response_schema)
        
        # Extract actual validations from code
        java_body = java_assertions.get("body", [])
        java_fields = {b["path"] for b in java_body}
        
        # Check for missing fields
        for field_path in expected_fields:
            if field_path not in java_fields:
                # Determine severity based on field importance
                severity = self._determine_field_severity(field_path, oracle.response_schema)
                
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.MISSING_VALIDATION,
                    severity=severity,
                    category="schema",
                    field_name=field_path,
                    oracle_expectation=self._get_field_type(field_path, oracle.response_schema),
                    code_implementation=None,
                    recommendation=f"Add validation for field '{field_path}'",
                    suggested_fix=f'.body("{field_path}", notNullValue())'
                ))
    
    def _check_jsonpath_assertions(
        self,
        oracle: Oracle,
        java_assertions: Dict,
        report: InconsistencyReport
    ) -> None:
        """Check JSONPath assertion consistency."""
        for json_path, assertion in oracle.json_path_assertions.items():
            # Simple check: look for the path in body assertions
            java_body = java_assertions.get("body", [])
            found = any(b["path"] == json_path for b in java_body)
            
            if not found:
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.MISSING_VALIDATION,
                    severity=InconsistencySeverity.MAJOR,
                    category="jsonpath",
                    field_name=json_path,
                    oracle_expectation=assertion,
                    code_implementation=None,
                    recommendation=f"Add JSONPath validation for '{json_path}'",
                    suggested_fix=f'.body("{json_path}", {self._assertion_to_hamcrest(assertion)})'
                ))
    
    def _check_business_rules(
        self,
        oracle: Oracle,
        java_code: str,
        gherkin_content: Optional[str],
        report: InconsistencyReport
    ) -> None:
        """Check business rule documentation."""
        for i, rule in enumerate(oracle.business_rules):
            # Check if rule is mentioned in comments
            if rule.lower() not in java_code.lower():
                report.add_inconsistency(Inconsistency(
                    type=InconsistencyType.MISSING_VALIDATION,
                    severity=InconsistencySeverity.MINOR,
                    category="business_rule",
                    field_name=f"rule_{i}",
                    oracle_expectation=rule,
                    code_implementation=None,
                    recommendation=f"Document or implement business rule: '{rule}'",
                    suggested_fix=f"// Business rule: {rule}"
                ))
    
    def _calculate_coherence_score(self, report: InconsistencyReport) -> float:
        """
        Calculate overall coherence score (0.0 to 1.0).
        
        Penalizes based on severity:
        - Critical: -0.2 per issue
        - Major: -0.1 per issue
        - Minor: -0.05 per issue
        - Info: -0.01 per issue
        """
        score = 1.0
        
        score -= len(report.critical) * 0.2
        score -= len(report.major) * 0.1
        score -= len(report.minor) * 0.05
        score -= len(report.info) * 0.01
        
        return max(0.0, score)
    
    def _count_expected_assertions(self, oracle: Oracle) -> int:
        """Count total expected assertions from oracle."""
        count = 1  # Status code
        count += len(oracle.required_headers)
        count += len(self._extract_schema_fields(oracle.response_schema or {}))
        count += len(oracle.json_path_assertions)
        return count
    
    def _count_expected_gherkin_steps(self, oracle: Oracle) -> int:
        """Count expected Gherkin validation steps."""
        count = 1  # Status code
        count += len(oracle.required_headers)
        count += len(self._extract_schema_fields(oracle.response_schema or {}))
        return count
    
    def _extract_schema_fields(self, schema: Dict[str, Any], prefix: str = "") -> Set[str]:
        """Extract all field paths from schema."""
        fields = set()
        
        if "properties" in schema:
            for key, value in schema["properties"].items():
                field_path = f"{prefix}.{key}" if prefix else key
                fields.add(field_path)
                
                # Recurse for nested objects
                if isinstance(value, dict) and value.get("type") == "object":
                    nested = self._extract_schema_fields(value, field_path)
                    fields.update(nested)
        
        return fields
    
    def _get_field_type(self, field_path: str, schema: Dict[str, Any]) -> Optional[str]:
        """Get the type of a field from schema."""
        parts = field_path.split('.')
        current = schema
        
        for part in parts:
            if "properties" in current and part in current["properties"]:
                current = current["properties"][part]
            else:
                return None
        
        return current.get("type")
    
    def _determine_field_severity(self, field_path: str, schema: Dict[str, Any]) -> InconsistencySeverity:
        """Determine severity based on field importance."""
        # ID fields are critical
        if "id" in field_path.lower():
            return InconsistencySeverity.CRITICAL
        
        # Check if field is required in schema
        parts = field_path.split('.')
        if len(parts) == 1:  # Top-level field
            if "required" in schema and field_path in schema["required"]:
                return InconsistencySeverity.MAJOR
        
        return InconsistencySeverity.MINOR
    
    def _assertion_to_hamcrest(self, assertion: Any) -> str:
        """Convert assertion dict to Hamcrest matcher string."""
        if isinstance(assertion, dict):
            if "equals" in assertion:
                return f'equalTo({assertion["equals"]})'
            if "greaterThan" in assertion:
                return f'greaterThan({assertion["greaterThan"]})'
            if "lessThan" in assertion:
                return f'lessThan({assertion["lessThan"]})'
        
        return "notNullValue()"
