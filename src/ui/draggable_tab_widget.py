"""Draggable tab widget for reordering tabs via drag-and-drop."""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import Qt, QMimeData, QByteArray, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap


class DraggableTabWidget(QTabWidget):
    """QTabWidget with drag-and-drop support for tab reordering."""

    # Signal emitted when tabs are reordered: (from_index, to_index)
    tabReordered = pyqtSignal(int, int)

    def __init__(self, parent=None):
        """Initialize the draggable tab widget."""
        super().__init__(parent)
        self._drag_start_pos = None
        self._dragged_tab_index = -1
        self.setMovable(True)  # Enable native tab movement

    def mousePressEvent(self, event):
        """Handle mouse press for starting drag."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Get the tab index at the clicked position
            tab_bar = self.tabBar()
            self._dragged_tab_index = tab_bar.tabAt(event.pos())

            if self._dragged_tab_index != -1:
                self._drag_start_pos = event.pos()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to complete drag."""
        self._drag_start_pos = None
        self._dragged_tab_index = -1
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging tabs."""
        if (
            event.buttons() == Qt.MouseButton.LeftButton
            and self._drag_start_pos is not None
            and self._dragged_tab_index != -1
        ):
            # Calculate drag distance
            distance = (event.pos() - self._drag_start_pos).manhattanLength()

            # Start drag if moved far enough
            if distance > 5:
                self._start_drag(event)

        super().mouseMoveEvent(event)

    def _start_drag(self, event):
        """Initiate drag operation."""
        tab_bar = self.tabBar()
        drag = QDrag(self)
        mime_data = QMimeData()

        # Store the tab index in mime data
        mime_data.setText(str(self._dragged_tab_index))
        drag.setMimeData(mime_data)

        # Create a pixmap of the tab for visual feedback
        tab_rect = tab_bar.tabRect(self._dragged_tab_index)
        pixmap = QPixmap(tab_rect.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        pixmap.fill(self.palette().color(self.backgroundRole()))

        # Draw the tab text on the pixmap
        painter_pixmap = pixmap
        tab_bar.paintEvent(event)

        drag.setPixmap(pixmap)
        drag.exec(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, event):
        """Handle drag enter event."""
        if event.mimeData().hasText():
            try:
                int(event.mimeData().text())
                event.acceptProposedAction()
            except ValueError:
                pass

    def dragMoveEvent(self, event):
        """Handle drag move event."""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event to reorder tabs."""
        if not event.mimeData().hasText():
            return

        try:
            from_index = int(event.mimeData().text())
        except (ValueError, AttributeError):
            return

        tab_bar = self.tabBar()
        to_index = tab_bar.tabAt(event.pos())

        if to_index == -1:
            # Dropped outside tab bar, put at the end
            to_index = self.count() - 1

        if from_index != to_index and 0 <= from_index < self.count() and 0 <= to_index < self.count():
            # Move tab to new position
            self._move_tab(from_index, to_index)

        event.acceptProposedAction()

    def _move_tab(self, from_index: int, to_index: int):
        """Move a tab from one position to another.

        Args:
            from_index: Current index of the tab
            to_index: Desired index for the tab
        """
        if from_index == to_index or from_index < 0 or to_index < 0:
            return

        # Get current tab widget and remove it
        widget = self.widget(from_index)
        icon = self.tabIcon(from_index)
        text = self.tabText(from_index)

        # Remove from source position
        self.removeTab(from_index)

        # Adjust target index after removal
        # When removing a tab before the target, indices shift down
        adjusted_to_index = to_index
        if from_index < to_index:
            adjusted_to_index = to_index - 1

        # Insert at destination position
        self.insertTab(adjusted_to_index, widget, icon, text)

        # Set the moved tab as current
        self.setCurrentIndex(adjusted_to_index)

        # Emit signal to notify parent of the reorder
        self.tabReordered.emit(from_index, adjusted_to_index)
