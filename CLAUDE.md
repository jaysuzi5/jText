# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**jText** is a macOS text editor application designed as a Notepad++ alternative for Mac users. The MVP supports opening, editing, and saving text files with copy/paste support and basic undo/redo.

- **Language:** Python 3.14
- **Package Manager:** uv
- **GUI Framework:** PyQt6
- **Testing Framework:** pytest
- **Platform:** macOS
- **Current Version:** MVP (single-tab text editor)

## Getting Started

### Development Environment

The project uses `uv` for dependency management with Python 3.14 and a virtual environment in `.venv/`.

### Running the Application

```bash
uv run python main.py
```

This launches the jText editor GUI. Keyboard shortcuts:
- **Cmd+N** - New document
- **Cmd+O** - Open file
- **Cmd+S** - Save file
- **Cmd+Shift+S** - Save As
- **Cmd+Z** - Undo
- **Cmd+Shift+Z** - Redo
- **Cmd+X** - Cut
- **Cmd+C** - Copy
- **Cmd+V** - Paste

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_document.py -v
```

**Current Coverage:** 100% for core modules (Document: src/document.py, FileManager: src/file_manager.py). UI code (src/ui/main_window.py) is not unit tested due to GUI requirements.

### Adding Dependencies

```bash
uv add <package_name>
```

Current dependencies: PyQt6, pytest, pytest-cov

## Project Structure

```
jText/
├── src/
│   ├── __init__.py              # Package marker
│   ├── document.py              # Document model with undo/redo (100% tested)
│   ├── file_manager.py          # File I/O operations (100% tested)
│   └── ui/
│       ├── __init__.py
│       └── main_window.py       # MainWindow UI with menus and editor
├── tests/
│   ├── __init__.py
│   ├── test_document.py         # 21 tests for Document model
│   └── test_file_manager.py     # 24 tests for FileManager
├── main.py                       # Application entry point
├── pyproject.toml               # Project configuration
└── uv.lock                       # Locked dependency versions
```

## Core Architecture

### Document Model (src/document.py)

Manages text content with these responsibilities:
- Content storage and modification tracking
- File path management
- Undo/redo stack management via `content` property setter
- Modified state tracking (compared to original saved state)

Key properties: `content`, `file_path`, `is_modified`, `can_undo()`, `can_redo()`

### FileManager (src/file_manager.py)

Handles file I/O with these operations:
- `open_file()` - Load file content into Document
- `save_file()` - Save Document to file (with optional new path)
- `save_as()` - Save to new file path
- `create_new_document()` - Create empty Document
- `get_file_extension()` - Extract file extension

All file operations use UTF-8 encoding and handle errors appropriately.

### MainWindow UI (src/ui/main_window.py)

PyQt6 application window with:
- QTextEdit for content editing
- File menu: New, Open, Save, Save As, Exit
- Edit menu: Undo, Redo, Cut, Copy, Paste
- Status bar showing file name, modification state, and cursor position
- All standard macOS keyboard shortcuts
- Document change synchronization

## Development Patterns

### Testing Pattern (TDD Approach)

All new features must have accompanying unit tests:
1. Write tests first in `tests/test_*.py`
2. Implement feature in `src/`
3. Run tests: `uv run pytest tests/test_*.py -v`
4. Verify coverage meets requirements
5. Commit code with passing tests

### File Operations Pattern

Use FileManager for all file I/O:
```python
from src.file_manager import FileManager

# Open
doc = FileManager.open_file("path/to/file.txt")

# Save
FileManager.save_file(doc, "path/to/file.txt")

# Save As
FileManager.save_as(doc, "new_path.txt")
```

### Document State Management Pattern

Document tracks modifications automatically:
```python
doc = Document("original")
assert not doc.is_modified

doc.content = "modified"
assert doc.is_modified

FileManager.save_file(doc, "path.txt")
assert not doc.is_modified  # Saved, no longer modified
```

## Future Enhancements

### Planned Features
1. **Multiple Tabs** - Tab widget for multiple open documents
2. **JSON Syntax Highlighting** - Syntax highlighter for JSON files
3. **Find/Replace** - Ctrl+H find and replace dialog
4. **Line Numbers** - Display line numbers in editor
5. **Recent Files** - Quick access to recently opened files

### Implementation Notes for Future Work
- New features should follow the same pattern: core logic first with tests, then UI integration
- UI components are in src/ui/ - organize complex features into separate files
- For syntax highlighting, consider using QSyntaxHighlighter from PyQt6
- Tab support requires refactoring MainWindow to use QTabWidget

## Important Notes

- All changes must maintain 100% coverage for core modules (Document, FileManager)
- The UI layer (MainWindow) cannot be unit tested without a display server, so integration testing should be done manually
- Keep undo/redo logic simple - currently tracks full content snapshots
- File operations assume UTF-8 encoding
- All keyboard shortcuts follow macOS conventions (Cmd instead of Ctrl)

## Helpful Commands

```bash
# Run tests with watch mode (requires pytest-watch)
# uv add pytest-watch
# uv run ptw tests/

# Generate HTML coverage report
uv run pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser

# Run specific test
uv run pytest tests/test_document.py::TestDocumentInitialization::test_create_empty_document -v
```
