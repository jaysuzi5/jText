"""Unit tests for tab reordering functionality (drag-and-drop)."""

import pytest
from src.tab_manager import TabManager
from src.document import Document


class TestTabManagerSwapTabs:
    """Test swapping tabs."""

    def test_swap_two_adjacent_tabs(self):
        """Test swapping two adjacent tabs."""
        manager = TabManager()
        doc1 = Document("content1")
        doc2 = Document("content2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert manager.swap_tabs(0, 1)
        assert manager.get_document(0) is doc2
        assert manager.get_document(1) is doc1

    def test_swap_tabs_maintains_active_index(self):
        """Test that swapping updates active tab index correctly."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.set_active_tab(0)

        manager.swap_tabs(0, 2)

        assert manager.get_active_index() == 2
        assert manager.get_active_document() is doc1

    def test_swap_tabs_when_second_is_active(self):
        """Test swapping when the second tab is active."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        manager.set_active_tab(1)

        manager.swap_tabs(0, 1)

        assert manager.get_active_index() == 0
        assert manager.get_active_document() is doc2

    def test_swap_same_index_returns_true(self):
        """Test swapping tab with itself returns true."""
        manager = TabManager()
        doc = Document("content")
        manager.add_tab(doc)

        assert manager.swap_tabs(0, 0)
        assert manager.get_document(0) is doc
        assert manager.get_active_index() == 0

    def test_swap_invalid_from_index(self):
        """Test swapping with invalid from_index."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        assert not manager.swap_tabs(5, 0)

    def test_swap_invalid_to_index(self):
        """Test swapping with invalid to_index."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        assert not manager.swap_tabs(0, 5)

    def test_swap_negative_indices(self):
        """Test swapping with negative indices."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        assert not manager.swap_tabs(-1, 0)
        assert not manager.swap_tabs(0, -1)

    def test_swap_multiple_tabs_in_sequence(self):
        """Test multiple swap operations."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        # Swap 0 and 1
        manager.swap_tabs(0, 1)
        assert manager.get_document(0) is doc2
        assert manager.get_document(1) is doc1
        assert manager.get_document(2) is doc3

        # Swap 1 and 2
        manager.swap_tabs(1, 2)
        assert manager.get_document(0) is doc2
        assert manager.get_document(1) is doc3
        assert manager.get_document(2) is doc1


class TestTabManagerReorderTab:
    """Test reordering tabs via drag-and-drop."""

    def test_reorder_tab_move_right(self):
        """Test moving a tab to the right."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        assert manager.reorder_tab(0, 2)
        assert manager.get_document(0) is doc2
        assert manager.get_document(1) is doc3
        assert manager.get_document(2) is doc1

    def test_reorder_tab_move_left(self):
        """Test moving a tab to the left."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        assert manager.reorder_tab(2, 0)
        assert manager.get_document(0) is doc3
        assert manager.get_document(1) is doc1
        assert manager.get_document(2) is doc2

    def test_reorder_tab_move_to_adjacent_right(self):
        """Test moving a tab to the adjacent position on right."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert manager.reorder_tab(0, 1)
        assert manager.get_document(0) is doc2
        assert manager.get_document(1) is doc1

    def test_reorder_tab_move_to_adjacent_left(self):
        """Test moving a tab to the adjacent position on left."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        assert manager.reorder_tab(1, 0)
        assert manager.get_document(0) is doc2
        assert manager.get_document(1) is doc1

    def test_reorder_tab_same_position_returns_true(self):
        """Test reordering to same position returns true."""
        manager = TabManager()
        doc = Document("content")
        manager.add_tab(doc)

        assert manager.reorder_tab(0, 0)
        assert manager.get_document(0) is doc

    def test_reorder_tab_invalid_from_index(self):
        """Test reordering with invalid from_index."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        assert not manager.reorder_tab(5, 0)

    def test_reorder_tab_invalid_to_index(self):
        """Test reordering with invalid to_index."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        assert not manager.reorder_tab(0, 5)

    def test_reorder_tab_negative_indices(self):
        """Test reordering with negative indices."""
        manager = TabManager()
        manager.add_tab(Document())
        manager.add_tab(Document())

        assert not manager.reorder_tab(-1, 0)
        assert not manager.reorder_tab(0, -1)

    def test_reorder_tab_updates_active_index_when_dragged(self):
        """Test that active index is updated when active tab is reordered."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.set_active_tab(0)

        # Move active tab from 0 to 2
        manager.reorder_tab(0, 2)

        assert manager.get_active_index() == 2
        assert manager.get_active_document() is doc1

    def test_reorder_tab_updates_active_index_when_moving_right(self):
        """Test active index update when other tabs move right past it."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.set_active_tab(1)

        # Move tab 0 to position 2 (doc2 should shift left)
        manager.reorder_tab(0, 2)

        assert manager.get_active_index() == 0
        assert manager.get_active_document() is doc2

    def test_reorder_tab_updates_active_index_when_moving_left(self):
        """Test active index update when other tabs move left past it."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.set_active_tab(1)

        # Move tab 2 to position 0 (doc2 should shift right)
        manager.reorder_tab(2, 0)

        assert manager.get_active_index() == 2
        assert manager.get_active_document() is doc2

    def test_reorder_tab_multiple_reorders_in_sequence(self):
        """Test multiple reorder operations."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")
        doc3 = Document("3")
        doc4 = Document("4")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)
        manager.add_tab(doc4)

        # Move doc1 to end
        manager.reorder_tab(0, 3)
        assert manager.get_document(3) is doc1

        # Move doc3 to beginning
        manager.reorder_tab(1, 0)
        assert manager.get_document(0) is doc3

        # Verify order
        docs = manager.get_all_documents()
        assert docs == [doc3, doc2, doc4, doc1]

    def test_reorder_tab_with_unsaved_documents(self):
        """Test reordering preserves modified state of documents."""
        manager = TabManager()
        doc1 = Document("1")
        doc2 = Document("2")

        manager.add_tab(doc1)
        manager.add_tab(doc2)

        # Modify first document
        doc1.content = "modified"
        assert doc1.is_modified

        manager.reorder_tab(0, 1)

        # Document should still be modified
        assert manager.get_document(1).is_modified
        assert manager.get_document(1) is doc1


class TestTabManagerReorderEdgeCases:
    """Test edge cases in reordering."""

    def test_reorder_single_tab_to_itself(self):
        """Test reordering single tab to itself."""
        manager = TabManager()
        doc = Document("content")
        manager.add_tab(doc)

        assert manager.reorder_tab(0, 0)
        assert manager.get_document(0) is doc

    def test_swap_single_tab_to_itself(self):
        """Test swapping single tab with itself."""
        manager = TabManager()
        doc = Document("content")
        manager.add_tab(doc)

        assert manager.swap_tabs(0, 0)
        assert manager.get_document(0) is doc

    def test_reorder_and_swap_comparison(self):
        """Test that adjacent reorder and swap produce same result."""
        manager1 = TabManager()
        manager2 = TabManager()

        doc_a1 = Document("a")
        doc_b1 = Document("b")
        doc_a2 = Document("a")
        doc_b2 = Document("b")

        manager1.add_tab(doc_a1)
        manager1.add_tab(doc_b1)

        manager2.add_tab(doc_a2)
        manager2.add_tab(doc_b2)

        # Use reorder on manager1
        manager1.reorder_tab(0, 1)

        # Use swap on manager2
        manager2.swap_tabs(0, 1)

        assert manager1.get_document(0) is doc_b1
        assert manager1.get_document(1) is doc_a1

        assert manager2.get_document(0) is doc_b2
        assert manager2.get_document(1) is doc_a2

    def test_reorder_maintains_document_integrity(self):
        """Test that reordering doesn't corrupt documents."""
        manager = TabManager()
        doc1 = Document("content1")
        doc2 = Document("content2")
        doc3 = Document("content3")

        manager.add_tab(doc1)
        manager.add_tab(doc2)
        manager.add_tab(doc3)

        manager.reorder_tab(1, 0)

        # Verify documents are intact
        assert manager.get_document(0) is doc2
        assert manager.get_document(0).content == "content2"

        assert manager.get_document(1) is doc1
        assert manager.get_document(1).content == "content1"

        assert manager.get_document(2) is doc3
        assert manager.get_document(2).content == "content3"

    def test_reorder_with_many_tabs(self):
        """Test reordering works with many tabs."""
        manager = TabManager()
        docs = [Document(f"content{i}") for i in range(10)]

        for doc in docs:
            manager.add_tab(doc)

        # Move first tab to end
        manager.reorder_tab(0, 9)

        # Verify first tab is now at end
        assert manager.get_document(9) is docs[0]
        assert manager.get_document(0) is docs[1]

        # Move last tab to beginning
        manager.reorder_tab(9, 0)

        # This moves the document that was at index 9 to index 0
        assert manager.get_document(0) is docs[0]
        assert manager.get_document(1) is docs[1]
