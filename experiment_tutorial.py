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
grating_stim = visual.GratingStim(win, size=8, mask='circle')
fb_stim_correct = visual.Circle(win, radius=5, fillColor=None, lineColor='green', lineWidth=8)
fb_stim_incorrect = visual.Circle(win, radius=5, fillColor=None, lineColor='red', lineWidth=8)

mouse = event.Mouse(visible=False, win=win)

# initial state
state = 'stim'

# state durations
t_iti = 1.0
t_fb_delay = 0.0
t_fb_dur = 1.0

fb_acc = 'NA'

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

config = pd.read_csv('config_cat_learn.csv')

trial=config['trial'].to_numpy()
x=config['x'].to_numpy()
y=config['y'].to_numpy()
cat=config['cat'].to_numpy()

num_trials = config.shape[0]
current_trial = 1

resp_keys = ['d', 'k']

trial_record = {'trial': [], 'x': [], 'y': [], 'cat': [], 'resp':[], 'rt':[]}


while current_trial <= num_trials:

    resp = event.getKeys(keyList=['d', 'k', 'escape'])

    mouse_position = mouse.getPos()

    if state == 'stim':
        grating_stim.sf = x[current_trial] / 50
        grating_stim.ori = y[current_trial]
        grating_stim.draw()
        if ('d' in resp) or ('k' in resp):
            state = 'response'
            state_clock.reset()

    if state == 'response':
        if state_clock.getTime() > t_fb_delay:
            state = 'feedback'
            if resp[0] == resp_keys[cat[current_trial]-1]:
                fb_acc = 'correct'
            else:
                fb_acc = 'incorrect'
            key_pressed = resp[0]
            rt = state_clock.getTime()
            state_clock.reset()

    if state == 'feedback':
        grating_stim.draw()

        if fb_acc == 'correct':
            fb_stim_correct.draw()

        elif fb_acc == 'incorrect':
            fb_stim_incorrect.draw()

        if state_clock.getTime() > t_fb_dur:
            state = 'iti'
            state_clock.reset()

    if state == 'iti':
        if state_clock.getTime() > t_iti:
            
            trial_record['trial'].append(current_trial)
            trial_record['x'].append(x[current_trial])
            trial_record['y'].append(y[current_trial])
            trial_record['cat'].append(cat[current_trial])
            trial_record['resp'].append(key_pressed)
            trial_record['rt'].append(rt)
            
            state = 'stim'
            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        pd.DataFrame(trial_record).to_csv('cat_results.csv', index=False)
        win.close()
        core.quit()

    win.flip()

pd.DataFrame(trial_record).to_csv('cat_results.csv')

win.close()
core.quit()