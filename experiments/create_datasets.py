"""
===============================================================================
Test Dataset Creation for RQ1 Experiments
===============================================================================

OBJECTIF:
    Créer des datasets de test diversifiés pour les expériences RQ1.

CONTENU DES DATASETS:
    1. Collections Bruno d'APIs réelles (pas de simulation)
    2. Différents niveaux de complétude de documentation
    3. Domaines API variés (REST CRUD, authentification, pagination, etc.)
    4. Annotations ground truth créées manuellement ou extraites

USAGE:
    python -m experiments.create_datasets

NOTE:
    Les datasets sont stockés dans experiments/datasets/

Auteur: Aurel IKAMA HONEY
Date: December 11, 2025
===============================================================================
"""
import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import UUID

from src.parsers.bruno_parser import BrunoParser
from src.shared_context.models import EndpointContext, HTTPMethod, AuthType
from experiments.ground_truth_manager import GroundTruthManager


@dataclass
class DatasetMetadata:
    """Metadata for a test dataset."""
    name: str
    description: str
    collection_path: str
    completeness_level: float
    num_endpoints: int
    domains: List[str]
    created_at: datetime


class RQ1DatasetCreator:
    """
    Creates test datasets for RQ1 experiments.
    
    Generates datasets with varying completeness levels from real API collections.
    """
    
    def __init__(
        self,
        collections_dir: Path = Path("bruno_collections"),
        output_dir: Path = Path("experiments/datasets")
    ):
        self.collections_dir = Path(collections_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.parser = BrunoParser()
        self.gt_manager = GroundTruthManager(
            storage_dir=self.output_dir / "ground_truths"
        )
    
    def _convert_bruno_items_to_endpoints(self, bruno_items: List) -> List[EndpointContext]:
        """
        Convert BrunoItem objects to EndpointContext objects.
        
        Args:
            bruno_items: List of BrunoItem objects from parser
            
        Returns:
            List of EndpointContext objects
        """
        endpoints = []
        
        for item in bruno_items:
            if not item.request:
                continue
            
            request = item.request
            
            # Convert headers to dict
            headers = {h.name: h.value for h in request.headers if h.enabled}
            
            # Convert query params to dict
            query_params = {p.name: p.value for p in request.params if p.enabled}
            
            # Extract path parameters from URL
            import re
            path_params = re.findall(r'\{(\w+)\}|:(\w+)', request.url)
            path_params = [p[0] or p[1] for p in path_params]
            
            # Parse body
            body = None
            body_schema = None
            if request.body.mode == "json" and request.body.json:
                try:
                    body = json.loads(request.body.json)
                except:
                    body = {"raw": request.body.json}
            
            # Map auth type
            auth_type_map = {
                "none": AuthType.NONE,
                "basic": AuthType.BASIC,
                "bearer": AuthType.BEARER,
                "apikey": AuthType.API_KEY,
                "oauth2": AuthType.OAUTH2
            }
            auth_type = auth_type_map.get(request.auth.mode, AuthType.NONE)
            
            # Create EndpointContext
            endpoint = EndpointContext(
                name=item.name,
                method=HTTPMethod[request.method],
                url=request.url,
                headers=headers,
                query_params=query_params,
                path_params=path_params,
                body=body,
                body_schema=body_schema,
                auth_type=auth_type,
                auth_config={
                    "username": request.auth.username,
                    "password": request.auth.password,
                    "token": request.auth.token
                } if auth_type != AuthType.NONE else {},
                description=request.docs or item.name,
                tags=item.tags,
                documentation_completeness=1.0  # Assume full completeness initially
            )
            
            endpoints.append(endpoint)
        
        return endpoints
    
    def create_dataset_from_collection(
        self,
        collection_path: str,
        completeness_levels: List[float] = [1.0, 0.75, 0.5, 0.25],
        dataset_name: Optional[str] = None
    ) -> List[DatasetMetadata]:
        """
        Create multiple datasets from a single collection at different completeness levels.
        
        Args:
            collection_path: Path to Bruno collection JSON file
            completeness_levels: List of completeness levels to generate
            dataset_name: Base name for datasets (default: collection name)
            
        Returns:
            List of DatasetMetadata for created datasets
        """
        print(f"\n{'='*60}")
        print(f"CREATING DATASETS FROM: {collection_path}")
        print(f"{'='*60}\n")
        
        # Parse collection
        collection_file = self.collections_dir / collection_path
        with open(collection_file, 'r') as f:
            collection_data = json.load(f)
        
        collection_name = collection_data.get("name", "Unknown Collection")
        if dataset_name is None:
            dataset_name = collection_name.replace(" ", "_").lower()
        
        # Parse endpoints
        parse_result = self.parser.parse_collection_from_json(str(collection_file))
        bruno_items = parse_result.get_all_requests()
        
        # Convert BrunoItems to EndpointContext
        endpoints = self._convert_bruno_items_to_endpoints(bruno_items)
        print(f"✓ Parsed {len(endpoints)} endpoints from collection")
        
        # Create ground truths for full completeness
        ground_truths = self._create_ground_truths_for_endpoints(endpoints)
        print(f"✓ Created {len(ground_truths)} ground truths")
        
        # Save full completeness ground truths
        self.gt_manager.ground_truths = {gt.endpoint_id: gt for gt in ground_truths}
        gt_filename = f"{dataset_name}_gt_full.json"
        self.gt_manager.save_to_file(gt_filename)
        
        # Create datasets at different completeness levels
        datasets = []
        
        for completeness in completeness_levels:
            print(f"\n--- Creating dataset with {completeness*100:.0f}% completeness ---")
            
            # Modify endpoints to target completeness
            modified_endpoints = self._reduce_completeness(
                endpoints, completeness
            )
            
            # Save modified endpoints
            endpoints_filename = f"{dataset_name}_c{int(completeness*100)}_endpoints.json"
            endpoints_path = self.output_dir / endpoints_filename
            self._save_endpoints(modified_endpoints, endpoints_path)
            
            # Create metadata
            metadata = DatasetMetadata(
                name=f"{dataset_name}_c{int(completeness*100)}",
                description=f"{collection_name} at {completeness*100:.0f}% documentation completeness",
                collection_path=str(collection_path),
                completeness_level=completeness,
                num_endpoints=len(modified_endpoints),
                domains=self._identify_domains(endpoints),
                created_at=datetime.utcnow()
            )
            
            # Save metadata
            metadata_filename = f"{dataset_name}_c{int(completeness*100)}_metadata.json"
            self._save_metadata(metadata, self.output_dir / metadata_filename)
            
            datasets.append(metadata)
            
            print(f"✓ Created dataset: {metadata.name}")
            print(f"  Endpoints: {metadata.num_endpoints}")
            print(f"  Domains: {', '.join(metadata.domains)}")
        
        print(f"\n{'='*60}")
        print(f"CREATED {len(datasets)} DATASETS")
        print(f"{'='*60}\n")
        
        return datasets
    
    def _create_ground_truths_for_endpoints(
        self,
        endpoints: List[EndpointContext]
    ) -> List:
        """
        Create ground truth oracles for endpoints.
        
        This is a simplified version. In production, ground truths would be
        manually annotated by experts or extracted from comprehensive API docs.
        """
        from src.validation.oracle_metrics import GroundTruth
        
        ground_truths = []
        
        for endpoint in endpoints:
            # Infer expected responses based on HTTP method
            status_code = self._infer_status_code(endpoint.method)
            response_schema = self._infer_response_schema(endpoint)
            required_headers = self._infer_required_headers(endpoint)
            business_rules = self._infer_business_rules(endpoint)
            
            gt = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=status_code,
                required_headers=required_headers,
                optional_headers={},
                response_schema=response_schema,
                business_rules=business_rules,
                source="auto_generated",
                confidence=0.8,  # Auto-generated, not manually verified
                annotator="RQ1DatasetCreator"
            )
            
            ground_truths.append(gt)
        
        return ground_truths
    
    def _infer_status_code(self, method: str) -> int:
        """Infer expected status code from HTTP method."""
        if method == "POST":
            return 201
        elif method == "DELETE":
            return 204
        else:
            return 200
    
    def _infer_response_schema(self, endpoint: EndpointContext) -> Dict[str, Any]:
        """Infer response schema from endpoint information."""
        # Check if endpoint is a list operation
        if "list" in endpoint.name.lower() or "get all" in endpoint.name.lower():
            return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"}
                    }
                }
            }
        
        # Check if it's a single resource operation
        elif "get" in endpoint.method.lower():
            return {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"}
                },
                "required": ["id"]
            }
        
        # POST/PUT operations
        elif endpoint.method in ["POST", "PUT", "PATCH"]:
            return {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"}
                },
                "required": ["id"]
            }
        
        # DELETE operations
        elif endpoint.method == "DELETE":
            return {"type": "null"}
        
        else:
            return {"type": "object"}
    
    def _infer_required_headers(self, endpoint: EndpointContext) -> Dict[str, str]:
        """Infer required response headers."""
        headers = {
            "Content-Type": "application/json"
        }
        
        if endpoint.method == "POST":
            # POST should include Location header
            headers["Location"] = f"{endpoint.url}/{{id}}"
        
        return headers
    
    def _infer_business_rules(self, endpoint: EndpointContext) -> List[str]:
        """Infer business rules from endpoint."""
        rules = []
        
        # Add rules based on method
        if endpoint.method == "GET":
            if "{id}" in endpoint.url or "/:id" in endpoint.url:
                rules.append("Returns 404 if resource not found")
        
        elif endpoint.method == "POST":
            rules.append("Returns 400 if request body invalid")
            rules.append("Returns 409 if resource already exists")
        
        elif endpoint.method == "PUT":
            rules.append("Returns 404 if resource not found")
            rules.append("Returns 400 if request body invalid")
        
        elif endpoint.method == "DELETE":
            rules.append("Returns 404 if resource not found")
        
        # Add authentication rule if needed
        if "auth" in endpoint.name.lower() or "login" in endpoint.name.lower():
            rules.append("Returns 401 if authentication fails")
        
        return rules
    
    def _reduce_completeness(
        self,
        endpoints: List[EndpointContext],
        target_completeness: float
    ) -> List[EndpointContext]:
        """
        Reduce documentation completeness of endpoints.
        
        Args:
            endpoints: Original endpoints
            target_completeness: Target completeness level (0.0-1.0)
            
        Returns:
            Endpoints with reduced documentation
        """
        if target_completeness >= 1.0:
            return endpoints
        
        modified_endpoints = []
        
        for endpoint in endpoints:
            # Create modified copy
            modified = EndpointContext(
                id=endpoint.id,
                name=endpoint.name,
                method=endpoint.method,
                url=endpoint.url,
                description="",  # Will be modified based on completeness
                documentation_completeness=target_completeness
            )
            
            # Keep description if completeness >= 0.75
            if target_completeness >= 0.75 and endpoint.description:
                modified.description = endpoint.description
            
            # Keep partial description if completeness >= 0.5
            elif target_completeness >= 0.5 and endpoint.description:
                # Take first half of description (by words)
                words = endpoint.description.split()
                half_length = max(1, len(words) // 2)
                modified.description = ' '.join(words[:half_length])
            
            # Keep minimal description if completeness >= 0.25
            elif target_completeness >= 0.25 and endpoint.description:
                # Take first quarter of description (by words) to ensure shorter than 50%
                words = endpoint.description.split()
                quarter_length = max(1, len(words) // 4)
                modified.description = ' '.join(words[:quarter_length])
            
            # Otherwise, no description
            
            modified_endpoints.append(modified)
        
        return modified_endpoints
    
    def _identify_domains(self, endpoints: List[EndpointContext]) -> List[str]:
        """Identify API domains from endpoints."""
        domains = set()
        
        for endpoint in endpoints:
            name_lower = endpoint.name.lower()
            url_lower = endpoint.url.lower()
            
            # Check for common domains
            if any(word in name_lower or word in url_lower for word in ["user", "users"]):
                domains.add("user_management")
            
            if any(word in name_lower or word in url_lower for word in ["auth", "login", "token"]):
                domains.add("authentication")
            
            if any(word in name_lower or word in url_lower for word in ["product", "products"]):
                domains.add("product_catalog")
            
            if any(word in name_lower or word in url_lower for word in ["order", "orders"]):
                domains.add("order_management")
            
            if any(word in name_lower or word in url_lower for word in ["post", "posts", "comment", "comments"]):
                domains.add("content_management")
            
            # Check HTTP method patterns
            if endpoint.method in ["GET", "POST", "PUT", "DELETE"]:
                domains.add("rest_crud")
        
        return sorted(list(domains)) if domains else ["general"]
    
    def _save_endpoints(
        self,
        endpoints: List[EndpointContext],
        output_path: Path
    ):
        """Save endpoints to JSON file."""
        data = {
            "endpoints": [
                {
                    "id": str(ep.id),
                    "name": ep.name,
                    "method": ep.method,
                    "url": ep.url,
                    "description": ep.description,
                    "documentation_completeness": ep.documentation_completeness
                }
                for ep in endpoints
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  Saved endpoints to: {output_path}")
    
    def _save_metadata(
        self,
        metadata: DatasetMetadata,
        output_path: Path
    ):
        """Save dataset metadata to JSON file."""
        data = {
            "name": metadata.name,
            "description": metadata.description,
            "collection_path": metadata.collection_path,
            "completeness_level": metadata.completeness_level,
            "num_endpoints": metadata.num_endpoints,
            "domains": metadata.domains,
            "created_at": metadata.created_at.isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  Saved metadata to: {output_path}")
    
    def create_comprehensive_dataset_suite(self) -> List[DatasetMetadata]:
        """
        Create comprehensive suite of test datasets from all available collections.
        
        Returns:
            List of all created dataset metadata
        """
        print(f"\n{'='*70}")
        print("CREATING COMPREHENSIVE RQ1 TEST DATASET SUITE")
        print(f"{'='*70}\n")
        
        all_datasets = []
        
        # Find all Bruno collections
        collection_files = list(self.collections_dir.rglob("*.json"))
        
        print(f"Found {len(collection_files)} collection files:")
        for cf in collection_files:
            print(f"  - {cf.relative_to(self.collections_dir)}")
        
        # Create datasets from each collection
        for collection_file in collection_files:
            rel_path = collection_file.relative_to(self.collections_dir)
            
            try:
                datasets = self.create_dataset_from_collection(str(rel_path))
                all_datasets.extend(datasets)
            except Exception as e:
                print(f"⚠ Failed to create datasets from {rel_path}: {e}")
        
        # Save suite summary
        self._save_suite_summary(all_datasets)
        
        print(f"\n{'='*70}")
        print(f"DATASET SUITE CREATION COMPLETE")
        print(f"Total Datasets: {len(all_datasets)}")
        print(f"{'='*70}\n")
        
        return all_datasets
    
    def _save_suite_summary(self, datasets: List[DatasetMetadata]):
        """Save summary of entire dataset suite."""
        summary = {
            "created_at": datetime.utcnow().isoformat(),
            "total_datasets": len(datasets),
            "datasets": [
                {
                    "name": ds.name,
                    "description": ds.description,
                    "completeness": ds.completeness_level,
                    "num_endpoints": ds.num_endpoints,
                    "domains": ds.domains
                }
                for ds in datasets
            ]
        }
        
        summary_path = self.output_dir / "dataset_suite_summary.json"
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Saved dataset suite summary to: {summary_path}")


def create_rq1_test_datasets():
    """Create complete RQ1 test dataset suite."""
    creator = RQ1DatasetCreator()
    datasets = creator.create_comprehensive_dataset_suite()
    
    print("\nDataset Suite Summary:")
    print(f"  Total Datasets: {len(datasets)}")
    
    completeness_counts = {}
    for ds in datasets:
        level = ds.completeness_level
        completeness_counts[level] = completeness_counts.get(level, 0) + 1
    
    print("\n  Datasets by Completeness:")
    for level in sorted(completeness_counts.keys(), reverse=True):
        print(f"    {int(level*100)}%: {completeness_counts[level]} datasets")
    
    return datasets


if __name__ == "__main__":
    create_rq1_test_datasets()
