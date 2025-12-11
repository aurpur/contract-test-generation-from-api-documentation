"""
Reporting and Visualization for RQ1 Experiments

Creates publication-ready visualizations and reports:
- Precision/Recall/F1 comparison charts
- Statistical significance tables
- LaTeX tables for papers
- Interactive HTML dashboards
- CSV exports for further analysis

Author: Aurel IKAMA HONEY
Date: December 11, 2025
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

from experiments.rq1_oracle_validation import ExperimentReport
from experiments.rq1_orchestrator import BatchExperimentResults


class RQ1ReportGenerator:
    """
    Generate comprehensive reports and visualizations for RQ1 experiments.
    """
    
    def __init__(self, output_dir: Path = Path("experiments/results/rq1/reports")):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set plotting style
        if MATPLOTLIB_AVAILABLE:
            sns.set_style("whitegrid")
            plt.rcParams['figure.figsize'] = (10, 6)
            plt.rcParams['font.size'] = 12
    
    def generate_full_report(
        self,
        results: BatchExperimentResults,
        report_name: str = "rq1_full_report"
    ) -> Dict[str, Path]:
        """
        Generate complete report with all visualizations and tables.
        
        Args:
            results: Batch experiment results
            report_name: Base name for report files
            
        Returns:
            Dictionary mapping file types to output paths
        """
        output_files = {}
        
        print(f"\n{'='*60}")
        print(f"GENERATING COMPREHENSIVE REPORT: {report_name}")
        print(f"{'='*60}\n")
        
        # 1. Generate comparison chart
        if MATPLOTLIB_AVAILABLE:
            chart_path = self.create_llm_comparison_chart(
                results,
                filename=f"{report_name}_comparison.png"
            )
            output_files["comparison_chart"] = chart_path
        
        # 2. Generate precision-recall chart
        if MATPLOTLIB_AVAILABLE:
            pr_chart_path = self.create_precision_recall_chart(
                results,
                filename=f"{report_name}_precision_recall.png"
            )
            output_files["precision_recall_chart"] = pr_chart_path
        
        # 3. Generate completeness impact chart
        if MATPLOTLIB_AVAILABLE:
            completeness_chart_path = self.create_completeness_impact_chart(
                results,
                filename=f"{report_name}_completeness_impact.png"
            )
            output_files["completeness_chart"] = completeness_chart_path
        
        # 4. Generate LaTeX table
        latex_path = self.create_latex_table(
            results,
            filename=f"{report_name}_table.tex"
        )
        output_files["latex_table"] = latex_path
        
        # 5. Generate CSV export
        csv_path = self.export_to_csv(
            results,
            filename=f"{report_name}_data.csv"
        )
        output_files["csv_export"] = csv_path
        
        # 6. Generate HTML dashboard
        html_path = self.create_html_dashboard(
            results,
            filename=f"{report_name}_dashboard.html"
        )
        output_files["html_dashboard"] = html_path
        
        # 7. Generate markdown summary
        md_path = self.create_markdown_summary(
            results,
            filename=f"{report_name}_summary.md"
        )
        output_files["markdown_summary"] = md_path
        
        print(f"\n✓ Report generation complete!")
        print(f"  Files saved in: {self.output_dir}")
        for file_type, path in output_files.items():
            print(f"    - {file_type}: {path.name}")
        
        return output_files
    
    def create_llm_comparison_chart(
        self,
        results: BatchExperimentResults,
        filename: str = "llm_comparison.png"
    ) -> Path:
        """
        Create bar chart comparing LLM performance.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved chart
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠ Matplotlib not available, skipping chart generation")
            return None
        
        stats = results.statistical_results["llm_statistics"]
        
        # Extract data
        llms = list(stats.keys())
        precisions = [stats[llm]["precision"]["mean"] for llm in llms]
        recalls = [stats[llm]["recall"]["mean"] for llm in llms]
        f1_scores = [stats[llm]["f1_score"]["mean"] for llm in llms]
        
        # Error bars
        precision_stds = [stats[llm]["precision"]["stdev"] for llm in llms]
        recall_stds = [stats[llm]["recall"]["stdev"] for llm in llms]
        f1_stds = [stats[llm]["f1_score"]["stdev"] for llm in llms]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(llms))
        width = 0.25
        
        ax.bar([i - width for i in x], precisions, width, 
               yerr=precision_stds, label='Precision', capsize=5)
        ax.bar(x, recalls, width,
               yerr=recall_stds, label='Recall', capsize=5)
        ax.bar([i + width for i in x], f1_scores, width,
               yerr=f1_stds, label='F1 Score', capsize=5)
        
        ax.set_xlabel('LLM Model')
        ax.set_ylabel('Score')
        ax.set_title('LLM Performance Comparison (RQ1: Oracle Quality)')
        ax.set_xticks(x)
        ax.set_xticklabels(llms, rotation=45, ha='right')
        ax.legend()
        ax.set_ylim(0, 1.1)
        
        plt.tight_layout()
        
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Created LLM comparison chart: {output_path}")
        return output_path
    
    def create_precision_recall_chart(
        self,
        results: BatchExperimentResults,
        filename: str = "precision_recall.png"
    ) -> Path:
        """
        Create precision-recall scatter plot.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved chart
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        stats = results.statistical_results["llm_statistics"]
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        for llm, llm_stats in stats.items():
            precision = llm_stats["precision"]["mean"]
            recall = llm_stats["recall"]["mean"]
            
            ax.scatter(recall, precision, s=200, alpha=0.6, label=llm)
            ax.annotate(llm, (recall, precision), 
                       xytext=(5, 5), textcoords='offset points')
        
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_title('Precision vs Recall (RQ1: Oracle Quality)')
        ax.set_xlim(0, 1.05)
        ax.set_ylim(0, 1.05)
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)  # Diagonal line
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Created precision-recall chart: {output_path}")
        return output_path
    
    def create_completeness_impact_chart(
        self,
        results: BatchExperimentResults,
        filename: str = "completeness_impact.png"
    ) -> Path:
        """
        Create line chart showing impact of documentation completeness.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved chart
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        # Group reports by completeness level and LLM
        completeness_data = {}
        
        for report in results.reports:
            # Extract completeness from experiment ID
            # Format: experiment_id_c75_r1 -> completeness = 0.75
            parts = report.experiment_id.split('_')
            completeness = None
            for part in parts:
                if part.startswith('c'):
                    try:
                        completeness = int(part[1:]) / 100.0
                        break
                    except:
                        pass
            
            if completeness is None:
                continue
            
            if completeness not in completeness_data:
                completeness_data[completeness] = {}
            
            for llm, metrics in report.llm_metrics.items():
                if llm not in completeness_data[completeness]:
                    completeness_data[completeness][llm] = []
                completeness_data[completeness][llm].append(metrics["f1_score"])
        
        # Calculate means
        fig, ax = plt.subplots(figsize=(10, 6))
        
        completeness_levels = sorted(completeness_data.keys())
        
        for llm in results.config.llm_models:
            f1_means = []
            f1_stds = []
            
            for comp in completeness_levels:
                if llm in completeness_data[comp]:
                    scores = completeness_data[comp][llm]
                    f1_means.append(statistics.mean(scores))
                    f1_stds.append(statistics.stdev(scores) if len(scores) > 1 else 0.0)
                else:
                    f1_means.append(None)
                    f1_stds.append(None)
            
            ax.errorbar(
                [c * 100 for c in completeness_levels],
                f1_means,
                yerr=f1_stds,
                label=llm,
                marker='o',
                linewidth=2,
                capsize=5
            )
        
        ax.set_xlabel('Documentation Completeness (%)')
        ax.set_ylabel('F1 Score')
        ax.set_title('Impact of Documentation Completeness on Oracle Quality')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.1)
        
        plt.tight_layout()
        
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Created completeness impact chart: {output_path}")
        return output_path
    
    def create_latex_table(
        self,
        results: BatchExperimentResults,
        filename: str = "results_table.tex"
    ) -> Path:
        """
        Create LaTeX table for publication.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved table
        """
        stats = results.statistical_results["llm_statistics"]
        
        latex_content = []
        latex_content.append("\\begin{table}[htbp]")
        latex_content.append("\\centering")
        latex_content.append("\\caption{RQ1: Oracle Generation Quality by LLM Model}")
        latex_content.append("\\label{tab:rq1_results}")
        latex_content.append("\\begin{tabular}{lccc}")
        latex_content.append("\\toprule")
        latex_content.append("Model & Precision & Recall & F1 Score \\\\")
        latex_content.append("\\midrule")
        
        # Sort by F1 score
        sorted_llms = sorted(
            stats.items(),
            key=lambda x: x[1]["f1_score"]["mean"],
            reverse=True
        )
        
        for llm, llm_stats in sorted_llms:
            precision = llm_stats["precision"]["mean"]
            precision_std = llm_stats["precision"]["stdev"]
            recall = llm_stats["recall"]["mean"]
            recall_std = llm_stats["recall"]["stdev"]
            f1 = llm_stats["f1_score"]["mean"]
            f1_std = llm_stats["f1_score"]["stdev"]
            
            latex_content.append(
                f"{llm} & "
                f"{precision:.3f} $\\pm$ {precision_std:.3f} & "
                f"{recall:.3f} $\\pm$ {recall_std:.3f} & "
                f"\\textbf{{{f1:.3f}}} $\\pm$ {f1_std:.3f} \\\\"
            )
        
        latex_content.append("\\bottomrule")
        latex_content.append("\\end{tabular}")
        latex_content.append("\\end{table}")
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(latex_content))
        
        print(f"✓ Created LaTeX table: {output_path}")
        return output_path
    
    def export_to_csv(
        self,
        results: BatchExperimentResults,
        filename: str = "results.csv"
    ) -> Path:
        """
        Export results to CSV for further analysis.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved CSV
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            # Header
            f.write("experiment,llm_model,precision,recall,f1_score,completeness,replication\n")
            
            # Data rows
            for report in results.reports:
                # Extract metadata from experiment ID
                parts = report.experiment_id.split('_')
                completeness = "1.0"
                replication = "1"
                
                for part in parts:
                    if part.startswith('c'):
                        try:
                            completeness = str(int(part[1:]) / 100.0)
                        except:
                            pass
                    elif part.startswith('r'):
                        try:
                            replication = part[1:]
                        except:
                            pass
                
                for llm, metrics in report.aggregate_metrics.items():
                    f.write(
                        f"{report.experiment_id},"
                        f"{llm},"
                        f"{metrics.get('precision_mean', 0.0):.4f},"
                        f"{metrics.get('recall_mean', 0.0):.4f},"
                        f"{metrics.get('f1_mean', 0.0):.4f},"
                        f"{completeness},"
                        f"{replication}\n"
                    )
        
        print(f"✓ Exported data to CSV: {output_path}")
        return output_path
    
    def create_html_dashboard(
        self,
        results: BatchExperimentResults,
        filename: str = "dashboard.html"
    ) -> Path:
        """
        Create interactive HTML dashboard.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved dashboard
        """
        stats = results.statistical_results["llm_statistics"]
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>RQ1 Experiment Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .metric {{ font-weight: bold; color: #4CAF50; }}
        .summary {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>RQ1: Oracle Generation Quality - Experiment Results</h1>
    
    <div class="summary">
        <h2>Experiment Overview</h2>
        <p><strong>Name:</strong> {results.experiment_name}</p>
        <p><strong>Total Reports:</strong> {len(results.reports)}</p>
        <p><strong>LLM Models:</strong> {', '.join(results.config.llm_models)}</p>
        <p><strong>Completeness Levels:</strong> {', '.join([f'{c*100:.0f}%' for c in results.config.completeness_levels])}</p>
        <p><strong>Replications:</strong> {results.config.num_replications}</p>
        <p><strong>Completed:</strong> {results.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h2>Overall Performance</h2>
    <table>
        <tr>
            <th>LLM Model</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1 Score</th>
        </tr>
"""
        
        # Sort by F1 score
        sorted_llms = sorted(
            stats.items(),
            key=lambda x: x[1]["f1_score"]["mean"],
            reverse=True
        )
        
        for llm, llm_stats in sorted_llms:
            precision = llm_stats["precision"]["mean"]
            precision_std = llm_stats["precision"]["stdev"]
            recall = llm_stats["recall"]["mean"]
            recall_std = llm_stats["recall"]["stdev"]
            f1 = llm_stats["f1_score"]["mean"]
            f1_std = llm_stats["f1_score"]["stdev"]
            
            html_content += f"""
        <tr>
            <td><strong>{llm}</strong></td>
            <td>{precision:.3f} ± {precision_std:.3f}</td>
            <td>{recall:.3f} ± {recall_std:.3f}</td>
            <td class="metric">{f1:.3f} ± {f1_std:.3f}</td>
        </tr>
"""
        
        html_content += """
    </table>
    
    <h2>Pairwise Comparisons</h2>
    <table>
        <tr>
            <th>Comparison</th>
            <th>Mean F1 Difference</th>
            <th>Effect Size</th>
            <th>Better Model</th>
        </tr>
"""
        
        comparisons = results.statistical_results["pairwise_comparisons"]
        for comparison, comp_data in comparisons.items():
            html_content += f"""
        <tr>
            <td>{comparison}</td>
            <td>{comp_data['mean_f1_difference']:.4f}</td>
            <td>{comp_data['effect_size']:.4f}</td>
            <td class="metric">{comp_data['better_model']}</td>
        </tr>
"""
        
        html_content += """
    </table>
</body>
</html>
"""
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"✓ Created HTML dashboard: {output_path}")
        return output_path
    
    def create_markdown_summary(
        self,
        results: BatchExperimentResults,
        filename: str = "summary.md"
    ) -> Path:
        """
        Create markdown summary report.
        
        Args:
            results: Batch experiment results
            filename: Output filename
            
        Returns:
            Path to saved summary
        """
        stats = results.statistical_results["llm_statistics"]
        
        md_content = f"""# RQ1: Oracle Generation Quality - Experiment Results

## Experiment Overview

- **Name**: {results.experiment_name}
- **Total Reports**: {len(results.reports)}
- **LLM Models**: {', '.join(results.config.llm_models)}
- **Completeness Levels**: {', '.join([f'{c*100:.0f}%' for c in results.config.completeness_levels])}
- **Replications per Configuration**: {results.config.num_replications}
- **Completed**: {results.created_at.strftime('%Y-%m-%d %H:%M:%S')}

## Overall Performance

| LLM Model | Precision | Recall | F1 Score |
|-----------|-----------|--------|----------|
"""
        
        # Sort by F1 score
        sorted_llms = sorted(
            stats.items(),
            key=lambda x: x[1]["f1_score"]["mean"],
            reverse=True
        )
        
        for rank, (llm, llm_stats) in enumerate(sorted_llms, 1):
            precision = llm_stats["precision"]["mean"]
            precision_std = llm_stats["precision"]["stdev"]
            recall = llm_stats["recall"]["mean"]
            recall_std = llm_stats["recall"]["stdev"]
            f1 = llm_stats["f1_score"]["mean"]
            f1_std = llm_stats["f1_score"]["stdev"]
            
            md_content += f"| {llm} | {precision:.3f} ± {precision_std:.3f} | {recall:.3f} ± {recall_std:.3f} | **{f1:.3f} ± {f1_std:.3f}** |\n"
        
        md_content += f"""
## Key Findings

1. **Best Performing Model**: {sorted_llms[0][0]} with F1 score of {sorted_llms[0][1]['f1_score']['mean']:.3f}
2. **Total Experiments Run**: {len(results.reports)}
3. **Sample Size per Model**: {results.statistical_results['sample_sizes']}

## Pairwise Comparisons

"""
        
        comparisons = results.statistical_results["pairwise_comparisons"]
        for comparison, comp_data in comparisons.items():
            md_content += f"- **{comparison}**: Mean F1 difference = {comp_data['mean_f1_difference']:.4f}, Better model: {comp_data['better_model']}\n"
        
        md_content += """
## Interpretation

- **Precision**: Percentage of generated oracle constraints that are correct
- **Recall**: Percentage of ground truth constraints that were generated
- **F1 Score**: Harmonic mean of precision and recall

Higher values indicate better oracle generation quality.
"""
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write(md_content)
        
        print(f"✓ Created markdown summary: {output_path}")
        return output_path


def generate_sample_report():
    """Generate sample report from mock data."""
    # This would normally use real experiment results
    # For now, create a minimal structure for demonstration
    
    print("Note: This is a demonstration. Real reports require running experiments first.")
    print("To generate real reports:")
    print("  1. Run experiments using RQ1Orchestrator")
    print("  2. Pass BatchExperimentResults to RQ1ReportGenerator.generate_full_report()")


if __name__ == "__main__":
    generate_sample_report()
