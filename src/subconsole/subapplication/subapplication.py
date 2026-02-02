from PySide6.QtWidgets import (
    QGraphicsRectItem, 
    QGraphicsTextItem   
)
from PySide6.QtCore import (
    Slot, Signal, Qt, QObject, QTimer,
)
from PySide6.QtGui import (
    QFont, QColor
)
from settings_manager import SettingsManager
from ui.interface import ConsoleWindow


"""
        <SubApplication Extension of QObject. Facilitates internal 'subapplication' behavior.>
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


class SubApplication(QObject):
    appResponse = Signal(str)
    sendShellCommand = Signal(str)
    appStopped = Signal(str)
    windowChanged = Signal()
    def __init__(self, alias, parent=None):
        super().__init__(parent)
        if alias.find(" ") != -1:
            raise ValueError("Application Aliases must NOT contain SPACE characters")
 
        self._applicationAlias = alias
        self._settingsManager:None|SettingsManager = None
        self._rootGraphicsSceneParent:None|ConsoleWindow = None
        self._boundaryReferenceObject:None|QGraphicsRectItem = None
        self._timer = QTimer()
        
        self._activeViewerObject = None
        self._viewerType = None
        
        self._runArgument = None
        self._ignoreInput = False
        self._screenFull = False
        self._hasConsole = False
        self._isTerminalApplication = True
        self._isInitialized = False
        self._caseSensitiveCommands = False      
        self._useUiSettings = True

        self._waitMessage = "Please Wait..."
        self._terminalPrompt = ">_"
        self._appBrushStyle = "SOLID"
        self._appBackground = "BLACK"
        self._appTextColor = "GREEN"
        self._terminalTextColor = "GREEN"
        self._appThemeColor = "GREEN"
        self._appFontSize = 14
        self._terminalFontSize = 14
        self._appFontFamily = "Courier New"
        self._terminalFontFamily = "Courier New"
        self._consoleRatio = 8
        self._xPadding = 0
        self._yPadding = 0
        

### INTERNAL METHODS

    
    def syncManager(self, manager):
        self._settingsManager = manager
        if self.settingsManager.caseSensitiveCommands:
            name = self.applicationAlias
        else:
            name = self.applicationAlias.upper()
        self._stopCode = self.settingsManager.shellEndOperationRequestOpCode + " " + name
        self._superStop = f"${self.applicationAlias}$" + self.stopCode
        


    def initializeApp(self, reference_object, parent_view):
        self._caseSensitiveCommands = self.settingsManager.caseSensitiveCommands
        self._setOpCode = self.settingsManager.shellUiChangeOptionRequestOpCode
        self._runOpCode = self.settingsManager.shellRunOperationRequestOpCode
        self._endOpCode = self.settingsManager.shellEndOperationRequestOpCode
        self._brushStyleOpCode = self.settingsManager.shellUiBrushStyleOpCode
        self._backgroundOpCode = self.settingsManager.shellUiBackgroundOpCode
        self._themeOpCode = self.settingsManager.shellUiThemeColorOpCode
        self._textColorOpCode = self.settingsManager.shellUiTextColorOpCode
        self._fontSizeOpCode = self.settingsManager.shellUiFontSizeOpCode
        self._fontStyleOpCode = self.settingsManager.shellUiFontStyleOpCode
        self._promptOpCode = self.settingsManager.shellUiPromptTextOpCode
        self._consoleOpCode = self.settingsManager.shellUiConsoleHeightOpCode
        self._welcomeOpCode = self.settingsManager.shellUiWelcomeMessageOpCode
        self._opacityOpCode = self.settingsManager.shellUiOpacityOpCode
        self._topWindowOpCode = self.settingsManager.shellUiAlwaysTopWindowOpCode
        self._windowTitleOpCode = self.settingsManager.shellUiWindowTitleOpCode
        self._invalidOpCode = self.settingsManager.shellUiInvalidCommandResponseOpCode
        self._saveOpCode = self.settingsManager.shellUiSaveSettingsOpCode
        self._restoreOpCode = self.settingsManager.shellUiRestoreLastSaveOpCode
        
        
        if self._useUiSettings:
            self._appBrushStyle = self.settingsManager.uiBrushStyleGetBrushPatternFor
            self._terminalBrushStyle = self.settingsManager.uiBrushStyleGetBrushPatternFor
            self._appBackground = self.settingsManager.uiBackgroundColorConstructor
            self._terminalBackground = self.settingsManager.uiBackgroundColorConstructor
            self._appTextColor = self.settingsManager.uiTextColorConstructor
            self._terminalTextColor = self.settingsManager.uiTextColorConstructor
            self._appThemeColor = self.settingsManager.uiThemeColorConstructor
            self._appFontSize = self.settingsManager.uiFontSizeSetting
            self._terminalFontSize = self.settingsManager.uiFontSizeSetting
            self._appFontFamily = self.settingsManager.uiFontFamilyConstructor
            self._terminalFontFamily = self.settingsManager.uiFontFamilyConstructor
            self._consoleRatio = self.settingsManager.uiConsoleRatio

        self._boundaryReferenceObject = reference_object
        self._rootGraphicsSceneParent = parent_view
        self._isInitialized = True
        self._screenFull = self._rootGraphicsSceneParent.screen_full


    def cleanLoad(self):
        if self._activeViewerObject != None:
            self._rootGraphicsSceneParent.scene.removeItem(self._activeViewerObject)
            self._activeViewerObject.deleteLater()
            self._activeViewerObject = None
        self._hasConsole = True
        self.textSettings()
        self.startupActions()



    @ Slot()
    def boundaryChanged(self):
        self._screenFull = self._rootGraphicsSceneParent.screen_full
        if self._activeViewerObject != None:       

            if self._viewerType == "widget":

                self._activeViewerObject.setMinimumSize(self.windowRect[2], self.windowRect[3])
                self._interiorWidget.setMinimumSize(self.windowRect[2], self.windowRect[3])
                self._interiorWidget.setMaximumSize(self.windowRect[2], self.windowRect[3])
        if self._hasConsole:
            self.viewerChange()


                

    @ Slot()
    def removeActiveViewer(self):
        if self._activeViewerObject != None:
            self._rootGraphicsSceneParent.scene.removeItem(self._activeViewerObject)
            self._viewerType = None
            self._activeViewerText = None



    @ Slot(str)
    def receiveCommand(self, command):
        if command.startswith(f"${self.applicationAlias}$"):
            allocated = command[len(str(self.applicationAlias)) + 2:] 
        else:
            return
        if self._ignoreInput:
            self.echo(f"{self._waitMessage}")
            return

        if self._caseSensitiveCommands:
            safe_command = allocated
        else:
            safe_command = allocated.upper()
        match safe_command:
            case self._stopCode:

                self.sendShellCommand.emit(
                    f"${self.applicationAlias}$" + self.settingsManager.shellUiChangeOptionRequestOpCode + " " + self.settingsManager.shellUiRestoreLastSaveOpCode
                )
                self.removeActiveViewer()
                self._hasConsole = False
                return self.sendShellCommand.emit(
                    f"${self.applicationAlias}$" + allocated
                )
            case self.settingsManager.shellChangeWindowSizeRequestOpCode:
                return self.sendShellCommand.emit(
                f"${self.applicationAlias}$" + allocated
                )
            case self.settingsManager.shellMinimizeWindowSizeRequestOpCode:
                self.sendShellCommand.emit(
                    f"${self.applicationAlias}$" + allocated
                )
            case _:
                if safe_command.startswith(self.settingsManager.headApplicationAlias + "$"):
                    
                    self.sendShellCommand.emit(allocated)
        return self.commandInput(safe_command, allocated)

### @ PROPERTIES

    @ property
    def settingsManager(self):
        return self._settingsManager
    
    @ property
    def windowRect(self):
        return self.rootGraphicsSceneParent.window_interior.rect().getRect()


    @ property
    def rootGraphicsSceneParent(self):
        return self._rootGraphicsSceneParent
    
    @rootGraphicsSceneParent.setter
    def setRootGraphicsScene(self, scene):
        self._rootGraphicsSceneParent = scene

    @ property
    def applicationAlias(self):
        return self._applicationAlias
    
    @ property
    def hasConsole(self):
        return self._hasConsole
    
    @ property
    def stopCode(self):
        return self._stopCode
    
    @ property
    def superStop(self):
        return self._superStop
    

    @ property
    def setOpCode(self):
        return self._setOpCode
    
    @ property
    def runOpCode(self):
        return self._runOpCode
    
    @ property
    def runArgument(self):
        return self._runArgument
    
    @ property
    def endOpCode(self):
        return self._endOpCode
    
    @ property
    def brushStyleOpCode(self):
        return self._brushStyleOpCode
    
    @ property
    def backgroundOpCode(self):
        return self._backgroundOpCode
    
    @ property
    def themeOpCode(self):
        return self._themeOpCode
    
    @ property
    def opacityOpCode(self):
        return self._opacityOpCode
    
    @ property
    def topWindowOpCode(self):
        return self._topWindowOpCode
    
    @ property
    def welcomeOpCode(self):
        return self._welcomeOpCode
    
    @ property
    def windowTitleOpCode(self):
        return self._windowTitleOpCode

    @ property
    def consoleOpCode(self):
        return self._consoleOpCode
    
    @ property
    def textColorOpCode(self):
        return self._textColorOpCode
    
    @ property
    def fontStyleOpCode(self):
        return self._fontStyleOpCode
    
    @ property
    def fontSizeOpCode(self):
        return self._fontSizeOpCode
    
    @ property
    def promptOpCode(self):
        return self._promptOpCode
    
    @ property
    def invalidOpCode(self):
        return self._invalidOpCode
    
    @ property
    def saveOpCode(self):
        return self._saveOpCode
    
    @ property
    def restoreOpCode(self):
        return self._restoreOpCode
    
    
    @ property
    def isTerminalApplication(self):
        return self._isTerminalApplication
    
    @ property
    def terminalBrushStyle(self):
        return self._terminalBrushStyle
    
    @ property
    def appBrushStyle(self):
        return self._appBrushStyle

    @ property
    def appBackground(self):
        return self._appBackground
    
    @ property
    def terminalBackground(self):
        return self._terminalBackground
    
    @ property
    def appTextColor(self):
        return self._appTextColor
    
    @ property
    def terminalTextColor(self):
        return self._terminalTextColor
    
    @ property
    def appThemeColor(self):
        return self._appThemeColor
    
    @ property
    def terminalFontSize(self):
        return self._terminalFontSize
    
    @ property
    def appFontSize(self):
        return self._appFontSize
    
    @ property
    def appFontFamily(self):
        return self._appFontFamily
    
    @ property
    def terminalFontFamily(self):
        return self._terminalFontFamily
    
    @ property
    def consoleRatio(self):
        return self._consoleRatio
    
    @ property
    def screenFull(self):
        return self._screenFull

    @ property
    def timer(self):
        return self._timer

    @ property
    def viewPadding(self):
        return (self._xPadding, self._yPadding)

### COMMAND_LINE / SHELL INTERACTIONS


    def echo(self, response:str):
        """
        Send output to the terminal.
        
        :param self: SubApplication: QObject
        :param response: Response to be sent to the terminal output
        :type response: str
        """
        self.appResponse.emit(response)


    def sendShell(self, command:str):
        """
        Docstring for sendShell
        
        :param self: SubApplication: QObject
        :param command: Command to be sent to the shell to adjust interface settings.
        :type command: str
        """
        self.sendShellCommand.emit(
            f"${self.applicationAlias}${self.settingsManager.headApplicationAlias}${command}"
        )



### VIRTUAL METHODS


    ## OVERRIDE TO RECEIVE INPUT
    def commandInput(self, safe:str, raw:str):
        """
        Virtual Method for SubApplication to receive command line input
        
        :param self: SubApplication: QObject
        :param safe: User input modified according to case-sensitivity setting. UPPERCASE if case-insensitive.
        :param raw: Raw user input with communication prefixes removed
        """
        pass


    def ingoreInput(self):
        """
        Ignores command input from terminal. Useful for wrapping renderText method animations.
        ALWAYS handle inputs in commandInput prior to calling ignoreInput, best practice is 
        to wrap rendering sequences with ignoreInput followed by acceptInput(time)
        """
        self._ignoreInput = True

    def acceptInput(self, time, buffer=200):
        """
        Docstring for acceptInput
        
        :param self: SubApplication
        :param time: int: miliseconds to wait before accepting input.
        :param buffer: int: miliseconds=200: (somewhat excessive) precautionary buffer. 
        """
        self.timer.singleShot(
            time + buffer, self.executeAcceptInput
        )

    def executeAcceptInput(self):
        self._ignoreInput = False

    def setWaitMessage(self, message):
        self._waitMessage = message



    ### APP "INIT" BEHAVIOR
    def startupActions(self):
        """
        The SubApplication object calls __init__ at read-in,
        Define this virtual method to indicate what happens
        when the application is run from the console,
        Use the shell's instruction set to change UI features
        with the method self.sendShell() 
        
        :param self: SubApplication: QObject
        """
        pass


    def viewerChange(self):
        """
        Use to describe viewer change actions, these may have multiple occurences
        so its best to use state management to decide actions to be taken.
        This occurs whenever the window size is toggled between 1/4 and full screen

        :param self: SubApplication
        """
        pass


### CONFIGURATION METHODS

    def setUseUiSettings(self, useUiSettingsTrue: bool):
        if isinstance(useUiSettingsTrue, bool):
            self._useUiSettings = useUiSettingsTrue
        else:
            raise TypeError("useUiSettingsTrue must be bool: True | False")

    def setPadding(self, x, y):
        """
        Creates padding from top left (0, 0) to initial text position.
        
        :param self: SubApplication
        :param x: int: pixels from
        :param y: int: pixels
        """
        self._xPadding = x
        self._yPadding = y

    def textSettings(self,  color=None, font=None,  size=None):
        """
        Configure Viewer text settings
        
        :param self: SubApplication
        :param color: str: color constructor: color of text
        :param font: str: font family constructor
        :param size: int: font size of text

        """
        if color != None:
            self._appTextColor = color
        elif not self._isInitialized:
            self._appTextColor = self.settingsManager.uiTextColorConstructor
        if font != None:
            self._appFontFamily = font
        elif not self._isInitialized:
            self._appFontFamily = self.settingsManager.uiFontFamilyConstructor
        if size != None:
            if not isinstance(size, int):
                raise TypeError("size must be an integer")
            self._appFontSize = size



    def themeSettings(self, theme=None, background=None, brushstyle=None):
        """
        Configure UI theme settings
        
        :param self: SubApplication
        :param theme: str: color constructor: sets border colors
        :param background: str: color constructor
        :param brushstyle: str: brushstyle

        """
        if theme != None:
            self._appThemeColor = theme
            self.sendShell(f"{self.setOpCode} {self.themeOpCode} {theme}")
        if background != None:
            self._terminalBackground = background
            self.sendShell(f"{self.setOpCode} {self.backgroundOpCode} {background}")
        if brushstyle != None:
            self._terminalBrushStyle = brushstyle
            self.sendShell(f"{self.setOpCode} {self.brushStyleOpCode} {brushstyle}")


    def terminalSettings(self, prompt=None, textcolor=None, fontsize=None, fontfamily=None, ratio=None):
        """
        Configure Terminal settings.
        
        :param self: SubApplication
        :param prompt: None | str: Prompt text
        :param textcolor: None | str: color constructor
        :param fontsize: None | int:[10-20] font size 
        :param fontfamily: None | str: font family constructor
        :param ratio: None | int: [1-9] 1/int = terminal area

        """
        if prompt != None:
            self._terminalPrompt = prompt
            self.sendShell(f"{self.setOpCode} {self.promptOpCode} {prompt}")
        if textcolor != None:
            self._terminalTextColor = textcolor
            self.sendShell(f"{self.setOpCode} {self.textColorOpCode} {textcolor}")
        if fontsize != None:
            if not isinstance(fontsize, int):
                raise TypeError("SubApplication: themeSettings() 'fontsize' must be an integer")
            self._terminalFontSize = fontsize
            self.sendShell(f"{self.setOpCode} {self.fontSizeOpCode} {fontsize}")
        if fontfamily != None:
            self._terminalFontFamily = fontfamily
            self.sendShell(f"{self.setOpCode} {self.fontStyleOpCode} {fontfamily}")
        if ratio != None:
            if not isinstance(ratio, int):
                raise TypeError("SubApplication: terminalSettings() 'ratio' must be an integer")
            elif ratio > 9 or ratio < 1:
                raise ValueError("SubApplication: terminalSettings() 'ratio':int range:[1-9]")
            self._consoleRatio = ratio
            self.sendShell(f"{self.setOpCode} {self._consoleOpCode} {ratio}")


### UI RENDER METHODS
    # Used internally by renderText and renderHTML
    def addTextItemToScene(self, center=False, interact=False):
        """
        Safely adds a QGraphicsTextItem to the window.
        
        :param self: SubApplication: QObject
        :param center: bool: Centers top of text on y axis if true
        """
        self._viewerType = "text"
        
        if self._activeViewerObject != None:
            prior_object = True
            self.removeActiveViewer()
        else:
            prior_object = False
        if prior_object:
            delete_object = self._activeViewerObject
        self._activeViewerObject = QGraphicsTextItem("")
        color = QColor(self._appTextColor)
        self._activeViewerObject.setDefaultTextColor(color)
        rect = self.windowRect
        xpos = rect[0] 
        ypos = rect[1] 
        width = rect[2]
        #height = rect[3]
        font = QFont(self._appFontFamily)
        font.setPointSize(self._appFontSize)               
        self._activeViewerObject.setFont(font)
        self._activeViewerObject.setTextWidth(width - self._xPadding)
        if not interact:
            self._activeViewerObject.setTextInteractionFlags(Qt.NoTextInteraction)
        if prior_object:
            delete_object.deleteLater()
        calculated = (xpos + self._xPadding, ypos + self._yPadding)
        if center:
            text_rect = self._activeViewerObject.boundingRect()
            window = self.windowRect
            plus_x = (window[2] / 2) - (text_rect.width() / 2) + self._xPadding
            plus_y = (window[3] / 2) - (text_rect.height() / 2) + self._yPadding
            calculated = (window[0] + plus_x, window[1] + plus_y)
        self._activeViewerObject.setPos(calculated[0], calculated[1])      
        self._rootGraphicsSceneParent.scene.addItem(self._activeViewerObject)



    def renderText(self, text, animate=True, timeout=20, center=False):
        """
        Primitive text rendering with viewer reference.
        
        SubApplication controls font features, and this method is designed to provide
        a reasonable amount of control when rendering raw text output.
              
        It accepts newline and tab escape characters, therefore the text output can
        be formatted with these special characters.

        Text is animated by default. Animated text is limited to 250 chars total.
        
        Collision with the top of the terminal area is not managed by this method , 
        and the responsibility of managing text collision with the terminal belongs
        to the SubApplication developer. Setting a terminal height is recommended
        when overriding self.startupActions() to provide a predicatble view area
        in which to format the desired text.

        :param self: SubApplication: QObject
        :param text: str: text to be rendered
        :param animate: bool: if True: Animates text: Traditional typewritter style animation
        :param timeout: int: Number of ms between re-draw: Inverse correlation to speed of text animation 
        :param center: bool: if True: Centers initial cursor vertically in the window; else: Text cursor begins at @ property self.viewPadding  
        """
        self.addTextItemToScene(center=center)
        self.activeViewerText = text

        if animate and len(text) < 250:
            rate = timeout

            values = [(i * rate) for i in range(len(text) + 2)]           
            for i in range(len(text) + 1):
                self.timer.singleShot(
                   values[i], lambda i=i: self._activeViewerObject.setPlainText(text[:i])
                )               
            return values[-1]

        else:       
            self._activeViewerObject.setPlainText(text)
            return 0        

        

    def renderHTML(self, html):
        """
        Renders valid html in the view window.

        Padding determines upper left corner.
        
        :param self: SubApplication: QObject
        :param html: str: HTML to render
        """
        
        self.addTextItemToScene()
        self._viewerType = "HTML"
        self._activeViewerText = html
        self._activeViewerObject.setHtml(html)
        




    def renderWidget(self, widget):
        """
        Renders a single QtWidget item confining to the view area.
        Override wheelEvent to accept scroll wheel events.
        
        :param self: SubApplication
        :param widget: QtWidget Object.
        """
        self._viewerType = "widget"
        if self._activeViewerObject != None:
            prior_object = True
            self.removeActiveViewer()
        else:
            prior_object = False
        if prior_object:
            delete_object = self._activeViewerObject

        self._interiorWidget = widget                
        self._interiorWidget.setMinimumSize(self.windowRect[2], self.windowRect[3])
        self._interiorWidget.setMaximumSize(self.windowRect[2], self.windowRect[3])
        
        if prior_object:
            delete_object.deleteLater()
        self._activeViewerObject = self._rootGraphicsSceneParent.scene.addWidget(self._interiorWidget)   
        self._activeViewerObject.setPos(self.windowRect[0], self.windowRect[1])