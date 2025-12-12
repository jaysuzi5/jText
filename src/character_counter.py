"""Character counter for text analysis."""


class CharacterCounter:
    """Provides character counting and text statistics."""

    @staticmethod
    def count_characters(text: str) -> int:
        """Count total characters in text.

        Args:
            text: The text to count

        Returns:
            Total number of characters (including whitespace and newlines)
        """
        return len(text)

    @staticmethod
    def count_characters_no_whitespace(text: str) -> int:
        """Count characters excluding all whitespace.

        Args:
            text: The text to count

        Returns:
            Number of characters excluding spaces, tabs, and newlines
        """
        return len(text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", ""))

    @staticmethod
    def count_characters_no_spaces(text: str) -> int:
        """Count characters excluding only spaces (keeps tabs and newlines).

        Args:
            text: The text to count

        Returns:
            Number of characters excluding spaces only
        """
        return len(text.replace(" ", ""))

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text.

        Words are defined as sequences separated by whitespace.

        Args:
            text: The text to count

        Returns:
            Number of words
        """
        if not text.strip():
            return 0
        return len(text.split())

    @staticmethod
    def count_lines(text: str) -> int:
        """Count lines in text.

        Empty text returns 0 lines. Single line without newline returns 1.
        Each newline creates a new line.

        Args:
            text: The text to count

        Returns:
            Number of lines
        """
        if not text:
            return 0
        return text.count("\n") + 1

    @staticmethod
    def count_sentences(text: str) -> int:
        """Count sentences in text.

        Sentences are delimited by '.', '!', or '?'.

        Args:
            text: The text to count

        Returns:
            Number of sentences
        """
        if not text.strip():
            return 0

        count = 0
        for char in text:
            if char in ".!?":
                count += 1

        return count

    @staticmethod
    def count_paragraphs(text: str) -> int:
        """Count paragraphs in text.

        Paragraphs are separated by blank lines (lines containing only whitespace).

        Args:
            text: The text to count

        Returns:
            Number of paragraphs
        """
        if not text.strip():
            return 0

        # Split by double newlines (paragraph breaks)
        paragraphs = text.split("\n\n")
        # Count non-empty paragraphs
        return sum(1 for p in paragraphs if p.strip())

    @staticmethod
    def get_statistics(text: str) -> dict:
        """Get comprehensive statistics for text.

        Args:
            text: The text to analyze

        Returns:
            Dictionary with keys:
            - characters: total characters
            - characters_no_whitespace: characters excluding all whitespace
            - characters_no_spaces: characters excluding spaces only
            - words: word count
            - lines: line count
            - sentences: sentence count
            - paragraphs: paragraph count
        """
        return {
            "characters": CharacterCounter.count_characters(text),
            "characters_no_whitespace": CharacterCounter.count_characters_no_whitespace(text),
            "characters_no_spaces": CharacterCounter.count_characters_no_spaces(text),
            "words": CharacterCounter.count_words(text),
            "lines": CharacterCounter.count_lines(text),
            "sentences": CharacterCounter.count_sentences(text),
            "paragraphs": CharacterCounter.count_paragraphs(text),
        }
