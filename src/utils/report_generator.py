"""
Report generation utilities for contract test generation workflow.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from uuid import UUID
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
from loguru import logger

from shared_context.models import (
    EndpointContext,
    Oracle,
    GeneratedTest,
    TestExecutionResult,
)


class ReportGenerator:
    """Generate various reports for the workflow execution."""
    
    def __init__(self, output_dir: Path = Path("output/reports")):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.logs_dir = self.output_dir / "logs"
        self.graphs_dir = self.output_dir / "graphs"
        self.traces_dir = self.output_dir / "traces"
        
        for dir_path in [self.logs_dir, self.graphs_dir, self.traces_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def generate_agent_execution_report(
        self,
        session_id: UUID,
        metrics: Dict[str, Dict[str, int]],
        duration: float,
    ) -> Path:
        """
        Generate agent execution report with graphs.
        
        Args:
            session_id: Workflow session ID
            metrics: Agent metrics (tasks processed, succeeded, failed)
            duration: Total workflow duration in seconds
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_dir = self.output_dir / "html"
        html_dir.mkdir(parents=True, exist_ok=True)
        report_path = html_dir / f"agent_execution_report_{timestamp}.html"
        
        # Generate task distribution graph
        graph_path = self._generate_agent_metrics_graph(metrics, timestamp)
        
        # Create HTML report
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Agent Execution Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2196F3;
            color: white;
            padding: 20px;
            border-radius: 5px;
        }}
        .section {{
            background-color: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #2196F3;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px;
            padding: 15px;
            background-color: #e3f2fd;
            border-radius: 5px;
            min-width: 150px;
        }}
        .metric-label {{
            font-size: 12px;
            color: #666;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }}
        .success {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .failed {{
            color: #f44336;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Agent Execution Report</h1>
        <p>Session ID: {session_id}</p>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="section">
        <h2>📊 Summary Metrics</h2>
        <div class="metric">
            <div class="metric-label">Total Duration</div>
            <div class="metric-value">{duration:.2f}s</div>
        </div>
        <div class="metric">
            <div class="metric-label">Total Agents</div>
            <div class="metric-value">{len(metrics)}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Total Tasks</div>
            <div class="metric-value">{sum(m.get('tasks_processed', 0) for m in metrics.values())}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Success Rate</div>
            <div class="metric-value">{self._calculate_success_rate(metrics):.1f}%</div>
        </div>
    </div>
    
    <div class="section">
        <h2>📈 Agent Performance</h2>
        <table>
            <thead>
                <tr>
                    <th>Agent</th>
                    <th>Tasks Processed</th>
                    <th>Tasks Succeeded</th>
                    <th>Tasks Failed</th>
                    <th>Success Rate</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for agent_type, agent_metrics in metrics.items():
            processed = agent_metrics.get('tasks_processed', 0)
            succeeded = agent_metrics.get('tasks_succeeded', 0)
            failed = agent_metrics.get('tasks_failed', 0)
            success_rate = (succeeded / processed * 100) if processed > 0 else 0
            
            html_content += f"""
                <tr>
                    <td><strong>{agent_type}</strong></td>
                    <td>{processed}</td>
                    <td class="success">{succeeded}</td>
                    <td class="failed">{failed}</td>
                    <td>{success_rate:.1f}%</td>
                </tr>
"""
        
        html_content += f"""
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>📊 Visual Analytics</h2>
        <img src="{graph_path.name}" alt="Agent Metrics Graph">
    </div>
</body>
</html>
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Agent execution report saved: {report_path}")
        return report_path
    
    def generate_test_execution_report(
        self,
        session_id: UUID,
        results: List[TestExecutionResult],
        tests: List[GeneratedTest],
    ) -> Path:
        """
        Generate test execution report with graphs.
        
        Args:
            session_id: Workflow session ID
            results: Test execution results
            tests: Generated tests
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_dir = self.output_dir / "html"
        html_dir.mkdir(parents=True, exist_ok=True)
        report_path = html_dir / f"test_execution_report_{timestamp}.html"
        
        # Generate test results graph
        graph_path = self._generate_test_results_graph(results, timestamp)
        
        # Calculate metrics
        total_tests = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total_tests - passed
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        avg_time = sum(r.execution_time_ms for r in results) / total_tests if total_tests > 0 else 0
        
        # Create HTML report
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Execution Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 5px;
        }}
        .section {{
            background-color: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px;
            padding: 15px;
            background-color: #e8f5e9;
            border-radius: 5px;
            min-width: 150px;
        }}
        .metric-label {{
            font-size: 12px;
            color: #666;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .passed {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .failed {{
            color: #f44336;
            font-weight: bold;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ Test Execution Report</h1>
        <p>Session ID: {session_id}</p>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="section">
        <h2>📊 Summary Metrics</h2>
        <div class="metric">
            <div class="metric-label">Total Tests</div>
            <div class="metric-value">{total_tests}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Passed</div>
            <div class="metric-value" style="color: #4CAF50;">{passed}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Failed</div>
            <div class="metric-value" style="color: #f44336;">{failed}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Pass Rate</div>
            <div class="metric-value">{pass_rate:.1f}%</div>
        </div>
        <div class="metric">
            <div class="metric-label">Avg Time</div>
            <div class="metric-value">{avg_time:.0f}ms</div>
        </div>
    </div>
    
    <div class="section">
        <h2>📋 Test Results Details</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Execution Time</th>
                    <th>Assertions</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Match results with tests
        test_map = {test.id: test for test in tests}
        
        for result in results:
            test = test_map.get(result.test_id)
            test_name = test.test_class_name if test else "Unknown"
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            status_class = "passed" if result.passed else "failed"
            assertions = test.assertion_count if test else 0
            
            html_content += f"""
                <tr>
                    <td><strong>{test_name}</strong></td>
                    <td class="{status_class}">{status}</td>
                    <td>{result.execution_time_ms:.0f}ms</td>
                    <td>{assertions}</td>
                </tr>
"""
        
        html_content += f"""
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>📊 Visual Analytics</h2>
        <img src="{graph_path.name}" alt="Test Results Graph">
    </div>
</body>
</html>
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Test execution report saved: {report_path}")
        return report_path
    
    def generate_oracle_list(
        self,
        session_id: UUID,
        oracles: List[Oracle],
        endpoints: List[EndpointContext] = None,
    ) -> Path:
        """
        Generate list of oracles by name.
        
        Args:
            session_id: Workflow session ID
            oracles: List of generated oracles
            endpoints: List of endpoints (optional, for names)
            
        Returns:
            Path to oracle list file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to oracles directory
        oracles_dir = self.output_dir.parent / "oracles"
        oracles_dir.mkdir(parents=True, exist_ok=True)
        list_path = oracles_dir / f"oracle_list_{timestamp}.txt"
        
        # Create endpoint map for names
        endpoint_map = {}
        if endpoints:
            endpoint_map = {ep.id: ep.name for ep in endpoints}
        
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write(f"Oracle List - Session {session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Oracles: {len(oracles)}\n\n")
            
            for i, oracle in enumerate(oracles, 1):
                endpoint_name = endpoint_map.get(oracle.endpoint_id, "Unknown")
                f.write(f"{i}. {endpoint_name}\n")
                f.write(f"   - Oracle ID: {oracle.id}\n")
                f.write(f"   - Endpoint ID: {oracle.endpoint_id}\n")
                f.write(f"   - Expected Status: {oracle.status_code}\n")
                f.write(f"   - Confidence: {getattr(oracle, 'confidence', 'N/A')}\n")
                f.write(f"   - Assertions: {len(getattr(oracle, 'assertions', []))}\n")
                f.write("\n")
        
        logger.info(f"Oracle list saved: {list_path}")
        return list_path
    
    def generate_execution_trace(
        self,
        session_id: UUID,
        endpoints: List[EndpointContext],
        oracles: List[Oracle],
        tests: List[GeneratedTest],
        results: List[TestExecutionResult],
        duration: float,
    ) -> Path:
        """
        Generate detailed execution trace in JSON format.
        
        Args:
            session_id: Workflow session ID
            endpoints: Extracted endpoints
            oracles: Generated oracles
            tests: Generated tests
            results: Execution results
            duration: Total duration in seconds
            
        Returns:
            Path to trace file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_path = self.traces_dir / f"execution_trace_{timestamp}.json"
        
        trace_data = {
            "session_id": str(session_id),
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration,
            "workflow_phases": [
                {
                    "phase": 1,
                    "name": "Context Extraction",
                    "agent": "Inductor",
                    "endpoints_extracted": len(endpoints),
                    "endpoints": [
                        {
                            "id": str(ep.id),
                            "name": ep.name,
                            "method": ep.method.value,
                            "path": ep.url,
                        }
                        for ep in endpoints
                    ],
                },
                {
                    "phase": 2,
                    "name": "Oracle Generation",
                    "agent": "Oracle",
                    "oracles_generated": len(oracles),
                    "oracles": [
                        {
                            "id": str(oracle.id),
                            "endpoint_id": str(oracle.endpoint_id),
                            "confidence": getattr(oracle, 'confidence', 0.5),
                            "assertions": len(getattr(oracle, 'assertions', [])),
                        }
                        for oracle in oracles
                    ],
                },
                {
                    "phase": 3,
                    "name": "Test Generation",
                    "agent": "Contractor",
                    "tests_generated": len(tests),
                    "tests": [
                        {
                            "id": str(test.id),
                            "class_name": test.test_class_name,
                            "lines": test.line_count,
                            "assertions": test.assertion_count,
                            "has_gherkin": bool(test.feature_file_name),
                        }
                        for test in tests
                    ],
                },
                {
                    "phase": 4,
                    "name": "Test Execution",
                    "agent": "Runner",
                    "tests_executed": len(results),
                    "results": [
                        {
                            "test_id": str(result.test_id),
                            "passed": result.passed,
                            "execution_time_ms": result.execution_time_ms,
                        }
                        for result in results
                    ],
                },
            ],
            "summary": {
                "total_endpoints": len(endpoints),
                "total_oracles": len(oracles),
                "total_tests": len(tests),
                "tests_passed": sum(1 for r in results if r.passed),
                "tests_failed": sum(1 for r in results if not r.passed),
                "pass_rate": (sum(1 for r in results if r.passed) / len(results) * 100) if results else 0,
            },
        }
        
        with open(trace_path, 'w', encoding='utf-8') as f:
            json.dump(trace_data, f, indent=2)
        
        logger.info(f"Execution trace saved: {trace_path}")
        return trace_path
    
    def generate_workflow_log(
        self,
        session_id: UUID,
        log_entries: List[Dict[str, Any]],
    ) -> Path:
        """
        Generate structured workflow log file.
        
        Args:
            session_id: Workflow session ID
            log_entries: Log entries from workflow execution
            
        Returns:
            Path to log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = self.logs_dir / f"workflow_log_{timestamp}.log"
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"Workflow Log - Session {session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for entry in log_entries:
                timestamp = entry.get('timestamp', '')
                level = entry.get('level', 'INFO')
                message = entry.get('message', '')
                
                f.write(f"[{timestamp}] {level}: {message}\n")
        
        logger.info(f"Workflow log saved: {log_path}")
        return log_path
    
    def _generate_agent_metrics_graph(
        self,
        metrics: Dict[str, Dict[str, int]],
        timestamp: str,
    ) -> Path:
        """Generate bar graph for agent metrics."""
        graph_path = self.graphs_dir / f"agent_metrics_{timestamp}.png"
        
        agents = list(metrics.keys())
        processed = [metrics[a].get('tasks_processed', 0) for a in agents]
        succeeded = [metrics[a].get('tasks_succeeded', 0) for a in agents]
        failed = [metrics[a].get('tasks_failed', 0) for a in agents]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(agents))
        width = 0.25
        
        ax.bar([i - width for i in x], processed, width, label='Processed', color='#2196F3')
        ax.bar(x, succeeded, width, label='Succeeded', color='#4CAF50')
        ax.bar([i + width for i in x], failed, width, label='Failed', color='#f44336')
        
        ax.set_xlabel('Agents')
        ax.set_ylabel('Tasks')
        ax.set_title('Agent Task Execution Metrics')
        ax.set_xticks(x)
        ax.set_xticklabels(agents)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(graph_path, dpi=150)
        plt.close()
        
        return graph_path
    
    def _generate_test_results_graph(
        self,
        results: List[TestExecutionResult],
        timestamp: str,
    ) -> Path:
        """Generate pie chart for test results."""
        graph_path = self.graphs_dir / f"test_results_{timestamp}.png"
        
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        colors = ['#4CAF50', '#f44336']
        labels = [f'Passed ({passed})', f'Failed ({failed})']
        sizes = [passed, failed]
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Test Results Distribution')
        
        # Execution time bar chart
        test_names = [f"Test {i+1}" for i in range(len(results))]
        times = [r.execution_time_ms for r in results]
        bar_colors = ['#4CAF50' if r.passed else '#f44336' for r in results]
        
        ax2.bar(test_names, times, color=bar_colors)
        ax2.set_xlabel('Tests')
        ax2.set_ylabel('Execution Time (ms)')
        ax2.set_title('Test Execution Times')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(graph_path, dpi=150)
        plt.close()
        
        return graph_path
    
    def _calculate_success_rate(self, metrics: Dict[str, Dict[str, int]]) -> float:
        """Calculate overall success rate from metrics."""
        total_succeeded = sum(m.get('tasks_succeeded', 0) for m in metrics.values())
        total_processed = sum(m.get('tasks_processed', 0) for m in metrics.values())
        
        return (total_succeeded / total_processed * 100) if total_processed > 0 else 0
