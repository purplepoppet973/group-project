#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:14:59 2022

@author: freddie
"""

import pygame 
import sys 


WIDTH = 800
ROWS = 50
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

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
       
        
        
    def draw_boxes(self, WINDOW):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, WIDTH / ROWS ,WIDTH / ROWS ))
    

def create_grid():
    grid = []
    box_width = WIDTH//ROWS
    
    
    for i in range(ROWS):
        
        for j in range(ROWS):
            
           box = Box(j, i, box_width)
           grid.append([box])
   
    return grid

def draw_grid_lines():
    box_width = WIDTH/ROWS
    
    for i in range(ROWS):
        pygame.draw.line(WINDOW, BLACK, (0, i * box_width), (WIDTH, i * box_width))
        
    for j in range(ROWS):
        pygame.draw.line(WINDOW, BLACK , (j * box_width, 0), (j * box_width, WIDTH))  
    

def draw_grid():
    grid = create_grid()
    for row in grid:
        for point in row:
            point.draw_boxes(WINDOW)
    draw_grid_lines()        
    pygame.display.update()
    
def main():
    draw_grid()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




