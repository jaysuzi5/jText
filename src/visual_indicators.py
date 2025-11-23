"""Visual indicators for whitespace, line endings, and other editor features."""

from enum import Enum
from typing import Literal


class LineEnding(Enum):
    """Line ending types."""

    LF = "\n"  # Unix/Linux/Mac (0x0A)
    CRLF = "\r\n"  # Windows (0x0D 0x0A)
    CR = "\r"  # Old Mac (0x0D)
    AUTO = "auto"  # Auto-detect

    def display_name(self) -> str:
        """Get display name for line ending."""
        if self == LineEnding.LF:
            return "LF"
        elif self == LineEnding.CRLF:
            return "CRLF"
        elif self == LineEnding.CR:
            return "CR"
        else:
            return "Auto"


class VisualIndicatorSettings:
    """Settings for visual indicators."""

    def __init__(
        self,
        show_whitespace: bool = False,
        show_line_endings: bool = False,
        show_non_printable: bool = False,
        whitespace_char: str = "·",
        tab_char: str = "→",
        line_ending_char: str = "↵",
        space_char: str = "·",
    ):
        """Initialize visual indicator settings.

        Args:
            show_whitespace: Show whitespace characters
            show_line_endings: Show line ending characters
            show_non_printable: Show non-printable characters
            whitespace_char: Character for spaces
            tab_char: Character for tabs
            line_ending_char: Character for line endings
            space_char: Character for spaces (alternative)
        """
        self.show_whitespace = show_whitespace
        self.show_line_endings = show_line_endings
        self.show_non_printable = show_non_printable
        self.whitespace_char = whitespace_char
        self.tab_char = tab_char
        self.line_ending_char = line_ending_char
        self.space_char = space_char

    def toggle_whitespace(self) -> None:
        """Toggle whitespace visibility."""
        self.show_whitespace = not self.show_whitespace

    def toggle_line_endings(self) -> None:
        """Toggle line ending visibility."""
        self.show_line_endings = not self.show_line_endings

    def toggle_non_printable(self) -> None:
        """Toggle non-printable character visibility."""
        self.show_non_printable = not self.show_non_printable


class LineEndingDetector:
    """Detects line ending type in text."""

    @staticmethod
    def detect(text: str) -> LineEnding:
        """Detect line ending type in text.

        Args:
            text: Text to analyze

        Returns:
            Detected line ending type
        """
        if not text:
            return LineEnding.LF

        # Check for Windows line endings first (CRLF)
        if "\r\n" in text:
            return LineEnding.CRLF
        # Check for old Mac line endings
        elif "\r" in text:
            return LineEnding.CR
        # Check for Unix line endings
        elif "\n" in text:
            return LineEnding.LF
        else:
            return LineEnding.LF

    @staticmethod
    def get_line_ending_char(ending: LineEnding) -> str:
        """Get the character(s) for a line ending.

        Args:
            ending: Line ending type

        Returns:
            Character representation
        """
        if ending == LineEnding.CRLF:
            return "\r\n"
        elif ending == LineEnding.CR:
            return "\r"
        else:
            return "\n"

    @staticmethod
    def convert_line_endings(text: str, from_ending: LineEnding, to_ending: LineEnding) -> str:
        """Convert line endings in text.

        Args:
            text: Text to convert
            from_ending: Current line ending type
            to_ending: Target line ending type

        Returns:
            Text with converted line endings
        """
        if from_ending == to_ending:
            return text

        # First normalize to LF
        if from_ending == LineEnding.CRLF:
            normalized = text.replace("\r\n", "\n")
        elif from_ending == LineEnding.CR:
            normalized = text.replace("\r", "\n")
        else:
            normalized = text

        # Then convert to target ending
        if to_ending == LineEnding.CRLF:
            return normalized.replace("\n", "\r\n")
        elif to_ending == LineEnding.CR:
            return normalized.replace("\n", "\r")
        else:
            return normalized


class WhitespaceAnalyzer:
    """Analyzes whitespace usage in text."""

    @staticmethod
    def count_lines_with_tabs(text: str) -> int:
        """Count lines that contain tabs.

        Args:
            text: Text to analyze

        Returns:
            Number of lines with tabs
        """
        if not text:
            return 0
        return sum(1 for line in text.split("\n") if "\t" in line)

    @staticmethod
    def count_lines_with_spaces(text: str, min_spaces: int = 2) -> int:
        """Count lines that use spaces for indentation.

        Args:
            text: Text to analyze
            min_spaces: Minimum consecutive spaces to count

        Returns:
            Number of lines with space indentation
        """
        if not text:
            return 0

        count = 0
        for line in text.split("\n"):
            # Check if line starts with spaces
            stripped = line.lstrip()
            if stripped and line.startswith(" " * min_spaces):
                count += 1
        return count

    @staticmethod
    def get_indentation_style(text: str) -> Literal["tabs", "spaces", "mixed", "none"]:
        """Detect the primary indentation style.

        Args:
            text: Text to analyze

        Returns:
            'tabs', 'spaces', 'mixed', or 'none'
        """
        if not text:
            return "none"

        tabs_lines = WhitespaceAnalyzer.count_lines_with_tabs(text)
        spaces_lines = WhitespaceAnalyzer.count_lines_with_spaces(text)

        if tabs_lines == 0 and spaces_lines == 0:
            return "none"
        elif tabs_lines > 0 and spaces_lines > 0:
            return "mixed"
        elif tabs_lines > spaces_lines:
            return "tabs"
        else:
            return "spaces"

    @staticmethod
    def get_indent_size(text: str) -> int:
        """Detect the most common indentation size (for spaces).

        Args:
            text: Text to analyze

        Returns:
            Detected indent size (2, 4, or 8)
        """
        if not text:
            return 4

        indent_counts = {}
        for line in text.split("\n"):
            if not line or not line[0].isspace():
                continue

            # Count leading spaces
            spaces = len(line) - len(line.lstrip(" "))
            if spaces > 0 and line[spaces] != "\t":
                indent_counts[spaces] = indent_counts.get(spaces, 0) + 1

        if not indent_counts:
            return 4

        # Find most common indent
        most_common = max(indent_counts.items(), key=lambda x: x[1])[0]

        # Normalize to common indents
        if most_common <= 2:
            return 2
        elif most_common <= 4:
            return 4
        else:
            return 8


class VisualIndicatorRenderer:
    """Renders visual indicators for text."""

    @staticmethod
    def render_whitespace(text: str, settings: VisualIndicatorSettings) -> str:
        """Render whitespace characters in text.

        Args:
            text: Text to process
            settings: Visual indicator settings

        Returns:
            Text with visual indicators (for display purposes)
        """
        if not settings.show_whitespace:
            return text

        # Replace tabs with tab character + indicator
        result = text.replace("\t", settings.tab_char)
        # Replace spaces with space character indicator
        result = result.replace(" ", settings.space_char)

        return result

    @staticmethod
    def render_line_endings(text: str, settings: VisualIndicatorSettings) -> str:
        """Render line ending characters.

        Args:
            text: Text to process
            settings: Visual indicator settings

        Returns:
            Text with line ending indicators
        """
        if not settings.show_line_endings:
            return text

        # Replace line endings with visible character
        result = text.replace("\r\n", settings.line_ending_char)
        result = result.replace("\r", settings.line_ending_char)
        result = result.replace("\n", settings.line_ending_char)

        return result
