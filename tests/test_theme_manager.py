"""Unit tests for ThemeManager and theme system."""

import pytest
import json
import tempfile
from pathlib import Path
from src.theme_manager import ColorScheme, Theme, ThemeManager


class TestColorScheme:
    """Test ColorScheme."""

    def test_create_color_scheme(self):
        """Test creating a color scheme."""
        scheme = ColorScheme(
            background="#FFFFFF",
            foreground="#000000",
            line_number_bg="#F5F5F5",
            line_number_fg="#999999",
            selection_bg="#B4D7FF",
            selection_fg="#000000",
            cursor_color="#000000",
            current_line_bg="#F0F0F0",
            key_color="#0066CC",
            string_color="#009900",
            number_color="#CC6600",
            boolean_color="#CC0000",
            null_color="#666666",
            bracket_color="#666666",
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
            whitespace_color="#CCCCCC",
            line_ending_color="#CCCCCC",
        )

        assert scheme.background == "#FFFFFF"
        assert scheme.foreground == "#000000"

    def test_color_scheme_to_dict(self):
        """Test converting color scheme to dict."""
        scheme = ColorScheme(
            background="#FFFFFF",
            foreground="#000000",
            line_number_bg="#F5F5F5",
            line_number_fg="#999999",
            selection_bg="#B4D7FF",
            selection_fg="#000000",
            cursor_color="#000000",
            current_line_bg="#F0F0F0",
            key_color="#0066CC",
            string_color="#009900",
            number_color="#CC6600",
            boolean_color="#CC0000",
            null_color="#666666",
            bracket_color="#666666",
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
            whitespace_color="#CCCCCC",
            line_ending_color="#CCCCCC",
        )

        scheme_dict = scheme.to_dict()
        assert isinstance(scheme_dict, dict)
        assert scheme_dict["background"] == "#FFFFFF"

    def test_color_scheme_from_dict(self):
        """Test creating color scheme from dict."""
        data = {
            "background": "#FFFFFF",
            "foreground": "#000000",
            "line_number_bg": "#F5F5F5",
            "line_number_fg": "#999999",
            "selection_bg": "#B4D7FF",
            "selection_fg": "#000000",
            "cursor_color": "#000000",
            "current_line_bg": "#F0F0F0",
            "key_color": "#0066CC",
            "string_color": "#009900",
            "number_color": "#CC6600",
            "boolean_color": "#CC0000",
            "null_color": "#666666",
            "bracket_color": "#666666",
            "menu_bg": "#FFFFFF",
            "menu_fg": "#000000",
            "menu_hover_bg": "#E8E8E8",
            "button_bg": "#E8E8E8",
            "button_fg": "#000000",
            "status_bar_bg": "#F5F5F5",
            "status_bar_fg": "#000000",
            "tab_bg": "#EBEBEB",
            "tab_fg": "#666666",
            "tab_active_bg": "#FFFFFF",
            "tab_active_fg": "#000000",
            "error_color": "#CC0000",
            "warning_color": "#FF8800",
            "info_color": "#0066CC",
            "whitespace_color": "#CCCCCC",
            "line_ending_color": "#CCCCCC",
        }

        scheme = ColorScheme.from_dict(data)
        assert scheme.background == "#FFFFFF"
        assert scheme.foreground == "#000000"


class TestTheme:
    """Test Theme."""

    def test_create_theme(self):
        """Test creating a theme."""
        scheme = ThemeManager.LIGHT_THEME.colors
        theme = Theme("Light", "light", scheme)

        assert theme.name == "Light"
        assert theme.mode == "light"
        assert theme.colors is not None

    def test_theme_to_dict(self):
        """Test converting theme to dict."""
        theme = ThemeManager.LIGHT_THEME
        theme_dict = theme.to_dict()

        assert theme_dict["name"] == "Light"
        assert theme_dict["mode"] == "light"
        assert "colors" in theme_dict

    def test_theme_from_dict(self):
        """Test creating theme from dict."""
        original = ThemeManager.LIGHT_THEME
        theme_dict = original.to_dict()
        restored = Theme.from_dict(theme_dict)

        assert restored.name == original.name
        assert restored.mode == original.mode
        assert restored.colors.background == original.colors.background


class TestThemeManager:
    """Test ThemeManager."""

    def test_create_theme_manager(self):
        """Test creating theme manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            assert manager is not None
            assert manager.current_theme is not None

    def test_light_theme_exists(self):
        """Test light theme is available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            theme = manager.get_theme("light")
            assert theme.name == "Light"
            assert theme.mode == "light"

    def test_dark_theme_exists(self):
        """Test dark theme is available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            theme = manager.get_theme("dark")
            assert theme.name == "Dark"
            assert theme.mode == "dark"

    def test_set_theme(self):
        """Test setting a theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            result = manager.set_theme("dark")
            assert result is True
            assert manager.current_theme.name == "Dark"

    def test_set_invalid_theme(self):
        """Test setting invalid theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            result = manager.set_theme("nonexistent")
            assert result is False

    def test_get_current_theme(self):
        """Test getting current theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            theme = manager.get_current_theme()
            assert theme is not None
            assert theme.mode in ["light", "dark"]

    def test_get_available_themes(self):
        """Test getting available themes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            themes = manager.get_available_themes()
            assert "light" in themes
            assert "dark" in themes

    def test_toggle_theme_from_light_to_dark(self):
        """Test toggling from light to dark."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            manager.set_theme("light")
            new_theme = manager.toggle_theme()
            assert new_theme.mode == "dark"
            assert manager.current_theme.mode == "dark"

    def test_toggle_theme_from_dark_to_light(self):
        """Test toggling from dark to light."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            manager.set_theme("dark")
            new_theme = manager.toggle_theme()
            assert new_theme.mode == "light"
            assert manager.current_theme.mode == "light"

    def test_theme_persistence(self):
        """Test theme preference is saved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir)

            # Create manager and set theme
            manager1 = ThemeManager(config_path)
            manager1.set_theme("dark")

            # Create new manager - should load dark theme
            manager2 = ThemeManager(config_path)
            assert manager2.current_theme.mode == "dark"

    def test_register_custom_theme(self):
        """Test registering a custom theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))

            custom_scheme = ThemeManager.LIGHT_THEME.colors
            custom_theme = Theme("Custom", "light", custom_scheme)

            result = manager.register_theme(custom_theme)
            assert result is True
            assert "custom" in manager.get_available_themes()

    def test_cannot_register_duplicate_theme(self):
        """Test cannot register duplicate theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))

            custom_scheme = ThemeManager.LIGHT_THEME.colors
            custom_theme = Theme("Light", "light", custom_scheme)

            result = manager.register_theme(custom_theme)
            assert result is False

    def test_export_theme(self):
        """Test exporting a theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            export_path = Path(tmpdir) / "exported_theme.json"

            result = manager.export_theme("light", export_path)
            assert result is True
            assert export_path.exists()

            # Verify exported JSON
            with open(export_path) as f:
                data = json.load(f)
                assert data["name"] == "Light"

    def test_import_theme(self):
        """Test importing a theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))

            # Create and export a custom theme
            scheme = ThemeManager.LIGHT_THEME.colors
            custom_theme = Theme("ImportedTheme", "light", scheme)
            manager.register_theme(custom_theme)

            export_path = Path(tmpdir) / "exported_theme.json"
            manager.export_theme("importedtheme", export_path)

            # Create new manager and import
            manager2 = ThemeManager(Path(tmpdir) / "config")
            result = manager2.import_theme(export_path)
            assert result is True
            available = manager2.get_available_themes()
            assert "importedtheme" in available

    def test_export_invalid_theme(self):
        """Test exporting invalid theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            export_path = Path(tmpdir) / "theme.json"

            result = manager.export_theme("nonexistent", export_path)
            assert result is False
            assert not export_path.exists()

    def test_import_invalid_file(self):
        """Test importing invalid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))

            invalid_path = Path(tmpdir) / "invalid.json"
            invalid_path.write_text("invalid json")

            result = manager.import_theme(invalid_path)
            assert result is False

    def test_get_stylesheet(self):
        """Test generating stylesheet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            stylesheet = manager.get_stylesheet()

            assert isinstance(stylesheet, str)
            assert len(stylesheet) > 0
            assert "QMainWindow" in stylesheet
            assert "background-color" in stylesheet

    def test_stylesheet_for_dark_theme(self):
        """Test stylesheet for dark theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            dark_theme = manager.get_theme("dark")
            stylesheet = manager.get_stylesheet(dark_theme)

            assert dark_theme.colors.background in stylesheet
            assert dark_theme.colors.foreground in stylesheet

    def test_stylesheet_for_light_theme(self):
        """Test stylesheet for light theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager(Path(tmpdir))
            light_theme = manager.get_theme("light")
            stylesheet = manager.get_stylesheet(light_theme)

            assert light_theme.colors.background in stylesheet
            assert light_theme.colors.foreground in stylesheet
