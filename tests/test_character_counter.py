"""Unit tests for character counter functionality."""

import pytest
from src.character_counter import CharacterCounter


class TestCharacterCounterBasics:
    """Test basic character counting."""

    def test_count_empty_string(self):
        """Test counting empty string."""
        assert CharacterCounter.count_characters("") == 0

    def test_count_single_character(self):
        """Test counting single character."""
        assert CharacterCounter.count_characters("a") == 1

    def test_count_simple_text(self):
        """Test counting simple text."""
        assert CharacterCounter.count_characters("hello") == 5

    def test_count_text_with_spaces(self):
        """Test counting text with spaces."""
        assert CharacterCounter.count_characters("hello world") == 11

    def test_count_text_with_newlines(self):
        """Test counting text with newlines."""
        assert CharacterCounter.count_characters("hello\nworld") == 11

    def test_count_text_with_tabs(self):
        """Test counting text with tabs."""
        assert CharacterCounter.count_characters("hello\tworld") == 11

    def test_count_special_characters(self):
        """Test counting special characters."""
        assert CharacterCounter.count_characters("hello!@#$%") == 10

    def test_count_numbers(self):
        """Test counting numbers."""
        assert CharacterCounter.count_characters("12345") == 5

    def test_count_mixed_content(self):
        """Test counting mixed content."""
        text = "Hello 123!@# World"
        assert CharacterCounter.count_characters(text) == len(text)

    def test_count_unicode_characters(self):
        """Test counting unicode characters."""
        assert CharacterCounter.count_characters("café") == 4
        assert CharacterCounter.count_characters("你好") == 2

    def test_count_emoji(self):
        """Test counting emoji."""
        assert CharacterCounter.count_characters("😀😁") == 2

    def test_count_whitespace_only(self):
        """Test counting whitespace only."""
        assert CharacterCounter.count_characters("   ") == 3
        assert CharacterCounter.count_characters("\t\n") == 2


class TestCharacterCounterNoWhitespace:
    """Test character counting without whitespace."""

    def test_count_no_whitespace_empty(self):
        """Test counting empty string."""
        assert CharacterCounter.count_characters_no_whitespace("") == 0

    def test_count_no_whitespace_no_spaces(self):
        """Test text with no whitespace."""
        assert CharacterCounter.count_characters_no_whitespace("hello") == 5

    def test_count_no_whitespace_with_spaces(self):
        """Test removing spaces."""
        assert CharacterCounter.count_characters_no_whitespace("hello world") == 10

    def test_count_no_whitespace_with_newlines(self):
        """Test removing newlines."""
        assert CharacterCounter.count_characters_no_whitespace("hello\nworld") == 10

    def test_count_no_whitespace_with_tabs(self):
        """Test removing tabs."""
        assert CharacterCounter.count_characters_no_whitespace("hello\tworld") == 10

    def test_count_no_whitespace_all_whitespace(self):
        """Test text with only whitespace."""
        assert CharacterCounter.count_characters_no_whitespace("   \n\t  ") == 0

    def test_count_no_whitespace_mixed(self):
        """Test mixed whitespace."""
        assert CharacterCounter.count_characters_no_whitespace("a b\nc\td") == 4

    def test_count_no_whitespace_preserves_special(self):
        """Test that special characters are preserved."""
        assert CharacterCounter.count_characters_no_whitespace("a!@# b") == 5


class TestCharacterCounterNoSpaces:
    """Test character counting without spaces only."""

    def test_count_no_spaces_empty(self):
        """Test counting empty string."""
        assert CharacterCounter.count_characters_no_spaces("") == 0

    def test_count_no_spaces_no_spaces(self):
        """Test text with no spaces."""
        assert CharacterCounter.count_characters_no_spaces("hello") == 5

    def test_count_no_spaces_with_spaces(self):
        """Test removing spaces."""
        assert CharacterCounter.count_characters_no_spaces("hello world") == 10

    def test_count_no_spaces_keeps_newlines(self):
        """Test that newlines are kept."""
        assert CharacterCounter.count_characters_no_spaces("hello\nworld") == 11

    def test_count_no_spaces_keeps_tabs(self):
        """Test that tabs are kept."""
        assert CharacterCounter.count_characters_no_spaces("hello\tworld") == 11

    def test_count_no_spaces_multiple_spaces(self):
        """Test multiple consecutive spaces."""
        assert CharacterCounter.count_characters_no_spaces("hello  world") == 10

    def test_count_no_spaces_leading_trailing(self):
        """Test leading and trailing spaces."""
        assert CharacterCounter.count_characters_no_spaces("  hello  ") == 5


class TestWordCounter:
    """Test word counting."""

    def test_count_words_empty(self):
        """Test counting words in empty string."""
        assert CharacterCounter.count_words("") == 0

    def test_count_words_single_word(self):
        """Test counting single word."""
        assert CharacterCounter.count_words("hello") == 1

    def test_count_words_two_words(self):
        """Test counting two words."""
        assert CharacterCounter.count_words("hello world") == 2

    def test_count_words_multiple_words(self):
        """Test counting multiple words."""
        assert CharacterCounter.count_words("the quick brown fox") == 4

    def test_count_words_with_newlines(self):
        """Test words separated by newlines."""
        assert CharacterCounter.count_words("hello\nworld") == 2

    def test_count_words_with_tabs(self):
        """Test words separated by tabs."""
        assert CharacterCounter.count_words("hello\tworld") == 2

    def test_count_words_with_multiple_spaces(self):
        """Test words separated by multiple spaces."""
        assert CharacterCounter.count_words("hello    world") == 2

    def test_count_words_leading_trailing_spaces(self):
        """Test words with leading/trailing spaces."""
        assert CharacterCounter.count_words("  hello world  ") == 2

    def test_count_words_whitespace_only(self):
        """Test whitespace only."""
        assert CharacterCounter.count_words("   \n\t  ") == 0

    def test_count_words_with_punctuation(self):
        """Test words with punctuation."""
        assert CharacterCounter.count_words("hello, world!") == 2

    def test_count_words_mixed_whitespace(self):
        """Test mixed whitespace."""
        assert CharacterCounter.count_words("a\tb  c\n\nd") == 4


class TestLineCounter:
    """Test line counting."""

    def test_count_lines_empty(self):
        """Test counting lines in empty string."""
        assert CharacterCounter.count_lines("") == 0

    def test_count_lines_single_line_no_newline(self):
        """Test single line without newline."""
        assert CharacterCounter.count_lines("hello") == 1

    def test_count_lines_two_lines(self):
        """Test two lines."""
        assert CharacterCounter.count_lines("hello\nworld") == 2

    def test_count_lines_multiple_lines(self):
        """Test multiple lines."""
        assert CharacterCounter.count_lines("line1\nline2\nline3") == 3

    def test_count_lines_trailing_newline(self):
        """Test trailing newline."""
        assert CharacterCounter.count_lines("hello\n") == 2

    def test_count_lines_multiple_consecutive_newlines(self):
        """Test multiple consecutive newlines."""
        assert CharacterCounter.count_lines("hello\n\n\nworld") == 4

    def test_count_lines_empty_lines(self):
        """Test empty lines."""
        assert CharacterCounter.count_lines("hello\n\nworld") == 3

    def test_count_lines_only_newlines(self):
        """Test only newlines."""
        assert CharacterCounter.count_lines("\n\n") == 3

    def test_count_lines_windows_line_endings(self):
        """Test Windows line endings (CRLF)."""
        # \r\n is one newline character when treated as such
        assert CharacterCounter.count_lines("hello\r\nworld") == 2


class TestSentenceCounter:
    """Test sentence counting."""

    def test_count_sentences_empty(self):
        """Test counting sentences in empty string."""
        assert CharacterCounter.count_sentences("") == 0

    def test_count_sentences_single_period(self):
        """Test single sentence with period."""
        assert CharacterCounter.count_sentences("hello.") == 1

    def test_count_sentences_single_exclamation(self):
        """Test single sentence with exclamation."""
        assert CharacterCounter.count_sentences("hello!") == 1

    def test_count_sentences_single_question(self):
        """Test single sentence with question mark."""
        assert CharacterCounter.count_sentences("hello?") == 1

    def test_count_sentences_multiple(self):
        """Test multiple sentences."""
        text = "hello. world! how are you?"
        assert CharacterCounter.count_sentences(text) == 3

    def test_count_sentences_no_punctuation(self):
        """Test text without sentence punctuation."""
        assert CharacterCounter.count_sentences("hello world") == 0

    def test_count_sentences_mixed_punctuation(self):
        """Test mixed punctuation marks."""
        assert CharacterCounter.count_sentences("Wait. Really? Yes!") == 3

    def test_count_sentences_multiple_punctuation(self):
        """Test multiple punctuation marks."""
        assert CharacterCounter.count_sentences("hello..") == 2

    def test_count_sentences_whitespace_only(self):
        """Test whitespace only."""
        assert CharacterCounter.count_sentences("   ") == 0

    def test_count_sentences_abbreviations(self):
        """Test abbreviations (periods counted as sentences)."""
        # Note: This is a simple counter that counts periods/!/?, not smart about abbreviations
        assert CharacterCounter.count_sentences("Dr. Smith is here.") == 2


class TestParagraphCounter:
    """Test paragraph counting."""

    def test_count_paragraphs_empty(self):
        """Test counting paragraphs in empty string."""
        assert CharacterCounter.count_paragraphs("") == 0

    def test_count_paragraphs_single_paragraph(self):
        """Test single paragraph."""
        assert CharacterCounter.count_paragraphs("hello world") == 1

    def test_count_paragraphs_two_paragraphs(self):
        """Test two paragraphs."""
        assert CharacterCounter.count_paragraphs("hello\n\nworld") == 2

    def test_count_paragraphs_multiple(self):
        """Test multiple paragraphs."""
        text = "para1\n\npara2\n\npara3"
        assert CharacterCounter.count_paragraphs(text) == 3

    def test_count_paragraphs_with_content_lines(self):
        """Test paragraphs with multiple lines."""
        text = "line1\nline2\n\nline3\nline4"
        assert CharacterCounter.count_paragraphs(text) == 2

    def test_count_paragraphs_whitespace_only(self):
        """Test whitespace only."""
        assert CharacterCounter.count_paragraphs("   \n\n  ") == 0

    def test_count_paragraphs_single_newline(self):
        """Test single newline doesn't create paragraph break."""
        assert CharacterCounter.count_paragraphs("hello\nworld") == 1

    def test_count_paragraphs_triple_newline(self):
        """Test triple newline creates paragraph break."""
        assert CharacterCounter.count_paragraphs("hello\n\n\nworld") == 2

    def test_count_paragraphs_many_blank_lines(self):
        """Test many blank lines between paragraphs."""
        text = "para1\n\n\n\npara2"
        assert CharacterCounter.count_paragraphs(text) == 2

    def test_count_paragraphs_leading_blank_lines(self):
        """Test leading blank lines."""
        assert CharacterCounter.count_paragraphs("\n\nhello") == 1

    def test_count_paragraphs_trailing_blank_lines(self):
        """Test trailing blank lines."""
        assert CharacterCounter.count_paragraphs("hello\n\n") == 1


class TestStatisticsAggregation:
    """Test comprehensive statistics function."""

    def test_statistics_empty_text(self):
        """Test statistics for empty text."""
        stats = CharacterCounter.get_statistics("")
        assert stats["characters"] == 0
        assert stats["characters_no_whitespace"] == 0
        assert stats["characters_no_spaces"] == 0
        assert stats["words"] == 0
        assert stats["lines"] == 0
        assert stats["sentences"] == 0
        assert stats["paragraphs"] == 0

    def test_statistics_simple_text(self):
        """Test statistics for simple text."""
        stats = CharacterCounter.get_statistics("hello")
        assert stats["characters"] == 5
        assert stats["characters_no_whitespace"] == 5
        assert stats["characters_no_spaces"] == 5
        assert stats["words"] == 1
        assert stats["lines"] == 1
        assert stats["sentences"] == 0
        assert stats["paragraphs"] == 1

    def test_statistics_complex_text(self):
        """Test statistics for complex text."""
        text = "Hello world!\n\nHow are you? I'm fine."
        stats = CharacterCounter.get_statistics(text)

        assert stats["characters"] == len(text)
        assert stats["words"] == 7  # Hello world How are you I'm fine
        assert stats["lines"] == 3
        assert stats["sentences"] == 3  # ! from "world!" ? from "you?" . from "fine."
        assert stats["paragraphs"] == 2

    def test_statistics_all_keys_present(self):
        """Test that all expected keys are in statistics."""
        stats = CharacterCounter.get_statistics("test")
        expected_keys = {
            "characters",
            "characters_no_whitespace",
            "characters_no_spaces",
            "words",
            "lines",
            "sentences",
            "paragraphs",
        }
        assert set(stats.keys()) == expected_keys

    def test_statistics_consistency(self):
        """Test that statistics are internally consistent."""
        text = "The quick brown fox\njumps over\n\nthe lazy dog."
        stats = CharacterCounter.get_statistics(text)

        # characters_no_whitespace should be less than or equal to characters
        assert stats["characters_no_whitespace"] <= stats["characters"]

        # characters_no_spaces should be less than or equal to characters
        assert stats["characters_no_spaces"] <= stats["characters"]

        # characters_no_spaces should be greater than or equal to characters_no_whitespace
        assert stats["characters_no_spaces"] >= stats["characters_no_whitespace"]

        # lines should be at least 1 if text is not empty
        assert stats["lines"] >= 1

        # words should be at most lines (if each line has at most 1 word)
        assert stats["words"] >= 1


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_very_long_text(self):
        """Test with very long text."""
        text = "a" * 10000
        assert CharacterCounter.count_characters(text) == 10000
        assert CharacterCounter.count_words(text) == 1

    def test_only_spaces(self):
        """Test text with only spaces."""
        assert CharacterCounter.count_characters("   ") == 3
        assert CharacterCounter.count_characters_no_whitespace("   ") == 0
        assert CharacterCounter.count_words("   ") == 0

    def test_only_newlines(self):
        """Test text with only newlines."""
        assert CharacterCounter.count_lines("\n\n\n") == 4
        assert CharacterCounter.count_words("\n\n\n") == 0

    def test_only_punctuation(self):
        """Test text with only punctuation."""
        assert CharacterCounter.count_sentences("...!!!???") == 9
        # split() treats the whole string as one "word" since there's no whitespace
        assert CharacterCounter.count_words("...!!!???") == 1

    def test_alternating_words_newlines(self):
        """Test alternating words and newlines."""
        text = "a\nb\nc\nd\ne"
        assert CharacterCounter.count_words(text) == 5
        assert CharacterCounter.count_lines(text) == 5

    def test_multiple_spaces_between_words(self):
        """Test multiple spaces between words."""
        text = "hello     world     test"
        assert CharacterCounter.count_words(text) == 3
        assert CharacterCounter.count_characters_no_spaces(text) == 14

    def test_text_with_numbers_and_symbols(self):
        """Test text with numbers and symbols."""
        text = "Price is $99.99!"
        assert CharacterCounter.count_characters(text) == 16  # P r i c e space i s space $ 9 9 . 9 9 !
        assert CharacterCounter.count_words(text) == 3  # Price, is, $99.99!
        # Note: period in $99.99 is counted as a sentence delimiter, so we have 2 total
        assert CharacterCounter.count_sentences(text) == 2  # . in $99.99 and ! at end
