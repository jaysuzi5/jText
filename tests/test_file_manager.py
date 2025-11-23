"""Unit tests for FileManager."""

import pytest
import tempfile
from pathlib import Path
from src.file_manager import FileManager
from src.document import Document


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestFileManagerOpen:
    """Test FileManager file opening functionality."""

    def test_open_existing_file(self, temp_dir):
        """Test opening an existing file."""
        test_file = temp_dir / "test.txt"
        content = "Hello, World!"
        test_file.write_text(content, encoding="utf-8")

        doc = FileManager.open_file(test_file)
        assert doc.content == content
        assert doc.file_path == test_file
        assert not doc.is_modified

    def test_open_file_with_string_path(self, temp_dir):
        """Test opening file with string path."""
        test_file = temp_dir / "test.txt"
        content = "Test content"
        test_file.write_text(content, encoding="utf-8")

        doc = FileManager.open_file(str(test_file))
        assert doc.content == content
        assert doc.file_path == test_file

    def test_open_nonexistent_file(self, temp_dir):
        """Test opening a file that doesn't exist."""
        nonexistent = temp_dir / "nonexistent.txt"
        with pytest.raises(FileNotFoundError):
            FileManager.open_file(nonexistent)

    def test_open_file_with_special_characters(self, temp_dir):
        """Test opening file with special characters in content."""
        test_file = temp_dir / "special.txt"
        content = "Special chars: éàü\nNewlines\tTabs"
        test_file.write_text(content, encoding="utf-8")

        doc = FileManager.open_file(test_file)
        assert doc.content == content

    def test_open_empty_file(self, temp_dir):
        """Test opening an empty file."""
        test_file = temp_dir / "empty.txt"
        test_file.write_text("", encoding="utf-8")

        doc = FileManager.open_file(test_file)
        assert doc.content == ""
        assert not doc.is_modified

    def test_open_file_marks_not_modified(self, temp_dir):
        """Test that opened file is not marked as modified."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        doc = FileManager.open_file(test_file)
        assert not doc.is_modified
        assert not doc.can_undo()


class TestFileManagerSave:
    """Test FileManager file saving functionality."""

    def test_save_new_document(self, temp_dir):
        """Test saving a new document to a file."""
        doc = Document("Test content")
        test_file = temp_dir / "new.txt"

        saved_path = FileManager.save_file(doc, test_file)
        assert saved_path == test_file
        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == "Test content"

    def test_save_document_with_path(self, temp_dir):
        """Test saving document that already has a path."""
        test_file = temp_dir / "test.txt"
        doc = Document("original")
        doc.file_path = test_file
        doc.content = "modified"

        saved_path = FileManager.save_file(doc)
        assert saved_path == test_file
        assert test_file.read_text(encoding="utf-8") == "modified"

    def test_save_without_path_raises_error(self):
        """Test saving document without a path raises error."""
        doc = Document("content")
        with pytest.raises(ValueError, match="No file path provided"):
            FileManager.save_file(doc)

    def test_save_creates_parent_directories(self, temp_dir):
        """Test that save creates parent directories if needed."""
        nested_file = temp_dir / "subdir1" / "subdir2" / "file.txt"
        doc = Document("content")

        saved_path = FileManager.save_file(doc, nested_file)
        assert nested_file.exists()
        assert nested_file.read_text(encoding="utf-8") == "content"

    def test_save_marks_document_not_modified(self, temp_dir):
        """Test that save marks document as not modified."""
        doc = Document("content")
        test_file = temp_dir / "test.txt"

        FileManager.save_file(doc, test_file)
        assert not doc.is_modified

    def test_save_clears_undo_redo(self, temp_dir):
        """Test that save clears undo/redo history."""
        doc = Document("v1")
        doc.content = "v2"
        test_file = temp_dir / "test.txt"

        FileManager.save_file(doc, test_file)
        assert not doc.can_undo()
        assert not doc.can_redo()

    def test_save_overwrites_existing_file(self, temp_dir):
        """Test that save overwrites existing file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("old content", encoding="utf-8")

        doc = Document("new content")
        FileManager.save_file(doc, test_file)

        assert test_file.read_text(encoding="utf-8") == "new content"

    def test_save_with_special_characters(self, temp_dir):
        """Test saving content with special characters."""
        content = "Special: éàü\nNewline\tTab"
        doc = Document(content)
        test_file = temp_dir / "special.txt"

        FileManager.save_file(doc, test_file)
        assert test_file.read_text(encoding="utf-8") == content


class TestFileManagerSaveAs:
    """Test FileManager Save As functionality."""

    def test_save_as_new_path(self, temp_dir):
        """Test save as with new file path."""
        doc = Document("content")
        original_file = temp_dir / "original.txt"
        new_file = temp_dir / "new.txt"

        FileManager.save_as(doc, original_file)
        assert doc.file_path == original_file

        FileManager.save_as(doc, new_file)
        assert doc.file_path == new_file
        assert new_file.exists()
        assert new_file.read_text(encoding="utf-8") == "content"

    def test_save_as_updates_document_path(self, temp_dir):
        """Test that save as updates the document's file path."""
        doc = Document("content")
        new_file = temp_dir / "new.txt"

        FileManager.save_as(doc, new_file)
        assert doc.file_path == new_file


class TestFileManagerCreateNew:
    """Test FileManager new document creation."""

    def test_create_new_document(self):
        """Test creating a new empty document."""
        doc = FileManager.create_new_document()
        assert doc.content == ""
        assert doc.file_path is None
        assert not doc.is_modified

    def test_create_new_document_independence(self):
        """Test that multiple new documents are independent."""
        doc1 = FileManager.create_new_document()
        doc2 = FileManager.create_new_document()

        doc1.content = "content1"
        assert doc2.content == ""


class TestFileManagerExtension:
    """Test FileManager file extension handling."""

    def test_get_file_extension(self):
        """Test getting file extension."""
        assert FileManager.get_file_extension("file.txt") == "txt"
        assert FileManager.get_file_extension("document.json") == "json"
        assert FileManager.get_file_extension("archive.tar.gz") == "gz"

    def test_get_file_extension_no_extension(self):
        """Test getting extension for file without extension."""
        assert FileManager.get_file_extension("README") == ""

    def test_get_file_extension_with_path(self):
        """Test getting extension from full path."""
        assert FileManager.get_file_extension("/path/to/file.txt") == "txt"
        assert FileManager.get_file_extension("path/to/file.json") == "json"


class TestFileManagerRoundTrip:
    """Test round-trip file operations."""

    def test_open_save_open_preserves_content(self, temp_dir):
        """Test that content is preserved through open-save-open cycle."""
        original_content = "Line 1\nLine 2\nLine 3"
        test_file = temp_dir / "test.txt"

        # Create initial file
        test_file.write_text(original_content, encoding="utf-8")

        # Open, modify, and save
        doc = FileManager.open_file(test_file)
        doc.content = "Modified\nContent"
        FileManager.save_file(doc)

        # Open again and verify
        doc2 = FileManager.open_file(test_file)
        assert doc2.content == "Modified\nContent"
        assert not doc2.is_modified


class TestFileManagerErrorHandling:
    """Test FileManager error handling."""

    def test_open_unreadable_file(self, temp_dir):
        """Test opening a file with read permission denied."""
        test_file = temp_dir / "unreadable.txt"
        test_file.write_text("content", encoding="utf-8")

        # Make file unreadable
        import os

        os.chmod(test_file, 0o000)

        try:
            with pytest.raises(IOError):
                FileManager.open_file(test_file)
        finally:
            # Restore permissions for cleanup
            os.chmod(test_file, 0o644)

    def test_save_to_unwritable_directory(self, temp_dir):
        """Test saving to a directory with no write permission."""
        import os

        restricted_dir = temp_dir / "restricted"
        restricted_dir.mkdir()

        # Remove write permission
        os.chmod(restricted_dir, 0o555)

        doc = Document("content")

        try:
            with pytest.raises(IOError):
                FileManager.save_file(doc, restricted_dir / "file.txt")
        finally:
            # Restore permissions for cleanup
            os.chmod(restricted_dir, 0o755)
