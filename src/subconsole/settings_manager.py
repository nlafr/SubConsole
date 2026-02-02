import json
from json import JSONDecodeError

RELATIVE_PATH_TO_SETTINGS = "disk/settings.json"


"""
        <SettingsManager class definition. Manages Settings>
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


class SettingsManager:
    def __init__(self):
        self.loadSettings()
    
    # GLOBAL
    @ property
    def windowTitle(self):
        return self._windowTitle
    
    @ property
    def caseSensitiveCommands(self):
        return self._caseSensitiveCommands
    
    @ property
    def headApplicationAlias(self):
        return self._headApplicationAlias
    
    @ property
    def windowOpacity(self):
        return self._windowOpacity



    # SHELL

    @ property
    def shellUiWelocmeMessageOutput(self):
        return self._shellUiWelcomeMessageOutput
    
    @ property
    def shellInvalidCommandResponse(self):
        return self._shellInvalidCommandResponse
    
    @ property
    def shellUiInvalidCommandResponseOpCode(self):
        return self._shellUiInvalidCommandResponseOpCode
    
    @ property
    def shellEndOperationRequestOpCode(self):
        return self._shellEndOperationRequestOpCode
    
    @ property
    def shellRunOperationRequestOpCode(self):
        return self._shellRunOperationRequestOpCode
    
    @ property
    def shellRunFlagIgnoreUiChanges(self):
        return self._shellRunFlagIgnoreUiChanges
    
    @ property
    def shellUiChangeOptionRequestOpCode(self):
        return self._shellUiChangeOptionRequestOpCode
    
    @ property
    def shellMinimizeWindowSizeRequestOpCode(self):
        return self._shellMinmizeWindowRequestOpCode
    
    @ property
    def shellChangeWindowSizeRequestOpCode(self):
        return self._shellChangeWindowSizeRequestOpCode
    
    @ property
    def shellAddCustomCommandRequestOpCode(self):
        return self._shellAddCustomCommandRequestOpCode
    
    @ property
    def shellUiThemeColorOpCode(self):
        return self._shellUiThemeColorOpCode
    
    @ property
    def shellUiBrushStyleOpCode(self):
        return self._shellUiBrushStyleOpCode
    
    @ property
    def shellUiOpacityOpCode(self):
        return self._shellUiOpacityOpCode
    
    @ property
    def shellUiTextColorOpCode(self):
        return self._shellUiTextColorOpCode
    
    @ property
    def shellUiFontStyleOpCode(self):
        return self._shellUiFontStyleOpCode
    
    @ property
    def shellUiFontSizeOpCode(self):
        return self._shellUiFontSizeOpCode
    
    @ property
    def shellUiBackgroundOpCode(self):
        return self._shellUiBackgroundOpCode
    
    @ property
    def shellUiConsoleHeightOpCode(self):
        return self._shellUiConsoleHeightOpCode
    
    @ property
    def shellUiWelcomeMessageOpCode(self):
        return self._shellUiWelcomeMessageOpCode
    
    @ property
    def shellUiInvalidCommandResponseOpCode(self):
        return self._shellUiInvalidCommandResponseOpCode
    
    @ property
    def shellUiHeadApplicationAliasOpCode(self):
        return self._shellUiHeadApplicationAliasOpCode
    
    @ property
    def shellUiWindowTitleOpCode(self):
        return self._shellUiWindowTitleOpCode
    
    @ property
    def shellUiPromptTextOpCode(self):
        return self._shellUiPromptTextOpCode
    
    @ property
    def shellUiAlwaysTopWindowOpCode(self):
        return self._shellUiAlwaysTopWindowOpCode
    
    @ property
    def shellUiSaveSettingsOpCode(self):
        return self._shellUiSaveSettingsOpCode
    
    @ property
    def shellUiRestoreLastSaveOpCode(self):
        return self._shellUiRestoreLastSaveOpCode
    
    @ property
    def executableAliases(self):
        return self._executableAliases
    

    #UI
    
    @ property
    def uiSolidPatternOpCode(self):
        return self._uiSolidPatternOpCode
    
    @ property
    def uiDense1PatternOpCode(self):
        return self._uiDense1PatternOpCode
    
    @ property
    def uiDense2PatternOpCode(self):
        return self._uiDense2PatternOpCode
    
    @ property
    def uiDense3PatternOpCode(self):
        return self._uiDense3PatternOpCode
    
    @ property
    def uiDense4PatternOpCode(self):
        return self._uiDense4PatternOpCode
    
    @ property
    def uiDense5PatternOpCode(self):
        return self._uiDense5PatternOpCode
    
    @ property
    def uiDense6PatternOpCode(self):
        return self._uiDense6PatternOpCode
    
    @ property
    def uiDense7PatternOpCode(self):
        return self._uiDense7PatternOpCode
    
    @ property
    def uiCrossPatternOpCode(self):
        return self._uiCrossPatternOpCode
    
    @ property
    def uiDiagPatternOpCode(self):
        return self._uidiagPatternOpCode
    
    @ property
    def uiBrushStyleGetBrushPatternFor(self):
        return self._uiBrushStyleGetBrushPatternFor
    
    @ property
    def uiBackgroundColorConstructor(self):
        return self._uiBackgroundColorConstructor
    
    @ property
    def uiThemeColorConstructor(self):
        return self._uiThemeColorConstructor
    
    @ property
    def uiTextColorConstructor(self):
        return self._uiTextColorConstructor
    
    @ property
    def uiFontFamilyConstructor(self):
        return self._uiFontFamilyConstructor
    
    @ property
    def uiFontSizeSetting(self):
        return self._uiFontSizeSetting
    
    @ property
    def uiBorderWidth(self):
        return self._uiBorderWidth
    
    @ property
    def uiConsoleRatio(self):
        return self._uiConsoleRatio
    
    @ property
    def uiPromptText(self):
        return self._uiPromptText
    
    @ property
    def uiAlwaysTopWindow(self):
        return self._uiAlwaysTopWindow
    

    def loadSettings(self):
        try:
            with open(RELATIVE_PATH_TO_SETTINGS, "r") as file:
                settings = json.load(file)
                self.loadFromFile(settings)
        except FileNotFoundError:
            self.fallBackSettings()
        
        except JSONDecodeError:
            self.fallBackSettings()
        

    def saveSettings(self):
        config = {
        
            #GLOBAL
            "windowTitle": self._windowTitle,
            "caseSensitiveCommands": self._caseSensitiveCommands,
            "headApplicationAlias": self._headApplicationAlias,
            "windowOpacity": self._windowOpacity,
            # SHELL
            "shellUiWelcomeMessageOutput": self._shellUiWelcomeMessageOutput,
            "shellInvalidCommandResponse": self._shellInvalidCommandResponse,
            "shellEndOperationRequestOpCode": self._shellEndOperationRequestOpCode,
            "shellRunOperationRequestOpCode": self._shellRunOperationRequestOpCode,
            "shellUiChangeOptionRequestOpCode": self._shellUiChangeOptionRequestOpCode,
            "shellMinimizeWindowRequestOpCode": self._shellMinmizeWindowRequestOpCode,
            "shellChangeWindowSizeRequestOpCode": self._shellChangeWindowSizeRequestOpCode,
            "shellAddCustomCommandRequestOpCode": self._shellAddCustomCommandRequestOpCode,
            "shellUiThemeColorOpCode": self._shellUiThemeColorOpCode,
            "shellUiBrushStyleOpCode": self._shellUiBrushStyleOpCode,
            "shellUiOpacityOpCode": self._shellUiOpacityOpCode,
            "shellUiTextColorOpCode": self._shellUiTextColorOpCode,
            "shellUiFontStyleOpCode": self._shellUiFontStyleOpCode,
            "shellUiFontSizeOpCode": self._shellUiFontSizeOpCode,
            "shellUiBackgroundOpCode": self._shellUiBackgroundOpCode,
            "shellUiConsoleHeightOpCode": self._shellUiConsoleHeightOpCode,
            "shellUiWelcomeMessageOpCode": self._shellUiWelcomeMessageOpCode,   
            "shellUiInvalidCommandResponseOpCode":self._shellUiInvalidCommandResponseOpCode,
            "shellUiHeadApplicationAliasOpCode": self._shellUiHeadApplicationAliasOpCode,
            "shellUiWindowTitleOpCode": self._shellUiWindowTitleOpCode,
            "shellUiPromptTextOpCode": self._shellUiPromptTextOpCode,
            "shellUiAlwaysTopWindowOpCode": self._shellUiAlwaysTopWindowOpCode,
            "shellUiSaveSettingsOpCode": self._shellUiSaveSettingsOpCode,
            "shellUiRestoreLastSaveOpCode": self._shellUiRestoreLastSaveOpCode,
            "executableAliases": self._executableAliases,
            "shellRunFlagIgnoreUiChanges": self._shellRunFlagIgnoreUiChanges,
            

            #UI
            "uiSolidPatternOpCode": self._uiSolidPatternOpCode,
            "uiDense1PatternOpCode": self._uiDense1PatternOpCode,
            "uiDense2PatternOpCode": self._uiDense2PatternOpCode,
            "uiDense3PatternOpCode": self._uiDense3PatternOpCode,
            "uiDense4PatternOpCode": self._uiDense4PatternOpCode,
            "uiDense5PatternOpCode": self._uiDense5PatternOpCode,
            "uiDense6PatternOpCode": self._uiDense6PatternOpCode,
            "uiDense7PatternOpCode": self._uiDense7PatternOpCode,
            "uiCrossPatternOpCode": self._uiCrossPatternOpCode,
            "uiDiagPatternOpCode": self._uidiagPatternOpCode,

            "uiBrushStyleGetBrushPatternFor": self._uiBrushStyleGetBrushPatternFor,
            "uiBackgroundColorConstructor": self._uiBackgroundColorConstructor,
            "uiThemeColorConstructor": self._uiThemeColorConstructor,
            "uiTextColorConstructor": self._uiTextColorConstructor,
            "uiFontFamilyConstructor": self._uiFontFamilyConstructor,
            "uiFontSizeSetting": self._uiFontSizeSetting,
            "uiBorderWidth": self._uiBorderWidth,
            "uiConsoleRatio": self._uiConsoleRatio,
            "uiPromptText": self._uiPromptText,
            "uiAlwaysTopWindow": self._uiAlwaysTopWindow
        }
        
        with open(RELATIVE_PATH_TO_SETTINGS, "w") as file:
            json.dump(config, file, indent=4)

    def loadFromFile(self, settings):
        self.config = settings
        self.commitLoadFile()

    def commitLoadFile(self):
        #GLOBAL
        self._windowTitle = self.config["windowTitle"]
        self._caseSensitiveCommands = self.config["caseSensitiveCommands"]
        self._windowIsFullScreen = False
        self._headApplicationAlias = self.config["headApplicationAlias"]
        self._windowOpacity = self.config["windowOpacity"]

        #SHELL
        self._shellUiWelcomeMessageOutput = self.config["shellUiWelcomeMessageOutput"]
        self._shellInvalidCommandResponse = self.config["shellInvalidCommandResponse"]
        self._shellEndOperationRequestOpCode = self.config["shellEndOperationRequestOpCode"]
        self._shellRunOperationRequestOpCode = self.config["shellRunOperationRequestOpCode"]
        self._shellUiChangeOptionRequestOpCode = self.config["shellUiChangeOptionRequestOpCode"]
        self._shellMinmizeWindowRequestOpCode = self.config["shellMinimizeWindowRequestOpCode"]
        self._shellChangeWindowSizeRequestOpCode = self.config["shellChangeWindowSizeRequestOpCode"]
        self._shellAddCustomCommandRequestOpCode = self.config["shellAddCustomCommandRequestOpCode"]
        self._shellUiThemeColorOpCode = self.config["shellUiThemeColorOpCode"]
        self._shellUiBrushStyleOpCode = self.config["shellUiBrushStyleOpCode"]
        self._shellUiOpacityOpCode = self.config["shellUiOpacityOpCode"]
        self._shellUiTextColorOpCode = self.config["shellUiTextColorOpCode"]
        self._shellUiFontStyleOpCode = self.config["shellUiFontStyleOpCode"]
        self._shellUiFontSizeOpCode = self.config["shellUiFontSizeOpCode"]
        self._shellUiBackgroundOpCode = self.config["shellUiBackgroundOpCode"]
        self._shellUiConsoleHeightOpCode = self.config["shellUiConsoleHeightOpCode"]
        self._shellUiWelcomeMessageOpCode = self.config["shellUiWelcomeMessageOpCode"]
        self._shellUiInvalidCommandResponseOpCode = self.config["shellUiInvalidCommandResponseOpCode"]
        self._shellUiHeadApplicationAliasOpCode = self.config["shellUiHeadApplicationAliasOpCode"]
        self._shellUiWindowTitleOpCode = self.config["shellUiWindowTitleOpCode"]
        self._shellUiPromptTextOpCode = self.config["shellUiPromptTextOpCode"]
        self._shellUiAlwaysTopWindowOpCode = self.config["shellUiAlwaysTopWindowOpCode"]
        self._shellUiSaveSettingsOpCode = self.config["shellUiSaveSettingsOpCode"]
        self._shellUiRestoreLastSaveOpCode = self.config["shellUiRestoreLastSaveOpCode"]
        self._executableAliases = self.config["executableAliases"]
        self._shellRunFlagIgnoreUiChanges = self.config["shellRunFlagIgnoreUiChanges"]

        #UI
        self._uiSolidPatternOpCode = self.config["uiSolidPatternOpCode"]
        self._uiDense1PatternOpCode = self.config["uiDense1PatternOpCode"]
        self._uiDense2PatternOpCode = self.config["uiDense2PatternOpCode"]
        self._uiDense3PatternOpCode = self.config["uiDense3PatternOpCode"]
        self._uiDense4PatternOpCode = self.config["uiDense4PatternOpCode"]
        self._uiDense5PatternOpCode = self.config["uiDense5PatternOpCode"]
        self._uiDense6PatternOpCode = self.config["uiDense6PatternOpCode"]
        self._uiDense7PatternOpCode = self.config["uiDense7PatternOpCode"]
        self._uiCrossPatternOpCode = self.config["uiCrossPatternOpCode"]
        self._uidiagPatternOpCode = self.config["uiDiagPatternOpCode"]

        self._uiBrushStyleGetBrushPatternFor = self.config["uiBrushStyleGetBrushPatternFor"]
        self._uiBackgroundColorConstructor = self.config["uiBackgroundColorConstructor"]
        self._uiThemeColorConstructor = self.config["uiThemeColorConstructor"]
        self._uiTextColorConstructor = self.config["uiTextColorConstructor"]
        self._uiFontFamilyConstructor = self.config["uiFontFamilyConstructor"]
        self._uiFontSizeSetting = self.config["uiFontSizeSetting"]
        self._uiBorderWidth = self.config["uiBorderWidth"]
        self._uiConsoleRatio = self.config["uiConsoleRatio"]
        self._uiPromptText = self.config["uiPromptText"]
        self._uiAlwaysTopWindow = self.config["uiAlwaysTopWindow"]

    def fallBackSettings(self):
        #GLOBAL/CONSOLE
        self._windowTitle = "SubConsole"
        self._caseSensitiveCommands = False
        self._windowIsFullScreen = False
        self._headApplicationAlias = "SUBCONSOLE"
        self._windowOpacity = 0.9

        #SHELL
        self._shellUiWelcomeMessageOutput = "Hello, World"
        self._shellInvalidCommandResponse = "INVALID_COMMAND"
        self._shellEndOperationRequestOpCode = "END"
        self._shellRunOperationRequestOpCode = "RUN"
        self._shellUiChangeOptionRequestOpCode = "SET"
        self._shellMinmizeWindowRequestOpCode = "MIN"
        self._shellChangeWindowSizeRequestOpCode = "WIN"
        self._shellAddCustomCommandRequestOpCode = "ADD"
        self._shellUiThemeColorOpCode = "THEME"
        self._shellUiBrushStyleOpCode = "STYLE"
        self._shellUiOpacityOpCode = "OPACITY"
        self._shellUiTextColorOpCode = "TEXT"
        self._shellUiFontStyleOpCode = "FONT"
        self._shellUiFontSizeOpCode = "SIZE"
        self._shellUiBackgroundOpCode = "SCREEN"
        self._shellUiConsoleHeightOpCode = "TERMINAL"
        self._shellUiWelcomeMessageOpCode = "WELCOME"
        self._shellUiInvalidCommandResponseOpCode = "INVALID"
        self._shellUiHeadApplicationAliasOpCode = "HEAD_ALIAS"
        self._shellUiWindowTitleOpCode = "TITLE"
        self._shellUiPromptTextOpCode = "PROMPT"
        self._shellUiAlwaysTopWindowOpCode = "TOP_WINDOW"
        self._shellUiSaveSettingsOpCode = "SAVE"
        self._shellUiRestoreLastSaveOpCode = "BACK"


        self._executableAliases = []
        self._shellRunFlagIgnoreUiChanges = "IGNORE"
        

        #UI
    
        self._uiSolidPatternOpCode = "SOLID"
        self._uiDense1PatternOpCode = "DENSE1"
        self._uiDense2PatternOpCode = "DENSE2"
        self._uiDense3PatternOpCode = "DENSE3"
        self._uiDense4PatternOpCode = "DENSE4"
        self._uiDense5PatternOpCode = "DENSE5"
        self._uiDense6PatternOpCode = "DENSE6"
        self._uiDense7PatternOpCode = "DENSE7"
        self._uiCrossPatternOpCode = "GRID"
        self._uidiagPatternOpCode = "DIAG"

        self._uiBrushStyleGetBrushPatternFor = "DENSE1"
        self._uiBackgroundColorConstructor = "BLACK"
        self._uiThemeColorConstructor = "DARKGREEN"
        self._uiTextColorConstructor = "DARKGREEN"
        self._uiFontFamilyConstructor = "Courier New"
        self._uiFontSizeSetting = 14
        self._uiBorderWidth = 5
        self._uiConsoleRatio = 4
        self._uiPromptText = ">_ "
        self._uiAlwaysTopWindow = True

