# Author: Sulaiman Bakali Mueden
# Date: 6th Jan 2024

# This program loads a generated maze and solves it using Dijkstra's algorithm

import pickle
import pygame
import random
import math
import time

from pygame.locals import *

from Cell import Cell
from Cell import Grid
from Cell import *


# This is used to import the maze and assign it to a new Grid (maze) object

pickle_in = open("grid1","rb")
grid = pickle.load(pickle_in)

width = grid.gridLength()
height = grid.gridLength()


# These are used to initialize the game

# Initializing the Game
pygame.init()

pygame.font.init()

# Colours used in the program
colour = (255, 255, 255)
line_colour = (0,0,0)
rect_colour = (0,255,0)

# Initialize the canvas with the title and logo
canvas = pygame.display.set_mode((500, 500))

pygame.display.set_caption("a-star")

img = pygame.image.load('qmul_logo.jpg')
pygame.display.set_icon(img)

# Paint the canvas with the variable color's RBG value
canvas.fill(colour)

# Draw the grid
grid.drawGrid()


# These are used for maze generation and manipulation

# X and Y dimensions/size of the canvas
c1, c2 = canvas.get_size()

# Stack for the recursive maze generation
stack= []



# These are helper function which includes index, checkNeighbour and randomNeighbour

# The index function calculates the index value and performs checks, taking an integer as an argument.
# The assumption is that the maze dimensions are even. The dimensions must be kept even.
def index(i):
    if (i<0 or i>width-1 or i>height-1):
        return None
    return i


# The checkNeighbours function checks whether each side of a cell is traversable and hasn't been visited
# It takes the grid and current cell as arguments and it returns a random neighbouring cell.
# If there isn't a neighbouring cell that can be traversed to, then it returns the parameter current.
def checkNeighbours(grid, current):
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

#manhattan distance
def cityBlock(A, B):
    total=0
    if(A.x<B.x):
        total+=A.x-B.x
    else:
        total+=B.x-A.x
    if(A.y<B.y):
        total+=A.y-B.y
    else:
        total+=B.y-A.y
    return abs(total)


# The randomNeighbour function takes the grid and current cell as parameters.
# It returns a random neighbouring cell that hasn't had its weight evaluated.
# Otherwise, it simply returns the argument current.
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
    # This is checking whether each neighbouring cell has been evaluated
    # If not, add it to the neighbours list to be randomly selected
    if (not current.walls[0] and not top.evaluated):
        neighbours.append(top)
        
    if (not current.walls[1] and not right.evaluated):
        neighbours.append(right)
        
    if (not current.walls[2] and not bottom.evaluated):
        neighbours.append(bottom)
        
    if (not current.walls[3] and not left.evaluated):
        neighbours.append(left)

    # Checking if a neighbour has been added to the list and selecting a random one
    if (len(neighbours) > 0):
        r= random.randint(0, len(neighbours))
        return neighbours[r-1]

    # Otherwise, returning the current cell
    else:
        return current


# The function nearbyNeighbours returns a list of all neighbouring cells that are traversable and haven't been evaluated
def nearbyNeighbours(grid, current):
    neighbours = []

    x = current.x
    y = current.y

    #top = grid[index(x)][index(y-1)]
    top = current
    x = index(current.x)
    y = index(current.y-1)
    if (not x == None and not y == None):
        #print(x, y, "top")
        top = grid.getGridPos(x,y)

    #right = grid[index(x+1)][index(y)]
    right = current
    x = index(current.x+1)
    y = index(current.y)
    if (not x == None and not y == None):
        #print(x, y, "right")
        right = grid.getGridPos(x,y)

    #bottom = grid[index(x)][index(y+1)]
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
    if (not current.walls[0] and not top.evaluated):
        neighbours.append(top)
        
    if (not current.walls[1] and not right.evaluated):
        neighbours.append(right)
        
    if (not current.walls[2] and not bottom.evaluated):
        neighbours.append(bottom)
        
    if (not current.walls[3] and not left.evaluated):
        neighbours.append(left)

    # Checking if a neighbour has been added to the list and selecting a random one
    if (len(neighbours) > 0):
        return neighbours

    # Otherwise, returning the current cell
    else:
        return [current]


# The function randomNeighbours returns a list of all neighbouring cells that are traversable and haven't been solved
def randomNeighbours(grid, current):
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
    if (not current.walls[0] and top.evaluated):
        neighbours.append(top)
        
    if (not current.walls[1] and right.evaluated):
        neighbours.append(right)
        
    if (not current.walls[2] and bottom.evaluated):
        neighbours.append(bottom)
        
    if (not current.walls[3] and left.evaluated):
        neighbours.append(left)

    # Checking if a neighbour has been added to the list and selecting a random one
    if (len(neighbours) > 0):
        return neighbours

    # Otherwise, returning the current cell
    else:
        return [current]






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

allNodesChecked = False

evaluating_stack = []
second_evaluating_stack = []

beforeTime = 0
afterTime = 0

start=grid.getGridPos(0,0)
end=grid.getGridPos(0,0)

# Game Loop

running = True

while running:

    
    # Maze Generation
    
    # Checking whether the maze generation is complete
    if (not complete):

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
            complete = True


    # Solving Algorithm / Solving the Maze            

    elif (startSelected and destinationSelected and not solved):
        if (beforeTime == 0):
            beforeTime = time.time()
        
        if (solving_current == None):
            
            solving_current = grid.getGridPos(startingX, startingY)
            solving_current.evaluated = True
            solving_current.weight = 0
            start=grid.getGridPos(startingX, startingY)
            end=grid.getGridPos(destinationX, destinationY)

        if (not allNodesChecked):

            if(solving_current.x==destinationX and solving_current.y==destinationY):
                    allNodesChecked=True
                    solving_current = grid.getGridPos(destinationX, destinationY)
                    afterTime = time.time()
                    time=round(afterTime-beforeTime,2)
            else:
                next_cell = randomNeighbour(grid, solving_current)
                    
                if (solving_current != next_cell):
                        solving_stack.append(solving_current)

                        # checking nearby cells for lowest weighted cell
                        nearbyCells = nearbyNeighbours(grid, solving_current)
                        next_cell=nearbyCells[0]
                        for i in range(0, len(nearbyCells)):
                            if (cityBlock(nearbyCells[i],end))< cityBlock(next_cell,end):
                                next_cell = nearbyCells[i]

                        next_cell.weight = solving_current.weight+1

                        next_cell.evaluated = True
                        solving_current = next_cell

                        count += 1
                        full_count += 1
                        
                        pygame.draw.rect(canvas, ((255,194,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))

                        font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
                        text = font.render(str(solving_current.weight), True, (0,0,0))
                        textRect1 = text.get_rect()
                        textRect1.center = (((solving_current.x/width)*c1+(c1/width)/2),((solving_current.y/height)*c2+(c1/width)/2))
                        canvas.blit(text, textRect1)
                    
                elif(len(solving_stack)>0):
                    pygame.draw.rect(canvas, ((255,0,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))
                    font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
                    text1 = font.render(str(count), True, (0,0,0))
                    textRect2 = text1.get_rect()
                    textRect2.center = (((solving_current.x/width)*c1+(c1/width)/2),((solving_current.y/height)*c2+(c1/width)/2))
                    canvas.blit(text1, textRect2)
                    solving_current = solving_stack.pop()
                    count -= 1

        elif (not (solving_current.x == startingX and solving_current.y == startingY)):
            solving_stack.append(solving_current)
            solving_current.solved = True
            pygame.draw.rect(canvas, ((0,255,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))
            # Adding number text for the solved cells/squares
            font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
            text = font.render(str(solving_current.weight), True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (((solving_current.x/width)*c1+(c1/width)/2),((solving_current.y/height)*c2+(c1/width)/2))
            canvas.blit(text, textRect)

            # finds the lowest weighted next cell
            next_cells = randomNeighbours(grid, solving_current)
            for cell in next_cells:
                if (cell.weight <= solving_current.weight):
                    solving_current = cell

                
        else:
            solved = True
            print("solved by a*")
            print("The full count of number of steps/movements taken", full_count)
            print("The shortest path count", count)
            print("The time taken to solve the maze: ", time, "seconds.")
            f = open("a-star-output-file.txt", "w")
            f.write(str(time) + "\n")
            f.write(str(full_count) + "\n")
            f.write(str(count) + "\n")
            f.close()


    clock = pygame.time.Clock()
    clock.tick(10)
    pygame.display.update()


    # Ending the Game Loop if the Quit button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = pygame.mouse.get_pressed(3)
            mouseCoordinates = pygame.mouse.get_pos()
            mouseX = math.floor((mouseCoordinates[0])/(c1/width))*(c1/width)
            mouseY = math.floor((mouseCoordinates[1])/(c2/width))*(c2/height)
            gridPositionX = round(mouseX/(c1/width))
            gridPositionY = round(mouseY/(c2/height))
            #print(cityBlock(grid.getGridPos(gridPositionX, gridPositionY),end))
            if (not startSelected and complete):
                startingY = gridPositionY
                startingX = gridPositionX
                selected_current = grid.getGridPos(startingX, startingY)
                pygame.draw.rect(canvas, ((0,255,0)), ((selected_current.x/width)*c1,(selected_current.y/height)*c2,(c1/width), c2/height))
                startSelected = True
            elif(not destinationSelected and complete):
                destinationY = gridPositionY
                destinationX = gridPositionX
                selected_current = grid.getGridPos(destinationX, destinationY)
                pygame.draw.rect(canvas, ((255,0,0)), ((selected_current.x/width)*c1,(selected_current.y/height)*c2,(c1/width), c2/height))
                destinationSelected = True


pygame.quit() # Quit the program when close window button is pressed
