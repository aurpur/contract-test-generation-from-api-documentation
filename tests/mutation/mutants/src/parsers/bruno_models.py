"""
Bruno collection models using Pydantic.

Author: Aurel IKAMA HONEY

This module defines the Pydantic models representing the structure of Bruno API collections.
It supports both JSON format and .bru file format parsing.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_orig(self) -> bool:
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_1(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" and not self.json:
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_2(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode == "json" or not self.json:
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_3(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "XXjsonXX" or not self.json:
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_4(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "JSON" or not self.json:
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_5(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or self.json:
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
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_6(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return False
        
        if self._lazy_validated:
            return True
        
        try:
            import json as json_module
            json_module.loads(self.json)
            self._lazy_validated = True
            return True
        except Exception:
            return False
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_7(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return True
        
        if self._lazy_validated:
            return False
        
        try:
            import json as json_module
            json_module.loads(self.json)
            self._lazy_validated = True
            return True
        except Exception:
            return False
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_8(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return True
        
        if self._lazy_validated:
            return True
        
        try:
            import json as json_module
            json_module.loads(None)
            self._lazy_validated = True
            return True
        except Exception:
            return False
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_9(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return True
        
        if self._lazy_validated:
            return True
        
        try:
            import json as json_module
            json_module.loads(self.json)
            self._lazy_validated = None
            return True
        except Exception:
            return False
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_10(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return True
        
        if self._lazy_validated:
            return True
        
        try:
            import json as json_module
            json_module.loads(self.json)
            self._lazy_validated = False
            return True
        except Exception:
            return False
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_11(self) -> bool:
        """Lazy validation of JSON body format (called only when needed)."""
        if self.mode != "json" or not self.json:
            return True
        
        if self._lazy_validated:
            return True
        
        try:
            import json as json_module
            json_module.loads(self.json)
            self._lazy_validated = True
            return False
        except Exception:
            return False
    
    def xǁBrunoBodyǁvalidate_json_format__mutmut_12(self) -> bool:
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
            return True
    
    xǁBrunoBodyǁvalidate_json_format__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBrunoBodyǁvalidate_json_format__mutmut_1': xǁBrunoBodyǁvalidate_json_format__mutmut_1, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_2': xǁBrunoBodyǁvalidate_json_format__mutmut_2, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_3': xǁBrunoBodyǁvalidate_json_format__mutmut_3, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_4': xǁBrunoBodyǁvalidate_json_format__mutmut_4, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_5': xǁBrunoBodyǁvalidate_json_format__mutmut_5, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_6': xǁBrunoBodyǁvalidate_json_format__mutmut_6, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_7': xǁBrunoBodyǁvalidate_json_format__mutmut_7, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_8': xǁBrunoBodyǁvalidate_json_format__mutmut_8, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_9': xǁBrunoBodyǁvalidate_json_format__mutmut_9, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_10': xǁBrunoBodyǁvalidate_json_format__mutmut_10, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_11': xǁBrunoBodyǁvalidate_json_format__mutmut_11, 
        'xǁBrunoBodyǁvalidate_json_format__mutmut_12': xǁBrunoBodyǁvalidate_json_format__mutmut_12
    }
    
    def validate_json_format(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBrunoBodyǁvalidate_json_format__mutmut_orig"), object.__getattribute__(self, "xǁBrunoBodyǁvalidate_json_format__mutmut_mutants"), args, kwargs, self)
        return result 
    
    validate_json_format.__signature__ = _mutmut_signature(xǁBrunoBodyǁvalidate_json_format__mutmut_orig)
    xǁBrunoBodyǁvalidate_json_format__mutmut_orig.__name__ = 'xǁBrunoBodyǁvalidate_json_format'


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
    
    def xǁBrunoParseResultǁget_all_requests__mutmut_orig(self) -> List[BrunoItem]:
        """Recursively get all HTTP request items from the collection (optimized)."""
        return list(self._iter_requests(self.collection.items))
    
    def xǁBrunoParseResultǁget_all_requests__mutmut_1(self) -> List[BrunoItem]:
        """Recursively get all HTTP request items from the collection (optimized)."""
        return list(None)
    
    def xǁBrunoParseResultǁget_all_requests__mutmut_2(self) -> List[BrunoItem]:
        """Recursively get all HTTP request items from the collection (optimized)."""
        return list(self._iter_requests(None))
    
    xǁBrunoParseResultǁget_all_requests__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBrunoParseResultǁget_all_requests__mutmut_1': xǁBrunoParseResultǁget_all_requests__mutmut_1, 
        'xǁBrunoParseResultǁget_all_requests__mutmut_2': xǁBrunoParseResultǁget_all_requests__mutmut_2
    }
    
    def get_all_requests(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBrunoParseResultǁget_all_requests__mutmut_orig"), object.__getattribute__(self, "xǁBrunoParseResultǁget_all_requests__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_all_requests.__signature__ = _mutmut_signature(xǁBrunoParseResultǁget_all_requests__mutmut_orig)
    xǁBrunoParseResultǁget_all_requests__mutmut_orig.__name__ = 'xǁBrunoParseResultǁget_all_requests'
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_orig(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_1(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" or item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_2(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type != "http" and item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_3(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "XXhttpXX" and item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_4(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "HTTP" and item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_5(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type == "folder" or item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_6(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type != "folder" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_7(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type == "XXfolderXX" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_8(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type == "FOLDER" and item.items:
                yield from self._iter_requests(item.items)
    
    def xǁBrunoParseResultǁ_iter_requests__mutmut_9(self, items: List[BrunoItem]):
        """Generator for efficient recursive traversal (no intermediate lists)."""
        for item in items:
            if item.type == "http" and item.request:
                yield item
            elif item.type == "folder" and item.items:
                yield from self._iter_requests(None)
    
    xǁBrunoParseResultǁ_iter_requests__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBrunoParseResultǁ_iter_requests__mutmut_1': xǁBrunoParseResultǁ_iter_requests__mutmut_1, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_2': xǁBrunoParseResultǁ_iter_requests__mutmut_2, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_3': xǁBrunoParseResultǁ_iter_requests__mutmut_3, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_4': xǁBrunoParseResultǁ_iter_requests__mutmut_4, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_5': xǁBrunoParseResultǁ_iter_requests__mutmut_5, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_6': xǁBrunoParseResultǁ_iter_requests__mutmut_6, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_7': xǁBrunoParseResultǁ_iter_requests__mutmut_7, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_8': xǁBrunoParseResultǁ_iter_requests__mutmut_8, 
        'xǁBrunoParseResultǁ_iter_requests__mutmut_9': xǁBrunoParseResultǁ_iter_requests__mutmut_9
    }
    
    def _iter_requests(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBrunoParseResultǁ_iter_requests__mutmut_orig"), object.__getattribute__(self, "xǁBrunoParseResultǁ_iter_requests__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _iter_requests.__signature__ = _mutmut_signature(xǁBrunoParseResultǁ_iter_requests__mutmut_orig)
    xǁBrunoParseResultǁ_iter_requests__mutmut_orig.__name__ = 'xǁBrunoParseResultǁ_iter_requests'
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_orig(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_1(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = None
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_2(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = None
                method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_3(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = None
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_4(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, 0) - 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_5(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(None, 0) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_6(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, None) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_7(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(0) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_8(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, ) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_9(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, 1) + 1
        return method_counts
    
    def xǁBrunoParseResultǁget_endpoints_summary__mutmut_10(self) -> Dict[str, int]:
        """Get a summary of HTTP methods used."""
        method_counts = {}
        for req in self.get_all_requests():
            if req.request:
                method = req.request.method
                method_counts[method] = method_counts.get(method, 0) + 2
        return method_counts
    
    xǁBrunoParseResultǁget_endpoints_summary__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBrunoParseResultǁget_endpoints_summary__mutmut_1': xǁBrunoParseResultǁget_endpoints_summary__mutmut_1, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_2': xǁBrunoParseResultǁget_endpoints_summary__mutmut_2, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_3': xǁBrunoParseResultǁget_endpoints_summary__mutmut_3, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_4': xǁBrunoParseResultǁget_endpoints_summary__mutmut_4, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_5': xǁBrunoParseResultǁget_endpoints_summary__mutmut_5, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_6': xǁBrunoParseResultǁget_endpoints_summary__mutmut_6, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_7': xǁBrunoParseResultǁget_endpoints_summary__mutmut_7, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_8': xǁBrunoParseResultǁget_endpoints_summary__mutmut_8, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_9': xǁBrunoParseResultǁget_endpoints_summary__mutmut_9, 
        'xǁBrunoParseResultǁget_endpoints_summary__mutmut_10': xǁBrunoParseResultǁget_endpoints_summary__mutmut_10
    }
    
    def get_endpoints_summary(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBrunoParseResultǁget_endpoints_summary__mutmut_orig"), object.__getattribute__(self, "xǁBrunoParseResultǁget_endpoints_summary__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_endpoints_summary.__signature__ = _mutmut_signature(xǁBrunoParseResultǁget_endpoints_summary__mutmut_orig)
    xǁBrunoParseResultǁget_endpoints_summary__mutmut_orig.__name__ = 'xǁBrunoParseResultǁget_endpoints_summary'


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
