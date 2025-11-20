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
    
    def __init__(self):
        """Initialize message router."""
        self.handlers: Dict[str, MessageHandler] = {}
        self.default_handler: Optional[MessageHandler] = None
        logger.debug("MessageRouter initialized")
    
    def register_handler(
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
    
    def register_default_handler(self, handler: MessageHandler) -> None:
        """
        Register a default handler for unmatched message types.
        
        Args:
            handler: Default handler instance
        """
        self.default_handler = handler
        logger.debug("Registered default message handler")
    
    async def route_message(
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
    
    async def send(self, message: AgentMessage) -> None:
        """
        Send a message by routing it to the appropriate handler.
        
        This is an alias for route_message that doesn't return a value,
        used when the response is not needed.
        
        Args:
            message: Message to send
        """
        try:
            await self.route_message(message)
        except Exception as e:
            logger.error(f"Failed to send message {message.id}: {e}")
    
    def has_handler(self, message_type: str) -> bool:
        """
        Check if a handler is registered for a message type.
        
        Args:
            message_type: Message type to check
            
        Returns:
            True if handler exists, False otherwise
        """
        return message_type in self.handlers or self.default_handler is not None


class EventBus:
    """
    Event bus for publish-subscribe pattern between agents.
    
    Allows agents to subscribe to events and publish events without
    direct coupling.
    """
    
    def __init__(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_counts: Dict[str, int] = {}  # Track event publish counts
        self.total_events: int = 0  # Total events published
        logger.debug("EventBus initialized")
    
    def subscribe(
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
    
    def unsubscribe(
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
    
    async def publish(
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
        # Track event counts
        self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1
        self.total_events += 1
        
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
    
    def get_subscriber_count(self, event_type: str) -> int:
        """
        Get the number of subscribers for an event type.
        
        Args:
            event_type: Event type
            
        Returns:
            Number of subscribers
        """
        return len(self.subscribers.get(event_type, []))
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about published events.
        
        Returns:
            Dictionary with event statistics
        """
        return {
            "total_events": self.total_events,
            "event_counts": dict(self.event_counts),
            "unique_event_types": len(self.event_counts),
        }


class MessageBuilder:
    """
    Builder pattern for constructing agent messages.
    
    Provides a fluent interface for creating complex messages.
    """
    
    def __init__(self):
        """Initialize message builder."""
        self._from_agent: Optional[AgentType] = None
        self._to_agent: Optional[AgentType] = None
        self._message_type: Optional[str] = None
        self._payload: Dict[str, Any] = {}
        self._session_id: Optional[UUID] = None
        self._priority: int = MessagePriority.NORMAL
        self._parent_message_id: Optional[UUID] = None
    
    def from_agent(self, agent: AgentType) -> 'MessageBuilder':
        """Set the sender agent."""
        self._from_agent = agent
        return self
    
    def to_agent(self, agent: AgentType) -> 'MessageBuilder':
        """Set the receiver agent."""
        self._to_agent = agent
        return self
    
    def with_type(self, message_type: str) -> 'MessageBuilder':
        """Set the message type."""
        self._message_type = message_type
        return self
    
    def with_payload(self, payload: Dict[str, Any]) -> 'MessageBuilder':
        """Set the message payload."""
        self._payload = payload
        return self
    
    def add_to_payload(self, key: str, value: Any) -> 'MessageBuilder':
        """Add a key-value pair to the payload."""
        self._payload[key] = value
        return self
    
    def for_session(self, session_id: UUID) -> 'MessageBuilder':
        """Set the session ID."""
        self._session_id = session_id
        return self
    
    def with_priority(self, priority: MessagePriority) -> 'MessageBuilder':
        """Set the message priority."""
        self._priority = priority
        return self
    
    def in_reply_to(self, message_id: UUID) -> 'MessageBuilder':
        """Set the parent message ID."""
        self._parent_message_id = message_id
        return self
    
    def build(self) -> AgentMessage:
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
    
    def reset(self) -> 'MessageBuilder':
        """Reset the builder to initial state."""
        self._from_agent = None
        self._to_agent = None
        self._message_type = None
        self._payload = {}
        self._session_id = None
        self._priority = MessagePriority.NORMAL
        self._parent_message_id = None
        return self
    
    @classmethod
    def create_request(
        cls,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: str,
        payload: Dict[str, Any],
        session_id: UUID,
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> AgentMessage:
        """
        Create a request message (factory method).
        
        Args:
            from_agent: Sender agent
            to_agent: Receiver agent
            message_type: Type of message
            payload: Message payload
            session_id: Session ID
            priority: Message priority
            
        Returns:
            Constructed agent message
        """
        return cls() \
            .from_agent(from_agent) \
            .to_agent(to_agent) \
            .with_type(message_type) \
            .with_payload(payload) \
            .for_session(session_id) \
            .with_priority(priority) \
            .build()
    
    @classmethod
    def create_response(
        cls,
        original_message: AgentMessage,
        response_data: Dict[str, Any],
        message_type: Optional[str] = None,
    ) -> AgentMessage:
        """
        Create a response message to an original message (factory method).
        
        Args:
            original_message: The message being responded to
            response_data: Response payload
            message_type: Optional message type (defaults to original_type + '_response')
            
        Returns:
            Constructed response message
        """
        response_type = message_type or f"{original_message.message_type}_response"
        
        return cls() \
            .from_agent(original_message.to_agent) \
            .to_agent(original_message.from_agent) \
            .with_type(response_type) \
            .with_payload(response_data) \
            .for_session(original_message.session_id) \
            .with_priority(original_message.priority) \
            .in_reply_to(original_message.id) \
            .build()


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
