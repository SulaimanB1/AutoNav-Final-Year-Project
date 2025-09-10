# Author: Sulaiman Bakali Mueden
# Date: 7th Jan 2024

# This program loads a generated maze and solves it using Breadth-First Search

import pickle
import pygame
import random
import math
import time
from pygame.locals import *
from Cell import Cell
from Cell import Grid
from Cell import *


# This is used to import the maze and assign a reference of it to a new Grid (maze) object
pickle_in=open("grid1", "rb")
grid=pickle.load(pickle_in)
width=grid.gridLength()
height=grid.gridLength()

# Initializing the Game
pygame.init()
pygame.font.init()
canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("BFS")
img = pygame.image.load('qmul_logo.jpg')
pygame.display.set_icon(img)
colour = (255, 255, 255)
canvas.fill(colour)
line_colour = (0,0,0)
rect_colour = (0,255,0)
grid.drawGrid()

# These are used for maze generation and manipulation
c1, c2 = canvas.get_size()
stack= []

# The index function calculates the index value and performs checks, taking an integer as an argument.
# The assumption is that the maze dimensions are even. The dimensions must be kept even.
def index(i):
    if (i<0 or i>width-1 or i>height-1):
        return None
    return i

# The function randomNeighbours returns a list of all neighbouring cells that are traversable and haven't been evaluated
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


current = None # Initialize current outside of Game Loop to prevent it being reset
# Initialize current cell variable for solving and stack
solving_current = None
solving_stack = []
shortestPathStack=[]
solved = False
count = 0
full_count = 0
startSelected = False
destinationSelected = False
startTime=0
endTime=0
frontier=[]
explored=[]
allNodesChecked=False

# Game Loop

running = True

while running:
    if (not(startSelected and destinationSelected)):
        pass
    elif ((startSelected and destinationSelected) and (not solved)):
        if (startTime==0):
            startTime=time.time()
        if (solving_current==None):
            solving_current=grid.getGridPos(startingX,startingY)
            solving_current.evaluated=True
            frontier.append(solving_current)
        if (not allNodesChecked):
            if (not(solving_current.x==destinationX and solving_current.y==destinationY)):
                solving_current=frontier.pop(0)
                solving_current.evaluated=True
                next_cells = randomNeighbours(grid, solving_current)
                if (next_cells==solving_current):
                    explored.pop()
                for cell in next_cells:
                    if (cell.evaluated==False):
                        frontier.append(cell)
                        cell.explored.append(solving_current)
                        full_count+=1
                        pygame.draw.rect(canvas, ((255,194,0)), ((cell.x/width)*c1+(c1/width)/5,(cell.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))
            else:
                allNodesChecked=True
        elif (not solved):
            pygame.draw.rect(canvas, ((0,255,0)), ((solving_current.x/width)*c1+(c1/width)/5,(solving_current.y/height)*c2+(c2/height)/5,(c1/width)/1.5, (c2/height)/1.5))
            font = pygame.font.SysFont('freeanbold.tff', int(c1/(width+height)))
            text = font.render(str(count+1), True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (((solving_current.x/width)*c1+(c1/width)/2),((solving_current.y/height)*c2+(c1/width)/2))
            canvas.blit(text, textRect)
            shortestPathStack.append(solving_current)
            count+=1
            solving_current=solving_current.explored[0]
            if (solving_current.x==startingX and solving_current.y==startingY):
                solved=True
                endTime=time.time()
                time=round(endTime-startTime,2)
                print("solved using bfs")
                print("time:",time,"seconds")
                print("full count:",full_count)
                print("count:",count)
                f = open("bfs-output-file.txt", "w")
                f.write(str(time) + "\n")
                f.write(str(full_count) + "\n")
                f.write(str(count) + "\n")
                f.close()

    clock = pygame.time.Clock()
    clock.tick(10)
    pygame.display.update()
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
            if (not startSelected):
                startingY = gridPositionY
                startingX = gridPositionX
                selected_current = grid.getGridPos(startingX, startingY)
                pygame.draw.rect(canvas, ((0,255,0)), ((selected_current.x/width)*c1,(selected_current.y/height)*c2,(c1/width), c2/height))
                startSelected = True
                pygame.display.update()
            elif(not destinationSelected):
                destinationY = gridPositionY
                destinationX = gridPositionX
                selected_current = grid.getGridPos(destinationX, destinationY)
                pygame.draw.rect(canvas, ((255,0,0)), ((selected_current.x/width)*c1,(selected_current.y/height)*c2,(c1/width), c2/height))
                destinationSelected = True
                pygame.display.update()
pygame.quit()

