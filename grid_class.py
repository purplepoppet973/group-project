#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 17:03:46 2022

@author: freddie
"""
import pygame 
import sys 
from numpy import random
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 700
ROWS = 100


WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)



class Box:
    def __init__(self, row, column, width):
        self.row = row
        self.column = column
        self.x = int(row * width)
        self.y = int(column * width)
        self.colour = WHITE
        self.neighbours = 0 
        self.infection_timer = 0


    def draw_boxes(self, WINDOW):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, WIDTH / ROWS ,WIDTH / ROWS ))


    def create_grid():
        grid = []
        box_width = WIDTH//ROWS


        for i in range(ROWS):
            grid.append([])
            for j in range(ROWS):

               box = Box(i, j, box_width)
               grid[i].append(box)

        return grid

    def draw_grid_lines(WINDOW):
        box_width = WIDTH//ROWS

        for i in range(ROWS):
            pygame.draw.line(WINDOW, BLACK, (0, i * box_width), (WIDTH, i * box_width))

        for j in range(ROWS):
            pygame.draw.line(WINDOW, BLACK , (j * box_width, 0), (j * box_width, WIDTH))  


    def draw_grid(grid, WINDOW):
        for row in grid:
            for point in row:
                point.draw_boxes(WINDOW)
        Box.draw_grid_lines(WINDOW)        
        pygame.display.update()
        
  
       
       
       
       
       
       
       

     