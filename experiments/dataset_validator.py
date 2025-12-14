"""
Dataset Validator

This module validates the quality and consistency of generated datasets,
ensuring they meet quality standards for experimental use.

Validation checks:
1. Completeness of annotations
2. Schema consistency
3. Inter-variant consistency
4. Ground truth quality
5. Metadata completeness

Author: Aurel IKAMA HONEY
Date: December 12, 2025
"""
import json
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

import jsonschema


@dataclass
class ValidationReport:
    """Report of dataset validation."""
    dataset_name: str
    validation_date: str
    passed: bool
    overall_score: float
    checks: Dict[str, Any]
    issues: List[str]
    warnings: List[str]
    recommendations: List[str]


@dataclass
class ConsistencyReport:
    """Report of inter-variant consistency."""
    collection_name: str
    num_variants: int
    passed: bool
    consistency_score: float
    issues: List[str]
    warnings: List[str]


class DatasetValidator:
    """
    Validates quality and consistency of datasets.
    
    Responsibilities:
    1. Validate dataset completeness
    2. Check schema consistency
    3. Verify ground truth quality
    4. Validate inter-variant consistency
    5. Generate quality reports
    """
    
    def __init__(
        self,
        datasets_dir: Path = Path("experiments/datasets"),
        output_dir: Path = Path("experiments/datasets/validation")
    ):
        self.datasets_dir = Path(datasets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Quality thresholds
        self.thresholds = {
            "min_completeness": 0.90,
            "min_consistency": 0.85,
            "min_confidence": 0.80,
            "min_annotation_coverage": 1.0
        }
    
    def validate_dataset(
        self,
        dataset_path: Path,
        check_ground_truth: bool = True
    ) -> ValidationReport:
        """
        Validate a single dataset variant.
        
        Args:
            dataset_path: Path to dataset directory
            check_ground_truth: Whether to validate ground truth
            
        Returns:
            ValidationReport
        """
        print(f"\n🔍 Validating dataset: {dataset_path.name}")
        
        issues = []
        warnings = []
        recommendations = []
        checks = {}
        
        # Check 1: Metadata exists and is valid
        metadata_file = dataset_path / "metadata.json"
        if not metadata_file.exists():
            issues.append("Missing metadata.json")
            checks["has_metadata"] = False
        else:
            checks["has_metadata"] = True
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Validate required fields
                required_fields = [
                    "name", "completeness_level", "num_endpoints", "created_at"
                ]
                for field in required_fields:
                    if field not in metadata:
                        issues.append(f"Missing metadata field: {field}")
                
                checks["metadata_valid"] = len(issues) == 0
                
            except json.JSONDecodeError as e:
                issues.append(f"Invalid metadata JSON: {e}")
                checks["metadata_valid"] = False
        
        # Check 2: Endpoints file exists and is valid
        endpoints_file = dataset_path / "endpoints.json"
        if not endpoints_file.exists():
            issues.append("Missing endpoints.json")
            checks["has_endpoints"] = False
        else:
            checks["has_endpoints"] = True
            try:
                with open(endpoints_file, 'r') as f:
                    data = json.load(f)
                
                # Handle both direct list and wrapped format
                if isinstance(data, dict) and "endpoints" in data:
                    endpoints = data["endpoints"]
                elif isinstance(data, list):
                    endpoints = data
                else:
                    issues.append("endpoints.json has invalid format")
                    endpoints = []
                
                if len(endpoints) == 0:
                    issues.append("endpoints.json is empty")
                else:
                    checks["num_endpoints"] = len(endpoints)
                    
                    # Validate endpoint structure
                    endpoint_issues = self._validate_endpoints(endpoints)
                    if endpoint_issues:
                        issues.extend(endpoint_issues)
                        checks["endpoints_valid"] = False
                    else:
                        checks["endpoints_valid"] = True
                
            except json.JSONDecodeError as e:
                issues.append(f"Invalid endpoints JSON: {e}")
                checks["endpoints_valid"] = False
        
        # Check 3: Ground truth validation
        if check_ground_truth:
            ground_truth_file = dataset_path / "ground_truth.json"
            if not ground_truth_file.exists():
                warnings.append("Missing ground_truth.json")
                checks["has_ground_truth"] = False
            else:
                checks["has_ground_truth"] = True
                try:
                    with open(ground_truth_file, 'r') as f:
                        ground_truths = json.load(f)
                    
                    gt_issues = self._validate_ground_truths(ground_truths)
                    if gt_issues:
                        warnings.extend(gt_issues)
                    
                    # Check coverage
                    if checks.get("num_endpoints"):
                        coverage = len(ground_truths) / checks["num_endpoints"]
                        checks["ground_truth_coverage"] = coverage
                        
                        if coverage < self.thresholds["min_annotation_coverage"]:
                            warnings.append(
                                f"Low ground truth coverage: {coverage:.1%}"
                            )
                
                except json.JSONDecodeError as e:
                    warnings.append(f"Invalid ground truth JSON: {e}")
                    checks["ground_truths_valid"] = False
        
        # Check 4: Schema consistency
        if checks.get("endpoints_valid"):
            schema_issues = self._check_schema_consistency(endpoints)
            if schema_issues:
                warnings.extend(schema_issues)
            else:
                checks["schema_consistent"] = True
        
        # Calculate overall score
        passed_checks = sum(
            1 for v in checks.values() 
            if isinstance(v, bool) and v
        )
        total_checks = sum(
            1 for v in checks.values() 
            if isinstance(v, bool)
        )
        
        overall_score = passed_checks / total_checks if total_checks > 0 else 0.0
        checks["overall_score"] = overall_score
        
        # Determine pass/fail
        passed = len(issues) == 0 and overall_score >= 0.8
        
        # Generate recommendations
        if overall_score < 0.9:
            recommendations.append("Consider improving dataset quality")
        
        if checks.get("ground_truth_coverage", 1.0) < 1.0:
            recommendations.append("Add ground truths for all endpoints")
        
        # Create report
        report = ValidationReport(
            dataset_name=dataset_path.name,
            validation_date=datetime.utcnow().isoformat(),
            passed=passed,
            overall_score=overall_score,
            checks=checks,
            issues=issues,
            warnings=warnings,
            recommendations=recommendations
        )
        
        # Print summary
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status} - Score: {overall_score:.2%}")
        
        if issues:
            print(f"   ❌ {len(issues)} issues:")
            for issue in issues[:3]:  # Show first 3
                print(f"      - {issue}")
        
        if warnings:
            print(f"   ⚠️  {len(warnings)} warnings")
        
        return report
    
    def _validate_endpoints(self, endpoints: List[Dict]) -> List[str]:
        """Validate endpoint structure."""
        issues = []
        
        required_fields = ["id", "name", "method"]
        # Accept either 'path' or 'url' (EndpointContext uses 'url')
        path_or_url_required = True
        
        for idx, endpoint in enumerate(endpoints):
            for field in required_fields:
                if field not in endpoint:
                    issues.append(
                        f"Endpoint {idx}: Missing required field '{field}'"
                    )
            
            # Check for either 'path' or 'url'
            if path_or_url_required and "path" not in endpoint and "url" not in endpoint:
                issues.append(
                    f"Endpoint {idx}: Missing required field 'path' or 'url'"
                )
            
            # Validate method
            if "method" in endpoint:
                valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
                if endpoint["method"] not in valid_methods:
                    issues.append(
                        f"Endpoint {idx}: Invalid HTTP method '{endpoint['method']}'"
                    )
        
        return issues
    
    def _validate_ground_truths(self, ground_truths: Dict) -> List[str]:
        """Validate ground truth structure."""
        issues = []
        
        for endpoint_id, gt in ground_truths.items():
            if not isinstance(gt, dict):
                issues.append(f"Ground truth {endpoint_id}: Must be a dictionary")
                continue
            
            # Check required fields
            if "status_code" not in gt and "expected_status_codes" not in gt:
                issues.append(f"Ground truth {endpoint_id}: Missing status code")
            
            # Check confidence
            if "confidence" in gt:
                confidence = gt["confidence"]
                if not (0.0 <= confidence <= 1.0):
                    issues.append(
                        f"Ground truth {endpoint_id}: Invalid confidence {confidence}"
                    )
        
        return issues
    
    def _check_schema_consistency(self, endpoints: List[Dict]) -> List[str]:
        """Check consistency of endpoint schemas."""
        issues = []
        
        # Group by path pattern
        path_groups = defaultdict(list)
        for endpoint in endpoints:
            path = endpoint.get("path", "")
            # Normalize path (replace IDs with placeholder)
            normalized_path = self._normalize_path(path)
            path_groups[normalized_path].append(endpoint)
        
        # Check consistency within groups
        for path, group_endpoints in path_groups.items():
            if len(group_endpoints) > 1:
                # Check if methods are unique
                methods = [e.get("method") for e in group_endpoints]
                if len(methods) != len(set(methods)):
                    issues.append(
                        f"Duplicate methods for path '{path}': {methods}"
                    )
        
        return issues
    
    def _normalize_path(self, path: str) -> str:
        """Normalize path by replacing IDs with placeholder."""
        import re
        # Replace {id}, {uuid}, numeric IDs, etc.
        normalized = re.sub(r'\{[^}]+\}', '{id}', path)
        normalized = re.sub(r'/\d+', '/{id}', normalized)
        return normalized
    
    def validate_collection_consistency(
        self,
        collection_name: str
    ) -> ConsistencyReport:
        """
        Validate consistency across variants of a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            ConsistencyReport
        """
        print(f"\n🔍 Checking consistency: {collection_name}")
        
        variants_dir = self.datasets_dir / "variants" / collection_name
        
        if not variants_dir.exists():
            print(f"   ❌ Collection not found: {variants_dir}")
            return ConsistencyReport(
                collection_name=collection_name,
                num_variants=0,
                passed=False,
                consistency_score=0.0,
                issues=[f"Collection directory not found: {variants_dir}"],
                warnings=[]
            )
        
        issues = []
        warnings = []
        
        # Load all variants
        variants = {}
        for variant_dir in variants_dir.iterdir():
            if not variant_dir.is_dir():
                continue
            
            endpoints_file = variant_dir / "endpoints.json"
            if endpoints_file.exists():
                with open(endpoints_file, 'r') as f:
                    data = json.load(f)
                    # Handle both direct list and wrapped format
                    if isinstance(data, dict) and "endpoints" in data:
                        variants[variant_dir.name] = data["endpoints"]
                    elif isinstance(data, list):
                        variants[variant_dir.name] = data
                    else:
                        variants[variant_dir.name] = []
        
        if len(variants) < 2:
            warnings.append("Less than 2 variants found")
        
        # Check 1: Same number of endpoints
        endpoint_counts = {name: len(eps) for name, eps in variants.items()}
        if len(set(endpoint_counts.values())) > 1:
            issues.append(
                f"Variants have different endpoint counts: {endpoint_counts}"
            )
        
        # Check 2: Same endpoint IDs (for 100% variant)
        if "completeness_100" in variants:
            base_endpoints = variants["completeness_100"]
            base_ids = {
                ep.get("id") if isinstance(ep, dict) else str(ep)
                for ep in base_endpoints
            }
            
            for variant_name, endpoints in variants.items():
                if variant_name == "completeness_100":
                    continue
                
                variant_ids = {
                    ep.get("id") if isinstance(ep, dict) else str(ep)
                    for ep in endpoints
                }
                
                if base_ids != variant_ids:
                    missing = base_ids - variant_ids
                    extra = variant_ids - base_ids
                    
                    if missing:
                        issues.append(
                            f"{variant_name}: Missing {len(missing)} endpoints"
                        )
                    if extra:
                        warnings.append(
                            f"{variant_name}: Has {len(extra)} extra endpoints"
                        )
        
        # Check 3: Progressive degradation
        completeness_levels = []
        for variant_name in variants.keys():
            if "completeness_" in variant_name:
                try:
                    level = int(variant_name.split("_")[1])
                    completeness_levels.append(level)
                except:
                    pass
        
        if completeness_levels:
            expected_levels = [100, 75, 50, 25]
            missing_levels = set(expected_levels) - set(completeness_levels)
            if missing_levels:
                warnings.append(
                    f"Missing completeness levels: {sorted(missing_levels)}"
                )
        
        # Calculate consistency score
        consistency_score = 1.0 - (len(issues) * 0.2) - (len(warnings) * 0.05)
        consistency_score = max(0.0, consistency_score)
        
        passed = len(issues) == 0 and consistency_score >= self.thresholds["min_consistency"]
        
        report = ConsistencyReport(
            collection_name=collection_name,
            num_variants=len(variants),
            passed=passed,
            consistency_score=consistency_score,
            issues=issues,
            warnings=warnings
        )
        
        status = "✅ CONSISTENT" if passed else "❌ INCONSISTENT"
        print(f"   {status} - Score: {consistency_score:.2%}")
        
        if issues:
            print(f"   ❌ {len(issues)} issues")
        if warnings:
            print(f"   ⚠️  {len(warnings)} warnings")
        
        return report
    
    def validate_all_datasets(
        self,
        generate_report: bool = True
    ) -> Dict[str, ValidationReport]:
        """
        Validate all datasets in variants directory.
        
        Args:
            generate_report: Whether to generate HTML report
            
        Returns:
            Dictionary mapping dataset names to validation reports
        """
        print("\n" + "="*70)
        print(" VALIDATING ALL DATASETS ".center(70))
        print("="*70)
        
        reports = {}
        
        variants_dir = self.datasets_dir / "variants"
        if not variants_dir.exists():
            print(f"❌ Variants directory not found: {variants_dir}")
            return reports
        
        # Validate each collection's variants
        for collection_dir in variants_dir.iterdir():
            if not collection_dir.is_dir():
                continue
            
            print(f"\n📁 Collection: {collection_dir.name}")
            
            # Validate consistency across variants
            consistency_report = self.validate_collection_consistency(
                collection_dir.name
            )
            
            # Validate each variant
            for variant_dir in collection_dir.iterdir():
                if not variant_dir.is_dir():
                    continue
                
                report = self.validate_dataset(variant_dir)
                reports[variant_dir.name] = report
        
        # Summary
        total = len(reports)
        passed = sum(1 for r in reports.values() if r.passed)
        failed = total - passed
        
        print("\n" + "="*70)
        print(" VALIDATION SUMMARY ".center(70))
        print("="*70)
        print(f"\n   Total datasets:  {total}")
        print(f"   ✅ Passed:       {passed} ({passed/total:.1%})")
        print(f"   ❌ Failed:       {failed} ({failed/total:.1%})")
        
        avg_score = sum(r.overall_score for r in reports.values()) / total if total > 0 else 0
        print(f"   📊 Average score: {avg_score:.2%}")
        
        # Generate report
        if generate_report:
            self._generate_html_report(reports)
        
        return reports
    
    def _generate_html_report(self, reports: Dict[str, ValidationReport]) -> Path:
        """Generate HTML validation report."""
        html_path = self.output_dir / "validation_report.html"
        
        html = [
            "<html><head><title>Dataset Validation Report</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            "h1 { color: #333; }",
            ".passed { color: green; }",
            ".failed { color: red; }",
            ".warning { color: orange; }",
            "table { border-collapse: collapse; width: 100%; margin: 20px 0; }",
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "th { background-color: #4CAF50; color: white; }",
            "tr:nth-child(even) { background-color: #f2f2f2; }",
            "</style></head><body>",
            f"<h1>Dataset Validation Report</h1>",
            f"<p>Generated: {datetime.utcnow().isoformat()}</p>",
            "<table>",
            "<tr><th>Dataset</th><th>Status</th><th>Score</th><th>Issues</th><th>Warnings</th></tr>"
        ]
        
        for name, report in sorted(reports.items()):
            status_class = "passed" if report.passed else "failed"
            status_text = "✅ PASSED" if report.passed else "❌ FAILED"
            
            html.append(
                f"<tr>"
                f"<td>{name}</td>"
                f"<td class='{status_class}'>{status_text}</td>"
                f"<td>{report.overall_score:.1%}</td>"
                f"<td>{len(report.issues)}</td>"
                f"<td>{len(report.warnings)}</td>"
                f"</tr>"
            )
        
        html.append("</table></body></html>")
        
        with open(html_path, 'w') as f:
            f.write('\n'.join(html))
        
        print(f"\n📄 HTML report generated: {html_path}")
        
        return html_path


def main():
    """Main execution function."""
    validator = DatasetValidator()
    
    # Validate all datasets
    reports = validator.validate_all_datasets(generate_report=True)
    
    # Print summary of failed datasets
    failed = [name for name, report in reports.items() if not report.passed]
    
    if failed:
        print(f"\n❌ Failed datasets ({len(failed)}):")
        for name in failed:
            print(f"   - {name}")
    else:
        print("\n✅ All datasets passed validation!")


if __name__ == "__main__":
    main()
