from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
from psychopy import parallel
from psychopy.tools import coordinatetools
from psychopy.tools import mathtools
import datetime
import os
import sys
import serial
import time
import struct
import numpy as np
import pandas as pd

# allocate window and graphics
win = visual.Window(size=(800, 800),
                    pos=(100, 100),
                    fullscr=False,
                    screen=0,
                    allowGUI=False,
                    allowStencil=False,
                    monitor='testMonitor',
                    color='gray',
                    colorSpace='rgb',
                    blendMode='avg',
                    useFBO=False,
                    units='cm')

# circle stimulus
search_circle = visual.Circle(win, radius=0.5, lineColor='white', fillColor='gray')
cursor_circle = visual.Circle(win, radius=0.4, fillColor='white')
start_circle = visual.Circle(win, radius=0.5, fillColor='blue')
target_circle = visual.Circle(win, radius=0.5, fillColor='blue')
feedback_circle = visual.Circle(win, radius=0.5, fillColor='white')

mouse = event.Mouse(visible=False, win=win)

# initial state
state = 'search'

# state durations
t_hold = 1.0
t_iti = 1.0
t_feedback = 1.0

num_trials = 5
current_trial = 0

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

target_distance = 6
target_circle.pos = (0, target_distance)

cursor_rotation = 30

while current_trial < num_trials:

    resp = event.getKeys(keyList=['d', 'k', 'escape'])
    rt = state_clock.getTime()

    cursor_circle.pos = mouse.getPos()
    theta, r = coordinatetools.cart2pol(cursor_circle.pos[0], cursor_circle.pos[1])

    if state == 'search':
        search_circle.radius = r
        search_circle.draw()
        
        # exit state if cursor and start circles overlap
        if mathtools.distance(start_circle.pos, cursor_circle.pos) < 0.2:
            state = 'hold'
            state_clock.reset()

    if state == 'hold':
        start_circle.draw()
        cursor_circle.draw()
        if state_clock.getTime() >= t_hold:
            state = 'reach'
            state_clock.reset()

    if state == 'reach':
        cursor_circle.pos = coordinatetools.pol2cart(theta + cursor_rotation, r)
        start_circle.draw()
        target_circle.draw()
        cursor_circle.draw()
        if mathtools.distance(start_circle.pos, cursor_circle.pos) >= target_distance:
            feedback_circle.pos = coordinatetools.pol2cart(theta + cursor_rotation, target_distance)            
            state = 'feedback'
            state_clock.reset()

    if state == 'feedback':
        start_circle.draw()
        target_circle.draw()
        feedback_circle.draw()
        if state_clock.getTime() > t_feedback:
            state = 'iti'
            state_clock.reset()

    if state == 'iti':
        if state_clock.getTime() > t_iti:
            state = 'search'
            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        win.close()
        core.quit()

    win.flip()
