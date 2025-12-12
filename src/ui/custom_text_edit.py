"""Custom QTextEdit to override default behaviors."""

from PyQt6.QtWidgets import QTextEdit


class CustomTextEdit(QTextEdit):
    """A custom QTextEdit that forces pasting as plain text."""

    def __init__(self, parent=None):
        """Initialize the custom text edit."""
        super().__init__(parent)

    def insertFromMimeData(self, source):
        """Override to paste only plain text."""
        if source.hasText():
            self.insertPlainText(source.text())
        # We ignore other mime types to prevent rich text pasting.
