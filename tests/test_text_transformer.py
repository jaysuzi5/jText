"""Unit tests for text transformation utilities."""

import pytest
from src.text_transformer import TextTransformer


class TestCaseConversion:
    """Test case conversion functions."""

    def test_to_uppercase(self):
        """Test converting to uppercase."""
        assert TextTransformer.to_uppercase("hello") == "HELLO"
        assert TextTransformer.to_uppercase("Hello World") == "HELLO WORLD"

    def test_to_lowercase(self):
        """Test converting to lowercase."""
        assert TextTransformer.to_lowercase("HELLO") == "hello"
        assert TextTransformer.to_lowercase("Hello World") == "hello world"

    def test_to_titlecase(self):
        """Test converting to title case."""
        assert TextTransformer.to_titlecase("hello world") == "Hello World"
        assert TextTransformer.to_titlecase("python programming") == "Python Programming"

    def test_to_camelcase_from_snake(self):
        """Test converting from snake_case to camelCase."""
        assert TextTransformer.to_camelcase("hello_world") == "helloWorld"
        assert TextTransformer.to_camelcase("my_variable_name") == "myVariableName"

    def test_to_camelcase_from_spaces(self):
        """Test converting from spaces to camelCase."""
        assert TextTransformer.to_camelcase("hello world") == "helloWorld"
        assert TextTransformer.to_camelcase("multiple word string") == "multipleWordString"

    def test_to_camelcase_with_hyphens(self):
        """Test converting from hyphens to camelCase."""
        assert TextTransformer.to_camelcase("hello-world") == "helloWorld"

    def test_to_camelcase_single_word(self):
        """Test camelCase with single word."""
        assert TextTransformer.to_camelcase("hello") == "hello"

    def test_to_snakecase_from_camel(self):
        """Test converting from camelCase to snake_case."""
        assert TextTransformer.to_snakecase("helloWorld") == "hello_world"
        assert TextTransformer.to_snakecase("myVariableName") == "my_variable_name"

    def test_to_snakecase_from_spaces(self):
        """Test converting from spaces to snake_case."""
        assert TextTransformer.to_snakecase("hello world") == "hello_world"

    def test_to_snakecase_from_hyphens(self):
        """Test converting from hyphens to snake_case."""
        assert TextTransformer.to_snakecase("hello-world") == "hello_world"

    def test_to_snakecase_multiple_separators(self):
        """Test snake_case removes multiple consecutive separators."""
        assert TextTransformer.to_snakecase("hello__world") == "hello_world"
        assert TextTransformer.to_snakecase("hello  world") == "hello_world"


class TestWhitespaceOperations:
    """Test whitespace manipulation functions."""

    def test_trim_whitespace_both(self):
        """Test trimming whitespace from both sides."""
        assert TextTransformer.trim_whitespace("  hello  ") == "hello"
        assert TextTransformer.trim_whitespace("\t\thello\t\t") == "hello"

    def test_trim_whitespace_leading(self):
        """Test trimming leading whitespace."""
        assert TextTransformer.trim_whitespace("  hello  ", "leading") == "hello  "

    def test_trim_whitespace_trailing(self):
        """Test trimming trailing whitespace."""
        assert TextTransformer.trim_whitespace("  hello  ", "trailing") == "  hello"

    def test_trim_lines_both(self):
        """Test trimming whitespace from all lines."""
        text = "  hello  \n  world  \n  test  "
        result = TextTransformer.trim_lines(text, "both")
        assert result == "hello\nworld\ntest"

    def test_trim_lines_leading(self):
        """Test trimming leading whitespace from lines."""
        text = "  hello  \n  world  "
        result = TextTransformer.trim_lines(text, "leading")
        assert result == "hello  \nworld  "

    def test_remove_trailing_whitespace(self):
        """Test removing trailing whitespace from lines."""
        text = "hello  \nworld  \ntest"
        result = TextTransformer.remove_trailing_whitespace(text)
        assert result == "hello\nworld\ntest"

    def test_remove_leading_whitespace(self):
        """Test removing leading whitespace from lines."""
        text = "  hello\n  world\ntest"
        result = TextTransformer.remove_leading_whitespace(text)
        assert result == "hello\nworld\ntest"


class TestLineOperations:
    """Test line manipulation functions."""

    def test_sort_lines_alphabetically(self):
        """Test sorting lines alphabetically."""
        text = "zebra\napple\nbanana"
        result = TextTransformer.sort_lines(text)
        assert result == "apple\nbanana\nzebra"

    def test_sort_lines_reverse(self):
        """Test sorting lines in reverse order."""
        text = "apple\nbanana\nzebra"
        result = TextTransformer.sort_lines(text, reverse=True)
        assert result == "zebra\nbanana\napple"

    def test_sort_lines_by_length(self):
        """Test sorting lines by length."""
        text = "zebra\nap\nbanana"
        result = TextTransformer.sort_lines(text, by_length=True)
        assert result == "ap\nzebra\nbanana"

    def test_sort_lines_by_length_reverse(self):
        """Test sorting lines by length in reverse."""
        text = "ap\nzebra\nbanana"
        result = TextTransformer.sort_lines(text, by_length=True, reverse=True)
        assert result == "banana\nzebra\nap"

    def test_reverse_lines(self):
        """Test reversing line order."""
        text = "line1\nline2\nline3"
        result = TextTransformer.reverse_lines(text)
        assert result == "line3\nline2\nline1"

    def test_remove_duplicate_lines(self):
        """Test removing duplicate lines."""
        text = "apple\nbanana\napple\ncherry\nbanana"
        result = TextTransformer.remove_duplicate_lines(text)
        assert result == "apple\nbanana\ncherry"

    def test_remove_duplicate_lines_preserve_order(self):
        """Test that duplicate removal preserves order."""
        text = "zebra\napple\nzebra\nbanana"
        result = TextTransformer.remove_duplicate_lines(text, preserve_order=True)
        assert result == "zebra\napple\nbanana"

    def test_remove_empty_lines(self):
        """Test removing empty lines."""
        text = "line1\n\nline2\n  \nline3"
        result = TextTransformer.remove_empty_lines(text)
        assert result == "line1\nline2\nline3"

    def test_join_lines(self):
        """Test joining lines."""
        text = "line1\nline2\nline3"
        result = TextTransformer.join_lines(text)
        assert result == "line1 line2 line3"

    def test_join_lines_custom_separator(self):
        """Test joining lines with custom separator."""
        text = "line1\nline2\nline3"
        result = TextTransformer.join_lines(text, separator=", ")
        assert result == "line1, line2, line3"

    def test_split_line_word_aware(self):
        """Test splitting line with word awareness."""
        text = "this is a long line that should be split"
        result = TextTransformer.split_line(text, length=15)
        lines = result.split("\n")
        # Each line should be <= 15 characters
        for line in lines:
            assert len(line) <= 15


class TestIndentation:
    """Test indentation functions."""

    def test_indent_lines(self):
        """Test adding indentation."""
        text = "line1\nline2\nline3"
        result = TextTransformer.indent_lines(text, indent=4)
        assert result == "    line1\n    line2\n    line3"

    def test_indent_lines_custom_char(self):
        """Test indentation with custom character."""
        text = "line1\nline2"
        result = TextTransformer.indent_lines(text, indent=2, char="\t")
        assert result == "\t\tline1\n\t\tline2"

    def test_dedent_lines(self):
        """Test removing indentation."""
        text = "    line1\n    line2\n    line3"
        result = TextTransformer.dedent_lines(text, indent=4)
        assert result == "line1\nline2\nline3"

    def test_dedent_lines_partial(self):
        """Test dedenting when not all lines are indented."""
        text = "    line1\nline2\n    line3"
        result = TextTransformer.dedent_lines(text, indent=4)
        assert result == "line1\nline2\nline3"

    def test_dedent_lines_tab_char(self):
        """Test dedenting with tab character."""
        text = "\t\tline1\n\t\tline2"
        result = TextTransformer.dedent_lines(text, indent=2, char="\t")
        assert result == "line1\nline2"


class TestTabSpaceConversion:
    """Test tab and space conversion."""

    def test_convert_tabs_to_spaces(self):
        """Test converting tabs to spaces."""
        text = "hello\tworld\ttest"
        result = TextTransformer.convert_tabs_to_spaces(text, spaces=4)
        assert result == "hello    world    test"

    def test_convert_spaces_to_tabs(self):
        """Test converting spaces to tabs."""
        text = "hello    world    test"
        result = TextTransformer.convert_spaces_to_tabs(text, spaces=4)
        assert result == "hello\tworld\ttest"

    def test_convert_tabs_to_spaces_different_count(self):
        """Test converting tabs with different space count."""
        text = "a\tb"
        result = TextTransformer.convert_tabs_to_spaces(text, spaces=2)
        assert result == "a  b"


class TestTextManipulation:
    """Test text manipulation functions."""

    def test_reverse_text(self):
        """Test reversing text."""
        assert TextTransformer.reverse_text("hello") == "olleh"
        assert TextTransformer.reverse_text("12345") == "54321"

    def test_count_words(self):
        """Test counting words."""
        assert TextTransformer.count_words("hello world test") == 3
        assert TextTransformer.count_words("single") == 1
        assert TextTransformer.count_words("") == 0

    def test_count_lines(self):
        """Test counting lines."""
        assert TextTransformer.count_lines("line1\nline2\nline3") == 3
        assert TextTransformer.count_lines("single") == 1
        assert TextTransformer.count_lines("") == 0

    def test_count_characters(self):
        """Test counting characters."""
        assert TextTransformer.count_characters("hello") == 5
        assert TextTransformer.count_characters("hello world") == 11

    def test_count_characters_exclude_whitespace(self):
        """Test counting characters excluding whitespace."""
        assert TextTransformer.count_characters("hello world", exclude_whitespace=True) == 10
        assert TextTransformer.count_characters("h e l l o", exclude_whitespace=True) == 5
        assert TextTransformer.count_characters("line1\nline2", exclude_whitespace=True) == 10


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_string_transformations(self):
        """Test transformations on empty strings."""
        assert TextTransformer.to_uppercase("") == ""
        assert TextTransformer.to_lowercase("") == ""
        assert TextTransformer.reverse_text("") == ""

    def test_single_character(self):
        """Test transformations on single characters."""
        assert TextTransformer.to_uppercase("a") == "A"
        assert TextTransformer.to_lowercase("A") == "a"
        assert TextTransformer.reverse_text("a") == "a"

    def test_whitespace_only_string(self):
        """Test operations on whitespace-only strings."""
        assert TextTransformer.trim_whitespace("   ") == ""
        assert TextTransformer.remove_empty_lines("  \n  \n  ") == ""

    def test_special_characters(self):
        """Test transformations preserve special characters."""
        text = "hello!@#$world"
        assert TextTransformer.to_uppercase(text) == "HELLO!@#$WORLD"
        assert TextTransformer.reverse_text(text) == "dlrow$#@!olleh"

    def test_unicode_characters(self):
        """Test transformations work with unicode."""
        assert TextTransformer.to_uppercase("café") == "CAFÉ"
        assert TextTransformer.count_characters("你好") == 2

    def test_very_long_text(self):
        """Test operations on large text."""
        text = "word " * 1000
        assert TextTransformer.count_words(text) == 1000
        result = TextTransformer.to_uppercase(text)
        assert all(c.isupper() or c == " " for c in result)
