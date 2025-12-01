"""
Runner Agent - Executes Maven tests and analyzes results.

This agent executes generated Java tests using Maven, parses JUnit XML results,
analyzes failures, and provides feedback for test regeneration.

Author: Aurel IKAMA HONEY
"""
import asyncio
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from agents.base_agent import BaseAgent, AgentConfig
from agents.test_fixer import TestFixer
from shared_context import (
    ContextManager,
    GeneratedTest,
    TestExecutionResult,
    AgentType,
)
from orchestration import Task, MessageBuilder, TaskPriority
from utils.logging import logger


class MavenRunner:
    """
    Maven test execution wrapper.
    
    Handles Maven invocation, output parsing, and error handling.
    """
    
    def __init__(self, project_dir: str, maven_home: Optional[str] = None):
        """
        Initialize Maven runner.
        
        Args:
            project_dir: Path to Maven project directory
            maven_home: Optional Maven installation path
        """
        self.project_dir = Path(project_dir)
        self.maven_home = maven_home
        
        # Determine Maven command
        if maven_home:
            self.mvn_cmd = str(Path(maven_home) / "bin" / "mvn")
        else:
            self.mvn_cmd = "mvn"
        
        # Verify Maven is available
        self._verify_maven()
    
    def _verify_maven(self) -> None:
        """Verify Maven is installed and accessible."""
        try:
            result = subprocess.run(
                [self.mvn_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                raise RuntimeError(f"Maven not found: {result.stderr}")
            logger.info(f"Maven verified: {result.stdout.split()[2]}")
        except Exception as e:
            raise RuntimeError(f"Failed to verify Maven: {e}")
    
    async def run_tests(
        self,
        test_classes: Optional[List[str]] = None,
        timeout: int = 300,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Run Maven tests.
        
        Args:
            test_classes: Optional list of test class names to run
            timeout: Execution timeout in seconds
            
        Returns:
            Tuple of (success, output, metrics)
        """
        # Build Maven command
        cmd = [self.mvn_cmd, "test"]
        
        # Add specific test classes if provided
        if test_classes:
            test_pattern = ",".join(test_classes)
            cmd.extend(["-Dtest=" + test_pattern])
        
        logger.info(f"Executing Maven: {' '.join(cmd)}")
        
        try:
            # Run Maven
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.project_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            # Wait with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise TimeoutError(f"Maven execution timed out after {timeout}s")
            
            # Decode output
            output = stdout.decode('utf-8')
            error = stderr.decode('utf-8')
            
            # Parse metrics from output
            metrics = self._parse_maven_output(output)
            
            # Check success
            success = process.returncode == 0
            
            full_output = output + "\n" + error if error else output
            
            return success, full_output, metrics
            
        except Exception as e:
            logger.error(f"Maven execution failed: {e}")
            return False, str(e), {}
    
    def _parse_maven_output(self, output: str) -> Dict[str, Any]:
        """
        Parse Maven test output for metrics.
        
        Args:
            output: Maven output text
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_skipped": 0,
            "execution_time_ms": 0,
        }
        
        # Pattern: Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
        pattern = r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)"
        match = re.search(pattern, output)
        
        if match:
            tests_run = int(match.group(1))
            failures = int(match.group(2))
            errors = int(match.group(3))
            skipped = int(match.group(4))
            
            metrics["tests_run"] = tests_run
            metrics["tests_failed"] = failures + errors
            metrics["tests_passed"] = tests_run - failures - errors - skipped
            metrics["tests_skipped"] = skipped
        
        # Pattern: Time elapsed: 1.234 s
        time_pattern = r"Time elapsed: ([\d.]+) s"
        time_match = re.search(time_pattern, output)
        
        if time_match:
            metrics["execution_time_ms"] = float(time_match.group(1)) * 1000
        
        return metrics
    
    def parse_junit_xml(self, surefire_reports_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Parse JUnit XML reports.
        
        Args:
            surefire_reports_dir: Path to surefire-reports directory
            
        Returns:
            List of test result dictionaries
        """
        if surefire_reports_dir is None:
            surefire_reports_dir = self.project_dir / "target" / "surefire-reports"
        else:
            surefire_reports_dir = Path(surefire_reports_dir)
        
        if not surefire_reports_dir.exists():
            logger.warning(f"Surefire reports directory not found: {surefire_reports_dir}")
            return []
        
        results = []
        
        # Find all TEST-*.xml files
        for xml_file in surefire_reports_dir.glob("TEST-*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Parse testsuite
                testsuite = {
                    "name": root.get("name"),
                    "tests": int(root.get("tests", 0)),
                    "failures": int(root.get("failures", 0)),
                    "errors": int(root.get("errors", 0)),
                    "skipped": int(root.get("skipped", 0)),
                    "time": float(root.get("time", 0)),
                    "testcases": [],
                }
                
                # Parse testcases
                for testcase in root.findall("testcase"):
                    tc = {
                        "name": testcase.get("name"),
                        "classname": testcase.get("classname"),
                        "time": float(testcase.get("time", 0)),
                        "passed": True,
                        "failure": None,
                        "error": None,
                        "skipped": False,
                    }
                    
                    # Check for failure
                    failure = testcase.find("failure")
                    if failure is not None:
                        tc["passed"] = False
                        tc["failure"] = {
                            "message": failure.get("message"),
                            "type": failure.get("type"),
                            "text": failure.text,
                        }
                    
                    # Check for error
                    error = testcase.find("error")
                    if error is not None:
                        tc["passed"] = False
                        tc["error"] = {
                            "message": error.get("message"),
                            "type": error.get("type"),
                            "text": error.text,
                        }
                    
                    # Check for skipped
                    skipped = testcase.find("skipped")
                    if skipped is not None:
                        tc["skipped"] = True
                    
                    testsuite["testcases"].append(tc)
                
                results.append(testsuite)
                
            except Exception as e:
                logger.error(f"Failed to parse JUnit XML {xml_file}: {e}")
        
        return results


class RunnerAgent(BaseAgent):
    """
    Runner Agent executes Maven tests and analyzes results.
    
    Workflow:
    1. Retrieve generated tests from ContextManager
    2. Write test files to disk
    3. Execute Maven tests
    4. Parse JUnit XML results
    5. Analyze failures
    6. Store execution results in ContextManager
    7. Trigger regeneration for failed tests (feedback loop)
    
    Features:
    - Maven test execution
    - JUnit XML parsing
    - Failure analysis
    - Feedback loop for test regeneration
    - Retry logic with exponential backoff
    - Parallel test execution support
    - Timeout handling
    """
    
    def __init__(
        self,
        config: AgentConfig,
        context_manager: ContextManager,
        message_router,
        event_bus,
        task_queue,
        project_dir: str,
        maven_home: Optional[str] = None,
        max_retries: int = 2,
        timeout: int = 300,
    ):
        """
        Initialize Runner Agent.
        
        Args:
            config: Agent configuration
            context_manager: Shared context manager
            message_router: Message router for inter-agent communication
            event_bus: Event bus for publishing events
            task_queue: Task queue for processing
            project_dir: Maven project directory
            maven_home: Optional Maven installation path
            max_retries: Maximum retries for failed tests
            timeout: Test execution timeout in seconds
        """
        super().__init__(
            config=config,
            context_manager=context_manager,
            router=message_router,
            event_bus=event_bus,
            task_queue=task_queue,
        )
        
        self.project_dir = Path(project_dir)
        self.maven_runner = MavenRunner(project_dir, maven_home)
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Initialize test fixer sub-agent with LLM support
        from utils.llm_client import OllamaClient
        from utils.config import get_config
        
        config_data = get_config()
        test_fixer_config = config_data.agents.get('test_fixer', None)
        test_fixer_model = test_fixer_config.model if test_fixer_config and hasattr(test_fixer_config, 'model') else 'llama3.2'
        max_iterations = test_fixer_config.max_iterations if test_fixer_config and hasattr(test_fixer_config, 'max_iterations') else 3
        max_fixes_per_category = test_fixer_config.max_fixes_per_category if test_fixer_config and hasattr(test_fixer_config, 'max_fixes_per_category') else 2
        
        llm_client = OllamaClient(model=test_fixer_model)
        self.test_fixer = TestFixer(
            llm_client=llm_client,
            model_name=test_fixer_model,
            max_iterations=max_iterations,
            max_fixes_per_category=max_fixes_per_category
        )
        logger.info(f"🔧 Test fixer sub-agent initialized (model: {test_fixer_model}, max iterations: {max_iterations}, max fixes per category: {max_fixes_per_category})")
        
        # Metrics
        self._metrics["tests_run"] = 0
        self._metrics["tests_passed"] = 0
        self._metrics["tests_failed"] = 0
        self._metrics["execution_time_ms"] = 0
        self._metrics["retries"] = 0
        self._metrics["tests_auto_fixed"] = 0
    
    def register_handlers(self) -> None:
        """Register message handlers for test execution."""
        # Message routing is handled by BaseAgent
        pass
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process test execution tasks.
        
        Args:
            task: Task to process
            
        Returns:
            Task result dictionary
        """
        task_type = task.task_type
        
        if task_type == "execute_tests":
            return await self._execute_tests(task)
        elif task_type == "execute_single_test":
            return await self._execute_single_test(task)
        elif task_type == "analyze_failures":
            return await self._analyze_failures(task)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    async def _execute_tests(self, task: Task) -> Dict[str, Any]:
        """
        Execute multiple tests.
        
        Args:
            task: Task with test_ids in payload
            
        Returns:
            Result with execution summary
        """
        test_ids = task.payload.get("test_ids", [])
        session_id = task.payload.get("session_id")
        output_dir = task.payload.get("output_dir")
        
        # Update project_dir if specified in payload (for execution-specific directories)
        if output_dir:
            self.project_dir = Path(output_dir)
            self.maven_runner.project_dir = self.project_dir
            logger.debug(f"Updated project_dir to: {self.project_dir}")
        
        if not test_ids:
            logger.warning("No test IDs provided for execution")
            return {"status": "error", "error": "No test IDs provided"}
        
        logger.info(f"Executing {len(test_ids)} tests")
        
        # Retrieve tests
        session_id_uuid = session_id
        if isinstance(session_id_uuid, str):
            session_id_uuid = UUID(session_id_uuid)
        
        all_tests = await self.context_manager.get_tests(session_id=session_id_uuid)
        tests = []
        for test_id in test_ids:
            test_uuid = UUID(test_id) if isinstance(test_id, str) else test_id
            test = next((t for t in all_tests if t.id == test_uuid), None)
            if test:
                tests.append(test)
        
        if not tests:
            logger.warning("No tests found to execute")
            return {"status": "error", "error": "No tests found"}
        
        # Write tests to disk
        await self._write_tests_to_disk(tests)
        
        # First, try to compile the project to detect errors in generated code
        logger.info("🔨 Compiling project to detect errors in generated code...")
        compile_success = await self._compile_and_fix_generated_code(session_id_uuid)
        
        if not compile_success:
            logger.warning("⚠️ Compilation still has errors after auto-fix attempts")
        
        # Execute Maven tests
        test_classes = [test.test_class_name for test in tests]
        success, output, metrics = await self.maven_runner.run_tests(
            test_classes=test_classes,
            timeout=self.timeout,
        )
        
        # Parse JUnit XML
        junit_results = self.maven_runner.parse_junit_xml()
        
        # Create execution results
        execution_results = []
        for test in tests:
            result = await self._create_execution_result(test, junit_results, output)
            if result:
                await self.context_manager.add_execution_result(session_id_uuid, result)
                execution_results.append(result)
        
        # Update metrics
        self._metrics["tests_run"] += metrics.get("tests_run", 0)
        self._metrics["tests_passed"] += metrics.get("tests_passed", 0)
        self._metrics["tests_failed"] += metrics.get("tests_failed", 0)
        self._metrics["execution_time_ms"] += metrics.get("execution_time_ms", 0)
        
        # Analyze failures
        failed_tests = [r for r in execution_results if not r.passed]
        
        # Try to auto-fix failed tests before triggering regeneration
        if failed_tests and session_id:
            execution_results, failed_tests = await self._try_auto_fix_tests(
                failed_tests, 
                execution_results, 
                session_id_uuid
            )
        
        # Trigger regeneration for tests that couldn't be auto-fixed
        if failed_tests and session_id:
            await self._trigger_regeneration(failed_tests, session_id)
        
        # Publish event
        if session_id:
            await self.event_bus.publish(
                event_type="tests_executed",
                event_data={
                    "session_id": str(session_id),
                    "tests_run": len(execution_results),
                    "tests_passed": len([r for r in execution_results if r.passed]),
                    "tests_failed": len(failed_tests),
                    "execution_time_ms": metrics.get("execution_time_ms", 0),
                },
            )
        
        return {
            "status": "success",
            "tests_run": len(execution_results),
            "tests_passed": len([r for r in execution_results if r.passed]),
            "tests_failed": len(failed_tests),
            "execution_time_ms": metrics.get("execution_time_ms", 0),
            "maven_success": success,
        }
    
    async def _compile_and_fix_generated_code(self, session_id: UUID) -> bool:
        """
        Compile project and fix any errors in generated code (not tests).
        
        This method:
        1. Runs 'mvn compile' to compile only the generated code
        2. Detects compilation errors
        3. Uses TestFixer to fix errors in generated code
        4. Retries compilation after fixes
        
        Args:
            session_id: Session ID
            
        Returns:
            True if compilation succeeds (after fixes), False otherwise
        """
        logger.info("🔨 Attempting to compile generated code...")
        
        max_compile_attempts = 3
        for attempt in range(1, max_compile_attempts + 1):
            logger.info(f"📝 Compilation attempt {attempt}/{max_compile_attempts}")
            
            # Run Maven compile (not test-compile, just compile)
            cmd = [self.maven_runner.mvn_cmd, "compile", "-f", str(self.maven_runner.project_dir / "pom.xml")]
            
            try:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(self.maven_runner.project_dir)
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=120.0
                )
                
                output = stdout.decode() + stderr.decode()
                
                if process.returncode == 0:
                    logger.info("✅ Compilation successful!")
                    return True
                else:
                    logger.warning(f"❌ Compilation failed (exit code: {process.returncode})")
                    
                    # Try to fix generated code errors
                    if attempt < max_compile_attempts:
                        fixed = await self._fix_compilation_errors_in_generated_code(output, session_id)
                        if not fixed:
                            logger.warning("⚠️ Could not fix compilation errors")
                            break
                    else:
                        logger.error("🔴 Max compilation attempts reached")
                        return False
                        
            except asyncio.TimeoutError:
                logger.error("⏱️ Compilation timeout after 120s")
                return False
            except Exception as e:
                logger.error(f"❌ Compilation error: {e}")
                return False
        
        return False
    
    async def _fix_compilation_errors_in_generated_code(self, maven_output: str, session_id: UUID) -> bool:
        """
        Parse Maven compilation output and fix errors in generated code using TestFixer.
        
        Args:
            maven_output: Maven compilation output
            session_id: Session ID
            
        Returns:
            True if any fixes were applied, False otherwise
        """
        logger.info("🔧 Analyzing compilation errors in generated code...")
        
        # Parse compilation errors from Maven output
        # Pattern: [ERROR] /path/to/file.java:[line,col] error message
        error_pattern = r'\[ERROR\] (.+\.java):\[(\d+),(\d+)\] (.+)'
        errors = re.findall(error_pattern, maven_output)
        
        if not errors:
            logger.warning("No compilation errors found in Maven output")
            return False
        
        logger.info(f"Found {len(errors)} compilation errors in generated code")
        
        fixed_any = False
        fixed_files = set()
        
        for file_path, line, col, error_msg in errors:
            if file_path in fixed_files:
                continue  # Already processed this file
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                logger.warning(f"File not found: {file_path}")
                continue
            
            # Read the file
            try:
                with open(file_path_obj, 'r') as f:
                    original_code = f.read()
                
                logger.info(f"🔧 Attempting to fix: {file_path_obj.name}")
                
                # Use TestFixer to fix generated code
                full_error_message = f"[Line {line}, Col {col}] {error_msg}\n\nFull Maven output:\n{maven_output[:1000]}"
                
                fixed_code = await self.test_fixer.analyze_and_fix_generated_code(
                    code=original_code,
                    error_message=full_error_message,
                    file_name=file_path_obj.name,
                    file_type="Java"
                )
                
                if fixed_code and fixed_code != original_code:
                    # Write fixed code back to file
                    with open(file_path_obj, 'w') as f:
                        f.write(fixed_code)
                    
                    logger.info(f"✅ Fixed generated code: {file_path_obj.name}")
                    fixed_files.add(file_path)
                    fixed_any = True
                else:
                    logger.warning(f"❌ Could not fix: {file_path_obj.name}")
                    
            except Exception as e:
                logger.error(f"Error fixing {file_path}: {e}")
                continue
        
        if fixed_any:
            logger.info(f"✅ Fixed {len(fixed_files)} generated code files")
        else:
            logger.warning("❌ No generated code files were fixed")
        
        return fixed_any
    
    async def _try_auto_fix_tests(
        self, 
        failed_tests: List[TestExecutionResult], 
        all_results: List[TestExecutionResult],
        session_id: UUID
    ) -> Tuple[List[TestExecutionResult], List[TestExecutionResult]]:
        """
        Try to automatically fix failed tests using TestFixer.
        
        Args:
            failed_tests: List of failed test results
            all_results: List of all execution results
            session_id: Session ID
            
        Returns:
            Tuple of (updated_all_results, remaining_failed_tests)
        """
        logger.info(f"Attempting auto-fix for {len(failed_tests)} failed tests")
        
        fixed_count = 0
        remaining_failed = []
        updated_results = all_results.copy()
        
        for failed_result in failed_tests:
            try:
                # Get test from context
                all_tests = await self.context_manager.get_tests(session_id=session_id)
                test = next((t for t in all_tests if t.id == failed_result.test_id), None)
                
                if not test:
                    logger.warning(f"Test not found for result {failed_result.test_id}")
                    remaining_failed.append(failed_result)
                    continue
                
                # Analyze and fix the test
                logger.info(f"Attempting to fix test: {test.test_class_name}")
                fixed_code = await self.test_fixer.analyze_and_fix_test(
                    test_code=test.test_code,
                    error_message=failed_result.error_message or "",
                    test_name=test.test_class_name
                )
                
                # If code was modified, update test and re-execute
                if fixed_code and fixed_code != test.test_code:
                    logger.info(f"Test fixed, re-executing: {test.test_class_name}")
                    
                    # Update test code
                    test.test_code = fixed_code
                    await self.context_manager.update_test(test, session_id)
                    
                    # Write fixed test to disk
                    await self._write_tests_to_disk([test])
                    
                    # Re-execute the fixed test
                    success, output, metrics = await self.maven_runner.run_tests(
                        test_classes=[test.test_class_name],
                        timeout=self.timeout,
                    )
                    
                    # Parse JUnit XML for new results
                    junit_results = self.maven_runner.parse_junit_xml()
                    
                    # Create new execution result
                    new_result = await self._create_execution_result(test, junit_results, output)
                    
                    if new_result:
                        # Update metrics
                        if new_result.passed:
                            fixed_count += 1
                            self._metrics["tests_auto_fixed"] += 1
                            logger.info(f"✓ Test auto-fixed successfully: {test.test_class_name}")
                        else:
                            remaining_failed.append(new_result)
                            logger.warning(f"✗ Test still failing after fix: {test.test_class_name}")
                        
                        # Replace old result with new one
                        updated_results = [
                            new_result if r.test_id == failed_result.test_id else r 
                            for r in updated_results
                        ]
                        
                        # Store new result
                        await self.context_manager.add_execution_result(session_id, new_result)
                    else:
                        remaining_failed.append(failed_result)
                else:
                    # No fix applied, keep as failed
                    remaining_failed.append(failed_result)
                    logger.info(f"No fix could be applied for: {test.test_class_name}")
                    
            except Exception as e:
                logger.error(f"Error during auto-fix: {e}")
                remaining_failed.append(failed_result)
        
        # Log statistics
        if fixed_count > 0:
            stats = self.test_fixer.get_statistics()
            logger.info(f"Auto-fix summary: {fixed_count}/{len(failed_tests)} tests fixed")
            logger.info(f"TestFixer stats: {stats}")
        
        return updated_results, remaining_failed
    
    async def _execute_single_test(self, task: Task) -> Dict[str, Any]:
        """
        Execute a single test.
        
        Args:
            task: Task with test_id in payload
            
        Returns:
            Result with execution details
        """
        test_id = task.payload.get("test_id")
        
        if not test_id:
            return {"status": "error", "error": "No test_id provided"}
        
        # Retrieve test
        session_id_uuid = task.session_id
        if isinstance(session_id_uuid, str):
            session_id_uuid = UUID(session_id_uuid)
        
        all_tests = await self.context_manager.get_tests(session_id=session_id_uuid)
        test_uuid = UUID(test_id) if isinstance(test_id, str) else test_id
        test = next((t for t in all_tests if t.id == test_uuid), None)
        
        if not test:
            return {"status": "error", "error": f"Test not found: {test_id}"}
        
        # Write test to disk
        await self._write_tests_to_disk([test])
        
        # Execute Maven
        success, output, metrics = await self.maven_runner.run_tests(
            test_classes=[test.test_class_name],
            timeout=self.timeout,
        )
        
        # Parse JUnit XML
        junit_results = self.maven_runner.parse_junit_xml()
        
        # Create execution result
        result = await self._create_execution_result(test, junit_results, output)
        
        if result:
            await self.context_manager.add_execution_result(session_id_uuid, result)
            
            self._metrics["tests_run"] += 1
            if result.passed:
                self._metrics["tests_passed"] += 1
            else:
                self._metrics["tests_failed"] += 1
            self._metrics["execution_time_ms"] += result.execution_time_ms
            
            return {
                "status": "success",
                "passed": result.passed,
                "execution_time_ms": result.execution_time_ms,
                "error_message": result.error_message,
            }
        else:
            return {"status": "error", "error": "Failed to create execution result"}
    
    async def _analyze_failures(self, task: Task) -> Dict[str, Any]:
        """
        Analyze test failures.
        
        Args:
            task: Task with result_ids in payload
            
        Returns:
            Failure analysis
        """
        result_ids = task.payload.get("result_ids", [])
        
        if not result_ids:
            return {"status": "error", "error": "No result IDs provided"}
        
        # Retrieve execution results
        results = []
        for result_id in result_ids:
            result = await self.context_manager.get_execution_result(
                result_id=UUID(result_id) if isinstance(result_id, str) else result_id
            )
            if result:
                results.append(result)
        
        # Analyze failures
        analysis = {
            "total_failures": len(results),
            "failure_types": {},
            "common_errors": [],
            "suggestions": [],
        }
        
        for result in results:
            if not result.passed:
                # Categorize failure
                failure_type = self._categorize_failure(result)
                analysis["failure_types"][failure_type] = \
                    analysis["failure_types"].get(failure_type, 0) + 1
                
                # Extract common errors
                if result.error_message:
                    analysis["common_errors"].append(result.error_message)
        
        # Generate suggestions
        analysis["suggestions"] = self._generate_suggestions(analysis)
        
        return {
            "status": "success",
            "analysis": analysis,
        }
    
    async def _write_tests_to_disk(self, tests: List[GeneratedTest]) -> None:
        """
        Write test files to disk in Maven structure.
        
        Args:
            tests: List of generated tests
        """
        # Create Maven structure for test execution
        maven_test_dir = self.project_dir / "src" / "test" / "java" / "generated"
        maven_test_dir.mkdir(parents=True, exist_ok=True)
        
        maven_features_dir = maven_test_dir / "features"
        maven_features_dir.mkdir(parents=True, exist_ok=True)
        
        # Create pom.xml if it doesn't exist
        self._create_maven_pom()
        
        for test in tests:
            # Write Java test file to Maven directory
            java_filename = f"{test.test_class_name}.java"
            maven_filepath = maven_test_dir / java_filename
            
            with open(maven_filepath, 'w', encoding='utf-8') as f:
                f.write(test.test_code)
            
            logger.info(f"Written test file: {maven_filepath}")
            
            # Write Gherkin feature file if present
            if test.feature_file_name and test.feature_content:
                maven_feature_path = maven_features_dir / test.feature_file_name
                with open(maven_feature_path, 'w', encoding='utf-8') as f:
                    f.write(test.feature_content)
                
                logger.info(f"Written feature file: {maven_feature_path}")
    
    def _create_maven_pom(self) -> None:
        """
        Create Maven pom.xml file for test execution.
        """
        pom_path = self.project_dir / "pom.xml"
        
        # Only create if it doesn't exist
        if pom_path.exists():
            logger.debug(f"Maven pom.xml already exists: {pom_path}")
            return
        
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.contract.test</groupId>
    <artifactId>generated-contract-tests</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Generated Contract Tests</name>
    <description>Auto-generated REST-Assured contract tests</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <rest-assured.version>5.3.0</rest-assured.version>
        <junit.version>5.9.3</junit.version>
        <cucumber.version>7.12.0</cucumber.version>
    </properties>

    <dependencies>
        <!-- REST-Assured for API testing -->
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <version>${rest-assured.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- JUnit 5 for test execution -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- Cucumber for BDD testing -->
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-java</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-junit-platform-engine</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- JSON parsing -->
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.10.1</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Maven Compiler Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>

            <!-- Maven Surefire Plugin for running tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0</version>
                <configuration>
                    <includes>
                        <include>**/*Test.java</include>
                    </includes>
                    <testFailureIgnore>false</testFailureIgnore>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""
        
        with open(pom_path, 'w', encoding='utf-8') as f:
            f.write(pom_content)
        
        logger.info(f"Created Maven pom.xml: {pom_path}")
    
    async def _create_execution_result(
        self,
        test: GeneratedTest,
        junit_results: List[Dict[str, Any]],
        maven_output: str,
    ) -> Optional[TestExecutionResult]:
        """
        Create execution result from JUnit XML and Maven output.
        
        Args:
            test: Generated test
            junit_results: Parsed JUnit XML results
            maven_output: Maven output text
            
        Returns:
            TestExecutionResult or None
        """
        # Find matching test case in JUnit results
        for testsuite in junit_results:
            for testcase in testsuite["testcases"]:
                if testcase["classname"] == f"generated.{test.test_class_name}":
                    # Create result
                    result = TestExecutionResult(
                        test_id=test.id,
                        passed=testcase["passed"],
                        execution_time_ms=testcase["time"] * 1000,
                        maven_output=maven_output,
                    )
                    
                    # Add failure details
                    if testcase.get("failure"):
                        failure = testcase["failure"]
                        result.error_message = failure.get("message")
                        result.stack_trace = failure.get("text")
                        
                        # Parse assertion failures
                        if failure.get("text"):
                            result.assertion_failures = self._parse_assertion_failures(
                                failure["text"]
                            )
                    
                    # Add error details
                    if testcase.get("error"):
                        error = testcase["error"]
                        result.error_message = error.get("message")
                        result.stack_trace = error.get("text")
                    
                    return result
        
        # No matching test case found, create basic result
        logger.warning(f"No JUnit result found for test: {test.test_class_name}")
        return TestExecutionResult(
            test_id=test.id,
            passed=False,
            execution_time_ms=0,
            error_message="Test not executed or result not found",
            maven_output=maven_output,
        )
    
    def _parse_assertion_failures(self, stack_trace: str) -> List[str]:
        """
        Parse assertion failures from stack trace.
        
        Args:
            stack_trace: Stack trace text
            
        Returns:
            List of assertion failure messages
        """
        failures = []
        
        # Pattern: Expected: <value> but was: <value>
        pattern = r"Expected: .+ but was: .+"
        matches = re.findall(pattern, stack_trace)
        failures.extend(matches)
        
        # Pattern: Expecting actual not to be null
        if "Expecting actual not to be null" in stack_trace:
            failures.append("Null value encountered")
        
        return failures
    
    def _categorize_failure(self, result: TestExecutionResult) -> str:
        """
        Categorize test failure.
        
        Args:
            result: Test execution result
            
        Returns:
            Failure category
        """
        if not result.error_message:
            return "unknown"
        
        error = result.error_message.lower()
        
        if "assertion" in error or "expected" in error:
            return "assertion_failure"
        elif "timeout" in error or "timed out" in error:
            return "timeout"
        elif "connection" in error or "network" in error:
            return "network_error"
        elif "null" in error:
            return "null_pointer"
        elif "compile" in error or "syntax" in error:
            return "compilation_error"
        else:
            return "runtime_error"
    
    def _generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate suggestions based on failure analysis.
        
        Args:
            analysis: Failure analysis
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        failure_types = analysis.get("failure_types", {})
        
        if "assertion_failure" in failure_types:
            suggestions.append(
                "Review oracle assertions - they may not match actual API behavior"
            )
        
        if "network_error" in failure_types:
            suggestions.append(
                "Check API availability and network connectivity"
            )
        
        if "null_pointer" in failure_types:
            suggestions.append(
                "Review response schema validation - fields may be missing or null"
            )
        
        if "timeout" in failure_types:
            suggestions.append(
                "Increase test timeout or optimize API performance"
            )
        
        if "compilation_error" in failure_types:
            suggestions.append(
                "Review generated code syntax and imports"
            )
        
        return suggestions
    
    async def _trigger_regeneration(
        self,
        failed_results: List[TestExecutionResult],
        session_id: UUID,
    ) -> None:
        """
        Trigger test regeneration for failed tests (feedback loop).
        Regenerated tests will be automatically executed through Runner + TestFixer.
        
        Args:
            failed_results: List of failed test results
            session_id: Workflow session ID
        """
        logger.info(f"🔄 Triggering regeneration for {len(failed_results)} failed tests")
        
        for result in failed_results:
            # Check retry count
            if result.retry_count >= self.max_retries:
                logger.warning(
                    f"⚠️ Max retries ({self.max_retries}) reached for test {result.test_id}, skipping regeneration"
                )
                continue
            
            logger.info(
                f"♻️ Regeneration requested for test {result.test_id}: "
                f"{result.error_message} (retry {result.retry_count + 1}/{self.max_retries})"
            )
            
            # Publish regeneration event to Contractor agent
            # The Contractor will regenerate the test and automatically execute it via Runner
            try:
                await self.event_bus.publish(
                    "contractor.regenerate_test",
                    {
                        "test_id": str(result.test_id),
                        "failure_reason": result.error_message,
                        "assertion_failures": result.assertion_failures,
                        "retry_count": result.retry_count + 1,
                        "session_id": str(session_id)
                    }
                )
                logger.info(f"✅ Regeneration event published for test {result.test_id}")
                self._metrics["retries"] += 1
            except Exception as e:
                logger.error(f"❌ Failed to publish regeneration event for test {result.test_id}: {e}")
    
    # Message handlers
    
    async def _handle_execute_tests_message(self, message) -> None:
        """Handle execute_tests message."""
        task = Task(
            agent_type=AgentType.RUNNER,
            task_type="execute_tests",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    async def _handle_execute_single_test_message(self, message) -> None:
        """Handle execute_single_test message."""
        task = Task(
            agent_type=AgentType.RUNNER,
            task_type="execute_single_test",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    async def _handle_analyze_failures_message(self, message) -> None:
        """Handle analyze_failures message."""
        task = Task(
            agent_type=AgentType.RUNNER,
            task_type="analyze_failures",
            session_id=message.session_id,
            payload=message.payload,
        )
        
        await self.task_queue.submit(task)
        
        response = MessageBuilder.create_response(
            original_message=message,
            response_data={"status": "accepted", "task_id": str(task.id)},
        )
        await self.message_router.send(response)
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"RunnerAgent(state={self.state.value}, "
            f"active_tasks={len(self._active_tasks)}, "
            f"tests_run={self._metrics['tests_run']}, "
            f"tests_passed={self._metrics['tests_passed']}, "
            f"tests_failed={self._metrics['tests_failed']})"
        )
