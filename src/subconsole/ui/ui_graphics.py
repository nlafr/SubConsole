from PySide6.QtCore import (
    Qt, Slot, Signal, QPoint
)
from PySide6.QtGui import (
    QColor, QBrush, QPen,
    QFont
)
from PySide6.QtWidgets import (
    QGraphicsTextItem, QGraphicsRectItem
)


"""
        <Custom Extensions for UI Assets.>
        Copyright (C) <2026>  <Nathan LaFrazia>

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class FocusedTextInput(QGraphicsTextItem):
    enterPressed = Signal()
    def __init__(self, text, color, parent=None):
        self.color = color
        super().__init__(text, parent)

    def paint(self, painter, option, widget=None):
        # Remove state flag to remove focus border - useful
        option.state &= ~option.state.State_HasFocus
        pen = QPen(self.color)
        painter.setPen(pen)
        super().paint(painter, option, widget)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.enterPressed.emit()
            event.accept()  
        else:
            super().keyPressEvent(event)



class ClickSignalTextIcon(QGraphicsTextItem):
    iconClicked = Signal()
    def __init__(self, text, textcolor: QColor, background: QColor, brushstyle, fontfamily, parent=None):
        super().__init__(text, parent)
        self.text = text
        self.text_color = textcolor
        self.background_color = background
        self.background_brush = brushstyle
        self.setDefaultTextColor(textcolor)
        self.setFontFamily(fontfamily)

    def paint(self, painter, option, widget=None):      
        rect = self.boundingRect()
        brush = QBrush(self.background_brush)
        brush.setColor(self.background_color)
        painter.setBrush(brush)
        painter.setPen(Qt.transparent)
        painter.drawRect(rect)
        super().paint(painter, option, widget)

    def mousePressEvent(self, event):
        event.accept()
        self.iconClicked.emit()

    def setBackgroundBrush(self, brush, color):
        self.background_brush = brush
        self.background_color = color

    def setFontFamily(self, fontfamily):
        self.font_family = fontfamily
        font = QFont(fontfamily)
        font.setPointSize(12)
        self.setFont(font)



class WindowDragIcon(ClickSignalTextIcon):
    def __init__(self, *args):
        super().__init__(*args)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.dragging = False
        self.drag_start_pos = QPoint()

    def select_window(self, window):
        self.parent_window = window

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.screenPos()
            self.window_start_pos = self.parent_window.pos()
        super().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.screenPos() - self.drag_start_pos

            self.parent_window.move(self.window_start_pos + delta)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)





class FocusingRectArea(QGraphicsRectItem):
    def __init__(self, focus_item, scene, parent=None):
        self.focus_item = focus_item
        self.scene = scene       
        super().__init__(parent)

    def mousePressEvent(self, event):
        event.accept()
        self.scene.setFocusItem(self.focus_item, focusReason=Qt.ActiveWindowFocusReason)


