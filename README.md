# SubConsole
A minimal command line interface which creates an internal *SubApplication* template for wrapping multiple CLI or PySide6 interactions into a single *shell-like* runtime.

### VERSION
**0.1.0 Alpha Test** 
- Command-based CLI customization
- SubApplication API renders raw text/HTML or QWidget
- SubApplication access to customization commands 

Developed in Windows 11, Python 3.13.9, built on PySide6 6.10.1

Ubuntu deployment test upcoming...

## Quick Start
Ensure Python3.10 or higher is installed, latest stable is recommended: 

From your code editor or shell:

Windows:
>python --version

Linux/Mac:
>python3 --version

If not installed, follow instructions at https://python.org/downlads

Navigate to the folder in which you wish to install SubConsole. Choose something easily accessible from your shell. This could be your *Terminal* app in Windows (PowerShell), Ubuntu (*BASH*) or Mac(Zsh).
Put this project close to the root of your user folder, so you don't have to enter a long/nested/string of directories to navigate to your custom-built SubConsole environment, once you're spending more time using your applications than building them.  

Clone this Repo:
>git clone https://github.com/nlafr/SubConsole.git

Create your Virtual Environment in the root (SubConsole) folder of this project:

&emsp;&emsp;*you can call the* .env *parameter whatever you want, the dot designates it as a hidden folder*

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

From the *SubConsole* command-line, type `help` and press enter to learn more about using and building within Subconsole.

You can also proceed to the `docs` folder for more instructions: `USER.md` Introduces the interface and project architecture, `subapplication.md` provides documentation on how to build your own SubApplications. 

SubConsole was created to be a runtime environment, not to be installed as a package, though it may frequently refer to itself as such in the documentation. A compiled version should be possible but hasn't been attempted, as this is intended as a *living-workstation* or a GUI that expands as you create it.

## What's This Repo?
This project is the realization of a series of efforts to consolidate dependencies into a single virtual environment and make interactive projects easily accesible from a single interface. **It is a terminal-style interface runtime, with an extension object (SubApplication) *template* that allows each extension to be treated as an application within the SubConsole *shell***.  

The **interface supports command-line interactions** and has native methods for **rendering text, HTML, or a QWidget to a view area above the terminal**. These **interactions can be scripted as *SubApplications*** by creating your own custom **SubApplication** class, and defining that as an `APP` in the `scripts/apps` folder. This is explained further `docs/subapplication.md` as well as the in the `HELP` SubApplication, which can be used as a **starting guide**.

This design allows you to create interactions as **a collection of SubApplications that can be run from the SubConsole shell**, where additional dependencies can be added to the root environment, and support modules can be built in the `scripts` folder and easily imported into your SubApplications in the `apps` folder.

SubApplication's also have a view method render a single **QWidget**, which using **PySide6** presents a variety of extension options for **GUI-based SubApplications**. From the *SubConsole* command-line, enter `RUN HELLO_WIDGETS` to see an example.

The application itself is **frameless, and window size is restricted to 1/4 screen or full screen**. This behavior was chosen to simplify UI re-draw (built with *Qt's* graphics tools), as well as provide **predictable window shapes** for easily formatting rendered text and widget layouts.

Despite being restricted to your screen's aspect ratio, much of the rest of the **interface is customizable**, including opacity, top window behavior, colors and fontstyles. These customizations are **accessible through the command-line directly, as well as through SubApplication methods**.

While having been built as a means to consolidate an ever growing collection of virtual environments, the shell itself represents a wrapper for any collection of command-line interactions, and can provide an **easy transition from the command-line to PySide's GUI features**.

## Who's This For?
To be perfectly honest, this project was designed to suit the needs and desires of it's author- a **Python programmer** who wanted to find a better **option for navigating between command-line programs**, and avoid the monotony and bloat of creating a flock of modules and virtual environments, each to support a simple command-line interaction. Reasoning against this, it seemed far more practical to create **a GUI that is essentially a CLI, and provides a means for scripting seperate and unique interactions within this interface**. Not only does this simplify summoning the desired interaction to a simple RUN command, but it conveniently **funnels all of your dependencies into one root environment**, stopping the prolific spread of virtual environments. In addition, your single virtual environment can be **activated from your native shell**, allowing you to run the GUI and your interactions **without the need for your code editor**. 

This project does not *only* suit the busy Python programmer who wants a streamlined workflow and consolidated environments, but **novice and student programmers** will likely enjoy the ease and satisfaction of seeing their creations rendered in a runtime interface. **Student use was heavily considered** when designing the SubApplication class, as well as its inteaction with the SubConsole Shell, which allows the SubApplication to control the user interface. All efforts were made to construct an exemplary architecture that extends to an **introductary-level API** with plenty of **room to grow to advanced features** inside a versatile interface framework (**Qt**). The *scripts* and *apps* (folders) module conventions encourage modular development and reuseable architectures by keeping the support modules for all of your SubApplications in one place- and readily accessible to one another. The Shell's interaction protocol is a human-friendly interpretation of, and is inspired by traditional instruction set architectures, giving a simple but authentic representation of operational control, while safely limiting those operations to interface changes. This architecture also seeks to encourage new programmers to **get familiar with version control**, by creating your interactive projects within a *repository*, you can create different *branches* or *versions* to represent **progress checkpoints** or **different toolkits** allowing you to mix and make your personal **Python playground** however you like. Students however should be aware, the very nature of this project **diverges from Python's conventions** with regards to development and project modularity, though the project aims to maintain a representation of this philosophy, however confined, for the end-developer's part, to the project's *scripts* module. The project's **small scale and relative simplicity** of startup also makes SubConsole a candidate platform for classroom or **small group repositories**.

**This package is ideal for those who have some familiarity with Qt for Python, or those who wish to get more familiar with the framework**. SubApplications have adopted many of Qt's conventions, like class extension, frequently refered to herein as creating a *custom* class, and providing virtual methods to be overridden by those extensions, which become common practice when building in Qt. While SubApplications provide methods for rendering text in the viewer, the renderWidget method allows for a QWidget to be constructed and rendered within the viewer, meaning any collection of Qt objects that can be stuffed into a single widget can also be rendered to the viewer, leaving **most of PySide6's features accesible and available to be rendered by SubApplications**.


## PySide6 | Qt For Python
This package is built on **PySide6 6.10.1**, and Qt modules can be imported from PySide6 without installing additional dependencies (limited to community version).

**Community Version:** Qt's Community Version is licensed under GNU GPL-v3 and by extension so is this repository and it's forks.

Check out the **Documentation:** 
>https://doc.qt.io/qtforpython-6/index.html

### Compatibility
**Qt** uses system resources to create interfaces, virtual systems (WSL and remote options like *codespaces*) and systems without window managers ***will face difficulty*** using the project without modification and other unique preparations.

**Conda** environmets and packages as well as **Matplotlib** packages are also known to have conflicts with **Qt**, and this experience is widely reported.

## License
This project is ***free software*** for you to use or modify as you choose, shared under the **GNU General Public License Version 3**, which requires all derivitave works to be **shared under the same license**. `See LICENSE.md`.

## Additional Documentation
This README and the HELP SubApplication serve as a quick-start guide. Additional documentation can be found in the `docs` folder. `USER.md` provides a light introduction to the interface and overview of SubConsole's structure, while `subapplication.md` introduces the SubApplication class and creating your own SubApplications, representing the primary utility of the package. Later versions will aspire to provide a complete set of documentation for those who wish to expand or modify the package, though this is likely the smaller portion of this package's users.

## Contribution (Not Implemented, Provided in the Event of Interest)
Though there is room for expansion and improvement within the "kernel" of SubConsole, it's expansion will have secondary priority to providing a reproduceable environment for shareable SubApplications. This means that the UI and shell functionality are unlikely to change unless such changes do not interfere with existing SubApplication methods or shell interactions. 

If project adoption exceeds expectations and a community forms around requested improvments, volunteer maintainers will be sought and provided with a greater volume of documentation and source annotations.

It is worthy to note *unit tests* are still *not implemented* as cross-platform testing has been prioritized (the repository has been made public in Alpha Test to facilitate a clone test for Ubuntu) and will likely not appear until Beta, along with a few essential SubApplications. It's safe to assume that the repo will not be ready for contribution until that time.

Considering the apparent direction of the project, there will be two repositories:
- The **SubConsole Shell** which will contain no SubApplications (excepting help and hello applications, or future essential utilities) 
- The **Community Console** which will contain a *curated* collection of contributions, which users can clone whole and cherry-pick which community applications to use in their own SubConsole.
This approach was chosen for it's relative simplicity for the benefit for the majority of this repo's projected audience, and alignment with this project's philosophy of resource consolidation. 

### Community Console 
- Only SubApplications and supporting modules within the `scripts` folder will be accepted.
- Due to default naming conventions, each app *alias* must be uppercase and underscores only. Therefore, namespaces are a limitation, so please check what's already used in the `community` folder, as well as `apps` and `scripts`, prior to building your contribution.
- A community folder will exist in the community repo, you must provide a markdown (README) explaining your SubApplication, using the *alias* as the name of your file ex: `MY_APP.md`. This allows others to see used namespaces at a glance, and outlining additional structures in your markdown can help other contributiors plan projects and avoid name collisions.
- Given the above standard, if you would like to make a contribution, start by providing a markdown in the `community` folder, and that will reserve the namespaces in the `scripts` and `apps` folders for your project.
- The addition of selective dependencies is being carefully considered for future revisions, however initially limit contribution dependencies to PySide6 Community Edition packages, and of course, Python's native libraries. In the meantime, those who wish to add dependencies to the module are encouraged to host a *fork*.
- SubApplication submissions will be reviewed for content and safety. Apps may be rejected for questionable content (keep in mind the educational audience), suspicious activity, and of course, significant bugs or runtime errors. While safety and functionality are paramount, remember that **GPL-v3 allows redistribution and modification** under the terms of the license, therefore you are free to **create and host a *fork* under the same license**, containing SubApplications intended for any audience you choose.


### Pull Instructions
Instructions will be found here in the community repo. (NOT IMPLEMENTED - ARRIVAL TBD)


## Author
Nathan LaFrazia
- nlafr@github.com
- Certification: edX CS50x/CS50P :: Certificate *does not* imply endorsement. Excellent introductory course. 
