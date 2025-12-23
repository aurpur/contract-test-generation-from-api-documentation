"""
===============================================================================
Dataset Splitter for Train/Test Division
===============================================================================

OBJECTIF:
    Diviser les datasets de manière stratifiée en ensembles train et test,
    garantissant une distribution représentative selon plusieurs critères.

FONCTIONNALITÉS:
    1. Split stratifié par critères multiples (domaine, complétude, complexité)
    2. Validation de la qualité du split
    3. Prévention des fuites de données (data leakage)
    4. Export/import des splits

USAGE:
    from experiments.dataset_splitter import DatasetSplitter
    splitter = DatasetSplitter()
    train, test = splitter.split(dataset, test_ratio=0.2)

Auteur: Aurel IKAMA HONEY
Date: December 12, 2025
===============================================================================
"""
import json
import random
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from uuid import uuid4

import numpy as np


@dataclass
class SplitMetadata:
    """Metadata for a train/test split."""
    split_id: str
    split_type: str  # "train" or "test"
    split_ratio: float
    total_samples: int
    num_samples: int
    collections_included: List[str]
    completeness_levels: List[float]
    domains: List[str]
    stratify_by: List[str]
    random_seed: int
    created_at: str


@dataclass
class DatasetSample:
    """Represents a single dataset sample."""
    sample_id: str
    collection_name: str
    variant_name: str
    completeness_level: float
    domain: str
    num_endpoints: int
    complexity_score: float
    endpoints_file: str
    ground_truth_file: str
    metadata_file: str


class DatasetSplitter:
    """
    Splits datasets into train and test sets with stratification.
    
    Responsibilities:
    1. Stratified split by domain/completeness/complexity
    2. Validation of split quality
    3. Prevention of data leakage
    4. Export train/test sets with metadata
    """
    
    def __init__(
        self,
        datasets_dir: Path = Path("experiments/datasets"),
        output_dir: Path = Path("experiments/datasets/splits"),
        random_seed: int = 42
    ):
        self.datasets_dir = Path(datasets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)
    
    def load_datasets(self) -> List[DatasetSample]:
        """
        Load all dataset samples from variants directory.
        
        Returns:
            List of DatasetSample objects
        """
        print("\n📂 Loading datasets...")
        
        samples = []
        variants_dir = self.datasets_dir / "variants"
        
        if not variants_dir.exists():
            print(f"❌ Variants directory not found: {variants_dir}")
            return samples
        
        # Iterate through collections
        for collection_dir in variants_dir.iterdir():
            if not collection_dir.is_dir():
                continue
            
            collection_name = collection_dir.name
            
            # Iterate through completeness variants
            for variant_dir in collection_dir.iterdir():
                if not variant_dir.is_dir():
                    continue
                
                variant_name = variant_dir.name
                
                # Load metadata
                metadata_file = variant_dir / "metadata.json"
                if not metadata_file.exists():
                    print(f"⚠️  Missing metadata: {metadata_file}")
                    continue
                
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Create sample
                sample = DatasetSample(
                    sample_id=str(uuid4()),
                    collection_name=collection_name,
                    variant_name=variant_name,
                    completeness_level=metadata.get("completeness_level", 1.0),
                    domain=metadata.get("domain", "unknown"),
                    num_endpoints=metadata.get("num_endpoints", 0),
                    complexity_score=self._calculate_complexity(metadata),
                    endpoints_file=str(variant_dir / "endpoints.json"),
                    ground_truth_file=str(variant_dir / "ground_truth.json"),
                    metadata_file=str(metadata_file)
                )
                
                samples.append(sample)
        
        print(f"✅ Loaded {len(samples)} dataset samples")
        return samples
    
    def _calculate_complexity(self, metadata: Dict) -> float:
        """
        Calculate complexity score for a dataset.
        
        Factors:
        - Number of endpoints
        - Schema depth
        - Number of parameters
        - Authentication requirements
        
        Args:
            metadata: Dataset metadata
            
        Returns:
            Complexity score (0.0-1.0)
        """
        num_endpoints = metadata.get("num_endpoints", 0)
        
        # Normalize to 0-1 scale (assume max 20 endpoints)
        endpoint_score = min(num_endpoints / 20.0, 1.0)
        
        # Add other factors when available
        complexity = endpoint_score
        
        return complexity
    
    def stratified_split(
        self,
        samples: List[DatasetSample],
        train_ratio: float = 0.7,
        stratify_by: List[str] = ["domain", "completeness_level"]
    ) -> Tuple[List[DatasetSample], List[DatasetSample]]:
        """
        Perform stratified split of datasets.
        
        Args:
            samples: List of dataset samples
            train_ratio: Ratio for training set (0.0-1.0)
            stratify_by: List of attributes to stratify by
            
        Returns:
            Tuple of (train_samples, test_samples)
        """
        print(f"\n🔀 Performing stratified split (train={train_ratio:.1%})...")
        print(f"   Stratify by: {', '.join(stratify_by)}")
        
        # Group samples by strata
        strata = defaultdict(list)
        
        for sample in samples:
            # Create stratum key
            key_parts = []
            for attr in stratify_by:
                value = getattr(sample, attr)
                if isinstance(value, float):
                    # Bin float values
                    value = f"{value:.2f}"
                key_parts.append(f"{attr}={value}")
            
            stratum_key = "|".join(key_parts)
            strata[stratum_key].append(sample)
        
        print(f"\n   Created {len(strata)} strata:")
        for key, samples_in_stratum in strata.items():
            print(f"   - {key}: {len(samples_in_stratum)} samples")
        
        # Split each stratum
        train_samples = []
        test_samples = []
        
        for stratum_key, stratum_samples in strata.items():
            # Shuffle samples within stratum
            random.shuffle(stratum_samples)
            
            # Calculate split point
            n_train = max(1, int(len(stratum_samples) * train_ratio))
            
            # Split
            train_samples.extend(stratum_samples[:n_train])
            test_samples.extend(stratum_samples[n_train:])
        
        print(f"\n✅ Split complete:")
        print(f"   Train: {len(train_samples)} samples ({len(train_samples)/len(samples):.1%})")
        print(f"   Test:  {len(test_samples)} samples ({len(test_samples)/len(samples):.1%})")
        
        return train_samples, test_samples
    
    def validate_split(
        self,
        train_samples: List[DatasetSample],
        test_samples: List[DatasetSample],
        stratify_by: List[str] = ["domain", "completeness_level"]
    ) -> Dict[str, Any]:
        """
        Validate quality of train/test split.
        
        Checks:
        1. No data leakage
        2. Distribution similarity
        3. Size ratios
        
        Args:
            train_samples: Training samples
            test_samples: Test samples
            stratify_by: Attributes that were stratified
            
        Returns:
            Validation report dictionary
        """
        print("\n🔍 Validating split quality...")
        
        report = {
            "passed": True,
            "checks": {},
            "warnings": [],
            "errors": []
        }
        
        # Check 1: No data leakage (no common samples)
        train_ids = {s.sample_id for s in train_samples}
        test_ids = {s.sample_id for s in test_samples}
        common_ids = train_ids & test_ids
        
        if len(common_ids) > 0:
            report["checks"]["no_leak"] = False
            report["passed"] = False
            report["errors"].append(f"Data leakage detected: {len(common_ids)} common samples")
        else:
            report["checks"]["no_leak"] = True
            print("   ✅ No data leakage")
        
        # Check 2: Size ratios
        total = len(train_samples) + len(test_samples)
        train_ratio = len(train_samples) / total
        test_ratio = len(test_samples) / total
        
        report["checks"]["train_ratio"] = train_ratio
        report["checks"]["test_ratio"] = test_ratio
        
        print(f"   ✅ Train ratio: {train_ratio:.3f}")
        print(f"   ✅ Test ratio:  {test_ratio:.3f}")
        
        # Check 3: Distribution similarity
        for attr in stratify_by:
            train_dist = self._get_distribution(train_samples, attr)
            test_dist = self._get_distribution(test_samples, attr)
            
            # Compare distributions
            similarity = self._compare_distributions(train_dist, test_dist)
            
            report["checks"][f"{attr}_distribution_similarity"] = similarity
            
            if similarity < 0.8:
                report["warnings"].append(
                    f"{attr} distribution differs: similarity={similarity:.2f}"
                )
                print(f"   ⚠️  {attr} distribution similarity: {similarity:.2f}")
            else:
                print(f"   ✅ {attr} distribution similarity: {similarity:.2f}")
        
        # Check 4: Minimum samples per stratum
        for attr in stratify_by:
            train_dist = self._get_distribution(train_samples, attr)
            test_dist = self._get_distribution(test_samples, attr)
            
            for value, count in train_dist.items():
                if count < 2:
                    report["warnings"].append(
                        f"Train: Only {count} sample(s) for {attr}={value}"
                    )
            
            for value, count in test_dist.items():
                if count < 1:
                    report["warnings"].append(
                        f"Test: No samples for {attr}={value}"
                    )
        
        # Summary
        if report["passed"]:
            print("\n✅ Split validation PASSED")
        else:
            print("\n❌ Split validation FAILED")
        
        if report["warnings"]:
            print(f"\n⚠️  {len(report['warnings'])} warnings:")
            for warning in report["warnings"]:
                print(f"   - {warning}")
        
        return report
    
    def _get_distribution(
        self,
        samples: List[DatasetSample],
        attribute: str
    ) -> Dict[Any, int]:
        """
        Get distribution of attribute values in samples.
        
        Args:
            samples: List of samples
            attribute: Attribute name
            
        Returns:
            Dictionary mapping values to counts
        """
        distribution = defaultdict(int)
        
        for sample in samples:
            value = getattr(sample, attribute)
            if isinstance(value, float):
                value = round(value, 2)
            distribution[value] += 1
        
        return dict(distribution)
    
    def _compare_distributions(
        self,
        dist1: Dict[Any, int],
        dist2: Dict[Any, int]
    ) -> float:
        """
        Compare similarity of two distributions.
        
        Uses cosine similarity of normalized distributions.
        
        Args:
            dist1: First distribution
            dist2: Second distribution
            
        Returns:
            Similarity score (0.0-1.0)
        """
        # Get all keys
        all_keys = set(dist1.keys()) | set(dist2.keys())
        
        if not all_keys:
            return 1.0
        
        # Create vectors
        vec1 = np.array([dist1.get(k, 0) for k in all_keys], dtype=float)
        vec2 = np.array([dist2.get(k, 0) for k in all_keys], dtype=float)
        
        # Normalize
        total1 = vec1.sum()
        total2 = vec2.sum()
        
        if total1 > 0:
            vec1 /= total1
        if total2 > 0:
            vec2 /= total2
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def export_split(
        self,
        train_samples: List[DatasetSample],
        test_samples: List[DatasetSample],
        split_name: str = "default",
        stratify_by: List[str] = ["domain", "completeness_level"]
    ) -> Tuple[Path, Path]:
        """
        Export train and test splits to disk.
        
        Args:
            train_samples: Training samples
            test_samples: Test samples
            split_name: Name for this split
            stratify_by: Attributes used for stratification
            
        Returns:
            Tuple of (train_dir, test_dir) paths
        """
        print(f"\n💾 Exporting split: {split_name}")
        
        # Create split directory
        split_dir = self.output_dir / split_name
        split_dir.mkdir(exist_ok=True)
        
        # Create train and test directories
        train_dir = split_dir / "train"
        test_dir = split_dir / "test"
        train_dir.mkdir(exist_ok=True)
        test_dir.mkdir(exist_ok=True)
        
        # Export train samples
        self._export_samples(train_samples, train_dir, "train", stratify_by)
        
        # Export test samples
        self._export_samples(test_samples, test_dir, "test", stratify_by)
        
        # Export split metadata
        total_samples = len(train_samples) + len(test_samples)
        
        metadata = {
            "split_name": split_name,
            "created_at": datetime.utcnow().isoformat(),
            "random_seed": self.random_seed,
            "stratify_by": stratify_by,
            "total_samples": total_samples,
            "train": {
                "num_samples": len(train_samples),
                "ratio": len(train_samples) / total_samples,
                "path": str(train_dir)
            },
            "test": {
                "num_samples": len(test_samples),
                "ratio": len(test_samples) / total_samples,
                "path": str(test_dir)
            }
        }
        
        metadata_file = split_dir / "split_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Exported split to: {split_dir}")
        print(f"   Train: {train_dir}")
        print(f"   Test:  {test_dir}")
        
        return train_dir, test_dir
    
    def _export_samples(
        self,
        samples: List[DatasetSample],
        output_dir: Path,
        split_type: str,
        stratify_by: List[str]
    ) -> None:
        """
        Export samples to directory.
        
        Args:
            samples: List of samples to export
            output_dir: Output directory
            split_type: "train" or "test"
            stratify_by: Stratification attributes
        """
        # Create samples index
        samples_index = []
        
        for sample in samples:
            samples_index.append(asdict(sample))
        
        # Save samples index
        index_file = output_dir / "samples_index.json"
        with open(index_file, 'w') as f:
            json.dump(samples_index, f, indent=2)
        
        # Create metadata
        collections = list(set(s.collection_name for s in samples))
        completeness_levels = list(set(s.completeness_level for s in samples))
        domains = list(set(s.domain for s in samples))
        
        metadata = SplitMetadata(
            split_id=str(uuid4()),
            split_type=split_type,
            split_ratio=len(samples) / (len(samples) + 1),  # Approximate
            total_samples=len(samples),
            num_samples=len(samples),
            collections_included=sorted(collections),
            completeness_levels=sorted(completeness_levels),
            domains=sorted(domains),
            stratify_by=stratify_by,
            random_seed=self.random_seed,
            created_at=datetime.utcnow().isoformat()
        )
        
        metadata_file = output_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)
        
        print(f"   - Exported {len(samples)} {split_type} samples")
    
    def create_split(
        self,
        train_ratio: float = 0.7,
        split_name: str = "default",
        stratify_by: List[str] = ["domain", "completeness_level"]
    ) -> Tuple[Path, Path]:
        """
        Complete workflow: load, split, validate, and export.
        
        Args:
            train_ratio: Ratio for training set
            split_name: Name for this split
            stratify_by: Attributes to stratify by
            
        Returns:
            Tuple of (train_dir, test_dir) paths
        """
        print("\n" + "="*70)
        print(" CREATING TRAIN/TEST SPLIT ".center(70))
        print("="*70)
        
        # Load datasets
        samples = self.load_datasets()
        
        if not samples:
            raise ValueError("No datasets found to split")
        
        # Perform split
        train_samples, test_samples = self.stratified_split(
            samples, train_ratio, stratify_by
        )
        
        # Validate split
        validation_report = self.validate_split(
            train_samples, test_samples, stratify_by
        )
        
        if not validation_report["passed"]:
            print("\n⚠️  WARNING: Split validation failed but continuing...")
        
        # Export split
        train_dir, test_dir = self.export_split(
            train_samples, test_samples, split_name, stratify_by
        )
        
        print("\n" + "="*70)
        print(" SPLIT CREATION COMPLETE ".center(70))
        print("="*70 + "\n")
        
        return train_dir, test_dir


def main():
    """Main execution function."""
    splitter = DatasetSplitter()
    
    # Create default split
    train_dir, test_dir = splitter.create_split(
        train_ratio=0.7,
        split_name="default",
        stratify_by=["domain", "completeness_level"]
    )
    
    print(f"\n✅ Train set: {train_dir}")
    print(f"✅ Test set:  {test_dir}")


if __name__ == "__main__":
    main()
