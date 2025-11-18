"""
Helper utilities for the contract test generation system.

Author: Aurel IKAMA HONEY
"""
import json
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


__all__ = [
    "ensure_dir",
    "load_json",
    "save_json",
    "get_timestamp",
    "sanitize_filename",
    "truncate_string",
    "format_duration",
]
