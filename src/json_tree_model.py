"""JSON tree model for representing hierarchical JSON structure."""

import json
from typing import Any, List, Optional, Dict


class JsonTreeNode:
    """Represents a single node in the JSON tree."""

    def __init__(
        self,
        key: Optional[str] = None,
        value: Any = None,
        parent: Optional["JsonTreeNode"] = None,
        is_array_item: bool = False,
        array_index: Optional[int] = None,
    ):
        """Initialize a JSON tree node.

        Args:
            key: The key for this node (None for array items or root)
            value: The value at this node
            parent: Parent node reference
            is_array_item: Whether this node is an array item
            array_index: Index if this is an array item
        """
        self.key = key
        self.value = value
        self.parent = parent
        self.is_array_item = is_array_item
        self.array_index = array_index
        self.children: List["JsonTreeNode"] = []
        self._expanded = True

    def add_child(self, child: "JsonTreeNode") -> None:
        """Add a child node.

        Args:
            child: Child node to add
        """
        child.parent = self
        self.children.append(child)

    def is_expandable(self) -> bool:
        """Check if node is expandable (has children)."""
        return len(self.children) > 0

    def get_display_text(self) -> str:
        """Get the display text for this node."""
        if self.is_array_item:
            if isinstance(self.value, (dict, list)):
                type_name = "Object" if isinstance(self.value, dict) else "Array"
                return f"[{self.array_index}] {type_name} ({len(self.value)} items)"
            else:
                return f"[{self.array_index}] {self._format_value(self.value)}"
        else:
            # Object key
            if isinstance(self.value, dict):
                return f'"{self.key}": Object ({len(self.value)} keys)'
            elif isinstance(self.value, list):
                return f'"{self.key}": Array ({len(self.value)} items)'
            else:
                return f'"{self.key}": {self._format_value(self.value)}'

    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a simple value for display."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            if len(value) > 50:
                return f'"{value[:47]}..."'
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return str(type(value).__name__)

    def toggle_expanded(self) -> None:
        """Toggle expanded state."""
        self._expanded = not self._expanded

    def set_expanded(self, expanded: bool) -> None:
        """Set expanded state.

        Args:
            expanded: True to expand, False to collapse
        """
        self._expanded = expanded

    def is_expanded(self) -> bool:
        """Check if node is currently expanded."""
        return self._expanded

    def collapse_all(self) -> None:
        """Recursively collapse all children."""
        self._expanded = False
        for child in self.children:
            child.collapse_all()

    def expand_all(self) -> None:
        """Recursively expand all children."""
        self._expanded = True
        for child in self.children:
            child.expand_all()


class JsonTreeModel:
    """Model for representing JSON data as a tree structure."""

    def __init__(self, json_str: str = ""):
        """Initialize the JSON tree model.

        Args:
            json_str: JSON string to parse
        """
        self.root: Optional[JsonTreeNode] = None
        self.raw_json = json_str
        if json_str and json_str.strip():
            self._parse_json(json_str)

    def _parse_json(self, json_str: str) -> None:
        """Parse JSON string and build tree.

        Args:
            json_str: JSON string to parse
        """
        try:
            data = json.loads(json_str)
            self.root = self._build_tree(data, None)
        except json.JSONDecodeError:
            self.root = None

    def _build_tree(
        self,
        data: Any,
        parent: Optional[JsonTreeNode],
        key: Optional[str] = None,
        is_array_item: bool = False,
        array_index: Optional[int] = None,
    ) -> JsonTreeNode:
        """Recursively build tree from JSON data.

        Args:
            data: JSON data (dict, list, or primitive)
            parent: Parent node
            key: Key for this node
            is_array_item: Whether this is an array item
            array_index: Index if array item

        Returns:
            Root node of subtree
        """
        node = JsonTreeNode(
            key=key,
            value=data,
            parent=parent,
            is_array_item=is_array_item,
            array_index=array_index,
        )

        if isinstance(data, dict):
            for item_key, item_value in data.items():
                child = self._build_tree(
                    item_value, node, key=item_key, is_array_item=False
                )
                node.add_child(child)
        elif isinstance(data, list):
            for idx, item_value in enumerate(data):
                child = self._build_tree(
                    item_value,
                    node,
                    is_array_item=True,
                    array_index=idx,
                )
                node.add_child(child)

        return node

    def get_root(self) -> Optional[JsonTreeNode]:
        """Get root node."""
        return self.root

    def collapse_all(self) -> None:
        """Collapse all nodes."""
        if self.root:
            self.root.collapse_all()

    def expand_all(self) -> None:
        """Expand all nodes."""
        if self.root:
            self.root.expand_all()

    def get_json_with_state(self) -> str:
        """Get formatted JSON string (for potential future use)."""
        if not self.root:
            return ""
        return json.dumps(self._node_to_dict(self.root), indent=2, ensure_ascii=False)

    @staticmethod
    def _node_to_dict(node: JsonTreeNode) -> Any:
        """Convert tree node back to dictionary/list.

        Args:
            node: Node to convert

        Returns:
            Dictionary, list, or primitive value
        """
        return node.value
