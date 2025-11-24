"""Unit tests for snippet manager."""

import pytest
import json
import tempfile
from pathlib import Path
from src.snippet_manager import SnippetManager, Snippet


class TestSnippet:
    """Test Snippet dataclass."""

    def test_create_snippet(self):
        """Test creating a snippet."""
        snippet = Snippet(name="test", title="Test Snippet", content="test content")
        assert snippet.name == "test"
        assert snippet.title == "Test Snippet"
        assert snippet.content == "test content"

    def test_snippet_with_all_options(self):
        """Test creating snippet with all options."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="content",
            language="python",
            description="A test snippet",
            shortcut="Ctrl+T",
            tags=["test", "example"],
            custom=True,
        )
        assert snippet.language == "python"
        assert snippet.description == "A test snippet"
        assert snippet.shortcut == "Ctrl+T"
        assert "test" in snippet.tags

    def test_snippet_has_placeholder(self):
        """Test detecting placeholders in snippet."""
        snippet1 = Snippet(name="t1", title="T1", content="hello ${name}")
        assert snippet1.has_placeholder()

        snippet2 = Snippet(name="t2", title="T2", content="hello world")
        assert not snippet2.has_placeholder()

    def test_snippet_get_placeholders(self):
        """Test extracting placeholders."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="hello ${name}, age ${age}",
        )
        placeholders = snippet.get_placeholders()
        assert "name" in placeholders
        assert "age" in placeholders

    def test_snippet_expand_basic(self):
        """Test expanding snippet without placeholders."""
        snippet = Snippet(name="test", title="Test", content="hello world")
        expanded = snippet.expand()
        assert expanded == "hello world"

    def test_snippet_expand_with_replacements(self):
        """Test expanding snippet with replacements."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="hello ${name}, you are ${age} years old",
        )
        expanded = snippet.expand({"name": "Alice", "age": "30"})
        assert "Alice" in expanded
        assert "30" in expanded

    def test_snippet_expand_partial_replacements(self):
        """Test expanding with partial replacements."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="hello ${name}, age ${age}",
        )
        expanded = snippet.expand({"name": "Bob"})
        assert "Bob" in expanded
        assert "${age}" in expanded


class TestSnippetManagerBasic:
    """Test basic snippet manager functionality."""

    def test_create_manager(self):
        """Test creating snippet manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            assert manager is not None

    def test_builtin_snippets_loaded(self):
        """Test that built-in snippets are loaded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            snippets = manager.get_all_snippets()
            assert len(snippets) > 0

    def test_has_python_snippets(self):
        """Test that Python snippets are available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            py_snippets = manager.get_snippets_by_language("python")
            assert len(py_snippets) > 0

    def test_has_javascript_snippets(self):
        """Test that JavaScript snippets are available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            js_snippets = manager.get_snippets_by_language("javascript")
            assert len(js_snippets) > 0


class TestSnippetOperations:
    """Test snippet operations."""

    def test_get_snippet(self):
        """Test getting a snippet by name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            snippet = manager.get_snippet("py_if")
            assert snippet is not None
            assert snippet.name == "py_if"

    def test_get_nonexistent_snippet(self):
        """Test getting non-existent snippet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            snippet = manager.get_snippet("nonexistent")
            assert snippet is None

    def test_add_custom_snippet(self):
        """Test adding a custom snippet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            custom = Snippet(
                name="custom_test",
                title="Custom Test",
                content="custom content",
            )
            manager.add_snippet(custom)
            retrieved = manager.get_snippet("custom_test")
            assert retrieved is not None
            assert retrieved.custom

    def test_remove_custom_snippet(self):
        """Test removing a custom snippet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            custom = Snippet(
                name="to_remove",
                title="Remove",
                content="content",
            )
            manager.add_snippet(custom)
            removed = manager.remove_snippet("to_remove")
            assert removed
            assert manager.get_snippet("to_remove") is None

    def test_cannot_remove_builtin(self):
        """Test that built-in snippets cannot be removed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            removed = manager.remove_snippet("py_if")
            assert not removed

    def test_update_snippet(self):
        """Test updating a snippet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            custom = Snippet(
                name="update_test",
                title="Update",
                content="original",
            )
            manager.add_snippet(custom)

            updated = Snippet(
                name="update_test",
                title="Update",
                content="modified",
            )
            manager.add_snippet(updated)

            retrieved = manager.get_snippet("update_test")
            assert retrieved.content == "modified"


class TestSnippetSearch:
    """Test snippet search functionality."""

    def test_search_by_name(self):
        """Test searching snippets by name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            results = manager.search_snippets("py_if")
            assert len(results) > 0
            assert any(s.name == "py_if" for s in results)

    def test_search_by_title(self):
        """Test searching snippets by title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            results = manager.search_snippets("function")
            assert len(results) > 0

    def test_search_case_insensitive(self):
        """Test search is case insensitive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            results1 = manager.search_snippets("PYTHON")
            results2 = manager.search_snippets("python")
            assert len(results1) == len(results2)

    def test_search_no_results(self):
        """Test search with no results."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            results = manager.search_snippets("nonexistent_xyz")
            assert len(results) == 0


class TestSnippetFiltering:
    """Test snippet filtering."""

    def test_get_snippets_by_language(self):
        """Test filtering by language."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            py_snippets = manager.get_snippets_by_language("python")
            assert all(s.language in ("python", "text") for s in py_snippets)

    def test_get_snippets_by_tag(self):
        """Test filtering by tag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            loop_snippets = manager.get_snippets_by_tag("loop")
            assert len(loop_snippets) > 0

    def test_get_languages(self):
        """Test getting list of languages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            languages = manager.get_languages()
            assert "python" in languages
            assert "javascript" in languages

    def test_get_tags(self):
        """Test getting list of tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            tags = manager.get_tags()
            assert "python" in tags or len(tags) > 0


class TestSnippetUsage:
    """Test snippet usage tracking."""

    def test_use_snippet(self):
        """Test using a snippet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            content = manager.use_snippet("py_if")
            assert content is not None
            assert "condition" in content

    def test_use_nonexistent_snippet(self):
        """Test using non-existent snippet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            content = manager.use_snippet("nonexistent")
            assert content is None

    def test_snippet_usage_count(self):
        """Test usage count tracking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            snippet = manager.get_snippet("py_if")
            original_count = snippet.usage_count

            manager.use_snippet("py_if")
            snippet = manager.get_snippet("py_if")
            assert snippet.usage_count == original_count + 1

    def test_use_snippet_with_replacements(self):
        """Test using snippet with replacements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            content = manager.use_snippet("py_if", {"condition": "x > 5"})
            assert "x > 5" in content

    def test_get_top_used_snippets(self):
        """Test getting top used snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)

            # Use some snippets
            manager.use_snippet("py_if")
            manager.use_snippet("py_if")
            manager.use_snippet("py_for")

            top_used = manager.get_top_used_snippets(5)
            assert len(top_used) > 0

    def test_get_recent_snippets(self):
        """Test getting recent snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)

            custom = Snippet(
                name="recent_test",
                title="Recent",
                content="content",
            )
            manager.add_snippet(custom)

            recent = manager.get_recent_snippets(5)
            assert len(recent) > 0


class TestSnippetPersistence:
    """Test snippet persistence."""

    def test_save_and_load_custom_snippets(self):
        """Test saving and loading custom snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create and save
            manager1 = SnippetManager(tmpdir)
            custom = Snippet(
                name="persist_test",
                title="Persist",
                content="persisted content",
            )
            manager1.add_snippet(custom)

            # Load in new manager
            manager2 = SnippetManager(tmpdir)
            retrieved = manager2.get_snippet("persist_test")
            assert retrieved is not None
            assert retrieved.content == "persisted content"

    def test_custom_snippets_file_created(self):
        """Test that custom snippets file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            custom = Snippet(
                name="file_test",
                title="File",
                content="content",
            )
            manager.add_snippet(custom)

            snippets_file = Path(tmpdir) / "snippets.json"
            assert snippets_file.exists()


class TestSnippetExportImport:
    """Test snippet export and import."""

    def test_export_custom_snippets(self):
        """Test exporting custom snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            custom = Snippet(
                name="export_test",
                title="Export",
                content="export content",
            )
            manager.add_snippet(custom)

            export_file = Path(tmpdir) / "export.json"
            success = manager.export_snippets(str(export_file), custom_only=True)
            assert success
            assert export_file.exists()

    def test_export_all_snippets(self):
        """Test exporting all snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            export_file = Path(tmpdir) / "all.json"
            success = manager.export_snippets(str(export_file), custom_only=False)
            assert success
            assert export_file.exists()

    def test_import_snippets(self):
        """Test importing snippets."""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                # Create and export
                manager1 = SnippetManager(tmpdir1)
                custom = Snippet(
                    name="import_test",
                    title="Import",
                    content="import content",
                )
                manager1.add_snippet(custom)

                export_file = Path(tmpdir1) / "export.json"
                manager1.export_snippets(str(export_file))

                # Import
                manager2 = SnippetManager(tmpdir2)
                imported, skipped = manager2.import_snippets(str(export_file))
                assert imported > 0
                assert manager2.get_snippet("import_test") is not None

    def test_import_with_overwrite(self):
        """Test importing with overwrite option."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)

            custom1 = Snippet(
                name="overwrite_test",
                title="Original",
                content="original",
            )
            manager.add_snippet(custom1)

            # Create import data
            import_data = {
                "snippets": [
                    {
                        "name": "overwrite_test",
                        "title": "Updated",
                        "content": "updated",
                        "language": "text",
                        "description": "",
                        "shortcut": None,
                        "tags": [],
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00",
                        "usage_count": 0,
                        "custom": True,
                    }
                ],
                "version": "1.0",
            }

            import_file = Path(tmpdir) / "import.json"
            with open(import_file, "w") as f:
                json.dump(import_data, f)

            # Import with overwrite
            imported, skipped = manager.import_snippets(str(import_file), overwrite=True)
            assert imported > 0


class TestSnippetStatistics:
    """Test snippet statistics."""

    def test_get_statistics(self):
        """Test getting statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)
            stats = manager.get_statistics()

            assert "total_snippets" in stats
            assert "custom_snippets" in stats
            assert "builtin_snippets" in stats
            assert stats["total_snippets"] > 0

    def test_clear_usage_stats(self):
        """Test clearing usage statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)

            # Use a snippet
            manager.use_snippet("py_if")
            snippet = manager.get_snippet("py_if")
            assert snippet.usage_count > 0

            # Clear stats
            manager.clear_usage_stats()
            snippet = manager.get_snippet("py_if")
            assert snippet.usage_count == 0


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_placeholder(self):
        """Test snippet with empty placeholder."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="hello ${}",
        )
        expanded = snippet.expand({"": "value"})
        assert "${}" in expanded or "value" in expanded

    def test_multiple_same_placeholder(self):
        """Test snippet with same placeholder multiple times."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="${name} and ${name}",
        )
        expanded = snippet.expand({"name": "Alice"})
        assert expanded.count("Alice") == 2

    def test_nested_placeholders(self):
        """Test searching for nested placeholders."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="hello ${name}${suffix}",
        )
        placeholders = snippet.get_placeholders()
        assert "name" in placeholders
        assert "suffix" in placeholders

    def test_special_chars_in_replacement(self):
        """Test replacement with special characters."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="code: ${code}",
        )
        expanded = snippet.expand({"code": "a.b*c+d"})
        assert "a.b*c+d" in expanded

    def test_unicode_in_snippet(self):
        """Test snippets with unicode."""
        snippet = Snippet(
            name="test",
            title="Test",
            content="hello ${name}, 你好",
        )
        expanded = snippet.expand({"name": "世界"})
        assert "世界" in expanded
        assert "你好" in expanded

    def test_very_long_snippet_content(self):
        """Test snippet with very long content."""
        long_content = "line\n" * 1000
        snippet = Snippet(
            name="test",
            title="Test",
            content=long_content,
        )
        # "line\n" is 5 chars, 1000 times = 5000 chars
        assert len(snippet.content) >= 5000

    def test_many_snippets(self):
        """Test manager with many snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SnippetManager(tmpdir)

            for i in range(100):
                custom = Snippet(
                    name=f"custom_{i}",
                    title=f"Custom {i}",
                    content=f"content {i}",
                )
                manager.add_snippet(custom)

            all_snippets = manager.get_all_snippets()
            assert len(all_snippets) >= 100

