#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 21:02:31 2022

@author: freddie
"""

import pygame 
import sys 
from numpy import random
import matplotlib.pyplot as plt
import numpy as np

# Width must be a multiple of rows as you cant have half a box
WIDTH = 700
ROWS = 100
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

prob = 0.07
death = 0.003
day_max = 300


def menu_create():
    pygame.display.set_caption('Simulation Menu')
    WINDOW.fill(WHITE)
    pygame.font.init()
    smallfont = pygame.font.SysFont('comic sans',35) 
    text1 = smallfont.render("Press Enter to begin the simulation" , False , BLACK) 
    text2 = smallfont.render("Press Space to pause/unpause the simulation" , False , BLACK) 
    text3 = smallfont.render("Press Escape to exit" , False , BLACK)
    WINDOW.blit(text1,(100,100))
    WINDOW.blit(text2,(100,200))
    WINDOW.blit(text3,(100,300))

    pygame.display.flip()
    running = True
    
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          pygame.quit()
          sys.exit()
          
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                begin()
                pygame.quit()
                sys.exit()
                
                
                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

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
        Box.draw_grid_lines()        
        pygame.display.update()
    


def infect(grid):

   
    pygame.time.delay(1000)
    x = random.randint(0, ROWS)
    y = random.randint(0,ROWS)
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
                if grid[i][j].colour != BLUE:
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


def begin():
    pygame.display.set_caption('Simulation')
    day = 0
    grid = Box.create_grid()
    Box.draw_grid(grid)
    grid = infect(grid)
    Box.draw_grid(grid)
    
    REDlist = []   
    WHITElist = []
    GREENlist = []
    BLUElist = []
    BLACKlist = [] 
    running = True
      
    while running == True:
        run = None
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = True
                    
                    
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                
                  
        while run == True:
           
            pygame.time.delay(1)
            grid = simulate(grid) 
            Box.draw_grid(grid)
            REDtotal = 0
            WHITEtotal = 0
            GREENtotal = 0
            BLUEtotal = 0
            BLACKtotal = 0
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
               
                    
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            
            
            for i in range(0,ROWS):
                for j in range(0,ROWS):
                    if grid[i][j].colour == RED:
                        REDtotal += 1
                    if grid[i][j].colour == WHITE:
                        WHITEtotal +=1
                    if grid[i][j].colour == GREEN:
                        GREENtotal +=1
                    if grid[i][j].colour == BLUE:
                        BLUEtotal +=1
                    if grid[i][j].colour == BLACK:
                        BLACKtotal +=1
            REDlist.append(REDtotal)
            WHITElist.append(WHITEtotal)
            GREENlist.append(GREENtotal)
            BLUElist.append(BLUEtotal)
            BLACKlist.append(BLACKtotal)
            day += 1
    
                
            if day > day_max:
                run = False
                running = False
    
    x = [0]
    for y in range(0,150):
        x.append(y)
    a = REDlist
    b = WHITElist 
    c = GREENlist
    d = BLUElist
    e = BLACKlist
    
    fig, ax = plt.subplots()
    
    ax.plot(x, a, 'r', label = 'infected')
    ax.plot(x, b, 'k--', label = 'succeptible')
    ax.plot(x, c, 'g', label = 'recovered')
    ax.plot(x, d, 'b', label = 'vaccinated')
    ax.plot(x, e, 'k', label = 'dead')
    
    leg = ax.legend()
    
    plt.ylabel('No. of people')
    plt.xlabel('Days')
    plt.title('SIR graph')
    plt.show()  


def main():
    menu_create()

main()






    
    




