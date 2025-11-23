"""Unit tests for JsonTreeModel and JsonTreeNode."""

import pytest
from src.json_tree_model import JsonTreeNode, JsonTreeModel


class TestJsonTreeNode:
    """Test JsonTreeNode."""

    def test_create_node_with_key(self):
        """Test creating a node with a key."""
        node = JsonTreeNode(key="name", value="John")
        assert node.key == "name"
        assert node.value == "John"
        assert node.parent is None
        assert len(node.children) == 0

    def test_create_array_item_node(self):
        """Test creating an array item node."""
        node = JsonTreeNode(value="item", is_array_item=True, array_index=0)
        assert node.is_array_item is True
        assert node.array_index == 0
        assert node.key is None

    def test_add_child(self):
        """Test adding a child node."""
        parent = JsonTreeNode(key="parent", value={})
        child = JsonTreeNode(key="child", value="value")
        parent.add_child(child)

        assert len(parent.children) == 1
        assert parent.children[0] is child
        assert child.parent is parent

    def test_is_expandable_with_children(self):
        """Test is_expandable with children."""
        parent = JsonTreeNode(key="parent", value={})
        child = JsonTreeNode(key="child", value="value")
        parent.add_child(child)

        assert parent.is_expandable() is True

    def test_is_expandable_no_children(self):
        """Test is_expandable without children."""
        node = JsonTreeNode(key="name", value="John")
        assert node.is_expandable() is False

    def test_display_text_simple_value(self):
        """Test display text for simple values."""
        node = JsonTreeNode(key="age", value=30)
        assert '"age": 30' in node.get_display_text()

    def test_display_text_object(self):
        """Test display text for object."""
        # Note: display text shows count from value (dict), not children
        parent = JsonTreeNode(key="user", value={"name": "John"})

        text = parent.get_display_text()
        assert '"user"' in text
        assert "Object" in text
        assert "1" in text  # 1 key in dict

    def test_display_text_array(self):
        """Test display text for array."""
        # Note: display text shows count from value (list), not children
        parent = JsonTreeNode(key="items", value=["item1", "item2"])

        text = parent.get_display_text()
        assert '"items"' in text
        assert "Array" in text
        assert "2" in text  # 2 items in list

    def test_display_text_array_item_primitive(self):
        """Test display text for array item with primitive value."""
        node = JsonTreeNode(value="item", is_array_item=True, array_index=2)
        text = node.get_display_text()
        assert "[2]" in text
        assert '"item"' in text

    def test_display_text_string_truncation(self):
        """Test display text truncates long strings."""
        long_string = "a" * 100
        node = JsonTreeNode(key="data", value=long_string)
        text = node.get_display_text()
        assert len(text) < len(long_string)
        assert "..." in text

    def test_toggle_expanded(self):
        """Test toggling expanded state."""
        node = JsonTreeNode(key="test", value={})
        assert node.is_expanded() is True

        node.toggle_expanded()
        assert node.is_expanded() is False

        node.toggle_expanded()
        assert node.is_expanded() is True

    def test_set_expanded(self):
        """Test setting expanded state."""
        node = JsonTreeNode(key="test", value={})
        node.set_expanded(False)
        assert node.is_expanded() is False

        node.set_expanded(True)
        assert node.is_expanded() is True

    def test_collapse_all(self):
        """Test recursive collapse."""
        root = JsonTreeNode(key="root", value={})
        child1 = JsonTreeNode(key="child1", value={})
        child2 = JsonTreeNode(key="child2", value={})
        grandchild = JsonTreeNode(key="grandchild", value="value")

        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(grandchild)

        root.collapse_all()

        assert root.is_expanded() is False
        assert child1.is_expanded() is False
        assert child2.is_expanded() is False
        assert grandchild.is_expanded() is False

    def test_expand_all(self):
        """Test recursive expand."""
        root = JsonTreeNode(key="root", value={})
        child1 = JsonTreeNode(key="child1", value={})
        grandchild = JsonTreeNode(key="grandchild", value="value")

        root.add_child(child1)
        child1.add_child(grandchild)

        root.collapse_all()  # First collapse all
        root.expand_all()  # Then expand all

        assert root.is_expanded() is True
        assert child1.is_expanded() is True
        assert grandchild.is_expanded() is True


class TestJsonTreeModel:
    """Test JsonTreeModel."""

    def test_create_empty_model(self):
        """Test creating empty model."""
        model = JsonTreeModel()
        assert model.get_root() is None

    def test_parse_simple_object(self):
        """Test parsing simple object."""
        json_str = '{"name": "John", "age": 30}'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 2

    def test_parse_array(self):
        """Test parsing array."""
        json_str = '[1, 2, 3]'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 3

    def test_parse_nested_object(self):
        """Test parsing nested object."""
        json_str = '{"user": {"name": "John", "address": {"city": "NYC"}}}'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 1
        user_node = root.children[0]
        assert len(user_node.children) == 2
        address_node = user_node.children[1]
        assert len(address_node.children) == 1

    def test_parse_array_of_objects(self):
        """Test parsing array of objects."""
        json_str = '[{"id": 1}, {"id": 2}]'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 2
        assert root.children[0].is_array_item is True
        assert root.children[1].is_array_item is True

    def test_parse_invalid_json(self):
        """Test parsing invalid JSON."""
        json_str = '{invalid}'
        model = JsonTreeModel(json_str)
        assert model.get_root() is None

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        model = JsonTreeModel("")
        assert model.get_root() is None

    def test_collapse_all_model(self):
        """Test collapsing all nodes in model."""
        json_str = '{"user": {"name": "John"}}'
        model = JsonTreeModel(json_str)

        model.collapse_all()

        root = model.get_root()
        assert root is not None
        assert root.is_expanded() is False
        assert root.children[0].is_expanded() is False

    def test_expand_all_model(self):
        """Test expanding all nodes in model."""
        json_str = '{"user": {"name": "John"}}'
        model = JsonTreeModel(json_str)

        model.collapse_all()
        model.expand_all()

        root = model.get_root()
        assert root is not None
        assert root.is_expanded() is True
        assert root.children[0].is_expanded() is True

    def test_get_json_with_state(self):
        """Test getting JSON string from model."""
        json_str = '{"name": "John", "age": 30}'
        model = JsonTreeModel(json_str)

        output = model.get_json_with_state()
        assert "name" in output
        assert "John" in output
        assert "age" in output
        assert "30" in output

    def test_parse_complex_structure(self):
        """Test parsing complex nested structure."""
        json_str = '''{
            "users": [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25}
            ],
            "total": 2
        }'''
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 2

        users_node = root.children[0]
        assert users_node.key == "users"
        assert len(users_node.children) == 2

    def test_parse_with_null_values(self):
        """Test parsing with null values."""
        json_str = '{"name": "John", "middle": null, "age": 30}'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 3

    def test_parse_with_boolean_values(self):
        """Test parsing with boolean values."""
        json_str = '{"active": true, "deleted": false}'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 2

    def test_parse_with_numbers(self):
        """Test parsing with various number types."""
        json_str = '{"int": 42, "float": 3.14, "negative": -10, "scientific": 1.5e-4}'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 4

    def test_empty_object(self):
        """Test parsing empty object."""
        json_str = '{}'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 0

    def test_empty_array(self):
        """Test parsing empty array."""
        json_str = '[]'
        model = JsonTreeModel(json_str)

        root = model.get_root()
        assert root is not None
        assert len(root.children) == 0
