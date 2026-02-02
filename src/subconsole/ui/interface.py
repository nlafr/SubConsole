from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem,
    QGraphicsLineItem
)
from PySide6.QtGui import(
    QFont, QColor, QBrush,
    QPen,
)
from PySide6.QtCore import (
    Qt, Slot, Signal,
)
from ui.ui_graphics import (
    FocusedTextInput, FocusingRectArea,
    ClickSignalTextIcon, WindowDragIcon
)
from settings_manager import SettingsManager


"""
        <ConsoleWindow Extension for QGraphicsView. Creates User Interface.>
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


class ConsoleWindow(QGraphicsView):
    commandIssued = Signal(str)
    forwardWindowResponse = Signal(str)
    stopApplicationRequest = Signal()
    windowSizeChangeRequest = Signal()
    minimizeWindowRequest = Signal()
    windowCalculated = Signal()
    def __init__(self, size, manager:SettingsManager=None, parent=None):
        super().__init__(parent)
        self._permanentMainWindowAlias = "permanentMainWindowAlias"
        self._authorizedWindowCheckoutAlias = "authorizedWindowCheckoutAlias"
        self._settingsManager = manager
        self._controllingApplication = self.settingsManager.headApplicationAlias

        self._solidPatternOpCode = self.settingsManager.uiSolidPatternOpCode
        self._dense1PatternOpCode = self.settingsManager.uiDense1PatternOpCode
        self._dense2PatternOpCode = self.settingsManager.uiDense2PatternOpCode
        self._dense3PatternOpCode = self.settingsManager.uiDense3PatternOpCode
        self._dense4PatternOpCode = self.settingsManager.uiDense4PatternOpCode
        self._dense5PatternOpCode = self.settingsManager.uiDense5PatternOpCode
        self._dense6PatternOpCode = self.settingsManager.uiDense6PatternOpCode
        self._dense7PatternOpCode = self.settingsManager.uiDense7PatternOpCode
        self._crossPatternOpCode = self.settingsManager.uiCrossPatternOpCode
        self._diagPatternOpCode = self.settingsManager.uiDiagPatternOpCode

        self.recent_history = []

        self.screen_full = False
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        brush_style = self.getBrushPattern(self.settingsManager.uiBrushStyleGetBrushPatternFor)[0]

        self.brush_style = brush_style
        self.background_brush = QBrush(self.brush_style)
        self.background_constructor = self.settingsManager.uiBackgroundColorConstructor
        self.background_color = QColor(self.background_constructor)
        self.background_brush.setColor(self.background_color)
        self.setBackgroundBrush(self.background_brush)

        self.theme_constructor = self.settingsManager.uiThemeColorConstructor
        self.theme_color = QColor(self.theme_constructor)
        self.border_brush = QBrush(self.brush_style)
        self.border_brush.setColor(self.theme_color)

        self.text_constructor = self.settingsManager.uiTextColorConstructor
        self.text_color = QColor(self.text_constructor)
        self.text_font = QFont()
        self.font_family = self.settingsManager.uiFontFamilyConstructor
        self.text_font.setFamily(self.font_family)
        self.font_size = self.settingsManager.uiFontSizeSetting
        self.text_font.setPointSize(self.font_size)
        self.border_width = self.settingsManager.uiBorderWidth
        self.configure_border(width=self.border_width)
        self.console_ratio = self.settingsManager.uiConsoleRatio
        if self.console_ratio == 1:
            self.full_console_init = True
        else:
            self.full_console_init = False
        self.prompt_text = self.settingsManager.uiPromptText
        self.prompt_icon = QGraphicsTextItem(self.prompt_text)
        self.prompt_icon.setFont(self.text_font)
        self.prompt_icon.setDefaultTextColor(self.text_color)
        self.command_line = FocusedTextInput("", self.text_color)

        self.command_line.setDefaultTextColor(self.text_color)
        self.command_line.setFont(self.text_font)
        self.command_line.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.command_line.setTabChangesFocus(False)

        self.window_interior = QGraphicsRectItem()
        self.window_interior.setOpacity(0)
        self.console_area = FocusingRectArea(self.command_line, self.scene)
        self.console_area.setOpacity(0.1)

        self.window_drag = WindowDragIcon(
            ">_", self.theme_color, self.background_color, self.brush_style, self.font_family
        )
        self.close_button = ClickSignalTextIcon(
            "X", self.theme_color, self.background_color, self.brush_style, self.font_family
        )
        self.full_screen_button = ClickSignalTextIcon(
            "[]", self.theme_color, self.background_color, self.brush_style, self.font_family
        )
        self.minimize_button = ClickSignalTextIcon(
            "_", self.theme_color, self.background_color, self.brush_style, self.font_family
        )

        self.create_borders()        
        self.calculateWindow(size)
        self.scene.addItem(self.window_drag)
        self.scene.addItem(self.close_button)
        self.scene.addItem(self.full_screen_button)
        self.scene.addItem(self.minimize_button)
        self.scene.addItem(self.prompt_icon)
        self.scene.addItem(self.command_line)
        self.scene.addItem(self.window_interior)
        self.scene.addItem(self.console_area)
        self.calculateWindow(size)

        self.command_line.enterPressed.connect(self.command_entered)
        self.cli_document = self.command_line.document() 
        self.cli_document.contentsChanged.connect(self.limitText)
        self.window_drag.setToolTip("Drag Window")
        self.close_button.setToolTip("Exit")
        self.full_screen_button.setToolTip("Full")
        self.minimize_button.setToolTip("Minimize")
        self.close_button.iconClicked.connect(self.emitStopRequest)
        self.full_screen_button.iconClicked.connect(self.emitWindowSizeChange)
        self.minimize_button.iconClicked.connect(self.emitMinimizeRequest)
        self.focus_console()

    def wheelEvent(self, event):
        event.ignore()


    def emitStopRequest(self):
        self.stopApplicationRequest.emit()

    def emitWindowSizeChange(self):
        self.windowSizeChangeRequest.emit()

    def emitMinimizeRequest(self):
        self.minimizeWindowRequest.emit()


    def configure_border(self, width, linestyle=Qt.SolidLine, capstyle=Qt.SquareCap):
        self.border_pen = QPen(linestyle)
        self.border_pen.setCapStyle(capstyle)
        self.border_pen.setBrush(self.border_brush)
        self.border_width = width
        self.border_pen.setWidth(self.border_width)


    def create_borders(self):
        self.console_division = QGraphicsLineItem()
        self.scene.addItem(self.console_division)
        self.top_border = QGraphicsLineItem()
        self.scene.addItem(self.top_border)
        self.left_border = QGraphicsLineItem()
        self.scene.addItem(self.left_border)
        self.bottom_border = QGraphicsLineItem()
        self.scene.addItem(self.bottom_border)
        self.right_border = QGraphicsLineItem()
        self.scene.addItem(self.right_border)


    def calculateWindow(self, size):
        self.window_width = size[0]
        self.window_height = size[1]
        pad = self.border_width  - 6
        half = self.border_width / 2
        self.console_height = int(self.window_height / self.console_ratio)
        self.console_top = self.window_height - self.console_height
        self.right_interior = self.window_width - 2 * self.border_width + pad + 2
        self.left_interior = 2 * self.border_width
        self.top_interior = 2 * self.border_width
        self.bottom_interior = self.console_top
        self.console_bottom = self.window_height - 2 * self.border_width + pad
        if not self.full_console_init:
            self.console_bottom += 2

        self.console_division.setLine(
            0, self.window_height - self.console_height, self.right_interior, 
            self.window_height - self.console_height
        )
        self.console_division.setPen(self.border_pen)
        self.top_border.setLine(
            0, 0, self.right_interior, 0
        )
        self.top_border.setPen(self.border_pen)       
        self.left_border.setLine(
            0, 0, 0, self.console_bottom
        )
        self.left_border.setPen(self.border_pen)       
        self.bottom_border.setLine(
            0, self.console_bottom, self.right_interior, 
            self.console_bottom
        )
        self.bottom_border.setPen(self.border_pen)       
        self.right_border.setLine(
            self.right_interior, 0, 
            self.right_interior,
            self.console_bottom
        )
        self.right_border.setPen(self.border_pen)
        self.cursor_height = self.window_height - 2 * (self.border_width + self.font_size + 4)
        self.prompt_icon.setPos(
            self.border_width,
            self.cursor_height
        )

        self.command_line.setPos(
            self.border_width + self.prompt_icon.boundingRect().width(),
            self.cursor_height
        )

        if self.console_ratio == 1:
            focuszone = self.close_button.boundingRect().height() - 1
        else:
            focuszone = half
        self.console_area.setRect(
            half, self.console_top + focuszone, self.right_interior - self.border_width, 
            self.console_height - 2 * self.border_width - half - 1
        )
        self.window_drag.setPos(0 - half, 0 - half)
        close = self.close_button.boundingRect().width()
        full = self.full_screen_button.boundingRect().width()
        mini = self.minimize_button.boundingRect().width()
        self.interior_side_margin = (close + full + mini)
        self.window_interior.setRect(
            self.interior_side_margin - half, self.border_width,
            self.right_interior - self.interior_side_margin * 2 - close,
            self.bottom_interior - self.border_width * 2
        )
        self.close_button.setPos(self.window_width - close - half, 0 - half)
        self.full_screen_button.setPos(self.window_width - (close + full) - half, 0 - half)
        self.minimize_button.setPos(self.window_width - (close + full + mini) - half, 0 - half)
        if self.background_color.rgb() == self.theme_color.rgb():
            self.window_drag.setDefaultTextColor(self.text_color)
            self.close_button.setDefaultTextColor(self.text_color)
            self.full_screen_button.setDefaultTextColor(self.text_color)
            self.minimize_button.setDefaultTextColor(self.text_color)
        else:
            self.window_drag.setDefaultTextColor(self.theme_color)
            self.close_button.setDefaultTextColor(self.theme_color)
            self.full_screen_button.setDefaultTextColor(self.theme_color)
            self.minimize_button.setDefaultTextColor(self.theme_color)
        if self.screen_full:
            self.full_screen_button.setToolTip("Restore")
            self.window_drag.hide()
        else:
            self.full_screen_button.setToolTip("Full")
            self.window_drag.show()
        
        self.render_history(clear=True)
        self.windowCalculated.emit()



    @ property
    def settingsManager(self):
        return self._settingsManager



    def focus_console(self):
        self.scene.setFocusItem(self.command_line, focusReason=Qt.ActiveWindowFocusReason)


    def command_entered(self):       
        command_text = self.command_line.toPlainText()       
        next_line = QGraphicsTextItem()

        next_line.setPlainText(self.prompt_text + str(command_text))
        next_line.setDefaultTextColor(self.text_color)
        next_line.setFont(self.text_font)

        self.clear_history()
        self.recent_history.append(next_line)
        self.command_line.setPlainText("")
        self.render_history()
        self.commandIssued.emit(command_text)


    def limitText(self):
        if self.command_line.collidesWithItem(self.right_border):
            cursor = self.command_line.textCursor()
            cursor.deletePreviousChar()


    @ Slot(str)
    def scrollConsole(self, response):
        self.clear_history()
        if response != "":
            message = QGraphicsTextItem(response)
            message.setDefaultTextColor(self.text_color)
            message.setFont(self.text_font)
            self.recent_history.append(message)
        self.render_history()


    def clear_history(self, erase=False):
        for item in self.recent_history:
            self.scene.removeItem(item)
        if erase == True:
            self.recent_history = []


    def render_history(self, clear=False, erase=False):
        if clear == True:
            self.clear_history(erase=erase)
        history = self.cursor_height
        for i in range(len(self.recent_history)):
            
            self.recent_history[i].setPos(
                self.border_width, 
                self.cursor_height - abs(len(self.recent_history) - i) * (self.font_size * 3 / 2)
                )
            
            self.scene.addItem(self.recent_history[i])

        for item in self.recent_history:
            if item.y() < self.console_top:
                self.scene.removeItem(item)
                item.deleteLater()
                self.recent_history = self.recent_history[1:]



    @ Slot(int)
    def setThemeConsoleRatio(self, ratio):
        if ratio < 1 or ratio > 9:
            return self.forwardWindowResponse.emit("range: [1:full_window_terminal - 9:minimal_terminal], ")
        else:
            self.console_ratio = ratio
        self.calculateWindow((self.window_width, self.window_height))
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiConsoleRatio = ratio


    def getBrushPattern(self, opcode):
        match opcode:
            case self._solidPatternOpCode:
                return Qt.SolidPattern, True
            case self._dense1PatternOpCode:
                return Qt.Dense1Pattern, True
            case self._dense2PatternOpCode:
                return Qt.Dense2Pattern, True
            case self._dense3PatternOpCode:
                return Qt.Dense3Pattern, True
            case self._dense4PatternOpCode:
                return Qt.Dense4Pattern, True
            case self._dense5PatternOpCode:
                return Qt.Dense5Pattern, True
            case self._dense6PatternOpCode:
                return Qt.Dense6Pattern, True
            case self._dense7PatternOpCode:
                return Qt.Dense7Pattern, True
            case self._crossPatternOpCode:
                return Qt.CrossPattern, True
            case self._diagPatternOpCode:
                return Qt.DiagCrossPattern, True
            case _:
                return Qt.SolidPattern, False



    @ Slot(str)
    def setThemeBrush(self, brush):
        self.background_constructor = brush.strip()
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiBrushStyleGetBrushPatternFor = brush
        new_brush = self.getBrushPattern(brush)
        if new_brush[1] == False:
            return self.forwardWindowResponse.emit("INVALID_PARAMETER")
        self.brush_style = new_brush[0]
        border_brush = QBrush(new_brush[0])
        self.border_brush = border_brush
        border_brush.setColor(self.theme_color)
        background_brush = QBrush(new_brush[0])
        self.background_brush = background_brush
        self.border_pen.setBrush(border_brush)
        self.background_brush.setColor(self.background_color)
        self.setBackgroundBrush(background_brush)
        self.window_drag.setBackgroundBrush(background_brush, self.background_color)
        self.close_button.setBackgroundBrush(background_brush, self.background_color)
        self.full_screen_button.setBackgroundBrush(background_brush, self.background_color)
        self.minimize_button.setBackgroundBrush(background_brush, self.background_color)

        self.calculateWindow((self.window_width, self.window_height))
        return self.forwardWindowResponse.emit(f"{self.settingsManager.shellUiBrushStyleOpCode} set to {brush}")


    @ Slot(str)
    def setThemeColor(self, color):
        self.theme_constructor = color.strip()
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiThemeColorConstructor
        self.settingsManager._uiThemeColorConstructor = self.theme_constructor
        self.theme_color = QColor(color) 
        self.border_brush = QBrush(self.brush_style)
        self.border_brush.setColor(self.theme_color)
        self.border_pen.setBrush(self.border_brush)
        self.window_drag.setDefaultTextColor(self.theme_color)
        self.close_button.setDefaultTextColor(self.theme_color)
        self.full_screen_button.setDefaultTextColor(self.theme_color)
        self.minimize_button.setDefaultTextColor(self.theme_color)
        self.calculateWindow((self.window_width, self.window_height))
        
        if self.theme_color.rgb() == self.background_color.rgb():
            return self.forwardWindowResponse.emit(f"!{self.settingsManager.shellUiThemeColorOpCode} SET TO {self.settingsManager.shellUiBackgroundOpCode} COLOR!")
        else:
            return self.forwardWindowResponse.emit(f"{self.settingsManager.shellUiThemeColorOpCode} set to {color}")


    @ Slot(str) 
    def setThemeTextColor(self, color):
        new_color = QColor(color)
        if new_color.rgb() == self.background_color.rgb():
            return self.forwardWindowResponse.emit(f"CANNOT SET {self.settingsManager.shellUiTextColorOpCode} TO {self.settingsManager.shellUiBackgroundOpCode} COLOR")
        self.text_constructor = color.strip()
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiTextColorConstructor = self.text_constructor
        self.text_color = new_color
        self.prompt_icon.setDefaultTextColor(self.text_color)
        self.command_line.setDefaultTextColor(self.text_color)
        self.calculateWindow((self.window_width, self.window_height))
        return self.forwardWindowResponse.emit(f"{self.settingsManager.shellUiTextColorOpCode} set to {color}")


    @ Slot(int)
    def setThemeFontSize(self, size):
        if size < 10 or size > 20:
            return self.forwardWindowResponse.emit("range: [10-20]")
        self.font_size = size
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiFontSizeSetting = self.font_size
        self.text_font.setPointSize(self.font_size)
        self.command_line.setFont(self.text_font)
        self.prompt_icon.setFont(self.text_font)
        self.calculateWindow((self.window_width, self.window_height))
        self.forwardWindowResponse.emit(f"{self.settingsManager.shellUiFontSizeOpCode} set to {size}")


    @ Slot(str)
    def setThemeFontStyle(self, style):
        self.font_family = style
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiFontFamilyConstructor = style
        self.text_font.setFamily(style)
        self.command_line.setFont(self.text_font)
        self.prompt_icon.setFont(self.text_font)
        self.window_drag.setFontFamily(style)
        self.minimize_button.setFontFamily(style)
        self.full_screen_button.setFontFamily(style)
        self.close_button.setFontFamily(style)
        self.calculateWindow((self.window_width, self.window_height))
        self.forwardWindowResponse.emit(f"{self.settingsManager.shellUiFontStyleOpCode} set to {style}")


    @ Slot(str)
    def setThemeBackgroundColor(self, color):
        new_color = QColor(color)

        if new_color.rgb() == self.text_color.rgb():
            return self.forwardWindowResponse.emit(f"CANNOT SET {self.settingsManager.shellUiBackgroundOpCode} TO {self.settingsManager.shellUiTextColorOpCode} COLOR")
        self.background_constructor = color
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiBackgroundColorConstructor = self.background_constructor
        self.background_color = new_color
        self.background_brush = QBrush(self.brush_style)
        self.background_brush.setColor(self.background_color)
        self.setBackgroundBrush(self.background_brush)
        self.window_drag.setBackgroundBrush(self.background_brush, self.background_color)
        self.minimize_button.setBackgroundBrush(self.background_brush, self.background_color)
        self.full_screen_button.setBackgroundBrush(self.background_brush, self.background_color)
        self.close_button.setBackgroundBrush(self.background_brush, self.background_color)
        self.calculateWindow((self.window_width, self.window_height))
        if new_color.rgb() == self.theme_color.rgb():
            return self.forwardWindowResponse.emit(f"!{self.settingsManager.shellUiBackgroundOpCode} SET TO {self.settingsManager.shellUiThemeColorOpCode} COLOR!")
        return self.forwardWindowResponse.emit(f"{self.settingsManager.shellUiBackgroundOpCode} set to {color}")
    
    @ Slot(str)
    def setPromptText(self, text):
        if self._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._uiPromptText = text
        self.prompt_text = text
        self.prompt_icon.setPlainText(text)
        self.calculateWindow((self.window_width, self.window_height))
        