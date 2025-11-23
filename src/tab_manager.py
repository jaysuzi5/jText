"""Tab manager for handling multiple document tabs."""

from typing import Optional, List
from src.document import Document


class TabManager:
    """Manages multiple text document tabs."""

    def __init__(self):
        """Initialize the tab manager."""
        self._documents: List[Document] = []
        self._active_index = -1

    def add_tab(self, document: Optional[Document] = None) -> int:
        """Add a new tab with a document.

        Args:
            document: Document to add (creates empty if None)

        Returns:
            Index of the newly added tab
        """
        if document is None:
            document = Document()

        self._documents.append(document)
        new_index = len(self._documents) - 1

        # Activate the new tab if no active tab exists
        if self._active_index == -1:
            self._active_index = new_index

        return new_index

    def close_tab(self, index: int) -> bool:
        """Close a tab at the given index.

        Args:
            index: Index of tab to close

        Returns:
            True if tab was closed, False if only one tab remains
        """
        if len(self._documents) <= 1:
            return False

        if 0 <= index < len(self._documents):
            self._documents.pop(index)

            # Adjust active index
            if self._active_index >= len(self._documents):
                self._active_index = len(self._documents) - 1

            return True

        return False

    def set_active_tab(self, index: int) -> bool:
        """Set the active tab.

        Args:
            index: Index of tab to activate

        Returns:
            True if tab was activated, False if index invalid
        """
        if 0 <= index < len(self._documents):
            self._active_index = index
            return True

        return False

    def get_active_document(self) -> Optional[Document]:
        """Get the currently active document.

        Returns:
            Active Document or None if no tabs exist
        """
        if self._active_index >= 0 and self._active_index < len(self._documents):
            return self._documents[self._active_index]

        return None

    def get_document(self, index: int) -> Optional[Document]:
        """Get a document by index.

        Args:
            index: Index of document

        Returns:
            Document at index or None if index invalid
        """
        if 0 <= index < len(self._documents):
            return self._documents[index]

        return None

    def get_active_index(self) -> int:
        """Get the index of the active tab.

        Returns:
            Index of active tab or -1 if no tabs
        """
        return self._active_index

    def get_tab_count(self) -> int:
        """Get the total number of tabs.

        Returns:
            Number of open tabs
        """
        return len(self._documents)

    def get_all_documents(self) -> List[Document]:
        """Get all documents.

        Returns:
            List of all open documents
        """
        return self._documents.copy()

    def has_unsaved_changes(self) -> bool:
        """Check if any tab has unsaved changes.

        Returns:
            True if any document is modified
        """
        return any(doc.is_modified for doc in self._documents)

    def clear(self) -> None:
        """Clear all tabs and reset state."""
        self._documents.clear()
        self._active_index = -1
