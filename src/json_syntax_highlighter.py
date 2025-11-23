"""JSON syntax highlighter for PyQt6."""

from PyQt6.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression


class JsonSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for JSON documents."""

    def __init__(self, document: QTextDocument):
        """Initialize the syntax highlighter.

        Args:
            document: QTextDocument to highlight
        """
        super().__init__(document)

        # Define formats
        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor("#0066cc"))  # Blue
        self.key_format.setFontWeight(QFont.Weight.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#009900"))  # Green

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#cc6600"))  # Orange

        self.true_false_null_format = QTextCharFormat()
        self.true_false_null_format.setForeground(QColor("#cc0000"))  # Red
        self.true_false_null_format.setFontWeight(QFont.Weight.Bold)

        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#666666"))  # Gray
        self.bracket_format.setFontWeight(QFont.Weight.Bold)

        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#ff0000"))  # Red background
        self.error_format.setBackground(QColor("#ffcccc"))

    def highlightBlock(self, text: str) -> None:
        """Highlight a block of text (a line).

        Args:
            text: The text block to highlight
        """
        # Highlight JSON keys (strings before colons)
        key_pattern = QRegularExpression(r'"([^"\\]|\\.)*"\s*(?=:)')
        iterator = key_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.key_format)

        # Highlight string values (strings not followed by colon)
        string_pattern = QRegularExpression(r'"(?:[^"\\]|\\.)*"')
        iterator = string_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            # Skip if this is a key (already highlighted)
            if text[match.capturedEnd():match.capturedEnd() + 1].lstrip() != ':':
                self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        # Highlight numbers
        number_pattern = QRegularExpression(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?')
        iterator = number_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            # Check if number is not inside a string
            if not self._is_in_string(text, match.capturedStart()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)

        # Highlight true, false, null
        for word in ['true', 'false', 'null']:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                if not self._is_in_string(text, match.capturedStart()):
                    self.setFormat(match.capturedStart(), match.capturedLength(), self.true_false_null_format)

        # Highlight brackets and braces
        bracket_pattern = QRegularExpression(r'[{}\[\],:;]')
        iterator = bracket_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            if not self._is_in_string(text, match.capturedStart()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.bracket_format)

    def _is_in_string(self, text: str, position: int) -> bool:
        """Check if a position is inside a string.

        Args:
            text: The text to check
            position: The position to check

        Returns:
            True if position is inside a string, False otherwise
        """
        in_string = False
        escape = False

        for i in range(min(position, len(text))):
            char = text[i]

            if escape:
                escape = False
                continue

            if char == '\\':
                escape = True
                continue

            if char == '"':
                in_string = not in_string

        return in_string
