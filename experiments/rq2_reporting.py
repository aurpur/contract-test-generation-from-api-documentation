"""
===============================================================================
Reporting and Visualization for RQ2 Consistency Experiments
===============================================================================

OBJECTIF:
    Générer des visualisations et rapports de qualité publication pour RQ2:
    - Graphiques comparatifs des scores de cohérence
    - Analyse des patterns d'incohérence
    - Visualisation des ratios de couverture (Java/Gherkin)
    - Tableaux de significativité statistique
    - Tableaux LaTeX pour articles scientifiques
    - Dashboards HTML interactifs
    - Exports CSV pour analyses complémentaires

USAGE:
    Ce module est appelé après l'exécution des expériences RQ2.
    Les données proviennent des vrais agents (pas de simulation).

Auteur: Aurel IKAMA HONEY
Date: December 11, 2025
===============================================================================
"""
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import statistics

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib/seaborn not available. Install with: pip install matplotlib seaborn")

from experiments.rq2_consistency_validation import ConsistencyExperimentReport
from experiments.rq2_orchestrator import (
    BatchConsistencyResults,
    ConsistencyPatternAnalysis,
    InconsistencyPattern
)


class RQ2ReportGenerator:
    """
    Generate comprehensive reports and visualizations for RQ2 consistency experiments.
    """
    
    def __init__(self, output_dir: Path = Path("experiments/results/rq2/reports")):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set plotting style
        if MATPLOTLIB_AVAILABLE:
            sns.set_style("whitegrid")
            plt.rcParams['figure.figsize'] = (12, 7)
            plt.rcParams['font.size'] = 11
    
    def generate_full_report(
        self,
        results: BatchConsistencyResults,
        report_name: str = "rq2_full_report"
    ) -> Dict[str, Path]:
        """
        Generate complete RQ2 report with all visualizations and tables.
        
        Args:
            results: Batch consistency experiment results
            report_name: Base name for report files
            
        Returns:
            Dictionary mapping file types to output paths
        """
        output_files = {}
        
        print(f"\n{'='*60}")
        print(f"GENERATING RQ2 COMPREHENSIVE REPORT: {report_name}")
        print(f"{'='*60}\n")
        
        # 1. Coherence comparison chart
        if MATPLOTLIB_AVAILABLE:
            coherence_chart = self.create_coherence_comparison_chart(
                results,
                filename=f"{report_name}_coherence_comparison.png"
            )
            output_files["coherence_chart"] = coherence_chart
        
        # 2. Coverage ratio chart (Java/Gherkin)
        if MATPLOTLIB_AVAILABLE:
            coverage_chart = self.create_coverage_ratio_chart(
                results,
                filename=f"{report_name}_coverage_ratios.png"
            )
            output_files["coverage_chart"] = coverage_chart
        
        # 3. Inconsistency distribution chart
        if MATPLOTLIB_AVAILABLE:
            inconsistency_chart = self.create_inconsistency_distribution_chart(
                results,
                filename=f"{report_name}_inconsistency_distribution.png"
            )
            output_files["inconsistency_chart"] = inconsistency_chart
        
        # 4. Pattern analysis chart
        if MATPLOTLIB_AVAILABLE and results.pattern_analysis:
            pattern_chart = self.create_pattern_analysis_chart(
                results.pattern_analysis,
                filename=f"{report_name}_pattern_analysis.png"
            )
            output_files["pattern_chart"] = pattern_chart
        
        # 5. LaTeX table
        latex_path = self.create_latex_table(
            results,
            filename=f"{report_name}_table.tex"
        )
        output_files["latex_table"] = latex_path
        
        # 6. CSV export
        csv_path = self.export_to_csv(
            results,
            filename=f"{report_name}_data.csv"
        )
        output_files["csv_export"] = csv_path
        
        # 7. HTML dashboard
        html_path = self.create_html_dashboard(
            results,
            filename=f"{report_name}_dashboard.html"
        )
        output_files["html_dashboard"] = html_path
        
        # 8. Markdown summary
        md_path = self.create_markdown_summary(
            results,
            filename=f"{report_name}_summary.md"
        )
        output_files["markdown_summary"] = md_path
        
        print(f"\n✓ RQ2 report generation complete!")
        print(f"  Files saved in: {self.output_dir}")
        for file_type, path in output_files.items():
            if path:
                print(f"    - {file_type}: {path.name}")
        
        return output_files
    
    def create_coherence_comparison_chart(
        self,
        results: BatchConsistencyResults,
        filename: str = "coherence_comparison.png"
    ) -> Optional[Path]:
        """
        Create bar chart comparing coherence scores across LLMs.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved chart, or None if matplotlib unavailable
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠ Matplotlib not available, skipping chart")
            return None
        
        # Extract coherence data
        models = []
        coherence_means = []
        coherence_stds = []
        
        for report in results.reports:
            for model, metrics in report.aggregate_metrics.items():
                models.append(model)
                coherence_means.append(metrics["coherence_mean"])
                coherence_stds.append(metrics["coherence_std"])
        
        if not models:
            print("⚠ No data available for coherence chart")
            return None
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_pos = range(len(models))
        bars = ax.bar(x_pos, coherence_means, yerr=coherence_stds,
                     capsize=5, alpha=0.8, color='steelblue')
        
        # Add threshold line
        if results.config:
            ax.axhline(y=results.config.min_coherence_score, 
                      color='red', linestyle='--', linewidth=2,
                      label=f'Threshold ({results.config.min_coherence_score:.2f})')
        
        # Customize
        ax.set_xlabel('LLM Model', fontsize=14, fontweight='bold')
        ax.set_ylabel('Coherence Score', fontsize=14, fontweight='bold')
        ax.set_title('Oracle-Code Coherence Comparison (RQ2)', 
                    fontsize=16, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.set_ylim([0, 1.0])
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, mean, std) in enumerate(zip(bars, coherence_means, coherence_stds)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{mean:.3f}\n±{std:.3f}',
                   ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        # Save
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Coherence comparison chart: {filename}")
        return output_path
    
    def create_coverage_ratio_chart(
        self,
        results: BatchConsistencyResults,
        filename: str = "coverage_ratios.png"
    ) -> Optional[Path]:
        """
        Create grouped bar chart showing Java and Gherkin coverage ratios.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved chart, or None if matplotlib unavailable
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        # Extract coverage data
        models = []
        java_coverage = []
        gherkin_coverage = []
        
        for report in results.reports:
            for model, metrics in report.aggregate_metrics.items():
                models.append(model)
                java_coverage.append(metrics["java_coverage_mean"])
                gherkin_coverage.append(metrics["gherkin_coverage_mean"])
        
        if not models:
            print("⚠ No data available for coverage chart")
            return None
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_pos = range(len(models))
        width = 0.35
        
        bars1 = ax.bar([p - width/2 for p in x_pos], java_coverage,
                       width, label='Java Coverage', alpha=0.8, color='#2ecc71')
        bars2 = ax.bar([p + width/2 for p in x_pos], gherkin_coverage,
                       width, label='Gherkin Coverage', alpha=0.8, color='#3498db')
        
        # Customize
        ax.set_xlabel('LLM Model', fontsize=14, fontweight='bold')
        ax.set_ylabel('Coverage Ratio', fontsize=14, fontweight='bold')
        ax.set_title('Oracle Validation Coverage: Java vs Gherkin (RQ2)',
                    fontsize=16, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.set_ylim([0, 1.0])
        ax.legend(loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1%}',
                       ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        # Save
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Coverage ratio chart: {filename}")
        return output_path
    
    def create_inconsistency_distribution_chart(
        self,
        results: BatchConsistencyResults,
        filename: str = "inconsistency_distribution.png"
    ) -> Optional[Path]:
        """
        Create stacked bar chart showing inconsistency severity distribution.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved chart, or None if matplotlib unavailable
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        # Extract inconsistency data
        models = []
        critical = []
        major = []
        minor = []
        info = []
        
        for report in results.reports:
            for model, metrics in report.aggregate_metrics.items():
                models.append(model)
                critical.append(metrics["critical_avg"])
                major.append(metrics["major_avg"])
                minor.append(metrics["minor_avg"])
                # Info not in metrics, default to 0
                info.append(0)
        
        if not models:
            print("⚠ No data available for inconsistency chart")
            return None
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_pos = range(len(models))
        width = 0.6
        
        # Stacked bars
        p1 = ax.bar(x_pos, critical, width, label='Critical',
                   color='#e74c3c', alpha=0.9)
        p2 = ax.bar(x_pos, major, width, bottom=critical,
                   label='Major', color='#f39c12', alpha=0.9)
        
        bottom_minor = [c + m for c, m in zip(critical, major)]
        p3 = ax.bar(x_pos, minor, width, bottom=bottom_minor,
                   label='Minor', color='#f1c40f', alpha=0.9)
        
        # Customize
        ax.set_xlabel('LLM Model', fontsize=14, fontweight='bold')
        ax.set_ylabel('Average Inconsistencies per Endpoint', fontsize=14, fontweight='bold')
        ax.set_title('Inconsistency Distribution by Severity (RQ2)',
                    fontsize=16, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.legend(loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Inconsistency distribution chart: {filename}")
        return output_path
    
    def create_pattern_analysis_chart(
        self,
        pattern_analysis: ConsistencyPatternAnalysis,
        filename: str = "pattern_analysis.png"
    ) -> Optional[Path]:
        """
        Create horizontal bar chart showing top inconsistency patterns.
        
        Args:
            pattern_analysis: Pattern analysis results
            filename: Output filename
            
        Returns:
            Path to saved chart, or None if matplotlib unavailable
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        if not pattern_analysis.common_patterns:
            print("⚠ No patterns available for chart")
            return None
        
        # Get top 10 patterns
        top_patterns = pattern_analysis.common_patterns[:10]
        
        # Extract data
        pattern_names = [p.pattern_type.replace("_", " ").title() for p in top_patterns]
        occurrence_rates = [p.occurrence_rate * 100 for p in top_patterns]  # Convert to %
        colors = [self._severity_color(p.severity) for p in top_patterns]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        y_pos = range(len(pattern_names))
        bars = ax.barh(y_pos, occurrence_rates, color=colors, alpha=0.8)
        
        # Customize
        ax.set_yticks(y_pos)
        ax.set_yticklabels(pattern_names)
        ax.set_xlabel('Occurrence Rate (%)', fontsize=14, fontweight='bold')
        ax.set_title('Top 10 Inconsistency Patterns (RQ2)',
                    fontsize=16, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, rate) in enumerate(zip(bars, occurrence_rates)):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{rate:.1f}%',
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        # Save
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Pattern analysis chart: {filename}")
        return output_path
    
    def _severity_color(self, severity) -> str:
        """Get color for severity level."""
        color_map = {
            "critical": "#e74c3c",
            "major": "#f39c12",
            "minor": "#f1c40f",
            "info": "#3498db"
        }
        return color_map.get(severity.value, "#95a5a6")
    
    def create_latex_table(
        self,
        results: BatchConsistencyResults,
        filename: str = "rq2_table.tex"
    ) -> Path:
        """
        Create LaTeX table for academic paper.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved LaTeX file
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write("% RQ2 Consistency Validation Results\n")
            f.write("% Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{Oracle-Code Consistency Validation Results (RQ2)}\n")
            f.write("\\label{tab:rq2_consistency}\n")
            f.write("\\begin{tabular}{lcccccc}\n")
            f.write("\\toprule\n")
            f.write("\\textbf{LLM} & \\textbf{Coherence} & \\textbf{Java Cov.} & ")
            f.write("\\textbf{Gherkin Cov.} & \\textbf{Critical} & \\textbf{Major} & \\textbf{Pass Rate} \\\\\n")
            f.write("\\midrule\n")
            
            # Aggregate across reports for each model
            model_data = {}
            for report in results.reports:
                for model, metrics in report.aggregate_metrics.items():
                    if model not in model_data:
                        model_data[model] = []
                    model_data[model].append(metrics)
            
            # Write rows
            for model in sorted(model_data.keys()):
                metrics_list = model_data[model]
                
                # Average across replications
                coherence = statistics.mean(m["coherence_mean"] for m in metrics_list)
                java_cov = statistics.mean(m["java_coverage_mean"] for m in metrics_list)
                gherkin_cov = statistics.mean(m["gherkin_coverage_mean"] for m in metrics_list)
                critical = statistics.mean(m["critical_avg"] for m in metrics_list)
                major = statistics.mean(m["major_avg"] for m in metrics_list)
                pass_rate = statistics.mean(m["pass_rate"] for m in metrics_list)
                
                f.write(f"{model} & ")
                f.write(f"{coherence:.3f} & ")
                f.write(f"{java_cov:.2f} & ")
                f.write(f"{gherkin_cov:.2f} & ")
                f.write(f"{critical:.1f} & ")
                f.write(f"{major:.1f} & ")
                f.write(f"{pass_rate:.2f} \\\\\n")
            
            f.write("\\bottomrule\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n")
        
        print(f"  ✓ LaTeX table: {filename}")
        return output_path
    
    def export_to_csv(
        self,
        results: BatchConsistencyResults,
        filename: str = "rq2_data.csv"
    ) -> Path:
        """
        Export results to CSV for external analysis.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved CSV file
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            # Header
            f.write("experiment_id,model,endpoint_id,endpoint_name,")
            f.write("coherence_score,java_coverage,gherkin_coverage,")
            f.write("critical_count,major_count,minor_count,")
            f.write("missing_validations,extra_validations,incorrect_implementations,")
            f.write("passes_threshold,has_critical_issues,has_major_issues\n")
            
            # Data rows
            for report in results.reports:
                exp_id = report.experiment_id
                
                for endpoint_result in report.endpoint_results:
                    f.write(f"{exp_id},")
                    f.write(f"{endpoint_result.llm_model},")
                    f.write(f"{endpoint_result.endpoint_id},")
                    f.write(f'"{endpoint_result.endpoint_name}",')
                    f.write(f"{endpoint_result.coherence_score},")
                    f.write(f"{endpoint_result.java_coverage_ratio},")
                    f.write(f"{endpoint_result.gherkin_coverage_ratio},")
                    f.write(f"{endpoint_result.critical_count},")
                    f.write(f"{endpoint_result.major_count},")
                    f.write(f"{endpoint_result.minor_count},")
                    f.write(f"{endpoint_result.missing_validations},")
                    f.write(f"{endpoint_result.extra_validations},")
                    f.write(f"{endpoint_result.incorrect_implementations},")
                    f.write(f"{endpoint_result.passes_threshold},")
                    f.write(f"{endpoint_result.has_critical_issues},")
                    f.write(f"{endpoint_result.has_major_issues}\n")
        
        print(f"  ✓ CSV export: {filename}")
        return output_path
    
    def create_html_dashboard(
        self,
        results: BatchConsistencyResults,
        filename: str = "rq2_dashboard.html"
    ) -> Path:
        """
        Create interactive HTML dashboard.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved HTML file
        """
        output_path = self.output_dir / filename
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RQ2 Consistency Validation Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-card h3 {{
            margin-top: 0;
            color: #3498db;
            font-size: 14px;
            text-transform: uppercase;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .status-pass {{
            color: #27ae60;
            font-weight: bold;
        }}
        .status-fail {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .severity-critical {{
            background-color: #e74c3c;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}
        .severity-major {{
            background-color: #f39c12;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}
        .severity-minor {{
            background-color: #f1c40f;
            color: #2c3e50;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <h1>🔍 RQ2 Consistency Validation Dashboard</h1>
    <p><strong>Experiment:</strong> {results.experiment_name}</p>
    <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
"""
        
        # Add summary metrics
        html_content += self._generate_html_summary_metrics(results)
        
        # Add model comparison table
        html_content += self._generate_html_model_table(results)
        
        # Add pattern analysis if available
        if results.pattern_analysis:
            html_content += self._generate_html_pattern_analysis(results.pattern_analysis)
        
        html_content += """
</body>
</html>
"""
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"  ✓ HTML dashboard: {filename}")
        return output_path
    
    def _generate_html_summary_metrics(self, results: BatchConsistencyResults) -> str:
        """Generate HTML for summary metrics."""
        total_endpoints = results.config.num_endpoints * len(results.reports)
        total_models = len(results.config.llm_models)
        
        html = """
    <h2>📊 Summary Metrics</h2>
    <div class="metric-grid">
        <div class="metric-card">
            <h3>Total Experiments</h3>
            <div class="metric-value">{}</div>
            <div class="metric-label">Completed</div>
        </div>
        <div class="metric-card">
            <h3>Total Endpoints</h3>
            <div class="metric-value">{}</div>
            <div class="metric-label">Validated</div>
        </div>
        <div class="metric-card">
            <h3>LLM Models</h3>
            <div class="metric-value">{}</div>
            <div class="metric-label">Compared</div>
        </div>
        <div class="metric-card">
            <h3>Replications</h3>
            <div class="metric-value">{}</div>
            <div class="metric-label">Per Configuration</div>
        </div>
    </div>
""".format(
            len(results.reports),
            total_endpoints,
            total_models,
            results.config.num_replications
        )
        
        return html
    
    def _generate_html_model_table(self, results: BatchConsistencyResults) -> str:
        """Generate HTML table for model comparison."""
        html = """
    <h2>🤖 LLM Model Comparison</h2>
    <table>
        <thead>
            <tr>
                <th>Model</th>
                <th>Coherence Score</th>
                <th>Java Coverage</th>
                <th>Gherkin Coverage</th>
                <th>Critical Issues</th>
                <th>Major Issues</th>
                <th>Pass Rate</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Aggregate data by model
        for report in results.reports:
            for model, metrics in report.aggregate_metrics.items():
                pass_status = "status-pass" if metrics["pass_rate"] >= 0.8 else "status-fail"
                
                html += f"""
            <tr>
                <td><strong>{model}</strong></td>
                <td>{metrics['coherence_mean']:.3f} ± {metrics['coherence_std']:.3f}</td>
                <td>{metrics['java_coverage_mean']:.1%}</td>
                <td>{metrics['gherkin_coverage_mean']:.1%}</td>
                <td><span class="severity-critical">{metrics['critical_avg']:.1f}</span></td>
                <td><span class="severity-major">{metrics['major_avg']:.1f}</span></td>
                <td class="{pass_status}">{metrics['pass_rate']:.1%}</td>
            </tr>
"""
        
        html += """
        </tbody>
    </table>
"""
        return html
    
    def _generate_html_pattern_analysis(self, pattern_analysis: ConsistencyPatternAnalysis) -> str:
        """Generate HTML for pattern analysis."""
        html = """
    <h2>🔍 Inconsistency Pattern Analysis</h2>
    <table>
        <thead>
            <tr>
                <th>Pattern</th>
                <th>Category</th>
                <th>Severity</th>
                <th>Occurrences</th>
                <th>Occurrence Rate</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for pattern in pattern_analysis.common_patterns[:10]:
            severity_class = f"severity-{pattern.severity.value}"
            pattern_name = pattern.pattern_type.replace("_", " ").title()
            
            html += f"""
            <tr>
                <td><strong>{pattern_name}</strong></td>
                <td>{pattern.category}</td>
                <td><span class="{severity_class}">{pattern.severity.value.upper()}</span></td>
                <td>{pattern.occurrence_count}</td>
                <td>{pattern.occurrence_rate:.1%}</td>
            </tr>
"""
        
        html += """
        </tbody>
    </table>
"""
        return html
    
    def create_markdown_summary(
        self,
        results: BatchConsistencyResults,
        filename: str = "rq2_summary.md"
    ) -> Path:
        """
        Create markdown summary report.
        
        Args:
            results: Batch consistency results
            filename: Output filename
            
        Returns:
            Path to saved markdown file
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write(f"# RQ2 Consistency Validation Summary\n\n")
            f.write(f"**Experiment:** {results.experiment_name}\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Overview\n\n")
            f.write(f"- **Total Experiments:** {len(results.reports)}\n")
            f.write(f"- **LLM Models:** {', '.join(results.config.llm_models)}\n")
            f.write(f"- **Test Suites:** {len(results.config.test_suites)}\n")
            f.write(f"- **Replications:** {results.config.num_replications}\n\n")
            
            f.write("## Model Comparison\n\n")
            f.write("| Model | Coherence | Java Cov. | Gherkin Cov. | Critical | Major | Pass Rate |\n")
            f.write("|-------|-----------|-----------|--------------|----------|-------|----------|\n")
            
            for report in results.reports:
                for model, metrics in report.aggregate_metrics.items():
                    f.write(f"| {model} | ")
                    f.write(f"{metrics['coherence_mean']:.3f} ± {metrics['coherence_std']:.3f} | ")
                    f.write(f"{metrics['java_coverage_mean']:.1%} | ")
                    f.write(f"{metrics['gherkin_coverage_mean']:.1%} | ")
                    f.write(f"{metrics['critical_avg']:.1f} | ")
                    f.write(f"{metrics['major_avg']:.1f} | ")
                    f.write(f"{metrics['pass_rate']:.1%} |\n")
            
            if results.pattern_analysis:
                f.write("\n## Top Inconsistency Patterns\n\n")
                for i, pattern in enumerate(results.pattern_analysis.common_patterns[:5], 1):
                    f.write(f"{i}. **{pattern.pattern_type.replace('_', ' ').title()}**\n")
                    f.write(f"   - Severity: {pattern.severity.value.upper()}\n")
                    f.write(f"   - Occurrences: {pattern.occurrence_count} ({pattern.occurrence_rate:.1%})\n")
                    f.write(f"   - Category: {pattern.category}\n\n")
        
        print(f"  ✓ Markdown summary: {filename}")
        return output_path


if __name__ == "__main__":
    print("RQ2 Report Generator")
    print("Use this module to generate reports from RQ2 consistency experiments")
