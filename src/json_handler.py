"""JSON handling functionality for jText."""

import json
from typing import Tuple, Optional


class JsonHandler:
    """Handles JSON formatting and validation."""

    @staticmethod
    def is_json(content: str) -> bool:
        """Check if content is valid JSON.

        Args:
            content: Text content to check

        Returns:
            True if content is valid JSON, False otherwise
        """
        if not content or not content.strip():
            return False

        try:
            json.loads(content)
            return True
        except (json.JSONDecodeError, ValueError):
            return False

    @staticmethod
    def format_json(content: str, indent: int = 2) -> Tuple[str, bool]:
        """Format JSON content with pretty printing.

        Args:
            content: JSON content to format
            indent: Number of spaces for indentation

        Returns:
            Tuple of (formatted_content, success)
            success is True if formatting succeeded, False if JSON is invalid
        """
        if not content or not content.strip():
            return "", False

        try:
            parsed = json.loads(content)
            formatted = json.dumps(parsed, indent=indent, sort_keys=False, ensure_ascii=False)
            return formatted, True
        except (json.JSONDecodeError, ValueError) as e:
            return content, False

    @staticmethod
    def minify_json(content: str) -> Tuple[str, bool]:
        """Minify JSON content (remove whitespace).

        Args:
            content: JSON content to minify

        Returns:
            Tuple of (minified_content, success)
            success is True if minification succeeded, False if JSON is invalid
        """
        if not content or not content.strip():
            return "", False

        try:
            parsed = json.loads(content)
            minified = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
            return minified, True
        except (json.JSONDecodeError, ValueError):
            return content, False

    @staticmethod
    def get_json_error(content: str) -> Optional[str]:
        """Get the error message if JSON is invalid.

        Args:
            content: JSON content to validate

        Returns:
            Error message if JSON is invalid, None if valid
        """
        if not content or not content.strip():
            return "Empty content"

        try:
            json.loads(content)
            return None
        except json.JSONDecodeError as e:
            return f"JSON Error at line {e.lineno}, column {e.colno}: {e.msg}"
        except ValueError as e:
            return str(e)

    @staticmethod
    def validate_json(content: str) -> Tuple[bool, Optional[str]]:
        """Validate JSON and return result with error message if invalid.

        Args:
            content: JSON content to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        error = JsonHandler.get_json_error(content)
        return error is None, error
