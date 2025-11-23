"""File manager for handling document file I/O operations."""

from pathlib import Path
from typing import Optional
from src.document import Document


class FileManager:
    """Manages file operations for text documents."""

    @staticmethod
    def open_file(file_path: str | Path) -> Document:
        """Open and read a text file into a Document.

        Args:
            file_path: Path to the file to open

        Returns:
            Document with file content and path set

        Raises:
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except IOError as e:
            raise IOError(f"Failed to read file {path}: {e}")

        doc = Document(content)
        doc.file_path = path
        doc.mark_saved()
        return doc

    @staticmethod
    def save_file(document: Document, file_path: Optional[str | Path] = None) -> Path:
        """Save a document to a file.

        Args:
            document: Document to save
            file_path: Path to save to (uses document's path if not provided)

        Returns:
            Path where file was saved

        Raises:
            ValueError: If no path is provided and document has no path
            IOError: If file cannot be written
        """
        path = None

        if file_path is not None:
            path = Path(file_path)
        elif document.file_path is not None:
            path = document.file_path
        else:
            raise ValueError("No file path provided and document has no path")

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(document.content)
        except IOError as e:
            raise IOError(f"Failed to write file {path}: {e}")

        document.file_path = path
        document.mark_saved()
        return path

    @staticmethod
    def save_as(document: Document, file_path: str | Path) -> Path:
        """Save document with a new file path (Save As).

        Args:
            document: Document to save
            file_path: New path to save to

        Returns:
            Path where file was saved
        """
        return FileManager.save_file(document, file_path)

    @staticmethod
    def create_new_document() -> Document:
        """Create a new empty document.

        Returns:
            New empty Document
        """
        return Document()

    @staticmethod
    def get_file_extension(file_path: str | Path) -> str:
        """Get the file extension.

        Args:
            file_path: Path to the file

        Returns:
            File extension (without dot) or empty string if no extension
        """
        return Path(file_path).suffix.lstrip(".")
