"""Dialog for viewing JSON as an expandable tree structure."""

from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from src.json_tree_view import JsonTreeView


class JsonTreeDialog(QDialog):
    """Dialog for displaying JSON in tree view format."""

    def __init__(self, parent=None):
        """Initialize JSON tree dialog.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("JSON Tree View")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Create JSON tree view
        self.tree_view = JsonTreeView()
        layout.addWidget(self.tree_view)

        self.setLayout(layout)

        # Setup keyboard shortcuts
        self._setup_shortcuts()

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        # Shortcut for expand all: Ctrl+E or Cmd+E
        self.setShortcutEnabled(
            self.addAction("Expand All (Cmd+E)"), True
        )

        # Shortcut for collapse all: Ctrl+L or Cmd+L
        self.setShortcutEnabled(
            self.addAction("Collapse All (Cmd+L)"), True
        )

    def load_json(self, json_str: str) -> bool:
        """Load JSON string into tree view.

        Args:
            json_str: JSON string to load

        Returns:
            True if successful, False if invalid JSON
        """
        return self.tree_view.load_json(json_str)

    def get_json(self) -> str:
        """Get current JSON as string.

        Returns:
            JSON string
        """
        return self.tree_view.get_current_json()
