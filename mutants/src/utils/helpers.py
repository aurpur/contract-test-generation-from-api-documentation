"""
Helper utilities for the contract test generation system.

Author: Aurel IKAMA HONEY
"""
import json
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path
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


def x_ensure_dir__mutmut_orig(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def x_ensure_dir__mutmut_1(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=None, exist_ok=True)
    return path


def x_ensure_dir__mutmut_2(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=True, exist_ok=None)
    return path


def x_ensure_dir__mutmut_3(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(exist_ok=True)
    return path


def x_ensure_dir__mutmut_4(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=True, )
    return path


def x_ensure_dir__mutmut_5(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=False, exist_ok=True)
    return path


def x_ensure_dir__mutmut_6(path: Path) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        The path object
    """
    path.mkdir(parents=True, exist_ok=False)
    return path

x_ensure_dir__mutmut_mutants : ClassVar[MutantDict] = {
'x_ensure_dir__mutmut_1': x_ensure_dir__mutmut_1, 
    'x_ensure_dir__mutmut_2': x_ensure_dir__mutmut_2, 
    'x_ensure_dir__mutmut_3': x_ensure_dir__mutmut_3, 
    'x_ensure_dir__mutmut_4': x_ensure_dir__mutmut_4, 
    'x_ensure_dir__mutmut_5': x_ensure_dir__mutmut_5, 
    'x_ensure_dir__mutmut_6': x_ensure_dir__mutmut_6
}

def ensure_dir(*args, **kwargs):
    result = _mutmut_trampoline(x_ensure_dir__mutmut_orig, x_ensure_dir__mutmut_mutants, args, kwargs)
    return result 

ensure_dir.__signature__ = _mutmut_signature(x_ensure_dir__mutmut_orig)
x_ensure_dir__mutmut_orig.__name__ = 'x_ensure_dir'


def x_load_json__mutmut_orig(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_1(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(None, "r", encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_2(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, None, encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_3(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", encoding=None) as f:
        return json.load(f)


def x_load_json__mutmut_4(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open("r", encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_5(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_6(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", ) as f:
        return json.load(f)


def x_load_json__mutmut_7(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "XXrXX", encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_8(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "R", encoding="utf-8") as f:
        return json.load(f)


def x_load_json__mutmut_9(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", encoding="XXutf-8XX") as f:
        return json.load(f)


def x_load_json__mutmut_10(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", encoding="UTF-8") as f:
        return json.load(f)


def x_load_json__mutmut_11(filepath: Path) -> Dict[str, Any]:
    """
    Load JSON from a file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing the JSON data
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(None)

x_load_json__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_json__mutmut_1': x_load_json__mutmut_1, 
    'x_load_json__mutmut_2': x_load_json__mutmut_2, 
    'x_load_json__mutmut_3': x_load_json__mutmut_3, 
    'x_load_json__mutmut_4': x_load_json__mutmut_4, 
    'x_load_json__mutmut_5': x_load_json__mutmut_5, 
    'x_load_json__mutmut_6': x_load_json__mutmut_6, 
    'x_load_json__mutmut_7': x_load_json__mutmut_7, 
    'x_load_json__mutmut_8': x_load_json__mutmut_8, 
    'x_load_json__mutmut_9': x_load_json__mutmut_9, 
    'x_load_json__mutmut_10': x_load_json__mutmut_10, 
    'x_load_json__mutmut_11': x_load_json__mutmut_11
}

def load_json(*args, **kwargs):
    result = _mutmut_trampoline(x_load_json__mutmut_orig, x_load_json__mutmut_mutants, args, kwargs)
    return result 

load_json.__signature__ = _mutmut_signature(x_load_json__mutmut_orig)
x_load_json__mutmut_orig.__name__ = 'x_load_json'


def x_save_json__mutmut_orig(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
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


def x_save_json__mutmut_1(data: Dict[str, Any], filepath: Path, indent: int = 3) -> None:
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


def x_save_json__mutmut_2(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(None)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_3(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(None, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_4(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, None, encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_5(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding=None) as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_6(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_7(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_8(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", ) as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_9(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "XXwXX", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_10(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "W", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_11(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="XXutf-8XX") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_12(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_13(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(None, f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_14(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, None, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_15(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=None, ensure_ascii=False)


def x_save_json__mutmut_16(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=None)


def x_save_json__mutmut_17(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(f, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_18(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, indent=indent, ensure_ascii=False)


def x_save_json__mutmut_19(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def x_save_json__mutmut_20(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, )


def x_save_json__mutmut_21(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save to
        indent: JSON indentation level
    """
    ensure_dir(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=True)

x_save_json__mutmut_mutants : ClassVar[MutantDict] = {
'x_save_json__mutmut_1': x_save_json__mutmut_1, 
    'x_save_json__mutmut_2': x_save_json__mutmut_2, 
    'x_save_json__mutmut_3': x_save_json__mutmut_3, 
    'x_save_json__mutmut_4': x_save_json__mutmut_4, 
    'x_save_json__mutmut_5': x_save_json__mutmut_5, 
    'x_save_json__mutmut_6': x_save_json__mutmut_6, 
    'x_save_json__mutmut_7': x_save_json__mutmut_7, 
    'x_save_json__mutmut_8': x_save_json__mutmut_8, 
    'x_save_json__mutmut_9': x_save_json__mutmut_9, 
    'x_save_json__mutmut_10': x_save_json__mutmut_10, 
    'x_save_json__mutmut_11': x_save_json__mutmut_11, 
    'x_save_json__mutmut_12': x_save_json__mutmut_12, 
    'x_save_json__mutmut_13': x_save_json__mutmut_13, 
    'x_save_json__mutmut_14': x_save_json__mutmut_14, 
    'x_save_json__mutmut_15': x_save_json__mutmut_15, 
    'x_save_json__mutmut_16': x_save_json__mutmut_16, 
    'x_save_json__mutmut_17': x_save_json__mutmut_17, 
    'x_save_json__mutmut_18': x_save_json__mutmut_18, 
    'x_save_json__mutmut_19': x_save_json__mutmut_19, 
    'x_save_json__mutmut_20': x_save_json__mutmut_20, 
    'x_save_json__mutmut_21': x_save_json__mutmut_21
}

def save_json(*args, **kwargs):
    result = _mutmut_trampoline(x_save_json__mutmut_orig, x_save_json__mutmut_mutants, args, kwargs)
    return result 

save_json.__signature__ = _mutmut_signature(x_save_json__mutmut_orig)
x_save_json__mutmut_orig.__name__ = 'x_save_json'


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


def x_sanitize_filename__mutmut_orig(filename: str) -> str:
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


def x_sanitize_filename__mutmut_1(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = None
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def x_sanitize_filename__mutmut_2(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = 'XX<>:"/\\|?*XX'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def x_sanitize_filename__mutmut_3(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = None
    return filename


def x_sanitize_filename__mutmut_4(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(None, "_")
    return filename


def x_sanitize_filename__mutmut_5(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, None)
    return filename


def x_sanitize_filename__mutmut_6(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace("_")
    return filename


def x_sanitize_filename__mutmut_7(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, )
    return filename


def x_sanitize_filename__mutmut_8(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "XX_XX")
    return filename

x_sanitize_filename__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize_filename__mutmut_1': x_sanitize_filename__mutmut_1, 
    'x_sanitize_filename__mutmut_2': x_sanitize_filename__mutmut_2, 
    'x_sanitize_filename__mutmut_3': x_sanitize_filename__mutmut_3, 
    'x_sanitize_filename__mutmut_4': x_sanitize_filename__mutmut_4, 
    'x_sanitize_filename__mutmut_5': x_sanitize_filename__mutmut_5, 
    'x_sanitize_filename__mutmut_6': x_sanitize_filename__mutmut_6, 
    'x_sanitize_filename__mutmut_7': x_sanitize_filename__mutmut_7, 
    'x_sanitize_filename__mutmut_8': x_sanitize_filename__mutmut_8
}

def sanitize_filename(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize_filename__mutmut_orig, x_sanitize_filename__mutmut_mutants, args, kwargs)
    return result 

sanitize_filename.__signature__ = _mutmut_signature(x_sanitize_filename__mutmut_orig)
x_sanitize_filename__mutmut_orig.__name__ = 'x_sanitize_filename'


def x_truncate_string__mutmut_orig(text: str, max_length: int = 100, suffix: str = "...") -> str:
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


def x_truncate_string__mutmut_1(text: str, max_length: int = 101, suffix: str = "...") -> str:
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


def x_truncate_string__mutmut_2(text: str, max_length: int = 100, suffix: str = "XX...XX") -> str:
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


def x_truncate_string__mutmut_3(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) < max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def x_truncate_string__mutmut_4(text: str, max_length: int = 100, suffix: str = "...") -> str:
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
    return text[:max_length - len(suffix)] - suffix


def x_truncate_string__mutmut_5(text: str, max_length: int = 100, suffix: str = "...") -> str:
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
    return text[:max_length + len(suffix)] + suffix

x_truncate_string__mutmut_mutants : ClassVar[MutantDict] = {
'x_truncate_string__mutmut_1': x_truncate_string__mutmut_1, 
    'x_truncate_string__mutmut_2': x_truncate_string__mutmut_2, 
    'x_truncate_string__mutmut_3': x_truncate_string__mutmut_3, 
    'x_truncate_string__mutmut_4': x_truncate_string__mutmut_4, 
    'x_truncate_string__mutmut_5': x_truncate_string__mutmut_5
}

def truncate_string(*args, **kwargs):
    result = _mutmut_trampoline(x_truncate_string__mutmut_orig, x_truncate_string__mutmut_mutants, args, kwargs)
    return result 

truncate_string.__signature__ = _mutmut_signature(x_truncate_string__mutmut_orig)
x_truncate_string__mutmut_orig.__name__ = 'x_truncate_string'


def x_format_duration__mutmut_orig(seconds: float) -> str:
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


def x_format_duration__mutmut_1(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds <= 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_2(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 61:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_3(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds <= 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_4(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3601:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_5(seconds: float) -> str:
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
        minutes = None
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_6(seconds: float) -> str:
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
        minutes = seconds * 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_7(seconds: float) -> str:
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
        minutes = seconds / 61
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_8(seconds: float) -> str:
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
        hours = None
        return f"{hours:.2f}h"


def x_format_duration__mutmut_9(seconds: float) -> str:
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
        hours = seconds * 3600
        return f"{hours:.2f}h"


def x_format_duration__mutmut_10(seconds: float) -> str:
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
        hours = seconds / 3601
        return f"{hours:.2f}h"

x_format_duration__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_duration__mutmut_1': x_format_duration__mutmut_1, 
    'x_format_duration__mutmut_2': x_format_duration__mutmut_2, 
    'x_format_duration__mutmut_3': x_format_duration__mutmut_3, 
    'x_format_duration__mutmut_4': x_format_duration__mutmut_4, 
    'x_format_duration__mutmut_5': x_format_duration__mutmut_5, 
    'x_format_duration__mutmut_6': x_format_duration__mutmut_6, 
    'x_format_duration__mutmut_7': x_format_duration__mutmut_7, 
    'x_format_duration__mutmut_8': x_format_duration__mutmut_8, 
    'x_format_duration__mutmut_9': x_format_duration__mutmut_9, 
    'x_format_duration__mutmut_10': x_format_duration__mutmut_10
}

def format_duration(*args, **kwargs):
    result = _mutmut_trampoline(x_format_duration__mutmut_orig, x_format_duration__mutmut_mutants, args, kwargs)
    return result 

format_duration.__signature__ = _mutmut_signature(x_format_duration__mutmut_orig)
x_format_duration__mutmut_orig.__name__ = 'x_format_duration'


__all__ = [
    "ensure_dir",
    "load_json",
    "save_json",
    "get_timestamp",
    "sanitize_filename",
    "truncate_string",
    "format_duration",
]
