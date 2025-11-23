"""Unit tests for visual indicators and whitespace analysis."""

import pytest
from src.visual_indicators import (
    LineEnding,
    VisualIndicatorSettings,
    LineEndingDetector,
    WhitespaceAnalyzer,
    VisualIndicatorRenderer,
)


class TestLineEnding:
    """Test LineEnding enum."""

    def test_line_ending_values(self):
        """Test line ending values."""
        assert LineEnding.LF.value == "\n"
        assert LineEnding.CRLF.value == "\r\n"
        assert LineEnding.CR.value == "\r"

    def test_line_ending_display_names(self):
        """Test line ending display names."""
        assert LineEnding.LF.display_name() == "LF"
        assert LineEnding.CRLF.display_name() == "CRLF"
        assert LineEnding.CR.display_name() == "CR"
        assert LineEnding.AUTO.display_name() == "Auto"


class TestVisualIndicatorSettings:
    """Test VisualIndicatorSettings."""

    def test_create_settings(self):
        """Test creating settings."""
        settings = VisualIndicatorSettings()
        assert settings.show_whitespace is False
        assert settings.show_line_endings is False
        assert settings.show_non_printable is False

    def test_create_settings_with_options(self):
        """Test creating settings with custom options."""
        settings = VisualIndicatorSettings(
            show_whitespace=True,
            show_line_endings=True,
        )
        assert settings.show_whitespace is True
        assert settings.show_line_endings is True

    def test_toggle_whitespace(self):
        """Test toggling whitespace visibility."""
        settings = VisualIndicatorSettings(show_whitespace=False)
        settings.toggle_whitespace()
        assert settings.show_whitespace is True
        settings.toggle_whitespace()
        assert settings.show_whitespace is False

    def test_toggle_line_endings(self):
        """Test toggling line ending visibility."""
        settings = VisualIndicatorSettings(show_line_endings=False)
        settings.toggle_line_endings()
        assert settings.show_line_endings is True

    def test_toggle_non_printable(self):
        """Test toggling non-printable visibility."""
        settings = VisualIndicatorSettings(show_non_printable=False)
        settings.toggle_non_printable()
        assert settings.show_non_printable is True


class TestLineEndingDetector:
    """Test LineEndingDetector."""

    def test_detect_lf(self):
        """Test detecting LF line endings."""
        text = "line1\nline2\nline3"
        assert LineEndingDetector.detect(text) == LineEnding.LF

    def test_detect_crlf(self):
        """Test detecting CRLF line endings."""
        text = "line1\r\nline2\r\nline3"
        assert LineEndingDetector.detect(text) == LineEnding.CRLF

    def test_detect_cr(self):
        """Test detecting CR line endings."""
        text = "line1\rline2\rline3"
        assert LineEndingDetector.detect(text) == LineEnding.CR

    def test_detect_empty_string(self):
        """Test detecting line ending in empty string."""
        assert LineEndingDetector.detect("") == LineEnding.LF

    def test_detect_single_line(self):
        """Test detecting line ending in single line."""
        assert LineEndingDetector.detect("no newline") == LineEnding.LF

    def test_get_line_ending_char_lf(self):
        """Test getting LF character."""
        assert LineEndingDetector.get_line_ending_char(LineEnding.LF) == "\n"

    def test_get_line_ending_char_crlf(self):
        """Test getting CRLF characters."""
        assert LineEndingDetector.get_line_ending_char(LineEnding.CRLF) == "\r\n"

    def test_get_line_ending_char_cr(self):
        """Test getting CR character."""
        assert LineEndingDetector.get_line_ending_char(LineEnding.CR) == "\r"

    def test_convert_crlf_to_lf(self):
        """Test converting CRLF to LF."""
        text = "line1\r\nline2\r\nline3"
        result = LineEndingDetector.convert_line_endings(
            text, LineEnding.CRLF, LineEnding.LF
        )
        assert result == "line1\nline2\nline3"

    def test_convert_lf_to_crlf(self):
        """Test converting LF to CRLF."""
        text = "line1\nline2\nline3"
        result = LineEndingDetector.convert_line_endings(
            text, LineEnding.LF, LineEnding.CRLF
        )
        assert result == "line1\r\nline2\r\nline3"

    def test_convert_cr_to_lf(self):
        """Test converting CR to LF."""
        text = "line1\rline2\rline3"
        result = LineEndingDetector.convert_line_endings(
            text, LineEnding.CR, LineEnding.LF
        )
        assert result == "line1\nline2\nline3"

    def test_convert_same_ending(self):
        """Test converting to same ending returns unchanged."""
        text = "line1\nline2\nline3"
        result = LineEndingDetector.convert_line_endings(
            text, LineEnding.LF, LineEnding.LF
        )
        assert result == text


class TestWhitespaceAnalyzer:
    """Test WhitespaceAnalyzer."""

    def test_count_lines_with_tabs(self):
        """Test counting lines with tabs."""
        text = "line1\n\tline2\nline3\n\tline4"
        assert WhitespaceAnalyzer.count_lines_with_tabs(text) == 2

    def test_count_lines_with_tabs_empty(self):
        """Test counting tabs in empty text."""
        assert WhitespaceAnalyzer.count_lines_with_tabs("") == 0

    def test_count_lines_with_tabs_none(self):
        """Test counting tabs when none exist."""
        text = "line1\nline2\nline3"
        assert WhitespaceAnalyzer.count_lines_with_tabs(text) == 0

    def test_count_lines_with_spaces(self):
        """Test counting lines with spaces."""
        text = "line1\n  line2\nline3\n    line4"
        assert WhitespaceAnalyzer.count_lines_with_spaces(text) == 2

    def test_count_lines_with_spaces_empty(self):
        """Test counting spaces in empty text."""
        assert WhitespaceAnalyzer.count_lines_with_spaces("") == 0

    def test_get_indentation_style_tabs(self):
        """Test detecting tabs as indentation."""
        text = "\tline1\n\tline2\nline3"
        assert WhitespaceAnalyzer.get_indentation_style(text) == "tabs"

    def test_get_indentation_style_spaces(self):
        """Test detecting spaces as indentation."""
        text = "    line1\n    line2\nline3"
        assert WhitespaceAnalyzer.get_indentation_style(text) == "spaces"

    def test_get_indentation_style_mixed(self):
        """Test detecting mixed indentation."""
        text = "\tline1\n    line2\nline3"
        assert WhitespaceAnalyzer.get_indentation_style(text) == "mixed"

    def test_get_indentation_style_none(self):
        """Test detecting no indentation."""
        text = "line1\nline2\nline3"
        assert WhitespaceAnalyzer.get_indentation_style(text) == "none"

    def test_get_indent_size_two(self):
        """Test detecting 2-space indentation."""
        text = "line\n  indent\n    double"
        size = WhitespaceAnalyzer.get_indent_size(text)
        assert size == 2

    def test_get_indent_size_four(self):
        """Test detecting 4-space indentation."""
        text = "line\n    indent\n        double"
        size = WhitespaceAnalyzer.get_indent_size(text)
        assert size == 4

    def test_get_indent_size_default(self):
        """Test default indent size for empty text."""
        assert WhitespaceAnalyzer.get_indent_size("") == 4

    def test_get_indent_size_no_indentation(self):
        """Test indent size with no indentation."""
        text = "line1\nline2\nline3"
        assert WhitespaceAnalyzer.get_indent_size(text) == 4


class TestVisualIndicatorRenderer:
    """Test VisualIndicatorRenderer."""

    def test_render_whitespace_disabled(self):
        """Test rendering with whitespace disabled."""
        settings = VisualIndicatorSettings(show_whitespace=False)
        text = "hello\tworld"
        result = VisualIndicatorRenderer.render_whitespace(text, settings)
        assert result == text

    def test_render_whitespace_tabs(self):
        """Test rendering tabs."""
        settings = VisualIndicatorSettings(
            show_whitespace=True,
            tab_char="→",
        )
        text = "hello\tworld"
        result = VisualIndicatorRenderer.render_whitespace(text, settings)
        assert "→" in result
        assert "\t" not in result

    def test_render_whitespace_spaces(self):
        """Test rendering spaces."""
        settings = VisualIndicatorSettings(
            show_whitespace=True,
            space_char="·",
        )
        text = "hello world"
        result = VisualIndicatorRenderer.render_whitespace(text, settings)
        assert "·" in result

    def test_render_line_endings_disabled(self):
        """Test rendering with line endings disabled."""
        settings = VisualIndicatorSettings(show_line_endings=False)
        text = "line1\nline2"
        result = VisualIndicatorRenderer.render_line_endings(text, settings)
        assert result == text

    def test_render_line_endings_lf(self):
        """Test rendering LF line endings."""
        settings = VisualIndicatorSettings(
            show_line_endings=True,
            line_ending_char="↵",
        )
        text = "line1\nline2"
        result = VisualIndicatorRenderer.render_line_endings(text, settings)
        assert "↵" in result
        assert "\n" not in result

    def test_render_line_endings_crlf(self):
        """Test rendering CRLF line endings."""
        settings = VisualIndicatorSettings(
            show_line_endings=True,
            line_ending_char="↵",
        )
        text = "line1\r\nline2"
        result = VisualIndicatorRenderer.render_line_endings(text, settings)
        assert "↵" in result
        assert "\r" not in result
