"""Manager for tracking recently opened files."""

import json
from pathlib import Path
from typing import List, Optional


class RecentFilesManager:
    """Manages a list of recently opened files."""

    def __init__(self, config_dir: Optional[Path] = None, max_files: int = 10):
        """Initialize the recent files manager.

        Args:
            config_dir: Directory to store recent files config (uses .config if None)
            max_files: Maximum number of recent files to track
        """
        self.max_files = max_files

        if config_dir is None:
            config_dir = Path.home() / ".config" / "jtext"

        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "recent_files.json"
        self._recent_files: List[str] = []

        self._load_recent_files()

    def add_file(self, file_path: str | Path) -> None:
        """Add a file to the recent files list.

        Args:
            file_path: Path to the file
        """
        file_path_str = str(Path(file_path).resolve())

        # Remove if already in list
        if file_path_str in self._recent_files:
            self._recent_files.remove(file_path_str)

        # Add to front
        self._recent_files.insert(0, file_path_str)

        # Trim to max size
        self._recent_files = self._recent_files[: self.max_files]

        # Save to disk
        self._save_recent_files()

    def get_recent_files(self) -> List[str]:
        """Get the list of recent files.

        Returns:
            List of file paths in order of most recent first
        """
        return self._recent_files.copy()

    def get_existing_recent_files(self) -> List[str]:
        """Get recent files that still exist on disk.

        Returns:
            List of existing file paths
        """
        return [f for f in self._recent_files if Path(f).exists()]

    def remove_file(self, file_path: str | Path) -> bool:
        """Remove a file from recent files.

        Args:
            file_path: Path to remove

        Returns:
            True if file was removed, False if not found
        """
        file_path_str = str(Path(file_path).resolve())

        if file_path_str in self._recent_files:
            self._recent_files.remove(file_path_str)
            self._save_recent_files()
            return True

        return False

    def clear(self) -> None:
        """Clear all recent files."""
        self._recent_files.clear()
        self._save_recent_files()

    def _load_recent_files(self) -> None:
        """Load recent files from config file."""
        if not self.config_file.exists():
            self._recent_files = []
            return

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._recent_files = data.get("recent_files", [])
        except (json.JSONDecodeError, IOError):
            self._recent_files = []

    def _save_recent_files(self) -> None:
        """Save recent files to config file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)

            data = {"recent_files": self._recent_files}

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass
