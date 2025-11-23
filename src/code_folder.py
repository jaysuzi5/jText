"""Code folding support for detecting and managing foldable code regions."""

import re
from typing import List, Optional, Tuple, Literal
from dataclasses import dataclass


@dataclass
class FoldRegion:
    """Represents a foldable code region."""

    start_line: int
    end_line: int
    level: int
    region_type: Literal["function", "class", "block", "indent", "comment"]
    is_folded: bool = False

    @property
    def line_count(self) -> int:
        """Get the number of lines in this region."""
        return self.end_line - self.start_line + 1

    def contains_line(self, line_num: int) -> bool:
        """Check if a line is within this region.

        Args:
            line_num: The line number to check

        Returns:
            True if line is within region
        """
        return self.start_line <= line_num <= self.end_line

    def overlaps_with(self, other: "FoldRegion") -> bool:
        """Check if this region overlaps with another.

        Args:
            other: Another FoldRegion

        Returns:
            True if regions overlap
        """
        return not (self.end_line < other.start_line or self.start_line > other.end_line)


class CodeFolder:
    """Detects and manages foldable code regions."""

    # Pattern for function definitions (Python, JavaScript, Java, etc.)
    FUNCTION_PATTERN = re.compile(r"^\s*(def|function|func|void|int|double|string|async\s+function)\s+\w+\s*\(")
    # Pattern for class definitions
    CLASS_PATTERN = re.compile(r"^\s*(class|interface|struct)\s+\w+")
    # Pattern for block starts (if, for, while, try, etc.) - matches with optional parentheses or colon
    BLOCK_PATTERN = re.compile(r"^\s*(if|for|while|try|catch|finally|switch|else\s+if|else)[\s\(:]")
    # Pattern for comment blocks
    COMMENT_PATTERN = re.compile(r"^\s*#|^\s*//|^\s*/\*")

    def __init__(self):
        """Initialize the code folder."""
        self.regions: List[FoldRegion] = []
        self._indentation_levels: List[int] = []

    def analyze(self, text: str, language: str = "auto") -> List[FoldRegion]:
        """Analyze text and detect foldable regions.

        Args:
            text: The code text to analyze
            language: Programming language ("python", "javascript", "auto", etc.)

        Returns:
            List of detected fold regions
        """
        self.regions = []
        self._indentation_levels = []

        if not text:
            return self.regions

        lines = text.split("\n")

        # Detect syntax-based regions (functions, classes, blocks)
        self._detect_syntax_regions(lines)

        # Detect indentation-based regions
        self._detect_indent_regions(lines)

        # Sort regions by start line
        self.regions.sort(key=lambda r: (r.start_line, -r.level))

        return self.regions

    def _detect_syntax_regions(self, lines: List[str]) -> None:
        """Detect function, class, and block regions.

        Args:
            lines: List of code lines
        """
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for class definition
            if self.CLASS_PATTERN.search(line):
                end_line = self._find_block_end(lines, i)
                if end_line > i:
                    self.regions.append(
                        FoldRegion(
                            start_line=i,
                            end_line=end_line,
                            level=0,
                            region_type="class",
                        )
                    )
                    # Don't skip, continue to detect nested functions
                    i += 1
                    continue

            # Check for function definition
            if self.FUNCTION_PATTERN.search(line):
                end_line = self._find_block_end(lines, i)
                if end_line > i:
                    # Determine level based on indentation
                    indent = len(line) - len(line.lstrip())
                    level = 1 if indent == 0 else 2
                    self.regions.append(
                        FoldRegion(
                            start_line=i,
                            end_line=end_line,
                            level=level,
                            region_type="function",
                        )
                    )
                    # Don't skip, continue to detect nested functions
                    i += 1
                    continue

            # Check for block statements
            if self.BLOCK_PATTERN.search(line):
                end_line = self._find_block_end(lines, i)
                if end_line > i:
                    self.regions.append(
                        FoldRegion(
                            start_line=i,
                            end_line=end_line,
                            level=2,
                            region_type="block",
                        )
                    )
                    i += 1
                    continue

            # Check for comment blocks
            if self.COMMENT_PATTERN.search(line):
                end_line = self._find_comment_end(lines, i)
                if end_line > i:
                    self.regions.append(
                        FoldRegion(
                            start_line=i,
                            end_line=end_line,
                            level=3,
                            region_type="comment",
                        )
                    )
                    i = end_line
                    continue

            i += 1

    def _detect_indent_regions(self, lines: List[str]) -> None:
        """Detect indentation-based folding regions.

        Args:
            lines: List of code lines
        """
        indent_stack: List[Tuple[int, int, int]] = []  # (indent_level, start_line, level)

        for i, line in enumerate(lines):
            if not line.strip():  # Skip empty lines
                continue

            # Get indentation level
            indent = len(line) - len(line.lstrip())

            # Pop from stack if this line has less indentation
            while indent_stack and indent_stack[-1][0] >= indent:
                prev_indent, start_line, level = indent_stack.pop()
                if i - start_line > 1:  # Only fold if more than 1 line
                    self.regions.append(
                        FoldRegion(
                            start_line=start_line,
                            end_line=i - 1,
                            level=level,
                            region_type="indent",
                        )
                    )

            # Push current indentation
            if line.strip():
                indent_stack.append((indent, i, 4 + (indent // 4)))

    def _find_block_end(self, lines: List[str], start: int) -> int:
        """Find the end line of a code block starting at given line.

        Args:
            lines: List of code lines
            start: Starting line index

        Returns:
            Index of the last line of the block
        """
        if start >= len(lines):
            return start

        start_indent = len(lines[start]) - len(lines[start].lstrip())

        # Find the next line with same or less indentation (but not empty)
        for i in range(start + 1, len(lines)):
            line = lines[i]
            if not line.strip():  # Skip empty lines
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= start_indent:
                return i - 1

        return len(lines) - 1

    def _find_comment_end(self, lines: List[str], start: int) -> int:
        """Find the end of a comment block.

        Args:
            lines: List of code lines
            start: Starting line index

        Returns:
            Index of the last line of the comment
        """
        if start >= len(lines):
            return start

        # Find next non-comment line
        for i in range(start + 1, len(lines)):
            if not self.COMMENT_PATTERN.search(lines[i]):
                return i - 1

        return len(lines) - 1

    def get_regions_at_line(self, line_num: int) -> List[FoldRegion]:
        """Get all regions that contain a specific line.

        Args:
            line_num: The line number (0-indexed)

        Returns:
            List of regions containing the line
        """
        return [r for r in self.regions if r.contains_line(line_num)]

    def get_top_level_regions(self) -> List[FoldRegion]:
        """Get only top-level regions (level 0).

        Returns:
            List of top-level regions
        """
        return [r for r in self.regions if r.level == 0]

    def get_nested_regions(self, parent: FoldRegion) -> List[FoldRegion]:
        """Get regions nested within a parent region.

        Args:
            parent: The parent region

        Returns:
            List of nested regions
        """
        return [
            r
            for r in self.regions
            if r.start_line > parent.start_line and r.end_line < parent.end_line and r.level > parent.level
        ]

    def toggle_fold(self, region: FoldRegion) -> None:
        """Toggle fold state of a region.

        Args:
            region: The region to toggle
        """
        region.is_folded = not region.is_folded

    def get_folded_regions(self) -> List[FoldRegion]:
        """Get all currently folded regions.

        Returns:
            List of folded regions
        """
        return [r for r in self.regions if r.is_folded]

    def fold_all(self) -> None:
        """Fold all regions."""
        for region in self.regions:
            region.is_folded = True

    def unfold_all(self) -> None:
        """Unfold all regions."""
        for region in self.regions:
            region.is_folded = False

    def fold_level(self, level: int) -> None:
        """Fold all regions at or above a specific level.

        Args:
            level: The nesting level to fold
        """
        for region in self.regions:
            region.is_folded = region.level <= level

    def unfold_level(self, level: int) -> None:
        """Unfold all regions at or above a specific level.

        Args:
            level: The nesting level to unfold
        """
        for region in self.regions:
            if region.level <= level:
                region.is_folded = False

    def get_visible_lines(self, text: str) -> List[int]:
        """Get list of line numbers that should be visible (not folded).

        Args:
            text: The original text

        Returns:
            List of visible line numbers (0-indexed)
        """
        total_lines = len(text.split("\n"))
        visible = set(range(total_lines))

        # Remove lines that are inside folded regions
        for region in self.regions:
            if region.is_folded:
                for i in range(region.start_line + 1, region.end_line + 1):
                    visible.discard(i)

        return sorted(visible)

    def get_fold_indicators(self) -> List[Tuple[int, bool]]:
        """Get fold indicators for each region start line.

        Returns:
            List of (line_number, is_folded) tuples
        """
        indicators = []
        for region in self.regions:
            if region.end_line > region.start_line:  # Only if multi-line
                indicators.append((region.start_line, region.is_folded))
        return sorted(indicators)

    def clear(self) -> None:
        """Clear all regions."""
        self.regions = []
        self._indentation_levels = []
