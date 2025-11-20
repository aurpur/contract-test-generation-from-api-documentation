"""
Communication protocol for inter-agent messaging.

This module defines the protocol and interfaces for agents to communicate
with each other during the test generation workflow.

Author: Aurel IKAMA HONEY
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID, uuid4

from utils.logging import logger
from shared_context import AgentMessage, AgentType
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


class MessagePriority(int, Enum):
    """Message priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3


class MessageStatus(str, Enum):
    """Message processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CommunicationProtocol(ABC):
    """
    Abstract base class for communication protocols.
    
    Defines the interface that all communication protocols must implement
    for inter-agent messaging.
    """
    
    @abstractmethod
    async def send_message(
        self,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        session_id: UUID,
        priority: MessagePriority = MessagePriority.NORMAL,
        parent_message_id: Optional[UUID] = None,
    ) -> AgentMessage:
        """
        Send a message from one agent to another.
        
        Args:
            from_agent: Sender agent type
            to_agent: Receiver agent type
            message_type: Type of message
            payload: Message payload
            session_id: Workflow session ID
            priority: Message priority
            parent_message_id: Optional parent message ID
            
        Returns:
            Created agent message
        """
        pass
    
    @abstractmethod
    async def receive_messages(
        self,
        agent: AgentType,
        session_id: UUID,
        limit: int = 10,
    ) -> List[AgentMessage]:
        """
        Receive pending messages for an agent.
        
        Args:
            agent: Agent type receiving messages
            session_id: Workflow session ID
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of pending messages
        """
        pass
    
    @abstractmethod
    async def acknowledge_message(
        self,
        message_id: UUID,
        status: MessageStatus,
    ) -> None:
        """
        Acknowledge processing of a message.
        
        Args:
            message_id: Message UUID
            status: Processing status
        """
        pass
    
    @abstractmethod
    async def broadcast_message(
        self,
        from_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        session_id: UUID,
        exclude_agents: Optional[List[AgentType]] = None,
    ) -> List[AgentMessage]:
        """
        Broadcast a message to all agents (except excluded ones).
        
        Args:
            from_agent: Sender agent type
            message_type: Type of message
            payload: Message payload
            session_id: Workflow session ID
            exclude_agents: Agents to exclude from broadcast
            
        Returns:
            List of created messages
        """
        pass


class MessageHandler(ABC):
    """
    Abstract base class for message handlers.
    
    Agents implement message handlers to process different types of messages.
    """
    
    @abstractmethod
    async def handle_message(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Handle a received message.
        
        Args:
            message: Message to handle
            
        Returns:
            Response payload
        """
        pass
    
    @abstractmethod
    def can_handle(self, message_type: str) -> bool:
        """
        Check if this handler can process a message type.
        
        Args:
            message_type: Type of message
            
        Returns:
            True if can handle, False otherwise
        """
        pass


class MessageRouter:
    """
    Routes messages to appropriate handlers based on message type.
    
    Each agent has a message router that dispatches incoming messages
    to registered handlers.
    """
    
    def xǁMessageRouterǁ__init____mutmut_orig(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = None
        logger.debug("MessageRouter initialized")
    
    def xǁMessageRouterǁ__init____mutmut_1(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = None
        self.default_handler: Optional[MessageHandler] = None
        logger.debug("MessageRouter initialized")
    
    def xǁMessageRouterǁ__init____mutmut_2(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = ""
        logger.debug("MessageRouter initialized")
    
    def xǁMessageRouterǁ__init____mutmut_3(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = None
        logger.debug(None)
    
    def xǁMessageRouterǁ__init____mutmut_4(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = None
        logger.debug("XXMessageRouter initializedXX")
    
    def xǁMessageRouterǁ__init____mutmut_5(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = None
        logger.debug("messagerouter initialized")
    
    def xǁMessageRouterǁ__init____mutmut_6(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = None
        logger.debug("MESSAGEROUTER INITIALIZED")
    
    xǁMessageRouterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageRouterǁ__init____mutmut_1': xǁMessageRouterǁ__init____mutmut_1, 
        'xǁMessageRouterǁ__init____mutmut_2': xǁMessageRouterǁ__init____mutmut_2, 
        'xǁMessageRouterǁ__init____mutmut_3': xǁMessageRouterǁ__init____mutmut_3, 
        'xǁMessageRouterǁ__init____mutmut_4': xǁMessageRouterǁ__init____mutmut_4, 
        'xǁMessageRouterǁ__init____mutmut_5': xǁMessageRouterǁ__init____mutmut_5, 
        'xǁMessageRouterǁ__init____mutmut_6': xǁMessageRouterǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageRouterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁMessageRouterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁMessageRouterǁ__init____mutmut_orig)
    xǁMessageRouterǁ__init____mutmut_orig.__name__ = 'xǁMessageRouterǁ__init__'
    
    def xǁMessageRouterǁregister_handler__mutmut_orig(
        self,
        message_type: str,
        handler: MessageHandler,
    ) -> None:
        """
        Register a handler for a message type.
        
        Args:
            message_type: Type of message to handle
            handler: Handler instance
        """
        self.handlers[message_type] = handler
        logger.debug(f"Registered handler for message type: {message_type}")
    
    def xǁMessageRouterǁregister_handler__mutmut_1(
        self,
        message_type: str,
        handler: MessageHandler,
    ) -> None:
        """
        Register a handler for a message type.
        
        Args:
            message_type: Type of message to handle
            handler: Handler instance
        """
        self.handlers[message_type] = None
        logger.debug(f"Registered handler for message type: {message_type}")
    
    def xǁMessageRouterǁregister_handler__mutmut_2(
        self,
        message_type: str,
        handler: MessageHandler,
    ) -> None:
        """
        Register a handler for a message type.
        
        Args:
            message_type: Type of message to handle
            handler: Handler instance
        """
        self.handlers[message_type] = handler
        logger.debug(None)
    
    xǁMessageRouterǁregister_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageRouterǁregister_handler__mutmut_1': xǁMessageRouterǁregister_handler__mutmut_1, 
        'xǁMessageRouterǁregister_handler__mutmut_2': xǁMessageRouterǁregister_handler__mutmut_2
    }
    
    def register_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageRouterǁregister_handler__mutmut_orig"), object.__getattribute__(self, "xǁMessageRouterǁregister_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_handler.__signature__ = _mutmut_signature(xǁMessageRouterǁregister_handler__mutmut_orig)
    xǁMessageRouterǁregister_handler__mutmut_orig.__name__ = 'xǁMessageRouterǁregister_handler'
    
    def xǁMessageRouterǁregister_default_handler__mutmut_orig(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = handler
        logger.debug("Registered default message handler")
    
    def xǁMessageRouterǁregister_default_handler__mutmut_1(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = None
        logger.debug("Registered default message handler")
    
    def xǁMessageRouterǁregister_default_handler__mutmut_2(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = handler
        logger.debug(None)
    
    def xǁMessageRouterǁregister_default_handler__mutmut_3(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = handler
        logger.debug("XXRegistered default message handlerXX")
    
    def xǁMessageRouterǁregister_default_handler__mutmut_4(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = handler
        logger.debug("registered default message handler")
    
    def xǁMessageRouterǁregister_default_handler__mutmut_5(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = handler
        logger.debug("REGISTERED DEFAULT MESSAGE HANDLER")
    
    xǁMessageRouterǁregister_default_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageRouterǁregister_default_handler__mutmut_1': xǁMessageRouterǁregister_default_handler__mutmut_1, 
        'xǁMessageRouterǁregister_default_handler__mutmut_2': xǁMessageRouterǁregister_default_handler__mutmut_2, 
        'xǁMessageRouterǁregister_default_handler__mutmut_3': xǁMessageRouterǁregister_default_handler__mutmut_3, 
        'xǁMessageRouterǁregister_default_handler__mutmut_4': xǁMessageRouterǁregister_default_handler__mutmut_4, 
        'xǁMessageRouterǁregister_default_handler__mutmut_5': xǁMessageRouterǁregister_default_handler__mutmut_5
    }
    
    def register_default_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageRouterǁregister_default_handler__mutmut_orig"), object.__getattribute__(self, "xǁMessageRouterǁregister_default_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_default_handler.__signature__ = _mutmut_signature(xǁMessageRouterǁregister_default_handler__mutmut_orig)
    xǁMessageRouterǁregister_default_handler__mutmut_orig.__name__ = 'xǁMessageRouterǁregister_default_handler'
    
    async def xǁMessageRouterǁroute_message__mutmut_orig(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_1(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = None
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_2(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(None)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_3(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                None
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_4(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(None)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_5(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                None
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_6(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(None)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_7(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = None
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_8(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(None)
        raise ValueError(error_msg)
    
    async def xǁMessageRouterǁroute_message__mutmut_9(
        self,
        message: AgentMessage,
    ) -> Dict[str, Any]:
        """
        Route a message to the appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            Handler response
            
        Raises:
            ValueError: If no handler found for message type
        """
        handler = self.handlers.get(message.message_type)
        
        if handler:
            logger.debug(
                f"Routing message {message.id} to handler for type: "
                f"{message.message_type}"
            )
            return await handler.handle_message(message)
        
        if self.default_handler:
            logger.debug(
                f"Routing message {message.id} to default handler"
            )
            return await self.default_handler.handle_message(message)
        
        error_msg = (
            f"No handler found for message type: {message.message_type}"
        )
        logger.error(error_msg)
        raise ValueError(None)
    
    xǁMessageRouterǁroute_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageRouterǁroute_message__mutmut_1': xǁMessageRouterǁroute_message__mutmut_1, 
        'xǁMessageRouterǁroute_message__mutmut_2': xǁMessageRouterǁroute_message__mutmut_2, 
        'xǁMessageRouterǁroute_message__mutmut_3': xǁMessageRouterǁroute_message__mutmut_3, 
        'xǁMessageRouterǁroute_message__mutmut_4': xǁMessageRouterǁroute_message__mutmut_4, 
        'xǁMessageRouterǁroute_message__mutmut_5': xǁMessageRouterǁroute_message__mutmut_5, 
        'xǁMessageRouterǁroute_message__mutmut_6': xǁMessageRouterǁroute_message__mutmut_6, 
        'xǁMessageRouterǁroute_message__mutmut_7': xǁMessageRouterǁroute_message__mutmut_7, 
        'xǁMessageRouterǁroute_message__mutmut_8': xǁMessageRouterǁroute_message__mutmut_8, 
        'xǁMessageRouterǁroute_message__mutmut_9': xǁMessageRouterǁroute_message__mutmut_9
    }
    
    def route_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageRouterǁroute_message__mutmut_orig"), object.__getattribute__(self, "xǁMessageRouterǁroute_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    route_message.__signature__ = _mutmut_signature(xǁMessageRouterǁroute_message__mutmut_orig)
    xǁMessageRouterǁroute_message__mutmut_orig.__name__ = 'xǁMessageRouterǁroute_message'
    
    def xǁMessageRouterǁhas_handler__mutmut_orig(self, message_type: str) -> bool:
        """
        Check if a handler is registered for a message type.
        
        Args:
            message_type: Message type to check
            
        Returns:
            True if handler exists, False otherwise
        """
        return message_type in self.handlers or self.default_handler is not None
    
    def xǁMessageRouterǁhas_handler__mutmut_1(self, message_type: str) -> bool:
        """
        Check if a handler is registered for a message type.
        
        Args:
            message_type: Message type to check
            
        Returns:
            True if handler exists, False otherwise
        """
        return message_type in self.handlers and self.default_handler is not None
    
    def xǁMessageRouterǁhas_handler__mutmut_2(self, message_type: str) -> bool:
        """
        Check if a handler is registered for a message type.
        
        Args:
            message_type: Message type to check
            
        Returns:
            True if handler exists, False otherwise
        """
        return message_type not in self.handlers or self.default_handler is not None
    
    def xǁMessageRouterǁhas_handler__mutmut_3(self, message_type: str) -> bool:
        """
        Check if a handler is registered for a message type.
        
        Args:
            message_type: Message type to check
            
        Returns:
            True if handler exists, False otherwise
        """
        return message_type in self.handlers or self.default_handler is None
    
    xǁMessageRouterǁhas_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageRouterǁhas_handler__mutmut_1': xǁMessageRouterǁhas_handler__mutmut_1, 
        'xǁMessageRouterǁhas_handler__mutmut_2': xǁMessageRouterǁhas_handler__mutmut_2, 
        'xǁMessageRouterǁhas_handler__mutmut_3': xǁMessageRouterǁhas_handler__mutmut_3
    }
    
    def has_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageRouterǁhas_handler__mutmut_orig"), object.__getattribute__(self, "xǁMessageRouterǁhas_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has_handler.__signature__ = _mutmut_signature(xǁMessageRouterǁhas_handler__mutmut_orig)
    xǁMessageRouterǁhas_handler__mutmut_orig.__name__ = 'xǁMessageRouterǁhas_handler'


class EventBus:
    """
    Event bus for publish-subscribe pattern between agents.
    
    Allows agents to subscribe to events and publish events without
    direct coupling.
    """
    
    def xǁEventBusǁ__init____mutmut_orig(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        logger.debug("EventBus initialized")
    
    def xǁEventBusǁ__init____mutmut_1(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = None
        logger.debug("EventBus initialized")
    
    def xǁEventBusǁ__init____mutmut_2(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        logger.debug(None)
    
    def xǁEventBusǁ__init____mutmut_3(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        logger.debug("XXEventBus initializedXX")
    
    def xǁEventBusǁ__init____mutmut_4(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        logger.debug("eventbus initialized")
    
    def xǁEventBusǁ__init____mutmut_5(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        logger.debug("EVENTBUS INITIALIZED")
    
    xǁEventBusǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁ__init____mutmut_1': xǁEventBusǁ__init____mutmut_1, 
        'xǁEventBusǁ__init____mutmut_2': xǁEventBusǁ__init____mutmut_2, 
        'xǁEventBusǁ__init____mutmut_3': xǁEventBusǁ__init____mutmut_3, 
        'xǁEventBusǁ__init____mutmut_4': xǁEventBusǁ__init____mutmut_4, 
        'xǁEventBusǁ__init____mutmut_5': xǁEventBusǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁEventBusǁ__init____mutmut_orig)
    xǁEventBusǁ__init____mutmut_orig.__name__ = 'xǁEventBusǁ__init__'
    
    def xǁEventBusǁsubscribe__mutmut_orig(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Callback function to invoke on event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event type: {event_type}")
    
    def xǁEventBusǁsubscribe__mutmut_1(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Callback function to invoke on event
        """
        if event_type in self.subscribers:
            self.subscribers[event_type] = []
        
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event type: {event_type}")
    
    def xǁEventBusǁsubscribe__mutmut_2(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Callback function to invoke on event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = None
        
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event type: {event_type}")
    
    def xǁEventBusǁsubscribe__mutmut_3(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Callback function to invoke on event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        
        self.subscribers[event_type].append(None)
        logger.debug(f"Subscribed to event type: {event_type}")
    
    def xǁEventBusǁsubscribe__mutmut_4(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Callback function to invoke on event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        
        self.subscribers[event_type].append(callback)
        logger.debug(None)
    
    xǁEventBusǁsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁsubscribe__mutmut_1': xǁEventBusǁsubscribe__mutmut_1, 
        'xǁEventBusǁsubscribe__mutmut_2': xǁEventBusǁsubscribe__mutmut_2, 
        'xǁEventBusǁsubscribe__mutmut_3': xǁEventBusǁsubscribe__mutmut_3, 
        'xǁEventBusǁsubscribe__mutmut_4': xǁEventBusǁsubscribe__mutmut_4
    }
    
    def subscribe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁsubscribe__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁsubscribe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    subscribe.__signature__ = _mutmut_signature(xǁEventBusǁsubscribe__mutmut_orig)
    xǁEventBusǁsubscribe__mutmut_orig.__name__ = 'xǁEventBusǁsubscribe'
    
    def xǁEventBusǁunsubscribe__mutmut_orig(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Callback function to remove
        """
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from event type: {event_type}")
            except ValueError:
                logger.warning(
                    f"Callback not found in subscribers for: {event_type}"
                )
    
    def xǁEventBusǁunsubscribe__mutmut_1(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Callback function to remove
        """
        if event_type not in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from event type: {event_type}")
            except ValueError:
                logger.warning(
                    f"Callback not found in subscribers for: {event_type}"
                )
    
    def xǁEventBusǁunsubscribe__mutmut_2(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Callback function to remove
        """
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(None)
                logger.debug(f"Unsubscribed from event type: {event_type}")
            except ValueError:
                logger.warning(
                    f"Callback not found in subscribers for: {event_type}"
                )
    
    def xǁEventBusǁunsubscribe__mutmut_3(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Callback function to remove
        """
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
                logger.debug(None)
            except ValueError:
                logger.warning(
                    f"Callback not found in subscribers for: {event_type}"
                )
    
    def xǁEventBusǁunsubscribe__mutmut_4(
        self,
        event_type: str,
        callback: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Callback function to remove
        """
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from event type: {event_type}")
            except ValueError:
                logger.warning(
                    None
                )
    
    xǁEventBusǁunsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁunsubscribe__mutmut_1': xǁEventBusǁunsubscribe__mutmut_1, 
        'xǁEventBusǁunsubscribe__mutmut_2': xǁEventBusǁunsubscribe__mutmut_2, 
        'xǁEventBusǁunsubscribe__mutmut_3': xǁEventBusǁunsubscribe__mutmut_3, 
        'xǁEventBusǁunsubscribe__mutmut_4': xǁEventBusǁunsubscribe__mutmut_4
    }
    
    def unsubscribe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁunsubscribe__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁunsubscribe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    unsubscribe.__signature__ = _mutmut_signature(xǁEventBusǁunsubscribe__mutmut_orig)
    xǁEventBusǁunsubscribe__mutmut_orig.__name__ = 'xǁEventBusǁunsubscribe'
    
    async def xǁEventBusǁpublish__mutmut_orig(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_1(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_2(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(None)
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_3(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            None
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_4(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(None, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_5(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, None):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_6(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr('__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_7(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, ):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_8(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, 'XX__call__XX'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_9(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__CALL__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_10(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = None
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_11(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(None)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_12(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(None, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_13(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, None):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_14(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr('__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_15(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, ):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_16(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, 'XX__await__XX'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_17(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__AWAIT__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_18(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    None,
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_19(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=None,
                )
    
    async def xǁEventBusǁpublish__mutmut_20(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    exc_info=True,
                )
    
    async def xǁEventBusǁpublish__mutmut_21(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    )
    
    async def xǁEventBusǁpublish__mutmut_22(
        self,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        if event_type not in self.subscribers:
            logger.debug(f"No subscribers for event type: {event_type}")
            return
        
        logger.info(
            f"Publishing event '{event_type}' to "
            f"{len(self.subscribers[event_type])} subscribers"
        )
        
        for callback in self.subscribers[event_type]:
            try:
                # Support both sync and async callbacks
                if hasattr(callback, '__call__'):
                    result = callback(event_data)
                    # If it's a coroutine, await it
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_type}: {e}",
                    exc_info=False,
                )
    
    xǁEventBusǁpublish__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁpublish__mutmut_1': xǁEventBusǁpublish__mutmut_1, 
        'xǁEventBusǁpublish__mutmut_2': xǁEventBusǁpublish__mutmut_2, 
        'xǁEventBusǁpublish__mutmut_3': xǁEventBusǁpublish__mutmut_3, 
        'xǁEventBusǁpublish__mutmut_4': xǁEventBusǁpublish__mutmut_4, 
        'xǁEventBusǁpublish__mutmut_5': xǁEventBusǁpublish__mutmut_5, 
        'xǁEventBusǁpublish__mutmut_6': xǁEventBusǁpublish__mutmut_6, 
        'xǁEventBusǁpublish__mutmut_7': xǁEventBusǁpublish__mutmut_7, 
        'xǁEventBusǁpublish__mutmut_8': xǁEventBusǁpublish__mutmut_8, 
        'xǁEventBusǁpublish__mutmut_9': xǁEventBusǁpublish__mutmut_9, 
        'xǁEventBusǁpublish__mutmut_10': xǁEventBusǁpublish__mutmut_10, 
        'xǁEventBusǁpublish__mutmut_11': xǁEventBusǁpublish__mutmut_11, 
        'xǁEventBusǁpublish__mutmut_12': xǁEventBusǁpublish__mutmut_12, 
        'xǁEventBusǁpublish__mutmut_13': xǁEventBusǁpublish__mutmut_13, 
        'xǁEventBusǁpublish__mutmut_14': xǁEventBusǁpublish__mutmut_14, 
        'xǁEventBusǁpublish__mutmut_15': xǁEventBusǁpublish__mutmut_15, 
        'xǁEventBusǁpublish__mutmut_16': xǁEventBusǁpublish__mutmut_16, 
        'xǁEventBusǁpublish__mutmut_17': xǁEventBusǁpublish__mutmut_17, 
        'xǁEventBusǁpublish__mutmut_18': xǁEventBusǁpublish__mutmut_18, 
        'xǁEventBusǁpublish__mutmut_19': xǁEventBusǁpublish__mutmut_19, 
        'xǁEventBusǁpublish__mutmut_20': xǁEventBusǁpublish__mutmut_20, 
        'xǁEventBusǁpublish__mutmut_21': xǁEventBusǁpublish__mutmut_21, 
        'xǁEventBusǁpublish__mutmut_22': xǁEventBusǁpublish__mutmut_22
    }
    
    def publish(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁpublish__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁpublish__mutmut_mutants"), args, kwargs, self)
        return result 
    
    publish.__signature__ = _mutmut_signature(xǁEventBusǁpublish__mutmut_orig)
    xǁEventBusǁpublish__mutmut_orig.__name__ = 'xǁEventBusǁpublish'
    
    def get_subscriber_count(self, event_type: str) -> int:
        """
        Get the number of subscribers for an event type.
        
        Args:
            event_type: Event type
            
        Returns:
            Number of subscribers
        """
        return len(self.subscribers.get(event_type, []))


class MessageBuilder:
    """
    Builder pattern for constructing agent messages.
    
    Provides a fluent interface for creating complex messages.
    """
    
    def xǁMessageBuilderǁ__init____mutmut_orig(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_1(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = ""
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_2(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = ""
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_3(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = ""
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_4(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = None
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_5(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = ""
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_6(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = None
        self._parent_message_id: Optional[UUID] = None
    
    def xǁMessageBuilderǁ__init____mutmut_7(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = ""
    
    xǁMessageBuilderǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁ__init____mutmut_1': xǁMessageBuilderǁ__init____mutmut_1, 
        'xǁMessageBuilderǁ__init____mutmut_2': xǁMessageBuilderǁ__init____mutmut_2, 
        'xǁMessageBuilderǁ__init____mutmut_3': xǁMessageBuilderǁ__init____mutmut_3, 
        'xǁMessageBuilderǁ__init____mutmut_4': xǁMessageBuilderǁ__init____mutmut_4, 
        'xǁMessageBuilderǁ__init____mutmut_5': xǁMessageBuilderǁ__init____mutmut_5, 
        'xǁMessageBuilderǁ__init____mutmut_6': xǁMessageBuilderǁ__init____mutmut_6, 
        'xǁMessageBuilderǁ__init____mutmut_7': xǁMessageBuilderǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁMessageBuilderǁ__init____mutmut_orig)
    xǁMessageBuilderǁ__init____mutmut_orig.__name__ = 'xǁMessageBuilderǁ__init__'
    
    def xǁMessageBuilderǁfrom_agent__mutmut_orig(self, agent: AgentType) -> 'MessageBuilder':
        """Set the sender agent."""
        self._from_agent = agent
        return self
    
    def xǁMessageBuilderǁfrom_agent__mutmut_1(self, agent: AgentType) -> 'MessageBuilder':
        """Set the sender agent."""
        self._from_agent = None
        return self
    
    xǁMessageBuilderǁfrom_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁfrom_agent__mutmut_1': xǁMessageBuilderǁfrom_agent__mutmut_1
    }
    
    def from_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁfrom_agent__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁfrom_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    from_agent.__signature__ = _mutmut_signature(xǁMessageBuilderǁfrom_agent__mutmut_orig)
    xǁMessageBuilderǁfrom_agent__mutmut_orig.__name__ = 'xǁMessageBuilderǁfrom_agent'
    
    def xǁMessageBuilderǁto_agent__mutmut_orig(self, agent: AgentType) -> 'MessageBuilder':
        """Set the receiver agent."""
        self._to_agent = agent
        return self
    
    def xǁMessageBuilderǁto_agent__mutmut_1(self, agent: AgentType) -> 'MessageBuilder':
        """Set the receiver agent."""
        self._to_agent = None
        return self
    
    xǁMessageBuilderǁto_agent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁto_agent__mutmut_1': xǁMessageBuilderǁto_agent__mutmut_1
    }
    
    def to_agent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁto_agent__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁto_agent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_agent.__signature__ = _mutmut_signature(xǁMessageBuilderǁto_agent__mutmut_orig)
    xǁMessageBuilderǁto_agent__mutmut_orig.__name__ = 'xǁMessageBuilderǁto_agent'
    
    def xǁMessageBuilderǁwith_type__mutmut_orig(self, message_type: str) -> 'MessageBuilder':
        """Set the message type."""
        self._message_type = message_type
        return self
    
    def xǁMessageBuilderǁwith_type__mutmut_1(self, message_type: str) -> 'MessageBuilder':
        """Set the message type."""
        self._message_type = None
        return self
    
    xǁMessageBuilderǁwith_type__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁwith_type__mutmut_1': xǁMessageBuilderǁwith_type__mutmut_1
    }
    
    def with_type(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁwith_type__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁwith_type__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_type.__signature__ = _mutmut_signature(xǁMessageBuilderǁwith_type__mutmut_orig)
    xǁMessageBuilderǁwith_type__mutmut_orig.__name__ = 'xǁMessageBuilderǁwith_type'
    
    def xǁMessageBuilderǁwith_payload__mutmut_orig(self, payload: Dict[str, Any]) -> 'MessageBuilder':
        """Set the message payload."""
        self._payload = payload
        return self
    
    def xǁMessageBuilderǁwith_payload__mutmut_1(self, payload: Dict[str, Any]) -> 'MessageBuilder':
        """Set the message payload."""
        self._payload = None
        return self
    
    xǁMessageBuilderǁwith_payload__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁwith_payload__mutmut_1': xǁMessageBuilderǁwith_payload__mutmut_1
    }
    
    def with_payload(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁwith_payload__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁwith_payload__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_payload.__signature__ = _mutmut_signature(xǁMessageBuilderǁwith_payload__mutmut_orig)
    xǁMessageBuilderǁwith_payload__mutmut_orig.__name__ = 'xǁMessageBuilderǁwith_payload'
    
    def xǁMessageBuilderǁadd_to_payload__mutmut_orig(self, key: str, value: Any) -> 'MessageBuilder':
        """Add a key-value pair to the payload."""
        self._payload[key] = value
        return self
    
    def xǁMessageBuilderǁadd_to_payload__mutmut_1(self, key: str, value: Any) -> 'MessageBuilder':
        """Add a key-value pair to the payload."""
        self._payload[key] = None
        return self
    
    xǁMessageBuilderǁadd_to_payload__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁadd_to_payload__mutmut_1': xǁMessageBuilderǁadd_to_payload__mutmut_1
    }
    
    def add_to_payload(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁadd_to_payload__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁadd_to_payload__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_to_payload.__signature__ = _mutmut_signature(xǁMessageBuilderǁadd_to_payload__mutmut_orig)
    xǁMessageBuilderǁadd_to_payload__mutmut_orig.__name__ = 'xǁMessageBuilderǁadd_to_payload'
    
    def xǁMessageBuilderǁfor_session__mutmut_orig(self, session_id: UUID) -> 'MessageBuilder':
        """Set the session ID."""
        self._session_id = session_id
        return self
    
    def xǁMessageBuilderǁfor_session__mutmut_1(self, session_id: UUID) -> 'MessageBuilder':
        """Set the session ID."""
        self._session_id = None
        return self
    
    xǁMessageBuilderǁfor_session__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁfor_session__mutmut_1': xǁMessageBuilderǁfor_session__mutmut_1
    }
    
    def for_session(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁfor_session__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁfor_session__mutmut_mutants"), args, kwargs, self)
        return result 
    
    for_session.__signature__ = _mutmut_signature(xǁMessageBuilderǁfor_session__mutmut_orig)
    xǁMessageBuilderǁfor_session__mutmut_orig.__name__ = 'xǁMessageBuilderǁfor_session'
    
    def xǁMessageBuilderǁwith_priority__mutmut_orig(self, priority: MessagePriority) -> 'MessageBuilder':
        """Set the message priority."""
        self._priority = priority
        return self
    
    def xǁMessageBuilderǁwith_priority__mutmut_1(self, priority: MessagePriority) -> 'MessageBuilder':
        """Set the message priority."""
        self._priority = None
        return self
    
    xǁMessageBuilderǁwith_priority__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁwith_priority__mutmut_1': xǁMessageBuilderǁwith_priority__mutmut_1
    }
    
    def with_priority(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁwith_priority__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁwith_priority__mutmut_mutants"), args, kwargs, self)
        return result 
    
    with_priority.__signature__ = _mutmut_signature(xǁMessageBuilderǁwith_priority__mutmut_orig)
    xǁMessageBuilderǁwith_priority__mutmut_orig.__name__ = 'xǁMessageBuilderǁwith_priority'
    
    def xǁMessageBuilderǁin_reply_to__mutmut_orig(self, message_id: UUID) -> 'MessageBuilder':
        """Set the parent message ID."""
        self._parent_message_id = message_id
        return self
    
    def xǁMessageBuilderǁin_reply_to__mutmut_1(self, message_id: UUID) -> 'MessageBuilder':
        """Set the parent message ID."""
        self._parent_message_id = None
        return self
    
    xǁMessageBuilderǁin_reply_to__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁin_reply_to__mutmut_1': xǁMessageBuilderǁin_reply_to__mutmut_1
    }
    
    def in_reply_to(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁin_reply_to__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁin_reply_to__mutmut_mutants"), args, kwargs, self)
        return result 
    
    in_reply_to.__signature__ = _mutmut_signature(xǁMessageBuilderǁin_reply_to__mutmut_orig)
    xǁMessageBuilderǁin_reply_to__mutmut_orig.__name__ = 'xǁMessageBuilderǁin_reply_to'
    
    def xǁMessageBuilderǁbuild__mutmut_orig(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_1(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_2(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError(None)
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_3(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("XXfrom_agent is requiredXX")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_4(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("FROM_AGENT IS REQUIRED")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_5(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_6(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError(None)
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_7(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("XXto_agent is requiredXX")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_8(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("TO_AGENT IS REQUIRED")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_9(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_10(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError(None)
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_11(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("XXmessage_type is requiredXX")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_12(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("MESSAGE_TYPE IS REQUIRED")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_13(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_14(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError(None)
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_15(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("XXsession_id is requiredXX")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_16(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("SESSION_ID IS REQUIRED")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_17(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=None,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_18(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=None,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_19(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=None,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_20(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=None,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_21(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=None,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_22(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=None,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_23(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=None,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_24(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_25(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_26(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_27(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            session_id=self._session_id,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_28(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            priority=self._priority,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_29(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            parent_message_id=self._parent_message_id,
        )
    
    def xǁMessageBuilderǁbuild__mutmut_30(self) -> AgentMessage:
        """
        Build the agent message.
        
        Returns:
            Constructed agent message
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._from_agent:
            raise ValueError("from_agent is required")
        if not self._to_agent:
            raise ValueError("to_agent is required")
        if not self._message_type:
            raise ValueError("message_type is required")
        if not self._session_id:
            raise ValueError("session_id is required")
        
        return AgentMessage(
            from_agent=self._from_agent,
            to_agent=self._to_agent,
            message_type=self._message_type,
            payload=self._payload,
            session_id=self._session_id,
            priority=self._priority,
            )
    
    xǁMessageBuilderǁbuild__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁbuild__mutmut_1': xǁMessageBuilderǁbuild__mutmut_1, 
        'xǁMessageBuilderǁbuild__mutmut_2': xǁMessageBuilderǁbuild__mutmut_2, 
        'xǁMessageBuilderǁbuild__mutmut_3': xǁMessageBuilderǁbuild__mutmut_3, 
        'xǁMessageBuilderǁbuild__mutmut_4': xǁMessageBuilderǁbuild__mutmut_4, 
        'xǁMessageBuilderǁbuild__mutmut_5': xǁMessageBuilderǁbuild__mutmut_5, 
        'xǁMessageBuilderǁbuild__mutmut_6': xǁMessageBuilderǁbuild__mutmut_6, 
        'xǁMessageBuilderǁbuild__mutmut_7': xǁMessageBuilderǁbuild__mutmut_7, 
        'xǁMessageBuilderǁbuild__mutmut_8': xǁMessageBuilderǁbuild__mutmut_8, 
        'xǁMessageBuilderǁbuild__mutmut_9': xǁMessageBuilderǁbuild__mutmut_9, 
        'xǁMessageBuilderǁbuild__mutmut_10': xǁMessageBuilderǁbuild__mutmut_10, 
        'xǁMessageBuilderǁbuild__mutmut_11': xǁMessageBuilderǁbuild__mutmut_11, 
        'xǁMessageBuilderǁbuild__mutmut_12': xǁMessageBuilderǁbuild__mutmut_12, 
        'xǁMessageBuilderǁbuild__mutmut_13': xǁMessageBuilderǁbuild__mutmut_13, 
        'xǁMessageBuilderǁbuild__mutmut_14': xǁMessageBuilderǁbuild__mutmut_14, 
        'xǁMessageBuilderǁbuild__mutmut_15': xǁMessageBuilderǁbuild__mutmut_15, 
        'xǁMessageBuilderǁbuild__mutmut_16': xǁMessageBuilderǁbuild__mutmut_16, 
        'xǁMessageBuilderǁbuild__mutmut_17': xǁMessageBuilderǁbuild__mutmut_17, 
        'xǁMessageBuilderǁbuild__mutmut_18': xǁMessageBuilderǁbuild__mutmut_18, 
        'xǁMessageBuilderǁbuild__mutmut_19': xǁMessageBuilderǁbuild__mutmut_19, 
        'xǁMessageBuilderǁbuild__mutmut_20': xǁMessageBuilderǁbuild__mutmut_20, 
        'xǁMessageBuilderǁbuild__mutmut_21': xǁMessageBuilderǁbuild__mutmut_21, 
        'xǁMessageBuilderǁbuild__mutmut_22': xǁMessageBuilderǁbuild__mutmut_22, 
        'xǁMessageBuilderǁbuild__mutmut_23': xǁMessageBuilderǁbuild__mutmut_23, 
        'xǁMessageBuilderǁbuild__mutmut_24': xǁMessageBuilderǁbuild__mutmut_24, 
        'xǁMessageBuilderǁbuild__mutmut_25': xǁMessageBuilderǁbuild__mutmut_25, 
        'xǁMessageBuilderǁbuild__mutmut_26': xǁMessageBuilderǁbuild__mutmut_26, 
        'xǁMessageBuilderǁbuild__mutmut_27': xǁMessageBuilderǁbuild__mutmut_27, 
        'xǁMessageBuilderǁbuild__mutmut_28': xǁMessageBuilderǁbuild__mutmut_28, 
        'xǁMessageBuilderǁbuild__mutmut_29': xǁMessageBuilderǁbuild__mutmut_29, 
        'xǁMessageBuilderǁbuild__mutmut_30': xǁMessageBuilderǁbuild__mutmut_30
    }
    
    def build(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁbuild__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁbuild__mutmut_mutants"), args, kwargs, self)
        return result 
    
    build.__signature__ = _mutmut_signature(xǁMessageBuilderǁbuild__mutmut_orig)
    xǁMessageBuilderǁbuild__mutmut_orig.__name__ = 'xǁMessageBuilderǁbuild'
    
    def xǁMessageBuilderǁreset__mutmut_orig(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = None
        self._payload = {}
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_1(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = ""
        self._to_agent = None
        self._message_type = None
        self._payload = {}
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_2(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = ""
        self._message_type = None
        self._payload = {}
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_3(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = ""
        self._payload = {}
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_4(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = None
        self._payload = None
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_5(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = None
        self._payload = {}
        self._session_id = ""
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_6(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = None
        self._payload = {}
        self._session_id = None
        self._priority = None
        self._parent_message_id = None
        return self
    
    def xǁMessageBuilderǁreset__mutmut_7(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = None
        self._payload = {}
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = ""
        return self
    
    xǁMessageBuilderǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMessageBuilderǁreset__mutmut_1': xǁMessageBuilderǁreset__mutmut_1, 
        'xǁMessageBuilderǁreset__mutmut_2': xǁMessageBuilderǁreset__mutmut_2, 
        'xǁMessageBuilderǁreset__mutmut_3': xǁMessageBuilderǁreset__mutmut_3, 
        'xǁMessageBuilderǁreset__mutmut_4': xǁMessageBuilderǁreset__mutmut_4, 
        'xǁMessageBuilderǁreset__mutmut_5': xǁMessageBuilderǁreset__mutmut_5, 
        'xǁMessageBuilderǁreset__mutmut_6': xǁMessageBuilderǁreset__mutmut_6, 
        'xǁMessageBuilderǁreset__mutmut_7': xǁMessageBuilderǁreset__mutmut_7
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMessageBuilderǁreset__mutmut_orig"), object.__getattribute__(self, "xǁMessageBuilderǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁMessageBuilderǁreset__mutmut_orig)
    xǁMessageBuilderǁreset__mutmut_orig.__name__ = 'xǁMessageBuilderǁreset'


# Common message types
class MessageType:
    """Standard message types used in the system."""
    
    # Context-related
    CONTEXT_READY = "context_ready"
    CONTEXT_REQUEST = "context_request"
    CONTEXT_UPDATE = "context_update"
    
    # Oracle-related
    ORACLE_READY = "oracle_ready"
    ORACLE_REQUEST = "oracle_request"
    ORACLE_INVALID = "oracle_invalid"
    
    # Test generation
    TEST_READY = "test_ready"
    TEST_REQUEST = "test_request"
    TEST_FAILED = "test_failed"
    
    # Execution
    EXECUTION_COMPLETE = "execution_complete"
    EXECUTION_FAILED = "execution_failed"
    
    # Feedback loop
    RETRY_REQUEST = "retry_request"
    REFINEMENT_NEEDED = "refinement_needed"
    
    # Control
    START_WORKFLOW = "start_workflow"
    PAUSE_WORKFLOW = "pause_workflow"
    STOP_WORKFLOW = "stop_workflow"
    
    # Status
    STATUS_REQUEST = "status_request"
    STATUS_UPDATE = "status_update"
    
    # Error handling
    ERROR_OCCURRED = "error_occurred"
    ERROR_RESOLVED = "error_resolved"


# Common event types
class EventType:
    """Standard event types used in the system."""
    
    # Workflow events
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    
    # Agent events
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    
    # Data events
    ENDPOINT_EXTRACTED = "endpoint_extracted"
    ORACLE_GENERATED = "oracle_generated"
    TEST_GENERATED = "test_generated"
    TEST_EXECUTED = "test_executed"
    
    # Quality events
    INCONSISTENCY_DETECTED = "inconsistency_detected"
    QUALITY_ISSUE = "quality_issue"
    
    # System events
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"
