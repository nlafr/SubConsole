from PySide6.QtCore import (
    QObject, Slot, Signal, QCoreApplication, QTimer
)
import re

from settings_manager import SettingsManager


"""
        <SubShell QObject Extension. Communication Interchange for SubConsole.>
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


class SubShell(QObject):
    responseIssued = Signal(str)
    forwardCommand = Signal(str)
    forwardConsoleControl = Signal(str)
    changeBorderWidth = Signal(int)
    changeThemeBrush = Signal(str)
    changeThemeColor = Signal(str)
    changeTextColor = Signal(str)
    changeFontSize = Signal(int)
    changeFontStyle = Signal(str)
    changeBackground = Signal(str)
    changeOpacity = Signal(int)
    changeConsoleRatio = Signal(int)
    changePromptText = Signal(str)
    changeWindowTitle = Signal(str)
    windowSizeChangeCommand = Signal()
    saveSettings = Signal(bool)
    restoreSettings = Signal()
    minimizeCommand = Signal()
    def __init__(self, apps=None, manager:SettingsManager=None, parent=None):
        super().__init__(parent)
        self._windowIsFullScreen = False
        self._settingsManager = manager
        self._caseSensitiveCommands = False

        self._restorePromptText = self.settingsManager.uiPromptText
        self._headApplicationAlias = self.settingsManager.headApplicationAlias
        self._welcomeMessage = self.settingsManager.shellUiWelocmeMessageOutput
        self._invalidCommandResponse = self.settingsManager.shellInvalidCommandResponse
        self._endOperationRequest = "endOperationRequest"
        self._endOperationRequestOpCode = self.settingsManager.shellEndOperationRequestOpCode
        self._runOperationRequest = "runOperationRequest"
        self._runOperationRequestOpCode = self.settingsManager.shellRunOperationRequestOpCode
        self._uiChangeOptionRequest = "uiChangeOptionRequest"
        self._uiChangeOptionRequestOpCode = self.settingsManager.shellUiChangeOptionRequestOpCode
        self._minimizeWindowRequest = "minimizeWindowRequest"
        self._minimizeWindowRequestOpCode = self.settingsManager.shellMinimizeWindowSizeRequestOpCode
        self._changeWindowSizeRequest = "changeWindowSizeRequest"
        self._changeWindowSizeRequestOpCode = self.settingsManager.shellChangeWindowSizeRequestOpCode

        self._uiThemeColorOpCode = self.settingsManager.shellUiThemeColorOpCode
        self._uiBrushStyleOpCode = self.settingsManager.shellUiBrushStyleOpCode
        self._uiOpacityOpCode = self.settingsManager.shellUiOpacityOpCode
        self._uiTextColorOpCode = self.settingsManager.shellUiTextColorOpCode
        self._uiFontStyleOpCode = self.settingsManager.shellUiFontStyleOpCode
        self._uiFontSizeOpCode = self.settingsManager.shellUiFontSizeOpCode
        self._uiBackgroundOpCode = self.settingsManager.shellUiBackgroundOpCode
        self._uiConsoleHeightOpCode = self.settingsManager.shellUiConsoleHeightOpCode
        self._uiWelcomeMessageOpCode = self.settingsManager.shellUiWelcomeMessageOpCode
        self._headApplicationAliasOpCode = self.settingsManager.shellUiHeadApplicationAliasOpCode
        self._invalidCommandResponseOpCode = self.settingsManager.shellUiInvalidCommandResponseOpCode
        self._uiPromptTextOpCode = self.settingsManager.shellUiPromptTextOpCode
        self._uiAlwaysTopWindowOpCode = self.settingsManager.shellUiAlwaysTopWindowOpCode
        self._uiWindowTitleOpCode = self.settingsManager.shellUiWindowTitleOpCode
        self._uiSaveSettingsOpCode = self.settingsManager.shellUiSaveSettingsOpCode
        self._uiRestoreLastSaveOpCode = self.settingsManager.shellUiRestoreLastSaveOpCode

        self._uiArguments = [
            self._uiThemeColorOpCode,
            self._uiBrushStyleOpCode,
            self._uiOpacityOpCode,
            self._uiTextColorOpCode,
            self._uiFontSizeOpCode,
            self._uiFontSizeOpCode,
            self._uiBackgroundOpCode,
            self._uiConsoleHeightOpCode,
            self._uiWelcomeMessageOpCode,
            self._headApplicationAliasOpCode,
            self._invalidCommandResponseOpCode,
            self._uiPromptTextOpCode,
            self._uiWindowTitleOpCode,
            self._uiSaveSettingsOpCode,
            self._uiRestoreLastSaveOpCode,
            self._uiAlwaysTopWindowOpCode
        ]

        self._ignoreAppRequests = False
        self._appRunArgument = None
        self._flagIgnoreUiChanges = self.settingsManager.shellRunFlagIgnoreUiChanges

        self._namedFlags = [
            self._flagIgnoreUiChanges
        ]

        self._customCommandIndex = []
        self._customCommands = []
        self._customCommandArguments = []


        min_command = {
            "command": self._minimizeWindowRequestOpCode,
            "operation": self._minimizeWindowRequest,
            "argument" : None
        }
        self.addCommand(min_command)
        window_change = {
            "command": self._changeWindowSizeRequestOpCode,
            "operation": self._changeWindowSizeRequest,
            "argument": None
        }
        self.addCommand(window_change)
        help_me = ["help", "-h", "--help"]
        for help in help_me:
            helpLower = {
                "command": help,
                "operation": self._runOperationRequest,
                "argument": "HELP"
            }
            helpUpper = {
                "command": help.upper(),
                "operation": self._runOperationRequest,
                "argument": "HELP"
            }
            self.addCommand(helpLower)
            self.addCommand(helpUpper)
        ###ADD_ADDITIONAL_CUSTOM_COMMANDS###
        # customCommand = {
        #   "command": str: command, as to be acknowldedged at CLI,
        #   "operation": self._runOperationRequest | self._uiChangeOptionRequest (RUN | SET)
        #   "argument": str: argument to be passed to operation, run alias or set parameters
        # }
        # self.addCommand(customCommand)


        ###END_ADDITIONAL_CUSTOM_COMMANDS###

        self._executableAliases = self.settingsManager.executableAliases

        self._subApplicationHasConsole = False
        self._consoleControlApplication = self.headApplicationAlias
        self._subApplicationsIndex = []
        self._subApplications = []
        if apps != None:
            for app in apps:
                self.addSubApplication(app)

        self._runningApplicationsIndex = []
        self._runningApplications = []
        

    @ property
    def settingsManager(self):
        return self._settingsManager

    @ property
    def caseSensitiveCommands(self):
        return self._caseSensitiveCommands
    
    @ property
    def invalidCommandResponse(self):
        return self._invalidCommandResponse

    @ property
    def headApplicationAlias(self):
        return self._headApplicationAlias

    @ property 
    def customCommands(self):
        return self._customCommands
    
    @ property
    def customCommandIndex(self):
        return self._customCommandIndex
    
    @ property
    def subApplicationsIndex(self):
        return self._subApplicationsIndex

    @ property
    def subApplications(self):
        return self._subApplications

    @ property
    def endOperationRequest(self):
        return self._endOperationRequest
    
    @ property
    def endOperationRequestOpCode(self):
        return self._endOperationRequestOpCode
    
    @ property
    def runOperationRequest(self):
        return self._runOperationRequest
    
    @ property
    def appRunArgument(self):
        return self._appRunArgument
    
    @ property
    def flagIgnoreUiChanges(self):
        return self._flagIgnoreUiChanges
    
    @ property
    def runOperationRequestOpCode(self):
        return self._runOperationRequestOpCode
    
    @ property
    def uiChangeOptionRequest(self):
        return self._uiChangeOptionRequest

    @ property
    def uiChangeOptionRequestOpCode(self):
        return self._uiChangeOptionRequestOpCode
    
    @ property
    def minimizeWindowRequest(self):
        return self._minimizeWindowRequest
    
    @ property
    def changeWindowSizeRequest(self):
        return self._changeWindowSizeRequest
       
    @ property
    def windowIsFullScreen(self):
        return self._windowIsFullScreen

    @ property
    def uiThemeColorOpCode(self):
        return self._uiThemeColorOpCode

    @ property
    def uiBrushStyleOpCode(self):
        return self._uiBrushStyleOpCode
    
    @ property
    def uiOpacityOpCode(self):
        return self._uiOpacityOpCode
    
    @ property
    def uiTextColorOpCode(self):
        return self._uiTextColorOpCode
    
    @ property
    def uiFontSizeOpCode(self):
        return self._uiFontSizeOpCode
    
    @ property
    def uiFontStyleOpCode(self):
        return self._uiFontStyleOpCode
    
    @ property
    def uiBackgroundOpCode(self):
        return self._uiBackgroundOpCode
    
    @ property
    def uiWindowTitleOpCode(self):
        return self._uiWindowTitleOpCode
    
    @ property
    def headApplicationAliasOpCode(self):
        return self._headApplicationAliasOpCode
    
    @ property 
    def uiConsoleHeightOpCode(self):
        return self._uiConsoleHeightOpCode
    
    @ property
    def uiWelcomeMessageOpCode(self):
        return self._uiWelcomeMessageOpCode
    
    @ property
    def uiSaveSettingsOpCode(self):
        return self._uiSaveSettingsOpCode
    
    @ property
    def uiRestoreLastSaveOpCode(self):
        return self._uiRestoreLastSaveOpCode


    @ Slot()
    def emitWindowSizeChange(self):
        if self.windowIsFullScreen == True:
            self._windowIsFullScreen = False
        else:
            self._windowIsFullScreen = True
        self.windowSizeChangeCommand.emit()


    @ Slot()
    def emitMinimizeCommand(self):
        self.minimizeCommand.emit()


    @ Slot()
    def stopApplication(self):
        time = QTimer()      
        self.responseIssued.emit(f"STOPPING_{self._headApplicationAlias}....")
        time.singleShot(
            300, lambda: self.customAcknowldedgeMessage("SAVING_SETTINGS...")
        )       
        time.singleShot(900, lambda: self.sendSaveRequest(shutdown=True))
    

    def sendSaveRequest(self, shutdown=False):
        self.saveSettings.emit(shutdown)


    @ Slot()
    def concludeStopApplicationRequest(self):
        QCoreApplication.quit()


    def customAcknowldedgeMessage(self, message):
        return self.responseIssued.emit(message)
    

    @ Slot()
    def showWelcomeMessageAnimation(self, seqlen=28):
        time = QTimer()
        rate = 50
        message = ("//..........................")
        if seqlen > len(message):
            seq = len(message)
        else:
            seq = seqlen
        messages = [message[i:] for i in range(seq)]
        values = [(i * rate) for i in range(seq)]

        self.responseIssued.emit(message)
        for i in range(seq):
            time.singleShot(
                values[i], lambda i=i: self.customAcknowldedgeMessage(messages[i])
            )
        endtime = (seq + 1) * rate 
        time.singleShot(
            endtime, lambda: self.customAcknowldedgeMessage(self._welcomeMessage)
        )
    

    def addCommand(self, command):       
        if self.caseSensitiveCommands:
            self.customCommandIndex.append(command["command"].upper())
            self._customCommands.append(command["operation"].upper())     
            self._customCommandArguments.append(command["argument"].upper())
        else:
            self.customCommandIndex.append(command["command"]) 
            self._customCommands.append(command["operation"])     
            self._customCommandArguments.append(command["argument"])
        self.settingsManager._shellUiCustomCommands = self.customCommands


    def addSubApplication(self, app):
        if self.caseSensitiveCommands:
            self._subApplicationsIndex.append(app["application"].upper())
        else:
            self._subApplicationsIndex.append(app["application"])
        self._subApplications.append(app["object"])   


    def stopSubApplication(self, application):
        app = application
        if app in self._runningApplicationsIndex:
            self.forwardConsoleControl.emit(self.headApplicationAlias)
            index = self._runningApplicationsIndex.index(app)
            self._runningApplicationsIndex[index] = []
            self._ignoreAppRequests = False
            return f"{app} STOPPED"
        elif app not in self._subApplicationsIndex:
            return self.responseIssued.emit(f"{app} NOT FOUND")
        else:
            return self.responseIssued.emit(f"{app} NOT RUNNING")


    def processRunCommand(self, arguments):
        if self.caseSensitiveCommands:
            safe_arguments = arguments
        else:
            safe_arguments = arguments.upper()
        split_arguments = re.split(" ", safe_arguments, maxsplit=1)
        if len(split_arguments) == 1:
            if split_arguments[0] in self._subApplicationsIndex:
                self.responseIssued.emit(f"STARTING {arguments}")
                return self.executeRunCommand(split_arguments[0])
            elif split_arguments[0] == self.headApplicationAlias:
                return self.responseIssued.emit(f"{self.headApplicationAlias} running... cannot self propagate.")
            else:
                return self.responseIssued.emit(f"{split_arguments[0]} NOT FOUND")
        else:
            if split_arguments[0] in self._subApplicationsIndex:
                self.responseIssued.emit(f"STARTING {arguments}")
                if split_arguments[1] in self._namedFlags:
                    return self.executeRunCommand(split_arguments[0], flag=split_arguments[1])               
                else:
                    app_arguments = re.split(" ", arguments, maxsplit=1)
                    return self.executeRunCommand(split_arguments[0], flag=app_arguments[1].strip())
            else:
                return self.responseIssued.emit(f"{split_arguments[0]} NOT FOUND")



    def executeRunCommand(self, command, flag=None):
        if flag != None:
            if self.caseSensitiveCommands:
                safe_flag = flag
            else:
                safe_flag = flag.upper()
            if safe_flag == self._flagIgnoreUiChanges:
                self._ignoreAppRequests = True
            else:
                self._appRunArgument = flag
        self.forwardConsoleControl.emit(command)


    @ Slot(str)
    def forwardResponse(self, response):

            self.responseIssued.emit(response)
    

    @ Slot(str)
    def receiveSubApplicationRequest(self, request):
        if self.caseSensitiveCommands:
            safe_request = request.upper()
        else:
            safe_request = request
        if safe_request.startswith(f"{self.headApplicationAlias}$"):

            self.receiveCommand(request)
        
        elif safe_request.startswith(f"${self._consoleControlApplication}$"):
            
            self.receiveCommand(request)
        


    @ Slot(str)
    def receiveCommand(self, command):

        allocated = command
        if self.caseSensitiveCommands == False:
            safe_command = allocated.upper()
        
        if self._subApplicationHasConsole:
            if not safe_command.startswith(f"${self._consoleControlApplication}$") and not safe_command.startswith(f"{self.headApplicationAlias}$"):               

                return self.forwardCommand.emit(f"${self._consoleControlApplication}$" + command)
            elif safe_command.startswith(f"${self._consoleControlApplication}$"):
                allocated = command[len(str(self._consoleControlApplication)) + 2:]


        if self.caseSensitiveCommands == False:
            safe_command = allocated.upper()
        

        if safe_command.startswith(self.headApplicationAlias):
            safe_command = safe_command[len(str(self.headApplicationAlias)) + 1:]

        elif safe_command.startswith(f"${self._consoleControlApplication}$"):
            safe_command = safe_command[len(str(self._consoleControlApplication)) + 2:]


        if safe_command in self.customCommandIndex:
            handler = self.customCommands[self.customCommandIndex.index(safe_command)]
            custom_command = True
        else:           
            split_command = re.split(r" ", safe_command, maxsplit=1)
            if len(split_command) != 2:
                if self._subApplicationHasConsole:
                    return 
                else:
                    return self.responseIssued.emit(self.invalidCommandResponse)
            op_code = split_command[0]
            handler = self.decideHandler(op_code)
            if handler == self.invalidCommandResponse:
                if self._subApplicationHasConsole:
                    return self.forwardResponse(self.invalidCommandResponse)
                else:
                    return self.responseIssued.emit(self.invalidCommandResponse)
            custom_command = False
            safe_args = split_command[1]
            args = re.split(" ", command, maxsplit=1)[1]
        if self._subApplicationHasConsole:
            if handler != self.endOperationRequest:
                if self._ignoreAppRequests:
                    return

        match handler:
            case self.endOperationRequest:
                if custom_command == True:
                    self.stopApplication()
                elif safe_args == self.headApplicationAlias:
                    self.stopApplication()
                elif safe_args in self._runningApplicationsIndex:
                    return self.stopSubApplication(safe_args)
                else:
                    return self.stopSubApplication(safe_args)
                
            case self.runOperationRequest:
                if custom_command == True:
                    index = self._customCommandIndex.index(safe_command)
                    args = self._customCommandArguments[index]
                if not self._subApplicationHasConsole:
                    return self.processRunCommand(args)
                else:
                    return self.responseIssued.emit(
                        f"CANNOT ${self.runOperationRequestOpCode} {args} ::: {self._consoleControlApplication} :CONNECTED: {self.headApplicationAlias}:"
                    )
            case self._uiChangeOptionRequest:
                if custom_command == True:
                    index = self._customCommandIndex.index(safe_command)
                    args = self._customCommandArguments[index]
                return self.processChangeUi(args)

            
            case self.minimizeWindowRequest:
                self.emitMinimizeCommand()
                return self.responseIssued.emit("window_minimized")
            case self.changeWindowSizeRequest:
                self.emitWindowSizeChange()
                if self.windowIsFullScreen:
                    return self.responseIssued.emit("full_screen")
                else:
                    return self.responseIssued.emit("window_restored")  
            case _:
                return self.responseIssued.emit(handler)
            

    def decideHandler(self, op_code):
        match op_code:
            case self.endOperationRequestOpCode:
                return self.endOperationRequest
            case self.runOperationRequestOpCode:
                return self.runOperationRequest
            case self.uiChangeOptionRequestOpCode:
                return self.uiChangeOptionRequest
            case _:
                return self.invalidCommandResponse


    def processChangeUi(self, arguments):
        if self.caseSensitiveCommands:
            safe_arguments = arguments
        else:
            safe_arguments = arguments.upper()
        split_arguments = re.split(" ", safe_arguments, maxsplit=1)
        splitlen = len(split_arguments)
        if splitlen != 2:
            if split_arguments[0] == self._uiSaveSettingsOpCode:
                self.responseIssued.emit("SAVING_SETTINGS...")
                return self.saveSettings.emit(False)
            elif split_arguments[0] == self.uiRestoreLastSaveOpCode:
                self.responseIssued.emit("CHECKPOINT_RESTORED")
                return self.restoreSettings.emit()

            elif split_arguments[0] in self._uiArguments:
                return self.responseIssued.emit(f"{arguments} MISSING PARAMETER")
            return self.responseIssued.emit("INVALID_SETTING_ALIAS")

        parameter = split_arguments[1]
        if parameter.isspace() or parameter == "":
            return self.responseIssued.emit(f"{arguments} MISSING PARAMETER")
        match split_arguments[0]:
            case self.uiThemeColorOpCode:
                return self.changeThemeColor.emit(parameter)
            case self.uiBrushStyleOpCode:
                return self.changeThemeBrush.emit(parameter)
            case self.uiTextColorOpCode:
                return self.changeTextColor.emit(parameter)
            case self.uiFontSizeOpCode:
                try:
                    int(parameter)
                except ValueError:
                    return self.responseIssued.emit(f"{self.uiFontSizeOpCode} must be an integer")
                return self.changeFontSize.emit(int(parameter))
            case self.uiFontStyleOpCode:
                return self.changeFontStyle.emit(parameter)
            case self.uiBackgroundOpCode:
                return self.changeBackground.emit(parameter)
            case self.uiOpacityOpCode:
                try:
                    int(parameter)
                except ValueError:
                    return self.responseIssued.emit(f"{self.uiOpacityOpCode} must be an integer")
                return self.changeOpacity.emit(int(parameter))
            case self._uiConsoleHeightOpCode:
                try:
                    int(parameter)
                except ValueError:
                    return self.responseIssued.emit(f"{self.uiConsoleHeightOpCode} must be an integer")
                return self.changeConsoleRatio.emit(int(parameter))
            case self._uiWelcomeMessageOpCode:
                if self.caseSensitiveCommands == False:
                    self._welcomeMessage = re.split(" ", arguments, maxsplit=1)[1]
                else:
                    self._welcomeMessage = parameter
                self.settingsManager._shellUiWelcomeMessageOutput = self._welcomeMessage
                return self.responseIssued.emit(f"{self.uiWelcomeMessageOpCode} set to: {self._welcomeMessage}")
            case self._uiPromptTextOpCode:
                text = re.split(" ", arguments, maxsplit=1)[1]
                self.changePromptText.emit(text)
                if self._subApplicationHasConsole == False:
                    self._restorePromptText = text
                    self.settingsManager._uiPromptText = text
            case self._headApplicationAliasOpCode:
                if self._subApplicationHasConsole:
                    return self.emitRefusal(self.headApplicationAliasOpCode, self._consoleControlApplication)
                self._headApplicationAlias = parameter
                self.responseIssued.emit(f"!!! NEW {self.headApplicationAliasOpCode} !!! => SET TO::")
                self.settingsManager._headApplicationAlias = self._headApplicationAlias
                return self.responseIssued.emit(f"{self.headApplicationAlias}")
            case self._uiWindowTitleOpCode:
                title = re.split(" ", arguments, maxsplit=1)[1]
                self.changeWindowTitle.emit(title)
                return self.responseIssued.emit(f"{self.uiWindowTitleOpCode} APPLY ON RESTART")
            case self._invalidCommandResponseOpCode:
                self._invalidCommandResponse = re.split(" ", arguments, maxsplit=1)[1]
                self.settingsManager._shellInvalidCommandResponse = self._invalidCommandResponse
                return self.responseIssued.emit(f"INVALID_COMMANDS_NOW_RESPOND: {self._invalidCommandResponse}")
            case self._uiAlwaysTopWindowOpCode:
                option = re.split(" ", arguments, maxsplit=1)[1]
                if option.lower() in ["t", "true", "on"]:
                    self.settingsManager._uiAlwaysTopWindow = True
                    return self.responseIssued.emit(f"{arguments}: APPLY ON RESTART")
                elif option.lower() in ["f", "false", "off"]:
                    self.settingsManager._uiAlwaysTopWindow = False
                    return self.responseIssued.emit(f"{arguments}: APPLY ON RESTART")
                else:
                    return self.responseIssued.emit(f"{self._uiAlwaysTopWindowOpCode} must be: True | False")

            case _:
                return self.responseIssued.emit("INVALID_SETTING_ALIAS")


    def emitRefusal(self, opcode, sender):
        self.responseIssued.emit(
            f"!?!?!:REFUSED: {opcode} :REQUEST_FROM: {sender} :!?!?!"
        )



