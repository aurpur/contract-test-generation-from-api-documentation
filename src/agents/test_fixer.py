"""
Test Fixer Sub-Agent - Automatically fixes errors in generated tests and code.

This sub-agent analyzes test failures and compilation errors in generated code,
then applies LLM-powered corrections to make them work correctly.
It uses an iterative approach with multiple attempts to fix different types of failures.

Updates (2025-12-01):
- Converted to LLM-powered agent for intelligent fixing
- Added support for multiple error categories (assertion, compilation, runtime, timeout)
- Implements iterative fixing: tries multiple strategies per error category
- Uses specialized prompts for each error type
- Tracks detailed metrics per fix category
- Now handles BOTH test code AND generated source code errors

Author: Aurel IKAMA HONEY
"""
import asyncio
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from enum import Enum

from utils.logging import logger
from utils.llm_client import BaseLLMClient


class ErrorCategory(Enum):
    """Categories of errors that can be fixed (tests and generated code)."""
    ASSERTION_MISMATCH = "assertion_mismatch"
    COMPILATION_ERROR = "compilation_error"
    RUNTIME_ERROR = "runtime_error"
    TIMEOUT = "timeout"
    NULL_POINTER = "null_pointer"
    TIMING_DEPENDENT = "timing_dependent"
    GENERATED_CODE_ERROR = "generated_code_error"  # For errors in Contractor-generated code
    UNKNOWN = "unknown"


class TestFixer:
    """
    LLM-powered sub-agent that fixes errors in generated tests AND source code.
    
    Supports multiple error categories:
    - Assertion mismatches (expected vs actual values)
    - Compilation errors (syntax, missing imports)
    - Runtime errors (NullPointer, exceptions)
    - Timeout issues
    - Timing-dependent assertions
    - Generated code errors (issues in Contractor-generated code)
    
    Uses iterative fixing: applies multiple fix strategies per error category.
    Can fix both test files and generated source code files.
    """
    
    def __init__(
        self, 
        llm_client: BaseLLMClient,
        model_name: str = "llama3.2",
        max_iterations: int = 3,
        max_fixes_per_category: int = 2
    ):
        """
        Initialize Test Fixer with LLM support.
        
        Args:
            llm_client: LLM client for intelligent code fixing (BaseLLMClient instance)
            model_name: LLM model to use for fixes
            max_iterations: Maximum number of fix iterations per test
            max_fixes_per_category: Maximum fixes to try per error category
        """
        self.llm_client = llm_client
        self.model_name = model_name
        self.max_iterations = max_iterations
        self.max_fixes_per_category = max_fixes_per_category
        
        # Metrics
        self.fixes_applied = 0
        self.tests_fixed = 0
        self.generated_code_fixed = 0  # Track generated code fixes separately
        self.fixes_by_category: Dict[ErrorCategory, int] = {cat: 0 for cat in ErrorCategory}
        self.failed_fixes_by_category: Dict[ErrorCategory, int] = {cat: 0 for cat in ErrorCategory}
        
    async def analyze_and_fix_test(
        self,
        test_code: str,
        error_message: str,
        test_name: str,
        iteration: int = 1
    ) -> Optional[str]:
        """
        Analyze test failure and apply LLM-powered fixes iteratively.
        
        This method:
        1. Categorizes the error type
        2. Applies category-specific fixes using LLM
        3. Tries multiple fix strategies per category
        4. Tracks metrics per category
        
        Args:
            test_code: Original test code
            error_message: Error message from test execution
            test_name: Name of the test
            iteration: Current iteration number
            
        Returns:
            Fixed code if successful, None otherwise
        """
        if iteration > self.max_iterations:
            logger.warning(f"🔴 Max iterations ({self.max_iterations}) reached for {test_name}")
            return None
        
        logger.info(f"🔧 Analyzing test failure (iteration {iteration}/{self.max_iterations}): {test_name}")
        logger.debug(f"Error message: {error_message[:200]}...")
        
        # Categorize the error
        error_category = self._categorize_error(error_message)
        logger.info(f"📊 Error category: {error_category.value}")
        
        # Try multiple fix strategies for this error category
        for fix_attempt in range(1, self.max_fixes_per_category + 1):
            logger.info(f"🔄 Fix attempt {fix_attempt}/{self.max_fixes_per_category} for category {error_category.value}")
            
            fixed_code = await self._apply_llm_fix(
                test_code=test_code,
                error_message=error_message,
                error_category=error_category,
                test_name=test_name,
                attempt_number=fix_attempt
            )
            
            if fixed_code and fixed_code != test_code:
                self.fixes_applied += 1
                self.fixes_by_category[error_category] += 1
                logger.info(f"✅ Fix applied successfully (category: {error_category.value}, attempt: {fix_attempt})")
                return fixed_code
            else:
                logger.warning(f"❌ Fix attempt {fix_attempt} failed for category {error_category.value}")
        
        # All fix attempts failed for this category
        self.failed_fixes_by_category[error_category] += 1
        logger.warning(f"🔴 All {self.max_fixes_per_category} fix attempts failed for {test_name}")
        return None
    
    async def analyze_and_fix_generated_code(
        self,
        code: str,
        error_message: str,
        file_name: str,
        file_type: str = "Java",
        iteration: int = 1
    ) -> Optional[str]:
        """
        Analyze errors in generated code (not tests) and apply LLM-powered fixes.
        
        This method handles errors in code generated by Contractor agent, such as:
        - Missing imports
        - Syntax errors
        - Package structure issues
        - Compilation errors
        
        Args:
            code: Original generated code
            error_message: Error message from compilation
            file_name: Name of the file (for context)
            file_type: Type of file (default: "Java")
            iteration: Current iteration number
            
        Returns:
            Fixed code if successful, None otherwise
        """
        if iteration > self.max_iterations:
            logger.warning(f"🔴 Max iterations ({self.max_iterations}) reached for generated code: {file_name}")
            return None
        
        logger.info(f"🔧🏗️ Analyzing generated code error (iteration {iteration}/{self.max_iterations}): {file_name}")
        logger.debug(f"Error message: {error_message[:200]}...")
        
        # Categorize as generated code error
        error_category = self._categorize_error(error_message, is_generated_code=True)
        logger.info(f"📊 Error category: {error_category.value}")
        
        # Try multiple fix strategies
        for fix_attempt in range(1, self.max_fixes_per_category + 1):
            logger.info(f"🔄 Fix attempt {fix_attempt}/{self.max_fixes_per_category} for generated code")
            
            fixed_code = await self._apply_llm_fix_for_generated_code(
                code=code,
                error_message=error_message,
                error_category=error_category,
                file_name=file_name,
                file_type=file_type,
                attempt_number=fix_attempt
            )
            
            if fixed_code and fixed_code != code:
                self.fixes_applied += 1
                self.generated_code_fixed += 1
                self.fixes_by_category[error_category] += 1
                logger.info(f"✅ Generated code fix applied successfully (attempt: {fix_attempt})")
                return fixed_code
            else:
                logger.warning(f"❌ Generated code fix attempt {fix_attempt} failed")
        
        # All fix attempts failed
        self.failed_fixes_by_category[error_category] += 1
        logger.warning(f"🔴 All {self.max_fixes_per_category} fix attempts failed for generated code: {file_name}")
        return None
    
    def _categorize_error(self, error_message: str, is_generated_code: bool = False) -> ErrorCategory:
        """
        Categorize the error based on error message patterns.
        
        Args:
            error_message: Error message from test execution or compilation
            is_generated_code: True if error is from generated source code (not test)
            
        Returns:
            ErrorCategory enum
        """
        error_lower = error_message.lower()
        
        # Check for generated code errors first
        if is_generated_code or "package does not exist" in error_lower or "class file not found" in error_lower:
            return ErrorCategory.GENERATED_CODE_ERROR
        
        if "comparisonfailure" in error_lower or ("expected:" in error_lower and "but was:" in error_lower):
            return ErrorCategory.ASSERTION_MISMATCH
        elif "compilation" in error_lower or "cannot find symbol" in error_lower:
            return ErrorCategory.COMPILATION_ERROR
        elif "nullpointerexception" in error_lower:
            return ErrorCategory.NULL_POINTER
        elif "timeout" in error_lower or "timed out" in error_lower:
            return ErrorCategory.TIMEOUT
        elif any(timing in error_lower for timing in ["date", "age", "expires"]):
            return ErrorCategory.TIMING_DEPENDENT
        elif "exception" in error_lower or "error" in error_lower:
            return ErrorCategory.RUNTIME_ERROR
        else:
            return ErrorCategory.UNKNOWN
    
    async def _apply_llm_fix(
        self,
        test_code: str,
        error_message: str,
        error_category: ErrorCategory,
        test_name: str,
        attempt_number: int
    ) -> Optional[str]:
        """
        Apply LLM-powered fix for a specific error category.
        
        Args:
            test_code: Original test code
            error_message: Error message
            error_category: Categorized error type
            test_name: Name of test
            attempt_number: Current attempt number for this category
            
        Returns:
            Fixed code or None
        """
        # Build category-specific prompt
        prompt = self._build_fix_prompt(test_code, error_message, error_category, attempt_number)
        
        try:
            # Call LLM with timeout
            logger.debug(f"🤖 Calling LLM ({self.model_name}) for fix...")
            response = await asyncio.wait_for(
                self.llm_client.generate(prompt=prompt),
                timeout=60.0
            )
            
            # Extract fixed code from response
            fixed_code = self._extract_code_from_response(response)
            
            if fixed_code:
                logger.debug(f"✅ LLM returned fixed code ({len(fixed_code)} chars)")
                return fixed_code
            else:
                logger.warning(f"⚠️ LLM response did not contain valid code")
                return None
                
        except asyncio.TimeoutError:
            logger.error(f"⏱️ LLM timeout after 60s for {test_name}")
            return None
        except Exception as e:
            logger.error(f"❌ LLM fix failed: {e}")
            return None
    
    async def _apply_llm_fix_for_generated_code(
        self,
        code: str,
        error_message: str,
        error_category: ErrorCategory,
        file_name: str,
        file_type: str,
        attempt_number: int
    ) -> Optional[str]:
        """
        Apply LLM-powered fix for generated code errors.
        
        Args:
            code: Original generated code
            error_message: Error message
            error_category: Categorized error type
            file_name: Name of file
            file_type: Type of file (Java, etc.)
            attempt_number: Current attempt number for this category
            
        Returns:
            Fixed code or None
        """
        # Build prompt for generated code fix
        prompt = self._build_generated_code_fix_prompt(
            code, error_message, error_category, file_name, file_type, attempt_number
        )
        
        try:
            # Call LLM with timeout
            logger.debug(f"🤖 Calling LLM ({self.model_name}) for generated code fix...")
            response = await asyncio.wait_for(
                self.llm_client.generate(prompt=prompt),
                timeout=60.0
            )
            
            # Extract fixed code from response
            fixed_code = self._extract_code_from_response(response)
            
            if fixed_code:
                logger.debug(f"✅ LLM returned fixed generated code ({len(fixed_code)} chars)")
                return fixed_code
            else:
                logger.warning(f"⚠️ LLM response did not contain valid code")
                return None
                
        except asyncio.TimeoutError:
            logger.error(f"⏱️ LLM timeout after 60s for generated code: {file_name}")
            return None
        except Exception as e:
            logger.error(f"❌ LLM generated code fix failed: {e}")
            return None
    
    def _build_fix_prompt(
        self,
        test_code: str,
        error_message: str,
        error_category: ErrorCategory,
        attempt_number: int
    ) -> str:
        """
        Build category-specific prompt for LLM fix.
        
        Args:
            test_code: Original test code
            error_message: Error message
            error_category: Error category
            attempt_number: Current attempt number
            
        Returns:
            Prompt string
        """
        base_prompt = f"""You are a Java test fixing expert. Fix the following Rest-Assured test that is failing.

ERROR CATEGORY: {error_category.value}
ATTEMPT NUMBER: {attempt_number}

FAILING TEST CODE:
```java
{test_code}
```

ERROR MESSAGE:
{error_message}

"""
        
        # Add category-specific instructions
        if error_category == ErrorCategory.ASSERTION_MISMATCH:
            base_prompt += """
INSTRUCTIONS:
1. Analyze the 'expected' vs 'but was' values in the error
2. Update the assertEquals() calls with the correct expected values
3. Keep the test structure unchanged
4. Return ONLY the fixed Java code, no explanations
"""
        elif error_category == ErrorCategory.COMPILATION_ERROR:
            base_prompt += """
INSTRUCTIONS:
1. Fix syntax errors (missing semicolons, brackets, quotes)
2. Add missing imports if needed
3. Correct method signatures
4. Return ONLY the fixed Java code, no explanations
"""
        elif error_category == ErrorCategory.NULL_POINTER:
            base_prompt += """
INSTRUCTIONS:
1. Add null checks before accessing response values
2. Use Optional or conditional checks
3. Add assertNotNull() where appropriate
4. Return ONLY the fixed Java code, no explanations
"""
        elif error_category == ErrorCategory.TIMEOUT:
            base_prompt += """
INSTRUCTIONS:
1. Increase timeout values (double them)
2. Add .timeout() to Rest-Assured calls
3. Consider using async patterns if needed
4. Return ONLY the fixed Java code, no explanations
"""
        elif error_category == ErrorCategory.TIMING_DEPENDENT:
            base_prompt += """
INSTRUCTIONS:
1. Remove assertions on timing-dependent headers (Date, Age, Expires)
2. Remove or relax time-based validations
3. Keep all other assertions intact
4. Return ONLY the fixed Java code, no explanations
"""
        else:
            base_prompt += """
INSTRUCTIONS:
1. Analyze the error and determine the root cause
2. Apply the most appropriate fix
3. Ensure the test remains valid
4. Return ONLY the fixed Java code, no explanations
"""
        
        base_prompt += "\n\nFIXED CODE:"
        return base_prompt
    
    def _build_generated_code_fix_prompt(
        self,
        code: str,
        error_message: str,
        error_category: ErrorCategory,
        file_name: str,
        file_type: str,
        attempt_number: int
    ) -> str:
        """
        Build prompt for fixing generated code (not tests).
        
        Args:
            code: Original generated code
            error_message: Error message
            error_category: Error category
            file_name: Name of file
            file_type: Type of file
            attempt_number: Current attempt number
            
        Returns:
            Prompt string
        """
        base_prompt = f"""You are a {file_type} code fixing expert. Fix the following generated code that has compilation or runtime errors.

FILE: {file_name}
ERROR CATEGORY: {error_category.value}
ATTEMPT NUMBER: {attempt_number}

FAILING CODE:
```{file_type.lower()}
{code}
```

ERROR MESSAGE:
{error_message}

INSTRUCTIONS:
1. Analyze the error message carefully
2. Fix compilation errors (missing imports, syntax errors, package issues)
3. Ensure proper package structure and imports
4. Fix any type mismatches or missing dependencies
5. Keep the code functionality unchanged
6. Return ONLY the fixed {file_type} code with proper imports and package declaration
7. Do NOT add explanations, just return the corrected code

IMPORTANT:
- Include ALL necessary imports at the top
- Maintain the original package declaration if present
- Fix all syntax errors and missing symbols
- Ensure the code compiles successfully

FIXED CODE:"""
        
        return base_prompt
    
    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """
        Extract Java code from LLM response.
        
        Args:
            response: LLM response text
            
        Returns:
            Extracted code or None
        """
        # Try to find code block
        code_block_pattern = r'```(?:java)?\s*([\s\S]+?)```'
        match = re.search(code_block_pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # If no code block, try to find class definition
        if 'public class' in response or '@Test' in response:
            return response.strip()
        
        return None
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get detailed fixer statistics including per-category metrics.
        
        Returns:
            Dictionary with comprehensive statistics for both tests and generated code
        """
        total_attempts = self.fixes_applied + sum(self.failed_fixes_by_category.values())
        return {
            "fixes_applied": self.fixes_applied,
            "tests_fixed": self.tests_fixed,
            "generated_code_fixed": self.generated_code_fixed,
            "fixes_by_category": {cat.value: count for cat, count in self.fixes_by_category.items() if count > 0},
            "failed_fixes_by_category": {cat.value: count for cat, count in self.failed_fixes_by_category.items() if count > 0},
            "success_rate": round(self.fixes_applied / total_attempts * 100, 2) if total_attempts > 0 else 0.0,
            "total_attempts": total_attempts
        }
