"""Document model for managing text content and state."""

from typing import Optional
from pathlib import Path


class Document:
    """Represents a text document with state tracking."""

    def __init__(self, content: str = ""):
        """Initialize a document with optional content.

        Args:
            content: Initial text content
        """
        self._content = content
        self._original_content = content
        self._file_path: Optional[Path] = None
        self._undo_stack: list[str] = []
        self._redo_stack: list[str] = []

    @property
    def content(self) -> str:
        """Get the current content."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """Set the content and track for undo."""
        if self._content != value:
            self._undo_stack.append(self._content)
            self._redo_stack.clear()
            self._content = value

    @property
    def file_path(self) -> Optional[Path]:
        """Get the file path of the document."""
        return self._file_path

    @file_path.setter
    def file_path(self, path: Optional[Path]) -> None:
        """Set the file path."""
        self._file_path = path if path is None else Path(path)

    @property
    def is_modified(self) -> bool:
        """Check if document has unsaved changes."""
        return self._content != self._original_content

    def mark_saved(self) -> None:
        """Mark the document as saved (original content = current content)."""
        self._original_content = self._content
        self._undo_stack.clear()
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Undo the last change.

        Returns:
            True if undo was performed, False if no undo history
        """
        if not self._undo_stack:
            return False

        self._redo_stack.append(self._content)
        self._content = self._undo_stack.pop()
        return True

    def redo(self) -> bool:
        """Redo the last undone change.

        Returns:
            True if redo was performed, False if no redo history
        """
        if not self._redo_stack:
            return False

        self._undo_stack.append(self._content)
        self._content = self._redo_stack.pop()
        return True

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0

    def get_file_name(self) -> str:
        """Get the file name or 'Untitled' if no file is set."""
        if self._file_path is None:
            return "Untitled"
        return self._file_path.name

    def clear(self) -> None:
        """Clear the document and reset state."""
        self._content = ""
        self._original_content = ""
        self._file_path = None
        self._undo_stack.clear()
        self._redo_stack.clear()
