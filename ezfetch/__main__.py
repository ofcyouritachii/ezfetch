"""
Main entry point for ezfetch
"""
import argparse
import json
import sys
from typing import Dict, Any, Optional

from . import __version__
from .logo import get_logo, list_logos
from .info import *
from .colors import Colors, Theme, colorize
from .config import get_config
from .utils import truncate


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="ezfetch - A fast, cross-platform system info tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"ezfetch {__version__}",
        help="Show version and exit"
    )
    
    parser.add_argument(
        "-l", "--logo",
        type=str,
        metavar="NAME",
        help=f"Logo to display (available: {', '.join(list_logos()[:5])}...)"
    )
    
    parser.add_argument(
        "--list-logos",
        action="store_true",
        help="List all available logos"
    )
    
    parser.add_argument(
        "--no-logo",
        action="store_true",
        help="Don't display logo"
    )
    
    parser.add_argument(
        "--custom-logo",
        type=str,
        metavar="PATH",
        help="Path to custom ASCII logo file"
    )
    
    parser.add_argument(
        "-t", "--theme",
        type=str,
        default="default",
        help=f"Color theme (available: {', '.join(Theme.list_themes())})"
    )
    
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List all available themes"
    )
    
    parser.add_argument(
        "-c", "--config",
        type=str,
        metavar="PATH",
        help="Path to custom config file"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colors in output"
    )
    
    parser.add_argument(
        "-f", "--field",
        action="append",
        metavar="NAME",
        help="Show specific field(s) only (can be used multiple times)"
    )
    
    return parser.parse_args()


def get_system_info() -> Dict[str, Any]:
    """Collect all system information"""
    return {
        "User": get_user_host(),
        "Host": get_host(),
        "OS": get_os(),
        "Kernel": get_kernel(),
        "Uptime": get_uptime(),
        "Packages": get_packages(),
        "Shell": get_shell(),
        "Resolution": get_resolution(),
        "DE": get_desktop_env(),
        "WM": get_window_manager(),
        "Terminal": get_terminal(),
        "CPU": get_cpu(),
        "GPU": get_gpu(),
        "Memory": get_memory(),
        "Swap": get_swap(),
        "Disk": get_disk(),
        "Local IP": get_ip(),
        "Battery": get_battery(),
        "Locale": get_locale(),
    }


def filter_fields(
    fields: Dict[str, Any],
    enabled_fields: Optional[list] = None,
    hide_unavailable: bool = True,
    hide_unknown: bool = False
) -> Dict[str, str]:
    """Filter and format fields based on configuration"""
    filtered = {}
    
    for label, value in fields.items():
        # Skip if not in enabled list
        if enabled_fields and label not in enabled_fields:
            continue
        
        # Skip unavailable fields
        if hide_unavailable and value in ["Unavailable", "N/A"]:
            continue
        
        # Skip unknown fields
        if hide_unknown and value == "Unknown":
            continue
        
        # Add field
        filtered[label] = value if value else "Unknown"
    
    return filtered


def display_json(info: Dict[str, str]) -> None:
    """Display system info as JSON"""
    print(json.dumps(info, indent=2))


def display_info(
    logo_name: Optional[str] = None,
    custom_logo_path: Optional[str] = None,
    show_logo: bool = True,
    theme_name: str = "default",
    use_colors: bool = True,
    fields_filter: Optional[list] = None,
    truncate_length: int = 50,
    logo_padding: int = 30,
) -> None:
    """
    Display system information with ASCII logo
    
    Args:
        logo_name: Name of logo to display
        custom_logo_path: Path to custom logo file
        show_logo: Whether to show logo
        theme_name: Name of color theme
        use_colors: Whether to use colors
        fields_filter: List of field names to display
        truncate_length: Maximum length for field values
        logo_padding: Padding between logo and fields
    """
    # Get configuration
    config = get_config()
    
    # Initialize theme
    theme = Theme(theme_name) if use_colors else Theme("default")
    
    # Get system info
    info = get_system_info()
    
    # Filter fields
    enabled_fields = fields_filter or config.get("fields", "enabled")
    hide_unavailable = config.get("fields", "hide_unavailable", default=True)
    hide_unknown = config.get("fields", "hide_unknown", default=False)
    
    filtered_info = filter_fields(
        info,
        enabled_fields=enabled_fields,
        hide_unavailable=hide_unavailable,
        hide_unknown=hide_unknown
    )
    
    # Truncate long values
    for label in filtered_info:
        if len(filtered_info[label]) > truncate_length:
            filtered_info[label] = truncate(filtered_info[label], truncate_length)
    
    # Prepare logo
    logo_lines = []
    if show_logo:
        logo = get_logo(logo_name, custom_logo_path)
        logo_lines = logo.splitlines()
    
    # Prepare field lines
    max_label = max(len(label) for label in filtered_info.keys()) if filtered_info else 0
    field_lines = []
    
    for label, value in filtered_info.items():
        if use_colors:
            label_colored = colorize(label, theme.get("label"))
            separator = colorize(":", theme.get("separator"))
            value_colored = colorize(value, theme.get("value"))
            field_line = f"{label_colored:<{max_label + 10}} {separator} {value_colored}"
        else:
            field_line = f"{label:<{max_label}} : {value}"
        field_lines.append(field_line)
    
    # Display output
    max_lines = max(len(logo_lines), len(field_lines))
    
    for i in range(max_lines):
        logo_line = logo_lines[i] if i < len(logo_lines) else ""
        field_line = field_lines[i] if i < len(field_lines) else ""
        
        if show_logo:
            print(f"{logo_line:<{logo_padding}}  {field_line}")
        else:
            print(field_line)


def main() -> None:
    """Main entry point"""
    args = parse_args()
    
    # Handle special flags
    if args.list_logos:
        print("Available logos:")
        for logo in list_logos():
            print(f"  - {logo}")
        sys.exit(0)
    
    if args.list_themes:
        print("Available themes:")
        for theme in Theme.list_themes():
            print(f"  - {theme}")
        sys.exit(0)
    
    # Load config
    config = get_config(args.config)
    
    # Get display settings
    show_logo = not args.no_logo and config.get("display", "show_logo", default=True)
    use_colors = not args.no_color and config.get("display", "show_colors", default=True)
    truncate_length = config.get("display", "truncate_length", default=50)
    logo_padding = config.get("display", "logo_padding", default=30)
    
    # Get system info
    info = get_system_info()
    
    # Handle JSON output
    if args.json:
        display_json(info)
        sys.exit(0)
    
    # Display info
    display_info(
        logo_name=args.logo,
        custom_logo_path=args.custom_logo,
        show_logo=show_logo,
        theme_name=args.theme,
        use_colors=use_colors,
        fields_filter=args.field,
        truncate_length=truncate_length,
        logo_padding=logo_padding,
    )


if __name__ == "__main__":
    main()
