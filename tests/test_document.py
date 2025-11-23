"""Unit tests for Document model."""

import pytest
from pathlib import Path
from src.document import Document


class TestDocumentInitialization:
    """Test Document initialization."""

    def test_create_empty_document(self):
        """Test creating an empty document."""
        doc = Document()
        assert doc.content == ""
        assert doc.file_path is None
        assert not doc.is_modified

    def test_create_document_with_content(self):
        """Test creating a document with initial content."""
        content = "Hello, World!"
        doc = Document(content)
        assert doc.content == content
        assert doc.file_path is None
        assert not doc.is_modified

    def test_get_file_name_untitled(self):
        """Test getting file name for document without file path."""
        doc = Document()
        assert doc.get_file_name() == "Untitled"

    def test_get_file_name_with_path(self):
        """Test getting file name from file path."""
        doc = Document()
        doc.file_path = Path("/path/to/file.txt")
        assert doc.get_file_name() == "file.txt"


class TestDocumentContent:
    """Test Document content management."""

    def test_set_content(self):
        """Test setting document content."""
        doc = Document()
        content = "New content"
        doc.content = content
        assert doc.content == content

    def test_content_change_marks_modified(self):
        """Test that content change marks document as modified."""
        doc = Document("initial")
        assert not doc.is_modified
        doc.content = "changed"
        assert doc.is_modified

    def test_content_unchanged_after_set(self):
        """Test that setting content to same value does not mark modified."""
        doc = Document("content")
        assert not doc.is_modified
        # Setting to same content should not mark as modified
        doc.content = "content"
        assert not doc.is_modified

    def test_mark_saved(self):
        """Test marking document as saved."""
        doc = Document("initial")
        doc.content = "changed"
        assert doc.is_modified
        doc.mark_saved()
        assert not doc.is_modified

    def test_mark_saved_resets_undo_redo(self):
        """Test that mark_saved clears undo/redo stacks."""
        doc = Document("initial")
        doc.content = "changed"
        assert doc.can_undo()
        doc.mark_saved()
        assert not doc.can_undo()


class TestFilePath:
    """Test Document file path management."""

    def test_set_file_path_string(self):
        """Test setting file path with string."""
        doc = Document()
        doc.file_path = "/path/to/file.txt"
        assert isinstance(doc.file_path, Path)
        assert doc.file_path == Path("/path/to/file.txt")

    def test_set_file_path_path_object(self):
        """Test setting file path with Path object."""
        doc = Document()
        path = Path("/path/to/file.txt")
        doc.file_path = path
        assert doc.file_path == path

    def test_set_file_path_none(self):
        """Test setting file path to None."""
        doc = Document()
        doc.file_path = Path("/path/to/file.txt")
        doc.file_path = None
        assert doc.file_path is None


class TestUndoRedo:
    """Test Document undo/redo functionality."""

    def test_undo_single_change(self):
        """Test undoing a single content change."""
        doc = Document("initial")
        doc.content = "changed"
        assert doc.can_undo()
        assert doc.undo()
        assert doc.content == "initial"

    def test_undo_multiple_changes(self):
        """Test undoing multiple content changes."""
        doc = Document("v1")
        doc.content = "v2"
        doc.content = "v3"
        assert doc.undo()
        assert doc.content == "v2"
        assert doc.undo()
        assert doc.content == "v1"

    def test_undo_no_history(self):
        """Test undo when no history exists."""
        doc = Document("content")
        assert not doc.can_undo()
        assert not doc.undo()
        assert doc.content == "content"

    def test_redo_single_change(self):
        """Test redoing a single change."""
        doc = Document("v1")
        doc.content = "v2"
        doc.undo()
        assert doc.can_redo()
        assert doc.redo()
        assert doc.content == "v2"

    def test_redo_multiple_changes(self):
        """Test redoing multiple changes."""
        doc = Document("v1")
        doc.content = "v2"
        doc.content = "v3"
        doc.undo()
        doc.undo()
        assert doc.redo()
        assert doc.content == "v2"
        assert doc.redo()
        assert doc.content == "v3"

    def test_redo_no_history(self):
        """Test redo when no history exists."""
        doc = Document("content")
        assert not doc.can_redo()
        assert not doc.redo()
        assert doc.content == "content"

    def test_redo_clears_after_new_edit(self):
        """Test that new edit clears redo history."""
        doc = Document("v1")
        doc.content = "v2"
        doc.undo()
        assert doc.can_redo()
        doc.content = "v3"
        assert not doc.can_redo()
        assert doc.content == "v3"

    def test_undo_redo_sequence(self):
        """Test a complete undo/redo sequence."""
        doc = Document("v1")
        doc.content = "v2"
        doc.content = "v3"
        assert doc.undo()  # back to v2
        assert doc.undo()  # back to v1
        assert doc.redo()  # forward to v2
        assert doc.content == "v2"
        assert doc.redo()  # forward to v3
        assert doc.content == "v3"


class TestDocumentClear:
    """Test Document clearing."""

    def test_clear_document(self):
        """Test clearing all document state."""
        doc = Document("content")
        doc.file_path = Path("/path/to/file.txt")
        doc.content = "modified"
        doc.clear()
        assert doc.content == ""
        assert doc.file_path is None
        assert not doc.is_modified
        assert not doc.can_undo()
        assert not doc.can_redo()
