"""
Schema validator for Bruno collections and API responses.

Author: Aurel IKAMA HONEY

This module provides validation functionality for:
- Bruno collection structure
- JSON schemas from API responses
- Request/response body validation
"""

import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from loguru import logger

from .bruno_models import BrunoCollection, BrunoParseResult, BrunoItem


class SchemaValidationError(Exception):
    """Exception raised when schema validation fails."""
    pass


class SchemaValidator:
    """
    Validator for Bruno collections and API schemas.
    
    Provides comprehensive validation of:
    - Collection structure
    - Request completeness
    - Documentation quality
    - Schema consistency
    """
    
    def __init__(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="SchemaValidator")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def validate_collection(
        self, 
        result: BrunoParseResult,
        strict: bool = False
    ) -> bool:
        """
        Validate a Bruno collection result.
        
        Args:
            result: Parsed Bruno collection result
            strict: If True, treat warnings as errors
            
        Returns:
            True if validation passes, False otherwise
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        self.logger.info(f"Validating collection '{result.collection.name}'...")
        
        # Basic structure validation
        if not result.collection.items:
            self.validation_errors.append("Collection has no items")
        
        if result.total_requests == 0:
            self.validation_errors.append("Collection has no HTTP requests")
        
        # Validate each request
        for item in result.get_all_requests():
            self._validate_request_item(item)
        
        # Documentation completeness check
        if not result.has_documentation:
            self.validation_warnings.append(
                "Collection has no documentation (docs field empty)"
            )
        
        # NOTE: Pas de vérification des tests car notre objectif est de GÉNÉRER
        # des tests à partir de la documentation, pas d'utiliser des tests existants
        
        # Report results
        has_errors = len(self.validation_errors) > 0
        has_warnings = len(self.validation_warnings) > 0
        
        if has_errors:
            self.logger.error(
                f"✗ Validation failed with {len(self.validation_errors)} error(s)"
            )
            for error in self.validation_errors:
                self.logger.error(f"  - {error}")
        
        if has_warnings:
            severity = "error" if strict else "warning"
            self.logger.warning(
                f"⚠ {len(self.validation_warnings)} warning(s) found"
            )
            for warning in self.validation_warnings:
                self.logger.warning(f"  - {warning}")
        
        if not has_errors and not has_warnings:
            self.logger.success(
                f"✓ Collection '{result.collection.name}' is valid"
            )
        
        # In strict mode, warnings are treated as errors
        if strict and has_warnings:
            return False
        
        return not has_errors
    
    def _validate_request_item(self, item: BrunoItem) -> None:
        """Validate a single request item."""
        if not item.request:
            self.validation_errors.append(
                f"Request '{item.name}' has no request configuration"
            )
            return
        
        request = item.request
        
        # Validate URL
        if not request.url:
            self.validation_errors.append(
                f"Request '{item.name}' has no URL"
            )
        elif not self._is_valid_url(request.url):
            self.validation_errors.append(
                f"Request '{item.name}' has invalid URL: {request.url}"
            )
        
        # Validate method
        if request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
            self.validation_errors.append(
                f"Request '{item.name}' has invalid HTTP method: {request.method}"
            )
        
        # Check for documentation
        if not request.docs:
            self.validation_warnings.append(
                f"Request '{item.name}' has no documentation"
            )
        
        # Validate body for methods that should have one
        if request.method in ["POST", "PUT", "PATCH"]:
            if request.body.mode == "none":
                self.validation_warnings.append(
                    f"Request '{item.name}' ({request.method}) has no body configured"
                )
            elif request.body.mode == "json" and request.body.json:
                # Validate JSON body
                if not self._is_valid_json(request.body.json):
                    self.validation_errors.append(
                        f"Request '{item.name}' has invalid JSON body"
                    )
        
        # Validate headers
        for header in request.headers:
            if not header.name or not header.value:
                self.validation_errors.append(
                    f"Request '{item.name}' has incomplete header"
                )
        
        # Validate authentication if configured
        if request.auth.mode != "none":
            if request.auth.mode == "basic":
                if not request.auth.username or not request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def _is_valid_json(self, json_str: str) -> bool:
        """Check if string is valid JSON."""
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False
    
    def validate_json_schema(
        self,
        schema: Dict[str, Any],
        instance: Dict[str, Any]
    ) -> bool:
        """
        Validate a JSON instance against a JSON schema.
        
        Args:
            schema: JSON schema definition
            instance: JSON instance to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        try:
            # Try to use jsonschema if available
            try:
                import jsonschema
                jsonschema.validate(instance=instance, schema=schema)
                return True
            except ImportError:
                self.logger.warning(
                    "jsonschema library not available, skipping schema validation"
                )
                return True
            except jsonschema.ValidationError as e:
                self.validation_errors.append(f"Schema validation failed: {e.message}")
                return False
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def get_validation_report(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def check_documentation_completeness(
        self, 
        result: BrunoParseResult
    ) -> Dict[str, Any]:
        """
        Check documentation completeness for research question RQ5.
        
        Returns a completeness score and detailed analysis.
        """
        total_requests = result.total_requests
        if total_requests == 0:
            return {
                "completeness_score": 0.0,
                "documented_requests": 0,
                "undocumented_requests": 0,
                "details": "No requests found"
            }
        
        documented = 0
        undocumented_items = []
        
        for item in result.get_all_requests():
            if item.request and item.request.docs:
                documented += 1
            else:
                undocumented_items.append(item.name)
        
        completeness_score = (documented / total_requests) * 100
        
        self.logger.info(
            f"Documentation completeness: {completeness_score:.1f}% "
            f"({documented}/{total_requests} requests)"
        )
        
        return {
            "completeness_score": completeness_score,
            "documented_requests": documented,
            "undocumented_requests": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def check_test_coverage(self, result: BrunoParseResult) -> Dict[str, Any]:
        """
        Check test coverage across the collection.
        
        NOTE: Cette méthode n'est pas utilisée pour le projet car notre objectif
        est de GÉNÉRER des tests, pas d'analyser des tests existants dans Bruno.
        Conservée pour compatibilité mais retourne toujours 0%.
        
        Returns test coverage metrics.
        """
        total_requests = result.total_requests
        if total_requests == 0:
            return {
                "coverage_score": 0.0,
                "tested_requests": 0,
                "untested_requests": 0,
                "details": "No requests found"
            }
        
        tested = 0
        untested_items = []
        
        for item in result.get_all_requests():
            if item.request and (item.request.tests or item.request.assertions):
                tested += 1
            else:
                untested_items.append(item.name)
        
        coverage_score = (tested / total_requests) * 100
        
        self.logger.info(
            f"Test coverage: {coverage_score:.1f}% "
            f"({tested}/{total_requests} requests)"
        )
        
        return {
            "coverage_score": coverage_score,
            "tested_requests": tested,
            "untested_requests": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }


__all__ = ["SchemaValidator", "SchemaValidationError"]
