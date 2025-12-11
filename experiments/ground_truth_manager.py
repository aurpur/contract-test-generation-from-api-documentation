"""
Ground Truth Management System

This module provides tools for creating, managing, and persisting ground truth
oracles for RQ1 validation experiments.

Ground truths can be:
1. Manually annotated by experts
2. Extracted from real API responses
3. Imported from existing test suites
4. Generated from OpenAPI/Swagger specifications

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import UUID

from src.shared_context.models import EndpointContext, HTTPMethod
from src.validation.oracle_metrics import GroundTruth


class GroundTruthManager:
    """
    Manages collection and storage of ground truth oracles.
    
    Provides methods to:
    - Create ground truths from various sources
    - Store/load ground truths from JSON
    - Validate ground truths
    - Search and filter ground truths
    """
    
    def __init__(self, storage_dir: Path = Path("experiments/datasets/ground_truths")):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.ground_truths: Dict[UUID, GroundTruth] = {}
    
    def add_ground_truth(
        self,
        endpoint_id: UUID,
        status_code: int,
        required_headers: Dict[str, str],
        response_schema: Dict[str, Any],
        optional_headers: Optional[Dict[str, str]] = None,
        business_rules: Optional[List[str]] = None,
        source: str = "manual",
        confidence: float = 1.0,
        annotator: Optional[str] = None
    ) -> GroundTruth:
        """
        Add a new ground truth oracle.
        
        Args:
            endpoint_id: UUID of the endpoint
            status_code: Expected HTTP status code
            required_headers: Required response headers
            response_schema: JSON schema for response body
            optional_headers: Optional response headers
            business_rules: Business rule validations
            source: Source of ground truth (manual, api_call, spec, etc.)
            confidence: Confidence level (0.0-1.0)
            annotator: Name of person who created ground truth
            
        Returns:
            Created GroundTruth object
        """
        ground_truth = GroundTruth(
            endpoint_id=endpoint_id,
            status_code=status_code,
            required_headers=required_headers,
            optional_headers=optional_headers or {},
            response_schema=response_schema,
            business_rules=business_rules or [],
            source=source,
            confidence=confidence,
            annotator=annotator
        )
        
        self.ground_truths[endpoint_id] = ground_truth
        return ground_truth
    
    def import_from_api_response(
        self,
        endpoint_id: UUID,
        response_data: Dict[str, Any],
        annotator: Optional[str] = None
    ) -> GroundTruth:
        """
        Create ground truth from actual API response.
        
        Args:
            endpoint_id: UUID of the endpoint
            response_data: Dictionary with status, headers, body
            annotator: Name of person who collected response
            
        Returns:
            Created GroundTruth object
        """
        status_code = response_data.get("status", 200)
        headers = response_data.get("headers", {})
        body = response_data.get("body", {})
        
        # Infer schema from response body
        schema = self._infer_schema_from_response(body)
        
        # Separate required and optional headers
        required_headers = {
            k: v for k, v in headers.items()
            if k.lower() in ["content-type", "location"]
        }
        optional_headers = {
            k: v for k, v in headers.items()
            if k not in required_headers
        }
        
        return self.add_ground_truth(
            endpoint_id=endpoint_id,
            status_code=status_code,
            required_headers=required_headers,
            response_schema=schema,
            optional_headers=optional_headers,
            source="api_response",
            confidence=0.9,  # High but not perfect (could be edge case)
            annotator=annotator
        )
    
    def import_from_openapi_spec(
        self,
        endpoint_id: UUID,
        operation_spec: Dict[str, Any],
        annotator: Optional[str] = None
    ) -> GroundTruth:
        """
        Create ground truth from OpenAPI/Swagger specification.
        
        Args:
            endpoint_id: UUID of the endpoint
            operation_spec: OpenAPI operation object
            annotator: Name of person who imported spec
            
        Returns:
            Created GroundTruth object
        """
        # Extract status code (default to 200)
        responses = operation_spec.get("responses", {})
        status_code = int(list(responses.keys())[0]) if responses else 200
        
        # Extract response schema
        response_spec = responses.get(str(status_code), {})
        content = response_spec.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        
        # Extract headers
        headers_spec = response_spec.get("headers", {})
        required_headers = {
            "Content-Type": "application/json"
        }
        
        # Extract business rules from description
        description = operation_spec.get("description", "")
        summary = operation_spec.get("summary", "")
        business_rules = []
        if description:
            business_rules.append(description)
        if summary and summary != description:
            business_rules.append(summary)
        
        return self.add_ground_truth(
            endpoint_id=endpoint_id,
            status_code=status_code,
            required_headers=required_headers,
            response_schema=schema,
            business_rules=business_rules,
            source="openapi_spec",
            confidence=0.95,  # Very reliable but may miss edge cases
            annotator=annotator
        )
    
    def _infer_schema_from_response(self, body: Any) -> Dict[str, Any]:
        """
        Infer JSON schema from response body.
        
        Args:
            body: Response body (dict, list, or primitive)
            
        Returns:
            JSON schema dictionary
        """
        if isinstance(body, dict):
            properties = {}
            required = []
            
            for key, value in body.items():
                properties[key] = self._infer_schema_from_response(value)
                if value is not None:
                    required.append(key)
            
            return {
                "type": "object",
                "properties": properties,
                "required": required
            }
        
        elif isinstance(body, list):
            if body:
                item_schema = self._infer_schema_from_response(body[0])
            else:
                item_schema = {}
            
            return {
                "type": "array",
                "items": item_schema
            }
        
        elif isinstance(body, str):
            return {"type": "string"}
        
        elif isinstance(body, bool):
            return {"type": "boolean"}
        
        elif isinstance(body, int):
            return {"type": "integer"}
        
        elif isinstance(body, float):
            return {"type": "number"}
        
        elif body is None:
            return {"type": "null"}
        
        else:
            return {}
    
    def save_to_file(self, filename: Optional[str] = None):
        """
        Save all ground truths to JSON file.
        
        Args:
            filename: Output filename (default: ground_truths_TIMESTAMP.json)
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ground_truths_{timestamp}.json"
        
        output_path = self.storage_dir / filename
        
        # Convert to serializable format
        data = {
            "created_at": datetime.utcnow().isoformat(),
            "count": len(self.ground_truths),
            "ground_truths": [
                {
                    "endpoint_id": str(endpoint_id),
                    "status_code": gt.status_code,
                    "required_headers": gt.required_headers,
                    "optional_headers": gt.optional_headers,
                    "response_schema": gt.response_schema,
                    "business_rules": gt.business_rules,
                    "source": gt.source,
                    "confidence": gt.confidence,
                    "annotator": gt.annotator,
                    "created_at": gt.created_at.isoformat() if gt.created_at else None
                }
                for endpoint_id, gt in self.ground_truths.items()
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved {len(self.ground_truths)} ground truths to {output_path}")
        return output_path
    
    def load_from_file(self, filename: str) -> int:
        """
        Load ground truths from JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            Number of ground truths loaded
        """
        input_path = self.storage_dir / filename
        
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        count = 0
        for gt_data in data.get("ground_truths", []):
            endpoint_id = UUID(gt_data["endpoint_id"])
            
            ground_truth = GroundTruth(
                endpoint_id=endpoint_id,
                status_code=gt_data["status_code"],
                required_headers=gt_data["required_headers"],
                optional_headers=gt_data.get("optional_headers", {}),
                response_schema=gt_data["response_schema"],
                business_rules=gt_data.get("business_rules", []),
                source=gt_data.get("source", "unknown"),
                confidence=gt_data.get("confidence", 1.0),
                annotator=gt_data.get("annotator"),
                created_at=datetime.fromisoformat(gt_data["created_at"]) if gt_data.get("created_at") else None
            )
            
            self.ground_truths[endpoint_id] = ground_truth
            count += 1
        
        print(f"✓ Loaded {count} ground truths from {input_path}")
        return count
    
    def get_ground_truth(self, endpoint_id: UUID) -> Optional[GroundTruth]:
        """Get ground truth for specific endpoint."""
        return self.ground_truths.get(endpoint_id)
    
    def list_ground_truths(
        self,
        source_filter: Optional[str] = None,
        min_confidence: float = 0.0
    ) -> List[GroundTruth]:
        """
        List ground truths with optional filtering.
        
        Args:
            source_filter: Filter by source (e.g., "manual", "api_response")
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of matching ground truths
        """
        results = []
        
        for gt in self.ground_truths.values():
            if source_filter and gt.source != source_filter:
                continue
            if gt.confidence < min_confidence:
                continue
            results.append(gt)
        
        return results
    
    def validate_ground_truth(self, ground_truth: GroundTruth) -> List[str]:
        """
        Validate a ground truth for completeness and correctness.
        
        Args:
            ground_truth: Ground truth to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check status code
        if not (100 <= ground_truth.status_code < 600):
            errors.append(f"Invalid status code: {ground_truth.status_code}")
        
        # Check required headers
        if not ground_truth.required_headers:
            errors.append("No required headers specified")
        
        if "Content-Type" not in ground_truth.required_headers:
            errors.append("Content-Type header not specified")
        
        # Check response schema
        if not ground_truth.response_schema:
            errors.append("No response schema specified")
        elif "type" not in ground_truth.response_schema:
            errors.append("Response schema missing 'type' field")
        
        # Check confidence
        if not (0.0 <= ground_truth.confidence <= 1.0):
            errors.append(f"Invalid confidence: {ground_truth.confidence}")
        
        return errors
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about ground truths collection."""
        if not self.ground_truths:
            return {"count": 0}
        
        sources = {}
        confidences = []
        
        for gt in self.ground_truths.values():
            sources[gt.source] = sources.get(gt.source, 0) + 1
            confidences.append(gt.confidence)
        
        return {
            "count": len(self.ground_truths),
            "sources": sources,
            "avg_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences)
        }


def create_sample_ground_truth_dataset():
    """Create a sample dataset of ground truths for testing."""
    manager = GroundTruthManager()
    
    # Sample endpoints (would normally come from real collection)
    from experiments.rq1_oracle_validation import create_sample_endpoints
    endpoints = create_sample_endpoints()
    
    for endpoint in endpoints:
        if "Get User by ID" in endpoint.name:
            manager.add_ground_truth(
                endpoint_id=endpoint.id,
                status_code=200,
                required_headers={
                    "Content-Type": "application/json"
                },
                response_schema={
                    "type": "object",
                    "required": ["id", "email", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string", "format": "email"},
                        "name": {"type": "string", "minLength": 1},
                        "created_at": {"type": "string", "format": "date-time"}
                    }
                },
                optional_headers={
                    "Cache-Control": "max-age=3600"
                },
                business_rules=[
                    "Returns 404 if user not found",
                    "User ID must be positive integer"
                ],
                source="manual",
                confidence=1.0,
                annotator="Expert QA Team"
            )
        
        elif "Create User" in endpoint.name:
            manager.add_ground_truth(
                endpoint_id=endpoint.id,
                status_code=201,
                required_headers={
                    "Content-Type": "application/json",
                    "Location": "/api/users/{id}"
                },
                response_schema={
                    "type": "object",
                    "required": ["id", "email", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string"},
                        "name": {"type": "string"}
                    }
                },
                business_rules=[
                    "Returns 409 Conflict if email already exists",
                    "Returns 400 Bad Request if email format invalid",
                    "Email must be unique across all users"
                ],
                source="manual",
                confidence=1.0,
                annotator="Expert QA Team"
            )
        
        elif "List Users" in endpoint.name:
            manager.add_ground_truth(
                endpoint_id=endpoint.id,
                status_code=200,
                required_headers={
                    "Content-Type": "application/json"
                },
                response_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "email", "name"],
                        "properties": {
                            "id": {"type": "integer"},
                            "email": {"type": "string"},
                            "name": {"type": "string"}
                        }
                    }
                },
                optional_headers={
                    "X-Total-Count": "integer",
                    "X-Page-Number": "integer"
                },
                business_rules=[
                    "Default pagination: page=1, limit=10",
                    "Maximum limit=100",
                    "Returns empty array if no users"
                ],
                source="manual",
                confidence=1.0,
                annotator="Expert QA Team"
            )
    
    # Save to file
    output_path = manager.save_to_file("sample_ground_truths.json")
    
    # Print statistics
    stats = manager.get_statistics()
    print(f"\nGround Truth Statistics:")
    print(f"  Total: {stats['count']}")
    print(f"  Sources: {stats['sources']}")
    print(f"  Avg Confidence: {stats['avg_confidence']:.2f}")
    
    return manager


if __name__ == "__main__":
    # Create sample dataset
    create_sample_ground_truth_dataset()
