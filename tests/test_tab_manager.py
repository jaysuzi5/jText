"""Unit tests for TabManager."""

import pytest
from src.tab_manager import TabManager
from src.document import Document


class TestTabManagerInitialization:
    """Test TabManager initialization."""

    def test_create_empty_tab_manager(self):
        """Test creating an empty tab manager."""
        manager = TabManager()
        assert manager.get_tab_count() == 0
        assert manager.get_active_index() == -1
        assert manager.get_active_document() is None


class TestTabManagerAddTab:
    """Test adding tabs."""

    def test_add_tab_with_document(self):
        """Test adding a tab with a document."""
        manager = TabManager()
        doc = Document("content")
        index = manager.add_tab(doc)

        assert index == 0
        assert manager.get_tab_count() == 1
        assert manager.get_active_document() is doc

    def test_add_tab_without_document(self):
        """Test adding a tab creates empty document."""
        manager = TabManager()
        index = manager.add_tab()

        assert index == 0
        assert manager.get_tab_count() == 1
        doc = manager.get_active_document()
        assert doc is not None
        assert doc.content == ""

    def test_add_multiple_tabs(self):
        """Test adding multiple tabs."""
        manager = TabManager()
        doc1 = Document("content1")
        doc2 = Document("content2")
        doc3 = Document("content3")

        idx1 = manager.add_tab(doc1)
        idx2 = manager.add_tab(doc2)
        idx3 = manager.add_tab(doc3)

        assert idx1 == 0
        assert idx2 == 1
        assert idx3 == 2
        assert manager.get_tab_count() == 3
        # First added tab becomes active
        assert manager.get_active_document() is doc1

    def test_add_tab_sets_first_as_active(self):
        """Test that first tab becomes active."""
        manager = TabManager()
        doc = Document()
        manager.add_tab(doc)

        assert manager.get_active_index() == 0
        assert manager.get_active_document() is doc


class TestTabManagerCloseTab:
    """Test closing tabs."""

    def test_close_tab_with_multiple_tabs(self):
        """Test closing a tab when multiple tabs exist."""
        manager = TabManager()
        doc1 = Document("content1")
        doc2 = Document("content2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert manager.close_tab(0)
        assert manager.get_tab_count() == 1
        assert manager.get_active_document() is doc2

    def test_close_single_tab_fails(self):
        """Test that closing the only tab fails."""
        manager = TabManager()
        manager.add_tab(Document())

        assert not manager.close_tab(0)
        assert manager.get_tab_count() == 1

    def test_close_tab_invalid_index(self):
        """Test closing with invalid index."""
        manager = TabManager()
        manager.add_tab(Document())

        assert not manager.close_tab(5)
        assert manager.get_tab_count() == 1

    def test_close_tab_adjusts_active_index(self):
        """Test that closing tab adjusts active index correctly."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.set_active_tab(2)  # Active is doc3

        manager.close_tab(2)  # Close active tab

        assert manager.get_tab_count() == 2
        assert manager.get_active_index() == 1
        assert manager.get_active_document() is doc2

    def test_close_tab_middle(self):
        """Test closing a tab in the middle."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.close_tab(1)

        assert manager.get_tab_count() == 2
        assert manager.get_document(0) is doc1
        assert manager.get_document(1) is doc3


class TestTabManagerSetActiveTab:
    """Test setting active tab."""

    def test_set_active_tab(self):
        """Test setting the active tab."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert manager.set_active_tab(1)
        assert manager.get_active_index() == 1
        assert manager.get_active_document() is doc2

    def test_set_active_tab_invalid_index(self):
        """Test setting active tab with invalid index."""
        manager = TabManager()
        manager.add_tab(Document())

        assert not manager.set_active_tab(5)
        assert manager.get_active_index() == 0

    def test_set_active_tab_negative_index(self):
        """Test setting active tab with negative index."""
        manager = TabManager()
        manager.add_tab(Document())

        assert not manager.set_active_tab(-1)


class TestTabManagerGetDocument:
    """Test getting documents."""

    def test_get_document_by_index(self):
        """Test getting a document by index."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert manager.get_document(0) is doc1
        assert manager.get_document(1) is doc2

    def test_get_document_invalid_index(self):
        """Test getting document with invalid index."""
        manager = TabManager()
        manager.add_tab(Document())

        assert manager.get_document(5) is None

    def test_get_all_documents(self):
        """Test getting all documents."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        docs = manager.get_all_documents()
        assert len(docs) == 3
        assert docs[0] is doc1
        assert docs[1] is doc2
        assert docs[2] is doc3

    def test_get_all_documents_is_copy(self):
        """Test that get_all_documents returns a copy."""
        manager = TabManager()
        manager.add_tab(Document())

        docs1 = manager.get_all_documents()
        docs1.clear()

        docs2 = manager.get_all_documents()
        assert len(docs2) == 1


class TestTabManagerUnsavedChanges:
    """Test unsaved changes detection."""

    def test_has_unsaved_changes_no_changes(self):
        """Test has_unsaved_changes when all saved."""
        manager = TabManager()
        doc = Document("content")
        manager.add_tab(doc)

        assert not manager.has_unsaved_changes()

    def test_has_unsaved_changes_with_changes(self):
        """Test has_unsaved_changes when document modified."""
        manager = TabManager()
        doc = Document("content")
        manager.add_tab(doc)

        doc.content = "modified"

        assert manager.has_unsaved_changes()

    def test_has_unsaved_changes_multiple_tabs(self):
        """Test has_unsaved_changes with multiple tabs."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert not manager.has_unsaved_changes()

        doc2.content = "modified"

        assert manager.has_unsaved_changes()

    def test_has_unsaved_changes_one_tab_saved(self):
        """Test has_unsaved_changes with mixed save states."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        doc1.content = "modified"
        doc2.mark_saved()

        assert manager.has_unsaved_changes()


class TestTabManagerClear:
    """Test clearing tab manager."""

    def test_clear_tab_manager(self):
        """Test clearing all tabs."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        manager.clear()

        assert manager.get_tab_count() == 0
        assert manager.get_active_index() == -1
        assert manager.get_active_document() is None


class TestTabManagerEdgeCases:
    """Test edge cases."""

    def test_close_and_reopen_tabs(self):
        """Test closing and reopening tabs."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.close_tab(0)
        manager.add_tab(Document("3"))

        assert manager.get_tab_count() == 2
        assert manager.get_active_index() == 0

    def test_close_active_tab_switches_to_previous(self):
        """Test that closing active tab switches to previous."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.set_active_tab(2)
        manager.close_tab(2)

        assert manager.get_active_index() == 1
        assert manager.get_active_document() is doc2
