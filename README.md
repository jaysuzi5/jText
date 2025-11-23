# jText - A Notepad++ Alternative for macOS

A lightweight, feature-rich text editor for macOS designed as a Notepad++ alternative. Built with Python and PyQt6.

## Features

### MVP (Current Release)
- **Open & Edit Files** - Open text files and edit them in a clean, distraction-free interface
- **Save Files** - Save your work to disk with Save and Save As options
- **Copy & Paste** - Full clipboard support for text manipulation
- **Undo/Redo** - Complete undo/redo history for all changes
- **Status Bar** - Real-time display of file name, modification state, and cursor position
- **Keyboard Shortcuts** - All standard macOS keyboard shortcuts
- **Multiple File Types** - Works with .txt, .py, .json, and any text file

### Future Enhancements
- Multiple tabs for editing multiple files simultaneously
- JSON syntax highlighting with validation
- Find and replace functionality
- Line numbers display
- Recent files quick access

## System Requirements

- **macOS** - Tested on macOS 12+
- **Python 3.14** - Via Homebrew or system Python
- **PyQt6** - Automatically installed via package manager

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jaysuzi5/jText.git
cd jText
```

### 2. Set Up Virtual Environment
The project uses `uv` as the Python package manager (recommended) or standard `venv`:

**Option A: Using uv (Recommended)**
```bash
# Install uv if you don't have it
# See https://github.com/astral-sh/uv for installation

# Virtual environment is already set up in .venv/
source .venv/bin/activate
```

**Option B: Using venv**
```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Using uv
uv sync

# Or using pip
pip install PyQt6 pytest pytest-cov
```

## Usage

### Running jText

```bash
uv run python main.py
```

Or if you've activated the virtual environment:
```bash
python main.py
```

The application window will open with a blank document ready for editing.

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Cmd+N** | New document |
| **Cmd+O** | Open file |
| **Cmd+S** | Save file |
| **Cmd+Shift+S** | Save As |
| **Cmd+Z** | Undo |
| **Cmd+Shift+Z** | Redo |
| **Cmd+X** | Cut |
| **Cmd+C** | Copy |
| **Cmd+V** | Paste |
| **Cmd+Q** | Quit application |

### File Operations

**Opening a File:**
1. Press `Cmd+O` or go to File → Open
2. Navigate to the file you want to open
3. Click "Open"

**Saving a File:**
1. Press `Cmd+S` or go to File → Save
2. For new files, choose a location and name
3. File is automatically saved to the chosen location

**Save As:**
1. Press `Cmd+Shift+S` or go to File → Save As
2. Choose a new location or name
3. Click "Save"

## Development

### Running Tests

Run the complete test suite:
```bash
uv run pytest tests/ -v
```

Run tests with coverage report:
```bash
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

Generate HTML coverage report:
```bash
uv run pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in your browser
```

### Test Coverage

- **45 unit tests** covering core functionality
- **100% coverage** on Document and FileManager modules
- All tests pass before each commit

### Project Structure

```
jText/
├── src/
│   ├── document.py          # Document model with undo/redo
│   ├── file_manager.py      # File I/O operations
│   └── ui/
│       └── main_window.py   # PyQt6 main application window
├── tests/
│   ├── test_document.py     # Document tests (21 tests)
│   └── test_file_manager.py # FileManager tests (24 tests)
├── main.py                   # Application entry point
├── CLAUDE.md                 # Development guide for Claude Code
└── README.md                 # This file
```

### Adding New Dependencies

```bash
uv add <package_name>
```

### Development Workflow

1. Write unit tests for new features in `tests/`
2. Implement the feature in `src/`
3. Run tests: `uv run pytest tests/ -v`
4. Verify 100% coverage for core modules
5. Commit your changes

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## Architecture

jText is built with a clean separation of concerns:

- **Document Model** - Manages text content, modification state, and undo/redo
- **FileManager** - Handles all file I/O operations
- **MainWindow UI** - PyQt6 GUI with menus, editor, and status bar

This architecture makes the core logic fully testable and independent of the UI framework.

## License

This project is open source. See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure:
- All new code has corresponding unit tests
- Test coverage remains at 100% for core modules
- All tests pass before submitting pull requests
- Follow the development patterns in [CLAUDE.md](CLAUDE.md)

## Troubleshooting

### "command not found: uv"
Install uv from https://github.com/astral-sh/uv or use `pip install` instead.

### "ModuleNotFoundError: No module named 'PyQt6'"
Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
uv sync
```

### Application won't start
Ensure you're running Python 3.14+:
```bash
python3 --version
```

## Support

For issues, feature requests, or questions:
- Check [CLAUDE.md](CLAUDE.md) for development documentation
- Review test files for usage examples
- Open an issue on GitHub

## Future Roadmap

- [ ] Multiple tabs support
- [ ] JSON syntax highlighting
- [ ] Find and replace
- [ ] Line numbers
- [ ] Recent files menu
- [ ] Customizable themes
- [ ] Search and navigation
- [ ] Plugin system