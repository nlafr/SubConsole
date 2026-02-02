# SubConsole USER
Welcome to the user documentation for SubConsole.

This document will walk you through using the interface.

For best results, use a markdown viewer to view documentation.

If you haven't got the repo cloned in your own folder, or your virtual environment activated and subconsole.py running, head back to **Getting Started** in **README.md**.

## Interface

You should be confronted with a very bare interface 1/4 screen size, matching your aspect ratio.

The application is ***frameless*** and is limited to this (1/4) size and full screen, and a ***top window*** by default.

**Click and hold the** `>_` **icon in the upper left corner to move the window**. Place it somewhere it won't interfere with reading the markdown. The `_` `[]` `X` icons perform the expected window functions.

If you're not fond of the colors, font, opacity, top window behavior, or the background texture, it's okay, this is all yours to change.

We'll refer to the upper framed area as the **viewer**, and the lower area with the command prompt the **terminal**.

## Interaction

You can focus the **command-line** by clicking anywhere within the **terminal** area.

**Command input is case-*insensitive*** by default, though they are **shown capitalized** here, as this is ***how case-insensitivity is handled internally***.

**Input is limited to a single line**, the width of the terminal.

## Commands

### Window

You can **toggle between 1/4 and full screen** with the `WIN` command.

Similarly, the `MIN` command will minimize the window. Retrieve from taskbar or tray.

### RUN / END SubApplications

Once you start building **SubApplications**, they can be run from the terminal using `RUN MY_APP`, MY_APP representing your application's name.

SubApplications may be `RUN` with the optional `IGNORE` *flag* to ignore shell commands from the SubApplication. This will prevent SubApplications from making UI changes. Usage: `RUN MY_APP IGNORE`. *Currently only supported flag option. Argument support provided by SubApplication class*.

**End any application** from the terminal by entering `END MY_APP` using your application's name again in place of MY_APP.

You can try this with the provided `HELLO_WIDGETS` SubApplication by entering `RUN HELLO_WIDGETS` and stopping it by entering `END HELLO_WIDGETS`. Optionally, take a few moments to play with the buttons and try a few of your favorite fonts in the input, hit 'Set Font!' and enter some text in the terminal.

When not running a SubApplication, you can also `END SUBCONSOLE` from the terminal to **end the main application** *SubConsole*.

### HELP

Access a **condensed set of documentation from within SubConsole** by entering `HELP`, `--HELP`, or `-H` at the command line, use the terminal to navigate the menu.

The `HELP` SubApplication exists not only as a **reference tool** but as a **minimal structural example** of how to create a simple SubApplication using the `apps` folder and creating support modules in the `scripts` folder.

A `HELLOWORLD` SubApplication is also provided to help clarify usage and *demonstrate limitations* of the **renderText** method.
<br/>&emsp;*This application is somewhat intentionally obnoxious, with animated text often overflowing the viewer and <br/>&emsp;randomiziations to the interface prouce unreadable configurations, and may present problems for users with photosensitivite conditions<br/>&emsp;(those users may want to run *HELLOWORLD* with the *IGNORE* flag and go to helloworld.py line:131 renderText("Hello, World .. ..!", INSERT=>>***animate*=False**,...)).<br/> 
**You may want to direct your attention to the FONT NOTICE in `helloworld.py` and swap out for familiar fonts** if some don't seem to be rendering as expected. 

### SET & Customization

The `SET` command allows for a number of customization options. **See the table on page 2 of the** `HELP` **SubApplication**.

When using the SubConsole *Shell* (with no SubApplication active), the terminal will **accept commands as formed in the table. ex:** `SET TEXT YELLOW` will change the terminal text to yellow.

Certain settings only apply on restart, like `OPACITY`, `TOP_WINDOW` and `WELCOME`.

**To restore last saved settings enter** `SET BACK`.

**To save current settings enter** `SET SAVE`.

### Command-Line Override

Navigate to page 4 of `HELP` to review how to override SubApplications to send commands directly to the Shell.

Try `SUBCONSOLE$SET SCREEN BLACK` from within `HELP`. Navigate back to page 2 to use this technique with the table as a guide. Remeber to `SUBCONSOLE$SET SAVE` if you want to keep these settings, as ending a SubApplication restores last saved settings.

Using customization features you can give SubConsole your own window title in your system and even change the `HEAD_ALIAS` by entering the SET command `SET HEAD_ALIAS MYCONSOLE`, and SubConsole would no longer respond under the previous *alias*: `SUBCONSOLE`, but instead: `MYCONSOLE` and you would need to use `MYCONSOLE$SET ...` for override commands, or `END MYCONSOLE` to end the main application. 

See the subapplication markdown to learn more about building your own SubApplications.

## Modules & Extension

There's a lot going on in the SubConsole package, but your work will be limited to the `scripts` folder.

Here's a breif overview:

>SubConsole
<br/>&emsp;`.env` 
<br/>&emsp;&emsp;- Virtual Environment you created, containing dependencies.
<br/>&emsp;`src/subconsole`
<br/>&emsp;&emsp;- Source and project folder.
<br/>&emsp;&emsp;&emsp;`__pycache__` 
<br/>&emsp;&emsp;&emsp;&emsp;- Will appear in many subfolders, binaries created to facilitate PyQt.
<br/>&emsp;&emsp;&emsp;`core` 
<br/>&emsp;&emsp;&emsp;&emsp;- Contains subshell.py, effectively the 'kernel' of the SubConsole shell.
<br/>&emsp;&emsp;&emsp;`disk` 
<br/>&emsp;&emsp;&emsp;&emsp;- Contains settings.json. Potential internal future use.
<br/>&emsp;&emsp;&emsp;`docs` 
<br/>&emsp;&emsp;&emsp;&emsp;- Documents folder, containing documentation about SubConsole.
<br/>&emsp;&emsp;&emsp;**`scripts`** **<= <= <=** **Build your Modules**
<br/>&emsp;&emsp;&emsp;&emsp;- **Home for all of your SubApplication support modules**.
<br/>&emsp;&emsp;&emsp;&emsp;- Also Contains *settings_manager.py*, which discovers your APP
<br/>&emsp;&emsp;&emsp;&emsp;&emsp;**`apps`** **<= <= <=** **Create one APP instance per file**
<br/>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;- **Create SubApplication instance files here so they can be discovered by SubConsole**.
<br/>&emsp;&emsp;&emsp;&emsp;&emsp;`help` 
<br/>&emsp;&emsp;&emsp;&emsp;&emsp;- Assets for the HELP SubApplication.
<br/>&emsp;&emsp;&emsp;`subapplication` 
<br/>&emsp;&emsp;&emsp;&emsp;- Class definition module for SubApplication object.
<br/>&emsp;&emsp;&emsp;`ui` 
<br/>&emsp;&emsp;&emsp;&emsp;- Modules for creating the user interface.
<br/>&emsp;&emsp;&emsp;`__init__.py` 
<br/>&emsp;&emsp;&emsp;&emsp;- defines subconsole as a module.
<br/>&emsp;&emsp;&emsp;`.gitignore` 
<br/>&emsp;&emsp;&emsp;&emsp;- Ignores \_\_pycache__/ in Git (binaries vary by OS).
<br/>&emsp;&emsp;&emsp;`pyproject.toml` 
<br/>&emsp;&emsp;&emsp;&emsp;- Project metadata.
<br/>&emsp;&emsp;&emsp;`settings_manager.py` 
<br/>&emsp;&emsp;&emsp;&emsp;- Manages user settings and command language.
<br/>&emsp;&emsp;&emsp;`subconsole.py` **<= <= <=** **`python` or `python3` `subconsole.py`**
<br/>&emsp;&emsp;&emsp;&emsp;- **Runs SubConsole Application**.
<br/>&emsp;`LICENSE.md`
<br/>&emsp;&emsp;- GNU GPL-v3 License. 
<br/>&emsp;`README.md`
<br/>&emsp;&emsp;- Quickstart, about this repository.
<br/>&emsp;`requirements.txt`
<br/>&emsp;&emsp;- Dependency file for pip install.


## What's Next?

Head to `subapplication.md` to get started building your own SubApplications.