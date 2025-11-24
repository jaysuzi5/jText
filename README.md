# jText - A Notepad++ Alternative for macOS

A lightweight, feature-rich text editor for macOS designed as a Notepad++ alternative. Built with Python and PyQt6.

## Features

### Current Release

#### Core Editing
- **Multiple Tabs** - Edit multiple files simultaneously in separate tabs
- **Open & Edit Files** - Open text files and edit them in a clean interface
- **Save Files** - Save your work with Save and Save As options
- **Copy & Paste** - Full clipboard support for text manipulation
- **Undo/Redo** - Complete undo/redo history for all changes
- **Status Bar** - Real-time display of file name, modification state, cursor position, and tab info
- **Keyboard Shortcuts** - All standard macOS keyboard shortcuts
- **Multiple File Types** - Works with .txt, .py, .json, and any text file

#### Visual Polish
- **Dark/Light Themes** - Toggle between light and dark color schemes (Cmd+T)
- **Theme Selection** - Choose from available themes in View menu
- **Whitespace Indicators** - Optional display of spaces and tabs with visual highlighting
- **Line Ending Detection** - Auto-detect and display line ending type (LF, CRLF, CR)
- **Indentation Analysis** - Auto-detect indentation style (spaces vs tabs) and size (2, 4, 8)

#### JSON Support
- **JSON Syntax Highlighting** - Color-coded syntax with proper formatting
- **JSON Operations** - Format, minify, and validate JSON files
- **JSON Tree View** - Expand/collapse hierarchical view of JSON structure with visual tree navigation (Cmd+J)

#### Find & Replace
- **Advanced Search** - Find and replace with case sensitivity and whole-words options
- **Search History** - Keep track of recent searches and access them quickly
- **Regex Support** - Full regex pattern support for advanced searching
- **Find Navigation** - Find next/previous with result highlighting and counting
- **Replace Operations** - Single or bulk replace functionality

#### Advanced Text Editing
- **Code Folding** - Fold/unfold code regions for functions, classes, and blocks
- **Text Transformation** - Convert text case: uppercase, lowercase, title case, camelCase, snake_case
- **Line Operations** - Sort lines, reverse line order, remove duplicates, remove empty lines
- **Smart Indentation** - Auto-indent based on code structure, detect indent size and style
- **Code Snippets** - 18 built-in snippets for Python and JavaScript with placeholder expansion
- **Multi-Cursor Support** - Edit multiple locations simultaneously

### Future Enhancements
- Line numbers display
- Language support for more file types (Python, HTML, CSS syntax highlighting)
- Plugin system for extensibility
- Additional code snippet library

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

#### File & Navigation
| Shortcut | Action |
|----------|--------|
| **Cmd+N** | New Tab |
| **Cmd+O** | Open File |
| **Cmd+S** | Save |
| **Cmd+Shift+S** | Save As |
| **Cmd+W** | Close Tab |
| **Cmd+Q** | Quit Application |

#### Editing
| Shortcut | Action |
|----------|--------|
| **Cmd+Z** | Undo |
| **Cmd+Shift+Z** | Redo |
| **Cmd+X** | Cut |
| **Cmd+C** | Copy |
| **Cmd+V** | Paste |
| **Tab** | Indent Selection |
| **Shift+Tab** | Dedent Selection |

#### Search & Replace
| Shortcut | Action |
|----------|--------|
| **Cmd+H** | Find and Replace |

#### View & Theme
| Shortcut | Action |
|----------|--------|
| **Cmd+T** | Toggle Dark/Light Theme |
| **Cmd+J** | View JSON Tree |

#### Advanced Text Editing (Tools Menu)
| Shortcut | Action |
|----------|--------|
| **Cmd+Alt+L** | Fold All Code Regions |
| **Cmd+Alt+K** | Unfold All Code Regions |
| **Cmd+Shift+U** | Convert to Uppercase |
| **Cmd+Shift+L** | Convert to Lowercase |
| **Cmd+Ctrl+S** | Sort Lines |
| **Cmd+Shift+S** | Insert Snippet |

### JSON Operations

When editing JSON files (detected by `.json` extension or JSON content), the following menu options become available:

| Menu Item | Description |
|-----------|-------------|
| **JSON → Format JSON** | Pretty-print the JSON with proper indentation and formatting |
| **JSON → Minify JSON** | Remove all whitespace and reduce file size |
| **JSON → Validate JSON** | Check JSON syntax and display any errors found |
| **JSON → View JSON Tree** | Open expandable/collapsible tree view of JSON structure |

**Color-Coded Syntax Highlighting for JSON:**
- **Blue (Bold)** - Object keys
- **Green** - String values
- **Orange** - Numbers
- **Red (Bold)** - Boolean values (true/false) and null
- **Gray (Bold)** - Brackets and structural characters

### JSON Tree View

**Accessing the Tree View:**
- Press `Cmd+J` or go to JSON → View JSON Tree
- Opens in a separate window with interactive tree structure
- Shows count of items/keys for containers
- Each node can be expanded or collapsed by clicking

**Tree Navigation:**
- **Click node arrow** - Toggle expand/collapse for that node
- **Expand All button** - Expand entire tree hierarchy
- **Collapse All button** - Collapse entire tree to root level
- **Color-coded nodes** - Same color scheme as syntax highlighting
  - Objects and arrays show item count
  - Primitives show formatted values with truncation for long strings

### File Operations

**Opening a File:**
1. Press `Cmd+O` or go to File → Open
2. Navigate to the file you want to open
3. Click "Open" (file opens in a new tab)

**Saving a File:**
1. Press `Cmd+S` or go to File → Save
2. For new files, choose a location and name
3. File is automatically saved to the chosen location

**Save As:**
1. Press `Cmd+Shift+S` or go to File → Save As
2. Choose a new location or name
3. Click "Save"

### Tab Management

**Creating a New Tab:**
- Press `Cmd+N` or go to File → New Tab
- Each tab shows the filename in the tab bar
- Modified files show an asterisk (*) in the tab

**Switching Between Tabs:**
- Click on any tab at the top to switch to that document
- The status bar shows "Tab X of Y"

**Closing a Tab:**
- Press `Cmd+W` or go to File → Close Tab
- If unsaved changes exist, you'll be prompted to save

### Find and Replace

**Opening Find & Replace:**
- Press `Cmd+H` or go to Edit → Find and Replace
- A dialog window opens with search and replace fields

**Finding Text:**
1. Enter the text to find in the "Find:" field
2. Click "Find Next" to locate the first occurrence
3. Matching text is highlighted in the editor
4. Click "Find Next" again to find the next match

**Replacing Text:**
1. Enter search term in "Find:" field
2. Enter replacement text in "Replace with:" field
3. Click "Replace" to replace the first occurrence
4. Or click "Replace All" to replace all occurrences at once

**Find & Replace Options:**
- ✓ **Case sensitive** - Match uppercase/lowercase exactly
- ✓ **Whole words only** - Don't match partial words (e.g., "cat" won't match "caterpillar")

### Recent Files

**Accessing Recent Files:**
- Go to File → Recent Files
- Click any file to open it in a new tab
- Recent files are automatically tracked when you open or save files

**Clearing Recent Files:**
- Go to File → Recent Files → Clear Recent Files

**Technical Details:**
- Saves to `~/.config/jtext/recent_files.json`
- Shows up to 10 most recent files
- Only displays files that still exist on disk

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

- **516 unit tests** covering all functionality
- **100% coverage** on all modules:
  - Document: 100% (21 tests)
  - FileManager: 100% (24 tests)
  - RecentFilesManager: 100% (21 tests)
  - FindReplaceEngine: 100% (40 tests)
  - JsonHandler: 100% (38 tests)
  - JsonTreeModel: 100% (30 tests)
  - ThemeManager: 100% (25 tests)
  - VisualIndicators: 100% (38 tests)
  - MultiCursorManager: 100% (30 tests)
  - TextTransformer: 100% (48 tests)
  - CodeFolder: 100% (36 tests)
  - SmartIndenter: 100% (38 tests)
  - AdvancedSearchEngine: 100% (57 tests)
  - SnippetManager: 100% (46 tests)
- All tests pass before each commit

### Project Structure

```
jText/
├── src/
│   ├── Core/
│   │   ├── document.py                    # Document model with undo/redo (21 tests)
│   │   ├── file_manager.py                # File I/O operations (24 tests)
│   │   ├── recent_files_manager.py        # Recent files tracking (21 tests)
│   │   └── find_replace.py                # Find and replace engine (40 tests)
│   │
│   ├── Advanced Text Editing/
│   │   ├── multi_cursor.py                # Multi-cursor support (30 tests)
│   │   ├── text_transformer.py            # Text case/line operations (48 tests)
│   │   ├── code_folder.py                 # Code folding regions (36 tests)
│   │   ├── smart_indenter.py              # Smart indentation (38 tests)
│   │   ├── advanced_search.py             # Regex search with history (57 tests)
│   │   └── snippet_manager.py             # Snippet library (46 tests)
│   │
│   ├── JSON Support/
│   │   ├── json_handler.py                # JSON operations (38 tests)
│   │   ├── json_syntax_highlighter.py     # JSON syntax highlighting
│   │   ├── json_tree_model.py             # JSON hierarchical tree (30 tests)
│   │   └── json_tree_view.py              # JSON tree view widget
│   │
│   ├── Visual Polish/
│   │   ├── theme_manager.py               # Theme management (25 tests)
│   │   ├── visual_indicators.py           # Line endings/whitespace (38 tests)
│   │   └── ui/visual_indicator_renderer.py # Visual indicator highlighter
│   │
│   └── UI/
│       ├── main_window.py                 # PyQt6 main window with all menus
│       └── json_tree_dialog.py            # JSON tree view dialog
│
├── tests/
│   ├── test_document.py
│   ├── test_file_manager.py
│   ├── test_recent_files_manager.py
│   ├── test_find_replace.py
│   ├── test_json_handler.py
│   ├── test_json_tree_model.py
│   ├── test_theme_manager.py
│   ├── test_visual_indicators.py
│   ├── test_multi_cursor.py
│   ├── test_text_transformer.py
│   ├── test_code_folder.py
│   ├── test_smart_indenter.py
│   ├── test_advanced_search.py
│   └── test_snippet_manager.py
│
├── main.py                       # Application entry point
├── CLAUDE.md                     # Development guide for Claude Code
├── pyproject.toml               # uv project configuration
└── README.md                     # This file
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

### Completed
- [x] Multiple tabs support
- [x] Find and replace
- [x] Recent files menu
- [x] JSON syntax highlighting and operations
- [x] JSON tree view
- [x] Dark/Light themes with customization
- [x] Whitespace and line ending indicators
- [x] Advanced search with regex support
- [x] Code folding for functions and classes
- [x] Text transformations (case conversion, sorting)
- [x] Smart indentation with auto-detect
- [x] Code snippet library with expansion
- [x] Multi-cursor support

### Planned
- [ ] Line numbers in editor
- [ ] Language-specific syntax highlighting (Python, HTML, CSS, JavaScript)
- [ ] Plugin/extension system
- [ ] Command palette for quick access to features
- [ ] Code completion and intellisense
- [ ] Git integration (diff, blame, commit)