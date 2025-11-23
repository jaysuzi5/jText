"""Main window for the jText application."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTextEdit,
    QStatusBar,
    QFileDialog,
)
from PyQt6.QtGui import QKeySequence, QAction, QIcon
from PyQt6.QtCore import Qt, QTimer
from pathlib import Path
from src.document import Document
from src.file_manager import FileManager


class MainWindow(QMainWindow):
    """Main application window for jText editor."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("jText - Untitled")
        self.setGeometry(100, 100, 800, 600)

        self.document = Document()
        self._is_loading = False

        # Create UI (order matters: text_editor must exist before menu_bar)
        self._create_text_editor()
        self._create_menu_bar()
        self._create_status_bar()

        # Connect document changes
        self._update_title()

        # Timer for updating status bar position (debounced)
        self._position_timer = QTimer()
        self._position_timer.timeout.connect(self._update_status_position)
        self._position_timer.setSingleShot(True)

    def _create_menu_bar(self):
        """Create the menu bar with File menu items."""
        file_menu = self.menuBar().addMenu("&File")

        # New
        new_action = QAction("&New", self)
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
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        # Copy
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        # Paste
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

    def _create_text_editor(self):
        """Create the main text editor widget."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setFont(self.text_edit.font())
        self.text_edit.textChanged.connect(self._on_text_changed)
        self.text_edit.cursorPositionChanged.connect(self._on_cursor_position_changed)

        layout.addWidget(self.text_edit)
        central_widget.setLayout(layout)

    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar_label = QStatusBar()
        self.setStatusBar(self.status_bar_label)
        self._update_status()

    def _update_title(self):
        """Update the window title based on document state."""
        file_name = self.document.get_file_name()
        modified_indicator = "*" if self.document.is_modified else ""
        self.setWindowTitle(f"{file_name}{modified_indicator} - jText")

    def _update_status(self):
        """Update the status bar with file info."""
        file_name = self.document.get_file_name()
        modified_text = " (modified)" if self.document.is_modified else ""
        self.status_bar_label.showMessage(f"{file_name}{modified_text}")
        self._update_status_position()

    def _update_status_position(self):
        """Update cursor position in status bar."""
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        position_text = f"{self.document.get_file_name()} - Line {line}, Column {column}"
        if self.document.is_modified:
            position_text += " (modified)"
        self.status_bar_label.showMessage(position_text)

    def _on_text_changed(self):
        """Handle text change event."""
        if not self._is_loading:
            self.document.content = self.text_edit.toPlainText()
            self._update_title()
            self._update_status()

    def _on_cursor_position_changed(self):
        """Handle cursor position change."""
        # Debounce position updates
        self._position_timer.start(100)

    def _new_file(self):
        """Create a new file."""
        self.document = Document()
        self._is_loading = True
        self.text_edit.clear()
        self._is_loading = False
        self._update_title()
        self._update_status()

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
                self.document = FileManager.open_file(file_path)
                self._is_loading = True
                self.text_edit.setPlainText(self.document.content)
                self._is_loading = False
                self._update_title()
                self._update_status()
            except (FileNotFoundError, IOError) as e:
                self._show_error(f"Failed to open file: {e}")

    def _save_file(self):
        """Save the current file."""
        try:
            if self.document.file_path is None:
                self._save_file_as()
            else:
                FileManager.save_file(self.document)
                self._update_title()
                self._update_status()
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
                FileManager.save_as(self.document, file_path)
                self._update_title()
                self._update_status()
            except IOError as e:
                self._show_error(f"Failed to save file: {e}")

    def _undo(self):
        """Undo the last change."""
        if self.document.undo():
            self._is_loading = True
            self.text_edit.setPlainText(self.document.content)
            self._is_loading = False
            self._update_title()
            self._update_status()

    def _redo(self):
        """Redo the last undone change."""
        if self.document.redo():
            self._is_loading = True
            self.text_edit.setPlainText(self.document.content)
            self._is_loading = False
            self._update_title()
            self._update_status()

    def _show_error(self, message: str):
        """Show an error message to the user."""
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.critical(self, "Error", message)
