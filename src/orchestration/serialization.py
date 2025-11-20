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
    
    def __init__(self, pretty: bool = False):
        """
        Initialize JSON serializer.
        
        Args:
            pretty: Whether to pretty-print JSON
        """
        self.pretty = pretty
        logger.debug(f"JSONSerializer initialized (pretty={pretty})")
    
    def serialize(self, message: AgentMessage) -> bytes:
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
    
    def deserialize(self, data: bytes) -> AgentMessage:
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
    
    def __init__(self, protocol: int = pickle.HIGHEST_PROTOCOL):
        """
        Initialize Pickle serializer.
        
        Args:
            protocol: Pickle protocol version
        """
        self.protocol = protocol
        logger.debug(f"PickleSerializer initialized (protocol={protocol})")
    
    def serialize(self, message: AgentMessage) -> bytes:
        """Serialize message using pickle."""
        try:
            return pickle.dumps(message, protocol=self.protocol)
        
        except Exception as e:
            error_msg = f"Failed to pickle message: {e}"
            logger.error(error_msg)
            raise SerializationError(error_msg) from e
    
    def deserialize(self, data: bytes) -> AgentMessage:
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
    
    def __init__(
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
    
    def encode(
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
    
    def decode(
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
    
    def encode_payload(self, payload: Dict[str, Any]) -> str:
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
    
    def decode_payload(self, payload_str: str) -> Dict[str, Any]:
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


def encode_message(
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


def decode_message(
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
