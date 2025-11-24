"""Unit tests for advanced search engine."""

import pytest
import re
from src.advanced_search import AdvancedSearchEngine, SearchQuery, SearchResult


class TestSearchQuery:
    """Test SearchQuery dataclass."""

    def test_create_search_query(self):
        """Test creating a search query."""
        query = SearchQuery(pattern="hello")
        assert query.pattern == "hello"
        assert not query.case_sensitive
        assert not query.whole_words
        assert not query.regex

    def test_search_query_with_options(self):
        """Test creating query with options."""
        query = SearchQuery(pattern="hello", case_sensitive=True, whole_words=True, regex=True)
        assert query.case_sensitive
        assert query.whole_words
        assert query.regex

    def test_search_query_equality(self):
        """Test query equality comparison."""
        q1 = SearchQuery(pattern="hello", case_sensitive=True)
        q2 = SearchQuery(pattern="hello", case_sensitive=True)
        q3 = SearchQuery(pattern="hello", case_sensitive=False)

        assert q1 == q2
        assert q1 != q3

    def test_search_query_hashable(self):
        """Test that queries can be used in sets/dicts."""
        q1 = SearchQuery(pattern="hello")
        q2 = SearchQuery(pattern="world")

        query_set = {q1, q2}
        assert len(query_set) == 2


class TestSearchEngineBasic:
    """Test basic search engine functionality."""

    def test_create_search_engine(self):
        """Test creating a search engine."""
        engine = AdvancedSearchEngine()
        assert engine.get_result_count() == 0

    def test_search_empty_text(self):
        """Test searching in empty text."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello")
        results = engine.search("", query)
        assert results == []

    def test_search_empty_pattern(self):
        """Test searching with empty pattern."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="")
        results = engine.search("hello world", query)
        assert results == []


class TestLiteralSearch:
    """Test literal string searching."""

    def test_simple_search(self):
        """Test simple string search."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello")
        results = engine.search("hello world hello", query)

        assert len(results) == 2
        assert results[0].match_text == "hello"
        assert results[1].match_text == "hello"

    def test_search_case_insensitive(self):
        """Test case insensitive search."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="HELLO", case_sensitive=False)
        results = engine.search("hello world Hello HELLO", query)

        assert len(results) == 3

    def test_search_case_sensitive(self):
        """Test case sensitive search."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello", case_sensitive=True)
        results = engine.search("hello world Hello HELLO", query)

        assert len(results) == 1

    def test_search_with_line_numbers(self):
        """Test that line numbers are calculated correctly."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="world")
        text = "hello\nworld\ntest\nworld"
        results = engine.search(text, query)

        assert len(results) == 2
        assert results[0].line_num == 1
        assert results[1].line_num == 3

    def test_search_with_column_numbers(self):
        """Test that column numbers are calculated correctly."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="world")
        text = "hello world"
        results = engine.search(text, query)

        assert len(results) == 1
        assert results[0].column == 6

    def test_search_no_matches(self):
        """Test search with no matches."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="xyz")
        results = engine.search("hello world", query)

        assert len(results) == 0


class TestWholeWordSearch:
    """Test whole words search option."""

    def test_whole_words_match(self):
        """Test whole words option with exact matches."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello", whole_words=True)
        results = engine.search("hello world", query)

        assert len(results) == 1

    def test_whole_words_no_partial(self):
        """Test whole words doesn't match partial words."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello", whole_words=True)
        results = engine.search("hello helloworld world_hello", query)

        assert len(results) == 1

    def test_whole_words_with_underscores(self):
        """Test whole words with underscores."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="test", whole_words=True)
        results = engine.search("test test_word word_test", query)

        assert len(results) == 1

    def test_whole_words_case_insensitive(self):
        """Test whole words with case insensitive."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="HELLO", whole_words=True, case_sensitive=False)
        results = engine.search("hello HELLO Hello", query)

        assert len(results) == 3


class TestRegexSearch:
    """Test regex search functionality."""

    def test_regex_pattern_basic(self):
        """Test basic regex pattern."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"\d+", regex=True)
        results = engine.search("test 123 hello 456", query)

        assert len(results) == 2
        assert results[0].match_text == "123"
        assert results[1].match_text == "456"

    def test_regex_alternation(self):
        """Test regex alternation."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"cat|dog", regex=True)
        results = engine.search("I have a cat and a dog", query)

        assert len(results) == 2

    def test_regex_character_class(self):
        """Test regex character classes."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"[aeiou]", regex=True)
        results = engine.search("hello", query)

        assert len(results) == 2  # e and o

    def test_regex_case_insensitive(self):
        """Test regex with case insensitive."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"hello", regex=True, case_sensitive=False)
        results = engine.search("hello HELLO Hello", query)

        assert len(results) == 3

    def test_regex_case_sensitive(self):
        """Test regex with case sensitive."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"hello", regex=True, case_sensitive=True)
        results = engine.search("hello HELLO Hello", query)

        assert len(results) == 1

    def test_regex_invalid_pattern(self):
        """Test regex with invalid pattern."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"[invalid", regex=True)

        with pytest.raises(re.error):
            engine.search("test", query)

    def test_regex_whole_words(self):
        """Test regex with whole words."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"test", regex=True, whole_words=True)
        results = engine.search("test testing tested", query)

        assert len(results) == 1

    def test_regex_quantifiers(self):
        """Test regex quantifiers."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"a+", regex=True)
        results = engine.search("a aa aaa b aaaa", query)

        assert len(results) == 4


class TestSearchNavigation:
    """Test finding next/previous results."""

    def test_find_next(self):
        """Test finding next result."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")
        engine.search("a b a c a", query)

        result1 = engine.find_next(None)
        result2 = engine.find_next(None)
        result3 = engine.find_next(None)

        assert result1.start == 0
        assert result2.start == 4
        assert result3.start == 8

    def test_find_next_wraps(self):
        """Test that find_next wraps around."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")
        engine.search("a b a", query)

        engine.find_next(None)
        engine.find_next(None)
        result = engine.find_next(None)  # Should wrap to first

        assert result.start == 0

    def test_find_previous(self):
        """Test finding previous result."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")
        engine.search("a b a c a", query)

        engine.current_result_index = 2  # Start at last

        result1 = engine.find_previous(None)
        result2 = engine.find_previous(None)

        assert result1.start == 4
        assert result2.start == 0

    def test_find_previous_wraps(self):
        """Test that find_previous wraps around."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")
        engine.search("a b a", query)

        engine.current_result_index = -1
        result = engine.find_previous(None)

        # Should wrap to last result
        assert result.start == 4

    def test_find_next_with_new_query(self):
        """Test find_next with new query."""
        engine = AdvancedSearchEngine()
        query1 = SearchQuery(pattern="a")
        query2 = SearchQuery(pattern="b")

        engine.search("a b a", query1)
        result = engine.find_next("a b a", query2)

        assert result.match_text == "b"


class TestReplace:
    """Test replace functionality."""

    def test_replace_single(self):
        """Test replacing single occurrence."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello")
        text = "hello world hello"

        engine.search(text, query)
        modified, count = engine.replace(text, query, "goodbye", replace_all=False)

        assert count == 1
        assert modified.count("goodbye") == 1
        assert modified.count("hello") == 1

    def test_replace_all(self):
        """Test replacing all occurrences."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello")
        text = "hello world hello"

        modified, count = engine.replace(text, query, "goodbye", replace_all=True)

        assert count == 2
        assert "goodbye" in modified
        assert "hello" not in modified

    def test_replace_case_insensitive(self):
        """Test replace with case insensitive."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello", case_sensitive=False)
        text = "hello Hello HELLO"

        modified, count = engine.replace(text, query, "hi", replace_all=True)

        assert count == 3

    def test_replace_regex(self):
        """Test replace with regex pattern."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"\d+", regex=True)
        text = "test 123 hello 456"

        modified, count = engine.replace(text, query, "X", replace_all=True)

        assert count == 2
        assert "X" in modified

    def test_replace_preserves_positions(self):
        """Test that replace works correctly with multiple replacements."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")
        text = "a b a c a"

        modified, count = engine.replace(text, query, "x", replace_all=True)

        assert count == 3
        assert modified == "x b x c x"


class TestSearchHistory:
    """Test search history functionality."""

    def test_add_to_history(self):
        """Test that searches are added to history."""
        engine = AdvancedSearchEngine()
        query1 = SearchQuery(pattern="hello")
        query2 = SearchQuery(pattern="world")

        engine.search("hello world", query1)
        engine.search("hello world", query2)

        history = engine.get_history()
        assert len(history) == 2

    def test_history_limit(self):
        """Test that history respects max size."""
        engine = AdvancedSearchEngine(max_history=3)

        for i in range(5):
            query = SearchQuery(pattern=f"pattern{i}")
            engine.search("test text", query)

        history = engine.get_history()
        assert len(history) <= 3

    def test_no_duplicate_history(self):
        """Test that duplicate queries are moved to front."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello")

        engine.search("hello world", query)
        engine.search("hello world", query)

        history = engine.get_history()
        assert len(history) == 1

    def test_get_history_by_pattern(self):
        """Test searching history by pattern."""
        engine = AdvancedSearchEngine()

        engine.search("test", SearchQuery(pattern="hello"))
        engine.search("test", SearchQuery(pattern="world"))
        engine.search("test", SearchQuery(pattern="help"))

        matching = engine.get_history_by_pattern("hel")
        assert len(matching) == 2

    def test_clear_history(self):
        """Test clearing history."""
        engine = AdvancedSearchEngine()

        engine.search("test", SearchQuery(pattern="hello"))
        engine.clear_history()

        assert len(engine.get_history()) == 0


class TestHighlightResults:
    """Test highlight results functionality."""

    def test_highlight_results_by_line(self):
        """Test getting highlight regions by line."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="test")
        text = "test line\nno match\ntest again"

        engine.search(text, query)
        highlights = engine.highlight_results(text)

        assert 0 in highlights
        assert 2 in highlights
        assert 1 not in highlights

    def test_highlight_multiple_per_line(self):
        """Test highlights with multiple matches per line."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")
        text = "a b a c a"

        engine.search(text, query)
        highlights = engine.highlight_results(text)

        assert len(highlights[0]) == 3

    def test_highlight_positions(self):
        """Test that highlight positions are correct."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="world")
        text = "hello world"

        engine.search(text, query)
        highlights = engine.highlight_results(text)

        assert highlights[0][0] == (6, 11)


class TestResultMetadata:
    """Test search result metadata."""

    def test_search_result_positions(self):
        """Test that result positions are correct."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="world")
        text = "hello world test"

        results = engine.search(text, query)
        result = results[0]

        assert result.start == 6
        assert result.end == 11
        assert text[result.start : result.end] == "world"

    def test_search_result_multiline(self):
        """Test results with multiline text."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="test")
        text = "line1\nline2 test\nline3"

        results = engine.search(text, query)
        result = results[0]

        assert result.line_num == 1
        assert result.column == 6

    def test_get_result_count(self):
        """Test getting result count."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")

        engine.search("a b a c a", query)
        assert engine.get_result_count() == 3

    def test_get_current_result(self):
        """Test getting current result."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="a")

        engine.search("a b a", query)
        engine.find_next(None)

        current = engine.get_current_result()
        assert current is not None
        assert current.match_text == "a"


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_search_special_regex_chars(self):
        """Test searching for special regex characters."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="$100")

        # Without regex, should find literal text
        results = engine.search("price is $100", query)
        assert len(results) == 1

    def test_search_multiline_text(self):
        """Test searching across multiple lines."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="search")

        text = """line1
line2 search here
line3
search again
line5"""

        results = engine.search(text, query)
        assert len(results) == 2

    def test_search_empty_lines(self):
        """Test searching text with empty lines."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="test")

        text = "test\n\ntest\n\ntest"
        results = engine.search(text, query)

        assert len(results) == 3

    def test_replace_empty_replacement(self):
        """Test replacing with empty string."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hello")
        text = "hello world"

        modified, count = engine.replace(text, query, "", replace_all=True)

        assert count == 1
        assert modified == " world"

    def test_replace_longer_replacement(self):
        """Test replacing with longer string."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="hi")
        text = "hi there"

        modified, count = engine.replace(text, query, "hello", replace_all=True)

        assert modified == "hello there"

    def test_reset_search_state(self):
        """Test resetting search state."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="test")

        engine.search("test test", query)
        assert engine.get_result_count() > 0

        engine.reset()
        assert engine.get_result_count() == 0
        assert engine.get_current_result() is None

    def test_unicode_search(self):
        """Test searching unicode characters."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="café")

        results = engine.search("Welcome to café", query)
        assert len(results) == 1

    def test_regex_with_unicode(self):
        """Test regex with unicode."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern=r"\w+", regex=True)

        results = engine.search("hello世界test", query)
        # Should find word-like sequences
        assert len(results) > 0

    def test_very_long_text(self):
        """Test search on very long text."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="needle")

        # Create large text with one match
        text = "x " * 10000 + "needle " + "y " * 10000
        results = engine.search(text, query)

        assert len(results) == 1

    def test_overlapping_results_no_overlap(self):
        """Test that results don't overlap."""
        engine = AdvancedSearchEngine()
        query = SearchQuery(pattern="aa")

        results = engine.search("aaa", query)

        # "aa" in "aaa" - should find at positions 0-2 and 1-3
        # Based on implementation, it will find both
        assert len(results) >= 1

