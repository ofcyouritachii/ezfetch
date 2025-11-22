"""
Configuration management for ezfetch
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


DEFAULT_CONFIG = {
    "display": {
        "show_logo": True,
        "show_colors": True,
        "truncate_length": 50,
        "logo_padding": 30,
    },
    "theme": {
        "label_color": "bright_green",
        "value_color": "bright_cyan",
        "logo_color": "cyan",
    },
    "fields": {
        "enabled": [
            "User",
            "Host",
            "OS",
            "Kernel",
            "Uptime",
            "Packages",
            "Shell",
            "Resolution",
            "DE",
            "WM",
            "Terminal",
            "CPU",
            "GPU",
            "Memory",
            "Swap",
            "Disk",
            "Local IP",
            "Battery",
            "Locale",
        ],
        "hide_unavailable": True,
        "hide_unknown": False,
    },
    "performance": {
        "cache_enabled": True,
        "cache_duration": 300,  # 5 minutes
    },
}


class Config:
    """Configuration manager for ezfetch"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_dir = Path.home() / ".config" / "ezfetch"
        self.config_file = self.config_dir / "config.json"
        
        if config_path:
            self.config_file = Path(config_path)
        
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = DEFAULT_CONFIG.copy()
                self._deep_merge(config, user_config)
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Deep merge override dict into base dict"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key path"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys: str, value: Any) -> None:
        """Set configuration value by dot-separated key path"""
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value

    def save(self) -> None:
        """Save configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")

    def reset(self) -> None:
        """Reset configuration to defaults"""
        self.config = DEFAULT_CONFIG.copy()


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance"""
    global _config_instance
    if _config_instance is None or config_path:
        _config_instance = Config(config_path)
    return _config_instance
