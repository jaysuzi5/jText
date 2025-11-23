"""Find and replace functionality for text content."""

from typing import List, Tuple, Optional


class FindReplaceEngine:
    """Engine for finding and replacing text."""

    def __init__(self):
        """Initialize the find/replace engine."""
        self.case_sensitive = False
        self.whole_words = False

    def find_all(self, text: str, search_term: str) -> List[Tuple[int, int]]:
        """Find all occurrences of search term in text.

        Args:
            text: Text to search in
            search_term: Term to find

        Returns:
            List of (start_pos, end_pos) tuples for each match
        """
        if not search_term:
            return []

        matches = []
        search_text = text if self.case_sensitive else text.lower()
        search_term_lower = search_term if self.case_sensitive else search_term.lower()

        start = 0
        while True:
            pos = search_text.find(search_term_lower, start)
            if pos == -1:
                break

            # Check whole words constraint
            if self.whole_words:
                if not self._is_whole_word(text, pos, pos + len(search_term)):
                    start = pos + 1
                    continue

            matches.append((pos, pos + len(search_term)))
            start = pos + 1

        return matches

    def find_next(
        self, text: str, search_term: str, start_pos: int
    ) -> Optional[Tuple[int, int]]:
        """Find the next occurrence after start position.

        Args:
            text: Text to search in
            search_term: Term to find
            start_pos: Position to start searching from

        Returns:
            (start_pos, end_pos) or None if not found
        """
        if not search_term:
            return None

        search_text = text if self.case_sensitive else text.lower()
        search_term_lower = search_term if self.case_sensitive else search_term.lower()

        pos = search_text.find(search_term_lower, start_pos)

        while pos != -1:
            if self.whole_words:
                if self._is_whole_word(text, pos, pos + len(search_term)):
                    return (pos, pos + len(search_term))
                pos = search_text.find(search_term_lower, pos + 1)
            else:
                return (pos, pos + len(search_term))

        return None

    def find_previous(
        self, text: str, search_term: str, start_pos: int
    ) -> Optional[Tuple[int, int]]:
        """Find the previous occurrence before start position.

        Args:
            text: Text to search in
            search_term: Term to find
            start_pos: Position to start searching backwards from

        Returns:
            (start_pos, end_pos) or None if not found
        """
        if not search_term:
            return None

        search_text = text if self.case_sensitive else text.lower()
        search_term_lower = search_term if self.case_sensitive else search_term.lower()

        pos = search_text.rfind(search_term_lower, 0, start_pos)

        while pos != -1:
            if self.whole_words:
                if self._is_whole_word(text, pos, pos + len(search_term)):
                    return (pos, pos + len(search_term))
                pos = search_text.rfind(search_term_lower, 0, pos)
            else:
                return (pos, pos + len(search_term))

        return None

    def replace(self, text: str, search_term: str, replace_term: str) -> Tuple[str, int]:
        """Replace first occurrence of search term.

        Args:
            text: Text to search in
            search_term: Term to find
            replace_term: Replacement text

        Returns:
            (modified_text, match_count)
        """
        if not search_term:
            return text, 0

        matches = self.find_all(text, search_term)

        if not matches:
            return text, 0

        start, end = matches[0]
        modified = text[:start] + replace_term + text[end:]

        return modified, 1

    def replace_all(self, text: str, search_term: str, replace_term: str) -> Tuple[str, int]:
        """Replace all occurrences of search term.

        Args:
            text: Text to search in
            search_term: Term to find
            replace_term: Replacement text

        Returns:
            (modified_text, match_count)
        """
        if not search_term:
            return text, 0

        matches = self.find_all(text, search_term)

        if not matches:
            return text, 0

        # Replace from end to start to preserve positions
        modified = text
        for start, end in reversed(matches):
            modified = modified[:start] + replace_term + modified[end:]

        return modified, len(matches)

    def _is_whole_word(self, text: str, start: int, end: int) -> bool:
        """Check if match is a whole word (not part of larger word).

        Args:
            text: Full text
            start: Start position of match
            end: End position of match

        Returns:
            True if match is a whole word
        """
        # Check character before match
        if start > 0 and text[start - 1].isalnum():
            return False

        # Check character after match
        if end < len(text) and text[end].isalnum():
            return False

        return True

    def set_case_sensitive(self, case_sensitive: bool) -> None:
        """Set case sensitivity for searches.

        Args:
            case_sensitive: Whether to match case
        """
        self.case_sensitive = case_sensitive

    def set_whole_words(self, whole_words: bool) -> None:
        """Set whole words matching.

        Args:
            whole_words: Whether to match whole words only
        """
        self.whole_words = whole_words
