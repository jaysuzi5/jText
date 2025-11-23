"""JSON tree view widget for displaying hierarchical JSON structure."""

from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from src.json_tree_model import JsonTreeModel, JsonTreeNode


class JsonTreeView(QWidget):
    """Widget for displaying and interacting with JSON tree structure."""

    def __init__(self):
        """Initialize the JSON tree view."""
        super().__init__()
        self.model: JsonTreeModel = JsonTreeModel()
        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabel("JSON Tree")

        # Setup UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        layout = QVBoxLayout()

        # Control buttons
        button_layout = QHBoxLayout()
        expand_all_btn = QPushButton("Expand All")
        expand_all_btn.clicked.connect(self.expand_all)
        collapse_all_btn = QPushButton("Collapse All")
        collapse_all_btn.clicked.connect(self.collapse_all)
        button_layout.addWidget(expand_all_btn)
        button_layout.addWidget(collapse_all_btn)

        layout.addLayout(button_layout)
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

        # Setup tree widget styling
        self.tree_widget.setIndentation(20)
        self.tree_widget.itemExpanded.connect(self._on_item_expanded)
        self.tree_widget.itemCollapsed.connect(self._on_item_collapsed)

    def load_json(self, json_str: str) -> bool:
        """Load JSON string into tree view.

        Args:
            json_str: JSON string to load

        Returns:
            True if successful, False if invalid JSON
        """
        self.model = JsonTreeModel(json_str)

        if self.model.get_root() is None:
            return False

        self.tree_widget.clear()
        self._populate_tree()
        return True

    def _populate_tree(self) -> None:
        """Populate tree widget from model."""
        root = self.model.get_root()
        if root is None:
            return

        # Create root item
        if root.is_array_item or root.key:
            root_item = QTreeWidgetItem()
            root_item.setText(0, root.get_display_text())
            self._apply_formatting(root_item, root)
            root_item.setData(0, Qt.ItemDataRole.UserRole, root)
            self.tree_widget.addTopLevelItem(root_item)

            # Add children to root
            for child in root.children:
                self._add_tree_item(root_item, child)
        else:
            # Root is the JSON root (object or array)
            for child in root.children:
                child_item = QTreeWidgetItem()
                child_item.setText(0, child.get_display_text())
                self._apply_formatting(child_item, child)
                child_item.setData(0, Qt.ItemDataRole.UserRole, child)
                self.tree_widget.addTopLevelItem(child_item)

                # Add children
                for grandchild in child.children:
                    self._add_tree_item(child_item, grandchild)

    def _add_tree_item(
        self, parent_item: QTreeWidgetItem, node: JsonTreeNode
    ) -> QTreeWidgetItem:
        """Add tree item for a node.

        Args:
            parent_item: Parent tree widget item
            node: JSON tree node

        Returns:
            New tree widget item
        """
        item = QTreeWidgetItem()
        item.setText(0, node.get_display_text())
        self._apply_formatting(item, node)
        item.setData(0, Qt.ItemDataRole.UserRole, node)

        parent_item.addChild(item)

        # Add children recursively
        for child in node.children:
            self._add_tree_item(item, child)

        return item

    @staticmethod
    def _apply_formatting(item: QTreeWidgetItem, node: JsonTreeNode) -> None:
        """Apply formatting to a tree item.

        Args:
            item: Tree widget item
            node: JSON tree node
        """
        font = item.font(0)

        if isinstance(node.value, dict):
            # Object keys in blue
            item.setForeground(0, QColor("#0066cc"))
            font.setBold(True)
        elif isinstance(node.value, list):
            # Arrays in bold
            item.setForeground(0, QColor("#cc0000"))
            font.setBold(True)
        elif node.is_array_item:
            # Array items in green
            item.setForeground(0, QColor("#009900"))
        elif node.value is None:
            # null in gray
            item.setForeground(0, QColor("#666666"))
            font.setItalic(True)
        elif isinstance(node.value, bool):
            # Booleans in red
            item.setForeground(0, QColor("#cc0000"))
        elif isinstance(node.value, (int, float)):
            # Numbers in orange
            item.setForeground(0, QColor("#cc6600"))

        item.setFont(0, font)

    def _on_item_expanded(self, item: QTreeWidgetItem) -> None:
        """Handle item expanded event."""
        node = item.data(0, Qt.ItemDataRole.UserRole)
        if node:
            node.set_expanded(True)

    def _on_item_collapsed(self, item: QTreeWidgetItem) -> None:
        """Handle item collapsed event."""
        node = item.data(0, Qt.ItemDataRole.UserRole)
        if node:
            node.set_expanded(False)

    def expand_all(self) -> None:
        """Expand all nodes in the tree."""
        self.model.expand_all()
        self.tree_widget.expandAll()

    def collapse_all(self) -> None:
        """Collapse all nodes in the tree."""
        self.model.collapse_all()
        self.tree_widget.collapseAll()

    def get_current_json(self) -> str:
        """Get the current JSON as string."""
        return self.model.get_json_with_state()
