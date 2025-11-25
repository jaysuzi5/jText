"""UI integration tests for tab reordering to verify content/name consistency."""

import pytest
from PyQt6.QtWidgets import QApplication, QTextEdit
from src.ui.draggable_tab_widget import DraggableTabWidget


class TestDraggableTabWidgetBasics:
    """Test DraggableTabWidget basic functionality."""

    @pytest.fixture
    def app(self):
        """Provide QApplication instance."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def tab_widget(self, app):
        """Create a draggable tab widget for testing."""
        return DraggableTabWidget()

    def test_draggable_tab_widget_creation(self, tab_widget):
        """Test creating a draggable tab widget."""
        assert tab_widget is not None
        assert tab_widget.count() == 0

    def test_add_tab_with_content(self, tab_widget):
        """Test adding tabs with content."""
        text_edit1 = QTextEdit()
        text_edit1.setPlainText("Content 1")
        tab_widget.addTab(text_edit1, "Tab 1")

        text_edit2 = QTextEdit()
        text_edit2.setPlainText("Content 2")
        tab_widget.addTab(text_edit2, "Tab 2")

        assert tab_widget.count() == 2
        assert tab_widget.tabText(0) == "Tab 1"
        assert tab_widget.tabText(1) == "Tab 2"

        # Verify content
        assert tab_widget.widget(0).toPlainText() == "Content 1"
        assert tab_widget.widget(1).toPlainText() == "Content 2"

    def test_tab_reordered_signal_emission(self, tab_widget):
        """Test that tabReordered signal is emitted."""
        signal_received = []

        def on_reorder(from_idx, to_idx):
            signal_received.append((from_idx, to_idx))

        text_edit1 = QTextEdit()
        text_edit1.setPlainText("Content 1")
        tab_widget.addTab(text_edit1, "Tab 1")

        text_edit2 = QTextEdit()
        text_edit2.setPlainText("Content 2")
        tab_widget.addTab(text_edit2, "Tab 2")

        tab_widget.tabReordered.connect(on_reorder)

        # Simulate move operation
        tab_widget._move_tab(0, 1)

        # Check signal was emitted
        assert len(signal_received) == 1

    def test_adjacent_tab_swap(self, tab_widget):
        """Test swapping adjacent tabs."""
        text_edit1 = QTextEdit()
        text_edit1.setPlainText("Content 1")
        tab_widget.addTab(text_edit1, "Tab 1")

        text_edit2 = QTextEdit()
        text_edit2.setPlainText("Content 2")
        tab_widget.addTab(text_edit2, "Tab 2")

        # Swap by moving 1 to 0
        tab_widget._move_tab(1, 0)

        # After moving 1 to 0: remove at 1 -> [Tab1]
        # Insert at 0 (no adjustment since 1 > 0): [Tab2, Tab1]
        assert tab_widget.count() == 2
        assert tab_widget.widget(0).toPlainText() == "Content 2"
        assert tab_widget.widget(1).toPlainText() == "Content 1"

    def test_tab_widget_reference_preservation(self, tab_widget):
        """Test that widget references are preserved during moves."""
        text_edit1 = QTextEdit()
        text_edit1.setPlainText("Content 1")
        tab_widget.addTab(text_edit1, "Tab 1")

        text_edit2 = QTextEdit()
        text_edit2.setPlainText("Content 2")
        tab_widget.addTab(text_edit2, "Tab 2")

        # Get the actual widget objects
        widget1 = tab_widget.widget(0)
        widget2 = tab_widget.widget(1)

        assert widget1 is text_edit1
        assert widget2 is text_edit2

        # Move and verify references still work
        tab_widget._move_tab(1, 0)

        # Widgets should still be the same objects
        assert tab_widget.widget(0) is widget2
        assert tab_widget.widget(1) is widget1
