"""Theme management system for jText with light and dark modes."""

import json
from pathlib import Path
from typing import Dict, Optional, Literal
from dataclasses import dataclass


@dataclass
class ColorScheme:
    """Color scheme for a theme."""

    # Editor colors
    background: str
    foreground: str
    line_number_bg: str
    line_number_fg: str
    selection_bg: str
    selection_fg: str
    cursor_color: str
    current_line_bg: str

    # Syntax highlighting colors
    key_color: str
    string_color: str
    number_color: str
    boolean_color: str
    null_color: str
    bracket_color: str

    # UI colors
    menu_bg: str
    menu_fg: str
    menu_hover_bg: str
    button_bg: str
    button_fg: str
    status_bar_bg: str
    status_bar_fg: str
    tab_bg: str
    tab_fg: str
    tab_active_bg: str
    tab_active_fg: str
    error_color: str
    warning_color: str
    info_color: str

    # Visibility indicators
    whitespace_color: str
    line_ending_color: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "ColorScheme":
        """Create from dictionary."""
        return cls(**data)


class Theme:
    """Represents a complete theme."""

    def __init__(self, name: str, mode: Literal["light", "dark"], colors: ColorScheme):
        """Initialize theme.

        Args:
            name: Theme name
            mode: 'light' or 'dark'
            colors: Color scheme
        """
        self.name = name
        self.mode = mode
        self.colors = colors

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "mode": self.mode,
            "colors": self.colors.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Theme":
        """Create from dictionary."""
        colors = ColorScheme.from_dict(data["colors"])
        return cls(data["name"], data["mode"], colors)


class ThemeManager:
    """Manages themes and applies them to the application."""

    LIGHT_THEME = Theme(
        "Light",
        "light",
        ColorScheme(
            # Editor colors
            background="#FFFFFF",
            foreground="#000000",
            line_number_bg="#F5F5F5",
            line_number_fg="#999999",
            selection_bg="#B4D7FF",
            selection_fg="#000000",
            cursor_color="#000000",
            current_line_bg="#F0F0F0",
            # Syntax colors
            key_color="#0066CC",  # Blue
            string_color="#009900",  # Green
            number_color="#CC6600",  # Orange
            boolean_color="#CC0000",  # Red
            null_color="#666666",  # Gray
            bracket_color="#666666",  # Gray
            # UI colors
            menu_bg="#FFFFFF",
            menu_fg="#000000",
            menu_hover_bg="#E8E8E8",
            button_bg="#E8E8E8",
            button_fg="#000000",
            status_bar_bg="#F5F5F5",
            status_bar_fg="#000000",
            tab_bg="#EBEBEB",
            tab_fg="#666666",
            tab_active_bg="#FFFFFF",
            tab_active_fg="#000000",
            error_color="#CC0000",
            warning_color="#FF8800",
            info_color="#0066CC",
            # Visibility
            whitespace_color="#CCCCCC",
            line_ending_color="#CCCCCC",
        ),
    )

    DARK_THEME = Theme(
        "Dark",
        "dark",
        ColorScheme(
            # Editor colors
            background="#1E1E1E",
            foreground="#E0E0E0",
            line_number_bg="#252526",
            line_number_fg="#858585",
            selection_bg="#264F78",
            selection_fg="#E0E0E0",
            cursor_color="#AEAFAD",
            current_line_bg="#2D2D30",
            # Syntax colors
            key_color="#569CD6",  # Light Blue
            string_color="#CE9178",  # Orange (strings)
            number_color="#B5CEA8",  # Light Green
            boolean_color="#569CD6",  # Light Blue
            null_color="#999999",  # Gray
            bracket_color="#D4D4D4",  # Light Gray
            # UI colors
            menu_bg="#3E3E42",
            menu_fg="#CCCCCC",
            menu_hover_bg="#4A4A50",
            button_bg="#3E3E42",
            button_fg="#CCCCCC",
            status_bar_bg="#007ACC",
            status_bar_fg="#FFFFFF",
            tab_bg="#2D2D30",
            tab_fg="#969696",
            tab_active_bg="#1E1E1E",
            tab_active_fg="#CCCCCC",
            error_color="#F48771",
            warning_color="#DCD7A5",
            info_color="#569CD6",
            # Visibility
            whitespace_color="#404040",
            line_ending_color="#404040",
        ),
    )

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize theme manager.

        Args:
            config_dir: Directory for config files (default ~/.config/jtext)
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "jtext"
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.themes: Dict[str, Theme] = {
            "light": self.LIGHT_THEME,
            "dark": self.DARK_THEME,
        }
        self.current_theme = self._load_current_theme()

    def _load_current_theme(self) -> Theme:
        """Load the current theme preference.

        Returns:
            Current theme, defaulting to light theme
        """
        theme_file = self.config_dir / "theme.json"

        if theme_file.exists():
            try:
                with open(theme_file, "r") as f:
                    data = json.load(f)
                    theme_name = data.get("theme", "light")
                    return self.themes.get(theme_name, self.LIGHT_THEME)
            except (json.JSONDecodeError, IOError):
                return self.LIGHT_THEME

        return self.LIGHT_THEME

    def _save_current_theme(self) -> None:
        """Save current theme preference."""
        theme_file = self.config_dir / "theme.json"

        try:
            with open(theme_file, "w") as f:
                json.dump(
                    {
                        "theme": self.current_theme.name.lower(),
                        "mode": self.current_theme.mode,
                    },
                    f,
                    indent=2,
                )
        except IOError:
            pass

    def set_theme(self, theme_name: str) -> bool:
        """Set the current theme.

        Args:
            theme_name: Name of theme ('light' or 'dark')

        Returns:
            True if theme was changed, False if theme not found
        """
        if theme_name.lower() not in self.themes:
            return False

        self.current_theme = self.themes[theme_name.lower()]
        self._save_current_theme()
        return True

    def get_theme(self, theme_name: Optional[str] = None) -> Theme:
        """Get a theme by name.

        Args:
            theme_name: Name of theme (default current theme)

        Returns:
            Theme object
        """
        if theme_name is None:
            return self.current_theme
        return self.themes.get(theme_name.lower(), self.current_theme)

    def get_current_theme(self) -> Theme:
        """Get the current theme."""
        return self.current_theme

    def get_available_themes(self) -> list[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())

    def toggle_theme(self) -> Theme:
        """Toggle between light and dark themes.

        Returns:
            The new current theme
        """
        if self.current_theme.mode == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")
        return self.current_theme

    def register_theme(self, theme: Theme) -> bool:
        """Register a custom theme.

        Args:
            theme: Theme to register

        Returns:
            True if successful
        """
        if theme.name.lower() not in self.themes:
            self.themes[theme.name.lower()] = theme
            return True
        return False

    def export_theme(self, theme_name: str, output_path: Path) -> bool:
        """Export a theme to a JSON file.

        Args:
            theme_name: Name of theme to export
            output_path: Path to save theme

        Returns:
            True if successful
        """
        theme = self.themes.get(theme_name.lower())
        if not theme:
            return False

        try:
            with open(output_path, "w") as f:
                json.dump(theme.to_dict(), f, indent=2)
            return True
        except IOError:
            return False

    def import_theme(self, theme_path: Path) -> bool:
        """Import a theme from a JSON file.

        Args:
            theme_path: Path to theme file

        Returns:
            True if successful
        """
        try:
            with open(theme_path, "r") as f:
                data = json.load(f)
                theme = Theme.from_dict(data)
                return self.register_theme(theme)
        except (json.JSONDecodeError, IOError, KeyError):
            return False

    def get_stylesheet(self, theme: Optional[Theme] = None) -> str:
        """Generate Qt stylesheet for theme.

        Args:
            theme: Theme to use (default current)

        Returns:
            Stylesheet string
        """
        if theme is None:
            theme = self.current_theme

        colors = theme.colors

        stylesheet = f"""
        QMainWindow {{
            background-color: {colors.background};
            color: {colors.foreground};
        }}

        QTextEdit {{
            background-color: {colors.background};
            color: {colors.foreground};
            selection-background-color: {colors.selection_bg};
            selection-color: {colors.selection_fg};
            border: none;
        }}

        QMenuBar {{
            background-color: {colors.menu_bg};
            color: {colors.menu_fg};
        }}

        QMenuBar::item:selected {{
            background-color: {colors.menu_hover_bg};
        }}

        QMenu {{
            background-color: {colors.menu_bg};
            color: {colors.menu_fg};
        }}

        QMenu::item:selected {{
            background-color: {colors.menu_hover_bg};
        }}

        QPushButton {{
            background-color: {colors.button_bg};
            color: {colors.button_fg};
            border: 1px solid {colors.foreground};
            border-radius: 4px;
            padding: 5px;
        }}

        QPushButton:hover {{
            background-color: {colors.menu_hover_bg};
        }}

        QTabWidget::pane {{
            border: none;
        }}

        QTabBar::tab {{
            background-color: {colors.tab_bg};
            color: {colors.tab_fg};
            padding: 8px 20px;
            margin-right: 2px;
        }}

        QTabBar::tab:selected {{
            background-color: {colors.tab_active_bg};
            color: {colors.tab_active_fg};
        }}

        QStatusBar {{
            background-color: {colors.status_bar_bg};
            color: {colors.status_bar_fg};
        }}

        QDialog {{
            background-color: {colors.background};
            color: {colors.foreground};
        }}

        QLineEdit {{
            background-color: {colors.background};
            color: {colors.foreground};
            border: 1px solid {colors.foreground};
            border-radius: 4px;
            padding: 5px;
        }}

        QCheckBox {{
            color: {colors.foreground};
        }}

        QLabel {{
            color: {colors.foreground};
        }}

        QTreeWidget {{
            background-color: {colors.background};
            color: {colors.foreground};
            selection-background-color: {colors.selection_bg};
            alternate-background-color: {colors.current_line_bg};
        }}
        """
        return stylesheet
