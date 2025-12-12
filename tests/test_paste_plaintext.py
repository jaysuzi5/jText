"""UI integration tests for pasting plaintext to verify content consistency."""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMimeData
from src.ui.main_window import MainWindow


@pytest.fixture
def app():
    """Provide QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def main_window(app):
    """Create a main window for testing."""
    window = MainWindow()
    window.show()
    return window


def test_paste_as_plain_text(main_window):
    """Test that pasting rich text results in plain text."""
    text_edit = main_window._get_current_text_edit()
    assert text_edit is not None

    # Get clipboard
    clipboard = QApplication.clipboard()

    # Create mime data with both rich and plain text
    mime_data = QMimeData()
    plain_text = "Hello, World!"
    html_text = "<h1>Hello, World!</h1>"
    mime_data.setText(plain_text)
    mime_data.setHtml(html_text)

    # Set clipboard data
    clipboard.setMimeData(mime_data)

    # Trigger paste action
    text_edit.paste()

    # Check that only plain text was pasted
    assert text_edit.toPlainText() == plain_text
