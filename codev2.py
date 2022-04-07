#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:14:59 2022

@author: freddie
"""

import pygame 
import sys 
from numpy import random

# Width must be a multiple of rows as you cant have half a box
WIDTH = 700
ROWS = 70
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

prob = 0.06
death = 0.001

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

def draw_grid_lines():
    box_width = WIDTH//ROWS
    
    for i in range(ROWS):
        pygame.draw.line(WINDOW, BLACK, (0, i * box_width), (WIDTH, i * box_width))
        
    for j in range(ROWS):
        pygame.draw.line(WINDOW, BLACK , (j * box_width, 0), (j * box_width, WIDTH))  
    

def draw_grid(grid):
    
    for row in grid:
        for point in row:
            point.draw_boxes(WINDOW)
    draw_grid_lines()        
    pygame.display.update()
    

def box_locator(position):
    x,y = position 
    
    z = WIDTH/ROWS #Need to rename this variable 
    
    row_no = x //z
    col_no = y //z
    
    return row_no, col_no

def update_display(grid):
    
    for row in grid:

        for spot in row:
            spot.draw_boxes(WINDOW)

    draw_grid()

    pygame.display.update()


def infect(grid):
    pygame.time.delay(1000)
    x = ROWS//2
    y = ROWS//2
    grid[x][y].colour = RED
    
    return grid

    
def simulate(grid):

    for i in range(0,ROWS):
        for j in range(0,ROWS):
            
            if grid[i][j].colour == RED:
                for b in range(-1,2):
                    for c in range(-1,2):
                        grid[(i+b)%ROWS][(j+c)%ROWS].neighbours += 1
                        
    for i in range(0,ROWS):
        for j in range(0,ROWS):
            
            if grid[i][j].colour != BLACK:
                r = random.rand()
                d = random.rand()
            
                new_prob = prob * grid[i][j].neighbours
                if r < new_prob:
                    grid[i][j].colour = RED
                
                if grid[i][j].colour == RED:
                    grid[i][j].infection_timer += 1 
                grid[i][j].neighbours = 0
               
                if grid[i][j].infection_timer >= 14:
                    grid[i][j].colour = GREEN
                    
                
                if grid[i][j].colour == RED:
                    if d < death:
                        grid[i][j].colour = BLACK
                        
                 
    return grid


def main():
    day = 0
    grid = create_grid()
    draw_grid(grid)
    grid = infect(grid)
    draw_grid(grid)
    
       
    while day <=120:
        print("DAY:", day)
        pygame.time.delay(100)
        grid = simulate(grid) 
        draw_grid(grid)
        day += 1


    

main()

    
    
    
    
    




