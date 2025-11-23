"""Visual indicator renderer for showing whitespace and line endings in the editor."""

from PyQt6.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat, QColor
from src.visual_indicators import VisualIndicatorSettings


class VisualIndicatorHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for visual indicators (whitespace and line endings)."""

    def __init__(self, document: QTextDocument | None = None):
        """Initialize the highlighter.

        Args:
            document: The text document to highlight
        """
        super().__init__(document)
        self.settings = VisualIndicatorSettings()

    def set_show_whitespace(self, show: bool):
        """Enable/disable whitespace indicators.

        Args:
            show: Whether to show whitespace
        """
        self.settings.show_whitespace = show
        self.rehighlight()

    def set_show_line_endings(self, show: bool):
        """Enable/disable line ending indicators.

        Args:
            show: Whether to show line endings
        """
        self.settings.show_line_endings = show
        self.rehighlight()

    def highlightBlock(self, text: str):
        """Highlight whitespace and line ending characters.

        Args:
            text: The text block to highlight
        """
        # Format for indicator characters
        indicator_format = QTextCharFormat()
        indicator_format.setForeground(QColor("#999999"))  # Medium gray
        indicator_format.setFontItalic(True)

        # Highlight spaces and tabs
        if self.settings.show_whitespace:
            for i, char in enumerate(text):
                if char == " ":
                    # Highlight spaces in light gray
                    space_format = QTextCharFormat()
                    space_format.setForeground(QColor("#DDDDDD"))
                    self.setFormat(i, 1, space_format)
                elif char == "\t":
                    # Highlight tabs in light gray
                    tab_format = QTextCharFormat()
                    tab_format.setForeground(QColor("#DDDDDD"))
                    tab_format.setFontStrikeOut(False)
                    self.setFormat(i, 1, tab_format)

        # Line endings are shown differently - we can't actually insert them into the text
        # since they're implicit at the end of each line. Instead, we highlight the
        # last character or use block metadata.
        if self.settings.show_line_endings and len(text) > 0:
            # Optional: Highlight the last non-whitespace character to indicate line ending
            pass
