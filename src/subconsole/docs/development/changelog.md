# Change Log
Record of noteworthy package changes.

Recent changes are at the top.

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