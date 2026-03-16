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
The repository is in preparation to accomodate contribution. See `.github/CONTRIBUTING.md` for more details.


## Extended Development
The main interface and command line interactions are unlikely to change significantly 
after the initial version.

Continued development will driven largely by community input and involvement but should
focus on the *core concepts* outlined above.

The SubApplication class should be considered the target of feature expansion, while changes to 
the core should be made conservatively, with good cause, and the utmost attention to
backwards compatibility (must not break existing SubApplications).

