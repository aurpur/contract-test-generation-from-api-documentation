"""
Unit tests for RunnerAgent and MavenRunner.

Tests Maven execution, JUnit XML parsing, failure analysis,
and feedback loop for test regeneration.
"""
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from uuid import UUID, uuid4
import xml.etree.ElementTree as ET

from agents.runner import RunnerAgent, MavenRunner
from agents.base_agent import AgentConfig
from shared_context import (
    ContextManager,
    GeneratedTest,
    TestExecutionResult,
    AgentType,
)
from orchestration import Task


@pytest.fixture
def context_manager():
    """Mock context manager."""
    return MagicMock(spec=ContextManager)


@pytest.fixture
def message_router():
    """Mock message router."""
    router = MagicMock()
    router.register = MagicMock()
    router.send = AsyncMock()
    return router


@pytest.fixture
def event_bus():
    """Mock event bus."""
    bus = MagicMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture
def task_queue():
    """Mock task queue."""
    queue = MagicMock()
    queue.submit = AsyncMock()
    return queue


@pytest.fixture
def agent_config():
    """Agent configuration for tests."""
    return AgentConfig(
        agent_type=AgentType.RUNNER,
        max_concurrent_tasks=3,
        task_timeout=600.0,
    )


@pytest.fixture
def sample_generated_test():
    """Sample generated test."""
    return GeneratedTest(
        id=uuid4(),
        endpoint_id=uuid4(),
        oracle_id=uuid4(),
        test_class_name="GetUsersTest",
        test_method_name="testGetUsers",
        test_code="""
package generated;

import io.restassured.RestAssured;
import org.junit.jupiter.api.Test;
import static org.hamcrest.Matchers.*;

public class GetUsersTest {
    @Test
    public void testGetUsers() {
        RestAssured.given()
            .when()
            .get("/api/users")
            .then()
            .statusCode(200)
            .body("users", notNullValue());
    }
}
""",
        dependencies=["io.rest-assured:rest-assured:5.3.2"],
        generated_at=datetime.utcnow(),
    )


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create temporary Maven project directory."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()
    
    # Create target/surefire-reports directory
    reports_dir = project_dir / "target" / "surefire-reports"
    reports_dir.mkdir(parents=True)
    
    # Create src/test/java/generated directory
    test_dir = project_dir / "src" / "test" / "java" / "generated"
    test_dir.mkdir(parents=True)
    
    return project_dir


class TestMavenRunner:
    """Test MavenRunner functionality."""
    
    def test_initialization(self, temp_project_dir):
        """Test MavenRunner initialization."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            runner = MavenRunner(str(temp_project_dir))
            
            assert runner.project_dir == temp_project_dir
            assert runner.mvn_cmd == "mvn"
    
    def test_initialization_with_maven_home(self, temp_project_dir):
        """Test MavenRunner initialization with MAVEN_HOME."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            runner = MavenRunner(str(temp_project_dir), maven_home="/opt/maven")
            
            assert runner.mvn_cmd == "/opt/maven/bin/mvn"
    
    def test_verify_maven_failure(self, temp_project_dir):
        """Test Maven verification failure."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="mvn: command not found")
            
            with pytest.raises(RuntimeError, match="Maven not found"):
                MavenRunner(str(temp_project_dir))
    
    def test_parse_maven_output(self, temp_project_dir):
        """Test parsing Maven output for metrics."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            runner = MavenRunner(str(temp_project_dir))
        
        output = """
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running generated.GetUsersTest
Tests run: 5, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 1.234 s
"""
        
        metrics = runner._parse_maven_output(output)
        
        assert metrics["tests_run"] == 5
        assert metrics["tests_failed"] == 1
        assert metrics["tests_passed"] == 4
        assert metrics["tests_skipped"] == 0
        assert metrics["execution_time_ms"] == 1234.0
    
    def test_parse_junit_xml(self, temp_project_dir):
        """Test parsing JUnit XML reports."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            runner = MavenRunner(str(temp_project_dir))
        
        # Create sample JUnit XML
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="generated.GetUsersTest" tests="2" failures="1" errors="0" skipped="0" time="1.234">
    <testcase name="testGetUsers" classname="generated.GetUsersTest" time="0.5">
    </testcase>
    <testcase name="testGetUsersFails" classname="generated.GetUsersTest" time="0.734">
        <failure message="Expected: 200 but was: 404" type="java.lang.AssertionError">
java.lang.AssertionError: Expected: 200 but was: 404
    at generated.GetUsersTest.testGetUsersFails(GetUsersTest.java:25)
        </failure>
    </testcase>
</testsuite>
"""
        
        # Write XML file
        reports_dir = temp_project_dir / "target" / "surefire-reports"
        xml_file = reports_dir / "TEST-generated.GetUsersTest.xml"
        xml_file.write_text(xml_content)
        
        # Parse
        results = runner.parse_junit_xml()
        
        assert len(results) == 1
        testsuite = results[0]
        assert testsuite["name"] == "generated.GetUsersTest"
        assert testsuite["tests"] == 2
        assert testsuite["failures"] == 1
        assert len(testsuite["testcases"]) == 2
        
        # Check passed test
        assert testsuite["testcases"][0]["name"] == "testGetUsers"
        assert testsuite["testcases"][0]["passed"] is True
        
        # Check failed test
        assert testsuite["testcases"][1]["name"] == "testGetUsersFails"
        assert testsuite["testcases"][1]["passed"] is False
        assert testsuite["testcases"][1]["failure"]["message"] == "Expected: 200 but was: 404"


class TestRunnerAgentInitialization:
    """Test RunnerAgent initialization."""
    
    def test_initialization(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test agent initialization."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
            
            assert agent.agent_type == AgentType.RUNNER
            assert agent.project_dir == temp_project_dir
            assert agent.maven_runner is not None
            assert agent.max_retries == 2
            assert agent.timeout == 300
            assert agent.metrics["tests_run"] == 0


@pytest.mark.asyncio
class TestTestExecution:
    """Test test execution functionality."""
    
    async def test_write_tests_to_disk(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
        sample_generated_test,
    ):
        """Test writing tests to disk."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
            
            await agent._write_tests_to_disk([sample_generated_test])
            
            # Check file was written
            test_file = temp_project_dir / "src" / "test" / "java" / "generated" / "GetUsersTest.java"
            assert test_file.exists()
            
            # Check content
            content = test_file.read_text()
            assert "package generated;" in content
            assert "GetUsersTest" in content
    
    async def test_execute_single_test_task(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
        sample_generated_test,
    ):
        """Test execute_single_test task processing."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        # Mock context manager
        context_manager.get_generated_test = AsyncMock(return_value=sample_generated_test)
        context_manager.store_execution_result = AsyncMock()
        
        # Mock Maven execution
        with patch.object(agent.maven_runner, 'run_tests') as mock_run_tests:
            mock_run_tests.return_value = (
                True,
                "Tests run: 1, Failures: 0",
                {"tests_run": 1, "tests_passed": 1, "tests_failed": 0, "execution_time_ms": 500},
            )
            
            # Mock JUnit parsing
            with patch.object(agent.maven_runner, 'parse_junit_xml') as mock_parse:
                mock_parse.return_value = [{
                    "name": "generated.GetUsersTest",
                    "tests": 1,
                    "failures": 0,
                    "testcases": [{
                        "name": "testGetUsers",
                        "classname": "generated.GetUsersTest",
                        "time": 0.5,
                        "passed": True,
                    }]
                }]
                
                task = Task(
                    agent_type=AgentType.RUNNER,
                    task_type="execute_single_test",
                    session_id=uuid4(),
                    payload={"test_id": str(sample_generated_test.id)},
                )
                
                result = await agent.process_task(task)
                
                assert result["status"] == "success"
                assert result["passed"] is True
                assert result["execution_time_ms"] == 500


class TestFailureAnalysis:
    """Test failure analysis functionality."""
    
    def test_parse_assertion_failures(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test parsing assertion failures from stack trace."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        stack_trace = """
java.lang.AssertionError: Expected: 200 but was: 404
    at generated.GetUsersTest.testGetUsers(GetUsersTest.java:25)
"""
        
        failures = agent._parse_assertion_failures(stack_trace)
        
        assert len(failures) > 0
        assert "Expected: 200 but was: 404" in failures[0]
    
    def test_categorize_failure(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test failure categorization."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        # Assertion failure
        result1 = TestExecutionResult(
            test_id=uuid4(),
            passed=False,
            execution_time_ms=500,
            error_message="AssertionError: Expected 200 but was 404",
        )
        assert agent._categorize_failure(result1) == "assertion_failure"
        
        # Timeout
        result2 = TestExecutionResult(
            test_id=uuid4(),
            passed=False,
            execution_time_ms=5000,
            error_message="Test timed out after 5000ms",
        )
        assert agent._categorize_failure(result2) == "timeout"
        
        # Null pointer
        result3 = TestExecutionResult(
            test_id=uuid4(),
            passed=False,
            execution_time_ms=100,
            error_message="NullPointerException: Cannot read property 'users' of null",
        )
        assert agent._categorize_failure(result3) == "null_pointer"
    
    def test_generate_suggestions(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test generating suggestions from failure analysis."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        analysis = {
            "failure_types": {
                "assertion_failure": 3,
                "network_error": 1,
            }
        }
        
        suggestions = agent._generate_suggestions(analysis)
        
        assert len(suggestions) > 0
        assert any("oracle" in s.lower() for s in suggestions)
        assert any("network" in s.lower() for s in suggestions)


@pytest.mark.asyncio
class TestFeedbackLoop:
    """Test feedback loop for test regeneration."""
    
    async def test_trigger_regeneration(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test triggering test regeneration for failures."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        # Create failed results
        failed_results = [
            TestExecutionResult(
                test_id=uuid4(),
                passed=False,
                execution_time_ms=500,
                error_message="Assertion failed",
                assertion_failures=["Expected: 200 but was: 404"],
                retry_count=0,
            )
        ]
        
        session_id = uuid4()
        
        await agent._trigger_regeneration(failed_results, session_id)
        
        # Check message was sent
        message_router.send.assert_called_once()
        
        # Check metrics
        assert agent.metrics["retries"] == 1
    
    async def test_max_retries_exceeded(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test that regeneration is skipped when max retries exceeded."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
                max_retries=2,
            )
        
        # Create failed result with max retries
        failed_results = [
            TestExecutionResult(
                test_id=uuid4(),
                passed=False,
                execution_time_ms=500,
                error_message="Assertion failed",
                retry_count=2,  # Already at max
            )
        ]
        
        session_id = uuid4()
        
        await agent._trigger_regeneration(failed_results, session_id)
        
        # Check no message was sent
        message_router.send.assert_not_called()


@pytest.mark.asyncio
class TestMessageHandlers:
    """Test message handlers."""
    
    async def test_handle_execute_tests_message(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test execute_tests message handler."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        message = MagicMock()
        message.session_id = uuid4()
        message.payload = {"test_ids": [str(uuid4())]}
        
        await agent._handle_execute_tests_message(message)
        
        task_queue.submit.assert_called_once()
        message_router.send.assert_called_once()


class TestAgentRepr:
    """Test agent string representation."""
    
    def test_repr(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
    ):
        """Test string representation."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        repr_str = repr(agent)
        
        assert "RunnerAgent" in repr_str
        assert "state=" in repr_str
        assert "tests_run=" in repr_str
        assert "tests_passed=" in repr_str
        assert "tests_failed=" in repr_str


@pytest.mark.asyncio
class TestExecuteTestsIntegration:
    """Test execute_tests integration."""
    
    async def test_execute_multiple_tests(
        self,
        agent_config,
        context_manager,
        message_router,
        event_bus,
        task_queue,
        temp_project_dir,
        sample_generated_test,
    ):
        """Test executing multiple tests."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Apache Maven 3.8.1")
            
            agent = RunnerAgent(
                config=agent_config,
                context_manager=context_manager,
                message_router=message_router,
                event_bus=event_bus,
                task_queue=task_queue,
                project_dir=str(temp_project_dir),
            )
        
        # Create multiple tests
        test1 = sample_generated_test
        test2 = GeneratedTest(
            id=uuid4(),
            endpoint_id=uuid4(),
            oracle_id=uuid4(),
            test_class_name="PostUsersTest",
            test_method_name="testPostUsers",
            test_code="package generated; public class PostUsersTest {}",
            dependencies=[],
            generated_at=datetime.utcnow(),
        )
        
        # Mock context manager
        async def get_test_mock(test_id):
            if test_id == test1.id:
                return test1
            elif test_id == test2.id:
                return test2
            return None
        
        context_manager.get_generated_test = AsyncMock(side_effect=get_test_mock)
        context_manager.store_execution_result = AsyncMock()
        
        # Mock Maven execution
        with patch.object(agent.maven_runner, 'run_tests') as mock_run_tests:
            mock_run_tests.return_value = (
                True,
                "Tests run: 2, Failures: 0",
                {"tests_run": 2, "tests_passed": 2, "tests_failed": 0, "execution_time_ms": 1000},
            )
            
            # Mock JUnit parsing
            with patch.object(agent.maven_runner, 'parse_junit_xml') as mock_parse:
                mock_parse.return_value = [
                    {
                        "name": "generated.GetUsersTest",
                        "tests": 1,
                        "failures": 0,
                        "testcases": [{
                            "name": "testGetUsers",
                            "classname": "generated.GetUsersTest",
                            "time": 0.5,
                            "passed": True,
                        }]
                    },
                    {
                        "name": "generated.PostUsersTest",
                        "tests": 1,
                        "failures": 0,
                        "testcases": [{
                            "name": "testPostUsers",
                            "classname": "generated.PostUsersTest",
                            "time": 0.5,
                            "passed": True,
                        }]
                    }
                ]
                
                task = Task(
                    agent_type=AgentType.RUNNER,
                    task_type="execute_tests",
                    session_id=uuid4(),
                    payload={
                        "test_ids": [str(test1.id), str(test2.id)],
                        "session_id": str(uuid4()),
                    },
                )
                
                result = await agent.process_task(task)
                
                assert result["status"] == "success"
                assert result["tests_run"] == 2
                assert result["tests_passed"] == 2
                assert result["tests_failed"] == 0
