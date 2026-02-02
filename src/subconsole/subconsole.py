import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QStackedWidget, QSizePolicy,
)
from PySide6.QtCore import (
    Qt, Slot, Signal
)
from ui.interface import ConsoleWindow
from core.subshell import SubShell
from settings_manager import SettingsManager
from scripts.script_manager import ScriptManager
from subapplication.subapplication import SubApplication


"""
        <SubConsoleGUI Extension for QMainWindow. Main Python Callable for SubConsole>
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


class SubConsoleGUI(QMainWindow):
    confirmStopApplication = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._settingsManager = SettingsManager()
        screen = QApplication.primaryScreen()
        self.max_size = screen.availableGeometry().size()
        self.window_size = (self.max_size.width() / 2, self.max_size.height() / 2)
        self.window_title = self.settingsManager.windowTitle
        self.setWindowTitle(self.window_title)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.main_window = ConsoleWindow(self.window_size, manager=self.settingsManager)
        self.sub_shell = SubShell(manager=self.settingsManager)
        self.connection_index = []
        self.active_apps = {}

        self.running_application = self.settingsManager.headApplicationAlias

        self.script_manager = ScriptManager()
        self.script_manager.load_apps()
        self.addScripts(self.script_manager.apps)
        

        self.window_opacity = self.settingsManager.windowOpacity
        self.update_window_opacity = self.settingsManager.windowOpacity
        if self.settingsManager.uiAlwaysTopWindow:
            self.setWindowFlags(Qt.FramelessWindowHint  | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(self.window_opacity)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.main_window.setSizePolicy(self.size_policy)
        self.main_window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_window.resize(self.window_size[0], self.window_size[1])

        self.central_widget.addWidget(self.main_window)

        self.main_window.window_drag.select_window(self)

        self.main_window.commandIssued.connect(self.sub_shell.receiveCommand)
        self.sub_shell.responseIssued.connect(self.main_window.scrollConsole)
        self.main_window.stopApplicationRequest.connect(self.sub_shell.stopApplication)
        self.main_window.windowSizeChangeRequest.connect(self.sub_shell.emitWindowSizeChange)
        self.sub_shell.windowSizeChangeCommand.connect(self.toggleScreenSize)
        self.main_window.minimizeWindowRequest.connect(self.sub_shell.emitMinimizeCommand)
        self.sub_shell.minimizeCommand.connect(self.minimizeWindow)
        self.sub_shell.saveSettings.connect(self.saveSettings)
        self.sub_shell.restoreSettings.connect(self.restoreSettings)
        self.confirmStopApplication.connect(self.sub_shell.concludeStopApplicationRequest)

        self.sub_shell.changeThemeColor.connect(self.main_window.setThemeColor)
        self.sub_shell.changeThemeBrush.connect(self.main_window.setThemeBrush)
        self.sub_shell.changeTextColor.connect(self.main_window.setThemeTextColor)
        self.sub_shell.changeFontSize.connect(self.main_window.setThemeFontSize)
        self.sub_shell.changeFontStyle.connect(self.main_window.setThemeFontStyle)
        self.sub_shell.changeBackground.connect(self.main_window.setThemeBackgroundColor)
        self.sub_shell.changeOpacity.connect(self.setThemeOpacity)
        self.sub_shell.changeConsoleRatio.connect(self.main_window.setThemeConsoleRatio)
        self.sub_shell.changePromptText.connect(self.main_window.setPromptText)
        self.sub_shell.changeWindowTitle.connect(self.setThemeTitle)
        self.main_window.forwardWindowResponse.connect(self.sub_shell.forwardResponse)
        self.sub_shell.forwardConsoleControl.connect(self.manageConsoleControl)


    @ property
    def settingsManager(self):
        return self._settingsManager

    def addScripts(self, scripts:list[SubApplication]):
        for script in scripts:
            script.syncManager(self._settingsManager)
            self.sub_shell._subApplications.append(script)
            self.sub_shell._subApplicationsIndex.append(script.applicationAlias)
            self.connection_index.append(False)
            

    def minimizeWindow(self):
        self.showMinimized()

    def toggleScreenSize(self):
        if self.main_window.screen_full == True:
            self.main_window.screen_full = False
            self.showNormal()           
        else:
            self.main_window.screen_full = True
            self.showFullScreen()
            self.main_window.calculateWindow((self.max_size.width(), self.max_size.height()))


    def resizeEvent(self, event):
        super().resizeEvent(event)
        new = event.size()
        newsize = (new.width(), new.height())
        self.main_window.calculateWindow(newsize)


    @ Slot(str)
    def setThemeTitle(self, title):
        if self.main_window._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._windowTitle = title
        self.window_title = title


    @ Slot(int)
    def setThemeOpacity(self, opacity):
        if opacity < 0 or opacity > 10:
            return "range: [0-10]"
        self.update_window_opacity = 0.8 + ((2 * opacity) / 100)
        if self.main_window._controllingApplication == self.settingsManager.headApplicationAlias:
            self.settingsManager._windowOpacity = self.update_window_opacity
        self.main_window.forwardWindowResponse.emit("Restart application for new opacity")


    @ Slot(str)
    def manageConsoleControl(self, application):
        if self.settingsManager.caseSensitiveCommands:
            controller = application
        else:
            controller = application.upper()
        if controller == self.sub_shell.headApplicationAlias:
            index = self.sub_shell.subApplicationsIndex.index(self.sub_shell._consoleControlApplication)   
            self.main_window.forwardWindowResponse.emit(f"STOPPING {self.running_application}")
            self.running_application = self.sub_shell.headApplicationAlias
            self.main_window._controllingApplication = self.sub_shell._headApplicationAlias
            self.sub_shell._consoleControlApplication = self.settingsManager.headApplicationAlias
            self.sub_shell._subApplicationHasConsole = False
            self.sub_shell._ignoreAppRequests = False

        elif controller in self.sub_shell.subApplicationsIndex:
            self.running_application = controller
            self.sub_shell._subApplicationHasConsole = True
            self.main_window._controllingApplication = controller
            self.sub_shell._consoleControlApplication = controller

            self.sub_shell._subApplicationHasConsole = True
            
            self.sub_shell._runningApplicationsIndex.append(controller)
            index = self.sub_shell.subApplicationsIndex.index(controller)
            app: SubApplication = self.sub_shell.subApplications[index]
            app.syncManager(self.settingsManager) 

            if self.connection_index[index] == False:
                app: SubApplication = self.sub_shell.subApplications[index]
                app.initializeApp(self.main_window.window_interior, self.main_window)
                self.connection_index[index] = True
                self.sub_shell.forwardCommand.connect(app.receiveCommand)
                self.main_window.windowCalculated.connect(app.boundaryChanged)
                app.appResponse.connect(self.sub_shell.forwardResponse)
                app.sendShellCommand.connect(self.sub_shell.receiveSubApplicationRequest)
                app.appStopped.connect(self.manageConsoleControl)
                
            if app._activeViewerObject != None:
                delete_later = app._activeViewerObject
                app._activeViewerObject = None
                delete_later.deleteLater()
            app._runArgument = self.sub_shell.appRunArgument
            app.cleanLoad()

        else:
            self.running_application = self.sub_shell.headApplicationAlias
            self.main_window._controllingApplication = self.sub_shell._headApplicationAlias           
            self.sub_shell._consoleControlApplication = self.settingsManager.headApplicationAlias
            self.sub_shell._subApplicationHasConsole = False
            self.sub_shell._ignoreAppRequests = False
            self.main_window.forwardWindowResponse.emit(f"INVALID_APPLICATION_REQUEST: Defaulting to {self.sub_shell._headApplicationAlias}")



    @ Slot(bool)
    def saveSettings(self, shutdown):
        self.settingsManager.saveSettings()
        self.sub_shell.responseIssued.emit("SAVED")
        if shutdown:
            self.confirmStopApplication.emit()
        else:
            self.settingsManager.loadSettings()


    @ Slot()
    def restoreSettings(self):
        self.settingsManager.commitLoadFile()
        self.main_window.setThemeConsoleRatio(self.settingsManager.uiConsoleRatio)
        
        self.main_window.setThemeBrush(self.settingsManager.uiBrushStyleGetBrushPatternFor)
        self.main_window.setThemeColor(self.settingsManager.uiThemeColorConstructor)
        self.main_window.setThemeTextColor(self.settingsManager.uiTextColorConstructor)
        self.main_window.setThemeFontSize(self.settingsManager.uiFontSizeSetting)
        self.main_window.setThemeFontStyle(self.settingsManager.uiFontFamilyConstructor)
        self.main_window.setThemeBackgroundColor(self.settingsManager.uiBackgroundColorConstructor)
        self.main_window.setPromptText(self.settingsManager.uiPromptText)
        self.main_window.calculateWindow((self.main_window.window_width, self.main_window.window_height))



def main():
    app = QApplication()
    gui = SubConsoleGUI()
    size = gui.window_size
    gui.resize(size[0], size[1])
    gui.show()
    gui.sub_shell.showWelcomeMessageAnimation()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()