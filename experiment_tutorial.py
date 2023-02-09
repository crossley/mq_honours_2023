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
win = visual.Window(
    size=(500, 500),
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
fb_stim = visual.Circle(win, radius=2, fillColor='red')

mouse = event.Mouse(visible=False, win=win)

state = 'stim_presentation'

timer = core.Clock()

while True:

    resp = event.getKeys()
    mouse_position = mouse.getPos()

    if state == 'stim_presentation':
        circle_stim.draw()
        if 'a' in resp:
            state = 'response_feedback'
            timer.reset()

    if state == 'response_feedback':
        fb_stim.draw()
        if timer.getTime() > 3:
           state = 'stim_presentation'

    if state == 'iti':
        pass

    if 'escape' in resp:
        win.close()
        core.quit()

    win.flip()
