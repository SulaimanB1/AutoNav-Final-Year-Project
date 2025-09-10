MazeProgram README

***1. INSTALLATION***

As a basic requirement, you MUST have Python 3 installed.
The version used to write, test and run these programs is Python 3.12.
However, any version of Python 3 should be adequate with the required packages installed.

To run the program, firstly you must install the requirements.
The packages used are pygame and pygame_widgets.
To install these packages follow these steps:

1. Open Command Prompt or Terminal (or anywhere where you will have access to pip to install the requirements on your machine, such as Python Shell)
2. After unzipping the program, enter the "MazeProgram" folder (without the "").
3. Run the command: pip install -r requirements.txt


***2. PROGRAM SUITE OVERVIEW***

The MAIN program is Maze-Program.py.

The maze (generation) programs are:
1. Cell.py
1. Maze-Program.py
2. Maze-Fast.py (Great for maze testing purposes but not necessary to use)

The algorithm programs are:
1. A-Star.py
2. BFS.py
3. DFS.py
4. Dijkstra.py
5. Dijkstra-Fast.py (used in the Maze-Program.py)
6. Dijkstra-Full.py
7. Dijkstra-Full-Fast.py

dijkstra indicates evaluating one cell a time.
*-fast indicates it searches multiple cells at a time.
*-full indicates it evaluates the entire maze, even if the destination if found at an earlier point.
*-full-fast indicates it performs both of mentioned above.


***3. PROGRAM DETAILS***

The algorithm programs are the maze solvers and they solve the maze with their respective algorithms.

The maze programs are the maze generators and they are:
1. Maze-Program.py
2. Maze-Fast.py: produces 3 mazes quickly without displaying the GUI. It is NOT necessary to use this program.
Cell.py is a required support class that stores the required code to generate a grid and cells.


***4. HOW TO ACTUALLY RUN THE PROGRAM***

Disclaimer: The final maze used with the robot is the maze that came in the directory called grid1.
This will be overwirtten a generated maze is given the name grid1 as well.
If you wish to keep the final maze, then please rename it to avoid it being overwritten.
All programs load the maze called grid1 in the directory. If one doesn't exist, the program will not run.
And if one doesn't exist you can generate a new maze if you wish to by selecting to not load a maze when prompted by the program.

Execution Instructions

1. Run Maze-Program.py (or Maze-Fast.py which quickly generates 3 mazes without the GUI)
2. Load the final maze saved as grid1, or don't load a maze and enter the size of the maze you wish to generate (e.g. enter 15 for a 15x15 maze).
3. Click on a cell as the starting location, and then click on a cell as the destination location. This will solve the maze.
4. Click on the side buttons named after the algorithms to launch that Python program and solve the maze using that algorithm.
5. Repeat the instructions of selecting the start and destination location.
6. Close that program and solve the maze with another algorithm.

The algorithm results are output once the program is closed.
Compare results and continue to generate different mazes.