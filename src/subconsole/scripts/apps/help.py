from subapplication.subapplication import SubApplication
from scripts.help.help_assets import ASSETS


# LICENSE INFO
"""
        <HelpSubApplication Extension for SubApplication. For example and documentation.>
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

class HelpSubApplication(SubApplication):
    def __init__(self, alias, parent=None):
        super().__init__(alias, parent)
        
        # Define essential properties here, 
        # but __init__ isn't called when your application starts
        
        # The help module in the scripts folder contains crude
        # 'HTML' assets, not to be used as an example of HTML,
        # rather the flexibility that Qt's HTML reader allows
        # your layouts, and the ability to get desired results
        # leveraging improperly formed HTML to mutate the document.  
        self.assets = ASSETS
        self.currentMenu = self.assets["mainMenu"]
        
        # We create this here so we can assign it 
        # with a method we'll create 'calculateSizeOffset()'
        # This helps control the menu font size.
        self.sizeManager = 8
        
    
    def startupActions(self):
        # Ignoring input until 'Help...' message is finished
        self.ingoreInput()

        # We build this below to determine
        # a font size offset for full vs. 1/4 screen
        self.calculateSizeOffset()

        # Configure settings
        self.themeSettings(theme="gray", background="darkblue", brushstyle="solid")
        
        # You can use prompt to communicate interaction options
        self.terminalSettings(
            prompt="[ENTER MENU OPTION: Main= 0 : Exit= X | +/- to zoom]", textcolor="gray", fontsize=16,
            fontfamily="Georgia", ratio=7
        )
        
        # Configure settings for the initial animation multiplying resize_value for our 'title card'.
        self.textSettings(color="gray", font="Georgia", size=30 + (self.resize_value * 3))
        
        # Render text returns the time in ms
        time = self.renderText("\t\tHelp is on the way . . .", timeout=20, center=True)
        
        # Adjust size before rendering HTML
        # the textSettings need to be changed asynchroniously here
        # to allow the title card to render 
        # so we'll use the same form to do this as to render the main menu.
        self.timer.singleShot(
            time + 500, lambda: self.textSettings(size=self.sizeManager + self.resize_value)
        )
        # Give time for the message to render, as well as the settings 
        # to apply from the previous message's completion.
        # Render Main Menu in HTML.
        self.timer.singleShot(
           time + 700, lambda: self.renderHTML(self.assets["mainMenu"])
        )
        # Always exit your animated render logic with acceptInput using 
        # the total wait time needed to complete your actions.
        # If using animations with renderText, take the sum of all 'time'
        # values returned by renderText.
        self.acceptInput(time + 700)


    # Override viewerChange to handle window size changes
    def viewerChange(self):
        self.calculateSizeOffset() # built below
        # Adjust settings and re-render.
        self.textSettings(size=self.sizeManager + self.resize_value)
        self.renderHTML(self.currentMenu)
        

    # We use this above and in startupActions
    # to determine a screen size offset.    
    def calculateSizeOffset(self):
        # Use the property screenFull to check full screen state.
        if self.screenFull:
            self.resize_value = 10
        else:
            self.resize_value = 0


    def commandInput(self, safe, raw):
        # A simple switch menu with state-management for 'zoom' and currentMenu

        # renderText and renderHTML DO NOT automatically adjust sizes or
        # re-render after window resize events.
        # Override viewerChange (see above)

        match safe.strip():
            case "+":
                self.sizeManager += 1
                self.textSettings(size=self.sizeManager + self.resize_value)
                self.renderHTML(self.currentMenu)
            case "-":
                # We've hardcoded a very reasonable absolute minmum.
                if self.appFontSize > 4:
                    self.sizeManager -= 1
                    self.textSettings(size=self.sizeManager + self.resize_value)
                    self.renderHTML(self.currentMenu)
            case "X":
                # Exit the SubApplication
                return super().receiveCommand(self.superStop)
            
            # Render the chosen menu, manage menu state for easy fetching.
            case "0":
                self.renderHTML(self.assets["mainMenu"])
                self.currentMenu = self.assets["mainMenu"]
            case "1":
                self.renderHTML(self.assets["commandLine"])
                self.currentMenu = self.assets["commandLine"]
            case "2":
                self.renderHTML(self.assets["instructionSet"])
                self.currentMenu = self.assets["instructionSet"]
            case "3":
                self.renderHTML(self.assets["runApps"])
                self.currentMenu = self.assets["runApps"]
            case "4":
                self.renderHTML(self.assets["override"])
                self.currentMenu = self.assets["override"]
            case "5":
                self.renderHTML(self.assets["subApplications"])
                self.currentMenu = self.assets["subApplications"]
            case "6":
                self.renderHTML(self.assets["gettingStarted"])
                self.currentMenu = self.assets["gettingStarted"]
            case "7":
                self.renderHTML(self.assets["shellCommands"])
                self.currentMenu = self.assets["shellCommands"]
            case "8":
                self.renderHTML(self.assets["viewMethods"])
                self.currentMenu = self.assets["viewMethods"]
            case "9":
                self.renderHTML(self.assets["about"])
                self.currentMenu = self.assets["about"]



# Create your application instance.

APP = HelpSubApplication("HELP")