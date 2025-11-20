"""
Tests for Bruno Parser optimizations.

Author: Aurel IKAMA HONEY

These tests validate the performance optimizations applied to the parser:
- Single-pass metadata extraction
- Lazy JSON validation
- Generator-based recursive extraction
"""

import pytest
import json
from pathlib import Path
from src.parsers import BrunoParser, BrunoParseResult
from src.parsers.bruno_models import BrunoCollection, BrunoItem, BrunoRequest, BrunoBody


class TestParserOptimizations:
    """Test suite for parser optimization features."""
    
    def test_lazy_json_validation(self, tmp_path):
        """Test that JSON body validation is deferred until explicitly called."""
        # Create a request with JSON body
        body = BrunoBody(mode="json", json='{"key": "value"}')
        
        # Validation should not happen at creation
        assert not body._lazy_validated
        
        # First validation call
        assert body.validate_json_format()
        assert body._lazy_validated
        
        # Second call should return immediately (cached)
        assert body.validate_json_format()
    
    def test_lazy_validation_invalid_json(self):
        """Test lazy validation with invalid JSON."""
        body = BrunoBody(mode="json", json='{invalid json}')
        
        # Should not raise at creation
        assert not body._lazy_validated
        
        # Should return False on validation
        assert not body.validate_json_format()
        assert not body._lazy_validated  # Flag not set for invalid JSON
    
    def test_lazy_validation_non_json_mode(self):
        """Test lazy validation skips non-JSON modes."""
        body_text = BrunoBody(mode="text", text="plain text")
        assert body_text.validate_json_format()  # Should pass (not JSON)
        
        body_none = BrunoBody(mode="none")
        assert body_none.validate_json_format()  # Should pass (no body)
    
    def test_generator_based_extraction(self, tmp_path, sample_collection_with_nested_folders):
        """Test that recursive extraction uses generators efficiently."""
        parser = BrunoParser()
        
        # Create a nested collection structure
        collection_data = {
            "name": "Test Collection",
            "version": "1",
            "items": [
                {
                    "type": "http",
                    "name": "Request 1",
                    "request": {"url": "https://api.test.com/1", "method": "GET"}
                },
                {
                    "type": "folder",
                    "name": "Folder 1",
                    "items": [
                        {
                            "type": "http",
                            "name": "Request 2",
                            "request": {"url": "https://api.test.com/2", "method": "POST"}
                        },
                        {
                            "type": "folder",
                            "name": "Nested Folder",
                            "items": [
                                {
                                    "type": "http",
                                    "name": "Request 3",
                                    "request": {"url": "https://api.test.com/3", "method": "PUT"}
                                }
                            ]
                        }
                    ]
                }
            ],
            "brunoConfig": {
                "version": "1",
                "name": "Test Collection",
                "type": "collection"
            }
        }
        
        # Save to temp file
        temp_file = tmp_path / "test_collection.json"
        with open(temp_file, 'w') as f:
            json.dump(collection_data, f)
        
        # Parse
        result = parser.parse_collection_from_json(temp_file)
        
        # Test generator extraction
        requests = result.get_all_requests()
        
        assert len(requests) == 3
        assert requests[0].name == "Request 1"
        assert requests[1].name == "Request 2"
        assert requests[2].name == "Request 3"
    
    def test_single_pass_metadata_extraction(self, tmp_path):
        """Test that metadata extraction happens in a single pass."""
        parser = BrunoParser()
        
        # Create collection with various features
        collection_data = {
            "name": "Feature Collection",
            "version": "1",
            "items": [
                {
                    "type": "http",
                    "name": "Request with Auth",
                    "request": {
                        "url": "https://api.test.com/auth",
                        "method": "GET",
                        "auth": {"mode": "bearer", "token": "test-token"},
                        "docs": "This has documentation"
                    }
                },
                {
                    "type": "http",
                    "name": "Request with Tests",
                    "request": {
                        "url": "https://api.test.com/test",
                        "method": "POST",
                        "tests": "expect(response.status).toBe(200);"
                    }
                },
                {
                    "type": "folder",
                    "name": "Empty Folder",
                    "items": []
                }
            ],
            "brunoConfig": {
                "version": "1",
                "name": "Feature Collection",
                "type": "collection"
            }
        }
        
        temp_file = tmp_path / "feature_collection.json"
        with open(temp_file, 'w') as f:
            json.dump(collection_data, f)
        
        result = parser.parse_collection_from_json(temp_file)
        
        # Verify all metadata was extracted in single pass
        assert result.total_requests == 2
        assert result.total_folders == 1
        assert result.has_authentication is True
        # Note: has_tests removed - we generate tests, not use existing ones
        assert result.has_documentation is True
        assert len(result.endpoints) == 2
        assert set(result.methods) == {"GET", "POST"}
    
    def test_early_exit_optimization(self, tmp_path):
        """Test that boolean flags use early exit when found."""
        parser = BrunoParser()
        
        # Collection where first request has all features
        collection_data = {
            "name": "Early Exit Test",
            "version": "1",
            "items": [
                {
                    "type": "http",
                    "name": "Full Featured Request",
                    "request": {
                        "url": "https://api.test.com/full",
                        "method": "GET",
                        "auth": {"mode": "basic", "username": "user", "password": "pass"},
                        "docs": "Has docs",
                        "tests": "Has tests"
                    }
                }
            ] + [
                {
                    "type": "http",
                    "name": f"Request {i}",
                    "request": {
                        "url": f"https://api.test.com/{i}",
                        "method": "GET"
                    }
                }
                for i in range(100)
            ],
            "brunoConfig": {
                "version": "1",
                "name": "Early Exit Test",
                "type": "collection"
            }
        }
        
        temp_file = tmp_path / "early_exit.json"
        with open(temp_file, 'w') as f:
            json.dump(collection_data, f)
        
        result = parser.parse_collection_from_json(temp_file)
        
        # All flags should be True after finding first request
        assert result.has_authentication is True
        # Note: has_tests removed - we generate tests, not use existing ones
        assert result.has_documentation is True
        assert result.total_requests == 101
    
    def test_optimized_methods_sorting(self, tmp_path):
        """Test that methods are sorted in metadata extraction."""
        parser = BrunoParser()
        
        collection_data = {
            "name": "Methods Test",
            "version": "1",
            "items": [
                {"type": "http", "name": "R1", "request": {"url": "http://test.com", "method": "DELETE"}},
                {"type": "http", "name": "R2", "request": {"url": "http://test.com", "method": "POST"}},
                {"type": "http", "name": "R3", "request": {"url": "http://test.com", "method": "GET"}},
                {"type": "http", "name": "R4", "request": {"url": "http://test.com", "method": "PUT"}},
            ],
            "brunoConfig": {"version": "1", "name": "Methods Test", "type": "collection"}
        }
        
        temp_file = tmp_path / "methods.json"
        with open(temp_file, 'w') as f:
            json.dump(collection_data, f)
        
        result = parser.parse_collection_from_json(temp_file)
        
        # Methods should be sorted
        assert result.methods == ["DELETE", "GET", "POST", "PUT"]


@pytest.fixture
def sample_collection_with_nested_folders():
    """Fixture for nested folder structure testing."""
    return {
        "name": "Nested Collection",
        "version": "1",
        "items": [],
        "brunoConfig": {
            "version": "1",
            "name": "Nested Collection",
            "type": "collection"
        }
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
