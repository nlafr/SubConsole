from subapplication.subapplication import SubApplication
import random


# LICENSE INFO
"""
        <HelloSubApplication Extension for SubApplication. For example and documentation.>
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



# Extend SubApplication class
class HelloSubApplication(SubApplication):
    def __init__(self, alias,  parent=None):
        # Make sure your init contains:
        super().__init__(alias, parent)
        # You can add attributes here, 
        # but remember __init__ is called at runtime,
        # NOT when your SubApplication starts


    # Virtual method to determine what your app does when RUN
    def startupActions(self):
        # Configure the viewer text settings
        self.textSettings(
            color="RED", font="Showcard Gothic", size=50
        )
        # Using the shell instead of configuration methods for this example
        self.sendShell(f"{self.setOpCode} {self.backgroundOpCode} darkblue")  # Background color
        self.sendShell(f"{self.setOpCode} {self.promptOpCode} [PRESS_ENTER]") # Prompt text
        self.sendShell(f"{self.setOpCode} {self.consoleOpCode} 2")            # Terminal or Console ratio
        # The center parameter centers the text vertically, the '\t' is being used to center horizontally.
        self.renderText("\tHello, World ! ! !", animate=False, center=True)
        
        # When running HELLOWORLD, 
        # add a space and type some text as if passing in another parameter,
        # 'RUN HELLOWORLD argument'
        # The poriton 'argument' of the above becomes the value
        # of self.runArgument which is accesible during startupActions
        # allowing your apps to accept command line arguments.
        self.echo(f"{self.runArgument}")   
        

    # Virtual method to receive commands from interface
    def commandInput(self, safe, raw):

        # Create your own custom exit commands:
        if safe in ["QUIT", "EXIT"]:
            return super().receiveCommand(self.superStop)

        # These properties can be used in place
        # Assigned to variables for sake of illustration
        setcode = self.setOpCode # SET command
        # SET Parameters = property # Description : value param type : value param                     
        themecode = self.themeOpCode # Sets Theme (borders) Color : str : color
        textcode = self.textColorOpCode # Sets Terminal Text Color : str : color
        fontcode = self.fontStyleOpCode # Sets Font Family Constructor : str : font family
        stylecode = self.brushStyleOpCode # Sets UI Brushstyle : str : brushstyle

        # Not used in this example:
        sizecode = self.fontSizeOpCode
        # Less used but included for customization SubApplications
        welcomecode = self.welcomeOpCode # Sets welcome message
        opacitycode = self.opacityOpCode # Sets window opacity : int : apply on restart
        topwindowcode = self.topWindowOpCode # Controls top window behavior : bool : apply on restart
        titlecode = self.windowTitleOpCode # Sets system window title : str : apply on restart
        savecode = self.saveOpCode # Saves settings
        # These could be used to create a SubApplication that configures the user space.
        # Use configuration methods or shell commands to configure, then:
        ### self.sendShell(f"{setcode} {savecode}") to save the new configuration
        ### Use super().receiveCommand(self.superStop) to exit automatically when finished.


        # A short sample of colors in mixed-cases.
        colors = [
                "BLUE", "LIGHTblue",
                "green", "lightGreen",
                "orange", "darkORANGE",
                "indigo", "yellow",
                "gray", "magenta"
        ]
        color  = random.choice(colors)

        ###! ! ! :FONT NOTICE: ! ! !###
        # Fonts may not be valid with all systems, 
        # try substituting your system supported fonts here
        fonts = [
            "times new roman", "helvetica",
            "courier new", "algerian",
            "papyrus", "showcard gothic",
            "georgia", "wingdings"
        ]
        font = random.choice(fonts)

        # In the default config (recommended) shell parameters are case-insensitive,
        # allowing the shell to accept input in upper, lower or mixed-case.
        patterns = [
            "solid", "DENSE1", "dense2", "dense3", "dense4"
            "dense5", "dense6" "Dense7", "GRID", "diag"
        ]
        pattern = random.choice(patterns)


        # Use random.choice values to pick random
        # settings for viewer text
        self.textSettings(color=color, font=font)

        
        # This will demonstrate the different render properties of different fonts 
        # and illustrate how the lower viewer boundary is not managed by renderText (or renderHTML).
        # Use the form below when using renderText with animate=True 
        # If rendering multiple text animations, pass the sum of all 
        # values returned by renderText to acceptInput
        # However, renderText would need to be called asynchroniously
        # Which you can do with the built in QTimer, see help.py
        self.ingoreInput()
        time = self.renderText(f"\tHello, World\t!!! _____ !!! _____ !!! _____ !!! _____ !!! 000 111 Aa Bb", center=False)
        # See help.py to see how to use a timer and create sequential events.
        self.acceptInput(time)
       
        
        # We'll use the shell to set other
        # sendShell expects commands to be formed as they would from the SubConsole command-line
        self.sendShell(f"{setcode} {textcode} {color}")
        self.sendShell(f"{setcode} {fontcode} {font}")
        self.sendShell(f"{setcode} {stylecode} {pattern}")
        self.sendShell(f"{setcode} {themecode} {color}")
      
        # Use echo to 'print' to the terminal.
        self.echo("type: 'Quit' or 'Exit'  :to exit |or| Enter input to see how case-sensitivity is handled")
        self.echo(f"|| safe: {safe} ||| raw: {raw} ||")
        

# Always assign your extension class instance 
# to the variable APP, at the main level (no indentation) of your file.

APP = HelloSubApplication("HELLOWORLD")