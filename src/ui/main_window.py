"""Main window for the jText application."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QTextEdit,
    QStatusBar,
    QFileDialog,
    QTabWidget,
    QDialog,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtGui import QKeySequence, QAction, QTextCursor
from PyQt6.QtCore import QTimer
from pathlib import Path
from src.document import Document
from src.file_manager import FileManager
from src.recent_files_manager import RecentFilesManager
from src.find_replace import FindReplaceEngine
from src.json_handler import JsonHandler
from src.json_syntax_highlighter import JsonSyntaxHighlighter
from src.ui.json_tree_dialog import JsonTreeDialog
from src.theme_manager import ThemeManager
from src.visual_indicators import LineEndingDetector, WhitespaceAnalyzer
from src.ui.visual_indicator_renderer import VisualIndicatorHighlighter


class FindReplaceDialog(QDialog):
    """Dialog for find and replace operations."""

    def __init__(self, parent=None):
        """Initialize find/replace dialog."""
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()

        # Find field
        layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        layout.addWidget(self.find_input)

        # Replace field
        layout.addWidget(QLabel("Replace with:"))
        self.replace_input = QLineEdit()
        layout.addWidget(self.replace_input)

        # Options
        self.case_sensitive_check = QCheckBox("Case sensitive")
        layout.addWidget(self.case_sensitive_check)

        self.whole_words_check = QCheckBox("Whole words only")
        layout.addWidget(self.whole_words_check)

        # Buttons
        button_layout = QVBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")

        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """Main application window for jText editor."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("jText")
        self.setGeometry(100, 100, 1000, 700)

        # Initialize managers
        self.theme_manager = ThemeManager()
        self.recent_files = RecentFilesManager()
        self.find_replace_engine = FindReplaceEngine()
        self.json_tree_dialog: JsonTreeDialog | None = None

        self._is_loading = False
        self._current_find_position = 0
        self._current_line_ending = None
        self._current_indent_style = None
        self._current_indent_size = 4

        # Map tab widget indices to documents
        # We use QTabWidget directly without TabManager for simpler management
        self.documents = {}  # Maps tab_widget_index -> Document
        self.text_edits = {}  # Maps tab_widget_index -> QTextEdit
        self.highlighters = {}  # Maps tab_widget_index -> JsonSyntaxHighlighter
        self.visual_highlighters = {}  # Maps tab_widget_index -> VisualIndicatorHighlighter

        # Create UI (order matters: tab_widget must exist before menu_bar)
        self._create_tab_widget()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_find_replace_dialog()

        # Apply theme stylesheet
        self._apply_theme()

        # Timer for updating status bar position (debounced)
        self._position_timer = QTimer()
        self._position_timer.timeout.connect(self._update_status_position)
        self._position_timer.setSingleShot(True)

    def _create_tab_widget(self):
        """Create the tab widget with text editors."""
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.setCentralWidget(self.tab_widget)

        # Add initial blank tab
        self._add_new_tab()
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

    def _add_new_tab(self, document=None):
        """Add a new tab with a document.

        Args:
            document: Document to add (creates empty if None)
        """
        if document is None:
            document = Document()

        # Create text editor
        text_edit = QTextEdit()
        text_edit.setFont(text_edit.font())
        text_edit.textChanged.connect(self._on_text_changed)
        text_edit.cursorPositionChanged.connect(self._on_cursor_position_changed)

        # Add to tab widget and get index
        tab_index = self.tab_widget.addTab(text_edit, document.get_file_name())

        # Store document and text edit
        self.documents[tab_index] = document
        self.text_edits[tab_index] = text_edit

        # Always add visual indicator highlighter
        visual_highlighter = VisualIndicatorHighlighter(text_edit.document())
        self.visual_highlighters[tab_index] = visual_highlighter

        # Check if this is a JSON file and apply syntax highlighting
        is_json = False
        if document.file_path and str(document.file_path).endswith('.json'):
            is_json = True
        elif document.content and JsonHandler.is_json(document.content):
            is_json = True

        if is_json:
            highlighter = JsonSyntaxHighlighter(text_edit.document())
            self.highlighters[tab_index] = highlighter

        # Load content if exists
        if document.content:
            self._is_loading = True
            text_edit.setPlainText(document.content)
            self._is_loading = False

        # Analyze document properties
        self._analyze_document_properties(document)

        # Make this the active tab
        self.tab_widget.setCurrentIndex(tab_index)

    def _get_current_tab_index(self):
        """Get the current active tab index."""
        return self.tab_widget.currentIndex()

    def _get_current_document(self):
        """Get the currently active document."""
        index = self._get_current_tab_index()
        if index >= 0:
            return self.documents.get(index)
        return None

    def _get_current_text_edit(self):
        """Get the current active text editor."""
        index = self._get_current_tab_index()
        if index >= 0:
            return self.text_edits.get(index)
        return None

    def _create_menu_bar(self):
        """Create the menu bar with all menu items."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")

        # New
        new_action = QAction("&New Tab", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)

        # Open
        open_action = QAction("&Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        # Save As
        save_as_action = QAction("Save &As", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)

        # Close Tab
        close_tab_action = QAction("&Close Tab", self)
        close_tab_action.setShortcut("Cmd+W")
        close_tab_action.triggered.connect(self._close_current_tab)
        file_menu.addAction(close_tab_action)

        file_menu.addSeparator()

        # Recent Files
        self.recent_files_menu = file_menu.addMenu("&Recent Files")
        self._update_recent_files_menu()

        file_menu.addSeparator()

        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = self.menuBar().addMenu("&Edit")

        # Undo
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)

        # Redo
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Cut
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(lambda: self._get_current_text_edit() and self._get_current_text_edit().cut())
        edit_menu.addAction(cut_action)

        # Copy
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(lambda: self._get_current_text_edit() and self._get_current_text_edit().copy())
        edit_menu.addAction(copy_action)

        # Paste
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(lambda: self._get_current_text_edit() and self._get_current_text_edit().paste())
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        # Find and Replace
        find_action = QAction("&Find and Replace", self)
        find_action.setShortcut("Cmd+H")
        find_action.triggered.connect(self._show_find_replace)
        edit_menu.addAction(find_action)

        # View menu
        view_menu = self.menuBar().addMenu("&View")

        # Toggle theme
        toggle_theme_action = QAction("Toggle &Dark/Light Theme", self)
        toggle_theme_action.setShortcut("Cmd+T")
        toggle_theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(toggle_theme_action)

        # Select theme submenu
        self.theme_submenu = view_menu.addMenu("Select &Theme")
        self._update_theme_menu()

        view_menu.addSeparator()

        # Show whitespace
        self.show_whitespace_action = QAction("Show &Whitespace", self)
        self.show_whitespace_action.setCheckable(True)
        self.show_whitespace_action.setChecked(False)
        self.show_whitespace_action.triggered.connect(self._toggle_whitespace_indicators)
        view_menu.addAction(self.show_whitespace_action)

        # Show line endings
        self.show_line_endings_action = QAction("Show &Line Endings", self)
        self.show_line_endings_action.setCheckable(True)
        self.show_line_endings_action.setChecked(False)
        self.show_line_endings_action.triggered.connect(self._toggle_line_ending_indicators)
        view_menu.addAction(self.show_line_endings_action)

        # JSON menu
        json_menu = self.menuBar().addMenu("&JSON")

        # Format JSON
        format_json_action = QAction("&Format JSON", self)
        format_json_action.triggered.connect(self._format_json)
        json_menu.addAction(format_json_action)

        # Minify JSON
        minify_json_action = QAction("&Minify JSON", self)
        minify_json_action.triggered.connect(self._minify_json)
        json_menu.addAction(minify_json_action)

        # Validate JSON
        validate_json_action = QAction("&Validate JSON", self)
        validate_json_action.triggered.connect(self._validate_json)
        json_menu.addAction(validate_json_action)

        json_menu.addSeparator()

        # View JSON Tree
        view_tree_action = QAction("&View JSON Tree", self)
        view_tree_action.setShortcut("Cmd+J")
        view_tree_action.triggered.connect(self._show_json_tree)
        json_menu.addAction(view_tree_action)

    def _create_find_replace_dialog(self):
        """Create the find and replace dialog."""
        self.find_replace_dialog = FindReplaceDialog(self)
        self.find_replace_dialog.find_next_btn.clicked.connect(self._find_next)
        self.find_replace_dialog.replace_btn.clicked.connect(self._replace_single)
        self.find_replace_dialog.replace_all_btn.clicked.connect(self._replace_all)

    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar_label = QStatusBar()
        self.setStatusBar(self.status_bar_label)
        self._update_status()

    def _update_title(self):
        """Update the window title based on document state."""
        doc = self._get_current_document()
        if doc is None:
            self.setWindowTitle("jText")
            return

        file_name = doc.get_file_name()
        modified_indicator = "*" if doc.is_modified else ""
        self.setWindowTitle(f"{file_name}{modified_indicator} - jText")

        # Update tab title
        tab_index = self._get_current_tab_index()
        if tab_index >= 0:
            self.tab_widget.setTabText(tab_index, f"{file_name}{modified_indicator}")

    def _update_status(self):
        """Update the status bar with file info."""
        doc = self._get_current_document()
        if doc is None:
            self.status_bar_label.showMessage("No document")
            return

        file_name = doc.get_file_name()
        modified_text = " (modified)" if doc.is_modified else ""
        tab_count = self.tab_widget.count()
        current_tab = self._get_current_tab_index() + 1

        # Analyze document properties if not already done
        if self._current_line_ending is None or self._current_indent_style is None:
            self._analyze_document_properties(doc)

        # Build status message with line ending and indentation info
        line_ending_str = self._current_line_ending.display_name() if self._current_line_ending else "LF"
        indent_str = f"{self._current_indent_style} ({self._current_indent_size})" if self._current_indent_style != "none" else "no indent"

        self.status_bar_label.showMessage(
            f"{file_name}{modified_text} | {line_ending_str} | {indent_str} | Tab {current_tab} of {tab_count}"
        )
        self._update_status_position()

    def _update_status_position(self):
        """Update cursor position in status bar."""
        text_edit = self._get_current_text_edit()
        if text_edit is None:
            return

        cursor = text_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        position_text = f"Line {line}, Column {column}"
        self.status_bar_label.showMessage(position_text)

    def _on_text_changed(self):
        """Handle text change event."""
        if not self._is_loading:
            doc = self._get_current_document()
            text_edit = self._get_current_text_edit()
            if doc and text_edit:
                doc.content = text_edit.toPlainText()
                self._update_title()
                self._update_status()

    def _on_cursor_position_changed(self):
        """Handle cursor position change."""
        self._position_timer.start(100)

    def _on_tab_changed(self, index):
        """Handle tab change event."""
        if index >= 0:
            doc = self.documents.get(index)
            text_edit = self.text_edits.get(index)

            if doc and text_edit:
                self._is_loading = True
                text_edit.setPlainText(doc.content)
                self._is_loading = False

            # Analyze document properties for new tab
            self._analyze_document_properties(doc)
            self._update_title()
            self._update_status()

    def _on_tab_close_requested(self, index):
        """Handle tab close button click."""
        doc = self.documents.get(index)
        if doc and doc.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"'{doc.get_file_name()}' has unsaved changes. Save before closing?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
                | QMessageBox.StandardButton.Cancel,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self._save_file_at_index(index)
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        # Check if we're about to close the last tab
        if self.tab_widget.count() <= 1:
            QMessageBox.information(self, "Close Tab", "Cannot close the last tab. Use File → Exit to quit.")
            return

        self.tab_widget.removeTab(index)
        if index in self.documents:
            del self.documents[index]
        if index in self.text_edits:
            del self.text_edits[index]
        if index in self.highlighters:
            del self.highlighters[index]
        if index in self.visual_highlighters:
            del self.visual_highlighters[index]

    def _new_file(self):
        """Create a new file in a new tab."""
        self._add_new_tab()

    def _open_file(self):
        """Open a file dialog and load file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            str(Path.home()),
            "Text Files (*.txt);;Python Files (*.py);;JSON Files (*.json);;All Files (*)",
        )

        if file_path:
            try:
                doc = FileManager.open_file(file_path)
                self._add_new_tab(doc)
                self.recent_files.add_file(file_path)
                self._update_recent_files_menu()
            except (FileNotFoundError, IOError) as e:
                self._show_error(f"Failed to open file: {e}")

    def _save_file(self):
        """Save the current file."""
        doc = self._get_current_document()
        if not doc:
            return

        try:
            if doc.file_path is None:
                self._save_file_as()
            else:
                FileManager.save_file(doc)
                self.recent_files.add_file(doc.file_path)
                self._update_recent_files_menu()
                self._update_title()
                self._update_status()
        except (ValueError, IOError) as e:
            self._show_error(f"Failed to save file: {e}")

    def _save_file_at_index(self, index):
        """Save file at specific tab index."""
        doc = self.documents.get(index)
        if not doc:
            return

        try:
            if doc.file_path is None:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save File As",
                    str(Path.home()),
                    "Text Files (*.txt);;Python Files (*.py);;JSON Files (*.json);;All Files (*)",
                )
                if file_path:
                    FileManager.save_as(doc, file_path)
                    self.recent_files.add_file(file_path)
                    self._update_recent_files_menu()
            else:
                FileManager.save_file(doc)
                self.recent_files.add_file(doc.file_path)
                self._update_recent_files_menu()
        except (ValueError, IOError) as e:
            self._show_error(f"Failed to save file: {e}")

    def _save_file_as(self):
        """Save the file with a new name."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            str(Path.home()),
            "Text Files (*.txt);;Python Files (*.py);;JSON Files (*.json);;All Files (*)",
        )

        if file_path:
            try:
                doc = self._get_current_document()
                if doc:
                    FileManager.save_as(doc, file_path)
                    self.recent_files.add_file(file_path)
                    self._update_recent_files_menu()
                    self._update_title()
                    self._update_status()
            except IOError as e:
                self._show_error(f"Failed to save file: {e}")

    def _close_current_tab(self):
        """Close the current tab."""
        index = self._get_current_tab_index()
        if index >= 0:
            self._on_tab_close_requested(index)

    def _undo(self):
        """Undo the last change."""
        doc = self._get_current_document()
        if doc and doc.undo():
            self._is_loading = True
            text_edit = self._get_current_text_edit()
            if text_edit:
                text_edit.setPlainText(doc.content)
            self._is_loading = False
            self._update_title()
            self._update_status()

    def _redo(self):
        """Redo the last undone change."""
        doc = self._get_current_document()
        if doc and doc.redo():
            self._is_loading = True
            text_edit = self._get_current_text_edit()
            if text_edit:
                text_edit.setPlainText(doc.content)
            self._is_loading = False
            self._update_title()
            self._update_status()

    def _show_find_replace(self):
        """Show the find and replace dialog."""
        self.find_replace_dialog.show()
        self.find_replace_dialog.find_input.setFocus()
        self._current_find_position = 0

    def _find_next(self):
        """Find next occurrence."""
        text_edit = self._get_current_text_edit()
        doc = self._get_current_document()
        if not text_edit or not doc:
            return

        search_term = self.find_replace_dialog.find_input.text()
        if not search_term:
            return

        # Update engine settings
        self.find_replace_engine.set_case_sensitive(
            self.find_replace_dialog.case_sensitive_check.isChecked()
        )
        self.find_replace_engine.set_whole_words(
            self.find_replace_dialog.whole_words_check.isChecked()
        )

        # Find next
        result = self.find_replace_engine.find_next(
            doc.content, search_term, self._current_find_position
        )

        if result:
            start, end = result
            self._current_find_position = end

            # Select the found text
            cursor = text_edit.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            text_edit.setTextCursor(cursor)
        else:
            QMessageBox.information(
                self, "Find", f"No more occurrences of '{search_term}' found."
            )
            self._current_find_position = 0

    def _replace_single(self):
        """Replace the first occurrence."""
        doc = self._get_current_document()
        if not doc:
            return

        search_term = self.find_replace_dialog.find_input.text()
        replace_term = self.find_replace_dialog.replace_input.text()

        if not search_term:
            return

        # Update engine settings
        self.find_replace_engine.set_case_sensitive(
            self.find_replace_dialog.case_sensitive_check.isChecked()
        )
        self.find_replace_engine.set_whole_words(
            self.find_replace_dialog.whole_words_check.isChecked()
        )

        modified, count = self.find_replace_engine.replace(
            doc.content, search_term, replace_term
        )

        if count > 0:
            self._is_loading = True
            doc.content = modified
            text_edit = self._get_current_text_edit()
            if text_edit:
                text_edit.setPlainText(modified)
            self._is_loading = False
            QMessageBox.information(self, "Replace", f"Replaced {count} occurrence.")
        else:
            QMessageBox.information(
                self, "Replace", f"No occurrences of '{search_term}' found."
            )

    def _replace_all(self):
        """Replace all occurrences."""
        doc = self._get_current_document()
        if not doc:
            return

        search_term = self.find_replace_dialog.find_input.text()
        replace_term = self.find_replace_dialog.replace_input.text()

        if not search_term:
            return

        # Update engine settings
        self.find_replace_engine.set_case_sensitive(
            self.find_replace_dialog.case_sensitive_check.isChecked()
        )
        self.find_replace_engine.set_whole_words(
            self.find_replace_dialog.whole_words_check.isChecked()
        )

        modified, count = self.find_replace_engine.replace_all(
            doc.content, search_term, replace_term
        )

        if count > 0:
            self._is_loading = True
            doc.content = modified
            text_edit = self._get_current_text_edit()
            if text_edit:
                text_edit.setPlainText(modified)
            self._is_loading = False
            QMessageBox.information(
                self, "Replace All", f"Replaced {count} occurrences."
            )
        else:
            QMessageBox.information(
                self, "Replace All", f"No occurrences of '{search_term}' found."
            )

    def _update_recent_files_menu(self):
        """Update the recent files menu."""
        self.recent_files_menu.clear()

        recent_files = self.recent_files.get_existing_recent_files()

        if not recent_files:
            self.recent_files_menu.addAction("(No recent files)").setEnabled(False)
            return

        for file_path in recent_files[:10]:
            action = self.recent_files_menu.addAction(Path(file_path).name)
            action.triggered.connect(lambda checked, path=file_path: self._open_recent_file(path))

        self.recent_files_menu.addSeparator()
        clear_action = self.recent_files_menu.addAction("Clear Recent Files")
        clear_action.triggered.connect(self._clear_recent_files)

    def _open_recent_file(self, file_path):
        """Open a recent file."""
        try:
            doc = FileManager.open_file(file_path)
            self._add_new_tab(doc)
        except (FileNotFoundError, IOError) as e:
            self._show_error(f"Failed to open file: {e}")

    def _clear_recent_files(self):
        """Clear the recent files list."""
        self.recent_files.clear()
        self._update_recent_files_menu()

    def _show_error(self, message: str):
        """Show an error message to the user."""
        QMessageBox.critical(self, "Error", message)

    def _is_json_file(self):
        """Check if current file is a JSON file."""
        doc = self._get_current_document()
        if not doc:
            return False

        # Check by file extension
        if doc.file_path and str(doc.file_path).endswith('.json'):
            return True

        # Check by content validation
        return JsonHandler.is_json(doc.content)

    def _format_json(self):
        """Format the current JSON document."""
        doc = self._get_current_document()
        text_edit = self._get_current_text_edit()
        if not doc or not text_edit:
            return

        formatted, success = JsonHandler.format_json(doc.content)

        if success:
            self._is_loading = True
            doc.content = formatted
            text_edit.setPlainText(formatted)
            self._is_loading = False
            self._update_title()
            self._update_status()
            QMessageBox.information(self, "Format JSON", "JSON formatted successfully!")
        else:
            self._show_error("Invalid JSON: unable to format. Check syntax and try again.")

    def _minify_json(self):
        """Minify the current JSON document."""
        doc = self._get_current_document()
        text_edit = self._get_current_text_edit()
        if not doc or not text_edit:
            return

        minified, success = JsonHandler.minify_json(doc.content)

        if success:
            self._is_loading = True
            doc.content = minified
            text_edit.setPlainText(minified)
            self._is_loading = False
            self._update_title()
            self._update_status()
            QMessageBox.information(self, "Minify JSON", "JSON minified successfully!")
        else:
            self._show_error("Invalid JSON: unable to minify. Check syntax and try again.")

    def _validate_json(self):
        """Validate the current JSON document."""
        doc = self._get_current_document()
        if not doc:
            return

        is_valid, error = JsonHandler.validate_json(doc.content)

        if is_valid:
            QMessageBox.information(self, "Validate JSON", "JSON is valid!")
        else:
            QMessageBox.warning(self, "Validate JSON", f"JSON validation failed:\n{error}")

    def _show_json_tree(self):
        """Show JSON tree view dialog."""
        doc = self._get_current_document()
        if not doc:
            return

        # Validate JSON first
        is_valid, error = JsonHandler.validate_json(doc.content)
        if not is_valid:
            QMessageBox.warning(
                self,
                "Invalid JSON",
                f"Cannot display tree view for invalid JSON:\n{error}",
            )
            return

        # Create dialog if not exists
        if self.json_tree_dialog is None:
            self.json_tree_dialog = JsonTreeDialog(self)

        # Load JSON into tree view
        if self.json_tree_dialog.load_json(doc.content):
            self.json_tree_dialog.show()
            self.json_tree_dialog.raise_()
            self.json_tree_dialog.activateWindow()
        else:
            QMessageBox.warning(self, "Error", "Failed to load JSON into tree view.")

    def _apply_theme(self):
        """Apply the current theme stylesheet to the window."""
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)

    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme_manager.toggle_theme()
        self._apply_theme()

    def _update_theme_menu(self):
        """Update the theme selector menu with available themes."""
        self.theme_submenu.clear()
        available_themes = self.theme_manager.get_available_themes()

        for theme_name in sorted(available_themes):
            action = self.theme_submenu.addAction(theme_name.capitalize())
            action.triggered.connect(lambda checked, name=theme_name: self._select_theme(name))

    def _select_theme(self, theme_name):
        """Select a theme by name."""
        if self.theme_manager.set_theme(theme_name):
            self._apply_theme()

    def _analyze_document_properties(self, doc):
        """Analyze document to detect line endings and indentation style."""
        if not doc:
            self._current_line_ending = LineEndingDetector.detect("")
            self._current_indent_style = "none"
            self._current_indent_size = 4
            return

        # Detect line ending
        self._current_line_ending = LineEndingDetector.detect(doc.content)

        # Detect indentation
        self._current_indent_style = WhitespaceAnalyzer.get_indentation_style(doc.content)
        self._current_indent_size = WhitespaceAnalyzer.get_indent_size(doc.content)

    def _toggle_whitespace_indicators(self):
        """Toggle whitespace indicator display."""
        index = self._get_current_tab_index()
        if index >= 0 and index in self.visual_highlighters:
            show_whitespace = self.show_whitespace_action.isChecked()
            highlighter = self.visual_highlighters[index]
            highlighter.set_show_whitespace(show_whitespace)

    def _toggle_line_ending_indicators(self):
        """Toggle line ending indicator display."""
        index = self._get_current_tab_index()
        if index >= 0 and index in self.visual_highlighters:
            show_line_endings = self.show_line_endings_action.isChecked()
            highlighter = self.visual_highlighters[index]
            highlighter.set_show_line_endings(show_line_endings)
