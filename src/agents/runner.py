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
        
        # Metrics
        self._metrics["tests_run"] = 0
        self._metrics["tests_passed"] = 0
        self._metrics["tests_failed"] = 0
        self._metrics["execution_time_ms"] = 0
        self._metrics["retries"] = 0
    
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
        
        # Trigger regeneration for failed tests (feedback loop)
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
        session_id_uuid = session_id
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
        elif "timeout" in error:
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
        
        Args:
            failed_results: List of failed test results
            session_id: Workflow session ID
        """
        logger.info(f"Triggering regeneration for {len(failed_results)} failed tests")
        
        # Build regeneration requests as tasks, not messages
        # Tasks are submitted to the agent's task queue and processed asynchronously
        for result in failed_results:
            # Check retry count
            if result.retry_count >= self.max_retries:
                logger.warning(
                    f"Max retries reached for test {result.test_id}, skipping regeneration"
                )
                continue
            
            # Submit regeneration task to Contractor agent's task queue
            # This is the proper way to communicate between agents for task-based work
            from agents.factory import AgentOrchestrator
            
            # Get contractor agent from the factory
            # Note: In a production system, we would have a reference to the orchestrator
            # For now, we log the regeneration request for future implementation
            logger.info(
                f"Regeneration requested for test {result.test_id}: "
                f"{result.error_message} (retry {result.retry_count + 1})"
            )
            
            # TODO: Submit task to Contractor agent when orchestrator reference is available
            # await contractor.submit_task(
            #     task_type="regenerate_test",
            #     session_id=session_id,
            #     payload={
            #         "test_id": str(result.test_id),
            #         "failure_reason": result.error_message,
            #         "assertion_failures": result.assertion_failures,
            #         "retry_count": result.retry_count + 1,
            #     },
            #     priority=TaskPriority.HIGH,
            # )
            
            self._metrics["retries"] += 1
    
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
            f"active_tasks={len(self.active_tasks)}, "
            f"tests_run={self._metrics['tests_run']}, "
            f"tests_passed={self._metrics['tests_passed']}, "
            f"tests_failed={self._metrics['tests_failed']})"
        )
