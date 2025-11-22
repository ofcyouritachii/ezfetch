# ezfetch

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/ofcyouritachii/ezfetch)

> A blazing-fast, highly customizable, cross-platform system information tool written in Python.

Inspired by neofetch but with modern features, extensive customization, better performance, and rich CLI options.

---

## ✨ Features

- **⚡ Fast & Lightweight** — Pure Python with minimal dependencies (only psutil)
- **🌍 Cross-platform** — Linux (X11/Wayland), macOS, Windows, and Termux
- **🎨 Beautiful Output** — ASCII art logos with customizable color themes
- **📊 Comprehensive Info** — OS, CPU, GPU, RAM, resolution, shell, uptime, DE/WM, and more
- **🎭 Multiple Themes** — 6 built-in themes (default, nord, dracula, gruvbox, monokai, solarized)
- **🐧 16+ Logos** — Arch, Ubuntu, Debian, Fedora, Manjaro, Pop!_OS, Alpine, Gentoo, Kali, and more
- **⚙️ Highly Configurable** — JSON config file with extensive options
- **🎯 Smart Detection** — Auto-identifies desktop environments and window managers
- **📦 Smart Caching** — Cache expensive operations (3x faster on cached runs)
- **🔧 Rich CLI** — 11+ command-line options for quick customization
- **📄 JSON Export** — Machine-readable output for scripting and automation

---

## 📥 Installation

### Quick Start

```bash
git clone https://github.com/ofcyouritachii/ezfetch.git
cd ezfetch
python3 -m ezfetch
```

### Install System-wide

```bash
git clone https://github.com/ofcyouritachii/ezfetch.git
cd ezfetch
pip install -e .
ezfetch
```

---

## 🚀 Usage

### Basic Usage

```bash
ezfetch
```

### Command-Line Options

```bash
# Show version
ezfetch --version

# Use a specific logo
ezfetch --logo arch
ezfetch --logo ubuntu

# List all available logos
ezfetch --list-logos

# Use a color theme
ezfetch --theme nord
ezfetch --theme dracula

# List all available themes
ezfetch --list-themes

# Hide the logo
ezfetch --no-logo

# Disable colors
ezfetch --no-color

# Use custom logo
ezfetch --custom-logo /path/to/ascii-art.txt

# Export as JSON
ezfetch --json

# Show specific fields only
ezfetch --field OS --field CPU --field Memory

# Use custom config file
ezfetch --config /path/to/config.json
```

---

## ⚙️ Configuration

ezfetch creates a config file at `~/.config/ezfetch/config.json` which you can customize.

### Example Configuration

```json
{
  "display": {
    "show_logo": true,
    "show_colors": true,
    "truncate_length": 50,
    "logo_padding": 30
  },
  "theme": {
    "label_color": "bright_green",
    "value_color": "bright_cyan",
    "logo_color": "cyan"
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
      "Locale"
    ],
    "hide_unavailable": true,
    "hide_unknown": false
  },
  "performance": {
    "cache_enabled": true,
    "cache_duration": 300
  }
}
```

---

## 🎨 Available Themes

- **default** — Classic green and cyan
- **nord** — Cool northern palette
- **dracula** — Dark purple theme
- **gruvbox** — Retro warm colors
- **monokai** — Sublime Text inspired
- **solarized** — Precision colors

---

## 🐧 Supported Logos

- Arch Linux
- Ubuntu
- Debian
- Linux Mint
- Fedora
- Red Hat
- Manjaro
- Pop!_OS
- Alpine Linux
- Gentoo
- Kali Linux
- macOS
- Windows

*Custom logos supported via `--custom-logo` flag!*

---

## 📦 System Information Displayed

- **User & Host** — Current user and hostname
- **OS** — Operating system name and version
- **Kernel** — Kernel version
- **Uptime** — System uptime
- **Packages** — Number of installed packages (supports dpkg, rpm, pacman, apt, dnf, brew, etc.)
- **Shell** — Current shell with version
- **Resolution** — Screen resolution (X11/Wayland)
- **Desktop Environment** — DE with version (GNOME, KDE, XFCE, etc.)
- **Window Manager** — WM detection (Mutter, KWin, i3, Hyprland, etc.)
- **Terminal** — Terminal emulator
- **CPU** — Processor model, cores, and frequency
- **GPU** — Graphics card information
- **Memory** — RAM usage (used/total)
- **Swap** — Swap memory usage
- **Disk** — Disk usage with filesystem type
- **Local IP** — Network interface and IP address
- **Battery** — Battery status and percentage (laptops)
- **Locale** — System locale

---

## 🔧 Advanced Features

### Caching

ezfetch intelligently caches slow operations (like package counting) in `~/.cache/ezfetch/` to improve performance. Cache duration is configurable.

### Custom Colors

You can use RGB/hex colors in themes:

```python
from ezfetch.colors import Colors

# Use RGB
custom_color = Colors.rgb(255, 87, 51)

# Use hex
custom_color = Colors.from_hex("#FF5733")
```

### JSON Output

Perfect for scripting and automation:

```bash
ezfetch --json | jq '.CPU'
```

---

## 📋 Usage Examples

### Add to Shell Startup

Add to `~/.bashrc` or `~/.zshrc`:
```bash
ezfetch
```

### System Monitoring Script

```bash
#!/bin/bash
ezfetch --json | jq '{CPU: .CPU, Memory: .Memory, Disk: .Disk}'
```

### Custom Configuration

Create `~/.config/ezfetch/config.json`:
```json
{
  "fields": {
    "enabled": ["User", "OS", "Shell", "CPU", "Memory"]
  },
  "theme": {
    "label_color": "bright_magenta",
    "value_color": "bright_yellow"
  }
}
```

### Integration Examples

```bash
# Minimal output
ezfetch --no-logo --field OS --field CPU --field Memory

# Specific theme and logo
ezfetch --logo ubuntu --theme nord

# JSON with jq filtering
ezfetch --json | jq '.CPU'

# Save system info
ezfetch --json > system-info.json
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Issues:** [Report bugs or request features](https://github.com/ofcyouritachii/ezfetch/issues)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- **Inspired by:** [neofetch](https://github.com/dylanaraps/neofetch)
- **Created by:** yokaimsi & himonshuuu
- **ASCII Logos:** Various open-source projects

---

## 🔗 Links

- **Repository:** [github.com/ofcyouritachii/ezfetch](https://github.com/ofcyouritachii/ezfetch)
- **Issues:** [Bug Reports & Feature Requests](https://github.com/ofcyouritachii/ezfetch/issues)
- **Version:** 1.1.0

---

**Made with ❤️ by the ezfetch team**
