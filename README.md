# CS-3450-Team-5
## Big Blue Parking Genie Web Application
This project aims to build a web application for managing and selling parking for specific time slots.

The system will allow a user to rent out a parking spot, specifying the specific time slot that they want to rent it. The user will be given a form of identification that can be given to allow entry to the parking zone. The system will also have a manager mode that will allow for seeing how much space is left, dealing with discrepancies, handling customer complaints, and overriding errors in the system, etc.

## Organization:

- Docs - Contains use case UML's, Documentation of work and methodology, etc.\
- Src - Contains the thus far funcitonal code.  
- Src in progress - Contains the code that we are currently working on.  
- Other - contains any other files that might be relevent.  

## Version Control:

We will be updating the version every saturday, after the code has been 
verified by all members of the team, to ensure correctness and that the 
different pieces of code works together.

the first number refers to the current milestone we are working on
The second number refers to the week that we are on for this milestone
the third number refers to the update number that week.

ex: 2.3.2 (milestone 2, week 3, update 2)
 
## Tool Stack:

This team will be developing using Django (a high-level Python web development framework), Python, HTML, and CSS. We will all
have these set up on our personal computers for use.

## Build instructions:

1. pip install -r requirement.txt\
2. cd .../bbpg/
3. python manage.py runserver  

## Unit Testing Instructions:

Unit tests will be provided as an option in the source code. there are tests provided for creating an event, a parking lot, and a parking section. Run unittests.py to check the functionality. our tests of the system indicate that all of the unit tests pass.

1. cd .../bbpg/\
2. python manage.py test

## System Testing Instructions:

When testing the system, there are several cases that should be checked for;

1. purchasing a parking space for varying amounts of time
2. overriding a parking space sale
3. refunding a parking space sale
4. adding time to your purchased space
5. verifying the code for a purchased space
6. etc.

Check all of these, and more to ensure program functinality.

## Notes:

To access the sprint reports:

CS-3450-Team_5/docs/Milestone 3/

no current notes.
