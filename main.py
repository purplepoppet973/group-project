# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:06:41 2022

@author: freddie
"""

import pygame 
import sys 
from numpy import random
import matplotlib.pyplot as plt
import numpy as np
from grid_class import *
from Simulation_class import *

WIDTH = 700
ROWS = 100

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

# =============================================================================
# This section of the code sets up the parameters for the simulation
# =============================================================================


def settings():
    '''
    Determines from user input what simulations to run and graphs to produce.

    Returns
    -------
    None.

    '''
    
    q0 = input("Press 'a' if you would like to see a single simulation, or press 'b' if you would like to compare multiple variations of paramaters: ")
    
    if q0 == 'a':
        q1 = input("If you would like to use default settings: enter 'd', if you would like to use custom settings enter 'c': ")
        
        if q1 == "d":
            prob = 0.05
            death = 0.01
            day_max = 300
            vax_level = 0.008
            vax_day = 130
            menu_create(prob, death, day_max, vax_level, vax_day)
                
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
      
    elif q0 == "b":
        prob1 = float(input("Enter a value between 0 and 1 for the first simulation probability of infection: "))
        prob2 = float(input("Enter a value between 0 and 1 for the second simulation probability of infection: "))
            
        if prob1 >= 0 and prob1 <= 1 and prob2 >= 0 and prob2 <= 1:
            death1 = float(input("Enter a value between 0 and 1 for the first simulation probability of death: "))
            death2 = float(input("Enter a value between 0 and 1 for the second simulation probability of death: "))

            if death1 >= 0 and death1 <= 1 and death2 >= 0 and death2 <= 1 :  
                day_max = int(input("Enter an integer for how many days the simulation should run: "))
        
                q2 = input("If you wish for vaccinations to occur in simulation 1, enter 'y', otherwise enter 'n': ")
                 
                if q2 == 'y':
                    vax_day1 = int(input("At what day of the simulation do you wish for vaccinations to begin: "))
                    vax_level1 = float(input("Enter a value between 0 and 1 for the percetange of the susceptible poulation that get vaccainted each day: "))
                
                    if vax_level1 > 1 or vax_level1 < 0:
                        print("Error, not a correct input. Restart")
                        settings()
                
                elif q2 == 'n':
                    vax_day1 = 0
                    vax_level1 = 0
                    
                
                else:
                    print("Error, not a correct input. Restart")
                    settings()
                
                q3 = input("If you wish for vaccinations to occur in simulation 2, enter 'y', otherwise enter 'n': ")
                if q3 == 'y':
                    vax_day2 = int(input("At what day of the simulation do you wish for vaccinations to begin: "))
                    vax_level2 = float(input("Enter a value between 0 and 1 for the percetange of the susceptible poulation that get vaccainted each day: "))
                    
                    if vax_level2 > 1 or vax_level2 < 0:
                        print("Error, not a correct input. Restart")
                        settings()
                    
                    else:
                         print("Your simulations are now running. Your graphs will appear when the simualtions are complete.")
                         multi_sim(prob1,prob2, death1, death2, day_max, vax_level1, vax_level2, vax_day1, vax_day2)
               
                elif q3 == 'n':
                    vax_day2 = 0
                    vax_level2 = 0
                    print("Your simulations are now running. Your graphs will appear when the simualtions are complete.")
                    multi_sim(prob1,prob2, death1, death2, day_max, vax_level1, vax_level2, vax_day1, vax_day2)
                
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
        print("Error, not a correct input. Restart")
        settings()

# =============================================================================
# Section where the simulations are run 
# =============================================================================

def menu_create(prob, death, day_max, vax_level, vax_day,):
    '''
    Creates a startup menu in the pygame window explaining controls.

    Parameters
    ----------
    prob : The base probability of a covid spread to a new square
    death : The probability of an infected person dying
    day_max : The day at which the simulation ends
    vax_level : The proprotion of sucestible people being vaccinated each day
    vax_day : The day the vaccinations begin

    Returns
    -------
    None.

    '''
    WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
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
                single_sim(prob, death, day_max, vax_level, vax_day)
                pygame.quit()
                sys.exit()               
                     
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    

def single_sim(prob, death, day_max, vax_level, vax_day):
    '''
    Runs a simulation of covid in the pygame window.

    Parameters
    ----------
    prob : The base probability of a covid spread to a new square
    death : The probability of an infected person dying
    day_max : The day at which the simulation ends
    vax_level : The proprotion of sucestible people being vaccinated each day
    vax_day : The day the vaccinations begin

    Returns
    -------
    None.

    '''
    WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Simulation - Press space to begin')
    day = 0
    grid = Box.create_grid()
    Box.draw_grid(grid, WINDOW)
    

    REDlist, WHITElist, GREENlist, BLUElist, BLACKlist = [],[],[],[],[]

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
            grid = Simulation.simulate(grid, day, prob, death, day_max, vax_level, vax_day) 
            Box.draw_grid(grid, WINDOW)
            
            REDtotal, WHITEtotal, GREENtotal, BLUEtotal, BLACKtotal = 0,0,0,0,0
        

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

    

    single_graph_maker(REDlist, WHITElist, GREENlist, BLUElist, BLACKlist, vax_day, day_max)
    
def multi_sim(prob1,prob2, death1, death2, day_max, vax_level1, vax_level2, vax_day1, vax_day2):
    '''
    Runs two non-physical covid simulations.

    Parameters
    ----------
    prob1 : The base probability of a covid spread to a new square in simulation 1 
    prob2 : The base probability of a covid spread to a new square in simulation 2
    death1 : The probability of an infected person dying in simulation 1
    death2 : The probability of an infected person dying in simulation 2
    day_max : The day at which the simulation ends
    vax_level1 : The proprotion of sucestible people being vaccinated each day in simulation 1 
    vax_level2 : The proprotion of sucestible people being vaccinated each day in simulation 2
    vax_day1 : The day the vaccinations begin in simulation 1 
    vax_day2 : The day the vaccinations begin in simulation 2

    Returns
    -------
    None.

    '''
   
    REDlist1, WHITElist1, GREENlist1, BLUElist1, BLACKlist1 = [],[],[],[],[]
    REDlist2, WHITElist2, GREENlist2, BLUElist2, BLACKlist2 = [],[],[],[],[]
    day = 0
    grid1 = Box.create_grid()
    grid2 = Box.create_grid()
    run = True
    
    while run == True:
        REDtotal1, WHITEtotal1, GREENtotal1, BLUEtotal1, BLACKtotal1 = 0,0,0,0,0
        REDtotal2, WHITEtotal2, GREENtotal2, BLUEtotal2, BLACKtotal2 = 0,0,0,0,0
        grid1 = Simulation.simulate(grid1, day, prob1, death1, day_max, vax_level1, vax_day1)
        grid2 = Simulation.simulate(grid2, day, prob2, death2, day_max, vax_level2, vax_day2)
        
        
        for i in range(0,ROWS):
            for j in range(0,ROWS):
                if grid1[i][j].colour == RED:
                    REDtotal1 += 1
                if grid2[i][j].colour == RED:
                    REDtotal2 += 1
                
                if grid1[i][j].colour == WHITE:
                    WHITEtotal1 +=1
                if grid2[i][j].colour == WHITE:
                    WHITEtotal2 +=1
                
                if grid1[i][j].colour == GREEN:
                    GREENtotal1 +=1
                if grid2[i][j].colour == GREEN:
                    GREENtotal2 +=1
            
                if grid1[i][j].colour == BLUE:
                    BLUEtotal1 +=1
                if grid2[i][j].colour == BLUE:
                    BLUEtotal2 +=1
                
                if grid1[i][j].colour == BLACK:
                    BLACKtotal1 +=1
                if grid2[i][j].colour == BLACK:
                    BLACKtotal2 +=1

        REDlist1.append(REDtotal1)
        WHITElist1.append(WHITEtotal1)
        GREENlist1.append(GREENtotal1)
        BLUElist1.append(BLUEtotal1)
        BLACKlist1.append(BLACKtotal1)
        
        REDlist2.append(REDtotal2)
        WHITElist2.append(WHITEtotal2)
        GREENlist2.append(GREENtotal2)
        BLUElist2.append(BLUEtotal2)
        BLACKlist2.append(BLACKtotal2)
        
        day += 1


        if day > day_max:
            run = False
    
    multi_graph_maker(REDlist1, REDlist2, WHITElist1,WHITElist2,GREENlist1,GREENlist2,BLUElist1, BLUElist2,BLACKlist1, BLACKlist2, vax_day1, vax_day2, day_max )

# =============================================================================
# # This section contains the code where the graphs are made:
# =============================================================================

def single_graph_maker(REDlist, WHITElist, GREENlist, BLUElist, BLACKlist, vax_day, day_max):
    '''
    Creates a single SIRVD graph from the single simulation data

    Parameters
    ----------
    REDlist : The list of infected plot points
    WHITElist : The list of susceptible plot points
    GREENlist : The list of recovered plot points
    BLUElist : The list of vaccinated plot points
    BLACKlist : The list of dead plot points
    vax_day : The day the vaccinations begin
    day_max : The day the simulation ends

    Returns
    -------
    None.

    '''
    x = [0]
    for y in range(0,day_max):
        x.append(y)
    
  

    fig, ax = plt.subplots()

    ax.plot(x, REDlist, 'r', label = 'infected')
    ax.plot(x, WHITElist, 'k--', label = 'susceptible')
    ax.plot(x, GREENlist, 'g', label = 'recovered')
    ax.plot(x, BLUElist, 'b', label = 'vaccinated')
    ax.plot(x, BLACKlist, 'k', label = 'dead')
    plt.axvline(x= vax_day, ymin=0, ymax=1, color = 'blue', linestyle=":")
    
    
    leg = ax.legend()

    plt.ylabel('No. of people')
    plt.xlabel('Days')
    plt.title('SIRVD graph')
    plt.show()  

def multi_graph_maker(REDlist1, REDlist2, WHITElist1,WHITElist2,GREENlist1,GREENlist2,BLUElist1, BLUElist2,BLACKlist1, BLACKlist2, vax_day1, vax_day2, day_max ):
    '''
    Creates two SIRVD graphs for comparison from the multi-simulation data.

    Parameters
    ----------
    REDlist1 : The list of infected plot points for simulation 1 
    REDlist2 : The list of infected plot points for simulation 2 
    WHITElist1 : The list of susceptible plot points for simulation 1
    WHITElist2 : The list of susceptible plot points for simulation 2 
    GREENlist1 : The list of recovered plot points for simulation 1 
    GREENlist2 : The list of recovered plot points for simulation 2
    BLUElist1 : The list of vaccinated plot points for simulation 1 
    BLUElist2 : The list of vaccinated plot points for simulation 1 
    BLACKlist1 : The list of dead plot points for simulation 1
    BLACKlist2 : The list of dead plot points for simulation 2
    vax_day1 : The day the vaccinations begin in simulation 1 
    vax_day2 : The day the vaccinations begin in simulation 2
    day_max : The day the simulation ends
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    x = [0]
    for y in range(0, day_max):
        x.append(y)
    
    fig, axs = plt.subplots(2)
    fig.suptitle('Comparison of SIRVD Graphs')
    axs[0].plot(x, REDlist1, 'r', label = 'infected')
    axs[0].plot(x, WHITElist1, 'k--', label = 'susceptible')
    axs[0].plot(x, GREENlist1, 'g', label = 'recovered')
    axs[0].plot(x, BLUElist1, 'b', label = 'vaccinated')
    axs[0].plot(x, BLACKlist1, 'k', label = 'dead')
    
    if vax_day1 > 0:
        axs[0].axvline(x= vax_day1, ymin=0, ymax=1, color = 'blue', linestyle=":")

    axs[0].set_ylabel("No. of people")
    
    axs[1].plot(x, REDlist2, 'r', label = 'infected')
    axs[1].plot(x, WHITElist2, 'k--' ,label = 'susceptible')
    axs[1].plot(x, GREENlist2, 'g', label = 'recovered')
    axs[1].plot(x, BLUElist2, 'b', label = 'vaccinated')
    axs[1].plot(x, BLACKlist2, 'k', label = 'dead')
    
    if vax_day2 > 0:
        axs[1].axvline(x= vax_day2, ymin=0, ymax=1, color = 'blue', linestyle=":")
    
    axs[1].set_xlabel('Days')
    axs[1].set_ylabel("No. of people")
    
    
    axs[0].legend(fontsize = 'x-small')
    plt.show
    
   
# =============================================================================
# Where the code is run:        
# =============================================================================

def main():
    '''
    Runs settings() and begins the code.

    Returns
    -------
    None.

    '''
    settings()
   

main()
