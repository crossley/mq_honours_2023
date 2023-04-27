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
circle_stim = visual.Circle(win, radius=1, fillColor='white')
fb_stim_correct = visual.Circle(win, radius=2, fillColor='green')
fb_stim_incorrect = visual.Circle(win, radius=2, fillColor='red')

mouse = event.Mouse(visible=False, win=win)

# initial state
state = 'stim'

# state durations
t_iti = 0.5
t_fb_delay = 0.0
t_fb_dur = 0.5

fb_acc = 'NA'

num_trials = 5
current_trial = 0

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

while current_trial < num_trials:

    resp = event.getKeys(keyList=['d', 'k', 'escape'])
    rt = state_clock.getTime()

    mouse_position = mouse.getPos()

    if state == 'stim':k
        circle_stim.draw()
        if ('d' in resp) or ('k' in resp):
            state = 'response'
            state_clock.reset()

    if state == 'response':
        if state_clock.getTime() > t_fb_delay:
            state = 'feedback'
            fb_acc = 'correct'
            state_clock.reset()

    if state == 'feedback':

        if fb_acc == 'correct':
            fb_stim_correct.draw()

        elif fb_acc == 'incorrect':
            fb_stim_incorrect.draw()

        if state_clock.getTime() > t_fb_dur:
            state = 'iti'
            state_clock.reset()

    if state == 'iti':
        if state_clock.getTime() > t_iti:
            state = 'stim'
            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        win.close()
        core.quit()

    win.flip()