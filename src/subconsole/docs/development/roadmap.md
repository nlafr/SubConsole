# Roadmap
A description of desired future of SubConsole.

## Core Concepts
SubConsole intends to provide:
- A platform for easily creating interactions between
custom built tasks and interfaces.
- An environment suitable for peer collaboration and development.
- Prioritized focus on "small-development" scenarios
such as personalized toolkits, classrooms, and private labs.


## Sharing SubApplications
Depending on interest, the development of a registry repository is being considered for sharing 
SubApplications. This would require authors to register their remote, and a service SubApplication
will likely be implemented to simplify discovery and installation. Design details have not yet been
fully explored.

## Contribution
The repository is in preparation to accomodate contribution. Look forward to `contribution.md` 
in the development folder. Run `git branch` for a preview of the checkout structure.


## Extended Development
The main interface and command line interactions are unlikely to change significantly 
after the initial version.

The variety of case uses presented by personalized development implies a continued extension
of the functionality of the SubApplication class. Unlike the render methods, additional methods 
will not focus on abstractions to Qt, rather extend the system-wide functionality of 
SubApplications.

Plans for a socketserver utility have been moved to a unique repository. When ready, SubApplications
will be given compatible client methods.  

