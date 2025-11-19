"""
Unit tests for Bruno parser module.

Author: Aurel IKAMA HONEY
"""

import pytest
import json
from pathlib import Path
from src.parsers import BrunoParser, SchemaValidator, BrunoCollection


class TestBrunoParser:
    """Test suite for BrunoParser class."""
    
    @pytest.fixture
    def parser(self):
        """Create a BrunoParser instance."""
        return BrunoParser()
    
    @pytest.fixture
    def sample_json_path(self, tmp_path):
        """Create a sample Bruno collection JSON file."""
        collection_data = {
            "name": "Test Collection",
            "version": "1",
            "items": [
                {
                    "type": "http",
                    "name": "Get Users",
                    "filename": "Get Users.bru",
                    "seq": 1,
                    "request": {
                        "url": "https://api.example.com/users",
                        "method": "GET",
                        "headers": [],
                        "params": [],
                        "body": {"mode": "none"},
                        "auth": {"mode": "none"},
                        "docs": "Retrieve all users",
                        "tests": "assert response.status === 200"
                    }
                }
            ],
            "environments": [],
            "root": {"request": {"auth": {"mode": "none"}}},
            "brunoConfig": {
                "version": "1",
                "name": "Test Collection",
                "type": "collection",
                "ignore": ["node_modules", ".git"],
                "size": 0.0,
                "filesCount": 1
            }
        }
        
        json_file = tmp_path / "collection.json"
        with open(json_file, 'w') as f:
            json.dump(collection_data, f)
        
        return json_file
    
    @pytest.fixture
    def sample_bru_file(self, tmp_path):
        """Create a sample .bru file."""
        bru_content = """meta {
  name: Get Users
  type: http
}

get {
  url: https://api.example.com/users
}

headers {
  Content-Type: application/json
  Authorization: Bearer {{token}}
}

docs {
  This endpoint retrieves all users from the system.
}

tests {
  expect(response.status).toBe(200);
  expect(response.body).toBeArray();
}
"""
        bru_file = tmp_path / "get_users.bru"
        with open(bru_file, 'w') as f:
            f.write(bru_content)
        
        return bru_file
    
    def test_parse_json_collection(self, parser, sample_json_path):
        """Test parsing a Bruno collection from JSON."""
        result = parser.parse_collection_from_json(sample_json_path)
        
        assert result.collection.name == "Test Collection"
        assert result.total_requests == 1
        assert result.total_folders == 0
        assert len(result.endpoints) == 1
        assert "GET" in result.methods
        assert result.has_documentation
        # Note: has_tests removed - we generate tests, not use existing ones
    
    def test_parse_json_collection_invalid_path(self, parser):
        """Test parsing with invalid JSON path."""
        with pytest.raises(FileNotFoundError):
            parser.parse_collection_from_json("nonexistent.json")
    
    def test_parse_bru_file(self, parser, sample_bru_file):
        """Test parsing a single .bru file."""
        item = parser.parse_bru_file(sample_bru_file)
        
        assert item.name == "Get Users"
        assert item.type == "http"
        assert item.request is not None
        assert item.request.method == "GET"
        assert item.request.url == "https://api.example.com/users"
        assert len(item.request.headers) == 2
        assert item.request.docs
        assert item.request.tests
    
    def test_parse_bru_file_invalid_path(self, parser):
        """Test parsing with invalid .bru path."""
        with pytest.raises(FileNotFoundError):
            parser.parse_bru_file("nonexistent.bru")
    
    def test_parse_bru_folder(self, parser, tmp_path, sample_bru_file):
        """Test parsing all .bru files in a folder."""
        # The sample_bru_file is already in tmp_path
        result = parser.parse_bru_folder(tmp_path)
        
        assert result.collection.name == tmp_path.name
        assert result.total_requests == 1
        assert len(result.endpoints) == 1
    
    def test_get_all_requests(self, parser, sample_json_path):
        """Test extracting all requests from a collection."""
        result = parser.parse_collection_from_json(sample_json_path)
        requests = result.get_all_requests()
        
        assert len(requests) == 1
        assert requests[0].name == "Get Users"
    
    def test_get_endpoints_summary(self, parser, sample_json_path):
        """Test getting endpoints summary."""
        result = parser.parse_collection_from_json(sample_json_path)
        summary = result.get_endpoints_summary()
        
        assert "GET" in summary
        assert summary["GET"] == 1


class TestSchemaValidator:
    """Test suite for SchemaValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a SchemaValidator instance."""
        return SchemaValidator()
    
    @pytest.fixture
    def valid_collection_result(self, tmp_path):
        """Create a valid Bruno collection result."""
        parser = BrunoParser()
        
        collection_data = {
            "name": "Valid Collection",
            "version": "1",
            "items": [
                {
                    "type": "http",
                    "name": "Get Users",
                    "filename": "Get Users.bru",
                    "seq": 1,
                    "request": {
                        "url": "https://api.example.com/users",
                        "method": "GET",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "params": [],
                        "body": {"mode": "none"},
                        "auth": {"mode": "none"},
                        "docs": "Retrieve all users",
                        "tests": "assert response.status === 200"
                    }
                }
            ],
            "environments": [],
            "root": {"request": {"auth": {"mode": "none"}}},
            "brunoConfig": {
                "version": "1",
                "name": "Valid Collection",
                "type": "collection",
                "ignore": ["node_modules", ".git"],
                "size": 0.0,
                "filesCount": 1
            }
        }
        
        json_file = tmp_path / "valid_collection.json"
        with open(json_file, 'w') as f:
            json.dump(collection_data, f)
        
        return parser.parse_collection_from_json(json_file)
    
    def test_validate_valid_collection(self, validator, valid_collection_result):
        """Test validating a valid collection."""
        is_valid = validator.validate_collection(valid_collection_result)
        
        assert is_valid
        assert len(validator.validation_errors) == 0
    
    def test_check_documentation_completeness(self, validator, valid_collection_result):
        """Test checking documentation completeness."""
        report = validator.check_documentation_completeness(valid_collection_result)
        
        assert report["completeness_score"] == 100.0
        assert report["documented_requests"] == 1
        assert report["undocumented_requests"] == 0
    
    def test_check_test_coverage(self, validator, valid_collection_result):
        """Test checking test coverage."""
        report = validator.check_test_coverage(valid_collection_result)
        
        assert report["coverage_score"] == 100.0
        assert report["tested_requests"] == 1
        assert report["untested_requests"] == 0
    
    def test_validation_report(self, validator, valid_collection_result):
        """Test getting validation report."""
        validator.validate_collection(valid_collection_result)
        report = validator.get_validation_report()
        
        assert report["is_valid"]
        assert report["error_count"] == 0
        assert report["warning_count"] == 0
    
    def test_validate_invalid_url(self, validator):
        """Test URL validation."""
        assert not validator._is_valid_url("not-a-url")
        assert validator._is_valid_url("https://api.example.com/endpoint")
        assert validator._is_valid_url("http://localhost:8080/api")
        assert validator._is_valid_url("{{baseUrl}}/endpoint")
    
    def test_validate_json(self, validator):
        """Test JSON validation."""
        assert validator._is_valid_json('{"key": "value"}')
        assert validator._is_valid_json('[]')
        assert not validator._is_valid_json('not json')
        assert not validator._is_valid_json('{invalid}')


class TestBrunoModels:
    """Test suite for Bruno Pydantic models."""
    
    def test_bruno_request_creation(self):
        """Test creating a BrunoRequest instance."""
        from src.parsers.bruno_models import BrunoRequest
        
        request = BrunoRequest(
            url="https://api.example.com/users",
            method="GET"
        )
        
        assert request.url == "https://api.example.com/users"
        assert request.method == "GET"
        assert len(request.headers) == 0
        assert request.body.mode == "none"
    
    def test_bruno_collection_creation(self):
        """Test creating a BrunoCollection instance."""
        from src.parsers.bruno_models import BrunoCollection, BrunoConfig
        
        collection = BrunoCollection(
            name="Test Collection",
            version="1",
            brunoConfig=BrunoConfig(
                version="1",
                name="Test Collection",
                type="collection"
            )
        )
        
        assert collection.name == "Test Collection"
        assert collection.version == "1"
        assert len(collection.items) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
