from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
from psychopy import parallel
from psychopy.tools import coordinatetools
import datetime
import os
import sys
import serial
import time
import struct
import numpy as np
import pandas as pd

# allocate window and graphics
win = visual.Window(size=(500, 500),
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
cursor_circle = visual.Circle(win, radius=1, fillColor='white')
start_circle = visual.Circle(win, radius=1, fillColor='white')
target_circle = visual.Circle(win, radius=1, fillColor='white')
feedback_circle = visual.Circle(win, radius=1, fillColor='white')

mouse = event.Mouse(visible=False, win=win)

# initial state
state = 'search'

# state durations
t_iti = 0.5
t_feedback = 0.5

num_trials = 5
current_trial = 0

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

while current_trial < num_trials:

    resp = event.getKeys(keyList=['d', 'k', 'escape'])
    rt = state_clock.getTime()

    cursor_circle.pos = mouse.getPos()

    if state == 'search':
        cursor_circle.draw()
        start_circle.draw()
        if exit_state == True:
            state = 'hold'

    if state == 'hold':
        cursor_circle.draw()
        start_circle.draw()
        if exit_state == True:
            state = 'reach'


    if state == 'reach':
        cursor_circle.draw()
        start_circle.draw()
        target_circle.draw()
        if exit_state == True:
            state = 'feedback'

    if state == 'feedback':
        feedback_circle.draw()
        start_circle.draw()
        target_circle.draw()
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
