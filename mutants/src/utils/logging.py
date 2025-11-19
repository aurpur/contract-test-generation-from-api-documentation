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

def x_setup_logging__mutmut_orig(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_1(
    level: str = "XXINFOXX",
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_2(
    level: str = "info",
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_3(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "XX10 MBXX",
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_4(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 mb",
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_5(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "XX1 weekXX",
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_6(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 WEEK",
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_7(
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
    # Get configuration from environment
    level = None
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_8(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).lower()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_9(
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
    # Get configuration from environment
    level = os.getenv(None, level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_10(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", None).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_11(
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
    # Get configuration from environment
    level = os.getenv(level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_12(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", ).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_13(
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
    # Get configuration from environment
    level = os.getenv("XXLOG_LEVELXX", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_14(
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
    # Get configuration from environment
    level = os.getenv("log_level", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_15(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = None
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_16(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file and os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_17(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv(None, "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_18(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", None)
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_19(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_20(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", )
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_21(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("XXLOG_FILEXX", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_22(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("log_file", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_23(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "XXlogs/app.logXX")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_24(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "LOGS/APP.LOG")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_25(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is not None:
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_26(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = None
    
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_27(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "XX<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | XX"
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_28(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:yyyy-mm-dd hh:mm:ss.sss}</green> | "
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_29(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<GREEN>{TIME:YYYY-MM-DD HH:MM:SS.SSS}</GREEN> | "
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_30(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "XX<level>{level: <8}</level> | XX"
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_31(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<LEVEL>{LEVEL: <8}</LEVEL> | "
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_32(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "XX<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | XX"
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_33(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<CYAN>{NAME}</CYAN>:<CYAN>{FUNCTION}</CYAN>:<CYAN>{LINE}</CYAN> | "
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_34(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "XX<level>{message}</level>XX"
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_35(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<LEVEL>{MESSAGE}</LEVEL>"
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_36(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Console handler with colors
    logger.add(
        None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_37(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        format=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_38(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        level=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_39(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        colorize=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_40(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_41(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=None
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_42(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Console handler with colors
    logger.add(
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_43(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_44(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_45(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_46(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_47(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_48(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        colorize=False,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_49(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=False,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_50(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=False
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_51(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_52(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        format=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_53(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        level=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_54(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        rotation=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_55(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        retention=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_56(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_57(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_58(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=None,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_59(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        enqueue=None  # Thread-safe
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_60(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_61(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_62(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_63(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_64(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_65(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_66(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_67(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_68(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_69(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression="XXzipXX",
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_70(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression="ZIP",
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_71(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=False,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_72(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=False,
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_73(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        enqueue=False  # Thread-safe
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_74(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    error_log_file = None
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_75(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    error_log_file = str(None)
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_76(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    error_log_file = str(Path(log_file).parent * "error.log")
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_77(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    error_log_file = str(Path(None).parent / "error.log")
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_78(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    error_log_file = str(Path(log_file).parent / "XXerror.logXX")
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_79(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    error_log_file = str(Path(log_file).parent / "ERROR.LOG")
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
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_80(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        None,
        format=format_string,
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_81(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        format=None,
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_82(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        level=None,
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_83(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        rotation=None,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_84(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        retention=None,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_85(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression=None,
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_86(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=None,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_87(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=None,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_88(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        enqueue=None
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_89(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        format=format_string,
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_90(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_91(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_92(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_93(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_94(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_95(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_96(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_97(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_98(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        level="XXERRORXX",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_99(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        level="error",
        rotation=rotation,
        retention=retention,
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_100(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression="XXzipXX",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_101(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        compression="ZIP",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_102(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        backtrace=False,
        diagnose=True,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_103(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        diagnose=False,
        enqueue=True
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_104(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
        enqueue=False
    )
    
    logger.info(f"Logging initialized - Level: {level}, Log file: {log_file}")

def x_setup_logging__mutmut_105(
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
    # Get configuration from environment
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = log_file or os.getenv("LOG_FILE", "logs/app.log")
    
    # Default format with colors for console
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
    
    logger.info(None)

x_setup_logging__mutmut_mutants : ClassVar[MutantDict] = {
'x_setup_logging__mutmut_1': x_setup_logging__mutmut_1, 
    'x_setup_logging__mutmut_2': x_setup_logging__mutmut_2, 
    'x_setup_logging__mutmut_3': x_setup_logging__mutmut_3, 
    'x_setup_logging__mutmut_4': x_setup_logging__mutmut_4, 
    'x_setup_logging__mutmut_5': x_setup_logging__mutmut_5, 
    'x_setup_logging__mutmut_6': x_setup_logging__mutmut_6, 
    'x_setup_logging__mutmut_7': x_setup_logging__mutmut_7, 
    'x_setup_logging__mutmut_8': x_setup_logging__mutmut_8, 
    'x_setup_logging__mutmut_9': x_setup_logging__mutmut_9, 
    'x_setup_logging__mutmut_10': x_setup_logging__mutmut_10, 
    'x_setup_logging__mutmut_11': x_setup_logging__mutmut_11, 
    'x_setup_logging__mutmut_12': x_setup_logging__mutmut_12, 
    'x_setup_logging__mutmut_13': x_setup_logging__mutmut_13, 
    'x_setup_logging__mutmut_14': x_setup_logging__mutmut_14, 
    'x_setup_logging__mutmut_15': x_setup_logging__mutmut_15, 
    'x_setup_logging__mutmut_16': x_setup_logging__mutmut_16, 
    'x_setup_logging__mutmut_17': x_setup_logging__mutmut_17, 
    'x_setup_logging__mutmut_18': x_setup_logging__mutmut_18, 
    'x_setup_logging__mutmut_19': x_setup_logging__mutmut_19, 
    'x_setup_logging__mutmut_20': x_setup_logging__mutmut_20, 
    'x_setup_logging__mutmut_21': x_setup_logging__mutmut_21, 
    'x_setup_logging__mutmut_22': x_setup_logging__mutmut_22, 
    'x_setup_logging__mutmut_23': x_setup_logging__mutmut_23, 
    'x_setup_logging__mutmut_24': x_setup_logging__mutmut_24, 
    'x_setup_logging__mutmut_25': x_setup_logging__mutmut_25, 
    'x_setup_logging__mutmut_26': x_setup_logging__mutmut_26, 
    'x_setup_logging__mutmut_27': x_setup_logging__mutmut_27, 
    'x_setup_logging__mutmut_28': x_setup_logging__mutmut_28, 
    'x_setup_logging__mutmut_29': x_setup_logging__mutmut_29, 
    'x_setup_logging__mutmut_30': x_setup_logging__mutmut_30, 
    'x_setup_logging__mutmut_31': x_setup_logging__mutmut_31, 
    'x_setup_logging__mutmut_32': x_setup_logging__mutmut_32, 
    'x_setup_logging__mutmut_33': x_setup_logging__mutmut_33, 
    'x_setup_logging__mutmut_34': x_setup_logging__mutmut_34, 
    'x_setup_logging__mutmut_35': x_setup_logging__mutmut_35, 
    'x_setup_logging__mutmut_36': x_setup_logging__mutmut_36, 
    'x_setup_logging__mutmut_37': x_setup_logging__mutmut_37, 
    'x_setup_logging__mutmut_38': x_setup_logging__mutmut_38, 
    'x_setup_logging__mutmut_39': x_setup_logging__mutmut_39, 
    'x_setup_logging__mutmut_40': x_setup_logging__mutmut_40, 
    'x_setup_logging__mutmut_41': x_setup_logging__mutmut_41, 
    'x_setup_logging__mutmut_42': x_setup_logging__mutmut_42, 
    'x_setup_logging__mutmut_43': x_setup_logging__mutmut_43, 
    'x_setup_logging__mutmut_44': x_setup_logging__mutmut_44, 
    'x_setup_logging__mutmut_45': x_setup_logging__mutmut_45, 
    'x_setup_logging__mutmut_46': x_setup_logging__mutmut_46, 
    'x_setup_logging__mutmut_47': x_setup_logging__mutmut_47, 
    'x_setup_logging__mutmut_48': x_setup_logging__mutmut_48, 
    'x_setup_logging__mutmut_49': x_setup_logging__mutmut_49, 
    'x_setup_logging__mutmut_50': x_setup_logging__mutmut_50, 
    'x_setup_logging__mutmut_51': x_setup_logging__mutmut_51, 
    'x_setup_logging__mutmut_52': x_setup_logging__mutmut_52, 
    'x_setup_logging__mutmut_53': x_setup_logging__mutmut_53, 
    'x_setup_logging__mutmut_54': x_setup_logging__mutmut_54, 
    'x_setup_logging__mutmut_55': x_setup_logging__mutmut_55, 
    'x_setup_logging__mutmut_56': x_setup_logging__mutmut_56, 
    'x_setup_logging__mutmut_57': x_setup_logging__mutmut_57, 
    'x_setup_logging__mutmut_58': x_setup_logging__mutmut_58, 
    'x_setup_logging__mutmut_59': x_setup_logging__mutmut_59, 
    'x_setup_logging__mutmut_60': x_setup_logging__mutmut_60, 
    'x_setup_logging__mutmut_61': x_setup_logging__mutmut_61, 
    'x_setup_logging__mutmut_62': x_setup_logging__mutmut_62, 
    'x_setup_logging__mutmut_63': x_setup_logging__mutmut_63, 
    'x_setup_logging__mutmut_64': x_setup_logging__mutmut_64, 
    'x_setup_logging__mutmut_65': x_setup_logging__mutmut_65, 
    'x_setup_logging__mutmut_66': x_setup_logging__mutmut_66, 
    'x_setup_logging__mutmut_67': x_setup_logging__mutmut_67, 
    'x_setup_logging__mutmut_68': x_setup_logging__mutmut_68, 
    'x_setup_logging__mutmut_69': x_setup_logging__mutmut_69, 
    'x_setup_logging__mutmut_70': x_setup_logging__mutmut_70, 
    'x_setup_logging__mutmut_71': x_setup_logging__mutmut_71, 
    'x_setup_logging__mutmut_72': x_setup_logging__mutmut_72, 
    'x_setup_logging__mutmut_73': x_setup_logging__mutmut_73, 
    'x_setup_logging__mutmut_74': x_setup_logging__mutmut_74, 
    'x_setup_logging__mutmut_75': x_setup_logging__mutmut_75, 
    'x_setup_logging__mutmut_76': x_setup_logging__mutmut_76, 
    'x_setup_logging__mutmut_77': x_setup_logging__mutmut_77, 
    'x_setup_logging__mutmut_78': x_setup_logging__mutmut_78, 
    'x_setup_logging__mutmut_79': x_setup_logging__mutmut_79, 
    'x_setup_logging__mutmut_80': x_setup_logging__mutmut_80, 
    'x_setup_logging__mutmut_81': x_setup_logging__mutmut_81, 
    'x_setup_logging__mutmut_82': x_setup_logging__mutmut_82, 
    'x_setup_logging__mutmut_83': x_setup_logging__mutmut_83, 
    'x_setup_logging__mutmut_84': x_setup_logging__mutmut_84, 
    'x_setup_logging__mutmut_85': x_setup_logging__mutmut_85, 
    'x_setup_logging__mutmut_86': x_setup_logging__mutmut_86, 
    'x_setup_logging__mutmut_87': x_setup_logging__mutmut_87, 
    'x_setup_logging__mutmut_88': x_setup_logging__mutmut_88, 
    'x_setup_logging__mutmut_89': x_setup_logging__mutmut_89, 
    'x_setup_logging__mutmut_90': x_setup_logging__mutmut_90, 
    'x_setup_logging__mutmut_91': x_setup_logging__mutmut_91, 
    'x_setup_logging__mutmut_92': x_setup_logging__mutmut_92, 
    'x_setup_logging__mutmut_93': x_setup_logging__mutmut_93, 
    'x_setup_logging__mutmut_94': x_setup_logging__mutmut_94, 
    'x_setup_logging__mutmut_95': x_setup_logging__mutmut_95, 
    'x_setup_logging__mutmut_96': x_setup_logging__mutmut_96, 
    'x_setup_logging__mutmut_97': x_setup_logging__mutmut_97, 
    'x_setup_logging__mutmut_98': x_setup_logging__mutmut_98, 
    'x_setup_logging__mutmut_99': x_setup_logging__mutmut_99, 
    'x_setup_logging__mutmut_100': x_setup_logging__mutmut_100, 
    'x_setup_logging__mutmut_101': x_setup_logging__mutmut_101, 
    'x_setup_logging__mutmut_102': x_setup_logging__mutmut_102, 
    'x_setup_logging__mutmut_103': x_setup_logging__mutmut_103, 
    'x_setup_logging__mutmut_104': x_setup_logging__mutmut_104, 
    'x_setup_logging__mutmut_105': x_setup_logging__mutmut_105
}

def setup_logging(*args, **kwargs):
    result = _mutmut_trampoline(x_setup_logging__mutmut_orig, x_setup_logging__mutmut_mutants, args, kwargs)
    return result 

setup_logging.__signature__ = _mutmut_signature(x_setup_logging__mutmut_orig)
x_setup_logging__mutmut_orig.__name__ = 'x_setup_logging'


def x_get_logger__mutmut_orig(name: str):
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module/component
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


def x_get_logger__mutmut_1(name: str):
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module/component
        
    Returns:
        Logger instance
    """
    return logger.bind(name=None)

x_get_logger__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_logger__mutmut_1': x_get_logger__mutmut_1
}

def get_logger(*args, **kwargs):
    result = _mutmut_trampoline(x_get_logger__mutmut_orig, x_get_logger__mutmut_mutants, args, kwargs)
    return result 

get_logger.__signature__ = _mutmut_signature(x_get_logger__mutmut_orig)
x_get_logger__mutmut_orig.__name__ = 'x_get_logger'


# Initialize logging on import
setup_logging()

# Export logger
__all__ = ["logger", "get_logger", "setup_logging"]
