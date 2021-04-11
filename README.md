# CMSC421-Group6-Project

# Usage
The following command will clone the repository to your local:
> git clone https://github.com/Xutong-Qiu/CMSC421-Group6-Project.git
## Project Description

### FOPL Convention
As we have previously discussed, the parser will output a string representing a FOPL. The format of string should follow the following convention:
  * '|' represents OR. eg: mortal(socrates) | Greek(socrates)
  * '&' represents AND. eg: mortal(socrates) & Greek(socrates)
  * '~' represents negation. eg: ~ mortal(socrates)
  * 'Ex()' represents the existential quantifier. eg: Ex(X), Ex(X1), Ex(Human)
  * 'All()' represents the universal quantifier. eg: All(X), All(X1), All(Human)
  * Uppercase letter or words starting with uppercase letter represents varibles. eg: like(X,Y), like(X1,Y1), like(Person,Person)
  * Lowercase letter or words starting with lowercase letter represents constants. eg: like(a,b), like(a1,b1), Greek(socrates)
  * There's no convention for the name of predicates.\ 
FOPL example: Ex(X) like(X,cat) & like(X,dog)

### String to FOPL Converter
  Use regular expression to match the string.


### coreClasses.py
The file contains all core classes needed for the project.\
Predicate\
Clause\
FOPL\
To use these classes, you should have the following line in your header
>from coreClasses import *
>
##### The file also contains bugs and glitches. Let Xutong know if you find something that's not working.



