"""
===============================================================================
Dataset Exporter/Importer
===============================================================================

OBJECTIF:
    Utilitaires pour exporter et importer des datasets dans différents formats,
    facilitant le partage et la reproductibilité des expériences.

FORMATS SUPPORTÉS:
    1. JSON (format natif)
    2. Archives ZIP
    3. CSV/TSV pour les métadonnées
    4. Intégration avec les runners d'expériences

USAGE:
    from experiments.dataset_exporter import DatasetExporter
    exporter = DatasetExporter()
    exporter.export_to_zip(dataset, "output.zip")

Auteur: Aurel IKAMA HONEY
Date: December 12, 2025
===============================================================================
"""
import csv
import json
import shutil
import zipfile
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import pandas as pd


class DatasetExporter:
    """
    Exports datasets in various formats.
    
    Responsibilities:
    1. Export to JSON archive
    2. Export to ZIP archive
    3. Export metadata to CSV
    4. Generate dataset catalog
    """
    
    def __init__(
        self,
        datasets_dir: Path = Path("experiments/datasets"),
        output_dir: Path = Path("experiments/datasets/exports")
    ):
        self.datasets_dir = Path(datasets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_to_zip(
        self,
        collection_name: str,
        include_variants: Optional[List[str]] = None,
        output_name: Optional[str] = None
    ) -> Path:
        """
        Export a collection and its variants to a ZIP archive.
        
        Args:
            collection_name: Name of the collection
            include_variants: List of variant names to include (None = all)
            output_name: Output file name (default: collection_name.zip)
            
        Returns:
            Path to created ZIP file
        """
        print(f"\n📦 Exporting collection to ZIP: {collection_name}")
        
        if output_name is None:
            output_name = f"{collection_name}_{datetime.utcnow().strftime('%Y%m%d')}.zip"
        
        output_path = self.output_dir / output_name
        
        # Source directories
        collection_dir = self.datasets_dir / "collections" / collection_name
        variants_dir = self.datasets_dir / "variants" / collection_name
        
        # Create ZIP archive
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add collection files
            if collection_dir.exists():
                for file_path in collection_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.datasets_dir)
                        zipf.write(file_path, arcname)
                        print(f"   + {arcname}")
            
            # Add variant files
            if variants_dir.exists():
                for variant_dir in variants_dir.iterdir():
                    if not variant_dir.is_dir():
                        continue
                    
                    # Check if variant should be included
                    if include_variants and variant_dir.name not in include_variants:
                        continue
                    
                    for file_path in variant_dir.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(self.datasets_dir)
                            zipf.write(file_path, arcname)
                            print(f"   + {arcname}")
        
        print(f"✅ Exported to: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
        
        return output_path
    
    def export_all_to_zip(self, output_name: str = "all_datasets.zip") -> Path:
        """
        Export all datasets to a single ZIP archive.
        
        Args:
            output_name: Output file name
            
        Returns:
            Path to created ZIP file
        """
        print(f"\n📦 Exporting all datasets to ZIP")
        
        output_path = self.output_dir / output_name
        
        # Create ZIP archive
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dir_name in ["collections", "variants", "ground_truths"]:
                source_dir = self.datasets_dir / dir_name
                
                if not source_dir.exists():
                    continue
                
                print(f"   Adding {dir_name}...")
                
                for file_path in source_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.datasets_dir)
                        zipf.write(file_path, arcname)
        
        print(f"✅ Exported all datasets to: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        return output_path
    
    def export_metadata_to_csv(
        self,
        output_name: str = "datasets_metadata.csv"
    ) -> Path:
        """
        Export metadata of all datasets to CSV.
        
        Args:
            output_name: Output file name
            
        Returns:
            Path to created CSV file
        """
        print(f"\n📊 Exporting metadata to CSV")
        
        output_path = self.output_dir / output_name
        
        # Collect metadata from all variants
        metadata_records = []
        
        variants_dir = self.datasets_dir / "variants"
        if variants_dir.exists():
            for collection_dir in variants_dir.iterdir():
                if not collection_dir.is_dir():
                    continue
                
                for variant_dir in collection_dir.iterdir():
                    if not variant_dir.is_dir():
                        continue
                    
                    metadata_file = variant_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        # Flatten metadata
                        record = {
                            "collection": collection_dir.name,
                            "variant": variant_dir.name,
                            "name": metadata.get("name", ""),
                            "completeness_level": metadata.get("completeness_level", 0),
                            "num_endpoints": metadata.get("num_endpoints", 0),
                            "domain": metadata.get("domain", ""),
                            "created_at": metadata.get("created_at", "")
                        }
                        
                        metadata_records.append(record)
        
        # Write to CSV
        if metadata_records:
            df = pd.DataFrame(metadata_records)
            df.to_csv(output_path, index=False)
            
            print(f"✅ Exported {len(metadata_records)} dataset records to: {output_path}")
        else:
            print("⚠️  No metadata found to export")
        
        return output_path
    
    def generate_catalog(
        self,
        output_name: str = "datasets_catalog.json"
    ) -> Path:
        """
        Generate a comprehensive catalog of all datasets.
        
        Args:
            output_name: Output file name
            
        Returns:
            Path to created catalog file
        """
        print(f"\n📚 Generating dataset catalog")
        
        output_path = self.output_dir / output_name
        
        catalog = {
            "generated_at": datetime.utcnow().isoformat(),
            "datasets_dir": str(self.datasets_dir),
            "collections": [],
            "statistics": {
                "total_collections": 0,
                "total_variants": 0,
                "total_endpoints": 0,
                "completeness_levels": set(),
                "domains": set()
            }
        }
        
        # Scan collections
        collections_dir = self.datasets_dir / "collections"
        variants_dir = self.datasets_dir / "variants"
        
        if collections_dir.exists():
            for collection_dir in collections_dir.iterdir():
                if not collection_dir.is_dir():
                    continue
                
                collection_info = {
                    "name": collection_dir.name,
                    "path": str(collection_dir),
                    "variants": []
                }
                
                # Load collection metadata
                metadata_file = collection_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        collection_metadata = json.load(f)
                    collection_info["metadata"] = collection_metadata
                    
                    domain = collection_metadata.get("domain", "unknown")
                    catalog["statistics"]["domains"].add(domain)
                
                # Scan variants
                collection_variants_dir = variants_dir / collection_dir.name
                if collection_variants_dir.exists():
                    for variant_dir in collection_variants_dir.iterdir():
                        if not variant_dir.is_dir():
                            continue
                        
                        variant_metadata_file = variant_dir / "metadata.json"
                        if variant_metadata_file.exists():
                            with open(variant_metadata_file, 'r') as f:
                                variant_metadata = json.load(f)
                            
                            collection_info["variants"].append({
                                "name": variant_dir.name,
                                "path": str(variant_dir),
                                "metadata": variant_metadata
                            })
                            
                            catalog["statistics"]["total_variants"] += 1
                            catalog["statistics"]["total_endpoints"] += variant_metadata.get("num_endpoints", 0)
                            
                            completeness = variant_metadata.get("completeness_level", 1.0)
                            catalog["statistics"]["completeness_levels"].add(completeness)
                
                catalog["collections"].append(collection_info)
                catalog["statistics"]["total_collections"] += 1
        
        # Convert sets to lists for JSON serialization
        catalog["statistics"]["completeness_levels"] = sorted(
            list(catalog["statistics"]["completeness_levels"])
        )
        catalog["statistics"]["domains"] = sorted(
            list(catalog["statistics"]["domains"])
        )
        
        # Save catalog
        with open(output_path, 'w') as f:
            json.dump(catalog, f, indent=2)
        
        print(f"✅ Generated catalog: {output_path}")
        print(f"   Collections: {catalog['statistics']['total_collections']}")
        print(f"   Variants: {catalog['statistics']['total_variants']}")
        print(f"   Total endpoints: {catalog['statistics']['total_endpoints']}")
        
        return output_path


class DatasetImporter:
    """
    Imports datasets from various formats.
    
    Responsibilities:
    1. Import from ZIP archives
    2. Validate imported data
    3. Integrate with existing datasets
    """
    
    def __init__(
        self,
        datasets_dir: Path = Path("experiments/datasets")
    ):
        self.datasets_dir = Path(datasets_dir)
    
    def import_from_zip(
        self,
        zip_path: Path,
        overwrite: bool = False
    ) -> bool:
        """
        Import datasets from a ZIP archive.
        
        Args:
            zip_path: Path to ZIP file
            overwrite: Whether to overwrite existing files
            
        Returns:
            True if successful
        """
        print(f"\n📥 Importing from ZIP: {zip_path.name}")
        
        if not zip_path.exists():
            print(f"❌ ZIP file not found: {zip_path}")
            return False
        
        # Extract to temporary directory first
        temp_dir = self.datasets_dir / "temp_import"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(temp_dir)
                print(f"✅ Extracted {len(zipf.namelist())} files")
            
            # Move files to proper locations
            for source_path in temp_dir.rglob('*'):
                if not source_path.is_file():
                    continue
                
                # Calculate relative path
                rel_path = source_path.relative_to(temp_dir)
                target_path = self.datasets_dir / rel_path
                
                # Check if file exists
                if target_path.exists() and not overwrite:
                    print(f"⚠️  Skipping existing file: {rel_path}")
                    continue
                
                # Create parent directory
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.copy2(source_path, target_path)
                print(f"   + {rel_path}")
            
            # Clean up temp directory
            shutil.rmtree(temp_dir)
            
            print("✅ Import complete")
            return True
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            
            # Clean up temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            
            return False
    
    def validate_imported_dataset(
        self,
        dataset_path: Path
    ) -> bool:
        """
        Validate an imported dataset.
        
        Args:
            dataset_path: Path to dataset directory
            
        Returns:
            True if valid
        """
        required_files = ["metadata.json", "endpoints.json"]
        
        for filename in required_files:
            file_path = dataset_path / filename
            if not file_path.exists():
                print(f"❌ Missing required file: {filename}")
                return False
        
        # Validate JSON files
        try:
            metadata_file = dataset_path / "metadata.json"
            with open(metadata_file, 'r') as f:
                json.load(f)
            
            endpoints_file = dataset_path / "endpoints.json"
            with open(endpoints_file, 'r') as f:
                json.load(f)
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False


def main():
    """Main execution function."""
    exporter = DatasetExporter()
    
    # Generate catalog
    catalog_path = exporter.generate_catalog()
    
    # Export metadata to CSV
    csv_path = exporter.export_metadata_to_csv()
    
    # Export all to ZIP
    # zip_path = exporter.export_all_to_zip()
    
    print("\n✅ Export complete")


if __name__ == "__main__":
    main()
