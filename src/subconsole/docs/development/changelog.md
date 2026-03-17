# Change Log
Record of noteworthy package changes.

Recent changes are at the top.

## 3/16/26
- Console height and prompt text requests now bypass `IGNORE` flag behavior, as these are considered essential SubApplication interface utilities
- Arguments can now be assigned to appRunArgument after the ignore flag (and any future flags) `RUN MYAPP IGNORE MYARG`
<br/>&emsp;*purpose*: Persistent SubApp access to terminal and prompt control, add user control and functionality
<br/>&emsp;*location*: core/subshell.py

- Added clearViewer method to SubApplication, end-dev safe method to remove an item from the view
<br/>&emsp;*purpose*: Allows end-dev to clear view items, replaced code blocks in multiple locations
<br/>&emsp;*location*: subapplication/subapplication.py; blocks replaced: subconsole.py + subapplication.py

- SubApplication now prevents input during render events, ignoreInput no longer needed
<br/>&emsp;*purpose*: Convenience, spam input prevention, viewer method safety
<br/>&emsp;*location*: subapplication/subapplication.py

- Usage of ignoreInput removed from HELLOWORLD and HELP SubApplication examples, this method will not
be removed, however it's use is no longer essential and was converted to a #note

- Updated documentation with changes and added example of clearViewer to HELLOWORLD

## 3/15/26:
- Added `.github/`, containing CONTRIBUTING.md, adjust roadmap reference  
- README trimmed for clarity
- Added missing issue
- Reordered changelog

## 3/13/26:
- Prevent negative size error involving consoleRatio 1 and renderWidget by forcing ratio of 2
<br/>&emsp;*purpose*: Prevent removal / Allow view area positive space for rendered widgets
<br/>&emsp;*location*: subapplication/subapplication.py

## 3/12/26:
- Add cli argument "-f" to enable OS native window frame; 
<br/>&emsp;*purpose*: Current solution for frameless compatibility issues
<br/>&emsp;*location*: subconsole.py

- Change showWelcomeMessageAnimation, now accepts *consume*:str
<br/>&emsp;*purpose*: Allows welcome animation to be customized
<br/>&emsp;*location*: core/subshell.py

- Documentation added, including issues, roadmap, and changelog  