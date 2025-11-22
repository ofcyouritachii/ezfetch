"""
Color handling and theming for ezfetch
"""
from typing import Dict, Optional


class Colors:
    """ANSI color codes for terminal output"""
    
    # Reset
    RESET = "\033[0m"
    
    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Bold colors
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @staticmethod
    def rgb(r: int, g: int, b: int, background: bool = False) -> str:
        """
        Create RGB color code
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            background: Whether this is a background color
        
        Returns:
            ANSI color code string
        """
        code = 48 if background else 38
        return f"\033[{code};2;{r};{g};{b}m"
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """
        Convert hex color to RGB tuple
        
        Args:
            hex_color: Hex color string (e.g., "#FF5733" or "FF5733")
        
        Returns:
            RGB tuple (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def from_hex(hex_color: str, background: bool = False) -> str:
        """
        Create color code from hex string
        
        Args:
            hex_color: Hex color string (e.g., "#FF5733")
            background: Whether this is a background color
        
        Returns:
            ANSI color code string
        """
        r, g, b = Colors.hex_to_rgb(hex_color)
        return Colors.rgb(r, g, b, background)
    
    @classmethod
    def get_color(cls, name: str) -> str:
        """
        Get color code by name
        
        Args:
            name: Color name (e.g., "red", "bright_green")
        
        Returns:
            ANSI color code or empty string if not found
        """
        name_upper = name.upper().replace(" ", "_")
        return getattr(cls, name_upper, "")


class Theme:
    """Color theme for ezfetch display"""
    
    THEMES: Dict[str, Dict[str, str]] = {
        "default": {
            "label": Colors.BRIGHT_GREEN,
            "value": Colors.BRIGHT_CYAN,
            "logo": Colors.CYAN,
            "separator": Colors.WHITE,
        },
        "nord": {
            "label": Colors.from_hex("#88C0D0"),
            "value": Colors.from_hex("#ECEFF4"),
            "logo": Colors.from_hex("#5E81AC"),
            "separator": Colors.from_hex("#D8DEE9"),
        },
        "dracula": {
            "label": Colors.from_hex("#FF79C6"),
            "value": Colors.from_hex("#F8F8F2"),
            "logo": Colors.from_hex("#BD93F9"),
            "separator": Colors.from_hex("#6272A4"),
        },
        "gruvbox": {
            "label": Colors.from_hex("#B8BB26"),
            "value": Colors.from_hex("#EBDBB2"),
            "logo": Colors.from_hex("#83A598"),
            "separator": Colors.from_hex("#A89984"),
        },
        "monokai": {
            "label": Colors.from_hex("#A6E22E"),
            "value": Colors.from_hex("#F8F8F2"),
            "logo": Colors.from_hex("#66D9EF"),
            "separator": Colors.from_hex("#75715E"),
        },
        "solarized": {
            "label": Colors.from_hex("#859900"),
            "value": Colors.from_hex("#93A1A1"),
            "logo": Colors.from_hex("#268BD2"),
            "separator": Colors.from_hex("#586E75"),
        },
    }
    
    def __init__(self, theme_name: str = "default"):
        """
        Initialize theme
        
        Args:
            theme_name: Name of the theme to use
        """
        self.theme_name = theme_name
        self.colors = self.THEMES.get(theme_name, self.THEMES["default"])
    
    def get(self, element: str) -> str:
        """Get color for a theme element"""
        return self.colors.get(element, "")
    
    @classmethod
    def list_themes(cls) -> list:
        """Get list of available theme names"""
        return list(cls.THEMES.keys())


def colorize(text: str, color: str, reset: bool = True) -> str:
    """
    Colorize text with ANSI color codes
    
    Args:
        text: Text to colorize
        color: Color code or color name
        reset: Whether to add reset code at the end
    
    Returns:
        Colorized text
    """
    if not color:
        return text
    
    # Try to get color by name if it's not already a code
    if not color.startswith('\033'):
        color = Colors.get_color(color)
    
    if reset:
        return f"{color}{text}{Colors.RESET}"
    return f"{color}{text}"


def strip_ansi(text: str) -> str:
    """
    Remove ANSI color codes from text
    
    Args:
        text: Text containing ANSI codes
    
    Returns:
        Plain text without color codes
    """
    import re
    ansi_escape = re.compile(r'\033\[[0-9;]+m')
    return ansi_escape.sub('', text)
