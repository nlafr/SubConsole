# SubConsole
A minimal command line interface which creates an internal *SubApplication* template for wrapping multiple CLI or PySide6 interactions into a single *shell-like* runtime.

### VERSION
**0.1.6 Alpha Test** 
- Command-based UI customization
- SubApplication API renders raw text/HTML or QWidget
- SubApplication access to customization commands 
- Bug fixes, Improvements: *see docs/development/changelog.md*

Developed in Windows 11, Python 3.13.9, built on PySide6 6.10.1

Certain features incompatible with Ubuntu/GNOME. See Compatibility.

## Quick Start
Ensure Python3.10 or higher is installed, latest stable is recommended: 

From your code editor or shell:

Windows:
>python --version

Linux/Mac:
>python3 --version

If not installed, follow instructions at https://python.org/downlads

Navigate to the folder in which you wish to install SubConsole. Choose something easily accessible from your user folder.

Clone this Repo:
>git clone https://github.com/nlafr/SubConsole.git

Create your Virtual Environment in the root (SubConsole) folder of this project:


Windows:
>python -m venv .env

Linux/Mac:
>python3 -m venv .env

Activate

Windows:
>.env\Scripts\Activate

Linux/Mac:
>source .env/bin/activate

Install Dependencies:
>pip install -r requirements.txt

Navigate to the *src/subconsole* folder and run subconsole:
>cd src/subconsole 

Windows:
>python subconsole.py

Linux/Mac:
>python3 subconsole.py

***SubConsole's frameless features may not be compatible with all window managers***, *or you may simply prefer to run SubConsole with an OS window frame*. 

Use OS frame:
>python3 subconsole.py -f


From the *SubConsole* command-line, type `help` and press enter to learn more about using and building within SubConsole.

You can also proceed to the `docs` folder for more instructions: `USER.md` Introduces the interface and project architecture, `subapplication.md` provides documentation on how to build your own SubApplications. 


## What's This Repo?
**SubConsole is a terminal-style interface runtime, with an extension object (SubApplication) *template* that allows each extension to be treated as an application within the SubConsole *shell***.  

The **interface supports command-line interactions** and has native methods for **rendering text, HTML, or a QWidget to a view area above the terminal**. These **interactions can be scripted as *SubApplications*** by creating your own custom **SubApplication** subclass, and defining that as an `APP` in the `scripts/apps` folder. This is explained further `docs/subapplication.md` as well as the in the `HELP` SubApplication, which can be used as a **starting guide**.

This design allows you to create interactions as **a collection of SubApplications that can be run from the SubConsole shell**, where additional dependencies can be added to the root environment, and support modules can be built in the `scripts` folder and easily imported into your SubApplications in the `apps` folder.

SubApplication's also have a view method render a single **QWidget**, which using **PySide6** presents a variety of extension options for **GUI-based SubApplications**. From the *SubConsole* command-line, enter `RUN HELLO_WIDGETS` to see an example.

The application itself is **frameless, and window size is restricted to 1/4 screen or full screen**. This behavior was chosen to simplify UI re-draw (built with *Qt's* graphics tools), as well as provide **predictable window shapes** for easily formatting rendered text and widget layouts.

Despite being restricted to your screen's aspect ratio, much of the rest of the **interface is customizable**, including opacity, top window behavior, colors and fontstyles. These customizations are **accessible through the command-line directly, as well as through SubApplication methods**.


## Who's This For?
To be perfectly honest, this project was designed to suit the needs and desires of it's author- a **Python programmer** who wanted to find a better **option for navigating between command-line programs**, and avoid the monotony and bloat of creating a flock of modules and virtual environments, each to support a simple command-line interaction. Reasoning against this, it seemed far more practical to create **a GUI that is essentially a CLI, and provides a means for scripting seperate and unique interactions within this interface**. Not only does this simplify summoning the desired interaction to a simple RUN command, but it conveniently **funnels all of your dependencies into one root environment**, stopping the prolific spread of virtual environments. In addition, your single virtual environment can be **activated from your native shell**, allowing you to run the GUI and your interactions **without the need for your code editor**. 

**Student use was heavily considered** when designing the SubApplication class, as well as its inteaction with the SubConsole Shell, which allows the SubApplication to control the user interface. All efforts were made to construct an exemplary architecture that extends to an **introductary-level API** with plenty of **room to grow to advanced features** inside a versatile interface framework (**Qt**). The project's **small scale and relative simplicity** of startup also makes SubConsole a candidate platform for classroom or **small group repositories**.

**This package is ideal for those who have some familiarity with Qt for Python, or those who wish to get more familiar with the framework**. While SubApplications provide methods for rendering text in the viewer, the renderWidget method allows for a QWidget to be constructed and rendered within the viewer, meaning any collection of Qt objects that can be stuffed into a single widget can also be rendered to the viewer, leaving **most of PySide6's features accesible and available to be rendered by SubApplications**.


## PySide6 | Qt For Python
This package is built on **PySide6 6.10.1**, and Qt modules can be imported from PySide6 without installing additional dependencies (limited to community version).

**Community Version:** Qt's Community Version is licensed under GNU GPL-v3 and by extension so is this repository and it's forks.

Check out the **Documentation:** 
>https://doc.qt.io/qtforpython-6/index.html

### Compatibility

**Virtual systems and web assembly platforms** (WSL and remote options like *codespaces*) are ***not*** compatible with **Qt**.

**Conda** environmets and packages as well as **Matplotlib** packages are also known to have conflicts with **Qt**, and this experience is widely reported.

**Ubuntu** may not be compatible with frameless features (window drag), opacity, and top window behaviors. Use `python3 subconsole.py -f` to use your window manager's window frame.

## License
This project is ***free software*** for you to use or modify as you choose, shared under the **GNU General Public License Version 3**, which requires all derivitave works to be **shared under the same license**. `See LICENSE.md`.

## Additional Documentation
This README and the HELP SubApplication serve as a quick-start guide. Additional documentation can be found in the `docs` folder. `USER.md` provides a light introduction to the interface and overview of SubConsole's structure, while `subapplication.md` introduces the SubApplication class and creating your own SubApplications, representing the primary utility of the package.

## Development and Contribution
See `docs/development` for additional documentation. `.github/CONTRIBUTING.md` will have the latest details on contribution.


## Author
Nathan LaFrazia
- nlafr.dev@proton.me 
