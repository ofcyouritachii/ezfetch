"""
Utility functions for ezfetch
"""
import os
import subprocess
import shutil
from typing import Optional, List, Tuple


def run_command(cmd: str, shell: bool = True, timeout: int = 5) -> Optional[str]:
    """
    Run a shell command and return output or None on failure
    
    Args:
        cmd: Command to run
        shell: Whether to use shell
        timeout: Command timeout in seconds
    
    Returns:
        Command output as string or None on failure
    """
    try:
        result = subprocess.check_output(
            cmd,
            shell=shell,
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=timeout
        )
        return result.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None


def read_file(filepath: str) -> Optional[str]:
    """
    Safely read a file and return its contents
    
    Args:
        filepath: Path to file
    
    Returns:
        File contents or None on failure
    """
    try:
        with open(filepath, "r") as f:
            return f.read()
    except (IOError, FileNotFoundError):
        return None


def read_file_line(filepath: str, search_prefix: str) -> Optional[str]:
    """
    Read a file and return the first line starting with prefix
    
    Args:
        filepath: Path to file
        search_prefix: Prefix to search for
    
    Returns:
        Matching line or None
    """
    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith(search_prefix):
                    return line.strip()
    except (IOError, FileNotFoundError):
        pass
    return None


def which(command: str) -> bool:
    """Check if a command is available"""
    return shutil.which(command) is not None


def format_size(bytes_value: int, decimal_places: int = 2) -> str:
    """
    Format bytes to human-readable size
    
    Args:
        bytes_value: Size in bytes
        decimal_places: Number of decimal places
    
    Returns:
        Formatted string (e.g., "1.23 GiB")
    """
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(bytes_value)
    unit_index = 0
    
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    
    return f"{value:.{decimal_places}f} {units[unit_index]}"


def format_uptime(seconds: int) -> str:
    """
    Format uptime in seconds to human-readable string
    
    Args:
        seconds: Uptime in seconds
    
    Returns:
        Formatted string (e.g., "2 days, 3 hours, 15 mins")
    """
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0 or not parts:
        parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
    
    return ", ".join(parts)


def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to max length with suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_env(key: str, default: str = "") -> str:
    """Get environment variable with default"""
    return os.environ.get(key, default)


def parse_version(version_string: str) -> Tuple[int, ...]:
    """
    Parse version string to tuple of integers
    
    Args:
        version_string: Version string (e.g., "1.2.3")
    
    Returns:
        Tuple of version numbers (e.g., (1, 2, 3))
    """
    try:
        return tuple(int(x) for x in version_string.split(".") if x.isdigit())
    except (ValueError, AttributeError):
        return (0,)


def clean_string(text: str) -> str:
    """Remove extra whitespace and quotes from string"""
    return text.strip().strip('"').strip("'")
