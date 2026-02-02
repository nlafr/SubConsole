# SubApplication (class)
A class that provides an exclusive connection to the SubConsole command-line, and access to viewer renering methods.
Treated as an executable by SubConsole, SubApplications seize the command line when `RUN`, and can be `END` from the command line at any time.

>**SubApplication**(*self*, *alias*:str, *parent*=None)

**type:** PySide6.QtCore.QObject

***alias:*** str: SubApplication's alias, as to be called from command line.

- In the default package configuration, the parameter *alias* ***must contain only capital letters and underscores***.
The default shell is case-insensitive, but mixed-cased use is possible by setting *caseSensitiveCommands*: True; in settings.json, however this is not recommended, as *all* shell commands would become case-sensitive. SubApplications will not raise exceptions for strings that conflict this convention, though your shell will not recognize that the SubApplication exists. Consider this the cost of conveneience for case-insensitive commands, and of handing your applications directly to the *core*, as when caseSensitiveCommands is False (default), the *core* checks against uppercase strings.

***parent:*** QObject: used by PySide6's object heirarchy.

## Getting Started

Think of the *scripts* folder as your personal module library. Here you'll find the `apps` folder, where you can place Python files which should contain the *instance* of your custom SubApplication, assigned to the variable named `APP`. You can define your custom class in this file, or import it from a module you've created in the `scripts` folder. 

Minimally, all you need to get started is to create a Python file in the `apps` folder (Using the application's *alias* as a file name is recommended, though capitalization is not required for the Python filename), using the following template:

>**from** subapplication **import** **SubApplication**
<br/><br/>
class **MyCustomSubApplication**(**SubApplication**):
<br/>&emsp; def \_\_init__(self, alias, parent=None):
<br/>&emsp; &emsp; super().\_\_init__(alias, parent)
<br/><br/>
&emsp; def startupActions(self):
<br/>&emsp;&emsp;"""Your Startup Actions"""<br/>
<br/><br/>
&emsp; def commandInput(self, safe, raw):<br/>
&emsp; &emsp;"""Your Command Input Logic"""<br/><br/><br/><br/>
>APP = MyCustomSubApplication("MY_APP_NAME")

### \_\_init__

The above illustrates an important point about how SubApplications are created, which will determine how you treat your \_\_init__ method for SubApplications.

The instance of your app is created at read-in, which occurs before you even see the user interface on your screen. This limits \_\_init__'s utility to the creation and storage of any additonal data structures your SubApplication might need to function, however it is only called once at startup. Therefore, if you need to reset the value of an attribute each time the app is called, this is best defined in the startupActions method.

### startupActions

The **startupActions** method is a virtual method for you define actions that happen as the SubApplication gains control of the console and is a place for resetting property values, and presenting the user with some form of instruction on how to use your application in the interface. 


### commandInput

The **commandInput** method offers two verisons of user input: ***safe*** and ***raw***.

***safe***: str : has been processed by the *shell* and in the default configuration will be uppercase `*safe* = *raw*.upper()`. This may prove convenient for handling case-insensitivity at the terminal.

***raw***: str : literal user string from the command line. Most applications will likely want the **literal user input**. 



To create an **exit** condition in your command logic, use `super().receiveCommand(self.superStop)`. *This will be the **only** context where you will need to use the **receiveCommand** method*. Passing the superStop property will end the SubApplication.

## Viewer Methods
SubApplications are equipped with native methods for rendering text, HTML, or a QWigdet to a defined view area above the terminal. This area fills the interior between the top border and the line that divides the terminal area, and it is padded on both sides by slightly more than the width of the window icons in the top right corner. The height of this area can vary based on terminal height, or will not present a viewable size if the ratio of the terminal area is set to 1. Using 1 as a default setting for SubConsole creates a minor graphics offset on the top border, however, it can be used to temporarily create a full terminal window for purely shell-like interactions.  

There are two native text rendering options for the Viewer area, renderText, and renderHTML. 

### renderText

The **renderText** method renders a string as text, and accepts newline and tab escape characters. 

>self.renderText(*text*, *animate*=True, *timeout*=20, *center*=False)<br/>

***text***: str : Text to be rendered in the viewer area. **Lower boundary collisions are not managed** internally, however predictable formats can be achieved with different window sizes redefining the **viewerChange** method (another virtual method, more below). `RUN HELLOWORLD` in 1/4 screen for a demonstration of varied fonts of the same point size fitting or overflowing the view area. 

***animate***: bool : True by default, and will perform a typewriter style animation if the string passed to *text* is 250 characters or less. Strings greater in length will render instantly. The time (in ms) taken to render the text is returned by renderText, and using the methods **ignoreInput()** and **acceptInput(*time*)** can be used in conjunction with rendering logic to prevent unwanted user input during animations. It's best to wrap your animation sequence in these methods. You can choose to have the terminal send a custom response during this time using the **setWaitMessage** method. 

***timeout***: int : number of miliseconds between rendered characters. Lower numbers will render faster. 

***center***: bool : if True, will center the vertical starting position of the text only. It does not center the text alignment. This parameter is false by default and mostly only useful for single-line title-card style outputs.

**return:** *time* in miliseconds required for animation.

**ignoreInput**

Ignores input from terminal. Must call **acceptInput(*time*)** or your app will *"freeze"*.

>self.ignoreInput()

**renderText**

>time = self.renderText("Hello, world!")

&emsp;20ms * (13chars + 1) = 280 :: time = 280 <br/>&emsp;renderText uses an extra step internally.

**setWaitMessage**

Sets response to be *echoed* in the terminal while *ignoreInput* is effective.

***message***: str : message to **echo** or 'print' in terminal.

>self.setWaitMessage("This text will respond in the terminal while input is ignored")

**acceptInput**&emsp;**<=**&emsp;*Important!*

Determines the time your application will wait before it accepts input after calling **ignoreInput()**.

When using text animations one at a time, you can simply pass the value returned by **renderText** to **acceptInput**'s parameter ***time***, a positional which can be formed as `self.acceptInput(time)` if 'time' is the variable you assigned from *renderText* (see above).

>self.acceptInput(*time*, *buffer*=200)

***time***: int : miliseconds: should be the sum of all values returned by renderText for a sequence of renderings.

***buffer***: int: miliseconds: is a simple time buffer added to the *time* value to allow the system to complete events. The default value of 200 may be excessive but still insignificant to the user experience.

Each SubApplication comes with a built in **QTimer** under its own attribute *timer*.

**timer.singleShot**&emsp;**timer: QTimer**

>self.timer.singleShot(*msec*, *functor*)

***msec***: int : number of miliseconds to wait before *functor* takes action.

***functor***: Python Callable : method or function. If takes no parameters, pass without calling

>self.timer.singleShot(1000, self.myClassMethod)

If your method expects parameters, use `lambda`:

>self.timer.singleShot(1000, lambda: self.myClassMethod(param=value))

### renderHTML

The **renderHTML** method expects a string containing text in HTML format, and rendering does not require complete page layouts. Tags can be exploited creatively for text formatting. HTML's embedded features aren't supported, though this functionality is accesible through the PySide6 framework and SubApplication's renderWidget method. Use the method textSettings to control font size, style and color, both for renderText and renderHTML.

>self.renderHTML(*html*)

***html***: str : formatted as HTML. Accepts single tags and creative tag usage. Formatting only, web features don't work.

### viewerChange

Use viewerChange *cautiously*. Use the property `self.screenFull` to *check* the window state, and use your own state management to control window toggle events. *See* `help.py`.

Override the **viewerChange** method to adjust textSettings for window size change events, and re-render your current text in a different size to accomodate the size change, see `help.py` for an example of how to manage an active viewer asset and window size changes. Don't treat this as an Event in the Qt sense, though it is indirectly triggered by a QEvent, this event fires redundantly, So you can't simply assume each event represents a size change, however the `self.screenFull` property: True if Full; can assist in your state management logic.

>def viewerChange(self):<br/>
&emsp;&emsp;"""Respond to Window Size Changes."""

**screenFull**

&emsp;**return**: bool : True if screen full, False if 1/4 screen.

Widgets with layouts are not dependent on this override method and can be controlled efficiently with Qt's format policy customizations.

### renderWidget

The **renderWidget** method is the real powerhouse of SubApplication functionality (that being, Qt's native functionality). Though the method accepts only a single QWidget object, because of Qt's class heirarchy, **a single widget could be anything from a simple text editor to an entire user interface with a variety of features**.

If your application uses renderWidget, that widget should be constructed via a method that can perform the entire widget creation again if that widget will be reused. **Once a widget is removed from the viewer, it's instance is destroyed, and must be rebuilt if used again**.

See the PySide6 documentation to learn more about how to construct layouts and widgets. The file hello_widgets.py can help show you how to get started with widgets. From the SubConsole command-line `RUN HELLO_WIDGETS`

>self.renderWidget(*widget*:**QWidget**)

Learn more about **PySide6**:

>https://doc.qt.io/qtforpython-6/index.html

Be sure to check out *Getting Started*, *Package Details* and *Modules API*. Browse *Tutorials*, *Examples*, and *Videos* for more help and ideas on building your own Qt Creations.

And the **QWidget** class:

>https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html#PySide6.QtWidgets.QWidget

You'll find plenty of options to suit your SubApplication interface needs here. The docs can be intimidating at first, but they navigate much like Qt's object heirarchy, making it easy to find object and parent attributes which access all of Qt's features.

If your widgets need scrolling behavior, you need know that the SubConsole interface is ignoring wheelEvent by default, but in your main widget (the widget passed to renderWidget, or the highest level scroll area in your scene), you can `from PySide6.QtGui import QWheelEvent` and override that widgets *wheelEvent*: `def wheelEvent(self, event: QWheelEvent):` and simply `event.accept()` within that definition (or implement your own custom wheelEvent actions).



## Configuration Methods
SubApplications have convenience methods for configuring the interface, as well as settings for the text-based render methods.

As a convention, all parameters are named and None by default. Any parameter with the value None (or not passed explicitly) is ignored, and no changes are made to that parameter. This allows the method to be called to change a single named parameter while leaving other settings unchanged. This is true of all the configuration methods, except *useUiSettings* which accepts a **bool** and adopts the user settings for text rendering.

### useUiSettings

Application adopts user settings for viewer text. Created as convenience for \_\_init__ and other actions. Usage non-essential. 

***useUiSettingsTrue***: bool : if you wish to *use Ui Settings* pass *True*, else pass *False*: True by default at \_\_init__. 

>self.useUiSettings(*useUiSettingsTrue*:bool)

### textSettings

The **textSettings** method applies only to the *renderText* and *renderHTML* methods.

***color***: str : sets the color of the rendered text or HTML. 
- for a complete list of available colornames, `from PySide6 import QColor`, create an instance: `color = QColor()` and `print(color.colorNames())`

***font***: str : accepts a font family constructor, font support will vary based on your system, Qt uses a best-match algorithm for invalid fonts. 

***size***: int : sets font size.

>self.textSettings(*color*:str|None=None, *font*:str|None=None, *size*:int|None=None)

### themeSettings

The **themeSettings** method allows SubApplications to set the interface theme settings.

***theme***: str : color consructor. Changes border color.

***background***: str : color constructor. Changes background color.

***brushstyle***: str : brush style set option; SOLID, DENSE[1-7], GRID, DIAG

>self.themeSettings(*theme*:str|None=None, *background*:str|None=None, *brushstyle*:str|None=None)

### terminalSettings

The **terminalSettings** method allows SubApplications to control the settings in the terminal area.

***prompt***: str : sets prompt to str.

***textcolor***: str : color constructor. 

***fontsize***: int : range[10-20]. Sets font size to int.

***fontfamily***: str : font family constructor. Sets to font family.

***ratio***: int : range[1-9]. Sets terminal ratio to 1/int. Setting to 1 effectively eliminates the viewer for a purely shell-like environment. 

>self.terminalSettings(*prompt*:str|None=None, *textcolor*:str|None=None, *fontsize*:int|None=None, *fontfamily*:str|None=None)

## Shell Interactions

SubApplications have a means to interact with the shell directly and respond in the terminal area.

This only requires two methods, **sendShell** and **echo**.

### sendShell

Use the `SET` command and the property list below to send single commands to the shell, see *hello_widgets.py* or *helloworld.py*

>self.sendShell(f"{self.setOpCode} {self.promptOpCode} {yourPromptText}")


- self.setOpCode: SET Command
- self.backgroundOpCode: Background Color Option
- self.brushStyleOpCode: Brush Style Option
- self.themeOpCode: Theme (border) Color Option
- self.textColorOpCode: Terminal Text Color Option
- self.fontStyleOpCode: Font Style Option
- self.fontSizeOpCode: Font Size Option
- self.promptOpCode: Prompt Text Option
- self.opactityOpCode: Window Opacity Option
- self.welcomeOpCode: Welcome Message Option
- self.invalidOpCode: Invalid Command Response Option
- self.windowTitleOpCode: System Window Title Option
- self.topWindowOpCode: Top Window Behaivior Option
- self.saveOpCode: Save Settings Option

SubApplications have access to all settings except the HEAD_ALIAS (this is the main application's name: SUBCONSOLE by default, though customizable through the interface), so you can create applications that change your settings in bulk with a simple run command, or update your welcome message.

### echo

In keeping with the convention of many shells, your SubApplications can 'print' to the terminal with the **echo** method, by passing a string to echo's only named parameter *response*.

***response***: str : text to be "print" or sent as terminal output within SubConsole.

>self.echo("This text will be sent to the terminal area.")

### Command Line Arguments

SubApplications also have the option to accept *arguments* from the command line. The *argument* will take the place of the *flag* parameter and is accessible in the property `self.runArgument` assigned prior to **startupActions**. When you start `HELLOWOLRD` with no arguments, in the terminal output, one of the responses is "None", but if you `RUN HELLOWORLD argument` in the terminal, you will see "argument" in the output `self.echo(self.runArgument)`, making the illustration that *arguments* that aren't system *flags* are processed as raw user input, since they are entirely yours to use, and perform no native actions. Other parameters preserve their value parameter as a raw user string, such as: *Window Title, Invalid Command Response, and Welcome Message*.


## DOC_INFO
This represents the minimal documentation for the permanent SubApplication API features, and hopefully provides everything needed to get started building SubApplications.

This page will be updated with any permanent new SubApplication features.

Until package documentation is complete, the docstrings in subapplication.py may serve as additional support. The section of properties marks the beginning of more useful end-development methods, and anything above properties is related to interactions with the shell and interface. 