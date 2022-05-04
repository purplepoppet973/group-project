#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 18:13:08 2022

@author: freddie
"""
import pygame 
import sys 
from numpy import random
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 700
ROWS = 100
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


class Simulation:
    

    def __init__(self, grid, day, day_max, prob, death, vax_level, vax_day):
        self.grid = grid
        self.day = day
        self.day_max = day_max
        self.prob = prob
        self.death = death
        self.vax_level = vax_level
        self.vax_day = vax_day
    
    

    def infect(grid):
    
        x = random.randint(0, ROWS)
        y = random.randint(0,ROWS)
        grid[x][y].colour = RED
    
        return grid
    
    
    def vaccinate(grid, day, vax_level, vax_day):
    
        for i in range(0,ROWS):
            for j in range(0,ROWS):
                if grid[i][j].colour == WHITE:
                    v = random.rand()
                    if v < vax_level:
                        grid[i][j].colour = BLUE

        return grid
    
    def simulate(grid, day, prob, death, day_max, vax_level, vax_day):
    
        if day == 0 :
            Simulation.infect(grid)
    
        if day >= vax_day:
            Simulation.vaccinate(grid, day, vax_level, vax_day)
        
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
