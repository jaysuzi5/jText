"""Unit tests for RecentFilesManager."""

import pytest
import tempfile
import json
from pathlib import Path
from src.recent_files_manager import RecentFilesManager


@pytest.fixture
def temp_config_dir():
    """Create a temporary config directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_files():
    """Create temporary files for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        files = [
            temp_dir / "file1.txt",
            temp_dir / "file2.txt",
            temp_dir / "file3.txt",
            temp_dir / "file4.txt",
        ]
        for f in files:
            f.write_text("content")
        yield files


class TestRecentFilesManagerInitialization:
    """Test initialization of RecentFilesManager."""

    def test_create_with_custom_config_dir(self, temp_config_dir):
        """Test creating manager with custom config directory."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        assert manager.get_recent_files() == []

    def test_custom_max_files(self, temp_config_dir):
        """Test creating manager with custom max files."""
        manager = RecentFilesManager(config_dir=temp_config_dir, max_files=5)
        assert manager.max_files == 5


class TestRecentFilesManagerAddFile:
    """Test adding files to recent list."""

    def test_add_single_file(self, temp_config_dir, temp_files):
        """Test adding a single file."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])

        recent = manager.get_recent_files()
        assert len(recent) == 1
        assert recent[0] == str(temp_files[0].resolve())

    def test_add_multiple_files(self, temp_config_dir, temp_files):
        """Test adding multiple files."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])
        manager.add_file(temp_files[2])

        recent = manager.get_recent_files()
        assert len(recent) == 3
        assert recent[0] == str(temp_files[2].resolve())
        assert recent[1] == str(temp_files[1].resolve())
        assert recent[2] == str(temp_files[0].resolve())

    def test_add_duplicate_moves_to_front(self, temp_config_dir, temp_files):
        """Test that adding duplicate file moves it to front."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])
        manager.add_file(temp_files[0])

        recent = manager.get_recent_files()
        assert len(recent) == 2
        assert recent[0] == str(temp_files[0].resolve())
        assert recent[1] == str(temp_files[1].resolve())

    def test_add_file_respects_max_files(self, temp_config_dir):
        """Test that manager respects max files limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            files = [temp_dir / f"file{i}.txt" for i in range(15)]
            for f in files:
                f.write_text("content")

            manager = RecentFilesManager(config_dir=temp_config_dir, max_files=10)
            for f in files:
                manager.add_file(f)

            assert len(manager.get_recent_files()) == 10

    def test_add_file_with_string_path(self, temp_config_dir, temp_files):
        """Test adding file with string path."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(str(temp_files[0]))

        recent = manager.get_recent_files()
        assert len(recent) == 1


class TestRecentFilesManagerGetFiles:
    """Test getting recent files."""

    def test_get_recent_files_returns_copy(self, temp_config_dir, temp_files):
        """Test that get_recent_files returns a copy."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])

        recent1 = manager.get_recent_files()
        recent1.clear()

        recent2 = manager.get_recent_files()
        assert len(recent2) == 1

    def test_get_existing_recent_files(self, temp_config_dir, temp_files):
        """Test getting only existing files."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])
        manager.add_file(temp_files[2])

        # Delete a file
        temp_files[1].unlink()

        existing = manager.get_existing_recent_files()
        assert len(existing) == 2
        assert str(temp_files[1].resolve()) not in existing

    def test_get_existing_recent_files_order(self, temp_config_dir, temp_files):
        """Test that existing files maintain order."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])
        manager.add_file(temp_files[2])

        temp_files[1].unlink()

        existing = manager.get_existing_recent_files()
        assert existing[0] == str(temp_files[2].resolve())
        assert existing[1] == str(temp_files[0].resolve())


class TestRecentFilesManagerRemoveFile:
    """Test removing files."""

    def test_remove_existing_file(self, temp_config_dir, temp_files):
        """Test removing an existing file."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])

        assert manager.remove_file(temp_files[0])
        assert len(manager.get_recent_files()) == 1

    def test_remove_nonexistent_file(self, temp_config_dir, temp_files):
        """Test removing a file that's not in list."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])

        assert not manager.remove_file(temp_files[1])

    def test_remove_file_with_string_path(self, temp_config_dir, temp_files):
        """Test removing file with string path."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])

        assert manager.remove_file(str(temp_files[0]))


class TestRecentFilesManagerClear:
    """Test clearing recent files."""

    def test_clear_all_files(self, temp_config_dir, temp_files):
        """Test clearing all recent files."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])

        manager.clear()

        assert len(manager.get_recent_files()) == 0


class TestRecentFilesManagerPersistence:
    """Test persistence to disk."""

    def test_save_and_load_recent_files(self, temp_config_dir, temp_files):
        """Test that recent files are saved and loaded."""
        manager1 = RecentFilesManager(config_dir=temp_config_dir)
        manager1.add_file(temp_files[0])
        manager1.add_file(temp_files[1])

        # Create new manager with same config
        manager2 = RecentFilesManager(config_dir=temp_config_dir)

        assert manager2.get_recent_files() == manager1.get_recent_files()

    def test_config_file_structure(self, temp_config_dir, temp_files):
        """Test the structure of saved config file."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        manager.add_file(temp_files[1])

        config_file = temp_config_dir / "recent_files.json"
        assert config_file.exists()

        with open(config_file, "r") as f:
            data = json.load(f)
            assert "recent_files" in data
            assert len(data["recent_files"]) == 2

    def test_load_invalid_config_file(self, temp_config_dir):
        """Test loading with corrupted config file."""
        config_file = temp_config_dir / "recent_files.json"
        config_file.write_text("invalid json")

        manager = RecentFilesManager(config_dir=temp_config_dir)
        assert len(manager.get_recent_files()) == 0

    def test_create_config_directory_if_missing(self, temp_config_dir, temp_files):
        """Test that config directory is created if missing."""
        nested_dir = temp_config_dir / "nested" / "config"
        manager = RecentFilesManager(config_dir=nested_dir)
        manager.add_file(temp_files[0])

        assert nested_dir.exists()
        assert (nested_dir / "recent_files.json").exists()


class TestRecentFilesManagerEdgeCases:
    """Test edge cases."""

    def test_add_and_remove_same_file(self, temp_config_dir, temp_files):
        """Test adding and removing the same file."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        manager.add_file(temp_files[0])
        assert len(manager.get_recent_files()) == 1

        manager.remove_file(temp_files[0])
        assert len(manager.get_recent_files()) == 0

    def test_relative_and_absolute_paths_same_file(self, temp_config_dir, temp_files):
        """Test that relative and absolute paths are treated as same file."""
        manager = RecentFilesManager(config_dir=temp_config_dir)
        file_path = temp_files[0]

        manager.add_file(file_path)
        manager.add_file(str(file_path.resolve()))

        # Should still only have one entry (moved to front)
        assert len(manager.get_recent_files()) == 1

    def test_empty_recent_files_list(self, temp_config_dir):
        """Test operations on empty list."""
        manager = RecentFilesManager(config_dir=temp_config_dir)

        assert manager.get_recent_files() == []
        assert manager.get_existing_recent_files() == []
        assert len(manager.get_recent_files()) == 0
