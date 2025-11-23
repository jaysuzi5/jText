"""Multi-cursor support for editing multiple locations simultaneously."""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class CursorPosition:
    """Represents a cursor position with line and column."""

    line: int
    column: int

    def __eq__(self, other):
        """Check if two cursor positions are equal."""
        if not isinstance(other, CursorPosition):
            return False
        return self.line == other.line and self.column == other.column

    def __lt__(self, other):
        """Compare cursor positions for sorting."""
        if self.line != other.line:
            return self.line < other.line
        return self.column < other.column

    def __hash__(self):
        """Make cursor position hashable."""
        return hash((self.line, self.column))


class MultiCursorManager:
    """Manages multiple cursors for simultaneous editing."""

    def __init__(self):
        """Initialize the multi-cursor manager."""
        self.cursors: List[CursorPosition] = []
        self.primary_cursor_index = 0

    def add_cursor(self, position: CursorPosition) -> None:
        """Add a new cursor at the specified position.

        Args:
            position: The cursor position to add
        """
        # Don't add duplicate cursors
        if position not in self.cursors:
            self.cursors.append(position)
            self._normalize_cursors()

    def remove_cursor(self, index: int) -> None:
        """Remove a cursor by index.

        Args:
            index: The index of the cursor to remove
        """
        if 0 <= index < len(self.cursors):
            self.cursors.pop(index)
            # Adjust primary cursor index if needed
            if self.primary_cursor_index >= len(self.cursors) and self.cursors:
                self.primary_cursor_index = len(self.cursors) - 1

    def clear_cursors(self) -> None:
        """Clear all cursors except the primary one."""
        if self.cursors:
            primary = self.cursors[self.primary_cursor_index]
            self.cursors = [primary]
            self.primary_cursor_index = 0

    def select_all_occurrences(self, text: str, search_term: str, case_sensitive: bool = False) -> None:
        """Select all occurrences of a search term and place cursors at each.

        Args:
            text: The text to search in
            search_term: The term to find
            case_sensitive: Whether the search is case sensitive
        """
        self.cursors = []
        self.primary_cursor_index = 0

        if not search_term:
            return

        search_text = text if case_sensitive else text.lower()
        search_term_normalized = search_term if case_sensitive else search_term.lower()

        # Find all occurrences
        lines = search_text.split("\n")
        for line_num, line in enumerate(lines):
            start_pos = 0
            while True:
                pos = line.find(search_term_normalized, start_pos)
                if pos == -1:
                    break
                # Add cursor at end of match
                self.cursors.append(CursorPosition(line_num, pos + len(search_term)))
                start_pos = pos + 1

        # Sort cursors by position
        self._normalize_cursors()

    def get_primary_cursor(self) -> Optional[CursorPosition]:
        """Get the primary (main) cursor position.

        Returns:
            The primary cursor position or None if no cursors exist
        """
        if 0 <= self.primary_cursor_index < len(self.cursors):
            return self.cursors[self.primary_cursor_index]
        return None

    def set_primary_cursor(self, index: int) -> None:
        """Set which cursor is the primary cursor.

        Args:
            index: The index of the cursor to make primary
        """
        if 0 <= index < len(self.cursors):
            self.primary_cursor_index = index

    def get_cursor_count(self) -> int:
        """Get the number of active cursors.

        Returns:
            The number of cursors
        """
        return len(self.cursors)

    def move_all_cursors(self, line_delta: int = 0, column_delta: int = 0) -> None:
        """Move all cursors by the specified amounts.

        Args:
            line_delta: Number of lines to move (positive is down)
            column_delta: Number of columns to move (positive is right)
        """
        for cursor in self.cursors:
            cursor.line = max(0, cursor.line + line_delta)
            cursor.column = max(0, cursor.column + column_delta)

    def delete_at_all_cursors(self, text: str, delete_forward: bool = True) -> str:
        """Delete characters at all cursor positions.

        Args:
            text: The current text
            delete_forward: If True, delete forward; if False, delete backward

        Returns:
            The modified text
        """
        if not self.cursors:
            return text

        lines = text.split("\n")

        # Process deletions from end to start to avoid position shifts
        for cursor in sorted(self.cursors, reverse=True):
            if 0 <= cursor.line < len(lines):
                line = lines[cursor.line]
                if delete_forward and cursor.column < len(line):
                    # Delete forward
                    lines[cursor.line] = line[: cursor.column] + line[cursor.column + 1 :]
                elif not delete_forward and cursor.column > 0:
                    # Delete backward
                    lines[cursor.line] = line[: cursor.column - 1] + line[cursor.column :]
                    cursor.column = max(0, cursor.column - 1)

        return "\n".join(lines)

    def insert_at_all_cursors(self, text: str, insert_text: str) -> str:
        """Insert text at all cursor positions.

        Args:
            text: The current text
            insert_text: The text to insert

        Returns:
            The modified text
        """
        if not self.cursors:
            return text

        lines = text.split("\n")

        # Process insertions from end to start to avoid position shifts
        for cursor in sorted(self.cursors, reverse=True):
            if 0 <= cursor.line < len(lines):
                line = lines[cursor.line]
                lines[cursor.line] = line[: cursor.column] + insert_text + line[cursor.column :]
                cursor.column += len(insert_text)

        return "\n".join(lines)

    def merge_overlapping_cursors(self) -> None:
        """Remove cursors that are at the same position."""
        self.cursors = list(set(self.cursors))
        self._normalize_cursors()

    def _normalize_cursors(self) -> None:
        """Sort cursors and ensure primary cursor index is valid."""
        self.cursors.sort()
        if self.primary_cursor_index >= len(self.cursors):
            self.primary_cursor_index = max(0, len(self.cursors) - 1)
