"""
Message serialization and deserialization for inter-agent communication.

This module handles conversion of agent messages to/from various formats
(JSON, binary, etc.) for storage and transmission.

Author: Aurel IKAMA HONEY
"""
import json
import pickle
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Type, TypeVar
from uuid import UUID

from pydantic import ValidationError

from shared_context import AgentMessage, AgentType
from utils.logging import logger

T = TypeVar('T')
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


class SerializationFormat(str, Enum):
    """Supported serialization formats."""
    JSON = "json"
    PICKLE = "pickle"
    MSGPACK = "msgpack"


class SerializationError(Exception):
    """Exception raised when serialization fails."""
    pass


class DeserializationError(Exception):
    """Exception raised when deserialization fails."""
    pass


class MessageSerializer(ABC):
    """
    Abstract base class for message serializers.
    
    Defines the interface for serializing and deserializing agent messages.
    """
    
    @abstractmethod
    def serialize(self, message: AgentMessage) -> bytes:
        """
        Serialize a message to bytes.
        
        Args:
            message: Agent message to serialize
            
        Returns:
            Serialized message as bytes
            
        Raises:
            SerializationError: If serialization fails
        """
        pass
    
    @abstractmethod
    def deserialize(self, data: bytes) -> AgentMessage:
        """
        Deserialize bytes to a message.
        
        Args:
            data: Serialized message bytes
            
        Returns:
            Deserialized agent message
            
        Raises:
            DeserializationError: If deserialization fails
        """
        pass
    
    @abstractmethod
    def get_format(self) -> SerializationFormat:
        """
        Get the serialization format.
        
        Returns:
            Serialization format
        """
        pass


class JSONSerializer(MessageSerializer):
    """
    JSON-based message serializer.
    
    Uses JSON for human-readable serialization. Good for debugging
    and cross-platform compatibility.
    """
    
    def xǁJSONSerializerǁ__init____mutmut_orig(self, pretty: bool = False):
        """
        Initialize JSON serializer.
        
        Args:
            pretty: Whether to pretty-print JSON
        """
        self.pretty = pretty
        logger.debug(f"JSONSerializer initialized (pretty={pretty})")
    
    def xǁJSONSerializerǁ__init____mutmut_1(self, pretty: bool = True):
        """
        Initialize JSON serializer.
        
        Args:
            pretty: Whether to pretty-print JSON
        """
        self.pretty = pretty
        logger.debug(f"JSONSerializer initialized (pretty={pretty})")
    
    def xǁJSONSerializerǁ__init____mutmut_2(self, pretty: bool = False):
        """
        Initialize JSON serializer.
        
        Args:
            pretty: Whether to pretty-print JSON
        """
        self.pretty = None
        logger.debug(f"JSONSerializer initialized (pretty={pretty})")
    
    def xǁJSONSerializerǁ__init____mutmut_3(self, pretty: bool = False):
        """
        Initialize JSON serializer.
        
        Args:
            pretty: Whether to pretty-print JSON
        """
        self.pretty = pretty
        logger.debug(None)
    
    xǁJSONSerializerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁJSONSerializerǁ__init____mutmut_1': xǁJSONSerializerǁ__init____mutmut_1, 
        'xǁJSONSerializerǁ__init____mutmut_2': xǁJSONSerializerǁ__init____mutmut_2, 
        'xǁJSONSerializerǁ__init____mutmut_3': xǁJSONSerializerǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁJSONSerializerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁJSONSerializerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁJSONSerializerǁ__init____mutmut_orig)
    xǁJSONSerializerǁ__init____mutmut_orig.__name__ = 'xǁJSONSerializerǁ__init__'
    
    def xǁJSONSerializerǁserialize__mutmut_orig(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_1(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = None
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_2(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode=None)
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_3(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='XXjsonXX')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_4(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='JSON')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_5(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = None
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_6(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    None,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_7(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=None,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_8(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=None,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_9(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_10(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_11(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_12(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=3,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_13(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = None
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_14(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    None,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_15(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=None,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_16(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_17(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_18(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode(None)
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_19(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('XXutf-8XX')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_20(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('UTF-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_21(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = None
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_22(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(None)
            raise SerializationError(error_msg) from e
    
    def xǁJSONSerializerǁserialize__mutmut_23(self, message: AgentMessage) -> bytes:
        """Serialize message to JSON bytes."""
        try:
            # Convert Pydantic model to dict
            message_dict = message.model_dump(mode='json')
            
            # Convert to JSON
            if self.pretty:
                json_str = json.dumps(
                    message_dict,
                    indent=2,
                    default=self._json_default,
                )
            else:
                json_str = json.dumps(
                    message_dict,
                    default=self._json_default,
                )
            
            return json_str.encode('utf-8')
        
        except Exception as e:
            error_msg = f"Failed to serialize message to JSON: {e}"
            logger.error(error_msg)
            raise SerializationError(None) from e
    
    xǁJSONSerializerǁserialize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁJSONSerializerǁserialize__mutmut_1': xǁJSONSerializerǁserialize__mutmut_1, 
        'xǁJSONSerializerǁserialize__mutmut_2': xǁJSONSerializerǁserialize__mutmut_2, 
        'xǁJSONSerializerǁserialize__mutmut_3': xǁJSONSerializerǁserialize__mutmut_3, 
        'xǁJSONSerializerǁserialize__mutmut_4': xǁJSONSerializerǁserialize__mutmut_4, 
        'xǁJSONSerializerǁserialize__mutmut_5': xǁJSONSerializerǁserialize__mutmut_5, 
        'xǁJSONSerializerǁserialize__mutmut_6': xǁJSONSerializerǁserialize__mutmut_6, 
        'xǁJSONSerializerǁserialize__mutmut_7': xǁJSONSerializerǁserialize__mutmut_7, 
        'xǁJSONSerializerǁserialize__mutmut_8': xǁJSONSerializerǁserialize__mutmut_8, 
        'xǁJSONSerializerǁserialize__mutmut_9': xǁJSONSerializerǁserialize__mutmut_9, 
        'xǁJSONSerializerǁserialize__mutmut_10': xǁJSONSerializerǁserialize__mutmut_10, 
        'xǁJSONSerializerǁserialize__mutmut_11': xǁJSONSerializerǁserialize__mutmut_11, 
        'xǁJSONSerializerǁserialize__mutmut_12': xǁJSONSerializerǁserialize__mutmut_12, 
        'xǁJSONSerializerǁserialize__mutmut_13': xǁJSONSerializerǁserialize__mutmut_13, 
        'xǁJSONSerializerǁserialize__mutmut_14': xǁJSONSerializerǁserialize__mutmut_14, 
        'xǁJSONSerializerǁserialize__mutmut_15': xǁJSONSerializerǁserialize__mutmut_15, 
        'xǁJSONSerializerǁserialize__mutmut_16': xǁJSONSerializerǁserialize__mutmut_16, 
        'xǁJSONSerializerǁserialize__mutmut_17': xǁJSONSerializerǁserialize__mutmut_17, 
        'xǁJSONSerializerǁserialize__mutmut_18': xǁJSONSerializerǁserialize__mutmut_18, 
        'xǁJSONSerializerǁserialize__mutmut_19': xǁJSONSerializerǁserialize__mutmut_19, 
        'xǁJSONSerializerǁserialize__mutmut_20': xǁJSONSerializerǁserialize__mutmut_20, 
        'xǁJSONSerializerǁserialize__mutmut_21': xǁJSONSerializerǁserialize__mutmut_21, 
        'xǁJSONSerializerǁserialize__mutmut_22': xǁJSONSerializerǁserialize__mutmut_22, 
        'xǁJSONSerializerǁserialize__mutmut_23': xǁJSONSerializerǁserialize__mutmut_23
    }
    
    def serialize(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁJSONSerializerǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁJSONSerializerǁserialize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    serialize.__signature__ = _mutmut_signature(xǁJSONSerializerǁserialize__mutmut_orig)
    xǁJSONSerializerǁserialize__mutmut_orig.__name__ = 'xǁJSONSerializerǁserialize'
    
    def xǁJSONSerializerǁdeserialize__mutmut_orig(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_1(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = None
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_2(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode(None)
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_3(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('XXutf-8XX')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_4(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('UTF-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_5(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = None
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_6(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(None)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_7(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = None
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_8(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(None)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_9(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = None
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_10(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(None)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_11(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(None) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_12(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = None
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_13(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(None)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_14(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(None) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_15(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = None
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_16(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(None)
            raise DeserializationError(error_msg) from e
    
    def xǁJSONSerializerǁdeserialize__mutmut_17(self, data: bytes) -> AgentMessage:
        """Deserialize JSON bytes to message."""
        try:
            # Decode bytes to string
            json_str = data.decode('utf-8')
            
            # Parse JSON
            message_dict = json.loads(json_str)
            
            # Convert string UUIDs back to UUID objects
            message_dict = self._convert_uuids(message_dict)
            
            # Create AgentMessage from dict
            return AgentMessage(**message_dict)
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except ValidationError as e:
            error_msg = f"Invalid message structure: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize JSON to message: {e}"
            logger.error(error_msg)
            raise DeserializationError(None) from e
    
    xǁJSONSerializerǁdeserialize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁJSONSerializerǁdeserialize__mutmut_1': xǁJSONSerializerǁdeserialize__mutmut_1, 
        'xǁJSONSerializerǁdeserialize__mutmut_2': xǁJSONSerializerǁdeserialize__mutmut_2, 
        'xǁJSONSerializerǁdeserialize__mutmut_3': xǁJSONSerializerǁdeserialize__mutmut_3, 
        'xǁJSONSerializerǁdeserialize__mutmut_4': xǁJSONSerializerǁdeserialize__mutmut_4, 
        'xǁJSONSerializerǁdeserialize__mutmut_5': xǁJSONSerializerǁdeserialize__mutmut_5, 
        'xǁJSONSerializerǁdeserialize__mutmut_6': xǁJSONSerializerǁdeserialize__mutmut_6, 
        'xǁJSONSerializerǁdeserialize__mutmut_7': xǁJSONSerializerǁdeserialize__mutmut_7, 
        'xǁJSONSerializerǁdeserialize__mutmut_8': xǁJSONSerializerǁdeserialize__mutmut_8, 
        'xǁJSONSerializerǁdeserialize__mutmut_9': xǁJSONSerializerǁdeserialize__mutmut_9, 
        'xǁJSONSerializerǁdeserialize__mutmut_10': xǁJSONSerializerǁdeserialize__mutmut_10, 
        'xǁJSONSerializerǁdeserialize__mutmut_11': xǁJSONSerializerǁdeserialize__mutmut_11, 
        'xǁJSONSerializerǁdeserialize__mutmut_12': xǁJSONSerializerǁdeserialize__mutmut_12, 
        'xǁJSONSerializerǁdeserialize__mutmut_13': xǁJSONSerializerǁdeserialize__mutmut_13, 
        'xǁJSONSerializerǁdeserialize__mutmut_14': xǁJSONSerializerǁdeserialize__mutmut_14, 
        'xǁJSONSerializerǁdeserialize__mutmut_15': xǁJSONSerializerǁdeserialize__mutmut_15, 
        'xǁJSONSerializerǁdeserialize__mutmut_16': xǁJSONSerializerǁdeserialize__mutmut_16, 
        'xǁJSONSerializerǁdeserialize__mutmut_17': xǁJSONSerializerǁdeserialize__mutmut_17
    }
    
    def deserialize(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁJSONSerializerǁdeserialize__mutmut_orig"), object.__getattribute__(self, "xǁJSONSerializerǁdeserialize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    deserialize.__signature__ = _mutmut_signature(xǁJSONSerializerǁdeserialize__mutmut_orig)
    xǁJSONSerializerǁdeserialize__mutmut_orig.__name__ = 'xǁJSONSerializerǁdeserialize'
    
    def get_format(self) -> SerializationFormat:
        """Get serialization format."""
        return SerializationFormat.JSON
    
    @staticmethod
    def _json_default(obj: Any) -> Any:
        """Handle non-serializable objects."""
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    @staticmethod
    def _convert_uuids(data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert UUID strings back to UUID objects."""
        uuid_fields = ['id', 'session_id', 'parent_message_id']
        
        for field in uuid_fields:
            if field in data and data[field] is not None:
                try:
                    data[field] = UUID(data[field])
                except (ValueError, TypeError):
                    pass
        
        # Convert enum strings back to enums
        if 'from_agent' in data:
            data['from_agent'] = AgentType(data['from_agent'])
        if 'to_agent' in data:
            data['to_agent'] = AgentType(data['to_agent'])
        
        # Convert datetime strings back to datetime objects
        if 'created_at' in data and isinstance(data['created_at'], str):
            try:
                data['created_at'] = datetime.fromisoformat(data['created_at'])
            except ValueError:
                pass
        
        return data


class PickleSerializer(MessageSerializer):
    """
    Pickle-based message serializer.
    
    Uses Python's pickle for efficient binary serialization.
    Faster than JSON but not human-readable or cross-language compatible.
    """
    
    def xǁPickleSerializerǁ__init____mutmut_orig(self, protocol: int = pickle.HIGHEST_PROTOCOL):
        """
        Initialize Pickle serializer.
        
        Args:
            protocol: Pickle protocol version
        """
        self.protocol = protocol
        logger.debug(f"PickleSerializer initialized (protocol={protocol})")
    
    def xǁPickleSerializerǁ__init____mutmut_1(self, protocol: int = pickle.HIGHEST_PROTOCOL):
        """
        Initialize Pickle serializer.
        
        Args:
            protocol: Pickle protocol version
        """
        self.protocol = None
        logger.debug(f"PickleSerializer initialized (protocol={protocol})")
    
    def xǁPickleSerializerǁ__init____mutmut_2(self, protocol: int = pickle.HIGHEST_PROTOCOL):
        """
        Initialize Pickle serializer.
        
        Args:
            protocol: Pickle protocol version
        """
        self.protocol = protocol
        logger.debug(None)
    
    xǁPickleSerializerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPickleSerializerǁ__init____mutmut_1': xǁPickleSerializerǁ__init____mutmut_1, 
        'xǁPickleSerializerǁ__init____mutmut_2': xǁPickleSerializerǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPickleSerializerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPickleSerializerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPickleSerializerǁ__init____mutmut_orig)
    xǁPickleSerializerǁ__init____mutmut_orig.__name__ = 'xǁPickleSerializerǁ__init__'
    
    def xǁPickleSerializerǁserialize__mutmut_orig(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, protocol=self.protocol)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_1(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(None, protocol=self.protocol)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_2(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, protocol=None)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_3(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(protocol=self.protocol)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_4(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, )
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_5(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, protocol=self.protocol)
        
        except Exception as e:
            error_msg = None
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_6(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, protocol=self.protocol)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(None)
            raise SerializationError(error_msg) from e
    
    def xǁPickleSerializerǁserialize__mutmut_7(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, protocol=self.protocol)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(None) from e
    
    xǁPickleSerializerǁserialize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPickleSerializerǁserialize__mutmut_1': xǁPickleSerializerǁserialize__mutmut_1, 
        'xǁPickleSerializerǁserialize__mutmut_2': xǁPickleSerializerǁserialize__mutmut_2, 
        'xǁPickleSerializerǁserialize__mutmut_3': xǁPickleSerializerǁserialize__mutmut_3, 
        'xǁPickleSerializerǁserialize__mutmut_4': xǁPickleSerializerǁserialize__mutmut_4, 
        'xǁPickleSerializerǁserialize__mutmut_5': xǁPickleSerializerǁserialize__mutmut_5, 
        'xǁPickleSerializerǁserialize__mutmut_6': xǁPickleSerializerǁserialize__mutmut_6, 
        'xǁPickleSerializerǁserialize__mutmut_7': xǁPickleSerializerǁserialize__mutmut_7
    }
    
    def serialize(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPickleSerializerǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁPickleSerializerǁserialize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    serialize.__signature__ = _mutmut_signature(xǁPickleSerializerǁserialize__mutmut_orig)
    xǁPickleSerializerǁserialize__mutmut_orig.__name__ = 'xǁPickleSerializerǁserialize'
    
    def xǁPickleSerializerǁdeserialize__mutmut_orig(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_1(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = None
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_2(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(None)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_3(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_4(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    None
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_5(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(None)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_6(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = None
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_7(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(None)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_8(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(None) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_9(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = None
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_10(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(None)
            raise DeserializationError(error_msg) from e
    
    def xǁPickleSerializerǁdeserialize__mutmut_11(self, data: bytes) -> AgentMessage:
        """Deserialize pickle bytes to message."""
        try:
            message = pickle.loads(data)
            
            # Validate it's an AgentMessage
            if not isinstance(message, AgentMessage):
                raise DeserializationError(
                    f"Expected AgentMessage, got {type(message)}"
                )
            
            return message
        
        except pickle.UnpicklingError as e:
            error_msg = f"Failed to unpickle message: {e}"
            logger.error(error_msg)
            raise DeserializationError(error_msg) from e
        
        except Exception as e:
            error_msg = f"Failed to deserialize pickled message: {e}"
            logger.error(error_msg)
            raise DeserializationError(None) from e
    
    xǁPickleSerializerǁdeserialize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPickleSerializerǁdeserialize__mutmut_1': xǁPickleSerializerǁdeserialize__mutmut_1, 
        'xǁPickleSerializerǁdeserialize__mutmut_2': xǁPickleSerializerǁdeserialize__mutmut_2, 
        'xǁPickleSerializerǁdeserialize__mutmut_3': xǁPickleSerializerǁdeserialize__mutmut_3, 
        'xǁPickleSerializerǁdeserialize__mutmut_4': xǁPickleSerializerǁdeserialize__mutmut_4, 
        'xǁPickleSerializerǁdeserialize__mutmut_5': xǁPickleSerializerǁdeserialize__mutmut_5, 
        'xǁPickleSerializerǁdeserialize__mutmut_6': xǁPickleSerializerǁdeserialize__mutmut_6, 
        'xǁPickleSerializerǁdeserialize__mutmut_7': xǁPickleSerializerǁdeserialize__mutmut_7, 
        'xǁPickleSerializerǁdeserialize__mutmut_8': xǁPickleSerializerǁdeserialize__mutmut_8, 
        'xǁPickleSerializerǁdeserialize__mutmut_9': xǁPickleSerializerǁdeserialize__mutmut_9, 
        'xǁPickleSerializerǁdeserialize__mutmut_10': xǁPickleSerializerǁdeserialize__mutmut_10, 
        'xǁPickleSerializerǁdeserialize__mutmut_11': xǁPickleSerializerǁdeserialize__mutmut_11
    }
    
    def deserialize(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPickleSerializerǁdeserialize__mutmut_orig"), object.__getattribute__(self, "xǁPickleSerializerǁdeserialize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    deserialize.__signature__ = _mutmut_signature(xǁPickleSerializerǁdeserialize__mutmut_orig)
    xǁPickleSerializerǁdeserialize__mutmut_orig.__name__ = 'xǁPickleSerializerǁdeserialize'
    
    def get_format(self) -> SerializationFormat:
        """Get serialization format."""
        return SerializationFormat.PICKLE


class SerializerFactory:
    """
    Factory for creating message serializers.
    
    Provides a centralized way to obtain serializer instances.
    """
    
    _serializers: Dict[SerializationFormat, Type[MessageSerializer]] = {
        SerializationFormat.JSON: JSONSerializer,
        SerializationFormat.PICKLE: PickleSerializer,
    }
    
    @classmethod
    def create(
        cls,
        format: SerializationFormat,
        **kwargs: Any,
    ) -> MessageSerializer:
        """
        Create a serializer for the specified format.
        
        Args:
            format: Serialization format
            **kwargs: Additional arguments for the serializer
            
        Returns:
            Message serializer instance
            
        Raises:
            ValueError: If format is not supported
        """
        if format not in cls._serializers:
            raise ValueError(f"Unsupported serialization format: {format}")
        
        serializer_class = cls._serializers[format]
        return serializer_class(**kwargs)
    
    @classmethod
    def register_serializer(
        cls,
        format: SerializationFormat,
        serializer_class: Type[MessageSerializer],
    ) -> None:
        """
        Register a custom serializer.
        
        Args:
            format: Serialization format
            serializer_class: Serializer class
        """
        cls._serializers[format] = serializer_class
        logger.info(f"Registered serializer for format: {format}")
    
    @classmethod
    def get_supported_formats(cls) -> list[SerializationFormat]:
        """
        Get list of supported serialization formats.
        
        Returns:
            List of supported formats
        """
        return list(cls._serializers.keys())


class MessageCodec:
    """
    High-level codec for encoding/decoding messages.
    
    Provides a simple interface for serializing and deserializing
    messages with automatic format detection.
    """
    
    def xǁMessageCodecǁ__init____mutmut_orig(
        self,
        default_format: SerializationFormat = SerializationFormat.JSON,
    ):
        """
        Initialize message codec.
        
        Args:
            default_format: Default serialization format
        """
        self.default_format = default_format
        self.serializer = SerializerFactory.create(default_format)
        logger.info(f"MessageCodec initialized (format={default_format})")
    
    def xǁMessageCodecǁ__init____mutmut_1(
        self,
        default_format: SerializationFormat = SerializationFormat.JSON,
    ):
        """
        Initialize message codec.
        
        Args:
            default_format: Default serialization format
        """
        self.default_format = None
        self.serializer = SerializerFactory.create(default_format)
        logger.info(f"MessageCodec initialized (format={default_format})")
    
    def xǁMessageCodecǁ__init____mutmut_2(
        self,
        default_format: SerializationFormat = SerializationFormat.JSON,
    ):
        """
        Initialize message codec.
        
        Args:
            default_format: Default serialization format
        """
        self.default_format = default_format
        self.serializer = None
        logger.info(f"MessageCodec initialized (format={default_format})")
    
    def xǁMessageCodecǁ__init____mutmut_3(
        self,
        default_format: SerializationFormat = SerializationFormat.JSON,
    ):
        """
        Initialize message codec.
        
        Args:
            default_format: Default serialization format
        """
        self.default_format = default_format
        self.serializer = SerializerFactory.create(None)
        logger.info(f"MessageCodec initialized (format={default_format})")
    
    def xǁMessageCodecǁ__init____mutmut_4(
        self,
        default_format: SerializationFormat = SerializationFormat.JSON,
    ):
        """
        Initialize message codec.
        
        Args:
            default_format: Default serialization format
        """
        self.default_format = default_format
        self.serializer = SerializerFactory.create(default_format)
        logger.info(None)
    
    xǁMessageCodecǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageCodecǁ__init____mutmut_1': xǁMessageCodecǁ__init____mutmut_1, 
        'xǁMessageCodecǁ__init____mutmut_2': xǁMessageCodecǁ__init____mutmut_2, 
        'xǁMessageCodecǁ__init____mutmut_3': xǁMessageCodecǁ__init____mutmut_3, 
        'xǁMessageCodecǁ__init____mutmut_4': xǁMessageCodecǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageCodecǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁMessageCodecǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁMessageCodecǁ__init____mutmut_orig)
    xǁMessageCodecǁ__init____mutmut_orig.__name__ = 'xǁMessageCodecǁ__init__'
    
    def xǁMessageCodecǁencode__mutmut_orig(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_1(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format or format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_2(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format == self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_3(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format != self.default_format:
            serializer = None
        else:
            serializer = self.serializer
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_4(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(None)
        else:
            serializer = self.serializer
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_5(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = None
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_6(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(
            None
        )
        
        return serializer.serialize(message)
    
    def xǁMessageCodecǁencode__mutmut_7(
        self,
        message: AgentMessage,
        format: Optional[SerializationFormat] = None,
    ) -> bytes:
        """
        Encode a message to bytes.
        
        Args:
            message: Message to encode
            format: Optional format override
            
        Returns:
            Encoded message bytes
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(
            f"Encoding message {message.id} with format: "
            f"{serializer.get_format()}"
        )
        
        return serializer.serialize(None)
    
    xǁMessageCodecǁencode__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageCodecǁencode__mutmut_1': xǁMessageCodecǁencode__mutmut_1, 
        'xǁMessageCodecǁencode__mutmut_2': xǁMessageCodecǁencode__mutmut_2, 
        'xǁMessageCodecǁencode__mutmut_3': xǁMessageCodecǁencode__mutmut_3, 
        'xǁMessageCodecǁencode__mutmut_4': xǁMessageCodecǁencode__mutmut_4, 
        'xǁMessageCodecǁencode__mutmut_5': xǁMessageCodecǁencode__mutmut_5, 
        'xǁMessageCodecǁencode__mutmut_6': xǁMessageCodecǁencode__mutmut_6, 
        'xǁMessageCodecǁencode__mutmut_7': xǁMessageCodecǁencode__mutmut_7
    }
    
    def encode(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageCodecǁencode__mutmut_orig"), object.__getattribute__(self, "xǁMessageCodecǁencode__mutmut_mutants"), args, kwargs, self)
        return result 
    
    encode.__signature__ = _mutmut_signature(xǁMessageCodecǁencode__mutmut_orig)
    xǁMessageCodecǁencode__mutmut_orig.__name__ = 'xǁMessageCodecǁencode'
    
    def xǁMessageCodecǁdecode__mutmut_orig(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_1(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format or format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_2(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format == self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_3(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format != self.default_format:
            serializer = None
        else:
            serializer = self.serializer
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_4(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(None)
        else:
            serializer = self.serializer
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_5(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = None
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_6(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(None)
        
        return serializer.deserialize(data)
    
    def xǁMessageCodecǁdecode__mutmut_7(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> AgentMessage:
        """
        Decode bytes to a message.
        
        Args:
            data: Encoded message bytes
            format: Optional format override
            
        Returns:
            Decoded message
        """
        if format and format != self.default_format:
            serializer = SerializerFactory.create(format)
        else:
            serializer = self.serializer
        
        logger.debug(f"Decoding message with format: {serializer.get_format()}")
        
        return serializer.deserialize(None)
    
    xǁMessageCodecǁdecode__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageCodecǁdecode__mutmut_1': xǁMessageCodecǁdecode__mutmut_1, 
        'xǁMessageCodecǁdecode__mutmut_2': xǁMessageCodecǁdecode__mutmut_2, 
        'xǁMessageCodecǁdecode__mutmut_3': xǁMessageCodecǁdecode__mutmut_3, 
        'xǁMessageCodecǁdecode__mutmut_4': xǁMessageCodecǁdecode__mutmut_4, 
        'xǁMessageCodecǁdecode__mutmut_5': xǁMessageCodecǁdecode__mutmut_5, 
        'xǁMessageCodecǁdecode__mutmut_6': xǁMessageCodecǁdecode__mutmut_6, 
        'xǁMessageCodecǁdecode__mutmut_7': xǁMessageCodecǁdecode__mutmut_7
    }
    
    def decode(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageCodecǁdecode__mutmut_orig"), object.__getattribute__(self, "xǁMessageCodecǁdecode__mutmut_mutants"), args, kwargs, self)
        return result 
    
    decode.__signature__ = _mutmut_signature(xǁMessageCodecǁdecode__mutmut_orig)
    xǁMessageCodecǁdecode__mutmut_orig.__name__ = 'xǁMessageCodecǁdecode'
    
    def xǁMessageCodecǁencode_payload__mutmut_orig(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(payload, default=self._json_default)
        except Exception as e:
            logger.error(f"Failed to encode payload: {e}")
            raise SerializationError(f"Failed to encode payload: {e}") from e
    
    def xǁMessageCodecǁencode_payload__mutmut_1(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(None, default=self._json_default)
        except Exception as e:
            logger.error(f"Failed to encode payload: {e}")
            raise SerializationError(f"Failed to encode payload: {e}") from e
    
    def xǁMessageCodecǁencode_payload__mutmut_2(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(payload, default=None)
        except Exception as e:
            logger.error(f"Failed to encode payload: {e}")
            raise SerializationError(f"Failed to encode payload: {e}") from e
    
    def xǁMessageCodecǁencode_payload__mutmut_3(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(default=self._json_default)
        except Exception as e:
            logger.error(f"Failed to encode payload: {e}")
            raise SerializationError(f"Failed to encode payload: {e}") from e
    
    def xǁMessageCodecǁencode_payload__mutmut_4(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(payload, )
        except Exception as e:
            logger.error(f"Failed to encode payload: {e}")
            raise SerializationError(f"Failed to encode payload: {e}") from e
    
    def xǁMessageCodecǁencode_payload__mutmut_5(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(payload, default=self._json_default)
        except Exception as e:
            logger.error(None)
            raise SerializationError(f"Failed to encode payload: {e}") from e
    
    def xǁMessageCodecǁencode_payload__mutmut_6(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload dict to JSON string.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(payload, default=self._json_default)
        except Exception as e:
            logger.error(f"Failed to encode payload: {e}")
            raise SerializationError(None) from e
    
    xǁMessageCodecǁencode_payload__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageCodecǁencode_payload__mutmut_1': xǁMessageCodecǁencode_payload__mutmut_1, 
        'xǁMessageCodecǁencode_payload__mutmut_2': xǁMessageCodecǁencode_payload__mutmut_2, 
        'xǁMessageCodecǁencode_payload__mutmut_3': xǁMessageCodecǁencode_payload__mutmut_3, 
        'xǁMessageCodecǁencode_payload__mutmut_4': xǁMessageCodecǁencode_payload__mutmut_4, 
        'xǁMessageCodecǁencode_payload__mutmut_5': xǁMessageCodecǁencode_payload__mutmut_5, 
        'xǁMessageCodecǁencode_payload__mutmut_6': xǁMessageCodecǁencode_payload__mutmut_6
    }
    
    def encode_payload(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageCodecǁencode_payload__mutmut_orig"), object.__getattribute__(self, "xǁMessageCodecǁencode_payload__mutmut_mutants"), args, kwargs, self)
        return result 
    
    encode_payload.__signature__ = _mutmut_signature(xǁMessageCodecǁencode_payload__mutmut_orig)
    xǁMessageCodecǁencode_payload__mutmut_orig.__name__ = 'xǁMessageCodecǁencode_payload'
    
    def xǁMessageCodecǁdecode_payload__mutmut_orig(self, payload_str: str) -> Dict[str, Any]:
        """
        Decode a JSON string to payload dict.
        
        Args:
            payload_str: JSON string
            
        Returns:
            Payload dictionary
        """
        try:
            return json.loads(payload_str)
        except Exception as e:
            logger.error(f"Failed to decode payload: {e}")
            raise DeserializationError(f"Failed to decode payload: {e}") from e
    
    def xǁMessageCodecǁdecode_payload__mutmut_1(self, payload_str: str) -> Dict[str, Any]:
        """
        Decode a JSON string to payload dict.
        
        Args:
            payload_str: JSON string
            
        Returns:
            Payload dictionary
        """
        try:
            return json.loads(None)
        except Exception as e:
            logger.error(f"Failed to decode payload: {e}")
            raise DeserializationError(f"Failed to decode payload: {e}") from e
    
    def xǁMessageCodecǁdecode_payload__mutmut_2(self, payload_str: str) -> Dict[str, Any]:
        """
        Decode a JSON string to payload dict.
        
        Args:
            payload_str: JSON string
            
        Returns:
            Payload dictionary
        """
        try:
            return json.loads(payload_str)
        except Exception as e:
            logger.error(None)
            raise DeserializationError(f"Failed to decode payload: {e}") from e
    
    def xǁMessageCodecǁdecode_payload__mutmut_3(self, payload_str: str) -> Dict[str, Any]:
        """
        Decode a JSON string to payload dict.
        
        Args:
            payload_str: JSON string
            
        Returns:
            Payload dictionary
        """
        try:
            return json.loads(payload_str)
        except Exception as e:
            logger.error(f"Failed to decode payload: {e}")
            raise DeserializationError(None) from e
    
    xǁMessageCodecǁdecode_payload__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageCodecǁdecode_payload__mutmut_1': xǁMessageCodecǁdecode_payload__mutmut_1, 
        'xǁMessageCodecǁdecode_payload__mutmut_2': xǁMessageCodecǁdecode_payload__mutmut_2, 
        'xǁMessageCodecǁdecode_payload__mutmut_3': xǁMessageCodecǁdecode_payload__mutmut_3
    }
    
    def decode_payload(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageCodecǁdecode_payload__mutmut_orig"), object.__getattribute__(self, "xǁMessageCodecǁdecode_payload__mutmut_mutants"), args, kwargs, self)
        return result 
    
    decode_payload.__signature__ = _mutmut_signature(xǁMessageCodecǁdecode_payload__mutmut_orig)
    xǁMessageCodecǁdecode_payload__mutmut_orig.__name__ = 'xǁMessageCodecǁdecode_payload'
    
    @staticmethod
    def _json_default(obj: Any) -> Any:
        """Handle non-serializable objects in payload."""
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, 'model_dump'):
            # Pydantic model
            return obj.model_dump(mode='json')
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# Default codec instance
default_codec = MessageCodec(SerializationFormat.JSON)


def x_encode_message__mutmut_orig(
    message: AgentMessage,
    format: SerializationFormat = SerializationFormat.JSON,
) -> bytes:
    """
    Convenience function to encode a message.
    
    Args:
        message: Message to encode
        format: Serialization format
        
    Returns:
        Encoded message bytes
    """
    return default_codec.encode(message, format)


def x_encode_message__mutmut_1(
    message: AgentMessage,
    format: SerializationFormat = SerializationFormat.JSON,
) -> bytes:
    """
    Convenience function to encode a message.
    
    Args:
        message: Message to encode
        format: Serialization format
        
    Returns:
        Encoded message bytes
    """
    return default_codec.encode(None, format)


def x_encode_message__mutmut_2(
    message: AgentMessage,
    format: SerializationFormat = SerializationFormat.JSON,
) -> bytes:
    """
    Convenience function to encode a message.
    
    Args:
        message: Message to encode
        format: Serialization format
        
    Returns:
        Encoded message bytes
    """
    return default_codec.encode(message, None)


def x_encode_message__mutmut_3(
    message: AgentMessage,
    format: SerializationFormat = SerializationFormat.JSON,
) -> bytes:
    """
    Convenience function to encode a message.
    
    Args:
        message: Message to encode
        format: Serialization format
        
    Returns:
        Encoded message bytes
    """
    return default_codec.encode(format)


def x_encode_message__mutmut_4(
    message: AgentMessage,
    format: SerializationFormat = SerializationFormat.JSON,
) -> bytes:
    """
    Convenience function to encode a message.
    
    Args:
        message: Message to encode
        format: Serialization format
        
    Returns:
        Encoded message bytes
    """
    return default_codec.encode(message, )

x_encode_message__mutmut_mutants : ClassVar[MutantDict] = {
'x_encode_message__mutmut_1': x_encode_message__mutmut_1, 
    'x_encode_message__mutmut_2': x_encode_message__mutmut_2, 
    'x_encode_message__mutmut_3': x_encode_message__mutmut_3, 
    'x_encode_message__mutmut_4': x_encode_message__mutmut_4
}

def encode_message(*args, **kwargs):
    result = _mutmut_trampoline(x_encode_message__mutmut_orig, x_encode_message__mutmut_mutants, args, kwargs)
    return result 

encode_message.__signature__ = _mutmut_signature(x_encode_message__mutmut_orig)
x_encode_message__mutmut_orig.__name__ = 'x_encode_message'


def x_decode_message__mutmut_orig(
    data: bytes,
    format: SerializationFormat = SerializationFormat.JSON,
) -> AgentMessage:
    """
    Convenience function to decode a message.
    
    Args:
        data: Encoded message bytes
        format: Serialization format
        
    Returns:
        Decoded message
    """
    return default_codec.decode(data, format)


def x_decode_message__mutmut_1(
    data: bytes,
    format: SerializationFormat = SerializationFormat.JSON,
) -> AgentMessage:
    """
    Convenience function to decode a message.
    
    Args:
        data: Encoded message bytes
        format: Serialization format
        
    Returns:
        Decoded message
    """
    return default_codec.decode(None, format)


def x_decode_message__mutmut_2(
    data: bytes,
    format: SerializationFormat = SerializationFormat.JSON,
) -> AgentMessage:
    """
    Convenience function to decode a message.
    
    Args:
        data: Encoded message bytes
        format: Serialization format
        
    Returns:
        Decoded message
    """
    return default_codec.decode(data, None)


def x_decode_message__mutmut_3(
    data: bytes,
    format: SerializationFormat = SerializationFormat.JSON,
) -> AgentMessage:
    """
    Convenience function to decode a message.
    
    Args:
        data: Encoded message bytes
        format: Serialization format
        
    Returns:
        Decoded message
    """
    return default_codec.decode(format)


def x_decode_message__mutmut_4(
    data: bytes,
    format: SerializationFormat = SerializationFormat.JSON,
) -> AgentMessage:
    """
    Convenience function to decode a message.
    
    Args:
        data: Encoded message bytes
        format: Serialization format
        
    Returns:
        Decoded message
    """
    return default_codec.decode(data, )

x_decode_message__mutmut_mutants : ClassVar[MutantDict] = {
'x_decode_message__mutmut_1': x_decode_message__mutmut_1, 
    'x_decode_message__mutmut_2': x_decode_message__mutmut_2, 
    'x_decode_message__mutmut_3': x_decode_message__mutmut_3, 
    'x_decode_message__mutmut_4': x_decode_message__mutmut_4
}

def decode_message(*args, **kwargs):
    result = _mutmut_trampoline(x_decode_message__mutmut_orig, x_decode_message__mutmut_mutants, args, kwargs)
    return result 

decode_message.__signature__ = _mutmut_signature(x_decode_message__mutmut_orig)
x_decode_message__mutmut_orig.__name__ = 'x_decode_message'
