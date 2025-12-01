"""
Java Code Analyzer - Advanced detection of code smells and antipatterns.

This module provides comprehensive analysis of Java test code to detect:
- Code smells (poor coding practices)
- Antipatterns (common mistakes and bad patterns)
- Test-specific issues (test smells)

Author: Aurel IKAMA HONEY
"""
import re
from typing import Dict, List, Any


class JavaCodeSmell:
    """Represents a detected code smell."""
    
    def __init__(
        self,
        smell_type: str,
        severity: str,
        description: str,
        line_number: int = None,
        suggestion: str = None
    ):
        self.smell_type = smell_type
        self.severity = severity  # low, medium, high, critical
        self.description = description
        self.line_number = line_number
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.smell_type,
            "severity": self.severity,
            "description": self.description,
            "line_number": self.line_number,
            "suggestion": self.suggestion,
        }


class JavaCodeAnalyzer:
    """
    Analyzer for Java test code smells and antipatterns.
    
    Detects various categories of issues:
    - General code smells
    - Test-specific smells
    - Antipatterns
    - Complexity issues
    - Maintainability issues
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.smells: List[JavaCodeSmell] = []
    
    def analyze(self, java_code: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Analyze Java code for smells and antipatterns.
        
        Args:
            java_code: Java source code to analyze
            
        Returns:
            Dictionary with categorized issues
        """
        self.smells = []
        lines = java_code.split('\n')
        
        # Run all detectors
        self._detect_magic_numbers(java_code, lines)
        self._detect_long_methods(java_code, lines)
        self._detect_god_class(java_code, lines)
        self._detect_duplicate_code(java_code, lines)
        self._detect_deep_nesting(java_code, lines)
        self._detect_long_parameter_list(java_code, lines)
        self._detect_dead_code(java_code, lines)
        self._detect_primitive_obsession(java_code, lines)
        self._detect_missing_error_handling(java_code, lines)
        self._detect_poor_naming(java_code, lines)
        
        # Test-specific smells
        self._detect_test_smells(java_code, lines)
        
        # Antipatterns
        self._detect_antipatterns(java_code, lines)
        
        # Categorize results
        return self._categorize_smells()
    
    def _detect_magic_numbers(self, code: str, lines: List[str]) -> None:
        """Detect magic numbers in code."""
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('//') or line.strip().startswith('*'):
                continue
            
            # Find numbers that are not 0, 1, -1 (common acceptable values)
            magic_numbers = re.findall(r'\b(?!0\b|1\b|-1\b)\d{2,}\b', line)
            
            if magic_numbers:
                self.smells.append(JavaCodeSmell(
                    smell_type="magic_numbers",
                    severity="medium",
                    description=f"Magic numbers found: {', '.join(set(magic_numbers))}",
                    line_number=i,
                    suggestion="Replace magic numbers with named constants"
                ))
    
    def _detect_long_methods(self, code: str, lines: List[str]) -> None:
        """Detect long methods."""
        method_pattern = r'(public|private|protected)\s+\w+\s+(\w+)\s*\([^)]*\)\s*\{'
        
        current_method = None
        method_start = 0
        brace_count = 0
        
        for i, line in enumerate(lines, 1):
            # Detect method start
            method_match = re.search(method_pattern, line)
            if method_match:
                current_method = method_match.group(2)
                method_start = i
                brace_count = line.count('{') - line.count('}')
            elif current_method:
                brace_count += line.count('{') - line.count('}')
                
                # Method ends when braces are balanced
                if brace_count == 0:
                    method_length = i - method_start
                    
                    if method_length > 50:
                        self.smells.append(JavaCodeSmell(
                            smell_type="long_method",
                            severity="high",
                            description=f"Method '{current_method}' is too long ({method_length} lines)",
                            line_number=method_start,
                            suggestion="Split into smaller methods (aim for < 30 lines)"
                        ))
                    
                    current_method = None
    
    def _detect_god_class(self, code: str, lines: List[str]) -> None:
        """Detect God Class antipattern."""
        # Count methods and fields
        method_count = len(re.findall(r'(public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)', code))
        field_count = len(re.findall(r'private\s+\w+\s+\w+;', code))
        
        if method_count > 15 or field_count > 10:
            self.smells.append(JavaCodeSmell(
                smell_type="god_class",
                severity="high",
                description=f"Class has too many methods ({method_count}) or fields ({field_count})",
                suggestion="Split class into smaller, focused classes"
            ))
    
    def _detect_duplicate_code(self, code: str, lines: List[str]) -> None:
        """Detect duplicate code."""
        # Simplified: Look for repeated lines
        line_dict = {}
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Ignore short lines, comments, and braces
            if len(stripped) < 20 or stripped.startswith('//') or stripped in ['{', '}', '']:
                continue
            
            if stripped in line_dict:
                line_dict[stripped].append(i)
            else:
                line_dict[stripped] = [i]
        
        # Find lines repeated more than 3 times
        for line_content, occurrences in line_dict.items():
            if len(occurrences) > 3:
                self.smells.append(JavaCodeSmell(
                    smell_type="duplicate_code",
                    severity="medium",
                    description=f"Line appears {len(occurrences)} times: '{line_content[:50]}...'",
                    suggestion="Extract duplicate code into a helper method"
                ))
    
    def _detect_deep_nesting(self, code: str, lines: List[str]) -> None:
        """Detect deep nesting."""
        max_nesting = 0
        max_nesting_line = 0
        
        for i, line in enumerate(lines, 1):
            # Calculate nesting level based on indentation
            indent = len(line) - len(line.lstrip())
            nesting_level = indent // 4  # Assuming 4 spaces per level
            
            if nesting_level > max_nesting:
                max_nesting = nesting_level
                max_nesting_line = i
        
        if max_nesting > 4:
            self.smells.append(JavaCodeSmell(
                smell_type="deep_nesting",
                severity="high",
                description=f"Deep nesting detected ({max_nesting} levels)",
                line_number=max_nesting_line,
                suggestion="Refactor to reduce nesting (use early returns, extract methods)"
            ))
    
    def _detect_long_parameter_list(self, code: str, lines: List[str]) -> None:
        """Detect long parameter lists."""
        method_pattern = r'(public|private|protected)\s+\w+\s+(\w+)\s*\(([^)]*)\)'
        
        for match in re.finditer(method_pattern, code):
            params = match.group(3)
            param_count = len([p.strip() for p in params.split(',') if p.strip()])
            
            if param_count > 5:
                method_name = match.group(2)
                line_num = code[:match.start()].count('\n') + 1
                
                self.smells.append(JavaCodeSmell(
                    smell_type="long_parameter_list",
                    severity="medium",
                    description=f"Method '{method_name}' has too many parameters ({param_count})",
                    line_number=line_num,
                    suggestion="Use parameter object or builder pattern"
                ))
    
    def _detect_dead_code(self, code: str, lines: List[str]) -> None:
        """Detect potentially dead code."""
        # Detect unused private methods (simplified)
        private_methods = re.findall(r'private\s+\w+\s+(\w+)\s*\([^)]*\)', code)
        
        for method in private_methods:
            # Count occurrences (should be at least 2: definition + usage)
            occurrences = len(re.findall(rf'\b{method}\b', code))
            
            if occurrences < 2:
                self.smells.append(JavaCodeSmell(
                    smell_type="dead_code",
                    severity="low",
                    description=f"Potentially unused private method: '{method}'",
                    suggestion="Remove unused code or make method public if needed"
                ))
    
    def _detect_primitive_obsession(self, code: str, lines: List[str]) -> None:
        """Detect primitive obsession."""
        # Count primitive type parameters
        primitive_params = len(re.findall(
            r'\b(int|long|float|double|boolean|String)\s+\w+\s*[,)]',
            code
        ))
        
        total_params = len(re.findall(r'\w+\s+\w+\s*[,)]', code))
        
        if total_params > 10 and primitive_params / total_params > 0.7:
            self.smells.append(JavaCodeSmell(
                smell_type="primitive_obsession",
                severity="medium",
                description=f"Heavy use of primitives ({primitive_params}/{total_params} parameters)",
                suggestion="Consider using value objects instead of primitives"
            ))
    
    def _detect_missing_error_handling(self, code: str, lines: List[str]) -> None:
        """Detect missing error handling."""
        # Empty catch blocks
        empty_catch = re.finditer(r'catch\s*\([^)]+\)\s*\{\s*\}', code)
        for match in empty_catch:
            line_num = code[:match.start()].count('\n') + 1
            self.smells.append(JavaCodeSmell(
                smell_type="empty_catch_block",
                severity="critical",
                description="Empty catch block - silently swallowing exceptions",
                line_number=line_num,
                suggestion="Handle exceptions properly or at least log them"
            ))
        
        # Generic exception catching
        generic_catch = re.finditer(r'catch\s*\(\s*Exception\s+\w+\s*\)', code)
        for match in generic_catch:
            line_num = code[:match.start()].count('\n') + 1
            self.smells.append(JavaCodeSmell(
                smell_type="generic_exception_catch",
                severity="medium",
                description="Catching generic Exception",
                line_number=line_num,
                suggestion="Catch specific exception types"
            ))
    
    def _detect_poor_naming(self, code: str, lines: List[str]) -> None:
        """Detect poor naming conventions."""
        # Single letter variable names (except loop counters i, j, k)
        single_letter_vars = re.findall(r'\b(?!i\b|j\b|k\b)[a-z]\s+[a-z]\b', code)
        if single_letter_vars:
            self.smells.append(JavaCodeSmell(
                smell_type="poor_naming",
                severity="low",
                description=f"Single letter variable names found: {len(single_letter_vars)}",
                suggestion="Use descriptive variable names"
            ))
        
        # Method names not following camelCase
        method_names = re.findall(r'(public|private|protected)\s+\w+\s+(\w+)\s*\(', code)
        for _, name in method_names:
            if '_' in name or not name[0].islower():
                self.smells.append(JavaCodeSmell(
                    smell_type="naming_convention",
                    severity="low",
                    description=f"Method '{name}' doesn't follow camelCase convention",
                    suggestion="Use camelCase for method names"
                ))
    
    def _detect_test_smells(self, code: str, lines: List[str]) -> None:
        """Detect test-specific smells."""
        # Eager Test - multiple concerns tested in one test
        test_methods = re.findall(r'@Test[^}]+}', code, re.DOTALL)
        for test_method in test_methods:
            assertion_count = test_method.count('assert')
            if assertion_count > 10:
                self.smells.append(JavaCodeSmell(
                    smell_type="eager_test",
                    severity="medium",
                    description=f"Test has too many assertions ({assertion_count})",
                    suggestion="Split into multiple focused tests"
                ))
        
        # Mystery Guest - external resources without clear setup
        if re.search(r'new\s+File\(|FileReader|FileInputStream', code):
            self.smells.append(JavaCodeSmell(
                smell_type="mystery_guest",
                severity="medium",
                description="Test relies on external files",
                suggestion="Make test dependencies explicit in setup"
            ))
        
        # Conditional Test Logic - if/switch in tests
        if re.search(r'@Test.*?(if\s*\(|switch\s*\()', code, re.DOTALL):
            self.smells.append(JavaCodeSmell(
                smell_type="conditional_test_logic",
                severity="high",
                description="Test contains conditional logic",
                suggestion="Tests should be deterministic - remove conditionals"
            ))
        
        # Sleepy Test - using Thread.sleep
        if 'Thread.sleep(' in code:
            self.smells.append(JavaCodeSmell(
                smell_type="sleepy_test",
                severity="high",
                description="Test uses Thread.sleep()",
                suggestion="Use proper wait conditions or mocking"
            ))
        
        # For Testers Only - test code accessing production code internals
        if re.search(r'\.setAccessible\(true\)', code):
            self.smells.append(JavaCodeSmell(
                smell_type="for_testers_only",
                severity="medium",
                description="Test accesses private members via reflection",
                suggestion="Test through public interface only"
            ))
    
    def _detect_antipatterns(self, code: str, lines: List[str]) -> None:
        """Detect common antipatterns."""
        # Copy-Paste Programming
        method_bodies = re.findall(r'\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', code)
        if len(method_bodies) > 3:
            similar_count = 0
            for i, body1 in enumerate(method_bodies):
                for body2 in method_bodies[i+1:]:
                    # Simple similarity check
                    if len(body1) > 50 and len(body2) > 50:
                        similarity = len(set(body1.split()) & set(body2.split())) / len(set(body1.split()))
                        if similarity > 0.7:
                            similar_count += 1
            
            if similar_count > 2:
                self.smells.append(JavaCodeSmell(
                    smell_type="copy_paste_programming",
                    severity="high",
                    description=f"Detected {similar_count} similar method bodies",
                    suggestion="Extract common logic into shared methods"
                ))
        
        # Hard Coding
        if re.search(r'password\s*=|apiKey\s*=|secret\s*=', code, re.IGNORECASE):
            self.smells.append(JavaCodeSmell(
                smell_type="hard_coding",
                severity="critical",
                description="Potential hardcoded credentials detected",
                suggestion="Use configuration or environment variables"
            ))
        
        # Shotgun Surgery (many small changes needed in many classes)
        # Detected by high number of imports
        import_count = len(re.findall(r'import\s+[\w.]+;', code))
        if import_count > 20:
            self.smells.append(JavaCodeSmell(
                smell_type="shotgun_surgery",
                severity="medium",
                description=f"High number of imports ({import_count})",
                suggestion="Consider if class has too many dependencies"
            ))
        
        # Improper Exception Handling
        if 'printStackTrace()' in code:
            self.smells.append(JavaCodeSmell(
                smell_type="improper_exception_handling",
                severity="high",
                description="Using printStackTrace() instead of logging",
                suggestion="Use proper logging framework"
            ))
    
    def _categorize_smells(self) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize smells by severity and type."""
        categorized = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "by_type": {}
        }
        
        for smell in self.smells:
            smell_dict = smell.to_dict()
            
            # By severity
            categorized[smell.severity].append(smell_dict)
            
            # By type
            if smell.smell_type not in categorized["by_type"]:
                categorized["by_type"][smell.smell_type] = []
            categorized["by_type"][smell.smell_type].append(smell_dict)
        
        # Add summary
        categorized["summary"] = {
            "total_smells": len(self.smells),
            "critical_count": len(categorized["critical"]),
            "high_count": len(categorized["high"]),
            "medium_count": len(categorized["medium"]),
            "low_count": len(categorized["low"]),
        }
        
        return categorized


def analyze_java_code(java_code: str) -> Dict[str, Any]:
    """
    Convenience function to analyze Java code.
    
    Args:
        java_code: Java source code to analyze
        
    Returns:
        Analysis results with categorized smells and antipatterns
    """
    analyzer = JavaCodeAnalyzer()
    return analyzer.analyze(java_code)
