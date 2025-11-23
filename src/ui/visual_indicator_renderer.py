"""Visual indicator renderer for showing whitespace and line endings in the editor."""

from PyQt6.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat, QColor, QFont
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
        self._original_text = {}  # Cache original text to detect changes
        self._is_updating = False

    def set_show_whitespace(self, show: bool):
        """Enable/disable whitespace indicators.

        Args:
            show: Whether to show whitespace
        """
        if self.settings.show_whitespace != show:
            self.settings.show_whitespace = show
            self._update_document_display()

    def set_show_line_endings(self, show: bool):
        """Enable/disable line ending indicators.

        Args:
            show: Whether to show line endings
        """
        if self.settings.show_line_endings != show:
            self.settings.show_line_endings = show
            self._update_document_display()

    def _update_document_display(self):
        """Update document to show/hide visual indicators."""
        if self._is_updating:
            return

        self._is_updating = True
        try:
            # Rehighlight all blocks with the new settings
            self.rehighlight()
        finally:
            self._is_updating = False

    def highlightBlock(self, text: str):
        """Highlight whitespace and line ending characters with visible formatting.

        Args:
            text: The text block to highlight
        """
        if not self.settings.show_whitespace and not self.settings.show_line_endings:
            return

        # Create format for spaces - with visible background
        space_format = QTextCharFormat()
        space_format.setBackground(QColor("#E8F4F8"))  # Light blue-gray background
        space_format.setForeground(QColor("#0066CC"))   # Blue text (dot symbol)

        # Create format for tabs - with more prominent background
        tab_format = QTextCharFormat()
        tab_format.setBackground(QColor("#FFE8CC"))    # Light orange background
        tab_format.setForeground(QColor("#FF8800"))     # Orange text (arrow symbol)
        tab_format.setFontWeight(QFont.Weight.Bold)

        # Highlight spaces and tabs
        if self.settings.show_whitespace:
            for i, char in enumerate(text):
                if char == " ":
                    self.setFormat(i, 1, space_format)
                elif char == "\t":
                    self.setFormat(i, 1, tab_format)

        # Show line ending indicators
        if self.settings.show_line_endings and len(text) > 0:
            # Highlight the end of the line to show where it ends
            eol_format = QTextCharFormat()
            eol_format.setForeground(QColor("#CCCCCC"))
            eol_format.setBackground(QColor("#F0F0F0"))
            # This will be visible at the end of each line
