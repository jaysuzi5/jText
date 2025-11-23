"""Text transformation utilities for case conversion, line operations, and formatting."""

import re
from typing import List, Literal


class TextTransformer:
    """Provides text transformation operations for editing."""

    @staticmethod
    def to_uppercase(text: str) -> str:
        """Convert text to uppercase.

        Args:
            text: Text to convert

        Returns:
            Text in uppercase
        """
        return text.upper()

    @staticmethod
    def to_lowercase(text: str) -> str:
        """Convert text to lowercase.

        Args:
            text: Text to convert

        Returns:
            Text in lowercase
        """
        return text.lower()

    @staticmethod
    def to_titlecase(text: str) -> str:
        """Convert text to title case (first letter of each word capitalized).

        Args:
            text: Text to convert

        Returns:
            Text in title case
        """
        return text.title()

    @staticmethod
    def to_camelcase(text: str) -> str:
        """Convert text to camelCase.

        Args:
            text: Text to convert (typically snake_case or spaces)

        Returns:
            Text in camelCase
        """
        # Split by underscores, spaces, or hyphens
        words = re.split(r"[_\s-]+", text.strip())
        if not words:
            return text

        # First word lowercase, rest capitalized
        return words[0].lower() + "".join(word.capitalize() for word in words[1:])

    @staticmethod
    def to_snakecase(text: str) -> str:
        """Convert text to snake_case.

        Args:
            text: Text to convert (typically camelCase or spaces)

        Returns:
            Text in snake_case
        """
        # Insert underscore before uppercase letters (for camelCase)
        text = re.sub(r"(?<!^)(?=[A-Z])", "_", text)
        # Replace spaces and hyphens with underscores
        text = re.sub(r"[\s-]+", "_", text)
        # Remove extra underscores and convert to lowercase
        text = re.sub(r"_+", "_", text)
        return text.lower().strip("_")

    @staticmethod
    def trim_whitespace(text: str, mode: Literal["leading", "trailing", "both"] = "both") -> str:
        """Trim whitespace from text.

        Args:
            text: Text to trim
            mode: Where to trim ('leading', 'trailing', or 'both')

        Returns:
            Trimmed text
        """
        if mode == "leading":
            return text.lstrip()
        elif mode == "trailing":
            return text.rstrip()
        else:
            return text.strip()

    @staticmethod
    def trim_lines(text: str, mode: Literal["leading", "trailing", "both"] = "both") -> str:
        """Trim whitespace from each line in text.

        Args:
            text: Text with multiple lines
            mode: Where to trim each line

        Returns:
            Text with trimmed lines
        """
        lines = text.split("\n")
        trimmed_lines = [TextTransformer.trim_whitespace(line, mode) for line in lines]
        return "\n".join(trimmed_lines)

    @staticmethod
    def sort_lines(text: str, reverse: bool = False, by_length: bool = False) -> str:
        """Sort lines in text.

        Args:
            text: Text with multiple lines
            reverse: Sort in reverse order
            by_length: Sort by line length instead of alphabetically

        Returns:
            Text with sorted lines
        """
        lines = text.split("\n")

        if by_length:
            lines.sort(key=len, reverse=reverse)
        else:
            lines.sort(reverse=reverse)

        return "\n".join(lines)

    @staticmethod
    def reverse_lines(text: str) -> str:
        """Reverse the order of lines.

        Args:
            text: Text with multiple lines

        Returns:
            Text with reversed line order
        """
        lines = text.split("\n")
        return "\n".join(reversed(lines))

    @staticmethod
    def remove_duplicate_lines(text: str, preserve_order: bool = True) -> str:
        """Remove duplicate lines while preserving first occurrence.

        Args:
            text: Text with multiple lines
            preserve_order: Keep original order of first occurrences

        Returns:
            Text with duplicates removed
        """
        lines = text.split("\n")

        if preserve_order:
            seen = set()
            unique_lines = []
            for line in lines:
                if line not in seen:
                    seen.add(line)
                    unique_lines.append(line)
            return "\n".join(unique_lines)
        else:
            return "\n".join(sorted(set(lines)))

    @staticmethod
    def remove_empty_lines(text: str) -> str:
        """Remove empty lines from text.

        Args:
            text: Text with multiple lines

        Returns:
            Text without empty lines
        """
        lines = text.split("\n")
        return "\n".join(line for line in lines if line.strip())

    @staticmethod
    def indent_lines(text: str, indent: int = 4, char: str = " ") -> str:
        """Add indentation to all lines.

        Args:
            text: Text with multiple lines
            indent: Number of indent characters to add
            char: Character to use for indentation (space or tab)

        Returns:
            Text with added indentation
        """
        indent_str = char * indent
        lines = text.split("\n")
        return "\n".join(indent_str + line for line in lines)

    @staticmethod
    def dedent_lines(text: str, indent: int = 4, char: str = " ") -> str:
        """Remove indentation from all lines.

        Args:
            text: Text with multiple lines
            indent: Number of indent characters to remove
            char: Character used for indentation (space or tab)

        Returns:
            Text with removed indentation
        """
        indent_str = char * indent
        lines = text.split("\n")
        result = []

        for line in lines:
            if line.startswith(indent_str):
                result.append(line[indent:])
            elif line.strip():  # Non-empty line that doesn't start with indent
                result.append(line)
            else:  # Empty or whitespace-only line
                result.append(line.lstrip())

        return "\n".join(result)

    @staticmethod
    def reverse_text(text: str) -> str:
        """Reverse the characters in text.

        Args:
            text: Text to reverse

        Returns:
            Reversed text
        """
        return text[::-1]

    @staticmethod
    def join_lines(text: str, separator: str = " ") -> str:
        """Join multiple lines into a single line.

        Args:
            text: Text with multiple lines
            separator: String to join lines with

        Returns:
            Single-line text
        """
        lines = text.split("\n")
        return separator.join(line.strip() for line in lines if line.strip())

    @staticmethod
    def split_line(text: str, length: int = 80, separator: str = "\n") -> str:
        """Split text into lines of maximum length (word-aware).

        Args:
            text: Text to split
            length: Maximum line length
            separator: Line separator to use

        Returns:
            Text split into lines
        """
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if not current_line:
                current_line = word
            elif len(current_line) + 1 + len(word) <= length:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return separator.join(lines)

    @staticmethod
    def convert_tabs_to_spaces(text: str, spaces: int = 4) -> str:
        """Convert tabs to spaces.

        Args:
            text: Text containing tabs
            spaces: Number of spaces per tab

        Returns:
            Text with tabs converted to spaces
        """
        return text.replace("\t", " " * spaces)

    @staticmethod
    def convert_spaces_to_tabs(text: str, spaces: int = 4) -> str:
        """Convert spaces to tabs.

        Args:
            text: Text containing spaces
            spaces: Number of consecutive spaces that equal one tab

        Returns:
            Text with spaces converted to tabs
        """
        return text.replace(" " * spaces, "\t")

    @staticmethod
    def remove_trailing_whitespace(text: str) -> str:
        """Remove trailing whitespace from each line.

        Args:
            text: Text with multiple lines

        Returns:
            Text with trailing whitespace removed
        """
        lines = text.split("\n")
        return "\n".join(line.rstrip() for line in lines)

    @staticmethod
    def remove_leading_whitespace(text: str) -> str:
        """Remove leading whitespace from each line.

        Args:
            text: Text with multiple lines

        Returns:
            Text with leading whitespace removed
        """
        lines = text.split("\n")
        return "\n".join(line.lstrip() for line in lines)

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text.

        Args:
            text: Text to count

        Returns:
            Number of words
        """
        return len(text.split())

    @staticmethod
    def count_lines(text: str) -> int:
        """Count lines in text.

        Args:
            text: Text to count

        Returns:
            Number of lines
        """
        if not text:
            return 0
        return len(text.split("\n"))

    @staticmethod
    def count_characters(text: str, exclude_whitespace: bool = False) -> int:
        """Count characters in text.

        Args:
            text: Text to count
            exclude_whitespace: Exclude spaces and newlines from count

        Returns:
            Number of characters
        """
        if exclude_whitespace:
            return len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
        return len(text)
