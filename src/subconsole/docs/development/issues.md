# Issues
This document details known issues with the project.

Issues can be:
- `open` : An implementation to correct this issue is not in progress
- `checkout`: This issue has been checked out
- `closed`: The issue has been resolved
- `adapted`: An implementation has been provided to accommodate the issue

<br/><br/>
## Drag Window Icon Fails - Ubuntu/GNOME - `adapted`
- Issue Origin: Window Drag fails with frameless application in Ubuntu OS. 
Qt Frameless / GNOME compatibility issues are known.
- Status: *Adapted* application to support "-f" command line argument
which will use OS window frame. Frameless version icons are not removed and
their usage is preferred over the OS icons, as the OS "X" icon exits the application
without following SubConsole's internal shutdown protocol.

**Usage**:
> python3 subconsole.py -f

<br/>

## Window Opacity Fails - Ubuntu/GNOME - `open`
- Issue Origin: Window opacity settings not reflected in Ubuntu, research indicates
GNOME supports window opacity, potentially related to test hardware.
- Status: This issue remains *open* and requires further investigation.

<br/><br/>
## Upper Margin Graphics - Terminal / Console Ratio = 1 - `open`
- Issue Origin: Initializing SubConsole with the terminal or console ratio set to 1
causes an upper margin graphics offset.
- Status: This issue is *open* and a correction plan has not been formed.

<br/><br/>
## Negative Sizes - Widgets with Terminal / Console Ratio = 1 - `checkout`
- Issue Origin: Negative sizes error when using the SubApplication
renderWidget method and console ratio is set to 1.
- Status: A correction is planned in the subapplication namespace. 

<br/><br/><br/><br/>
## END as of 3/12/26