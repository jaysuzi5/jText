"""Smart indentation utilities for automatic indenting and bracket completion."""

import re
from typing import Tuple, Optional, Literal


class SmartIndenter:
    """Provides smart indentation features."""

    # Opening brackets that typically increase indentation
    OPENING_BRACKETS = {"(", "[", "{"}
    # Closing brackets
    CLOSING_BRACKETS = {")", "]", "}"}
    # Matching bracket pairs
    BRACKET_PAIRS = {"(": ")", "[": "]", "{": "}"}
    REVERSE_PAIRS = {")": "(", "]": "[", "}": "{"}

    # Keywords that trigger indentation increase
    INDENT_KEYWORDS = {
        "if", "elif", "else", "for", "while", "with", "try", "except",
        "finally", "def", "class", "case", "switch", "do"
    }

    # Keywords that typically should be dedented
    DEDENT_KEYWORDS = {"else", "elif", "except", "finally", "case"}

    def __init__(self, indent_size: int = 4, use_spaces: bool = True):
        """Initialize smart indenter.

        Args:
            indent_size: Number of spaces per indent level
            use_spaces: Use spaces (True) or tabs (False)
        """
        self.indent_size = indent_size
        self.use_spaces = use_spaces
        self.indent_char = " " if use_spaces else "\t"
        self.indent_string = self.indent_char * indent_size if use_spaces else self.indent_char

    def detect_indent_size(self, text: str) -> int:
        """Detect the indentation size used in text.

        Args:
            text: The text to analyze

        Returns:
            Detected indent size (2, 4, or 8)
        """
        lines = text.split("\n")
        indents = []

        for line in lines:
            if not line.strip():
                continue
            # Count leading spaces
            spaces = len(line) - len(line.lstrip(" "))
            if spaces > 0:
                indents.append(spaces)

        if not indents:
            return self.indent_size

        # Find greatest common divisor of all indents
        # Most common indent differences indicate size
        from math import gcd
        from functools import reduce

        if len(indents) == 1:
            return indents[0] if indents[0] in [2, 4, 8] else self.indent_size

        result = reduce(gcd, indents)
        return result if result in [2, 4, 8] else self.indent_size

    def detect_indent_style(self, text: str) -> Literal["spaces", "tabs", "mixed"]:
        """Detect whether text uses tabs or spaces for indentation.

        Args:
            text: The text to analyze

        Returns:
            'spaces', 'tabs', or 'mixed'
        """
        lines = text.split("\n")
        has_tabs = False
        has_spaces = False

        for line in lines:
            if line.startswith("\t"):
                has_tabs = True
            elif line.startswith(" "):
                has_spaces = True

        if has_tabs and has_spaces:
            return "mixed"
        elif has_tabs:
            return "tabs"
        else:
            return "spaces"

    def get_line_indent(self, line: str) -> str:
        """Get the indentation string of a line.

        Args:
            line: The line to analyze

        Returns:
            The indentation string (spaces or tabs)
        """
        return line[: len(line) - len(line.lstrip())]

    def get_indent_level(self, line: str) -> int:
        """Get the indentation level of a line.

        Args:
            line: The line to analyze

        Returns:
            The indentation level (number of indent units)
        """
        indent = self.get_line_indent(line)
        if not indent:
            return 0

        if "\t" in indent:
            return indent.count("\t")
        else:
            return len(indent) // self.indent_size

    def increase_indent(self, line: str) -> str:
        """Increase indentation of a line by one level.

        Args:
            line: The line to indent

        Returns:
            Line with increased indentation
        """
        return self.indent_string + line

    def decrease_indent(self, line: str) -> str:
        """Decrease indentation of a line by one level.

        Args:
            line: The line to dedent

        Returns:
            Line with decreased indentation
        """
        indent = self.get_line_indent(line)
        content = line[len(indent) :]

        if not indent:
            return line

        # Remove one indent level
        if self.use_spaces:
            if indent.endswith(self.indent_string):
                return indent[: -self.indent_size] + content
        else:
            if indent.endswith(self.indent_char):
                return indent[:-1] + content

        return line

    def auto_indent(self, text: str, line_num: int) -> str:
        """Calculate the appropriate indentation for a new line.

        Args:
            text: The full text
            line_num: The line number of the new line (0-indexed)

        Returns:
            The appropriate indentation string
        """
        lines = text.split("\n")

        if line_num == 0:
            return ""

        # Look at previous non-empty line
        prev_line = ""
        prev_indent = ""
        for i in range(line_num - 1, -1, -1):
            if i < len(lines) and lines[i].strip():
                prev_line = lines[i]
                prev_indent = self.get_line_indent(prev_line)
                break

        if not prev_line:
            return ""

        # Check if previous line ends with opening bracket
        stripped = prev_line.rstrip()
        if stripped and stripped[-1] in self.OPENING_BRACKETS:
            return prev_indent + self.indent_string

        # Check if previous line has a keyword that triggers indentation
        for keyword in self.INDENT_KEYWORDS:
            if re.search(rf"\b{keyword}\b", prev_line) and prev_line.rstrip().endswith(":"):
                return prev_indent + self.indent_string

        # Check if current line would be dedented (else, elif, except, etc.)
        current_line = lines[line_num] if line_num < len(lines) else ""
        for keyword in self.DEDENT_KEYWORDS:
            if re.search(rf"^\s*{keyword}\b", current_line):
                # Reduce indent level if applicable
                level = self.get_indent_level(prev_indent)
                if level > 0:
                    return self.indent_string * (level - 1)

        return prev_indent

    def close_bracket(self, line: str, position: int) -> Tuple[bool, Optional[str]]:
        """Check if a bracket can be automatically closed.

        Args:
            line: The current line
            position: The cursor position in the line

        Returns:
            Tuple of (should_close, closing_char)
        """
        if position == 0 or position > len(line):
            return False, None

        # Check the character before cursor
        char = line[position - 1] if position <= len(line) else None

        if char in self.OPENING_BRACKETS:
            return True, self.BRACKET_PAIRS[char]

        return False, None

    def find_matching_bracket(self, text: str, start_pos: int, opening: str) -> Optional[int]:
        """Find the matching closing bracket.

        Args:
            text: The full text
            start_pos: Position of opening bracket
            opening: The opening bracket character

        Returns:
            Position of matching closing bracket, or None
        """
        closing = self.BRACKET_PAIRS[opening]
        level = 0
        pos = start_pos

        while pos < len(text):
            char = text[pos]
            if char == opening:
                level += 1
            elif char == closing:
                level -= 1
                if level == 0:
                    return pos

            pos += 1

        return None

    def get_bracket_completion(self, char: str) -> Optional[str]:
        """Get the completion character for a bracket.

        Args:
            char: The opening bracket

        Returns:
            The closing bracket, or None
        """
        return self.BRACKET_PAIRS.get(char)

    def remove_trailing_whitespace(self, line: str) -> str:
        """Remove trailing whitespace from line.

        Args:
            line: The line to clean

        Returns:
            Line without trailing whitespace
        """
        return line.rstrip()

    def normalize_indent(self, text: str, target_indent_size: int = 4, use_spaces: bool = True) -> str:
        """Normalize indentation throughout text.

        Args:
            text: The text to normalize
            target_indent_size: Target spaces per indent level
            use_spaces: Use spaces (True) or tabs (False)

        Returns:
            Text with normalized indentation
        """
        lines = text.split("\n")
        target_char = " " if use_spaces else "\t"
        target_string = target_char * target_indent_size if use_spaces else target_char

        result = []
        for line in lines:
            if not line.strip():
                result.append("")
                continue

            # Get current indentation level
            level = self.get_indent_level(line)
            content = line.lstrip()

            # Apply new indentation
            new_indent = target_string * level
            result.append(new_indent + content)

        return "\n".join(result)

    def indent_selection(self, text: str, increase: bool = True) -> str:
        """Indent or dedent multiple lines.

        Args:
            text: The selected text (may be multiple lines)
            increase: Increase (True) or decrease (False) indentation

        Returns:
            Text with adjusted indentation
        """
        lines = text.split("\n")
        result = []

        for line in lines:
            if increase:
                result.append(self.increase_indent(line))
            else:
                result.append(self.decrease_indent(line))

        return "\n".join(result)

    def format_docstring(self, text: str) -> str:
        """Format a docstring with proper indentation.

        Args:
            text: The docstring text

        Returns:
            Formatted docstring
        """
        lines = text.split("\n")
        if not lines:
            return text

        # Get base indentation from first line
        base_indent = self.get_line_indent(lines[0]) if lines[0].strip() else ""

        result = []
        for i, line in enumerate(lines):
            if i == 0:
                result.append(line)
            elif not line.strip():
                result.append("")
            else:
                # Ensure consistent indentation
                stripped = line.lstrip()
                result.append(base_indent + stripped)

        return "\n".join(result)
