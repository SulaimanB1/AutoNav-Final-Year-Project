# Author: Sulaiman Bakali Mueden
# Date: 18th January 2024

# Title: Maze Generator
# Description: This program provides an interface to generate a randomly generated maze.

import pygame
import random
import math
import pickle

from pygame.locals import *


# Initializing the Game
pygame.init()

pygame.font.init()

# colours used in the program
colour = (255, 255, 255)
line_colour = (0,0,0)
rect_colour = (0,255,0)

# Initialize the canvas with the title and logo
canvas = pygame.display.set_mode((500, 500))

pygame.display.set_caption('Maze')

img = pygame.image.load('qmul_logo.jpg')
pygame.display.set_icon(img)

# X and Y dimensions/size of the canvas
c1, c2 = canvas.get_size()

maze_number = 1

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
        self.weight = float('inf') # default initialization of positive infinity
        self.explored = []  # list used to store explored cells
        
    def draw(self, line_colour):
        x = self.x
        y = self.y
        width = self.grid.width
        height = self.grid.height
        
        # top, right, bottom, left line
        if (self.walls[0]):
            pygame.draw.line(canvas, (line_colour), [(c1/width)*x,(c2/height)*y], [(c1/width)*(x+1),(c2/height)*(y)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(c1/width)*x,(c2/height)*y], [(c1/width)*(x+1),(c2/height)*(y)], 5)
            
        if (self.walls[1]):
            pygame.draw.line(canvas, (line_colour), [(c1/width)*(x+1),(c2/height)*(y)], [(c1/width)*(x+1),(c2/height)*(y+1)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(c1/width)*(x+1),(c2/height)*(y)], [(c1/width)*(x+1),(c2/height)*(y+1)], 5)
            
        if (self.walls[2]):
            pygame.draw.line(canvas, (line_colour), [(c1/width)*x,(c2/height)*(y+1)], [(c1/width)*(x+1),(c2/height)*(y+1)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(c1/width)*x,(c2/height)*(y+1)], [(c1/width)*(x+1),(c2/height)*(y+1)], 5)
        
        if (self.walls[3]):
            pygame.draw.line(canvas, (line_colour), [(c1/width)*x,(c2/height)*(y)], [(c1/width)*(x),(c2/height)*(y+1)], 5)
        else:
            pygame.draw.line(canvas, ((255,255,255)), [(c1/width)*x,(c2/height)*(y)], [(c1/width)*(x),(c2/height)*(y+1)], 5)

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
