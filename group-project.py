#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 17:57:55 2022

@author: freddie
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Total population, N.
N = 1000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.2, 1./10 
# A grid of time points (in days)
t = np.linspace(0, 160, 160)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()



#animation
import matplotlib.animation as animation

#a decay graph is appearing over time
#a generator driven animation
#changing axes limits during animation
#https://matplotlib.org/stable/gallery/animation/animate_decay.html
import itertools

def data_gen():
    for cnt in itertools.count():
        t = cnt / 10
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
        
def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []

def run(data):
    #update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()
    
    if t>= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)
    
    return line,

ani = animation.FuncAnimation(fig, run, data_gen, interval = 10, init_func=init)
plt.show()
    
#more examples on https://matplotlib.org/stable/api/animation_api.html
 



# to save an animation 
ani.save('animation.mp4',clear_temp = False)

#alternative 1
#import all of the above imports AND
from IPython import display

#do relevant plotting of graph
#following the example on https://www.geeksforgeeks.org/how-to-save-matplotlib-animation/

#have copy and pasted here
# initializing a figure
fig = plt.figure()
  
# labeling the x-axis and y-axis
axis = plt.axes(xlim=(0, 4),  ylim=(-1.5, 1.5))
  
# initializing a line variable
line, = axis.plot([], [], lw=3)
  
def animate(frame_number):
    x = np.linspace(0, 4, 1000)
  
    # plots a sine graph
    y = np.sin(2 * np.pi * (x - 0.01 * frame_number))
    line.set_data(x, y)
    line.set_color('green')
    return line,
  
  
anim = animation.FuncAnimation(fig, animate, frames=100, 
                               interval=20, blit=True)
fig.suptitle('Sine wave plot', fontsize=14)
  
# converting to an html5 video
video = anim.to_html5_video()
  
# embedding for the video
html = display.HTML(video)
  
# draw the animation
display.display(html)
plt.close()


#alternative 2

#instead of vconverting to a HTML steps, can save to m4
# saving to m4 using ffmpeg writer
writervideo = animation.FFMpegWriter(fps=60)
anim.save('increasingStraightLine.mp4', writer=writervideo)
plt.close()

   
    