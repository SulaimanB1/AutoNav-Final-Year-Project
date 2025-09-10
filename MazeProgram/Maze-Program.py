# Author: Sulaiman Bakali Mueden
# Date: 18th January 2024

# Title: Maze Generator
# Description: This program provides an interface to generate a randomly generated maze.

import pygame
import random
import math
import pickle
import time
import pygame_widgets

from pygame.locals import *
from pygame_widgets.dropdown import *
from pygame_widgets.button import *
from subprocess import call



# Initializing the Game
pygame.init()

pygame.font.init()

# colours used in the program
colour = (255, 255, 255)
line_colour = (0,0,0)
rect_colour = (0,255,0)

# Initialize the canvas with the title and logo

canvas = pygame.display.set_mode((700, 500))

pygame.display.set_caption('Maze')

img = pygame.image.load('qmul_logo.jpg')
pygame.display.set_icon(img)

# X and Y dimensions/size of the canvas
#c1, c2 = canvas.get_size()
c1 = 500
c2 = 500

# Stack for the recursive maze generation
stack= []

# Shortest path stack for recording shortest path elements
shortestPathStack = []

# Starting Point
# Temporary Values for the starting x and y coordinates and position
startingX = 1
startingY = 1

# Destination Point
#destinationX = width-1
#destinationY = height-1
destinationX = 5
destinationY = 5

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True] # boolean flag to determine whether top, right, bottom and left walls exist
        self.visited = False # boolean flag to determine whether the cell has been visited
        self.evaluated = False # boolean flag to determine whether the cell's weight has been evaluated.
        self.solved = False
        self.grid = grid
        self.weight = float('inf')
        self.explored = []  # list used to store explored cells

        
    def draw(self, line_colour):
        x = self.x
        y = self.y
        width = self.grid.width
        height = self.grid.height
        
        # top, right, bottom, left line
        if (self.walls[0]):
            pygame.draw.line(canvas, (line_colour), [(500/width)*x,(500/height)*y], [(500/width)*(x+1),(500/height)*(y)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(500/width)*x,(500/height)*y], [(500/width)*(x+1),(500/height)*(y)], 5)
            
        if (self.walls[1]):
            pygame.draw.line(canvas, (line_colour), [(500/width)*(x+1),(500/height)*(y)], [(500/width)*(x+1),(500/height)*(y+1)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(500/width)*(x+1),(500/height)*(y)], [(500/width)*(x+1),(500/height)*(y+1)], 5)
            
        if (self.walls[2]):
            pygame.draw.line(canvas, (line_colour), [(500/width)*x,(500/height)*(y+1)], [(500/width)*(x+1),(500/height)*(y+1)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(500/width)*x,(500/height)*(y+1)], [(500/width)*(x+1),(500/height)*(y+1)], 5)
        
        if (self.walls[3]):
            pygame.draw.line(canvas, (line_colour), [(500/width)*x,(500/height)*(y)], [(500/width)*(x),(500/height)*(y+1)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(500/width)*x,(500/height)*(y)], [(500/width)*(x),(500/height)*(y+1)], 5)

    def removeWall(self, other):
        if (other.x > self.x):
            other.walls[3] = False
            self.walls[1] = False
        if (self.x > other.x):
            self.walls[3] = False
            other.walls[1] = False
        if (other.y > self.y):
            other.walls[0] = False
            self.walls[2] = False
        if (self.y > other.y):
            self.walls[0] = False
            other.walls[2] = False
        self.draw(line_colour)
        other.draw(line_colour)


class Grid():
    def __init__(self, width, height):
        self.grid = []
        self.width = width
        self.height = height

    def createGrid(self):
        self.grid = [[Cell(x,y) for x in range(int(width))] for y in range(int(height))]

    def drawGrid(self):
        for i in range(len(self.grid)):
            for k in range(len(self.grid)):
                self.grid[i][k].draw(line_colour)

    def getGridPos(self, x, y):
        return self.grid[y][x]

    def setGridPos(self, x, y, v):
        self.grid[y][x] = v
        return

    def gridLength(self):
        return len(self.grid)

# Asking user whether they want to load a maze or create a new one
loadMaze = input("Do you want to load a maze ('Y' for yes, 'N' for no and to create a new one): ")
while (not ((loadMaze.upper() == "Y") or (loadMaze.upper() == "N"))):
    loadMaze = input("Please enter 'Y' for yes to load a maze and 'N' for no and to create a new one): ")

if (loadMaze.upper() == "Y"):
    loadMaze = True
else:
    loadMaze = False

# Adding width, height and grid variables
width = 0
height = 0
grid = None

# Asking user for the dimensions of the maze to generate
if (loadMaze):
    # This is used to import the maze and assign it to a new Grid (maze) object

    pickle_in = open("grid1","rb")
    grid = pickle.load(pickle_in)

    width = grid.gridLength()
    height = grid.gridLength()

else:
    # Size of the canvas
    # Dimensions are the same and checks whether the input is integer
    maze_size = input("Enter the size (width * height) of the maze: ")
    while (not (maze_size.isdigit())):
        maze_size = input("Please enter an integer for the size of the maze: ")

    width = int(maze_size)
    height = int(maze_size)

    grid = Grid(width, height)
    grid.createGrid()

    
# index function calculates the index value and performs checks. MUST KEEP DIMENSIONS EVEN
def index(i):
    if (i<0 or i>width-1 or i>height-1):
        return None
    return i
    

def checkNeighbours(grid, current):
    neighbours = []

    x = current.x
    y = current.y

    #top = grid[index(x)][index(y-1)]
    top = current
    x = index(current.x)
    y = index(current.y-1)
    if (not x == None and not y == None):
        top = grid.getGridPos(x,y)

    #right = grid[index(x+1)][index(y)]
    right = current
    x = index(current.x+1)
    y = index(current.y)
    if (not x == None and not y == None):
        right = grid.getGridPos(x,y)

    #bottom = grid[index(x)][index(y+1)]
    bottom = current
    x = index(current.x)
    y = index(current.y+1)
    if (not x == None and not y == None):
        bottom = grid.getGridPos(x,y)
  
    #left = grid[index(x-1)][index(y)]
    left = current
    x = index(current.x-1)
    y = index(current.y)
    if (not x == None and not y == None):
        left = grid.getGridPos(x,y)


    # This is checking whether each neighbouring cell has been visited
    # If not, add it to the neighbours list to be randomly selected
    if (not top.visited):
        neighbours.append(top)
        
    if (not right.visited):
        neighbours.append(right)
        
    if (not bottom.visited):
        neighbours.append(bottom)
        
    if (not left.visited):
        neighbours.append(left)

    # Checking if a neighbour has been added to the list and selecting a random one
    if (len(neighbours) > 0):
        r = random.randint(0, len(neighbours))
        return neighbours[r-1]

    # Otherwise, returning the current cell
    else:
        return current



def randomNeighbour(grid, current):
    neighbours = []

    x = current.x
    y = current.y

    top = current
    x = index(current.x)
    y = index(current.y-1)
    if (not x == None and not y == None):
        top = grid.getGridPos(x,y)

    right = current
    x = index(current.x+1)
    y = index(current.y)
    if (not x == None and not y == None):
        right = grid.getGridPos(x,y)

    bottom = current
    x = index(current.x)
    y = index(current.y+1)
    if (not x == None and not y == None):
        bottom = grid.getGridPos(x,y)
  
    left = current
    x = index(current.x-1)
    y = index(current.y)
    if (not x == None and not y == None):
        left = grid.getGridPos(x,y)


    # Add all sides to the neighbours list to be randomly selected
    # This is checking whether each neighbouring cell has been visited
    # If not, add it to the neighbours list to be randomly selected
    if (not current.walls[0] and not top.solved):
        neighbours.append(top)
        
    if (not current.walls[1] and not right.solved):
        neighbours.append(right)
        
    if (not current.walls[2] and not bottom.solved):
        neighbours.append(bottom)
        
    if (not current.walls[3] and not left.solved):
        neighbours.append(left)

    # Checking if a neighbour has been added to the list and selecting a random one
    if (len(neighbours) > 0):
        r= random.randint(0, len(neighbours))
        return neighbours[r-1]

    # Otherwise, returning the current cell
    else:
        return current


def solveNextCell(solving_current, next_cell, grid, solving_stack, shortestPathStack):
    textRect1 = None
    textRect2 = None
    
    if (solving_current != next_cell):
        solving_stack.append(solving_current)
        solving_current = next_cell
        solving_current.solved = True
        shortestPathStack.append(solving_current)
        pygame.draw.rect(canvas, ((255,194,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))
        
    else:
        solving_current = solving_stack.pop()
        pygame.draw.rect(canvas, ((255,0,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))
        shortestPathStack.pop()


# Paint the canvas with the variable color's RBG value
canvas.fill(colour)

# Initialize current outside of Game Loop to prevent it being reset
current = None

# Initialize current cell variable for solving and stack
solving_current = None
solving_stack = []
solved = False
count = 0
full_count = 0

complete = False

startSelected = False
destinationSelected = False

mazesToGenerate = 1
mazesGenerated = 0

beforeTime = 0
afterTime = 0
    

# Create array to store the names of the algorithms
algorithms = ["DFS", "BFS", "Dijkstra", "AStar"]

# Add clicked function to handle event when buttons are clicked

def clickedDFS():
    call(["python", "dfs.py"])

def clickedBFS():
    call(["python", "bfs.py"])

def clickedDijkstra():
    call(["python", "dijkstra-fast.py"])

def clickedAStar():
    call(["python", "a-star.py"])

    
# Add buttons to the canvas
    
# Add a button to the canvas
button1 = Button(
    canvas,
    525,
    100,
    150,
    50,
    text="DFS",  # Text to display
    fontSize=40,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=5,  # Radius of border corners (leave empty for not curved)
    onClick= lambda:clickedDFS()
)

buttons2 = Button(
    canvas,
    525,
    170,
    150,
    50,
    text="BFS",  # Text to display
    fontSize=40,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=5,  # Radius of border corners (leave empty for not curved)
    onClick= lambda:clickedBFS()
)

buttons3 = Button(
    canvas,
    525,
    240,
    150,
    50,
    text="Dijkstra",  # Text to display
    fontSize=40,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=5,  # Radius of border corners (leave empty for not curved)
    onClick= lambda:clickedDijkstra()
)

buttons4 = Button(
    canvas,
    525,
    310,
    150,
    50,
    text="AStar",  # Text to display
    fontSize=40,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=5,  # Radius of border corners (leave empty for not curved)
    onClick= lambda:clickedAStar()
)


# Game Loop

running = True

while running:
    # Maze Generation
    
    # Checking whether the maze generation is complete
    if (not complete and mazesToGenerate>0):
        grid.drawGrid()

        # Declaring current to the first square
        if current == None:
            current = grid.getGridPos(0, 0)
            current.visited = True


        # Finding a next random cell that hasn't been visited
        next_cell = checkNeighbours(grid, current)


        # Checking whether all cells have been visited or not
        # Otherwise, append to stack, remove wall between current and next cell and move to next cell
        if (current != next_cell):
            stack.append(current)

            if (current.visited):
                current.removeWall(next_cell)
                
            current = next_cell
            current.visited = True

        # Checking whether the maze generator reaches a dead-end and return to the previous cell
        # Until a unvisted neighbouring cell can be found
        elif (len(stack) > 0):
            current = stack.pop()

        else:
            pickle_out = open("grid"+str(mazesGenerated+1),"wb")
            pickle.dump(grid, pickle_out)
            pickle_out.close()
            if (mazesGenerated < (mazesToGenerate-1)):
                mazesGenerated += 1
                
                solving_current = None
                solving_stack = []
                solved = False
                count = 0
                full_count = 0

                startSelected = False
                destinationSelected = False

                grid = Grid(width, height)
                grid.createGrid()
            else:
                complete = True
                


    # Solving Algorithm / Solving the Maze            

    elif (startSelected and destinationSelected and not solved):
        if (beforeTime == 0):
            beforeTime = time.time()
            
        if (solving_current == None):
            
            solving_current = grid.getGridPos(startingX, startingY)
            solving_current.solved = True
            solving_current.weight = 0

        if (not (solving_current.x == destinationX and solving_current.y == destinationY)):
        
            next_cell = randomNeighbour(grid, solving_current)

            full_count += 1
            textRect1 = None
            textRect2 = None
            
            if (solving_current != next_cell):
                solving_stack.append(solving_current)

                next_cell.weight = solving_current.weight+1
                solving_current = next_cell
                solving_current.solved = True

                count += 1
                shortestPathStack.append(solving_current)
                
                pygame.draw.rect(canvas, ((255,194,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))

                font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
                text = font.render(str(solving_current.weight), True, (0,0,0))
                textRect1 = text.get_rect()
                textRect1.center = (((solving_current.x/width)*c1+(c1/width)/2),((solving_current.y/height)*c2+(c1/width)/2))
                canvas.blit(text, textRect1)
                
            else:
                pygame.draw.rect(canvas, ((255,0,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))

                font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
                text1 = font.render(str(solving_current.weight), True, (0,0,0))
                textRect2 = text1.get_rect()
                textRect2.center = (((solving_current.x/width)*c1+(c1/width)/2),((solving_current.y/height)*c2+(c1/width)/2))
                canvas.blit(text1, textRect2)
                count -= 1
                solving_current = solving_stack.pop()
                shortestPathStack.pop()
        
        else:
            afterTime = time.time()
            print("solved")
            solved = True
            print("The full count of number of steps/movements taken", full_count)
            print("The shortest path count", count)

            # Adding green square and text with number of cell/square for each cell/square
            for i in range(len(shortestPathStack)):
                solved_current = shortestPathStack[i]
                pygame.draw.rect(canvas, ((0,255,0)), ((solved_current.x/width)*c1+(c1/width)/5,(solved_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))

                # Adding number text for the solved cells/squares
                font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
                text = font.render(str(i+1), True, (0,0,0))
                textRect = text.get_rect()
                textRect.center = (((solved_current.x/width)*c1+(c1/width)/2),((solved_current.y/height)*c2+(c1/width)/2))
                canvas.blit(text, textRect)
            totalTime = round(afterTime-beforeTime, 2)
            print("The time taken to solve the maze: ", totalTime, "seconds.")

            
            
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.update()


    # Ending the Game Loop if the Quit button is pressed
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            f = open("maze-output-file.txt", "w")
            f.write(str(time) + "\n")
            f.write(str(full_count) + "\n")
            f.write(str(count) + "\n")
            f.close()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = pygame.mouse.get_pressed(3)
            mouseCoordinates = pygame.mouse.get_pos()
            mouseX = math.floor((mouseCoordinates[0])/(c1/width))*(c1/width)
            mouseY = math.floor((mouseCoordinates[1])/(c2/width))*(c2/height)
            gridPositionX = round(mouseX/(c1/width))
            gridPositionY = round(mouseY/(c2/height))
            if (not startSelected and complete):
                startingY = gridPositionY
                startingX = gridPositionX
                if (startingX < width and startingY < height):
                    selected_current = grid.getGridPos(startingX, startingY)
                    pygame.draw.rect(canvas, ((0,255,0)), ((selected_current.x/width)*c1,(selected_current.y/height)*c2,(c1/width), c2/height))
                    startSelected = True
            elif(not destinationSelected and complete):
                destinationY = gridPositionY
                destinationX = gridPositionX
                if (destinationX < width and destinationY < height):
                    selected_current = grid.getGridPos(destinationX, destinationY)
                    pygame.draw.rect(canvas, ((255,0,0)), ((selected_current.x/width)*c1,(selected_current.y/height)*c2,(c1/width), c2/height))
                    destinationSelected = True
            elif((gridPositionX==6 and gridPositionY==4) or (gridPositionX==7 and gridPositionY==4)):
    
                solving_current = None
                solving_stack = []
                solved = False
                count = 0
                full_count = 0
                startSelected = False
                destinationSelected = False
                beforeTime = 0
                afterTime = 0
        pygame_widgets.update(events)
        pygame.display.update()
                
                
pygame.quit() # Quit the program when close window button is pressed

