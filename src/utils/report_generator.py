"""
Report generation utilities for contract test generation workflow.
"""
import json
import math
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
    
    def __init__(self, output_dir: Path = Path("output"), execution_id: Optional[str] = None):
        """
        Initialize report generator.
        
        Args:
            output_dir: Base directory for all outputs (e.g., "output")
            execution_id: Unique execution ID (timestamp-based)
        """
        # Generate execution ID if not provided
        if execution_id is None:
            execution_id = datetime.now().strftime("exec_%Y%m%d_%H%M%S")
        
        self.execution_id = execution_id
        
        # Create execution-specific directory under output_dir
        self.execution_dir = output_dir / execution_id
        self.execution_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for this execution
        self.reports_dir = self.execution_dir / "reports"
        self.tests_dir = self.execution_dir / "tests"
        self.logs_dir = self.execution_dir / "logs"
        self.graphs_dir = self.execution_dir / "graphs"
        self.traces_dir = self.execution_dir / "traces"
        self.oracles_dir = self.execution_dir / "oracles"
        self.contexts_dir = self.execution_dir / "contexts"
        
        for dir_path in [self.reports_dir, self.tests_dir, self.logs_dir, 
                         self.graphs_dir, self.traces_dir, self.oracles_dir, self.contexts_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Note: test subdirectories (pom.xml and src/) are created by Runner agent
    
    def generate_agent_execution_report(
        self,
        session_id: UUID,
        metrics: Dict[str, Dict[str, int]],
        duration: float,
        oracles: List = None,
        event_stats: Dict[str, Any] = None,
        llm_models: Dict[str, str] = None,
    ) -> Path:
        """
        Generate agent execution report with graphs.
        
        Args:
            session_id: Workflow session ID
            metrics: Agent metrics (tasks processed, succeeded, failed)
            duration: Total workflow duration in seconds
            oracles: List of generated oracles (optional, for confidence)
            event_stats: Event bus statistics (optional, for agent interactions)
            
        Returns:
            Path to generated report
        """
        report_path = self.reports_dir / "agent_execution_report.html"
        
        # Generate task distribution graph
        graph_path = self._generate_agent_metrics_graph(metrics, self.execution_id)
        
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
        .warning {{
            color: #ff9800;
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
        <h2>🤖 LLM Models</h2>
        <table>
            <thead>
                <tr>
                    <th>Agent</th>
                    <th>LLM Model</th>
                </tr>
            </thead>
            <tbody>
{self._generate_llm_models_rows(llm_models)}
            </tbody>
        </table>
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
        <img src="../graphs/{graph_path.name}" alt="Agent Metrics Graph">
    </div>
"""
        
        # Add oracle confidence section if oracles provided
        if oracles:
            confidences = [getattr(oracle, 'confidence_score', 0.5) for oracle in oracles]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            min_confidence = min(confidences) if confidences else 0
            max_confidence = max(confidences) if confidences else 0
            
            html_content += f"""
    <div class="section">
        <h2>🎯 Oracle Confidence Metrics</h2>
        <div class="metric">
            <div class="metric-label">Average Confidence</div>
            <div class="metric-value">{avg_confidence:.2%}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Min Confidence</div>
            <div class="metric-value">{min_confidence:.2%}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Max Confidence</div>
            <div class="metric-value">{max_confidence:.2%}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Total Oracles</div>
            <div class="metric-value">{len(oracles)}</div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Oracle Name</th>
                    <th>Confidence</th>
                    <th>Quality</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for oracle in oracles:
                confidence = getattr(oracle, 'confidence_score', 0.5)
                oracle_name = getattr(oracle, 'name', 'Unknown')
                
                # Determine quality level
                if confidence >= 0.8:
                    quality = "🟢 High"
                    quality_class = "success"
                elif confidence >= 0.6:
                    quality = "🟡 Medium"
                    quality_class = "warning"
                else:
                    quality = "🔴 Low"
                    quality_class = "failed"
                
                html_content += f"""
                <tr>
                    <td><strong>{oracle_name}</strong></td>
                    <td>{confidence:.2%}</td>
                    <td class="{quality_class}">{quality}</td>
                </tr>
"""
            
            html_content += """
            </tbody>
        </table>
    </div>
"""
        
        # Add agent interactions/events section if event_stats provided
        if event_stats:
            total_events = event_stats.get('total_events', 0)
            unique_types = event_stats.get('unique_event_types', 0)
            event_counts = event_stats.get('event_counts', {})
            
            html_content += f"""
    <div class="section">
        <h2>🔄 Agent Interactions & Workflow Iterations</h2>
        <div class="metric">
            <div class="metric-label">Total Events Published</div>
            <div class="metric-value">{total_events}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Unique Event Types</div>
            <div class="metric-value">{unique_types}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Avg Events per Type</div>
            <div class="metric-value">{total_events / unique_types if unique_types > 0 else 0:.1f}</div>
        </div>
        
        <h3>Event Distribution</h3>
        <table>
            <thead>
                <tr>
                    <th>Event Type</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_events * 100) if total_events > 0 else 0
                html_content += f"""
                <tr>
                    <td><strong>{event_type}</strong></td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
"""
            
            html_content += """
            </tbody>
        </table>
        <p><em>Note: Chaque événement représente une interaction ou un aller-retour entre agents dans le workflow.</em></p>
    </div>
"""
        
        html_content += """
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
        report_path = self.reports_dir / "test_execution_report.html"
        
        # Generate test results graph
        graph_path = self._generate_test_results_graph(results, self.execution_id)
        
        # Calculate metrics
        total_tests = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total_tests - passed
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        avg_time = sum(r.execution_time_ms for r in results) / total_tests if total_tests > 0 else 0
        # Handle NaN values
        if math.isnan(avg_time) or math.isinf(avg_time):
            avg_time = 0
        
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
            
            # Handle NaN values in execution time
            exec_time = result.execution_time_ms
            if math.isnan(exec_time) or math.isinf(exec_time):
                exec_time = 0
            
            html_content += f"""
                <tr>
                    <td><strong>{test_name}</strong></td>
                    <td class="{status_class}">{status}</td>
                    <td>{exec_time:.0f}ms</td>
                    <td>{assertions}</td>
                </tr>
"""
        
        html_content += f"""
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>📊 Visual Analytics</h2>
        <img src="../graphs/{graph_path.name}" alt="Test Results Graph">
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
        list_path = self.oracles_dir / "oracle_list.txt"
        
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
                oracle_name = getattr(oracle, 'name', None) or endpoint_map.get(oracle.endpoint_id, "Unknown")
                f.write(f"{i}. {oracle_name}\n")
                f.write(f"   - Oracle ID: {oracle.id}\n")
                f.write(f"   - Endpoint ID: {oracle.endpoint_id}\n")
                f.write(f"   - Expected Status: {oracle.status_code}\n")
                f.write(f"   - Confidence: {getattr(oracle, 'confidence_score', 'N/A')}\n")
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
        event_stats: Dict[str, Any] = None,
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
            event_stats: Event bus statistics (optional)
            
        Returns:
            Path to trace file
        """
        trace_path = self.traces_dir / "execution_trace.json"
        
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
                            "name": getattr(oracle, 'name', f"Oracle {oracle.id}"),
                            "endpoint_id": str(oracle.endpoint_id),
                            "confidence": getattr(oracle, 'confidence_score', 0.5),
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
        
        # Add agent interactions section if event_stats provided
        if event_stats:
            trace_data["agent_interactions"] = {
                "total_events": event_stats.get('total_events', 0),
                "unique_event_types": event_stats.get('unique_event_types', 0),
                "event_counts": event_stats.get('event_counts', {}),
                "description": "Total number of events/messages exchanged between agents during workflow execution"
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
        log_path = self.logs_dir / "workflow_log.log"
        
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
    
    def _generate_llm_models_rows(self, llm_models: Dict[str, str] = None) -> str:
        """
        Generate HTML rows for LLM models table.
        
        Args:
            llm_models: Dictionary mapping agent types to LLM model names
            
        Returns:
            HTML string with table rows
        """
        if not llm_models:
            return "                <tr><td colspan='2'>No LLM model information available</td></tr>"
        
        rows = []
        for agent_type, model_name in llm_models.items():
            # Extract agent name from AgentType enum or string
            agent_name = str(agent_type).split('.')[-1] if '.' in str(agent_type) else str(agent_type)
            rows.append(f"                <tr><td>{agent_name}</td><td>{model_name}</td></tr>")
        
        return "\n".join(rows)
    
    def _calculate_success_rate(self, metrics: Dict[str, Dict[str, int]]) -> float:
        """Calculate overall success rate from metrics."""
        total_succeeded = sum(m.get('tasks_succeeded', 0) for m in metrics.values())
        total_processed = sum(m.get('tasks_processed', 0) for m in metrics.values())
        
        return (total_succeeded / total_processed * 100) if total_processed > 0 else 0
