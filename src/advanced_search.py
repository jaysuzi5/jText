"""Advanced search engine with regex support, history, and search options."""

import re
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchResult:
    """Represents a single search result."""

    start: int  # Position in text where match starts
    end: int  # Position in text where match ends
    line_num: int  # Line number (0-indexed)
    column: int  # Column in line (0-indexed)
    match_text: str  # The matched text


@dataclass
class SearchQuery:
    """Represents a search query with options."""

    pattern: str
    case_sensitive: bool = False
    whole_words: bool = False
    regex: bool = False
    timestamp: datetime = field(default_factory=datetime.now)

    def __hash__(self) -> int:
        """Make SearchQuery hashable for use in sets/dicts."""
        return hash((self.pattern, self.case_sensitive, self.whole_words, self.regex))

    def __eq__(self, other: object) -> bool:
        """Compare queries."""
        if not isinstance(other, SearchQuery):
            return NotImplemented
        return (
            self.pattern == other.pattern
            and self.case_sensitive == other.case_sensitive
            and self.whole_words == other.whole_words
            and self.regex == other.regex
        )


class AdvancedSearchEngine:
    """Advanced search engine with regex support and history."""

    def __init__(self, max_history: int = 50):
        """Initialize search engine.

        Args:
            max_history: Maximum number of search queries to keep in history
        """
        self.max_history = max_history
        self.search_history: List[SearchQuery] = []
        self.last_results: List[SearchResult] = []
        self.current_result_index: int = -1

    def search(self, text: str, query: SearchQuery) -> List[SearchResult]:
        """Search for pattern in text.

        Args:
            text: The text to search in
            query: The search query with pattern and options

        Returns:
            List of search results
        """
        self.last_results = []
        self.current_result_index = -1

        if not text or not query.pattern:
            return []

        # Add to history
        self._add_to_history(query)

        # Perform search
        if query.regex:
            results = self._regex_search(text, query)
        else:
            results = self._literal_search(text, query)

        self.last_results = results
        return results

    def _literal_search(self, text: str, query: SearchQuery) -> List[SearchResult]:
        """Perform literal string search.

        Args:
            text: The text to search in
            query: The search query

        Returns:
            List of search results
        """
        pattern = query.pattern

        if not query.case_sensitive:
            pattern = pattern.lower()
            text_search = text.lower()
        else:
            text_search = text

        results = []
        start = 0

        while True:
            pos = text_search.find(pattern, start)
            if pos == -1:
                break

            # Check whole words requirement
            if query.whole_words:
                if not self._is_whole_word(text, pos, len(pattern)):
                    start = pos + 1
                    continue

            # Get line and column info
            line_num = text[:pos].count("\n")
            line_start = text.rfind("\n", 0, pos) + 1
            column = pos - line_start

            # Get matched text from original
            match_text = text[pos : pos + len(pattern)]

            results.append(
                SearchResult(
                    start=pos,
                    end=pos + len(pattern),
                    line_num=line_num,
                    column=column,
                    match_text=match_text,
                )
            )

            start = pos + 1

        return results

    def _regex_search(self, text: str, query: SearchQuery) -> List[SearchResult]:
        """Perform regex search.

        Args:
            text: The text to search in
            query: The search query

        Returns:
            List of search results

        Raises:
            re.error: If regex pattern is invalid
        """
        results = []
        flags = 0 if query.case_sensitive else re.IGNORECASE

        try:
            pattern = query.pattern
            if query.whole_words:
                pattern = r"\b" + pattern + r"\b"

            regex = re.compile(pattern, flags)

            for match in regex.finditer(text):
                pos = match.start()
                line_num = text[:pos].count("\n")
                line_start = text.rfind("\n", 0, pos) + 1
                column = pos - line_start

                results.append(
                    SearchResult(
                        start=match.start(),
                        end=match.end(),
                        line_num=line_num,
                        column=column,
                        match_text=match.group(),
                    )
                )

            return results

        except re.error:
            raise

    def _is_whole_word(self, text: str, pos: int, length: int) -> bool:
        """Check if text at position is a whole word.

        Args:
            text: The full text
            pos: Position to check
            length: Length of match

        Returns:
            True if match is a whole word
        """
        # Check character before
        if pos > 0:
            if text[pos - 1].isalnum() or text[pos - 1] == "_":
                return False

        # Check character after
        end_pos = pos + length
        if end_pos < len(text):
            if text[end_pos].isalnum() or text[end_pos] == "_":
                return False

        return True

    def find_next(self, text: str, query: Optional[SearchQuery] = None) -> Optional[SearchResult]:
        """Find next occurrence from current position.

        Args:
            text: The text to search in
            query: Optional new search query (if not provided, uses last results)

        Returns:
            Next search result or None
        """
        if query:
            self.search(text, query)

        if not self.last_results:
            return None

        self.current_result_index = (self.current_result_index + 1) % len(self.last_results)
        return self.last_results[self.current_result_index]

    def find_previous(self, text: str, query: Optional[SearchQuery] = None) -> Optional[SearchResult]:
        """Find previous occurrence from current position.

        Args:
            text: The text to search in
            query: Optional new search query (if not provided, uses last results)

        Returns:
            Previous search result or None
        """
        if query:
            self.search(text, query)

        if not self.last_results:
            return None

        # If at start or no current result, start from end
        if self.current_result_index <= 0:
            self.current_result_index = len(self.last_results) - 1
        else:
            self.current_result_index -= 1

        return self.last_results[self.current_result_index]

    def replace(
        self, text: str, query: SearchQuery, replacement: str, replace_all: bool = False
    ) -> Tuple[str, int]:
        """Replace occurrences in text.

        Args:
            text: The text to search and replace in
            query: The search query
            replacement: The replacement text
            replace_all: Replace all occurrences if True, else just current

        Returns:
            Tuple of (modified_text, number_of_replacements)
        """
        results = self.search(text, query)

        if not results:
            return text, 0

        if replace_all:
            # Replace all results (from end to start to preserve positions)
            modified_text = text
            for result in reversed(results):
                modified_text = modified_text[: result.start] + replacement + modified_text[result.end :]
            return modified_text, len(results)
        else:
            # Replace only current result
            if self.current_result_index < 0 or self.current_result_index >= len(results):
                self.current_result_index = 0

            result = results[self.current_result_index]
            modified_text = text[: result.start] + replacement + text[result.end :]
            return modified_text, 1

    def _add_to_history(self, query: SearchQuery) -> None:
        """Add query to search history.

        Args:
            query: The search query to add
        """
        # Remove duplicate if exists
        self.search_history = [q for q in self.search_history if q != query]

        # Add to beginning
        self.search_history.insert(0, query)

        # Keep only max_history items
        self.search_history = self.search_history[: self.max_history]

    def get_history(self) -> List[SearchQuery]:
        """Get search history.

        Returns:
            List of recent search queries
        """
        return self.search_history.copy()

    def clear_history(self) -> None:
        """Clear search history."""
        self.search_history = []

    def get_history_by_pattern(self, pattern: str) -> List[SearchQuery]:
        """Get search history items matching pattern.

        Args:
            pattern: The pattern to search for in history

        Returns:
            List of matching search queries
        """
        return [q for q in self.search_history if pattern.lower() in q.pattern.lower()]

    def highlight_results(self, text: str, results: Optional[List[SearchResult]] = None) -> Dict[int, List[Tuple[int, int]]]:
        """Get highlight regions for search results by line.

        Args:
            text: The original text
            results: The search results (uses last results if not provided)

        Returns:
            Dictionary mapping line number to list of (start, end) tuples
        """
        if results is None:
            results = self.last_results

        highlights: Dict[int, List[Tuple[int, int]]] = {}

        for result in results:
            if result.line_num not in highlights:
                highlights[result.line_num] = []

            highlights[result.line_num].append((result.column, result.column + len(result.match_text)))

        return highlights

    def get_result_count(self) -> int:
        """Get count of results from last search.

        Returns:
            Number of search results
        """
        return len(self.last_results)

    def get_current_result(self) -> Optional[SearchResult]:
        """Get the current result.

        Returns:
            Current search result or None
        """
        if self.current_result_index < 0 or self.current_result_index >= len(self.last_results):
            return None
        return self.last_results[self.current_result_index]

    def reset(self) -> None:
        """Reset search state."""
        self.last_results = []
        self.current_result_index = -1
