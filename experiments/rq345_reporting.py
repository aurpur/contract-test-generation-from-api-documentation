"""
===============================================================================
RQ345 Integrated Reporting - Comprehensive Visualization and Analysis
===============================================================================

OBJECTIF:
    Reporting complet et visualisations pour les Questions de Recherche 3, 4 et 5.
    Génère des outputs prêts pour publication incluant:
    - Tableaux statistiques (LaTeX, CSV, Markdown)
    - Graphiques comparatifs (qualité, performance)
    - Heatmaps de corrélation
    - Dashboards interactifs (HTML)
    - Résumés exécutifs

FONCTIONNEMENT:
    Ce module intègre les résultats des trois RQ et produit des visualisations
    multi-dimensionnelles adaptées aux publications académiques.
    
    IMPORTANT: Utilise uniquement des modèles Ollama locaux.
    Pas de métriques de coût cloud (remplacees par efficacité temps/qualité).

Auteur: Aurel IKAMA HONEY
Date: December 11, 2025
===============================================================================
"""
import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from experiments.rq345_orchestrator import RQ345BatchReport, RQ345Results, CrossRQAnalysis


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    # Output formats
    generate_latex: bool = True
    generate_csv: bool = True
    generate_markdown: bool = True
    generate_html: bool = True
    generate_charts: bool = True
    
    # Chart configuration
    chart_format: str = "png"  # png, pdf, svg
    chart_dpi: int = 300
    chart_style: str = "seaborn-v0_8-darkgrid"
    
    # Output directory
    output_dir: Path = Path("experiments/reports/rq345")
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "output_formats": {
                "latex": self.generate_latex,
                "csv": self.generate_csv,
                "markdown": self.generate_markdown,
                "html": self.generate_html,
                "charts": self.generate_charts
            },
            "chart_config": {
                "format": self.chart_format,
                "dpi": self.chart_dpi,
                "style": self.chart_style
            },
            "output_dir": str(self.output_dir)
        }


class RQ345ReportGenerator:
    """Comprehensive report generator for RQ3/4/5 experiments."""
    
    def __init__(self, config: ReportConfig):
        """Initialize report generator."""
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set matplotlib style if available
        if MATPLOTLIB_AVAILABLE:
            try:
                plt.style.use(self.config.chart_style)
            except Exception:
                pass  # Fall back to default style
    
    def generate_full_report(self, batch_report: RQ345BatchReport) -> Dict[str, Path]:
        """
        Generate complete report with all formats and visualizations.
        
        Returns:
            Dictionary mapping output type to file path
        """
        output_files = {}
        
        # Generate text-based reports
        if self.config.generate_latex:
            output_files["latex"] = self._generate_latex_report(batch_report)
        
        if self.config.generate_csv:
            csv_files = self._generate_csv_reports(batch_report)
            output_files.update(csv_files)
        
        if self.config.generate_markdown:
            output_files["markdown"] = self._generate_markdown_report(batch_report)
        
        if self.config.generate_html:
            output_files["html"] = self._generate_html_dashboard(batch_report)
        
        # Generate visualizations
        if self.config.generate_charts and MATPLOTLIB_AVAILABLE:
            chart_files = self._generate_all_charts(batch_report)
            output_files.update(chart_files)
        
        return output_files
    
    def _generate_latex_report(self, report: RQ345BatchReport) -> Path:
        """Generate LaTeX report with tables."""
        output_path = self.config.output_dir / f"rq345_report_{report.experiment_id}.tex"
        
        latex_content = self._build_latex_content(report)
        
        with open(output_path, 'w') as f:
            f.write(latex_content)
        
        return output_path
    
    def _build_latex_content(self, report: RQ345BatchReport) -> str:
        """Build LaTeX document content."""
        lines = [
            "\\documentclass{article}",
            "\\usepackage{booktabs}",
            "\\usepackage{graphicx}",
            "\\usepackage{longtable}",
            "\\usepackage{float}",
            "\\begin{document}",
            "",
            f"\\section{{RQ3/4/5 Experimental Results}}",
            f"\\subsection{{Experiment: {report.config.name}}}",
            f"Experiment ID: \\texttt{{{report.experiment_id}}}\\\\",
            f"Started: {report.started_at.strftime('%Y-%m-%d %H:%M:%S')}\\\\",
            f"Completed: {report.completed_at.strftime('%Y-%m-%d %H:%M:%S') if report.completed_at else 'N/A'}\\\\",
            f"Duration: {report.total_execution_time_seconds:.2f}s\\\\",
            f"Endpoints: {report.total_endpoints_analyzed}\\\\",
            f"Tests Generated: {report.total_tests_generated}\\\\",
            ""
        ]
        
        # RQ3 Table - Code Quality
        if report.results.rq3_report:
            lines.extend(self._latex_rq3_table(report))
        
        # RQ4 Table - LLM Comparison
        if report.results.rq4_report:
            lines.extend(self._latex_rq4_table(report))
        
        # RQ5 Table - Completeness Impact
        if report.results.rq5_report:
            lines.extend(self._latex_rq5_table(report))
        
        # Overall Rankings Table
        lines.extend(self._latex_overall_rankings_table(report))
        
        lines.extend([
            "",
            "\\end{document}"
        ])
        
        return "\n".join(lines)
    
    def _latex_rq3_table(self, report: RQ345BatchReport) -> List[str]:
        """Generate LaTeX table for RQ3 results."""
        rq3 = report.results.rq3_report
        lines = [
            "\\subsection{RQ3: Code Quality Assessment}",
            "\\begin{table}[H]",
            "\\centering",
            "\\caption{Code Quality Metrics by LLM Model}",
            "\\begin{tabular}{lrrrr}",
            "\\toprule",
            "Model & Correctness & Readability & Maintainability & Overall \\\\",
            "\\midrule"
        ]
        
        for model, metrics in rq3.aggregate_metrics.items():
            correctness = metrics.get("mean_correctness_score", 0.0)
            readability = metrics.get("mean_readability_score", 0.0)
            maintainability = metrics.get("mean_maintainability_score", 0.0)
            overall = metrics.get("mean_overall_quality", 0.0)
            
            lines.append(
                f"{model} & {correctness:.3f} & {readability:.3f} & "
                f"{maintainability:.3f} & {overall:.3f} \\\\"
            )
        
        lines.extend([
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            ""
        ])
        
        return lines
    
    def _latex_rq4_table(self, report: RQ345BatchReport) -> List[str]:
        """Generate LaTeX table for RQ4 results."""
        rq4 = report.results.rq4_report
        lines = [
            "\\subsection{RQ4: LLM Comparison}",
            "\\begin{table}[H]",
            "\\centering",
            "\\caption{Multi-Dimensional LLM Comparison}",
            "\\begin{tabular}{lrrrrr}",
            "\\toprule",
            "Model & Oracle F1 & Code Quality & Consistency & Cost (USD) & Overall \\\\",
            "\\midrule"
        ]
        
        for result in rq4.model_results:
            lines.append(
                f"{result.llm_model} & {result.oracle_f1:.3f} & "
                f"{result.code_overall_quality:.3f} & {result.coherence_score:.3f} & "
                f"{result.total_cost_usd:.2f} & {result.overall_score:.3f} \\\\"
            )
        
        lines.extend([
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            ""
        ])
        
        return lines
    
    def _latex_rq5_table(self, report: RQ345BatchReport) -> List[str]:
        """Generate LaTeX table for RQ5 results."""
        rq5 = report.results.rq5_report
        lines = [
            "\\subsection{RQ5: Completeness Impact}",
            "\\begin{table}[H]",
            "\\centering",
            "\\caption{Impact of Documentation Completeness}",
            "\\begin{tabular}{lrrrr}",
            "\\toprule",
            "Model & Correlation & Degradation Rate & Min Completeness & Robustness \\\\",
            "\\midrule"
        ]
        
        for result in rq5.model_results:
            lines.append(
                f"{result.llm_model} & {result.completeness_quality_correlation:.3f} & "
                f"{result.quality_degradation_rate:.3f} & "
                f"{result.min_completeness_for_quality_80:.2f} & "
                f"{result.robustness_score:.3f} \\\\"
            )
        
        lines.extend([
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            ""
        ])
        
        return lines
    
    def _latex_overall_rankings_table(self, report: RQ345BatchReport) -> List[str]:
        """Generate LaTeX table for overall rankings."""
        lines = [
            "\\subsection{Overall Model Rankings}",
            "\\begin{table}[H]",
            "\\centering",
            "\\caption{Overall Model Rankings Across All Dimensions}",
            "\\begin{tabular}{lr}",
            "\\toprule",
            "Model & Rank \\\\",
            "\\midrule"
        ]
        
        sorted_rankings = sorted(report.overall_model_rankings.items(), key=lambda x: x[1])
        for model, rank in sorted_rankings:
            symbol = "\\textbf{*}" if model == report.best_overall_model else ""
            lines.append(f"{model}{symbol} & {rank} \\\\")
        
        lines.extend([
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            ""
        ])
        
        return lines
    
    def _generate_csv_reports(self, report: RQ345BatchReport) -> Dict[str, Path]:
        """Generate CSV reports for each RQ."""
        csv_files = {}
        
        # RQ3 CSV
        if report.results.rq3_report:
            path = self._generate_rq3_csv(report)
            csv_files["rq3_csv"] = path
        
        # RQ4 CSV
        if report.results.rq4_report:
            path = self._generate_rq4_csv(report)
            csv_files["rq4_csv"] = path
        
        # RQ5 CSV
        if report.results.rq5_report:
            path = self._generate_rq5_csv(report)
            csv_files["rq5_csv"] = path
        
        # Overall rankings CSV
        path = self._generate_rankings_csv(report)
        csv_files["rankings_csv"] = path
        
        return csv_files
    
    def _generate_rq3_csv(self, report: RQ345BatchReport) -> Path:
        """Generate CSV for RQ3 results."""
        output_path = self.config.output_dir / f"rq3_quality_{report.experiment_id}.csv"
        
        with open(output_path, 'w') as f:
            f.write("Model,Correctness,Readability,Maintainability,Overall Quality\n")
            
            for model, metrics in report.results.rq3_report.aggregate_metrics.items():
                f.write(
                    f"{model},"
                    f"{metrics.get('mean_correctness_score', 0.0)},"
                    f"{metrics.get('mean_readability_score', 0.0)},"
                    f"{metrics.get('mean_maintainability_score', 0.0)},"
                    f"{metrics.get('mean_overall_quality', 0.0)}\n"
                )
        
        return output_path
    
    def _generate_rq4_csv(self, report: RQ345BatchReport) -> Path:
        """Generate CSV for RQ4 results."""
        output_path = self.config.output_dir / f"rq4_comparison_{report.experiment_id}.csv"
        
        with open(output_path, 'w') as f:
            f.write("Model,Oracle Precision,Oracle Recall,Oracle F1,"
                   "Code Correctness,Code Readability,Code Maintainability,Code Overall,"
                   "Coherence Score,Avg Time (ms),Total Cost (USD),Overall Score\n")
            
            for result in report.results.rq4_report.model_results:
                f.write(
                    f"{result.llm_model},"
                    f"{result.oracle_precision},"
                    f"{result.oracle_recall},"
                    f"{result.oracle_f1},"
                    f"{result.code_correctness},"
                    f"{result.code_readability},"
                    f"{result.code_maintainability},"
                    f"{result.code_overall_quality},"
                    f"{result.coherence_score},"
                    f"{result.avg_generation_time_ms},"
                    f"{result.total_cost_usd},"
                    f"{result.overall_score}\n"
                )
        
        return output_path
    
    def _generate_rq5_csv(self, report: RQ345BatchReport) -> Path:
        """Generate CSV for RQ5 results."""
        output_path = self.config.output_dir / f"rq5_completeness_{report.experiment_id}.csv"
        
        with open(output_path, 'w') as f:
            f.write("Model,Completeness-Quality Correlation,Degradation Rate,"
                   "Min Completeness for 80% Quality,Robustness Score\n")
            
            for result in report.results.rq5_report.model_results:
                f.write(
                    f"{result.llm_model},"
                    f"{result.completeness_quality_correlation},"
                    f"{result.quality_degradation_rate},"
                    f"{result.min_completeness_for_quality_80},"
                    f"{result.robustness_score}\n"
                )
        
        return output_path
    
    def _generate_rankings_csv(self, report: RQ345BatchReport) -> Path:
        """Generate CSV for overall rankings."""
        output_path = self.config.output_dir / f"rankings_{report.experiment_id}.csv"
        
        with open(output_path, 'w') as f:
            f.write("Model,Overall Rank\n")
            
            sorted_rankings = sorted(report.overall_model_rankings.items(), key=lambda x: x[1])
            for model, rank in sorted_rankings:
                f.write(f"{model},{rank}\n")
        
        return output_path
    
    def _generate_markdown_report(self, report: RQ345BatchReport) -> Path:
        """Generate Markdown executive summary."""
        output_path = self.config.output_dir / f"SUMMARY_{report.experiment_id}.md"
        
        md_content = self._build_markdown_content(report)
        
        with open(output_path, 'w') as f:
            f.write(md_content)
        
        return output_path
    
    def _build_markdown_content(self, report: RQ345BatchReport) -> str:
        """Build Markdown document content."""
        lines = [
            f"# RQ3/4/5 Experimental Results Summary",
            "",
            f"**Experiment**: {report.config.name}",
            f"**ID**: `{report.experiment_id}`",
            f"**Date**: {report.started_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Duration**: {report.total_execution_time_seconds:.2f}s",
            "",
            "## Overview",
            "",
            f"- **Endpoints Analyzed**: {report.total_endpoints_analyzed}",
            f"- **Tests Generated**: {report.total_tests_generated}",
            f"- **Models Evaluated**: {', '.join(report.config.llm_models)}",
            f"- **Best Overall Model**: **{report.best_overall_model}**",
            ""
        ]
        
        # RQ3 Summary
        if report.results.rq3_report:
            lines.extend(self._markdown_rq3_summary(report))
        
        # RQ4 Summary
        if report.results.rq4_report:
            lines.extend(self._markdown_rq4_summary(report))
        
        # RQ5 Summary
        if report.results.rq5_report:
            lines.extend(self._markdown_rq5_summary(report))
        
        # Cross-RQ Insights
        if report.cross_rq_analysis:
            lines.extend(self._markdown_cross_rq_insights(report))
        
        # Recommendations
        lines.extend(self._markdown_recommendations(report))
        
        return "\n".join(lines)
    
    def _markdown_rq3_summary(self, report: RQ345BatchReport) -> List[str]:
        """Generate Markdown summary for RQ3."""
        rq3 = report.results.rq3_report
        lines = [
            "## RQ3: Code Quality Assessment",
            "",
            "| Model | Correctness | Readability | Maintainability | Overall |",
            "|-------|-------------|-------------|-----------------|---------|"
        ]
        
        for model, metrics in rq3.aggregate_metrics.items():
            lines.append(
                f"| {model} | "
                f"{metrics.get('mean_correctness_score', 0.0):.3f} | "
                f"{metrics.get('mean_readability_score', 0.0):.3f} | "
                f"{metrics.get('mean_maintainability_score', 0.0):.3f} | "
                f"{metrics.get('mean_overall_quality', 0.0):.3f} |"
            )
        
        lines.append("")
        return lines
    
    def _markdown_rq4_summary(self, report: RQ345BatchReport) -> List[str]:
        """Generate Markdown summary for RQ4."""
        rq4 = report.results.rq4_report
        lines = [
            "## RQ4: LLM Comparison",
            "",
            "| Model | Oracle F1 | Code Quality | Cost (USD) | Overall Score |",
            "|-------|-----------|--------------|------------|---------------|"
        ]
        
        for result in rq4.model_results:
            lines.append(
                f"| {result.llm_model} | "
                f"{result.oracle_f1:.3f} | "
                f"{result.code_overall_quality:.3f} | "
                f"${result.total_cost_usd:.2f} | "
                f"{result.overall_score:.3f} |"
            )
        
        lines.extend([
            "",
            f"**Best for Oracle Quality**: {rq4.best_for_oracle_quality}",
            f"**Best for Code Quality**: {rq4.best_for_code_quality}",
            f"**Most Cost-Effective**: {rq4.best_for_cost}",
            ""
        ])
        
        return lines
    
    def _markdown_rq5_summary(self, report: RQ345BatchReport) -> List[str]:
        """Generate Markdown summary for RQ5."""
        rq5 = report.results.rq5_report
        lines = [
            "## RQ5: Completeness Impact",
            "",
            "| Model | Correlation | Degradation Rate | Min Completeness | Robustness |",
            "|-------|-------------|------------------|------------------|------------|"
        ]
        
        for result in rq5.model_results:
            lines.append(
                f"| {result.llm_model} | "
                f"{result.completeness_quality_correlation:.3f} | "
                f"{result.quality_degradation_rate:.3f} | "
                f"{result.min_completeness_for_quality_80:.2f} | "
                f"{result.robustness_score:.3f} |"
            )
        
        lines.extend([
            "",
            f"**Most Robust Model**: {rq5.most_robust_model}",
            f"**Recommended Min Completeness**: {rq5.recommended_min_completeness*100:.0f}%",
            ""
        ])
        
        return lines
    
    def _markdown_cross_rq_insights(self, report: RQ345BatchReport) -> List[str]:
        """Generate Markdown cross-RQ insights."""
        analysis = report.cross_rq_analysis
        lines = [
            "## Cross-RQ Insights",
            "",
            f"**Quality Leaders**: {', '.join(analysis.quality_leaders)}",
            f"**Cost-Effective Models**: {', '.join(analysis.cost_effective_models)}",
            f"**Robust Performers**: {', '.join(analysis.robust_performers)}",
            "",
            "### Key Findings:",
            ""
        ]
        
        for finding in analysis.key_findings:
            lines.append(f"- {finding}")
        
        lines.append("")
        return lines
    
    def _markdown_recommendations(self, report: RQ345BatchReport) -> List[str]:
        """Generate Markdown recommendations."""
        lines = [
            "## Recommendations",
            ""
        ]
        
        for category, recommendations in report.recommendations.items():
            if recommendations:
                lines.append(f"### {category.replace('_', ' ').title()}")
                lines.append("")
                for rec in recommendations:
                    lines.append(f"- {rec}")
                lines.append("")
        
        return lines
    
    def _generate_html_dashboard(self, report: RQ345BatchReport) -> Path:
        """Generate interactive HTML dashboard."""
        output_path = self.config.output_dir / f"dashboard_{report.experiment_id}.html"
        
        html_content = self._build_html_content(report)
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
    
    def _build_html_content(self, report: RQ345BatchReport) -> str:
        """Build HTML dashboard content."""
        # Simple HTML dashboard (can be enhanced with JavaScript charting libraries)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>RQ3/4/5 Dashboard - {report.experiment_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; 
                  border: 1px solid #ddd; border-radius: 5px; }}
        .best {{ background-color: #d4edda; }}
    </style>
</head>
<body>
    <h1>RQ3/4/5 Experimental Results Dashboard</h1>
    <p><strong>Experiment:</strong> {report.config.name}</p>
    <p><strong>ID:</strong> {report.experiment_id}</p>
    <p><strong>Date:</strong> {report.started_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>Overview</h2>
    <div class="metric">Endpoints: {report.total_endpoints_analyzed}</div>
    <div class="metric">Tests: {report.total_tests_generated}</div>
    <div class="metric">Duration: {report.total_execution_time_seconds:.2f}s</div>
    <div class="metric best">Best Model: {report.best_overall_model}</div>
"""
        
        # Add RQ3 table
        if report.results.rq3_report:
            html += self._html_rq3_table(report)
        
        # Add RQ4 table
        if report.results.rq4_report:
            html += self._html_rq4_table(report)
        
        # Add RQ5 table
        if report.results.rq5_report:
            html += self._html_rq5_table(report)
        
        html += """
</body>
</html>
"""
        return html
    
    def _html_rq3_table(self, report: RQ345BatchReport) -> str:
        """Generate HTML table for RQ3."""
        html = """
    <h2>RQ3: Code Quality</h2>
    <table>
        <tr>
            <th>Model</th>
            <th>Correctness</th>
            <th>Readability</th>
            <th>Maintainability</th>
            <th>Overall</th>
        </tr>
"""
        for model, metrics in report.results.rq3_report.aggregate_metrics.items():
            html += f"""
        <tr>
            <td>{model}</td>
            <td>{metrics.get('mean_correctness_score', 0.0):.3f}</td>
            <td>{metrics.get('mean_readability_score', 0.0):.3f}</td>
            <td>{metrics.get('mean_maintainability_score', 0.0):.3f}</td>
            <td>{metrics.get('mean_overall_quality', 0.0):.3f}</td>
        </tr>
"""
        html += "    </table>\n"
        return html
    
    def _html_rq4_table(self, report: RQ345BatchReport) -> str:
        """Generate HTML table for RQ4."""
        html = """
    <h2>RQ4: LLM Comparison</h2>
    <table>
        <tr>
            <th>Model</th>
            <th>Oracle F1</th>
            <th>Code Quality</th>
            <th>Cost (USD)</th>
            <th>Overall</th>
        </tr>
"""
        for result in report.results.rq4_report.model_results:
            html += f"""
        <tr>
            <td>{result.llm_model}</td>
            <td>{result.oracle_f1:.3f}</td>
            <td>{result.code_overall_quality:.3f}</td>
            <td>${result.total_cost_usd:.2f}</td>
            <td>{result.overall_score:.3f}</td>
        </tr>
"""
        html += "    </table>\n"
        return html
    
    def _html_rq5_table(self, report: RQ345BatchReport) -> str:
        """Generate HTML table for RQ5."""
        html = """
    <h2>RQ5: Completeness Impact</h2>
    <table>
        <tr>
            <th>Model</th>
            <th>Correlation</th>
            <th>Degradation</th>
            <th>Min Completeness</th>
            <th>Robustness</th>
        </tr>
"""
        for result in report.results.rq5_report.model_results:
            html += f"""
        <tr>
            <td>{result.llm_model}</td>
            <td>{result.completeness_quality_correlation:.3f}</td>
            <td>{result.quality_degradation_rate:.3f}</td>
            <td>{result.min_completeness_for_quality_80:.2f}</td>
            <td>{result.robustness_score:.3f}</td>
        </tr>
"""
        html += "    </table>\n"
        return html
    
    def _generate_all_charts(self, report: RQ345BatchReport) -> Dict[str, Path]:
        """Generate all visualization charts."""
        if not MATPLOTLIB_AVAILABLE:
            print("Warning: matplotlib not available. Skipping chart generation.")
            return {}
        
        chart_files = {}
        
        try:
            # RQ3 charts
            if report.results.rq3_report:
                chart_files["rq3_quality_chart"] = self._generate_quality_comparison_chart(report)
            
            # RQ4 charts
            if report.results.rq4_report:
                chart_files["rq4_radar_chart"] = self._generate_multidimensional_radar_chart(report)
                chart_files["rq4_cost_chart"] = self._generate_cost_comparison_chart(report)
            
            # RQ5 charts
            if report.results.rq5_report:
                chart_files["rq5_correlation_chart"] = self._generate_completeness_correlation_chart(report)
            
            # Cross-RQ charts
            if report.cross_rq_analysis:
                chart_files["cross_rq_heatmap"] = self._generate_correlation_heatmap(report)
        
        except Exception as e:
            print(f"Warning: Error generating charts: {e}")
        
        return chart_files
    
    def _generate_quality_comparison_chart(self, report: RQ345BatchReport) -> Path:
        """Generate bar chart comparing code quality across models."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        models = list(report.results.rq3_report.aggregate_metrics.keys())
        qualities = [
            metrics.get("mean_overall_quality", 0.0)
            for metrics in report.results.rq3_report.aggregate_metrics.values()
        ]
        
        ax.bar(models, qualities, color='steelblue')
        ax.set_xlabel('LLM Model')
        ax.set_ylabel('Overall Quality Score')
        ax.set_title('RQ3: Code Quality Comparison')
        ax.set_ylim(0, 1.0)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_path = self.config.output_dir / f"rq3_quality_{report.experiment_id}.{self.config.chart_format}"
        fig.savefig(output_path, dpi=self.config.chart_dpi, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
    
    def _generate_multidimensional_radar_chart(self, report: RQ345BatchReport) -> Path:
        """Generate radar chart for multi-dimensional LLM comparison."""
        # Simplified radar chart (requires more complex implementation for true radar)
        fig, ax = plt.subplots(figsize=(12, 8))
        
        dimensions = ['Oracle F1', 'Code Quality', 'Consistency', 'Performance', 'Cost', 'Robustness']
        models = [r.llm_model for r in report.results.rq4_report.model_results]
        
        x = range(len(dimensions))
        width = 0.8 / len(models)
        
        for i, result in enumerate(report.results.rq4_report.model_results):
            values = [
                result.oracle_f1,
                result.code_overall_quality,
                result.coherence_score,
                1.0 / (result.avg_generation_time_ms / 1000) if result.avg_generation_time_ms > 0 else 0,
                1.0 - min(result.total_cost_usd / 100, 1.0),  # Normalize cost
                result.overall_score
            ]
            ax.bar([pos + i * width for pos in x], values, width, label=result.llm_model)
        
        ax.set_xlabel('Dimension')
        ax.set_ylabel('Normalized Score')
        ax.set_title('RQ4: Multi-Dimensional LLM Comparison')
        ax.set_xticks([pos + width * (len(models) - 1) / 2 for pos in x])
        ax.set_xticklabels(dimensions, rotation=45, ha='right')
        ax.legend()
        ax.set_ylim(0, 1.0)
        plt.tight_layout()
        
        output_path = self.config.output_dir / f"rq4_radar_{report.experiment_id}.{self.config.chart_format}"
        fig.savefig(output_path, dpi=self.config.chart_dpi, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
    
    def _generate_cost_comparison_chart(self, report: RQ345BatchReport) -> Path:
        """Generate chart comparing cost vs quality."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        models = []
        costs = []
        qualities = []
        
        for result in report.results.rq4_report.model_results:
            models.append(result.llm_model)
            costs.append(result.total_cost_usd)
            qualities.append(result.overall_score)
        
        scatter = ax.scatter(costs, qualities, s=100, alpha=0.6)
        
        for i, model in enumerate(models):
            ax.annotate(model, (costs[i], qualities[i]), fontsize=9)
        
        ax.set_xlabel('Total Cost (USD)')
        ax.set_ylabel('Overall Quality Score')
        ax.set_title('RQ4: Cost vs Quality Trade-off')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = self.config.output_dir / f"rq4_cost_{report.experiment_id}.{self.config.chart_format}"
        fig.savefig(output_path, dpi=self.config.chart_dpi, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
    
    def _generate_completeness_correlation_chart(self, report: RQ345BatchReport) -> Path:
        """Generate chart showing completeness vs quality correlation."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for result in report.results.rq5_report.model_results:
            if result.level_results:
                completeness = [r.completeness_level for r in result.level_results]
                quality = [r.avg_overall_quality for r in result.level_results]
                ax.plot(completeness, quality, marker='o', label=result.llm_model)
        
        ax.set_xlabel('Documentation Completeness')
        ax.set_ylabel('Overall Quality Score')
        ax.set_title('RQ5: Impact of Documentation Completeness on Quality')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = self.config.output_dir / f"rq5_correlation_{report.experiment_id}.{self.config.chart_format}"
        fig.savefig(output_path, dpi=self.config.chart_dpi, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
    
    def _generate_correlation_heatmap(self, report: RQ345BatchReport) -> Path:
        """Generate correlation heatmap across all metrics."""
        # Placeholder for correlation heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # This would require building a full correlation matrix
        # Simplified version shown here
        ax.text(0.5, 0.5, 'Correlation Heatmap\n(Full implementation requires correlation matrix)',
                ha='center', va='center', fontsize=12)
        ax.set_title('Cross-RQ Correlation Heatmap')
        ax.axis('off')
        
        output_path = self.config.output_dir / f"cross_rq_heatmap_{report.experiment_id}.{self.config.chart_format}"
        fig.savefig(output_path, dpi=self.config.chart_dpi, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
