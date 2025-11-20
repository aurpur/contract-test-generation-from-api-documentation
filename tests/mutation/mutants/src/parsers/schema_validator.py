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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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
    
    def xǁSchemaValidatorǁ__init____mutmut_orig(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="SchemaValidator")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_1(self):
        """Initialize the schema validator."""
        self.logger = None
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_2(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component=None)
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_3(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="XXSchemaValidatorXX")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_4(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="schemavalidator")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_5(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="SCHEMAVALIDATOR")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_6(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="SchemaValidator")
        self.validation_errors: List[str] = None
        self.validation_warnings: List[str] = []
    
    def xǁSchemaValidatorǁ__init____mutmut_7(self):
        """Initialize the schema validator."""
        self.logger = logger.bind(component="SchemaValidator")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = None
    
    xǁSchemaValidatorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁ__init____mutmut_1': xǁSchemaValidatorǁ__init____mutmut_1, 
        'xǁSchemaValidatorǁ__init____mutmut_2': xǁSchemaValidatorǁ__init____mutmut_2, 
        'xǁSchemaValidatorǁ__init____mutmut_3': xǁSchemaValidatorǁ__init____mutmut_3, 
        'xǁSchemaValidatorǁ__init____mutmut_4': xǁSchemaValidatorǁ__init____mutmut_4, 
        'xǁSchemaValidatorǁ__init____mutmut_5': xǁSchemaValidatorǁ__init____mutmut_5, 
        'xǁSchemaValidatorǁ__init____mutmut_6': xǁSchemaValidatorǁ__init____mutmut_6, 
        'xǁSchemaValidatorǁ__init____mutmut_7': xǁSchemaValidatorǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSchemaValidatorǁ__init____mutmut_orig)
    xǁSchemaValidatorǁ__init____mutmut_orig.__name__ = 'xǁSchemaValidatorǁ__init__'
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_orig(
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_1(
        self, 
        result: BrunoParseResult,
        strict: bool = True
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_2(
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
        self.validation_errors = None
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_3(
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
        self.validation_warnings = None
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_4(
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
        
        self.logger.info(None)
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_5(
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
        if result.collection.items:
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_6(
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
            self.validation_errors.append(None)
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_7(
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
            self.validation_errors.append("XXCollection has no itemsXX")
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_8(
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
            self.validation_errors.append("collection has no items")
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_9(
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
            self.validation_errors.append("COLLECTION HAS NO ITEMS")
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_10(
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
        
        if result.total_requests != 0:
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_11(
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
        
        if result.total_requests == 1:
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_12(
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
            self.validation_errors.append(None)
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_13(
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
            self.validation_errors.append("XXCollection has no HTTP requestsXX")
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_14(
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
            self.validation_errors.append("collection has no http requests")
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_15(
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
            self.validation_errors.append("COLLECTION HAS NO HTTP REQUESTS")
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_16(
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
            self._validate_request_item(None)
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_17(
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
        if result.has_documentation:
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_18(
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
                None
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_19(
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
                "XXCollection has no documentation (docs field empty)XX"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_20(
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
                "collection has no documentation (docs field empty)"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_21(
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
                "COLLECTION HAS NO DOCUMENTATION (DOCS FIELD EMPTY)"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_22(
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
        has_errors = None
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_23(
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
        has_errors = len(self.validation_errors) >= 0
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_24(
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
        has_errors = len(self.validation_errors) > 1
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_25(
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
        has_warnings = None
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_26(
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
        has_warnings = len(self.validation_warnings) >= 0
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_27(
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
        has_warnings = len(self.validation_warnings) > 1
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_28(
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
                None
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_29(
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
                self.logger.error(None)
        
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_30(
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
            severity = None
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_31(
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
            severity = "XXerrorXX" if strict else "warning"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_32(
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
            severity = "ERROR" if strict else "warning"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_33(
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
            severity = "error" if strict else "XXwarningXX"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_34(
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
            severity = "error" if strict else "WARNING"
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_35(
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
                None
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
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_36(
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
                self.logger.warning(None)
        
        if not has_errors and not has_warnings:
            self.logger.success(
                f"✓ Collection '{result.collection.name}' is valid"
            )
        
        # In strict mode, warnings are treated as errors
        if strict and has_warnings:
            return False
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_37(
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
        
        if not has_errors or not has_warnings:
            self.logger.success(
                f"✓ Collection '{result.collection.name}' is valid"
            )
        
        # In strict mode, warnings are treated as errors
        if strict and has_warnings:
            return False
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_38(
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
        
        if has_errors and not has_warnings:
            self.logger.success(
                f"✓ Collection '{result.collection.name}' is valid"
            )
        
        # In strict mode, warnings are treated as errors
        if strict and has_warnings:
            return False
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_39(
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
        
        if not has_errors and has_warnings:
            self.logger.success(
                f"✓ Collection '{result.collection.name}' is valid"
            )
        
        # In strict mode, warnings are treated as errors
        if strict and has_warnings:
            return False
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_40(
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
                None
            )
        
        # In strict mode, warnings are treated as errors
        if strict and has_warnings:
            return False
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_41(
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
        if strict or has_warnings:
            return False
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_42(
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
            return True
        
        return not has_errors
    
    def xǁSchemaValidatorǁvalidate_collection__mutmut_43(
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
        
        return has_errors
    
    xǁSchemaValidatorǁvalidate_collection__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁvalidate_collection__mutmut_1': xǁSchemaValidatorǁvalidate_collection__mutmut_1, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_2': xǁSchemaValidatorǁvalidate_collection__mutmut_2, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_3': xǁSchemaValidatorǁvalidate_collection__mutmut_3, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_4': xǁSchemaValidatorǁvalidate_collection__mutmut_4, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_5': xǁSchemaValidatorǁvalidate_collection__mutmut_5, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_6': xǁSchemaValidatorǁvalidate_collection__mutmut_6, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_7': xǁSchemaValidatorǁvalidate_collection__mutmut_7, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_8': xǁSchemaValidatorǁvalidate_collection__mutmut_8, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_9': xǁSchemaValidatorǁvalidate_collection__mutmut_9, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_10': xǁSchemaValidatorǁvalidate_collection__mutmut_10, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_11': xǁSchemaValidatorǁvalidate_collection__mutmut_11, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_12': xǁSchemaValidatorǁvalidate_collection__mutmut_12, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_13': xǁSchemaValidatorǁvalidate_collection__mutmut_13, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_14': xǁSchemaValidatorǁvalidate_collection__mutmut_14, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_15': xǁSchemaValidatorǁvalidate_collection__mutmut_15, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_16': xǁSchemaValidatorǁvalidate_collection__mutmut_16, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_17': xǁSchemaValidatorǁvalidate_collection__mutmut_17, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_18': xǁSchemaValidatorǁvalidate_collection__mutmut_18, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_19': xǁSchemaValidatorǁvalidate_collection__mutmut_19, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_20': xǁSchemaValidatorǁvalidate_collection__mutmut_20, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_21': xǁSchemaValidatorǁvalidate_collection__mutmut_21, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_22': xǁSchemaValidatorǁvalidate_collection__mutmut_22, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_23': xǁSchemaValidatorǁvalidate_collection__mutmut_23, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_24': xǁSchemaValidatorǁvalidate_collection__mutmut_24, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_25': xǁSchemaValidatorǁvalidate_collection__mutmut_25, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_26': xǁSchemaValidatorǁvalidate_collection__mutmut_26, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_27': xǁSchemaValidatorǁvalidate_collection__mutmut_27, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_28': xǁSchemaValidatorǁvalidate_collection__mutmut_28, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_29': xǁSchemaValidatorǁvalidate_collection__mutmut_29, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_30': xǁSchemaValidatorǁvalidate_collection__mutmut_30, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_31': xǁSchemaValidatorǁvalidate_collection__mutmut_31, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_32': xǁSchemaValidatorǁvalidate_collection__mutmut_32, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_33': xǁSchemaValidatorǁvalidate_collection__mutmut_33, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_34': xǁSchemaValidatorǁvalidate_collection__mutmut_34, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_35': xǁSchemaValidatorǁvalidate_collection__mutmut_35, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_36': xǁSchemaValidatorǁvalidate_collection__mutmut_36, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_37': xǁSchemaValidatorǁvalidate_collection__mutmut_37, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_38': xǁSchemaValidatorǁvalidate_collection__mutmut_38, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_39': xǁSchemaValidatorǁvalidate_collection__mutmut_39, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_40': xǁSchemaValidatorǁvalidate_collection__mutmut_40, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_41': xǁSchemaValidatorǁvalidate_collection__mutmut_41, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_42': xǁSchemaValidatorǁvalidate_collection__mutmut_42, 
        'xǁSchemaValidatorǁvalidate_collection__mutmut_43': xǁSchemaValidatorǁvalidate_collection__mutmut_43
    }
    
    def validate_collection(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁvalidate_collection__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁvalidate_collection__mutmut_mutants"), args, kwargs, self)
        return result 
    
    validate_collection.__signature__ = _mutmut_signature(xǁSchemaValidatorǁvalidate_collection__mutmut_orig)
    xǁSchemaValidatorǁvalidate_collection__mutmut_orig.__name__ = 'xǁSchemaValidatorǁvalidate_collection'
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_orig(self, item: BrunoItem) -> None:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_1(self, item: BrunoItem) -> None:
        """Validate a single request item."""
        if item.request:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_2(self, item: BrunoItem) -> None:
        """Validate a single request item."""
        if not item.request:
            self.validation_errors.append(
                None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_3(self, item: BrunoItem) -> None:
        """Validate a single request item."""
        if not item.request:
            self.validation_errors.append(
                f"Request '{item.name}' has no request configuration"
            )
            return
        
        request = None
        
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_4(self, item: BrunoItem) -> None:
        """Validate a single request item."""
        if not item.request:
            self.validation_errors.append(
                f"Request '{item.name}' has no request configuration"
            )
            return
        
        request = item.request
        
        # Validate URL
        if request.url:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_5(self, item: BrunoItem) -> None:
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
                None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_6(self, item: BrunoItem) -> None:
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
        elif self._is_valid_url(request.url):
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_7(self, item: BrunoItem) -> None:
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
        elif not self._is_valid_url(None):
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_8(self, item: BrunoItem) -> None:
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
                None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_9(self, item: BrunoItem) -> None:
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
        if request.method in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_10(self, item: BrunoItem) -> None:
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
        if request.method not in ["XXGETXX", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_11(self, item: BrunoItem) -> None:
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
        if request.method not in ["get", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_12(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "XXPOSTXX", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_13(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "post", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_14(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "XXPUTXX", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_15(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "put", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_16(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "XXDELETEXX", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_17(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "delete", "PATCH", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_18(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "DELETE", "XXPATCHXX", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_19(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "DELETE", "patch", "HEAD", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_20(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "XXHEADXX", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_21(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "head", "OPTIONS"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_22(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "XXOPTIONSXX"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_23(self, item: BrunoItem) -> None:
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
        if request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "options"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_24(self, item: BrunoItem) -> None:
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
                None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_25(self, item: BrunoItem) -> None:
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
        if request.docs:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_26(self, item: BrunoItem) -> None:
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
                None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_27(self, item: BrunoItem) -> None:
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
        if request.method not in ["POST", "PUT", "PATCH"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_28(self, item: BrunoItem) -> None:
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
        if request.method in ["XXPOSTXX", "PUT", "PATCH"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_29(self, item: BrunoItem) -> None:
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
        if request.method in ["post", "PUT", "PATCH"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_30(self, item: BrunoItem) -> None:
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
        if request.method in ["POST", "XXPUTXX", "PATCH"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_31(self, item: BrunoItem) -> None:
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
        if request.method in ["POST", "put", "PATCH"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_32(self, item: BrunoItem) -> None:
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
        if request.method in ["POST", "PUT", "XXPATCHXX"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_33(self, item: BrunoItem) -> None:
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
        if request.method in ["POST", "PUT", "patch"]:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_34(self, item: BrunoItem) -> None:
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
            if request.body.mode != "none":
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_35(self, item: BrunoItem) -> None:
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
            if request.body.mode == "XXnoneXX":
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_36(self, item: BrunoItem) -> None:
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
            if request.body.mode == "NONE":
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_37(self, item: BrunoItem) -> None:
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
                    None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_38(self, item: BrunoItem) -> None:
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
            elif request.body.mode == "json" or request.body.json:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_39(self, item: BrunoItem) -> None:
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
            elif request.body.mode != "json" and request.body.json:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_40(self, item: BrunoItem) -> None:
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
            elif request.body.mode == "XXjsonXX" and request.body.json:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_41(self, item: BrunoItem) -> None:
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
            elif request.body.mode == "JSON" and request.body.json:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_42(self, item: BrunoItem) -> None:
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
                if self._is_valid_json(request.body.json):
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_43(self, item: BrunoItem) -> None:
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
                if not self._is_valid_json(None):
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_44(self, item: BrunoItem) -> None:
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
                        None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_45(self, item: BrunoItem) -> None:
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
            if not header.name and not header.value:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_46(self, item: BrunoItem) -> None:
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
            if header.name or not header.value:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_47(self, item: BrunoItem) -> None:
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
            if not header.name or header.value:
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_48(self, item: BrunoItem) -> None:
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
                    None
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_49(self, item: BrunoItem) -> None:
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
        if request.auth.mode == "none":
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_50(self, item: BrunoItem) -> None:
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
        if request.auth.mode != "XXnoneXX":
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_51(self, item: BrunoItem) -> None:
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
        if request.auth.mode != "NONE":
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
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_52(self, item: BrunoItem) -> None:
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
            if request.auth.mode != "basic":
                if not request.auth.username or not request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_53(self, item: BrunoItem) -> None:
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
            if request.auth.mode == "XXbasicXX":
                if not request.auth.username or not request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_54(self, item: BrunoItem) -> None:
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
            if request.auth.mode == "BASIC":
                if not request.auth.username or not request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_55(self, item: BrunoItem) -> None:
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
                if not request.auth.username and not request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_56(self, item: BrunoItem) -> None:
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
                if request.auth.username or not request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_57(self, item: BrunoItem) -> None:
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
                if not request.auth.username or request.auth.password:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete basic auth"
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_58(self, item: BrunoItem) -> None:
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
                        None
                    )
            elif request.auth.mode == "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_59(self, item: BrunoItem) -> None:
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
            elif request.auth.mode != "bearer":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_60(self, item: BrunoItem) -> None:
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
            elif request.auth.mode == "XXbearerXX":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_61(self, item: BrunoItem) -> None:
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
            elif request.auth.mode == "BEARER":
                if not request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_62(self, item: BrunoItem) -> None:
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
                if request.auth.token:
                    self.validation_errors.append(
                        f"Request '{item.name}' has incomplete bearer auth"
                    )
    
    def xǁSchemaValidatorǁ_validate_request_item__mutmut_63(self, item: BrunoItem) -> None:
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
                        None
                    )
    
    xǁSchemaValidatorǁ_validate_request_item__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁ_validate_request_item__mutmut_1': xǁSchemaValidatorǁ_validate_request_item__mutmut_1, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_2': xǁSchemaValidatorǁ_validate_request_item__mutmut_2, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_3': xǁSchemaValidatorǁ_validate_request_item__mutmut_3, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_4': xǁSchemaValidatorǁ_validate_request_item__mutmut_4, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_5': xǁSchemaValidatorǁ_validate_request_item__mutmut_5, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_6': xǁSchemaValidatorǁ_validate_request_item__mutmut_6, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_7': xǁSchemaValidatorǁ_validate_request_item__mutmut_7, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_8': xǁSchemaValidatorǁ_validate_request_item__mutmut_8, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_9': xǁSchemaValidatorǁ_validate_request_item__mutmut_9, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_10': xǁSchemaValidatorǁ_validate_request_item__mutmut_10, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_11': xǁSchemaValidatorǁ_validate_request_item__mutmut_11, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_12': xǁSchemaValidatorǁ_validate_request_item__mutmut_12, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_13': xǁSchemaValidatorǁ_validate_request_item__mutmut_13, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_14': xǁSchemaValidatorǁ_validate_request_item__mutmut_14, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_15': xǁSchemaValidatorǁ_validate_request_item__mutmut_15, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_16': xǁSchemaValidatorǁ_validate_request_item__mutmut_16, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_17': xǁSchemaValidatorǁ_validate_request_item__mutmut_17, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_18': xǁSchemaValidatorǁ_validate_request_item__mutmut_18, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_19': xǁSchemaValidatorǁ_validate_request_item__mutmut_19, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_20': xǁSchemaValidatorǁ_validate_request_item__mutmut_20, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_21': xǁSchemaValidatorǁ_validate_request_item__mutmut_21, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_22': xǁSchemaValidatorǁ_validate_request_item__mutmut_22, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_23': xǁSchemaValidatorǁ_validate_request_item__mutmut_23, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_24': xǁSchemaValidatorǁ_validate_request_item__mutmut_24, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_25': xǁSchemaValidatorǁ_validate_request_item__mutmut_25, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_26': xǁSchemaValidatorǁ_validate_request_item__mutmut_26, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_27': xǁSchemaValidatorǁ_validate_request_item__mutmut_27, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_28': xǁSchemaValidatorǁ_validate_request_item__mutmut_28, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_29': xǁSchemaValidatorǁ_validate_request_item__mutmut_29, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_30': xǁSchemaValidatorǁ_validate_request_item__mutmut_30, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_31': xǁSchemaValidatorǁ_validate_request_item__mutmut_31, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_32': xǁSchemaValidatorǁ_validate_request_item__mutmut_32, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_33': xǁSchemaValidatorǁ_validate_request_item__mutmut_33, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_34': xǁSchemaValidatorǁ_validate_request_item__mutmut_34, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_35': xǁSchemaValidatorǁ_validate_request_item__mutmut_35, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_36': xǁSchemaValidatorǁ_validate_request_item__mutmut_36, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_37': xǁSchemaValidatorǁ_validate_request_item__mutmut_37, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_38': xǁSchemaValidatorǁ_validate_request_item__mutmut_38, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_39': xǁSchemaValidatorǁ_validate_request_item__mutmut_39, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_40': xǁSchemaValidatorǁ_validate_request_item__mutmut_40, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_41': xǁSchemaValidatorǁ_validate_request_item__mutmut_41, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_42': xǁSchemaValidatorǁ_validate_request_item__mutmut_42, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_43': xǁSchemaValidatorǁ_validate_request_item__mutmut_43, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_44': xǁSchemaValidatorǁ_validate_request_item__mutmut_44, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_45': xǁSchemaValidatorǁ_validate_request_item__mutmut_45, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_46': xǁSchemaValidatorǁ_validate_request_item__mutmut_46, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_47': xǁSchemaValidatorǁ_validate_request_item__mutmut_47, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_48': xǁSchemaValidatorǁ_validate_request_item__mutmut_48, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_49': xǁSchemaValidatorǁ_validate_request_item__mutmut_49, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_50': xǁSchemaValidatorǁ_validate_request_item__mutmut_50, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_51': xǁSchemaValidatorǁ_validate_request_item__mutmut_51, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_52': xǁSchemaValidatorǁ_validate_request_item__mutmut_52, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_53': xǁSchemaValidatorǁ_validate_request_item__mutmut_53, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_54': xǁSchemaValidatorǁ_validate_request_item__mutmut_54, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_55': xǁSchemaValidatorǁ_validate_request_item__mutmut_55, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_56': xǁSchemaValidatorǁ_validate_request_item__mutmut_56, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_57': xǁSchemaValidatorǁ_validate_request_item__mutmut_57, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_58': xǁSchemaValidatorǁ_validate_request_item__mutmut_58, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_59': xǁSchemaValidatorǁ_validate_request_item__mutmut_59, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_60': xǁSchemaValidatorǁ_validate_request_item__mutmut_60, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_61': xǁSchemaValidatorǁ_validate_request_item__mutmut_61, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_62': xǁSchemaValidatorǁ_validate_request_item__mutmut_62, 
        'xǁSchemaValidatorǁ_validate_request_item__mutmut_63': xǁSchemaValidatorǁ_validate_request_item__mutmut_63
    }
    
    def _validate_request_item(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁ_validate_request_item__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁ_validate_request_item__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _validate_request_item.__signature__ = _mutmut_signature(xǁSchemaValidatorǁ_validate_request_item__mutmut_orig)
    xǁSchemaValidatorǁ_validate_request_item__mutmut_orig.__name__ = 'xǁSchemaValidatorǁ_validate_request_item'
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_orig(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_1(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") and url.startswith("${"):
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_2(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith(None) or url.startswith("${"):
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_3(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("XX{{XX") or url.startswith("${"):
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_4(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith(None):
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_5(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("XX${XX"):
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_6(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return False
        
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_7(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = None
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_8(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            None, re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_9(self, url: str) -> bool:
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
            r'(?:/?|[/?]\S+)$', None)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_10(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_11(self, url: str) -> bool:
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
            r'(?:/?|[/?]\S+)$', )
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_12(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'XX^https?://XX'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_13(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_14(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'^HTTPS?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_15(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'XX(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|XX'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_16(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_17(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_18(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'XXlocalhost|XX'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_19(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_20(self, url: str) -> bool:
        """Check if URL is valid."""
        # Allow environment variables in URLs
        if url.startswith("{{") or url.startswith("${"):
            return True
        
        # Basic URL validation
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'LOCALHOST|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_21(self, url: str) -> bool:
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
            r'XX\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})XX'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_22(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_23(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_24(self, url: str) -> bool:
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
            r'XX(?::\d+)?XX'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_25(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_26(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_27(self, url: str) -> bool:
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
            r'XX(?:/?|[/?]\S+)$XX', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_28(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_29(self, url: str) -> bool:
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
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_30(self, url: str) -> bool:
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
        
        return bool(None)
    
    def xǁSchemaValidatorǁ_is_valid_url__mutmut_31(self, url: str) -> bool:
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
        
        return bool(url_pattern.match(None))
    
    xǁSchemaValidatorǁ_is_valid_url__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁ_is_valid_url__mutmut_1': xǁSchemaValidatorǁ_is_valid_url__mutmut_1, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_2': xǁSchemaValidatorǁ_is_valid_url__mutmut_2, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_3': xǁSchemaValidatorǁ_is_valid_url__mutmut_3, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_4': xǁSchemaValidatorǁ_is_valid_url__mutmut_4, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_5': xǁSchemaValidatorǁ_is_valid_url__mutmut_5, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_6': xǁSchemaValidatorǁ_is_valid_url__mutmut_6, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_7': xǁSchemaValidatorǁ_is_valid_url__mutmut_7, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_8': xǁSchemaValidatorǁ_is_valid_url__mutmut_8, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_9': xǁSchemaValidatorǁ_is_valid_url__mutmut_9, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_10': xǁSchemaValidatorǁ_is_valid_url__mutmut_10, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_11': xǁSchemaValidatorǁ_is_valid_url__mutmut_11, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_12': xǁSchemaValidatorǁ_is_valid_url__mutmut_12, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_13': xǁSchemaValidatorǁ_is_valid_url__mutmut_13, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_14': xǁSchemaValidatorǁ_is_valid_url__mutmut_14, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_15': xǁSchemaValidatorǁ_is_valid_url__mutmut_15, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_16': xǁSchemaValidatorǁ_is_valid_url__mutmut_16, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_17': xǁSchemaValidatorǁ_is_valid_url__mutmut_17, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_18': xǁSchemaValidatorǁ_is_valid_url__mutmut_18, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_19': xǁSchemaValidatorǁ_is_valid_url__mutmut_19, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_20': xǁSchemaValidatorǁ_is_valid_url__mutmut_20, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_21': xǁSchemaValidatorǁ_is_valid_url__mutmut_21, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_22': xǁSchemaValidatorǁ_is_valid_url__mutmut_22, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_23': xǁSchemaValidatorǁ_is_valid_url__mutmut_23, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_24': xǁSchemaValidatorǁ_is_valid_url__mutmut_24, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_25': xǁSchemaValidatorǁ_is_valid_url__mutmut_25, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_26': xǁSchemaValidatorǁ_is_valid_url__mutmut_26, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_27': xǁSchemaValidatorǁ_is_valid_url__mutmut_27, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_28': xǁSchemaValidatorǁ_is_valid_url__mutmut_28, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_29': xǁSchemaValidatorǁ_is_valid_url__mutmut_29, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_30': xǁSchemaValidatorǁ_is_valid_url__mutmut_30, 
        'xǁSchemaValidatorǁ_is_valid_url__mutmut_31': xǁSchemaValidatorǁ_is_valid_url__mutmut_31
    }
    
    def _is_valid_url(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁ_is_valid_url__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁ_is_valid_url__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _is_valid_url.__signature__ = _mutmut_signature(xǁSchemaValidatorǁ_is_valid_url__mutmut_orig)
    xǁSchemaValidatorǁ_is_valid_url__mutmut_orig.__name__ = 'xǁSchemaValidatorǁ_is_valid_url'
    
    def xǁSchemaValidatorǁ_is_valid_json__mutmut_orig(self, json_str: str) -> bool:
        """Check if string is valid JSON."""
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False
    
    def xǁSchemaValidatorǁ_is_valid_json__mutmut_1(self, json_str: str) -> bool:
        """Check if string is valid JSON."""
        try:
            json.loads(None)
            return True
        except json.JSONDecodeError:
            return False
    
    def xǁSchemaValidatorǁ_is_valid_json__mutmut_2(self, json_str: str) -> bool:
        """Check if string is valid JSON."""
        try:
            json.loads(json_str)
            return False
        except json.JSONDecodeError:
            return False
    
    def xǁSchemaValidatorǁ_is_valid_json__mutmut_3(self, json_str: str) -> bool:
        """Check if string is valid JSON."""
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return True
    
    xǁSchemaValidatorǁ_is_valid_json__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁ_is_valid_json__mutmut_1': xǁSchemaValidatorǁ_is_valid_json__mutmut_1, 
        'xǁSchemaValidatorǁ_is_valid_json__mutmut_2': xǁSchemaValidatorǁ_is_valid_json__mutmut_2, 
        'xǁSchemaValidatorǁ_is_valid_json__mutmut_3': xǁSchemaValidatorǁ_is_valid_json__mutmut_3
    }
    
    def _is_valid_json(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁ_is_valid_json__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁ_is_valid_json__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _is_valid_json.__signature__ = _mutmut_signature(xǁSchemaValidatorǁ_is_valid_json__mutmut_orig)
    xǁSchemaValidatorǁ_is_valid_json__mutmut_orig.__name__ = 'xǁSchemaValidatorǁ_is_valid_json'
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_orig(
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
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_1(
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
                jsonschema.validate(instance=None, schema=schema)
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
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_2(
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
                jsonschema.validate(instance=instance, schema=None)
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
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_3(
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
                jsonschema.validate(schema=schema)
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
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_4(
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
                jsonschema.validate(instance=instance, )
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
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_5(
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
                return False
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
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_6(
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
                    None
                )
                return True
            except jsonschema.ValidationError as e:
                self.validation_errors.append(f"Schema validation failed: {e.message}")
                return False
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_7(
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
                    "XXjsonschema library not available, skipping schema validationXX"
                )
                return True
            except jsonschema.ValidationError as e:
                self.validation_errors.append(f"Schema validation failed: {e.message}")
                return False
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_8(
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
                    "JSONSCHEMA LIBRARY NOT AVAILABLE, SKIPPING SCHEMA VALIDATION"
                )
                return True
            except jsonschema.ValidationError as e:
                self.validation_errors.append(f"Schema validation failed: {e.message}")
                return False
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_9(
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
                return False
            except jsonschema.ValidationError as e:
                self.validation_errors.append(f"Schema validation failed: {e.message}")
                return False
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_10(
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
                self.validation_errors.append(None)
                return False
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_11(
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
                return True
        except Exception as e:
            self.validation_errors.append(f"Schema validation error: {str(e)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_12(
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
            self.validation_errors.append(None)
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_13(
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
            self.validation_errors.append(f"Schema validation error: {str(None)}")
            return False
    
    def xǁSchemaValidatorǁvalidate_json_schema__mutmut_14(
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
            return True
    
    xǁSchemaValidatorǁvalidate_json_schema__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁvalidate_json_schema__mutmut_1': xǁSchemaValidatorǁvalidate_json_schema__mutmut_1, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_2': xǁSchemaValidatorǁvalidate_json_schema__mutmut_2, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_3': xǁSchemaValidatorǁvalidate_json_schema__mutmut_3, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_4': xǁSchemaValidatorǁvalidate_json_schema__mutmut_4, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_5': xǁSchemaValidatorǁvalidate_json_schema__mutmut_5, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_6': xǁSchemaValidatorǁvalidate_json_schema__mutmut_6, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_7': xǁSchemaValidatorǁvalidate_json_schema__mutmut_7, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_8': xǁSchemaValidatorǁvalidate_json_schema__mutmut_8, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_9': xǁSchemaValidatorǁvalidate_json_schema__mutmut_9, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_10': xǁSchemaValidatorǁvalidate_json_schema__mutmut_10, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_11': xǁSchemaValidatorǁvalidate_json_schema__mutmut_11, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_12': xǁSchemaValidatorǁvalidate_json_schema__mutmut_12, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_13': xǁSchemaValidatorǁvalidate_json_schema__mutmut_13, 
        'xǁSchemaValidatorǁvalidate_json_schema__mutmut_14': xǁSchemaValidatorǁvalidate_json_schema__mutmut_14
    }
    
    def validate_json_schema(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁvalidate_json_schema__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁvalidate_json_schema__mutmut_mutants"), args, kwargs, self)
        return result 
    
    validate_json_schema.__signature__ = _mutmut_signature(xǁSchemaValidatorǁvalidate_json_schema__mutmut_orig)
    xǁSchemaValidatorǁvalidate_json_schema__mutmut_orig.__name__ = 'xǁSchemaValidatorǁvalidate_json_schema'
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_orig(self) -> Dict[str, Any]:
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
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_1(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "XXis_validXX": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_2(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "IS_VALID": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_3(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) != 0,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_4(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 1,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_5(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "XXerrorsXX": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_6(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "ERRORS": self.validation_errors,
            "warnings": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_7(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "XXwarningsXX": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_8(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "WARNINGS": self.validation_warnings,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_9(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "XXerror_countXX": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_10(self) -> Dict[str, Any]:
        """
        Get a detailed validation report.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "ERROR_COUNT": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_11(self) -> Dict[str, Any]:
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
            "XXwarning_countXX": len(self.validation_warnings),
        }
    
    def xǁSchemaValidatorǁget_validation_report__mutmut_12(self) -> Dict[str, Any]:
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
            "WARNING_COUNT": len(self.validation_warnings),
        }
    
    xǁSchemaValidatorǁget_validation_report__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁget_validation_report__mutmut_1': xǁSchemaValidatorǁget_validation_report__mutmut_1, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_2': xǁSchemaValidatorǁget_validation_report__mutmut_2, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_3': xǁSchemaValidatorǁget_validation_report__mutmut_3, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_4': xǁSchemaValidatorǁget_validation_report__mutmut_4, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_5': xǁSchemaValidatorǁget_validation_report__mutmut_5, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_6': xǁSchemaValidatorǁget_validation_report__mutmut_6, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_7': xǁSchemaValidatorǁget_validation_report__mutmut_7, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_8': xǁSchemaValidatorǁget_validation_report__mutmut_8, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_9': xǁSchemaValidatorǁget_validation_report__mutmut_9, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_10': xǁSchemaValidatorǁget_validation_report__mutmut_10, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_11': xǁSchemaValidatorǁget_validation_report__mutmut_11, 
        'xǁSchemaValidatorǁget_validation_report__mutmut_12': xǁSchemaValidatorǁget_validation_report__mutmut_12
    }
    
    def get_validation_report(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁget_validation_report__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁget_validation_report__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_validation_report.__signature__ = _mutmut_signature(xǁSchemaValidatorǁget_validation_report__mutmut_orig)
    xǁSchemaValidatorǁget_validation_report__mutmut_orig.__name__ = 'xǁSchemaValidatorǁget_validation_report'
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_orig(
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_1(
        self, 
        result: BrunoParseResult
    ) -> Dict[str, Any]:
        """
        Check documentation completeness for research question RQ5.
        
        Returns a completeness score and detailed analysis.
        """
        total_requests = None
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_2(
        self, 
        result: BrunoParseResult
    ) -> Dict[str, Any]:
        """
        Check documentation completeness for research question RQ5.
        
        Returns a completeness score and detailed analysis.
        """
        total_requests = result.total_requests
        if total_requests != 0:
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_3(
        self, 
        result: BrunoParseResult
    ) -> Dict[str, Any]:
        """
        Check documentation completeness for research question RQ5.
        
        Returns a completeness score and detailed analysis.
        """
        total_requests = result.total_requests
        if total_requests == 1:
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_4(
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
                "XXcompleteness_scoreXX": 0.0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_5(
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
                "COMPLETENESS_SCORE": 0.0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_6(
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
                "completeness_score": 1.0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_7(
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
                "XXdocumented_requestsXX": 0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_8(
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
                "DOCUMENTED_REQUESTS": 0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_9(
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
                "documented_requests": 1,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_10(
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
                "XXundocumented_requestsXX": 0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_11(
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
                "UNDOCUMENTED_REQUESTS": 0,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_12(
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
                "undocumented_requests": 1,
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_13(
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
                "XXdetailsXX": "No requests found"
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_14(
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
                "DETAILS": "No requests found"
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_15(
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
                "details": "XXNo requests foundXX"
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_16(
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
                "details": "no requests found"
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_17(
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
                "details": "NO REQUESTS FOUND"
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_18(
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
        
        documented = None
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_19(
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
        
        documented = 1
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_20(
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
        undocumented_items = None
        
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_21(
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
            if item.request or item.request.docs:
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_22(
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
                documented = 1
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_23(
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
                documented -= 1
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_24(
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
                documented += 2
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_25(
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
                undocumented_items.append(None)
        
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_26(
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
        
        completeness_score = None
        
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_27(
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
        
        completeness_score = (documented / total_requests) / 100
        
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_28(
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
        
        completeness_score = (documented * total_requests) * 100
        
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_29(
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
        
        completeness_score = (documented / total_requests) * 101
        
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
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_30(
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
            None
        )
        
        return {
            "completeness_score": completeness_score,
            "documented_requests": documented,
            "undocumented_requests": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_31(
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
            "XXcompleteness_scoreXX": completeness_score,
            "documented_requests": documented,
            "undocumented_requests": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_32(
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
            "COMPLETENESS_SCORE": completeness_score,
            "documented_requests": documented,
            "undocumented_requests": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_33(
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
            "XXdocumented_requestsXX": documented,
            "undocumented_requests": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_34(
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
            "DOCUMENTED_REQUESTS": documented,
            "undocumented_requests": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_35(
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
            "XXundocumented_requestsXX": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_36(
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
            "UNDOCUMENTED_REQUESTS": total_requests - documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_37(
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
            "undocumented_requests": total_requests + documented,
            "total_requests": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_38(
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
            "XXtotal_requestsXX": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_39(
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
            "TOTAL_REQUESTS": total_requests,
            "undocumented_items": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_40(
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
            "XXundocumented_itemsXX": undocumented_items,
        }
    
    def xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_41(
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
            "UNDOCUMENTED_ITEMS": undocumented_items,
        }
    
    xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_1': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_1, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_2': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_2, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_3': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_3, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_4': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_4, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_5': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_5, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_6': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_6, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_7': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_7, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_8': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_8, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_9': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_9, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_10': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_10, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_11': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_11, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_12': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_12, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_13': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_13, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_14': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_14, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_15': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_15, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_16': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_16, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_17': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_17, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_18': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_18, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_19': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_19, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_20': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_20, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_21': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_21, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_22': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_22, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_23': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_23, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_24': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_24, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_25': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_25, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_26': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_26, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_27': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_27, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_28': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_28, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_29': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_29, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_30': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_30, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_31': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_31, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_32': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_32, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_33': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_33, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_34': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_34, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_35': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_35, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_36': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_36, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_37': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_37, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_38': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_38, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_39': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_39, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_40': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_40, 
        'xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_41': xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_41
    }
    
    def check_documentation_completeness(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check_documentation_completeness.__signature__ = _mutmut_signature(xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_orig)
    xǁSchemaValidatorǁcheck_documentation_completeness__mutmut_orig.__name__ = 'xǁSchemaValidatorǁcheck_documentation_completeness'
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_orig(self, result: BrunoParseResult) -> Dict[str, Any]:
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_1(self, result: BrunoParseResult) -> Dict[str, Any]:
        """
        Check test coverage across the collection.
        
        NOTE: Cette méthode n'est pas utilisée pour le projet car notre objectif
        est de GÉNÉRER des tests, pas d'analyser des tests existants dans Bruno.
        Conservée pour compatibilité mais retourne toujours 0%.
        
        Returns test coverage metrics.
        """
        total_requests = None
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_2(self, result: BrunoParseResult) -> Dict[str, Any]:
        """
        Check test coverage across the collection.
        
        NOTE: Cette méthode n'est pas utilisée pour le projet car notre objectif
        est de GÉNÉRER des tests, pas d'analyser des tests existants dans Bruno.
        Conservée pour compatibilité mais retourne toujours 0%.
        
        Returns test coverage metrics.
        """
        total_requests = result.total_requests
        if total_requests != 0:
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_3(self, result: BrunoParseResult) -> Dict[str, Any]:
        """
        Check test coverage across the collection.
        
        NOTE: Cette méthode n'est pas utilisée pour le projet car notre objectif
        est de GÉNÉRER des tests, pas d'analyser des tests existants dans Bruno.
        Conservée pour compatibilité mais retourne toujours 0%.
        
        Returns test coverage metrics.
        """
        total_requests = result.total_requests
        if total_requests == 1:
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_4(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "XXcoverage_scoreXX": 0.0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_5(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "COVERAGE_SCORE": 0.0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_6(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "coverage_score": 1.0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_7(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "XXtested_requestsXX": 0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_8(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "TESTED_REQUESTS": 0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_9(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "tested_requests": 1,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_10(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "XXuntested_requestsXX": 0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_11(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "UNTESTED_REQUESTS": 0,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_12(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "untested_requests": 1,
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_13(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "XXdetailsXX": "No requests found"
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_14(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "DETAILS": "No requests found"
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_15(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "details": "XXNo requests foundXX"
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_16(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "details": "no requests found"
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_17(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                "details": "NO REQUESTS FOUND"
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_18(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        
        tested = None
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_19(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        
        tested = 1
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_20(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        untested_items = None
        
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_21(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            if item.request or (item.request.tests or item.request.assertions):
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_22(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            if item.request and (item.request.tests and item.request.assertions):
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_23(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                tested = 1
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_24(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                tested -= 1
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_25(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                tested += 2
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_26(self, result: BrunoParseResult) -> Dict[str, Any]:
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
                untested_items.append(None)
        
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_27(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        
        coverage_score = None
        
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_28(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        
        coverage_score = (tested / total_requests) / 100
        
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_29(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        
        coverage_score = (tested * total_requests) * 100
        
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_30(self, result: BrunoParseResult) -> Dict[str, Any]:
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
        
        coverage_score = (tested / total_requests) * 101
        
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
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_31(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            None
        )
        
        return {
            "coverage_score": coverage_score,
            "tested_requests": tested,
            "untested_requests": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_32(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "XXcoverage_scoreXX": coverage_score,
            "tested_requests": tested,
            "untested_requests": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_33(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "COVERAGE_SCORE": coverage_score,
            "tested_requests": tested,
            "untested_requests": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_34(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "XXtested_requestsXX": tested,
            "untested_requests": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_35(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "TESTED_REQUESTS": tested,
            "untested_requests": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_36(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "XXuntested_requestsXX": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_37(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "UNTESTED_REQUESTS": total_requests - tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_38(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "untested_requests": total_requests + tested,
            "total_requests": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_39(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "XXtotal_requestsXX": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_40(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "TOTAL_REQUESTS": total_requests,
            "untested_items": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_41(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "XXuntested_itemsXX": untested_items,
        }
    
    def xǁSchemaValidatorǁcheck_test_coverage__mutmut_42(self, result: BrunoParseResult) -> Dict[str, Any]:
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
            "UNTESTED_ITEMS": untested_items,
        }
    
    xǁSchemaValidatorǁcheck_test_coverage__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSchemaValidatorǁcheck_test_coverage__mutmut_1': xǁSchemaValidatorǁcheck_test_coverage__mutmut_1, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_2': xǁSchemaValidatorǁcheck_test_coverage__mutmut_2, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_3': xǁSchemaValidatorǁcheck_test_coverage__mutmut_3, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_4': xǁSchemaValidatorǁcheck_test_coverage__mutmut_4, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_5': xǁSchemaValidatorǁcheck_test_coverage__mutmut_5, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_6': xǁSchemaValidatorǁcheck_test_coverage__mutmut_6, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_7': xǁSchemaValidatorǁcheck_test_coverage__mutmut_7, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_8': xǁSchemaValidatorǁcheck_test_coverage__mutmut_8, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_9': xǁSchemaValidatorǁcheck_test_coverage__mutmut_9, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_10': xǁSchemaValidatorǁcheck_test_coverage__mutmut_10, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_11': xǁSchemaValidatorǁcheck_test_coverage__mutmut_11, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_12': xǁSchemaValidatorǁcheck_test_coverage__mutmut_12, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_13': xǁSchemaValidatorǁcheck_test_coverage__mutmut_13, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_14': xǁSchemaValidatorǁcheck_test_coverage__mutmut_14, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_15': xǁSchemaValidatorǁcheck_test_coverage__mutmut_15, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_16': xǁSchemaValidatorǁcheck_test_coverage__mutmut_16, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_17': xǁSchemaValidatorǁcheck_test_coverage__mutmut_17, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_18': xǁSchemaValidatorǁcheck_test_coverage__mutmut_18, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_19': xǁSchemaValidatorǁcheck_test_coverage__mutmut_19, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_20': xǁSchemaValidatorǁcheck_test_coverage__mutmut_20, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_21': xǁSchemaValidatorǁcheck_test_coverage__mutmut_21, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_22': xǁSchemaValidatorǁcheck_test_coverage__mutmut_22, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_23': xǁSchemaValidatorǁcheck_test_coverage__mutmut_23, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_24': xǁSchemaValidatorǁcheck_test_coverage__mutmut_24, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_25': xǁSchemaValidatorǁcheck_test_coverage__mutmut_25, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_26': xǁSchemaValidatorǁcheck_test_coverage__mutmut_26, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_27': xǁSchemaValidatorǁcheck_test_coverage__mutmut_27, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_28': xǁSchemaValidatorǁcheck_test_coverage__mutmut_28, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_29': xǁSchemaValidatorǁcheck_test_coverage__mutmut_29, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_30': xǁSchemaValidatorǁcheck_test_coverage__mutmut_30, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_31': xǁSchemaValidatorǁcheck_test_coverage__mutmut_31, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_32': xǁSchemaValidatorǁcheck_test_coverage__mutmut_32, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_33': xǁSchemaValidatorǁcheck_test_coverage__mutmut_33, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_34': xǁSchemaValidatorǁcheck_test_coverage__mutmut_34, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_35': xǁSchemaValidatorǁcheck_test_coverage__mutmut_35, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_36': xǁSchemaValidatorǁcheck_test_coverage__mutmut_36, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_37': xǁSchemaValidatorǁcheck_test_coverage__mutmut_37, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_38': xǁSchemaValidatorǁcheck_test_coverage__mutmut_38, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_39': xǁSchemaValidatorǁcheck_test_coverage__mutmut_39, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_40': xǁSchemaValidatorǁcheck_test_coverage__mutmut_40, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_41': xǁSchemaValidatorǁcheck_test_coverage__mutmut_41, 
        'xǁSchemaValidatorǁcheck_test_coverage__mutmut_42': xǁSchemaValidatorǁcheck_test_coverage__mutmut_42
    }
    
    def check_test_coverage(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSchemaValidatorǁcheck_test_coverage__mutmut_orig"), object.__getattribute__(self, "xǁSchemaValidatorǁcheck_test_coverage__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check_test_coverage.__signature__ = _mutmut_signature(xǁSchemaValidatorǁcheck_test_coverage__mutmut_orig)
    xǁSchemaValidatorǁcheck_test_coverage__mutmut_orig.__name__ = 'xǁSchemaValidatorǁcheck_test_coverage'


__all__ = ["SchemaValidator", "SchemaValidationError"]
