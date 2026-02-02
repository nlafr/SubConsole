ASSETS = {}


"""
        <HTML asset dictionary for help.py SubApplication.>
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



ASSETS["mainMenu"] = """
<h3>click and hold ">_" to move window</h3>
<h1>Main Menu</h1>
    <h2><table>
        <tr><td></td>  <td>___________</td> <td></td>  <td>___________</td> <td></td></tr>
        <tr><td>The Command Line</td>  <td></td> <td></td> <td></td> <td>1</td></tr>
        <tr><td></td> <td></td> <td>The "Set" Command</td> <td></td>           <td>2</td></tr>
        <tr><td></td> <td></td> <td>Run/End SubApplications</td> <td></td>     <td>3</td></tr>
        <tr><td></td> <td></td> <td>Override features</td> <td></td>           <td>4</td></tr>
        <tr><td>Building SubApplications</td><td></td> <td></td> <td></td>     <td>5</td></tr>
        <tr><td></td> <td></td> <td>Getting Started</td> <td></td>             <td>6</td></tr>
        <tr><td></td> <td></td> <td>Commanding the Shell</td> <td></td>        <td>7</td></tr>
        <tr><td></td><td></td> <td>Using Viewer Methods</td> <td></td>         <td>8</td></tr>
        <tr><td></td><td></td> <td>About</td> <td></td>                <td>9</td></tr>
        <tr><td>Exit</td> <td></td> <td></td> <td></td>                        <td>X</td></tr>
    </table></h2>
"""
ASSETS["commandLine"] = """
<h1>The Command Line</h1>
    <p>The command line is the primary interaction method for SubConsole.</p>
    <p>In the default configuration, shell command interactions are case-insensitive.</p>
    <p>Click anywhere inside the terminal area to focus the cursor on the command line.</p>
    <p>Input length is limited to the width of the terminal. Inputs and responses do not wrap lines.</p>
    <p>The default "WIN" toggles full/quarter screen, and "MIN" will minimize the window.</p>
    <p>When not running a SubApplication, the command line readily accepts a number of customization commands.</p>
    <p>Options exist for color and styling, window opacity, title, and top window behavior.</p>
    <p>The command line is accesible through the SubApplication template for easily scripting interactions.</p>
    <p>SubApplications have access to the shell through a minimal ISA, allowing SubApplications to temporarily customize the interface.</p>
"""

ASSETS["instructionSet"] = """
<h1>The "SET" Command</h1>   
    <table>
        <tr><th>COMMAND</th> <th>____</th> <th>OPCODE</th> <th>_____</th> <th>PARAM 1</th> <th>______</th> <th>PARAM 2</th> <th>_____</th> <th>OPERATION</th></tr>
        <tr><td>Set Command</td> <td></td> <td>SET</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td>Interface changes</td></tr>
        <tr><td>Text Color</td> <td></td> <td></td> <td></td> <td>TEXT</td> <td></td> <td>str: color</td> <td></td> <td>Sets text to str: color</td></tr>
        <tr><td>Font Style</td> <td></td> <td></td> <td></td> <td>FONT</td> <td></td> <td>str: font</td> <td></td> <td>Sets Font Style to str: font</td></tr>
        <tr><td>Font Size</td> <td></td> <td></td> <td></td> <td>SIZE</td> <td></td> <td>int: size</td> <td></td> <td>Sets Font Size range:[10-18]</td></tr>
        <tr><td>Background</td> <td></td> <td></td> <td></td> <td>SCREEN</td> <td></td> <td>str: color</td> <td></td> <td>Sets Background to str: color</td></tr>
        <tr><td>Brush Style</td> <td></td> <td></td> <td></td> <td>STYLE</td> <td></td> <td>str: brushstyle</td> <td></td> <td>Draws Ui with selected brush</td></tr>
        <tr><td>Theme</td> <td></td> <td></td> <td></td> <td>THEME</td> <td></td> <td>str: color</td> <td></td> <td>Sets Ui Borders to color</td></tr>
        <tr><td>Terminal Ratio</td> <td></td> <td></td> <td></td> <td>TERMINAL</td> <td></td> <td>int: ratio</td> <td></td> <td>Sets Ratio: 1/ratio [1-9]</td></tr> 
        <tr><td>Opacity</td> <td></td> <td></td> <td></td> <td>OPACITY</td> <td></td> <td>int: opacity</td> <td></td> <td>Sets Opacity range: [0-10]</td></tr>
        <tr><td>Always On Top</td> <td></td> <td></td> <td></td> <td>TOP_WINDOW</td> <td></td> <td>bool: true/false</td> <td></td> <td>Sets Always on top to: bool</td></tr>
        <tr><td>Window Title</td> <td></td> <td></td> <td></td> <td>TITLE</td> <td></td> <td>str: title</td> <td></td> <td>Sets System Window Title to: title</tr>
        <tr><td>Prompt Text</td> <td></td> <td></td> <td></td> <td>PROMPT</td> <td></td> <td>str: text</td> <td></td> <td>Sets Prompt to: text</td></tr>
        <tr><td>Welcome Message</td> <td></td> <td></td> <td></td> <td>WELCOME</td> <td></td> <td>str: message</td> <td></td> <td>Startup will display: message</td></tr>
        <tr><td>Invalid Command Response</td> <td></td> <td></td> <td></td> <td>INVALID</td> <td></td> <td>str: response</td> <td></td> <td>Invalid commands respond: response</td></tr>
        <tr><td>Internal SubConsole Alias</td> <td></td> <td></td> <td></td> <td>HEAD_ALIAS</td> <td></td> <td>str: alias</td> <td></td> <td>Sets internal "self" alias for override commands</td></tr>
        <tr><td>Save Settings</td> <td></td> <td></td> <td></td> <td>SAVE</td> <td></td> <td></td> <td></td>  <td>Save Current Settings</td></tr>
        <tr><td>Restore Saved</td> <td></td> <td></td> <td></td> <td>BACK</td> <td></td> <td></td> <td></td> <td>Restore All Settings to Last Saved</td></tr> 
    </table>
    <p>Look in settings.json for complete list of brush styles.</p>
    <p>Qt supports a variety of color constructor strings, invalid strings will render black.</p>
    <p>Font support will vary with your system, Qt uses a best-match algorithm for unsupported strings.</p>
"""

ASSETS["runApps"] = """
<h1>Run / End Applications</h1>
    <p>One application can be run at a time from the command line.</p>
    <p>The default run command, RUN can be combined with a SubApplication's given 'alias' seperated by a single space to run an application:</p> 
    <h3>RUN SUBAPPLICATION</h3>
    <p>To stop a SubApplication, enter END seperated by a space from that application's 'alias' into the terminal at any time:</p>
    <h3>END SUBAPPLICATION</h3>
    <p>This would work now if you entered END HELP, even though this option isn't presented in the menu.</p>
    <p>To stop the main application, from the Shell enter END SUBCONSOLE (or your chosen HEAD_ALIAS, see section on SET command.)
"""

ASSETS["override"] = """
<h1>Override SubApplications</h1>
    <p>Both the Shell and SubApplications use a common "thread" to use the command interface.</p>
    <p>When no SubApplication is active, the Shell will accept commands in the usual format.</p>
    <p>When a SubApplication is active, the Shell is forwarding your command to the application with its $NAME$ prefix.</p>
    <p>During this time the Shell expects UI commands to come in the format of the app name, followed by its own name:</p>
    <h3>$NAME$SUBCONSOLE$</h3>
    <p>Knowing this, commands can be issued directly to the Shell by bypassing the SubApplication as so:</p>
    <h3>SUBCONSOLE$SET THEME RED</h3>
    <p>Feel free to try it in the terminal.</p>
    <p>This will work with all set commands excepting the HEAD_ALIAS, whose default is SUBCONSOLE.</p>
"""

ASSETS["subApplications"] = """
<h1>SubApplications</h1>
    <p>This is the true main feature of SubConsole, collecting all of your custom crafted command line interactions.</p>
    <p>In an effort to consolidate virtual environments of similar dependencies into a single interactable workflow, a Sub-Shell like environment was created.</p>
    <p>The SubApplication class was designed to be subclassed and customized for a variety of uses.</p>
    <p>It provides virtual methods which are meant to be overridden to allow command-line interaction.</p>
    <p>SubApplications have access to the command-line, a majority of Shell commands, and a defined view area.</p>
    <p>SubApplication's viewer can be used with the renderText and renderHTML methods, or a single QWidget can be passed to renderWidget for a light extension to most of PyQt.</p> 
    <p>HELP itself is a SubApplication, rendering HTML in the viewer. Check out the help.py and help/help_assets.py files to see how to create a simple application like HELP.</p>    
"""

ASSETS["gettingStarted"] = """
<h1>Getting Started</h1>
    <p>SubConsole finds SubApplications in the "apps" folder within the "scripts" folder.</p>
    <p>Treat startupActions like __init__ for SubApplications. Read docs/subapplication.md for a complete guide.</p>
    <h3>from subapplication import SubApplication</h3>
    <h3>class MyCustomSubApplication(SubApplication):</h3>
    <table><tr><td></td><td></td><td><h3>def __init__(self, alias, parent=None):<table><tr> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td><td>super().__init__(alias, parent)</td></tr></table></h3>
    <h3>def startupActions(self):<table><tr> <td></td> <td></td> <td></td> <td></td> <td></td> <td>"Your App Startup Actions"</tr></table></h3>
    <h3>def commandInput(self, safe, raw):<table><tr> <td></td> <td></td> <td></td> <td></td> <td></td> <td>"Your Command Input Logic"</td></tr></table></h3></td></tr></table>
    <p>To create an exit conditon in your logic use: super().receiveCommand(self.superStop)</p>
    <p>Each "app" in the apps folder should be a signle Python file defining or importing a custom SubApplication object, and creating an instance called APP, as follows:</p>
    <h3>APP = MyCustomSubApplication("MYAPPNAME")</h3>
    <p>The constant's name must be APP. App alias must be capital letters or underscores.<p/>
"""

ASSETS["shellCommands"] = """
<h1>Shell Commands</h1>
    <p>The methods themeSettings and terminalSettings allow for named parameters to be passed for quickly configuring the interface.</p.>
    <h3>themeSettings(theme=None|str:color, background=None|str:color, brushstyle=None|str:brushstyle)</h3>
    <h3>terminalSettings(prompt=None|str:text, textcolor=None|str:color, fontsize=None|int:[10-20] fontfamily=None|str:fontfamily, ratio=None|int:[1-9])</h3>
    <p>Each named parmameter changes its corresponding setting, accepting the same constructor strings as command line inputs for colors, brushstyles and fonts.</p>
    <p>The default value for each parameter is None, which will affect no changes to the current settings if no parameter is passed.</p>
    <p>Your applications can also provide responses in the terminal, using the conventionally named echo() method.</p>
    <h3>self.echo("This text will 'print' in the terminal")</h3>
    <p>Use the sendShell method to send commands directly to the shell as if sending from the terminal, use SubConsole's properties to ensure compatibility</p>
    <h3>self.sendShell(f"{self.setOpCode} {self.themeOpCode} BLUE")</h3>
    <p>This will set the borders blue.</p>
"""

ASSETS["viewMethods"] = """
<h1>Viewer Methods</h1>
    <p>The Viewer area is a rectangle padded on the left and right and centered in the area above the terminal.</p>
    <p>The methods renderText(text) and renderHTML(html) offer a simple means to create text in the Viewer.</p>
    <p>Text collisions with the terminal area are not directly managed, and text is able to overflow the Viewer.</p>
    <h3>time = renderText(text, animate=True, timeout=20, center=False)</h3>
    <p>The render text features a default typewriter style animation (up to 250 chars), and returns the time required to render.</p>
    <p>This allows for multiple text animations to occur between user inputs.</p>
    <p>The parameter timeout is the number in miliseconds between the appearance of each letter (lower numbers are faster)</p>
    <p>The parameter center centers the start of the text vertically in the viewer, but does not center the bulk, nor the alignment.
    <p>The methods ignoreInput() and acceptInput() allow you to manage unwanted input during animations by calling ignoreInput() prior to rendering, and acceptInput(time), passing the sum of all values returned by renderText.</p>        <p>Use the method textSettings to control the appearance of text in the Viewer.</p>
    <h3>textSettings(color=None|str:color, font=None|str:fontstyle, size=None)</h3>
    <p>Each parameter changes its respective setting. No changes are made to parameters passed None as default.</p>
    <p>The method renderWidget can be passed any PyQt widget object to be rendered to the viewer. See PyQt's Docs.</p>

"""

ASSETS["about"] = """
<h1>About SubConsole...</h1>
    <p>SubConsole is a minimal shell-like application that allows multiple command-line interactions to be created sharing a single interface and virtual environment.</p>
    <p>With the goal of providing a means to reduce the bloat of redundant virtual environments for small projects, SubConsole creates a structure that allows for the creation of quick and shareable interactions.</p>
    <p>Additional dependencies can be added to the same root environment, and projects stay contained in the scripts folder, where you can start building your modular toolkit.</p>
    <p>This aims to streamline workflow and system overhead, by changing between projects within the SubConsole's shell, instead of different folders within your code editor.</p>
    <p>Though natively only offering simple text and HTML rendering, SubConsole's true potential can be unlocked through familiarity with PyQt, and the SubApplication's renderWidget method.</p>
    <p>The extreme variety of utilities offered by the QWidget class will allow for plenty of creative exploration, all while being bundled within one minimal interface.</p>
"""