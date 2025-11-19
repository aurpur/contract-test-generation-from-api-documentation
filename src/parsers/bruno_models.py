"""
Bruno collection models using Pydantic.

Author: Aurel IKAMA HONEY

This module defines the Pydantic models representing the structure of Bruno API collections.
It supports both JSON format and .bru file format parsing.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class BrunoAuth(BaseModel):
    """Authentication configuration for Bruno requests."""
    
    model_config = ConfigDict(extra='allow')
    
    mode: Literal["none", "basic", "bearer", "apikey", "oauth2"] = "none"
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    prefix: Optional[str] = None


class BrunoHeader(BaseModel):
    """HTTP header for Bruno request."""
    
    name: str
    value: str
    enabled: bool = True


class BrunoParam(BaseModel):
    """Query parameter for Bruno request."""
    
    name: str
    value: str
    enabled: bool = True


class BrunoFormField(BaseModel):
    """Form field for multipart or url-encoded requests."""
    
    name: str
    value: str
    enabled: bool = True


class BrunoBody(BaseModel):
    """Request body configuration with lazy JSON validation."""
    
    model_config = ConfigDict(extra='allow')
    
    mode: Literal["none", "json", "xml", "text", "formUrlEncoded", "multipartForm", "file"] = "none"
    json: Optional[str] = None
    xml: Optional[str] = None
    text: Optional[str] = None
    formUrlEncoded: List[BrunoFormField] = Field(default_factory=list)
    multipartForm: List[BrunoFormField] = Field(default_factory=list)
    file: List[Dict[str, Any]] = Field(default_factory=list)
    _lazy_validated: bool = False  # Private flag for lazy validation
    
    def validate_json_format(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return True
        
        if self._lazy_validated:
            return True
        
        try:
            import json as json_module
            json_module.loads(self.json)
            self._lazy_validated = True
            return True
        except Exception:
            return False


class BrunoScript(BaseModel):
    """Pre-request or post-response script."""
    
    model_config = ConfigDict(extra='allow')
    
    req: Optional[str] = None  # Pre-request script
    res: Optional[str] = None  # Post-response script


class BrunoAssertion(BaseModel):
    """Test assertion for Bruno request."""
    
    model_config = ConfigDict(extra='allow')
    
    name: str
    value: str
    enabled: bool = True


class BrunoRequest(BaseModel):
    """Complete Bruno HTTP request specification."""
    
    model_config = ConfigDict(extra='allow')
    
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    headers: List[BrunoHeader] = Field(default_factory=list)
    params: List[BrunoParam] = Field(default_factory=list)
    body: BrunoBody = Field(default_factory=BrunoBody)
    script: BrunoScript = Field(default_factory=BrunoScript)
    vars: Dict[str, Any] = Field(default_factory=dict)
    assertions: List[BrunoAssertion] = Field(default_factory=list)
    tests: str = ""
    docs: str = ""
    auth: BrunoAuth = Field(default_factory=BrunoAuth)


class BrunoItem(BaseModel):
    """Individual item in a Bruno collection."""
    
    model_config = ConfigDict(extra='allow')
    
    type: Literal["http", "folder"] = "http"
    name: str
    filename: Optional[str] = None
    seq: int = 0
    settings: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    examples: List[Any] = Field(default_factory=list)
    request: Optional[BrunoRequest] = None
    items: Optional[List['BrunoItem']] = None  # For folders containing sub-items


class BrunoEnvironment(BaseModel):
    """Environment variables configuration."""
    
    model_config = ConfigDict(extra='allow')
    
    name: str
    variables: Dict[str, str] = Field(default_factory=dict)


class BrunoRootRequest(BaseModel):
    """Root-level request configuration (applies to all requests)."""
    
    model_config = ConfigDict(extra='allow')
    
    auth: BrunoAuth = Field(default_factory=BrunoAuth)


class BrunoRoot(BaseModel):
    """Root configuration for the collection."""
    
    model_config = ConfigDict(extra='allow')
    
    request: BrunoRootRequest = Field(default_factory=BrunoRootRequest)


class BrunoConfig(BaseModel):
    """Bruno collection configuration."""
    
    model_config = ConfigDict(extra='allow')
    
    version: str = "1"
    name: str
    type: Literal["collection"] = "collection"
    ignore: List[str] = Field(default_factory=lambda: ["node_modules", ".git"])
    size: float = 0.0
    filesCount: int = 0


class BrunoCollection(BaseModel):
    """Complete Bruno API collection."""
    
    model_config = ConfigDict(extra='allow')
    
    name: str
    version: str = "1"
    items: List[BrunoItem] = Field(default_factory=list)
    environments: List[BrunoEnvironment] = Field(default_factory=list)
    root: BrunoRoot = Field(default_factory=BrunoRoot)
    brunoConfig: BrunoConfig


class BrunoParseResult(BaseModel):
    """Result of parsing a Bruno collection with metadata."""
    
    collection: BrunoCollection
    total_requests: int = 0
    total_folders: int = 0
    endpoints: List[str] = Field(default_factory=list)
    methods: List[str] = Field(default_factory=list)
    has_authentication: bool = False
    has_documentation: bool = False
    
    def get_all_requests(self) -> List[BrunoItem]:
        """Recursively get all HTTP request items from the collection (optimized)."""
        return list(self._iter_requests(self.collection.items))
    
    def _iter_requests(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def get_endpoints_summary(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts


__all__ = [
    "BrunoAuth",
    "BrunoHeader",
    "BrunoParam",
    "BrunoFormField",
    "BrunoBody",
    "BrunoScript",
    "BrunoAssertion",
    "BrunoRequest",
    "BrunoItem",
    "BrunoEnvironment",
    "BrunoRootRequest",
    "BrunoRoot",
    "BrunoConfig",
    "BrunoCollection",
    "BrunoParseResult",
]
