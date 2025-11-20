"""
Logging configuration for the contract test generation system.
Provides structured logging with rotation and different log levels.

Author: Aurel IKAMA HONEY
"""
import sys
import os
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
    
    # Console handler with colors
    logger.add(
        sys.stderr,
        format=format_string,
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # File handler with rotation
    logger.add(
        log_file,
        format=format_string,
        level=level,
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True  # Thread-safe
    )
    
    # Separate error log file
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
        enqueue=True
    )
    
    _logging_initialized = True
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")


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
