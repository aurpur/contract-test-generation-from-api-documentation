"""
Bruno collection parser for extracting API documentation.

Author: Aurel IKAMA HONEY

This module provides functionality to parse Bruno API collections from both JSON
and .bru file formats, extracting endpoints, requests, and documentation.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from loguru import logger

from .bruno_models import (
    BrunoCollection,
    BrunoItem,
    BrunoRequest,
    BrunoHeader,
    BrunoParam,
    BrunoBody,
    BrunoAuth,
    BrunoScript,
    BrunoConfig,
    BrunoRoot,
    BrunoParseResult,
)


class BrunoParser:
    """
    Parser for Bruno API collections.
    
    Supports:
    - JSON format collections
    - Individual .bru files
    - Folder structures with multiple .bru files
    """
    
    def __init__(self):
        """Initialize the Bruno parser."""
        self.logger = logger.bind(component="BrunoParser")
    
    def parse_collection_from_json(self, json_path: Union[str, Path]) -> BrunoParseResult:
        """
        Parse a Bruno collection from a JSON file.
        
        Args:
            json_path: Path to the JSON collection file
            
        Returns:
            BrunoParseResult with parsed collection and metadata
            
        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            ValueError: If the JSON is invalid or doesn't match Bruno schema
        """
        json_path = Path(json_path)
        
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        self.logger.info(f"Parsing Bruno collection from JSON: {json_path}")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse the collection using Pydantic models (no validation of JSON bodies)
            collection = BrunoCollection(**data)
            
            # Extract metadata with optimized single-pass traversal
            metadata = self._extract_metadata_optimized(collection)
            
            result = BrunoParseResult(
                collection=collection,
                total_requests=metadata['total_requests'],
                total_folders=metadata['total_folders'],
                endpoints=metadata['endpoints'],
                methods=metadata['methods'],
                has_authentication=metadata['has_authentication'],
                has_documentation=metadata['has_documentation'],
            )
            
            self.logger.success(
                f"✓ Parsed collection '{collection.name}': "
                f"{metadata['total_requests']} requests, {metadata['total_folders']} folders"
            )
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse Bruno collection: {e}")
    
    def parse_bru_file(self, bru_path: Union[str, Path]) -> BrunoItem:
        """
        Parse a single .bru file.
        
        Args:
            bru_path: Path to the .bru file
            
        Returns:
            BrunoItem representing the parsed request
            
        Raises:
            FileNotFoundError: If the .bru file doesn't exist
            ValueError: If the .bru format is invalid
        """
        bru_path = Path(bru_path)
        
        if not bru_path.exists():
            raise FileNotFoundError(f".bru file not found: {bru_path}")
        
        self.logger.info(f"Parsing .bru file: {bru_path}")
        
        try:
            with open(bru_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse .bru format
            item = self._parse_bru_content(content, bru_path.stem)
            
            self.logger.success(f"✓ Parsed .bru file '{item.name}'")
            
            return item
            
        except Exception as e:
            raise ValueError(f"Failed to parse .bru file: {e}")
    
    def parse_bru_folder(self, folder_path: Union[str, Path]) -> BrunoParseResult:
        """
        Parse all .bru files in a folder structure.
        
        Args:
            folder_path: Path to the folder containing .bru files
            
        Returns:
            BrunoParseResult with all parsed requests
            
        Raises:
            FileNotFoundError: If the folder doesn't exist
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        self.logger.info(f"Parsing .bru files from folder: {folder_path}")
        
        # Find all .bru files
        bru_files = list(folder_path.rglob("*.bru"))
        
        if not bru_files:
            self.logger.warning(f"No .bru files found in {folder_path}")
        
        items = []
        for bru_file in bru_files:
            try:
                item = self.parse_bru_file(bru_file)
                items.append(item)
            except Exception as e:
                self.logger.error(f"Failed to parse {bru_file}: {e}")
        
        # Create a collection from the parsed items
        collection = BrunoCollection(
            name=folder_path.name,
            version="1",
            items=items,
            brunoConfig=BrunoConfig(
                version="1",
                name=folder_path.name,
                filesCount=len(items),
            )
        )
        
        # Extract metadata with optimized single-pass traversal
        metadata = self._extract_metadata_optimized(collection)
        
        result = BrunoParseResult(
            collection=collection,
            total_requests=metadata['total_requests'],
            total_folders=metadata['total_folders'],
            endpoints=metadata['endpoints'],
            methods=metadata['methods'],
            has_authentication=metadata['has_authentication'],
            has_documentation=metadata['has_documentation'],
        )
        
        self.logger.success(
            f"✓ Parsed {len(bru_files)} .bru files from '{folder_path.name}'"
        )
        
        return result
    
    def _parse_bru_content(self, content: str, name: str) -> BrunoItem:
        """
        Parse the content of a .bru file.
        
        The .bru format is a custom text format with sections like:
        meta {
          name: Request Name
          type: http
        }
        
        get {
          url: https://api.example.com/endpoint
        }
        
        headers {
          Content-Type: application/json
        }
        
        body:json {
          {"key": "value"}
        }
        
        docs {
          Description of the request
        }
        """
        sections = self._extract_sections(content)
        
        # Parse meta section
        meta = sections.get('meta', {})
        request_name = meta.get('name', name)
        request_type = meta.get('type', 'http')
        
        # Parse request method and URL
        method = None
        url = None
        
        for verb in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
            if verb in sections:
                method = verb.upper()
                verb_data = sections[verb]
                url = verb_data.get('url', '')
                break
        
        if not method or not url:
            raise ValueError(f"Could not extract method and URL from .bru file")
        
        # Parse headers
        headers = []
        if 'headers' in sections:
            for key, value in sections['headers'].items():
                headers.append(BrunoHeader(name=key, value=value))
        
        # Parse query params
        params = []
        if 'params' in sections or 'query' in sections:
            query_section = sections.get('params', sections.get('query', {}))
            for key, value in query_section.items():
                params.append(BrunoParam(name=key, value=value))
        
        # Parse body (lazy - no immediate JSON validation)
        body = BrunoBody()
        if 'body:json' in sections:
            body.mode = 'json'
            body.json = sections['body:json'].get('_raw_content', '')  # No validation yet
        elif 'body:xml' in sections:
            body.mode = 'xml'
            body.xml = sections['body:xml'].get('_raw_content', '')
        elif 'body:text' in sections:
            body.mode = 'text'
            body.text = sections['body:text'].get('_raw_content', '')
        
        # Parse auth
        auth = BrunoAuth()
        if 'auth' in sections:
            auth_data = sections['auth']
            auth.mode = auth_data.get('mode', 'none')
            if 'basic' in auth_data:
                auth.username = auth_data['basic'].get('username')
                auth.password = auth_data['basic'].get('password')
            elif 'bearer' in auth_data:
                auth.token = auth_data['bearer'].get('token')
        
        # Parse docs
        docs = sections.get('docs', {}).get('_raw_content', '')
        
        # Parse tests/assertions
        tests = sections.get('tests', {}).get('_raw_content', '')
        assertions = sections.get('assert', {}).get('_raw_content', '')
        
        # Create the request
        request = BrunoRequest(
            url=url,
            method=method,
            headers=headers,
            params=params,
            body=body,
            auth=auth,
            docs=docs,
            tests=tests or assertions,
        )
        
        # Create the item
        item = BrunoItem(
            type=request_type,
            name=request_name,
            filename=f"{name}.bru",
            request=request,
        )
        
        return item
    
    def _extract_sections(self, content: str) -> Dict[str, Any]:
        """Extract sections from .bru file content."""
        sections = {}
        
        # Pattern to match sections: name { content }
        section_pattern = r'(\w+(?::\w+)?)\s*\{([^}]*)\}'
        
        matches = re.finditer(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            section_name = match.group(1).strip()
            section_content = match.group(2).strip()
            
            # Parse key-value pairs or raw content
            if ':' in section_content and not section_name.startswith('body:'):
                # Parse as key-value pairs
                pairs = {}
                for line in section_content.split('\n'):
                    line = line.strip()
                    if ':' in line and not line.startswith('//'):
                        key, value = line.split(':', 1)
                        pairs[key.strip()] = value.strip()
                sections[section_name] = pairs
            else:
                # Store raw content for body sections
                sections[section_name] = {'_raw_content': section_content}
        
        return sections
    
    def _extract_metadata_optimized(self, collection: BrunoCollection) -> Dict[str, Any]:
        """Optimized metadata extraction with single-pass traversal.
        
        Extracts all metadata in one pass to avoid multiple tree traversals:
        - counts, endpoints, methods, auth, tests, docs
        """
        metadata = {
            'total_requests': 0,
            'total_folders': 0,
            'endpoints': [],
            'methods': set(),
            'has_authentication': False,
            'has_documentation': False,
        }
        
        # Check root authentication
        if collection.root.request.auth.mode != "none":
            metadata['has_authentication'] = True
        
        # Single recursive pass
        def traverse(items: List[BrunoItem]):
            for item in items:
                if item.type == "http":
                    metadata['total_requests'] += 1
                    
                    if item.request:
                        # Extract endpoint
                        metadata['endpoints'].append(item.request.url)
                        
                        # Extract method
                        metadata['methods'].add(item.request.method)
                        
                        # Check auth
                        if not metadata['has_authentication'] and item.request.auth.mode != "none":
                            metadata['has_authentication'] = True
                        
                        # Check docs
                        if not metadata['has_documentation'] and item.request.docs:
                            metadata['has_documentation'] = True
                
                elif item.type == "folder":
                    metadata['total_folders'] += 1
                    if item.items:
                        traverse(item.items)
        
        traverse(collection.items)
        
        # Convert methods set to sorted list
        metadata['methods'] = sorted(list(metadata['methods']))
        
        return metadata
    
    def _count_items(self, items: List[BrunoItem]) -> tuple[int, int]:
        """Count total requests and folders recursively (legacy method)."""
        requests = 0
        folders = 0
        
        for item in items:
            if item.type == "http":
                requests += 1
            elif item.type == "folder":
                folders += 1
                if item.items:
                    sub_requests, sub_folders = self._count_items(item.items)
                    requests += sub_requests
                    folders += sub_folders
        
        return requests, folders
    
    def _extract_endpoints(self, items: List[BrunoItem]) -> List[str]:
        """Extract all endpoint URLs from items."""
        endpoints = []
        
        for item in items:
            if item.type == "http" and item.request:
                endpoints.append(item.request.url)
            elif item.type == "folder" and item.items:
                endpoints.extend(self._extract_endpoints(item.items))
        
        return endpoints
    
    def _extract_methods(self, items: List[BrunoItem]) -> List[str]:
        """Extract all HTTP methods from items."""
        methods = []
        
        for item in items:
            if item.type == "http" and item.request:
                methods.append(item.request.method)
            elif item.type == "folder" and item.items:
                methods.extend(self._extract_methods(item.items))
        
        return methods
    
    def _check_authentication(self, collection: BrunoCollection) -> bool:
        """Check if the collection has authentication configured."""
        # Check root auth
        if collection.root.request.auth.mode != "none":
            return True
        
        # Check individual requests
        for item in collection.items:
            if item.type == "http" and item.request:
                if item.request.auth.mode != "none":
                    return True
        
        return False
    
    def _check_tests(self, items: List[BrunoItem]) -> bool:
        """Check if any items have tests/assertions."""
        for item in items:
            if item.type == "http" and item.request:
                if item.request.tests or item.request.assertions:
                    return True
            elif item.type == "folder" and item.items:
                if self._check_tests(item.items):
                    return True
        
        return False
    
    def _check_documentation(self, items: List[BrunoItem]) -> bool:
        """Check if any items have documentation."""
        for item in items:
            if item.type == "http" and item.request:
                if item.request.docs:
                    return True
            elif item.type == "folder" and item.items:
                if self._check_documentation(item.items):
                    return True
        
        return False


__all__ = ["BrunoParser"]
