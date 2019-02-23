# CS342 Design Patterns
## Fall 2018
### PROJECT 2 README FILE

## DESIGN OVERVIEW:
- State each design pattern used (if any)
- Brief (< 5 sentences) description of your overall design
- Description of your search algorithm

## KNOWN BUGS AND INCOMPLETE PARTS:
- What parts of the project you were not able to complete

## REFERENCES:
- List any outside resources used

## MISCELLANEOUS COMMENTS:
- Anything you would like the grader to know

## Assignment Description
***
# Project 2 - Ants
### Due Date: 11:59 p.m., October 26th, 2018

*All programs will be tested on the machines in the Q22 lab. If your code does not run on the system in this lab, it is considered non-functioning EVEN IF IT RUNS ON YOUR PERSONAL COMPUTER. Always check that your code runs on the lab machines before submitting.*

### Driver Code and Test Files
* project2.py

### Grading Rubric
**Total: 60 points**
* Meadow (12 points)
    * Meadow class with a fixed sized grid (3 points)
    * Each grid cell contains hill, food, and ant references (2 pts)
    * Anthills are spawned during initialization using Builder pattern (3 points)
    * The simulation ends when only 1 or less anthills remains (2 points)
    * Each cycle is managed by the meadow (2 pts)
* Anthills (13 Points)
    * Anthills contains references to all Ants and Rooms (2 points)
    * Anthill creates ants each cycle using its rooms (3 points)
    * Each cycle, an anthill can only create a number of ants equalling the maximum number of workers, total rooms, and does not exceed the grid size (5 points)
    * All wandering ants move randomly every cycle (3 points)
* Ants (16 Points)
    * Forager finds food and returns it to the anthill (3 points)
    * Foragers have a chance to die when encountering Warriors (1 point)
    * When two warriors meet, a unique algorithm determines the outcome (2 points)
    * When a warrior happens on another Anthill, there is a small chance the Anthill will be obliterated, otherwise the warrior dies (2 points)
    * When a warrior wins a fight, it gains some attribute decorator (5 points)
    * Ants do not leave the meadow when they move (2 points)
    * Worker ants die when they create a room (1 points)
* Room (6 points)
    * Each room creates a specific type of ants each cycle if there are enough workers (3 points)
    * Creating new rooms cost 1 food and kills the worker (3 points)
* Display (13 points)
    * A menu that asks the user to display state or run for n cycles (3 points)
    * Displays when a warrior enters a fight (2 points)
    * Displays when a forager finds and returns food (2 points)
    * Display when a builder creates a room (2 points)
    * Displays when an Anthill is destroyed (2 points)
    * Display summary when only one or less anthill is left (2 points)
* Submission:
    * Follows requested project structure and submission format (-5 points)
    * No global variables (-5 points)
    * Meets the commit requirement of having 3 significant commits 24 hours apart

### Guidelines
This is a pair programming assignment. You and a partner can divide up the work. Although both of you may not work on all parts of the program you should understand and be able to fully explain every portion of the code. Outside of your team, it is permissible to consult with classmates to ask general questions about the assignment, to help discover and fix specific bugs, and to talk about high level approaches in general terms. It is not permissible to give or receive answers or solution details from fellow students.

You may research online for additional resources; however, you may not use code that was written specifically to solve the problem you have been given, and you may not have anyone else help you or your partner write the code or solve the problem. You may use code snippets found online, providing that they are appropriately and clearly cited, within your submitted code.

If you or your partner are found to have plagiarized any part of the assignment, both will receive a 0 and be reported.

*By submitting this assignment, you agree that you have followed the above guidelines regarding collaboration and research.*

__In this project, you will learn to__:

* Use Several Design Patterns discussed in class to build an Ant Farm

***


## Description


For our second assignment we are going to build an Ant Farm where several colonies of ants battle it out to be the last AntHill standing.

You are going to build an antfarm, and you're going to use some common design patterns to do it. The program will create several anthills in a meadow using the builder pattern. Each anthill will act as a factory that builds different kinds of Ants. What kinds of ants are built each turn will depend on the Anthill factories. Ants must leave the anthill and randomly wander the meadow in search of food.  When they do, they may randomly run into other ants. If the other ant is from another hill and is of a certain type, they should fight. The program will run cycles in which the state of the meadow will print to the console each cycle. The program will continue until only a single anthill is left.

## Part A - Building Your Ant Farm
For this assignment, you will have a single meadow that contains many ant hills. The ant hills will in turn manage the ants and the ant factories.

### Meadow
* The meadow will be a 20 x 20 grid
    * You may adjust the grid size if you feel a smaller or larger grid is more effective
* Each grid element should contain a Cell object that is initialized with the following information
    * hill = None
    * food = 0
    * ants = []
* The Meadow class is responsible for initializing the meadow and managing each cycle.
    * `__init__`:
        * Creates builder objects that configure and place Anthills in the meadow at various starting positions.
    * `cycle`:
        * Each cycle, the following should occur:
            * Food: The meadow should ensure 'food' is randomly placed in a couple locations each cycle
                * In practice, this means randomly selecting a few cells every cycle and incrementing the amount of food in those cells
            * The meadow should make sure each anthill has an opportunity to direct all of its ants and build any additional ants
            * At the end of every cycle you should present the user with a menu that asks:
                * If they would like to display the state of the meadow
                * Run the next n cycles without halting
* A meadow should spawn between 3-4 anthills on initialization
    * Anthills are spawned by ‘releasing a queen’ (builder object) who randomly selects a grid cell to build her anthill, then creates and initializes the anthill.
    * Anthills start with 1 piece of food and any additional attributes you think it needs (1 worker, 1 warrior, etc.)

### Anthill
An anthill should take up a single grid Cell and contain references to all its ants.
* Anthills can spawn ants of the following type on each cycle
    * foragers (used to search for food)
    * warriors (used to kill other ants)
    * workers (used to create rooms in the anthill)
* There are two limitations on the number of ants:
    * You cannot spawn more ants unless you have enough rooms (more information on rooms below).
        * 1 room allows you to create 1 ant per turn
    * You cannot create more ants than the number of cell rows
        * If your grid is 20x20, each hill cannot have more than 20 ants

### Ants
When an ant is created, it will immediately start working according to its type.
* For ants that wander the meadow, each ant moves 1 square in the meadow per turn.
     * Movement should be random, but the ant should not move off the grid. For example, if the ant is in a corner cell, it should only have 2 directions it can travel in and not be able to leave the ‘meadow’.

There are 3 ant types:
* `Forager`
    * The Forager searches each square for food as it wanders the meadow
        * Food can only be found by foragers
        * Once food is found, the forager must make its way back to the AntHill. If it dies on it's way back, the food is lost.
* `Warrior`
    * The warrior searches each cell for other ants as it wanders the meadow
        * If the other ant is a forager and from a different anthill, the forager has a 50% chance of dying.
        * If the other ant is a warrior and from a different anthill, a winner is selected based on a random algorithm of your choosing
    * For every fight the warrior wins, it gains a some attribute. This should be implemented as a decorator pattern.
        * For example, you may have 3 additional classes (SpeedBoost, SecondChance, and OddsBoost), and each time a Warrior wins a fight, you wrap the warrior in a new booster object. The booster object should be indistinguishable from the warrior class, only adding to it.
* `Worker`
    * The worker ant will create rooms that will in turn spawn your ants.

### Rooms

Ants are spawned by rooms. Each room spawns 1 ant of a specified type per cycle as long as certain requirements are met.

* A room can only spawn ants of a certain type (forager, worker, warrior). This must be decided when a room is created by the worker.
    * For example, you will have a `WorkerRoom`, `ForagerRoom`, and `WarriorRoom` that each create ants of that type only.
* Creating rooms costs 1 food and kills the worker ant
* Rooms are only effective if they have a worker, so if your hill only has 4 workers, then only 4 rooms will spawn new Ants, even if you have 10 rooms.
* :bulb: Although not required, I recommend having an abstract factory method that cycles through each of the rooms to create the ants for that cycle.

## Part B - Displaying and Ending the Simulation

An Anthill can be destroyed in several different ways:

* If a warrior of an ant colony wanders onto the anthill of another ant colony, it has a low chance to destroy the entire anthill (something like 1/5, but experiment with what you think works best).
    * If it succeeds in killing the hill of another colony, the colony (including all its ants) dies and is deleted from the meadow.
    * Otherwise, the warrior is killed
* If an anthill has 0 foragers at the end of a turn, it is destroyed

The simulation ends when there is 1 (or less) active colonies.

### Output

Finally, there are several events where you must output information to the console:
* A warrior :
    * enters a fight with a forager, just display if the forager escaped
    * enters a fight with a warrior, display the details and winner of the fight
    * finds a rival hill, display the outcome
* A forager
    * finds food
    * A forager returns food to the hill
* A builder:
    * creates a room
* An Anthill is destroyed
* Only one or less anthill is left

## Part C - Technical Requirements: (Design patterns bolded)
* There should be a single base Ant class and three subclasses, Forager, Warrior, and Worker.
* Each Room is an AntFactory that contains a factory method to create the specific ant type. Once the ant is created, it should then give them a unique ID and send them to work.
    * You may use pythonic factory and pass the Class as a parameter rather than creating subfactories, but you _must_ note this in your README (__factory pattern__).
    * You will need to have some way to differentiate between ant types and hill of origin for when the ants encounter each other in the meadow.
* On initialization, a Queen object should be created (__builder__), then should select a random location in the meadow for their ant hill.
    * The queen should configure the anthill first with initial number of rooms, food, and ants, then place it in the meadow.
        * :bulb: I would recommend coming up with a way to vary the initial configuration to make the simulation more interesting.
* Warriors should have multiple __decorator__ classes that wrap the warrior in additional functionality

## Part D: Submission

Required code organization:
* project2.py
    * this contains your main driver code. You should not have any classes in this file and it should just start your program.
* Meadow.py
    * This can contain both the cell and the meadow class.
* AntHill.py
* Ant.py
    * Depending on how you designed this, you may need additional Warrior.py, Worker.py, and Forager.py files.
* Room.py
    * Depending on how you designed this, you may need additional WarriorRoom.py, WorkerRoom.py, and ForagerRoom.py files.
* any additional files you feel are necessary

### Git

You must commit your changes throughout the development of your project. You do not necessarily need to push the commits to Github, but we will look at your repository commit history to ensure you have **3 significant commits 24 hours apart**. If you do not meet the commit requirements, we will not accept your project and you will receive a 0.

These are a reminder of the git commands you will need to submit your project.

:warning: *These commands all presume that your current working directory is within the directory tracked by `git`.*

```shell
git status
git add info.txt
git commit -a -m "final commit message"
git push
```
:warning: *You* __must__ *add any new files you create to the repository with the `git add` command or they will not upload to the repo, and your code will not work.*

To find your most recent commit hash, use the following command:

```shell
git rev-parse HEAD
```    



To complete your submission, you must copy and paste this number into mycourses. Go to MyCourses, select cs342, and **Assignment Hash Submission**. Select Project 2, and where it says text submission, paste your commit hash. The TAs will only grade your submission that corresponds to the hash you submitted. You can update this as often as you like until the deadline.

I strongly recommend making a submission early on, even if your assignment is not 100% working, to avoid late penalties. You can resubmit as many times as you like.

:warning: You __MUST__ submit the commit hash on mycourses before the deadline to be considered on time **even if your project is completely working before the deadline**. :warning:
