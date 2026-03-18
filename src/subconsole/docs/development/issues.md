# Issues
This document details known issues with the project.

Issues can be:
- `open` : An implementation to correct this issue is not in progress
- `scheduled`: A plan is in place to correct the issue
- `checkout`: This issue has been checked out
- `closed`: The issue has been resolved
- `adapted`: An implementation has been provided to accommodate the issue

<br/>

## Drag Window Icon Fails - Ubuntu/GNOME - `adapted`
- Issue Origin: Window Drag fails with frameless application in Ubuntu OS. 
Qt Frameless / GNOME compatibility issues are known.
- Status: *Adapted* application to support "-f" command line argument
which will use OS window frame. Frameless version icons are not removed.

**Usage**:
> python3 subconsole.py -f

<br/>

## Window Opacity Fails - Ubuntu/GNOME - `open`
- Issue Origin: Window opacity settings not reflected in Ubuntu, research indicates
GNOME supports window opacity.
- Status: This issue remains *open* and requires further investigation.

<br/>

## Top Window Fails - Ubuntu/GNOME = `open`
- Issue Origin: Top window behavior not performing in Ubuntu, should be supported.
- Status: This issue is *open* and requires further investigation

<br/>

## Upper Margin Graphics - Terminal / Console Ratio = 1 - `open`
- Issue Origin: Initializing SubConsole with the terminal or console ratio set to 1
causes an upper margin graphics offset.
- Status: This issue is *open* and a correction plan has not been formed.

<br/>

## SubApplication appArgument - Value persistence bug - `closed`
- Issue Origin: Values persist from previous SubApplication appArgument and are assigned to subsequently run SubApplications.
- Status: Corrected in subconsole.py, assignment value now resets.

<br/>

## End SubApplication Override - Viewer / Settings not reset on END APP - `closed`
- Issue Origin: Using end operation overrides "subconsole$end myapp" would cause the SubApplication to close without clearing the viewer or restoring settings.
- Status: End override commands now forward a non-override to the SubApplication, ensuring proper ending behavior.  

<br/>

## Negative Sizes - Widgets with Terminal / Console Ratio = 1 - `closed`
- Issue Origin: Negative sizes error when using the SubApplication
renderWidget method and console ratio is set to 1.
- Status: Console ratio is now automatically adjusted if the ratio is set to 1.
This behavior is enforced over user override commands. 

<br/><br/><br/>

## END as of 3/12/26