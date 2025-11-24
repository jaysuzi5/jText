"""Unit tests for smart indentation."""

import pytest
from src.smart_indenter import SmartIndenter


class TestSmartIndenterBasic:
    """Test basic SmartIndenter functionality."""

    def test_create_indenter(self):
        """Test creating a smart indenter."""
        indenter = SmartIndenter(indent_size=4, use_spaces=True)
        assert indenter.indent_size == 4
        assert indenter.use_spaces is True
        assert indenter.indent_char == " "

    def test_create_with_tabs(self):
        """Test creating indenter with tabs."""
        indenter = SmartIndenter(indent_size=1, use_spaces=False)
        assert indenter.use_spaces is False
        assert indenter.indent_char == "\t"


class TestIndentDetection:
    """Test indent detection."""

    def test_detect_indent_size_4(self):
        """Test detecting 4-space indentation."""
        code = "line\n    indented\n        double"
        indenter = SmartIndenter()
        size = indenter.detect_indent_size(code)
        assert size == 4

    def test_detect_indent_size_2(self):
        """Test detecting 2-space indentation."""
        code = "line\n  indented\n    double"
        indenter = SmartIndenter()
        size = indenter.detect_indent_size(code)
        assert size == 2

    def test_detect_indent_style_spaces(self):
        """Test detecting space indentation."""
        code = "line\n    indented"
        indenter = SmartIndenter()
        style = indenter.detect_indent_style(code)
        assert style == "spaces"

    def test_detect_indent_style_tabs(self):
        """Test detecting tab indentation."""
        code = "line\n\tindented"
        indenter = SmartIndenter()
        style = indenter.detect_indent_style(code)
        assert style == "tabs"

    def test_detect_indent_style_mixed(self):
        """Test detecting mixed indentation."""
        code = "line\n    spaces\n\ttabs"
        indenter = SmartIndenter()
        style = indenter.detect_indent_style(code)
        assert style == "mixed"


class TestLineIndent:
    """Test line indentation analysis."""

    def test_get_line_indent_spaces(self):
        """Test getting indentation from line."""
        indenter = SmartIndenter()
        indent = indenter.get_line_indent("    hello")
        assert indent == "    "

    def test_get_line_indent_tabs(self):
        """Test getting tab indentation."""
        indenter = SmartIndenter()
        indent = indenter.get_line_indent("\t\thello")
        assert indent == "\t\t"

    def test_get_line_indent_none(self):
        """Test line with no indentation."""
        indenter = SmartIndenter()
        indent = indenter.get_line_indent("hello")
        assert indent == ""

    def test_get_indent_level(self):
        """Test getting indent level."""
        indenter = SmartIndenter(indent_size=4)
        level = indenter.get_indent_level("    hello")
        assert level == 1

    def test_get_indent_level_multiple(self):
        """Test indent level with multiple indents."""
        indenter = SmartIndenter(indent_size=4)
        level = indenter.get_indent_level("        hello")
        assert level == 2


class TestIndentOperations:
    """Test indent operations."""

    def test_increase_indent(self):
        """Test increasing indentation."""
        indenter = SmartIndenter(indent_size=4)
        result = indenter.increase_indent("hello")
        assert result == "    hello"

    def test_increase_indent_already_indented(self):
        """Test increasing already indented line."""
        indenter = SmartIndenter(indent_size=4)
        result = indenter.increase_indent("    hello")
        assert result == "        hello"

    def test_decrease_indent(self):
        """Test decreasing indentation."""
        indenter = SmartIndenter(indent_size=4)
        result = indenter.decrease_indent("    hello")
        assert result == "hello"

    def test_decrease_indent_no_indent(self):
        """Test decreasing line with no indentation."""
        indenter = SmartIndenter(indent_size=4)
        result = indenter.decrease_indent("hello")
        assert result == "hello"


class TestAutoIndent:
    """Test automatic indentation."""

    def test_auto_indent_first_line(self):
        """Test auto indent for first line."""
        indenter = SmartIndenter()
        result = indenter.auto_indent("", 0)
        assert result == ""

    def test_auto_indent_simple(self):
        """Test basic auto indentation."""
        code = "if True:"
        indenter = SmartIndenter(indent_size=4)
        result = indenter.auto_indent(code, 1)
        assert result == "    "

    def test_auto_indent_bracket(self):
        """Test auto indent after opening bracket."""
        code = "items = ["
        indenter = SmartIndenter(indent_size=4)
        result = indenter.auto_indent(code, 1)
        assert result == "    "

    def test_auto_indent_nested(self):
        """Test nested auto indentation."""
        code = "if True:\n    if inner:"
        indenter = SmartIndenter(indent_size=4)
        result = indenter.auto_indent(code, 2)
        assert result == "        "

    def test_auto_indent_preserve_previous(self):
        """Test preserving indentation from previous line."""
        code = "    code\n    more"
        indenter = SmartIndenter(indent_size=4)
        result = indenter.auto_indent(code, 2)
        assert result == "    "


class TestBracketHandling:
    """Test bracket detection and matching."""

    def test_close_bracket_after_open(self):
        """Test bracket closure detection."""
        indenter = SmartIndenter()
        should_close, closing = indenter.close_bracket("(", 1)
        assert should_close is True
        assert closing == ")"

    def test_close_bracket_square(self):
        """Test square bracket closure."""
        indenter = SmartIndenter()
        should_close, closing = indenter.close_bracket("[", 1)
        assert should_close is True
        assert closing == "]"

    def test_close_bracket_curly(self):
        """Test curly bracket closure."""
        indenter = SmartIndenter()
        should_close, closing = indenter.close_bracket("{", 1)
        assert should_close is True
        assert closing == "}"

    def test_close_bracket_no_bracket(self):
        """Test no bracket closure needed."""
        indenter = SmartIndenter()
        should_close, closing = indenter.close_bracket("a", 1)
        assert should_close is False
        assert closing is None

    def test_find_matching_bracket(self):
        """Test finding matching bracket."""
        indenter = SmartIndenter()
        text = "(hello world)"
        pos = indenter.find_matching_bracket(text, 0, "(")
        assert pos == 12

    def test_find_matching_bracket_nested(self):
        """Test finding matching bracket with nesting."""
        indenter = SmartIndenter()
        text = "(hello (world))"
        pos = indenter.find_matching_bracket(text, 0, "(")
        assert pos == 14

    def test_find_matching_bracket_not_found(self):
        """Test when no matching bracket exists."""
        indenter = SmartIndenter()
        text = "(hello"
        pos = indenter.find_matching_bracket(text, 0, "(")
        assert pos is None

    def test_get_bracket_completion(self):
        """Test getting bracket completion."""
        indenter = SmartIndenter()
        assert indenter.get_bracket_completion("(") == ")"
        assert indenter.get_bracket_completion("[") == "]"
        assert indenter.get_bracket_completion("{") == "}"
        assert indenter.get_bracket_completion("a") is None


class TestNormalization:
    """Test indentation normalization."""

    def test_normalize_indent_spaces_to_spaces(self):
        """Test normalizing spaces to spaces."""
        code = "line\n  indented\n    double"
        indenter = SmartIndenter(indent_size=4)
        result = indenter.normalize_indent(code, target_indent_size=4, use_spaces=True)
        assert "line" in result
        assert result.count("    ") >= 1

    def test_normalize_indent_spaces_to_tabs(self):
        """Test normalizing spaces to tabs."""
        code = "line\n    indented"
        indenter = SmartIndenter()
        result = indenter.normalize_indent(code, target_indent_size=1, use_spaces=False)
        assert "\t" in result

    def test_normalize_indent_tabs_to_spaces(self):
        """Test normalizing tabs to spaces."""
        code = "line\n\tindented"
        indenter = SmartIndenter()
        result = indenter.normalize_indent(code, target_indent_size=4, use_spaces=True)
        assert "    " in result


class TestSelectionIndent:
    """Test indenting selections."""

    def test_indent_selection_increase(self):
        """Test increasing indentation of selection."""
        text = "line1\nline2\nline3"
        indenter = SmartIndenter(indent_size=4)
        result = indenter.indent_selection(text, increase=True)
        lines = result.split("\n")
        assert all(line.startswith("    ") for line in lines)

    def test_indent_selection_decrease(self):
        """Test decreasing indentation of selection."""
        text = "    line1\n    line2"
        indenter = SmartIndenter(indent_size=4)
        result = indenter.indent_selection(text, increase=False)
        lines = result.split("\n")
        assert lines[0] == "line1"
        assert lines[1] == "line2"


class TestDocstring:
    """Test docstring formatting."""

    def test_format_docstring(self):
        """Test formatting docstring."""
        docstring = '"""\nFirst line\nSecond line\n"""'
        indenter = SmartIndenter(indent_size=4)
        result = indenter.format_docstring(docstring)
        assert '"""' in result
        assert "First line" in result

    def test_format_docstring_with_indent(self):
        """Test formatting indented docstring."""
        docstring = '    """\n    First\n    Second\n    """'
        indenter = SmartIndenter(indent_size=4)
        result = indenter.format_docstring(docstring)
        lines = result.split("\n")
        assert lines[0].startswith("    ")


class TestRemoveTrailingWhitespace:
    """Test trailing whitespace removal."""

    def test_remove_trailing_whitespace(self):
        """Test removing trailing whitespace."""
        indenter = SmartIndenter()
        result = indenter.remove_trailing_whitespace("hello   ")
        assert result == "hello"

    def test_remove_trailing_whitespace_none(self):
        """Test line without trailing whitespace."""
        indenter = SmartIndenter()
        result = indenter.remove_trailing_whitespace("hello")
        assert result == "hello"
