from subapplication.subapplication import SubApplication

# This is just a small sample of widgets
from PySide6.QtWidgets import (
    QPushButton, QLineEdit, QHBoxLayout, 
    QLabel, QVBoxLayout, QGroupBox
)
from PySide6.QtCore import (
    Qt
)
import random


# LICENSE INFO
"""
        <HelloWidgetSubApplication Extension for SubApplication. For example and documentation.>
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



# Extend the SubApplication Class
class HelloWidgetSubApplication(SubApplication):
    def __init__(self, alias, parent=None):
        super().__init__(alias, parent)

        self.colors = [
            "red", "orange", "yellow", 
            "green", "blue", "indigo",
            "violet", "magenta", "cyan",
            "darkred", "darkorange", "darkblue",
            "darkgreen", "lightgreen", "gray",
            "black"
        ]

        self.brushstyles = [
            "solid", "dense1", "dense2",
            "dense3", "dense4", "dense5",
            "dense6", "dense7", "grid",
            "diag"
        ]




    def startupActions(self):

        # IMPORTANT: Define your inital widgets in startupActions, NOT __init__, to ensure proper behavior.
        # All viewer objects are destroyed after use, so 
        # navigating multiple groups would require a creation method for each group.
        # QGroupBox was chosen for its use as an example,
        # See PySide6 documentation for QWidget for full variety of accepted objects 
        
        self.terminalSettings(ratio=2)
        
        # This method creates the whole interface
        self.buildGroupBox()

        self.renderWidget(self.group)




    def buildGroupBox(self):
        # We'll use the group box as a container
        self.group = QGroupBox("Group Widget")
        
        # Create a few buttons
        self.themeButton = QPushButton("Theme")
        self.backgroundButton = QPushButton("Background")
        self.brushButton = QPushButton("Brush Style")
        self.textButton = QPushButton("Text Color")
        self.fontStyleSetButton = QPushButton("Set Font Style!")

        # Create a single-line text input
        self.fontStyleInput = QLineEdit()
        # Create a label and make sure it stays at its
        # lowest possible position in it's layout order
        styleInputLabel = QLabel("Font Style")
        styleInputLabel.setAlignment(Qt.AlignBottom)
        
        # Create a 'sublayout' to be stuffed into another layout
        sublayout = QHBoxLayout() # H-BOX Horizontal Box

        # You can add Widgets to layouts without parameters
        # This offers minimal control over positioning however,
        # the order added will determine their position
        # See Qt's docs to learn advanced layout features
        sublayout.addWidget(self.themeButton) 
        sublayout.addWidget(self.backgroundButton)
        sublayout.addWidget(self.brushButton)
        
        # This will be our main layout
        layout = QVBoxLayout() # V-BOX Vertical Box

        # First we'll add the sublayout, 
        # placing it at the top of the layout
        layout.addLayout(sublayout)

        # Below We add the other buttons and inputs
        layout.addWidget(self.textButton)
        layout.addWidget(styleInputLabel)
        layout.addWidget(self.fontStyleInput)
        layout.addWidget(self.fontStyleSetButton)

        # Set the layout to the widget 
        # to be passed to renderWidget 
        self.group.setLayout(layout)

        # Check out Qt's Events, Slots And Signals
        # Here, when a button's 'clicked' event occurs
        # that event can be connected to a method or function.
        # That functor must be presented as a callable, 
        # NOT called in place (as the value of the functor's return is not callable).
        # Below we create methods that send the appropriate
        # shell command when the method is called.
        self.themeButton.clicked.connect(self.randomThemeColor)
        self.backgroundButton.clicked.connect(self.randomBackgroundColor)
        self.brushButton.clicked.connect(self.randomBrushStyle)
        self.textButton.clicked.connect(self.randomTextColor)
        self.fontStyleSetButton.clicked.connect(self.applyFont)

        


    # Customization randomizations as shell commands

    def randomThemeColor(self):
        color = random.choice(self.colors)
        self.sendShell(f"{self.setOpCode} {self.themeOpCode} {color}")

    def randomBackgroundColor(self):
        color = random.choice(self.colors)
        self.sendShell(f"{self.setOpCode} {self.backgroundOpCode} {color}")

    def randomTextColor(self):
        color = random.choice(self.colors)
        self.sendShell(f"{self.setOpCode} {self.textColorOpCode} {color}")

    def randomBrushStyle(self):
        style = random.choice(self.brushstyles)
        self.sendShell(f"{self.setOpCode} {self.brushStyleOpCode} {style}")


    # Grab values from objects
    def applyFont(self):
        # The QLineEdit's text() method returns the current text in that Widget
        style = self.fontStyleInput.text()
        self.sendShell(f"{self.setOpCode} {self.fontStyleOpCode} {style}")
        # Once we have the value, we can use setText(text) to clear or change the text
        self.fontStyleInput.setText("")


    def commandInput(self, safe, raw):
        # All our command line does here is provide an exit condition
        if safe.strip() == "EXIT":
            super().receiveCommand(self.superStop)
        else:
            self.echo("Enter EXIT to Quit")


# Always create an instance of your extension
APP = HelloWidgetSubApplication("HELLO_WIDGETS")