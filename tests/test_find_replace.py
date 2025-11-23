"""Unit tests for FindReplaceEngine."""

import pytest
from src.find_replace import FindReplaceEngine


class TestFindAll:
    """Test finding all occurrences."""

    def test_find_all_basic(self):
        """Test finding all occurrences of a term."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 2
        assert matches[0] == (0, 5)
        assert matches[1] == (12, 17)

    def test_find_all_no_match(self):
        """Test finding when no match exists."""
        engine = FindReplaceEngine()
        text = "hello world"
        matches = engine.find_all(text, "foo")

        assert matches == []

    def test_find_all_empty_search_term(self):
        """Test finding with empty search term."""
        engine = FindReplaceEngine()
        text = "hello world"
        matches = engine.find_all(text, "")

        assert matches == []

    def test_find_all_case_insensitive(self):
        """Test case insensitive find."""
        engine = FindReplaceEngine()
        text = "Hello world hello HELLO"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 3

    def test_find_all_case_sensitive(self):
        """Test case sensitive find."""
        engine = FindReplaceEngine()
        engine.set_case_sensitive(True)
        text = "Hello world hello HELLO"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 1
        assert matches[0] == (12, 17)

    def test_find_all_whole_words(self):
        """Test whole words matching."""
        engine = FindReplaceEngine()
        engine.set_whole_words(True)
        text = "hello world helloworld hello"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 2
        assert matches[0] == (0, 5)
        assert matches[1] == (23, 28)

    def test_find_all_overlapping(self):
        """Test finding overlapping matches."""
        engine = FindReplaceEngine()
        text = "aaaa"
        matches = engine.find_all(text, "aa")

        assert len(matches) == 3
        assert matches[0] == (0, 2)
        assert matches[1] == (1, 3)
        assert matches[2] == (2, 4)


class TestFindNext:
    """Test finding next occurrence."""

    def test_find_next_basic(self):
        """Test finding next occurrence."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        result = engine.find_next(text, "hello", 0)

        assert result == (0, 5)

    def test_find_next_after_first(self):
        """Test finding next after first match."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        result = engine.find_next(text, "hello", 6)

        assert result == (12, 17)

    def test_find_next_no_match(self):
        """Test finding next when no match after start."""
        engine = FindReplaceEngine()
        text = "hello world"
        result = engine.find_next(text, "hello", 10)

        assert result is None

    def test_find_next_empty_search(self):
        """Test find next with empty search."""
        engine = FindReplaceEngine()
        text = "hello world"
        result = engine.find_next(text, "", 0)

        assert result is None

    def test_find_next_case_sensitive(self):
        """Test case sensitive find next."""
        engine = FindReplaceEngine()
        engine.set_case_sensitive(True)
        text = "Hello hello Hello"
        result = engine.find_next(text, "Hello", 0)

        assert result == (0, 5)

        result = engine.find_next(text, "Hello", 6)
        assert result == (12, 17)

    def test_find_next_whole_words(self):
        """Test whole words find next."""
        engine = FindReplaceEngine()
        engine.set_whole_words(True)
        text = "hello helloworld hello"
        result = engine.find_next(text, "hello", 0)

        assert result == (0, 5)

        result = engine.find_next(text, "hello", 6)
        assert result == (17, 22)


class TestFindPrevious:
    """Test finding previous occurrence."""

    def test_find_previous_basic(self):
        """Test finding previous occurrence."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        result = engine.find_previous(text, "hello", len(text))

        assert result == (12, 17)

    def test_find_previous_before_second(self):
        """Test finding previous before second match."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        result = engine.find_previous(text, "hello", 12)

        assert result == (0, 5)

    def test_find_previous_no_match(self):
        """Test finding previous when no match before start."""
        engine = FindReplaceEngine()
        text = "hello world"
        result = engine.find_previous(text, "hello", 3)

        assert result is None

    def test_find_previous_case_sensitive(self):
        """Test case sensitive find previous."""
        engine = FindReplaceEngine()
        engine.set_case_sensitive(True)
        text = "Hello hello Hello"
        result = engine.find_previous(text, "Hello", len(text))

        assert result == (12, 17)

    def test_find_previous_whole_words(self):
        """Test whole words find previous."""
        engine = FindReplaceEngine()
        engine.set_whole_words(True)
        text = "hello helloworld hello"
        result = engine.find_previous(text, "hello", len(text))

        assert result == (17, 22)

        result = engine.find_previous(text, "hello", 17)
        assert result == (0, 5)


class TestReplace:
    """Test replacing first occurrence."""

    def test_replace_basic(self):
        """Test replacing first occurrence."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        modified, count = engine.replace(text, "hello", "goodbye")

        assert modified == "goodbye world hello"
        assert count == 1

    def test_replace_no_match(self):
        """Test replace when no match."""
        engine = FindReplaceEngine()
        text = "hello world"
        modified, count = engine.replace(text, "foo", "bar")

        assert modified == text
        assert count == 0

    def test_replace_empty_search(self):
        """Test replace with empty search."""
        engine = FindReplaceEngine()
        text = "hello world"
        modified, count = engine.replace(text, "", "bar")

        assert modified == text
        assert count == 0

    def test_replace_with_empty_replacement(self):
        """Test replace with empty replacement (delete)."""
        engine = FindReplaceEngine()
        text = "hello world"
        modified, count = engine.replace(text, "hello ", "")

        assert modified == "world"
        assert count == 1

    def test_replace_case_insensitive(self):
        """Test case insensitive replace."""
        engine = FindReplaceEngine()
        text = "Hello world"
        modified, count = engine.replace(text, "hello", "goodbye")

        assert modified == "goodbye world"
        assert count == 1

    def test_replace_case_sensitive(self):
        """Test case sensitive replace."""
        engine = FindReplaceEngine()
        engine.set_case_sensitive(True)
        text = "Hello hello world"
        modified, count = engine.replace(text, "hello", "goodbye")

        assert modified == "Hello goodbye world"
        assert count == 1


class TestReplaceAll:
    """Test replacing all occurrences."""

    def test_replace_all_basic(self):
        """Test replacing all occurrences."""
        engine = FindReplaceEngine()
        text = "hello world hello"
        modified, count = engine.replace_all(text, "hello", "goodbye")

        assert modified == "goodbye world goodbye"
        assert count == 2

    def test_replace_all_no_match(self):
        """Test replace all when no match."""
        engine = FindReplaceEngine()
        text = "hello world"
        modified, count = engine.replace_all(text, "foo", "bar")

        assert modified == text
        assert count == 0

    def test_replace_all_empty_search(self):
        """Test replace all with empty search."""
        engine = FindReplaceEngine()
        text = "hello world"
        modified, count = engine.replace_all(text, "", "bar")

        assert modified == text
        assert count == 0

    def test_replace_all_case_insensitive(self):
        """Test case insensitive replace all."""
        engine = FindReplaceEngine()
        text = "Hello world hello HELLO"
        modified, count = engine.replace_all(text, "hello", "goodbye")

        assert modified == "goodbye world goodbye goodbye"
        assert count == 3

    def test_replace_all_case_sensitive(self):
        """Test case sensitive replace all."""
        engine = FindReplaceEngine()
        engine.set_case_sensitive(True)
        text = "Hello world hello HELLO"
        modified, count = engine.replace_all(text, "hello", "goodbye")

        assert modified == "Hello world goodbye HELLO"
        assert count == 1

    def test_replace_all_with_deletion(self):
        """Test replace all with empty replacement."""
        engine = FindReplaceEngine()
        text = "a b a b a"
        modified, count = engine.replace_all(text, "a", "")

        assert modified == " b  b "
        assert count == 3

    def test_replace_all_whole_words(self):
        """Test replace all with whole words."""
        engine = FindReplaceEngine()
        engine.set_whole_words(True)
        text = "hello helloworld hello"
        modified, count = engine.replace_all(text, "hello", "goodbye")

        assert modified == "goodbye helloworld goodbye"
        assert count == 2


class TestSettings:
    """Test engine settings."""

    def test_set_case_sensitive(self):
        """Test setting case sensitivity."""
        engine = FindReplaceEngine()
        assert not engine.case_sensitive

        engine.set_case_sensitive(True)
        assert engine.case_sensitive

        engine.set_case_sensitive(False)
        assert not engine.case_sensitive

    def test_set_whole_words(self):
        """Test setting whole words."""
        engine = FindReplaceEngine()
        assert not engine.whole_words

        engine.set_whole_words(True)
        assert engine.whole_words

        engine.set_whole_words(False)
        assert not engine.whole_words


class TestEdgeCases:
    """Test edge cases."""

    def test_single_character_search(self):
        """Test searching for single character."""
        engine = FindReplaceEngine()
        text = "aaa"
        matches = engine.find_all(text, "a")

        assert len(matches) == 3

    def test_search_longer_than_text(self):
        """Test searching for term longer than text."""
        engine = FindReplaceEngine()
        text = "hi"
        matches = engine.find_all(text, "hello")

        assert matches == []

    def test_whole_word_with_punctuation(self):
        """Test whole word matching with punctuation."""
        engine = FindReplaceEngine()
        engine.set_whole_words(True)
        text = "hello, world hello. test"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 2

    def test_special_characters_in_text(self):
        """Test with special characters."""
        engine = FindReplaceEngine()
        text = "hello@world hello-test"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 2

    def test_multiline_text(self):
        """Test with multiline text."""
        engine = FindReplaceEngine()
        text = "hello\nworld\nhello\ntest"
        matches = engine.find_all(text, "hello")

        assert len(matches) == 2
        assert matches[0] == (0, 5)
        assert matches[1] == (12, 17)

    def test_unicode_text(self):
        """Test with unicode text."""
        engine = FindReplaceEngine()
        text = "café café"
        matches = engine.find_all(text, "café")

        assert len(matches) == 2

    def test_replace_with_longer_term(self):
        """Test replacing with longer term."""
        engine = FindReplaceEngine()
        text = "hi"
        modified, count = engine.replace_all(text, "hi", "hello world")

        assert modified == "hello world"
        assert count == 1
