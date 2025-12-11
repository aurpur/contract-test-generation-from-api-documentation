"""
Logging configuration for the contract test generation system.
Provides structured logging with rotation and different log levels.

Author: Aurel IKAMA HONEY
"""
import sys
import os
import re
from pathlib import Path
from loguru import logger
from typing import Optional

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Remove default logger
logger.remove()

# Flag to track if logging has been initialized
_logging_initialized = False

# Secret scrubbing patterns (adapted from secure_logging.py)
SECRET_PATTERNS = [
    (r"(?i)(password|pwd|passwd)\s*[:=]\s*['\"]?([^'\"}\s,]+)", r"\1=***REDACTED***"),
    (r"(?i)(api[-_]?key|apikey)\s*[:=]\s*['\"]?([^'\"}\s,]+)", r"\1=***REDACTED***"),
    (r"(?i)(token|access[-_]?token|refresh[-_]?token)\s*[:=]\s*['\"]?([^'\"}\s,]+)", r"\1=***REDACTED***"),
    (r"(?i)(secret|client[-_]?secret)\s*[:=]\s*['\"]?([^'\"}\s,]+)", r"\1=***REDACTED***"),
    (r"(?i)Authorization:\s*Bearer\s+([^\s]+)", r"Authorization: Bearer ***REDACTED***"),
    (r"(?i)Authorization:\s*Basic\s+([^\s]+)", r"Authorization: Basic ***REDACTED***"),
    (r"(?i)X-API-Key:\s*([^\s]+)", r"X-API-Key: ***REDACTED***"),
    (r"(postgresql|mysql|mongodb|redis)://([^:]+):([^@]+)@", r"\1://\2:***REDACTED***@"),
    (r"AKIA[0-9A-Z]{16}", r"***REDACTED***"),
    (r"eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*", r"***REDACTED***"),
]

def scrub_secrets(message: str) -> str:
    """
    Scrub sensitive data from log messages.
    
    Args:
        message: Log message to scrub
        
    Returns:
        Scrubbed message
    """
    if not message:
        return message
    
    scrubbed = message
    for pattern, replacement in SECRET_PATTERNS:
        scrubbed = re.sub(pattern, replacement, scrubbed)
    
    return scrubbed

def secure_log_formatter(record: dict) -> str:
    """
    Custom formatter that scrubs secrets before logging.
    
    Args:
        record: Loguru record dictionary
        
    Returns:
        Formatted and scrubbed log message
    """
    # Scrub the message
    message = record.get("message", "")
    record["message"] = scrub_secrets(message)
    
    # Return formatted message
    format_string = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    return format_string

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
    format_string: Optional[str] = None
) -> None:
    """
    Configure logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If None, uses default from environment
        rotation: Log rotation policy (e.g., "10 MB", "1 day")
        retention: Log retention policy (e.g., "1 week", "30 days")
        format_string: Custom format string for logs
    """
    global _logging_initialized
    
    # Skip if already initialized to prevent duplicate handlers
    if _logging_initialized:
        return
    
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format - simpler for better readability
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Patcher function to scrub secrets from messages
    def secret_scrubber(record):
        record["message"] = scrub_secrets(record["message"])
    
    # Console handler with colors and secret scrubbing
    logger.add(
        sys.stderr,
        format=format_string,
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True,
        filter=lambda record: secret_scrubber(record) or True
    )
    
    # File handler with rotation and secret scrubbing
    logger.add(
        log_file,
        format=format_string,
        level=level,
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,  # Thread-safe
        filter=lambda record: secret_scrubber(record) or True
    )
    
    # Separate error log file with secret scrubbing
    error_log_file = str(Path(log_file).parent / "error.log")
    logger.add(
        error_log_file,
        format=format_string,
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
        filter=lambda record: secret_scrubber(record) or True
    )
    
    _logging_initialized = True
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")
    logger.info("Secure logging enabled - secrets will be automatically redacted")


def get_logger(name: str):
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module/component
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Initialize logging on import
setup_logging()

# Export logger
__all__ = ["logger", "get_logger", "setup_logging"]
