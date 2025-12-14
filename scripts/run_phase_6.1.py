"""
Phase 6.1 Master Script: Complete Dataset Creation Workflow

This script orchestrates the complete Phase 6.1 workflow:
1. Crawl public API collections
2. Create dataset variants with different completeness levels
3. Generate ground truth annotations
4. Create train/test splits
5. Validate all datasets
6. Export datasets and generate catalogs

Author: Aurel IKAMA HONEY
Date: December 12, 2025
"""
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experiments.collection_crawler import CollectionCrawler
from experiments.create_datasets import RQ1DatasetCreator
from experiments.dataset_splitter import DatasetSplitter
from experiments.dataset_validator import DatasetValidator
from experiments.dataset_exporter import DatasetExporter


class Phase61Orchestrator:
    """
    Orchestrates the complete Phase 6.1 workflow.
    
    Workflow:
    1. Crawl and download public API collections
    2. Generate dataset variants at different completeness levels
    3. Create ground truth annotations
    4. Split datasets into train/test sets
    5. Validate all generated datasets
    6. Export datasets and generate catalogs
    """
    
    def __init__(
        self,
        base_dir: Path = Path("experiments/datasets"),
        collections_dir: Path = Path("bruno_collections")
    ):
        self.base_dir = Path(base_dir)
        self.collections_dir = Path(collections_dir)
        
        # Initialize components
        self.crawler = CollectionCrawler(output_dir=collections_dir)
        self.dataset_creator = RQ1DatasetCreator(
            collections_dir=collections_dir,
            output_dir=base_dir
        )
        self.splitter = DatasetSplitter(datasets_dir=base_dir)
        self.validator = DatasetValidator(datasets_dir=base_dir)
        self.exporter = DatasetExporter(datasets_dir=base_dir)
        
        self.execution_log = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.execution_log.append(log_entry)
        print(log_entry)
    
    def step_1_crawl_collections(self) -> bool:
        """
        Step 1: Crawl public API collections.
        
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 1: CRAWLING PUBLIC API COLLECTIONS")
        self.log("=" * 80)
        
        try:
            collections = self.crawler.crawl_all_public_apis()
            
            if not collections:
                self.log("No collections were crawled", "ERROR")
                return False
            
            self.log(f"Successfully crawled {len(collections)} collections", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Failed to crawl collections: {e}", "ERROR")
            return False
    
    def step_2_create_variants(self, collections: list = None) -> bool:
        """
        Step 2: Create dataset variants with different completeness levels.
        
        Args:
            collections: List of collection paths (None = discover automatically)
            
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 2: CREATING DATASET VARIANTS")
        self.log("=" * 80)
        
        try:
            # Discover collections if not provided
            if collections is None:
                collections = []
                for collection_dir in self.collections_dir.iterdir():
                    if collection_dir.is_dir():
                        collection_file = collection_dir / "collection.json"
                        if collection_file.exists():
                            collections.append(
                                str(collection_file.relative_to(self.collections_dir))
                            )
            
            if not collections:
                self.log("No collections found to process", "WARNING")
                return False
            
            self.log(f"Processing {len(collections)} collections")
            
            total_variants = 0
            
            for collection_path in collections:
                self.log(f"\nProcessing: {collection_path}")
                
                try:
                    # Create datasets at different completeness levels
                    datasets = self.dataset_creator.create_dataset_from_collection(
                        collection_path=collection_path,
                        completeness_levels=[1.0, 0.75, 0.5, 0.25]
                    )
                    
                    total_variants += len(datasets)
                    self.log(f"Created {len(datasets)} variants for {collection_path}")
                    
                except Exception as e:
                    self.log(f"Failed to process {collection_path}: {e}", "ERROR")
                    continue
            
            self.log(f"\nTotal variants created: {total_variants}", "SUCCESS")
            return total_variants > 0
            
        except Exception as e:
            self.log(f"Failed to create variants: {e}", "ERROR")
            return False
    
    def step_2_5_organize_variants(self) -> bool:
        """
        Step 2.5: Organize dataset variants into proper directory structure.
        
        Moves files from flat structure to variants/<collection>/<completeness>/ structure.
        
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 2.5: ORGANIZING DATASET VARIANTS")
        self.log("=" * 80)
        
        try:
            import re
            import shutil
            
            variants_dir = self.base_dir / "variants"
            variants_dir.mkdir(parents=True, exist_ok=True)
            
            # Find all endpoint and metadata files in base directory
            endpoint_files = list(self.base_dir.glob("*_endpoints.json"))
            metadata_files = list(self.base_dir.glob("*_metadata.json"))
            
            # Pattern to extract collection name and completeness level
            # Example: jsonplaceholder_rest_api_c100_endpoints.json
            pattern = r"(.+)_c(\d+)_(endpoints|metadata)\.json"
            
            organized = 0
            for file_path in endpoint_files + metadata_files:
                match = re.match(pattern, file_path.name)
                if not match:
                    continue
                
                collection_name = match.group(1)
                completeness = match.group(2)
                file_type = match.group(3)
                
                # Create variant directory
                variant_dir = variants_dir / collection_name / f"completeness_{completeness}"
                variant_dir.mkdir(parents=True, exist_ok=True)
                
                # Move file to variant directory
                dest_path = variant_dir / f"{file_type}.json"
                shutil.move(str(file_path), str(dest_path))
                organized += 1
            
            # Copy ground truths to variants
            ground_truths_dir = self.base_dir / "ground_truths"
            if ground_truths_dir.exists():
                for gt_file in ground_truths_dir.glob("*_gt_full.json"):
                    # Extract collection name (remove _gt_full.json)
                    collection_name = gt_file.stem.replace("_gt_full", "")
                    
                    # Copy to all completeness levels for this collection
                    collection_variants_dir = variants_dir / collection_name
                    if collection_variants_dir.exists():
                        for completeness_dir in collection_variants_dir.glob("completeness_*"):
                            dest_path = completeness_dir / "ground_truth.json"
                            shutil.copy(str(gt_file), str(dest_path))
            
            self.log(f"Organized {organized} files into variants structure", "SUCCESS")
            return organized > 0
            
        except Exception as e:
            self.log(f"Failed to organize variants: {e}", "ERROR")
            return False
    
    def step_3_create_ground_truths(self) -> bool:
        """
        Step 3: Create ground truth annotations.
        
        Note: Ground truths are created as part of step 2.
        This step validates and enhances them.
        
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 3: VALIDATING GROUND TRUTH ANNOTATIONS")
        self.log("=" * 80)
        
        try:
            ground_truths_dir = self.base_dir / "ground_truths"
            
            if not ground_truths_dir.exists():
                self.log("No ground truths directory found", "WARNING")
                return False
            
            # Count ground truth files
            gt_files = list(ground_truths_dir.glob("*.json"))
            
            self.log(f"Found {len(gt_files)} ground truth files")
            
            # TODO: Add ground truth validation and enhancement
            # For now, just report what we have
            
            return len(gt_files) > 0
            
        except Exception as e:
            self.log(f"Failed to validate ground truths: {e}", "ERROR")
            return False
    
    def step_4_create_splits(self) -> bool:
        """
        Step 4: Create train/test splits.
        
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 4: CREATING TRAIN/TEST SPLITS")
        self.log("=" * 80)
        
        try:
            train_dir, test_dir = self.splitter.create_split(
                train_ratio=0.7,
                split_name="default",
                stratify_by=["domain", "completeness_level"]
            )
            
            self.log(f"Train set: {train_dir}", "SUCCESS")
            self.log(f"Test set:  {test_dir}", "SUCCESS")
            
            return True
            
        except Exception as e:
            self.log(f"Failed to create splits: {e}", "ERROR")
            return False
    
    def step_5_validate_datasets(self) -> bool:
        """
        Step 5: Validate all datasets.
        
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 5: VALIDATING DATASETS")
        self.log("=" * 80)
        
        try:
            reports = self.validator.validate_all_datasets(generate_report=True)
            
            # Calculate statistics
            total = len(reports)
            passed = sum(1 for r in reports.values() if r.passed)
            
            if total == 0:
                self.log("No datasets found to validate", "WARNING")
                return False
            
            pass_rate = passed / total
            
            self.log(f"\nValidation Results:", "SUCCESS")
            self.log(f"  Total datasets: {total}")
            self.log(f"  Passed: {passed} ({pass_rate:.1%})")
            self.log(f"  Failed: {total - passed}")
            
            # Pass if at least 80% of datasets are valid
            return pass_rate >= 0.8
            
        except Exception as e:
            self.log(f"Failed to validate datasets: {e}", "ERROR")
            return False
    
    def step_6_export_datasets(self) -> bool:
        """
        Step 6: Export datasets and generate catalogs.
        
        Returns:
            True if successful
        """
        self.log("=" * 80)
        self.log("STEP 6: EXPORTING DATASETS AND GENERATING CATALOGS")
        self.log("=" * 80)
        
        try:
            # Generate catalog
            catalog_path = self.exporter.generate_catalog()
            self.log(f"Generated catalog: {catalog_path}")
            
            # Export metadata to CSV
            csv_path = self.exporter.export_metadata_to_csv()
            self.log(f"Exported metadata: {csv_path}")
            
            # Optionally export to ZIP (commented out to save disk space)
            # zip_path = self.exporter.export_all_to_zip()
            # self.log(f"Exported ZIP archive: {zip_path}")
            
            self.log("Export complete", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Failed to export datasets: {e}", "ERROR")
            return False
    
    def execute_full_workflow(self) -> bool:
        """
        Execute the complete Phase 6.1 workflow.
        
        Returns:
            True if all steps completed successfully
        """
        start_time = datetime.utcnow()
        
        self.log("\n" + "=" * 80)
        self.log(" PHASE 6.1: DATASET CREATION WORKFLOW ".center(80))
        self.log("=" * 80)
        self.log(f"Start time: {start_time.isoformat()}\n")
        
        results = {}
        
        # Step 1: Crawl collections
        results["step_1"] = self.step_1_crawl_collections()
        
        # Step 2: Create variants
        if results["step_1"]:
            results["step_2"] = self.step_2_create_variants()
        else:
            self.log("Skipping step 2 (step 1 failed)", "WARNING")
            results["step_2"] = False
        
        # Step 2.5: Organize variants
        if results["step_2"]:
            results["step_2_5"] = self.step_2_5_organize_variants()
        else:
            self.log("Skipping step 2.5 (step 2 failed)", "WARNING")
            results["step_2_5"] = False
        
        # Step 3: Ground truths
        if results["step_2_5"]:
            results["step_3"] = self.step_3_create_ground_truths()
        else:
            self.log("Skipping step 3 (step 2.5 failed)", "WARNING")
            results["step_3"] = False
        
        # Step 4: Train/test splits
        if results["step_3"]:
            results["step_4"] = self.step_4_create_splits()
        else:
            self.log("Skipping step 4 (step 3 failed)", "WARNING")
            results["step_4"] = False
        
        # Step 5: Validation
        if results["step_2_5"]:  # Can validate even if splits failed
            results["step_5"] = self.step_5_validate_datasets()
        else:
            self.log("Skipping step 5 (no datasets to validate)", "WARNING")
            results["step_5"] = False
        
        # Step 6: Export
        if results["step_2_5"]:  # Can export even if validation had issues
            results["step_6"] = self.step_6_export_datasets()
        else:
            self.log("Skipping step 6 (no datasets to export)", "WARNING")
            results["step_6"] = False
        
        # Calculate success
        end_time = datetime.utcnow()
        duration = end_time - start_time
        
        successful_steps = sum(results.values())
        total_steps = len(results)
        success_rate = successful_steps / total_steps
        
        self.log("\n" + "=" * 80)
        self.log(" WORKFLOW SUMMARY ".center(80))
        self.log("=" * 80)
        
        for step, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            self.log(f"{step}: {status}")
        
        self.log(f"\nSuccess rate: {successful_steps}/{total_steps} ({success_rate:.1%})")
        self.log(f"Duration: {duration}")
        self.log(f"End time: {end_time.isoformat()}")
        
        # Save execution log
        log_file = self.base_dir / "phase_6.1_execution.log"
        with open(log_file, 'w') as f:
            f.write('\n'.join(self.execution_log))
        
        self.log(f"\nExecution log saved: {log_file}")
        
        # Overall success if at least 80% of steps passed
        overall_success = success_rate >= 0.8
        
        if overall_success:
            self.log("\n🎉 PHASE 6.1 COMPLETED SUCCESSFULLY! 🎉", "SUCCESS")
        else:
            self.log("\n⚠️  PHASE 6.1 COMPLETED WITH ERRORS ⚠️", "WARNING")
        
        self.log("=" * 80 + "\n")
        
        return overall_success
    
    def execute_quick_workflow(self) -> bool:
        """
        Execute a quick workflow (skip crawling, use existing collections).
        
        Returns:
            True if successful
        """
        start_time = datetime.utcnow()
        
        self.log("\n" + "=" * 80)
        self.log(" PHASE 6.1: QUICK WORKFLOW (EXISTING COLLECTIONS) ".center(80))
        self.log("=" * 80)
        
        results = {}
        
        # Skip step 1, start with step 2
        results["step_2"] = self.step_2_create_variants()
        
        if results["step_2"]:
            results["step_3"] = self.step_3_create_ground_truths()
            results["step_4"] = self.step_4_create_splits()
            results["step_5"] = self.step_5_validate_datasets()
            results["step_6"] = self.step_6_export_datasets()
        
        end_time = datetime.utcnow()
        duration = end_time - start_time
        
        self.log(f"\nDuration: {duration}")
        
        return all(results.values())


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Phase 6.1: Complete Dataset Creation Workflow"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "quick"],
        default="full",
        help="Workflow mode: 'full' (crawl + create) or 'quick' (use existing)"
    )
    
    args = parser.parse_args()
    
    orchestrator = Phase61Orchestrator()
    
    if args.mode == "full":
        success = orchestrator.execute_full_workflow()
    else:
        success = orchestrator.execute_quick_workflow()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
