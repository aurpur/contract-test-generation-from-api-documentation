"""
Secure Logging - Secret Scrubbing Filter

This module provides logging filters to automatically scrub sensitive information
from log messages, preventing accidental exposure of secrets in log files.

The SecretScrubbingFilter automatically masks:
- Passwords (password=..., pwd=..., passwd=...)
- API Keys (api_key=..., apikey=..., api-key=...)
- Tokens (token=..., access_token=..., refresh_token=...)
- Secrets (secret=..., client_secret=...)
- Authorization headers (Authorization: Bearer ..., Authorization: Basic ...)
- Connection strings with embedded credentials

Usage:
    import logging
    from src.utils.secure_logging import SecretScrubbingFilter
    
    # Add filter to logger
    logger = logging.getLogger("my_app")
    logger.addFilter(SecretScrubbingFilter())
    
    # Secrets will be automatically masked
    logger.info("User authenticated with password=secret123")
    # Output: User authenticated with password=***REDACTED***
    
    # With custom patterns
    filter = SecretScrubbingFilter(
        additional_patterns={
            "credit_card": r'credit_card["\']?\s*[:=]\s*["\']?(\d{13,19})'
        }
    )
    logger.addFilter(filter)

Security Note:
    This filter should be added to ALL loggers in production environments
    to prevent accidental logging of sensitive information.

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import logging
import re
from typing import Dict, Optional, Pattern


class SecretScrubbingFilter(logging.Filter):
    """
    Logging filter that automatically scrubs sensitive information from log records.
    
    This filter uses regex patterns to detect and mask common secret patterns
    in log messages, including passwords, API keys, tokens, and authorization headers.
    
    Attributes:
        patterns: Dictionary of compiled regex patterns for secret detection
        redaction_text: Text to replace secrets with (default: "***REDACTED***")
    """
    
    # Default patterns for common secrets
    DEFAULT_PATTERNS = {
        # Password patterns
        "password": r'(?i)(password|pwd|passwd)["\']?\s*[:=]\s*["\']?([^\s\'"&,}]+)',
        
        # API key patterns
        "api_key": r'(?i)(api[_-]?key|apikey)["\']?\s*[:=]\s*["\']?([^\s\'"&,}]+)',
        
        # Token patterns
        "token": r'(?i)(token|access[_-]?token|refresh[_-]?token|auth[_-]?token)["\']?\s*[:=]\s*["\']?([^\s\'"&,}]+)',
        
        # Secret patterns
        "secret": r'(?i)(secret|client[_-]?secret)["\']?\s*[:=]\s*["\']?([^\s\'"&,}]+)',
        
        # Authorization header patterns
        "auth_bearer": r'(?i)(Authorization:\s*Bearer\s+)([^\s]+)',
        "auth_basic": r'(?i)(Authorization:\s*Basic\s+)([^\s]+)',
        
        # X-API-Key header
        "x_api_key": r'(?i)(X-API-Key:\s*)([^\s]+)',
        
        # Connection strings with passwords
        "connection_string": r'(?i)(postgresql|mysql|mongodb|redis)://([^:]+):([^@]+)@',
        
        # AWS credentials
        "aws_access_key": r'(?i)(aws[_-]?access[_-]?key[_-]?id)["\']?\s*[:=]\s*["\']?(AKIA[0-9A-Z]{16})',
        "aws_secret_key": r'(?i)(aws[_-]?secret[_-]?access[_-]?key)["\']?\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})',
        
        # JWT tokens (Bearer tokens in various formats)
        "jwt": r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}',
        
        # Base64 encoded credentials (basic auth)
        "base64_creds": r'(?i)(Authorization:\s*Basic\s+)([A-Za-z0-9+/]{20,}={0,2})',
    }
    
    def __init__(
        self,
        redaction_text: str = "***REDACTED***",
        additional_patterns: Optional[Dict[str, str]] = None,
        enabled: bool = True
    ):
        """
        Initialize secret scrubbing filter.
        
        Args:
            redaction_text: Text to replace secrets with
            additional_patterns: Additional regex patterns to detect secrets
                Format: {"pattern_name": r"regex_pattern"}
            enabled: If False, filter is disabled (for testing)
        """
        super().__init__()
        self.redaction_text = redaction_text
        self.enabled = enabled
        
        # Compile patterns for performance
        self.patterns: Dict[str, Pattern] = {}
        
        # Add default patterns
        for name, pattern in self.DEFAULT_PATTERNS.items():
            try:
                self.patterns[name] = re.compile(pattern)
            except re.error as e:
                # Log pattern compilation error but continue
                logging.warning(f"Failed to compile pattern '{name}': {e}")
        
        # Add additional patterns
        if additional_patterns:
            for name, pattern in additional_patterns.items():
                try:
                    self.patterns[f"custom_{name}"] = re.compile(pattern)
                except re.error as e:
                    logging.warning(f"Failed to compile custom pattern '{name}': {e}")
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log record by scrubbing sensitive information.
        
        Args:
            record: Log record to filter
        
        Returns:
            Always returns True (record is always logged, just scrubbed)
        """
        if not self.enabled:
            return True
        
        # Scrub the main message
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = self._scrub_message(record.msg)
        
        # Scrub formatted message (if already formatted)
        if hasattr(record, 'message') and isinstance(record.message, str):
            record.message = self._scrub_message(record.message)
        
        # Scrub args (for format strings)
        if hasattr(record, 'args') and record.args:
            if isinstance(record.args, dict):
                record.args = {k: self._scrub_value(v) for k, v in record.args.items()}
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(self._scrub_value(arg) for arg in record.args)
        
        return True
    
    def _scrub_message(self, message: str) -> str:
        """
        Scrub sensitive information from a message.
        
        Args:
            message: Message to scrub
        
        Returns:
            Scrubbed message with secrets replaced
        """
        if not message:
            return message
        
        scrubbed = message
        
        for pattern_name, pattern in self.patterns.items():
            try:
                # Different replacement strategies based on pattern type
                if pattern_name in ["password", "api_key", "token", "secret", "aws_access_key", "aws_secret_key"]:
                    # Replace the value part only, keep the key name
                    scrubbed = pattern.sub(
                        lambda m: f"{m.group(1)}={self.redaction_text}",
                        scrubbed
                    )
                elif pattern_name in ["auth_bearer", "auth_basic", "x_api_key", "base64_creds"]:
                    # Replace the credential part after the header name
                    scrubbed = pattern.sub(
                        lambda m: f"{m.group(1)}{self.redaction_text}",
                        scrubbed
                    )
                elif pattern_name == "connection_string":
                    # Replace password in connection string
                    scrubbed = pattern.sub(
                        lambda m: f"{m.group(1)}://{m.group(2)}:{self.redaction_text}@",
                        scrubbed
                    )
                elif pattern_name == "jwt":
                    # Replace entire JWT
                    scrubbed = pattern.sub(self.redaction_text, scrubbed)
                else:
                    # For custom patterns, replace the entire match
                    scrubbed = pattern.sub(self.redaction_text, scrubbed)
                    
            except Exception as e:
                # If scrubbing fails for a pattern, continue with others
                logging.debug(f"Failed to apply pattern '{pattern_name}': {e}")
                continue
        
        return scrubbed
    
    def _scrub_value(self, value):
        """
        Scrub a single value (used for log record args).
        
        Args:
            value: Value to scrub
        
        Returns:
            Scrubbed value
        """
        if isinstance(value, str):
            return self._scrub_message(value)
        elif isinstance(value, dict):
            return {k: self._scrub_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return type(value)(self._scrub_value(item) for item in value)
        else:
            return value
    
    def add_pattern(self, name: str, pattern: str):
        """
        Add a new secret pattern to the filter.
        
        Args:
            name: Name for the pattern
            pattern: Regex pattern to detect secrets
        
        Raises:
            ValueError: If pattern fails to compile
        """
        try:
            self.patterns[name] = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{name}': {e}")
    
    def remove_pattern(self, name: str):
        """
        Remove a secret pattern from the filter.
        
        Args:
            name: Name of the pattern to remove
        """
        if name in self.patterns:
            del self.patterns[name]
    
    def disable(self):
        """Disable the filter (secrets will not be scrubbed)."""
        self.enabled = False
    
    def enable(self):
        """Enable the filter (secrets will be scrubbed)."""
        self.enabled = True


def configure_secure_logging(
    logger: Optional[logging.Logger] = None,
    redaction_text: str = "***REDACTED***"
) -> SecretScrubbingFilter:
    """
    Configure secure logging by adding SecretScrubbingFilter to a logger.
    
    Args:
        logger: Logger to configure (default: root logger)
        redaction_text: Text to replace secrets with
    
    Returns:
        The SecretScrubbingFilter instance that was added
    
    Example:
        # Configure root logger
        configure_secure_logging()
        
        # Configure specific logger
        my_logger = logging.getLogger("my_app")
        configure_secure_logging(my_logger)
    """
    if logger is None:
        logger = logging.getLogger()
    
    # Create and add filter
    filter = SecretScrubbingFilter(redaction_text=redaction_text)
    logger.addFilter(filter)
    
    return filter


def configure_all_loggers(redaction_text: str = "***REDACTED***"):
    """
    Configure secure logging for all existing loggers.
    
    This function adds SecretScrubbingFilter to the root logger and all
    existing loggers in the logging hierarchy.
    
    Args:
        redaction_text: Text to replace secrets with
    
    Example:
        # Configure all loggers at application startup
        configure_all_loggers()
    """
    # Configure root logger
    configure_secure_logging(redaction_text=redaction_text)
    
    # Configure all existing loggers
    for logger_name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        if isinstance(logger, logging.Logger):
            configure_secure_logging(logger, redaction_text)
