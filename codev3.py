# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:06:41 2022

@author: daisy
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

    
def settings():
    q1 = input("If you would like to use default settings: enter 'd', if you would like to use custom settings enter 'c': ")
    
    if q1 == "d":
        prob = 0.07
        death = 0.01
        day_max = 300
        vax_level = 0.008
        vax_day = 100
            
    elif q1 == "c":
        prob = float(input("Enter a value between 0 and 1 for the probability of infection: "))
        
        if prob >= 0 and prob <= 1:
            death = float(input("Enter a value between 0 and 1 for the probability of death: "))
            
            if death >= 0 and death <= 1:  
                day_max = int(input("Enter an integer for how many days the simulation should run: "))
        
                q2 = input("If you wish for vaccinations to occur in this simulation, enter 'y', otherwise enter 'n': ")
                 
                if q2 == 'y':
                    vax_day = int(input("At what day of the simulation do you wish for vaccinations to begin: "))
                    vax_level = float(input("Enter a value between 0 and 1 for the percetange of the susceptible poulation that get vaccainted each day: "))
                
                    if vax_level > 1 or vax_level < 0:
                        print("Error, not a correct input. Restart")
                        settings()
                
                    else:
                        menu_create(prob, death, day_max, vax_level, vax_day)
                    
                elif q2 == 'n':
                    vax_day = 0
                    vax_level = 0
                    menu_create(prob, death, day_max, vax_level, vax_day)
                else:
                    print("Error, not a correct input. Restart")
                    settings()
            
            
            
            else: 
                print("Error, not a correct input. Restart")
                settings()
   
        else:
            print("Error, not a correct input. Restart")
            settings()
   
    else:
        print("Error, not a correct input. Restart.")
        settings()
    



def menu_create(prob, death, day_max, vax_level, vax_day):
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
                begin(prob, death, day_max, vax_level, vax_day)
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

    caption = "Simulation - press space to start" 
    pygame.time.delay(1000)
    x = random.randint(0, ROWS)
    y = random.randint(0,ROWS)
    grid[x][y].colour = RED

    return grid


def vaccinate(grid, day, vax_level, vax_day):

    if day >= vax_day:

        for i in range(0,ROWS):
            for j in range(0,ROWS):
                if grid[i][j].colour == WHITE:
                    v = random.rand()
                    if v < vax_level:
                        grid[i][j].colour = BLUE

    return grid
def simulate(grid, day, prob, death, day_max, vax_level, vax_day):

    vaccinate(grid, day, vax_level, vax_day)
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


def begin(prob, death, day_max, vax_level, vax_day):
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
            caption = "Simulation day number: " + str(day)
            pygame.display.set_caption(caption)
            pygame.time.delay(1)
            grid = simulate(grid, day, prob, death, day_max, vax_level, vax_day) 
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
    for y in range(0,day_max):
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
    plt.title('SIRVD graph')
    plt.show()  


def main():
    settings()
   

main()