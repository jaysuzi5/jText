"""Unit tests for multi-cursor support."""

import pytest
from src.multi_cursor import CursorPosition, MultiCursorManager


class TestCursorPosition:
    """Test CursorPosition dataclass."""

    def test_create_cursor_position(self):
        """Test creating a cursor position."""
        pos = CursorPosition(5, 10)
        assert pos.line == 5
        assert pos.column == 10

    def test_cursor_position_equality(self):
        """Test cursor position equality."""
        pos1 = CursorPosition(5, 10)
        pos2 = CursorPosition(5, 10)
        pos3 = CursorPosition(5, 11)
        assert pos1 == pos2
        assert pos1 != pos3

    def test_cursor_position_less_than(self):
        """Test cursor position comparison."""
        pos1 = CursorPosition(5, 10)
        pos2 = CursorPosition(5, 20)
        pos3 = CursorPosition(6, 10)
        assert pos1 < pos2
        assert pos2 < pos3
        assert not pos2 < pos1

    def test_cursor_position_hash(self):
        """Test cursor position is hashable."""
        pos1 = CursorPosition(5, 10)
        pos2 = CursorPosition(5, 10)
        assert hash(pos1) == hash(pos2)
        # Can be used in sets
        s = {pos1, pos2}
        assert len(s) == 1


class TestMultiCursorManager:
    """Test MultiCursorManager."""

    def test_create_manager(self):
        """Test creating a multi-cursor manager."""
        manager = MultiCursorManager()
        assert manager.get_cursor_count() == 0
        assert manager.cursors == []

    def test_add_cursor(self):
        """Test adding cursors."""
        manager = MultiCursorManager()
        pos = CursorPosition(5, 10)
        manager.add_cursor(pos)
        assert manager.get_cursor_count() == 1
        assert manager.cursors[0] == pos

    def test_add_multiple_cursors(self):
        """Test adding multiple cursors."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 20))
        manager.add_cursor(CursorPosition(3, 5))
        assert manager.get_cursor_count() == 3
        # Should be sorted
        assert manager.cursors[0].line == 3
        assert manager.cursors[1].line == 5
        assert manager.cursors[2].line == 10

    def test_no_duplicate_cursors(self):
        """Test that duplicate cursors are not added."""
        manager = MultiCursorManager()
        pos = CursorPosition(5, 10)
        manager.add_cursor(pos)
        manager.add_cursor(pos)
        assert manager.get_cursor_count() == 1

    def test_remove_cursor(self):
        """Test removing a cursor."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 20))
        manager.remove_cursor(0)
        assert manager.get_cursor_count() == 1
        assert manager.cursors[0].line == 10

    def test_remove_cursor_invalid_index(self):
        """Test removing with invalid index."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.remove_cursor(5)
        assert manager.get_cursor_count() == 1

    def test_clear_cursors(self):
        """Test clearing all cursors."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 20))
        manager.add_cursor(CursorPosition(3, 5))
        manager.set_primary_cursor(1)
        manager.clear_cursors()
        # Should only have the primary cursor
        assert manager.get_cursor_count() == 1
        assert manager.cursors[0].line == 5

    def test_get_primary_cursor(self):
        """Test getting the primary cursor."""
        manager = MultiCursorManager()
        pos = CursorPosition(5, 10)
        manager.add_cursor(pos)
        assert manager.get_primary_cursor() == pos

    def test_set_primary_cursor(self):
        """Test setting the primary cursor."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 20))
        manager.set_primary_cursor(1)
        assert manager.primary_cursor_index == 1
        assert manager.get_primary_cursor().line == 10

    def test_set_primary_cursor_invalid_index(self):
        """Test setting primary cursor with invalid index."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.set_primary_cursor(5)
        assert manager.primary_cursor_index == 0

    def test_select_all_occurrences_case_insensitive(self):
        """Test selecting all occurrences (case insensitive)."""
        manager = MultiCursorManager()
        text = "hello world\nhello there\nHELLO again"
        manager.select_all_occurrences(text, "hello", case_sensitive=False)
        assert manager.get_cursor_count() == 3
        # Should have cursors at end of each "hello"
        assert manager.cursors[0].line == 0
        assert manager.cursors[1].line == 1
        assert manager.cursors[2].line == 2

    def test_select_all_occurrences_case_sensitive(self):
        """Test selecting all occurrences (case sensitive)."""
        manager = MultiCursorManager()
        text = "hello world\nhello there\nHELLO again"
        manager.select_all_occurrences(text, "hello", case_sensitive=True)
        assert manager.get_cursor_count() == 2
        assert manager.cursors[0].line == 0
        assert manager.cursors[1].line == 1

    def test_select_all_occurrences_empty_search(self):
        """Test selecting with empty search term."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.select_all_occurrences("hello", "", case_sensitive=False)
        assert manager.get_cursor_count() == 0

    def test_select_all_occurrences_no_matches(self):
        """Test selecting with no matches."""
        manager = MultiCursorManager()
        manager.select_all_occurrences("hello world", "xyz", case_sensitive=False)
        assert manager.get_cursor_count() == 0

    def test_move_all_cursors(self):
        """Test moving all cursors."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 20))
        manager.move_all_cursors(line_delta=2, column_delta=5)
        assert manager.cursors[0].line == 7
        assert manager.cursors[0].column == 15
        assert manager.cursors[1].line == 12
        assert manager.cursors[1].column == 25

    def test_move_all_cursors_line_only(self):
        """Test moving cursors by lines only."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.move_all_cursors(line_delta=3)
        assert manager.cursors[0].line == 8
        assert manager.cursors[0].column == 10

    def test_move_all_cursors_column_only(self):
        """Test moving cursors by columns only."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.move_all_cursors(column_delta=5)
        assert manager.cursors[0].line == 5
        assert manager.cursors[0].column == 15

    def test_move_all_cursors_no_negative_positions(self):
        """Test that cursors don't go below 0."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.move_all_cursors(line_delta=-10, column_delta=-20)
        assert manager.cursors[0].line == 0
        assert manager.cursors[0].column == 0

    def test_delete_at_all_cursors_forward(self):
        """Test deleting forward at all cursors."""
        manager = MultiCursorManager()
        text = "hello world\nhello there"
        manager.select_all_occurrences(text, "hello", case_sensitive=True)
        result = manager.delete_at_all_cursors(text, delete_forward=True)
        # Cursor is at position 5 (after "hello"), deleting forward deletes the space
        assert "helloworld" in result
        assert "hellothere" in result

    def test_delete_at_all_cursors_backward(self):
        """Test deleting backward at all cursors."""
        manager = MultiCursorManager()
        text = "hello world"
        manager.add_cursor(CursorPosition(0, 5))
        result = manager.delete_at_all_cursors(text, delete_forward=False)
        # Should delete 'o' from hello
        assert result == "hell world"

    def test_insert_at_all_cursors(self):
        """Test inserting text at all cursors."""
        manager = MultiCursorManager()
        text = "hello world\nhello there"
        manager.select_all_occurrences(text, "hello", case_sensitive=True)
        result = manager.insert_at_all_cursors(text, "!")
        assert "hello! world" in result
        assert "hello! there" in result

    def test_insert_at_all_cursors_empty_text(self):
        """Test inserting with no cursors."""
        manager = MultiCursorManager()
        result = manager.insert_at_all_cursors("hello", "!")
        assert result == "hello"

    def test_merge_overlapping_cursors(self):
        """Test merging duplicate cursors."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(5, 10))
        # Duplicates should already be prevented by add_cursor
        assert manager.get_cursor_count() == 1

    def test_primary_cursor_adjustment_on_remove(self):
        """Test that primary cursor is adjusted when primary is removed."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 20))
        manager.add_cursor(CursorPosition(15, 30))
        manager.set_primary_cursor(2)
        manager.remove_cursor(2)
        # Primary should be adjusted
        assert manager.primary_cursor_index < len(manager.cursors)

    def test_cursor_sorting_on_normalize(self):
        """Test that cursors are sorted after normalization."""
        manager = MultiCursorManager()
        manager.add_cursor(CursorPosition(20, 30))
        manager.add_cursor(CursorPosition(5, 10))
        manager.add_cursor(CursorPosition(10, 15))
        # Should be sorted by line, then column
        assert manager.cursors[0].line == 5
        assert manager.cursors[1].line == 10
        assert manager.cursors[2].line == 20

    def test_select_all_occurrences_multiple_per_line(self):
        """Test selecting multiple occurrences on same line."""
        manager = MultiCursorManager()
        text = "the the the"
        manager.select_all_occurrences(text, "the", case_sensitive=True)
        assert manager.get_cursor_count() == 3
        # All on line 0, different columns
        assert all(c.line == 0 for c in manager.cursors)
        assert manager.cursors[0].column == 3
        assert manager.cursors[1].column == 7
        assert manager.cursors[2].column == 11
