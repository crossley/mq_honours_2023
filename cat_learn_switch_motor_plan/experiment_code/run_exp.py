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

sub_num = 1

# allocate window and graphics
win = visual.Window(size=(800, 800),
                    pos=(50, 50),
                    fullscr=False,
                    screen=0,
                    allowGUI=False,
                    allowStencil=False,
                    monitor='testMonitor',
                    color='black',
                    colorSpace='rgb',
                    blendMode='avg',
                    useFBO=False,
                    units='cm')

# TODO
# Add text messages and logic to display them
# e.g., begin exp, end exp, between blocks, too slow, one key at a time, etc

# stimuli
sub_task_stim = visual.Rect(win, width=15, height=15, fillColor='gray', ori=0)
grating_stim = visual.GratingStim(win,
                                  size=8,
                                  mask='circle',
                                  colorSpace='rgb',
                                  texRes=512)
fb_stim_correct = visual.Circle(win,
                                radius=5,
                                fillColor=None,
                                lineColor='green',
                                lineWidth=8)
fb_stim_incorrect = visual.Circle(win,
                                  radius=5,
                                  fillColor=None,
                                  lineColor='red',
                                  lineWidth=8)

mouse = event.Mouse(visible=False, win=win)

# initial state
state = 'stim'

# state durations
t_iti = 1.5
t_fb_delay = 0.0
t_fb_dur = 0.75

fb_acc = 'NA'

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

config = pd.read_csv('../config/config_cat_learn' + str(sub_num) + '.csv')

x = config['x'].to_numpy()
y = config['y'].to_numpy()
xt = config['xt'].to_numpy()
yt = config['yt'].to_numpy()
cat = config['cat'].to_numpy()
sub_task = config['sub_task'].to_numpy()
condition = config['condition'].to_numpy()
trial = config['trial'].to_numpy()

num_trials = config.shape[0]
current_trial = 0

if np.unique(condition).shape[0] > 1:
    print('Error in condition assignment 1')
    win.close()
    core.quit()
else:
    if np.unique(condition) == 'two_finger_two_key':
        resp_keys = ['d', 'k', 'escape']
    elif np.unique(condition) == 'two_finger_four_key':
        resp_keys = ['s', 'd', 'k', 'l', 'escape']
    elif np.unique(condition) == 'four_finger_two_key':
        resp_keys = ['d', 'k', 'escape']
    elif np.unique(condition) == 'four_finger_four_key':
        resp_keys = ['s', 'd', 'k', 'l', 'escape']
    else:
        print('Error in condition assignment 2')
        win.close()
        core.quit()

trial_record = {
    'condition': [],
    'trial': [],
    'sub_task': [],
    'x': [],
    'y': [],
    'xt': [],
    'yt': [],
    'cat': [],
    'resp': [],
    'rt': []
}

while current_trial < num_trials:

    resp = event.getKeys(keyList=resp_keys)
    mouse_position = mouse.getPos()

    if sub_task[current_trial] == 1:
        sub_task_stim.ori = 45
    elif sub_task[current_trial] == 2:
        sub_task_stim.ori = 0

    if state == 'stim':
        sub_task_stim.draw()
        grating_stim.sf = xt[current_trial]
        grating_stim.ori = yt[current_trial]
        grating_stim.draw()
        if len(resp) > 0:
            if len(resp) > 1:
                # TODO: This should transition to a new state and then
                # transitition back without incrementing to the next trial
                # TODO: The new state should draw this message instead of
                # merely printing to the console
                print('please press only one key per trial')
            else:
                if (resp[0] in resp_keys):
                    state = 'response'
                    state_clock.reset()

    if state == 'response':
        sub_task_stim.draw()
        if state_clock.getTime() > t_fb_delay:
            state = 'feedback'
            # NOTE: The purpose of the -1 in the following line of code is to
            # convert cat[current_trial] from (1, 2) into (0, 1) so that it can
            # be used as an appropriate index into resp_keys.
            if resp[0] == resp_keys[cat[current_trial] - 1]:
                fb_acc = 'correct'
            else:
                fb_acc = 'incorrect'
            key_pressed = resp[0]
            rt = state_clock.getTime()
            state_clock.reset()

    if state == 'feedback':
        sub_task_stim.draw()
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

            trial_record['condition'].append(condition[current_trial])
            trial_record['trial'].append(trial[current_trial])
            trial_record['sub_task'].append(sub_task[current_trial])
            trial_record['x'].append(x[current_trial])
            trial_record['y'].append(y[current_trial])
            trial_record['xt'].append(xt[current_trial])
            trial_record['yt'].append(yt[current_trial])
            trial_record['cat'].append(cat[current_trial])
            trial_record['resp'].append(key_pressed)
            trial_record['rt'].append(rt)

            state = 'stim'
            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        pd.DataFrame(trial_record).to_csv('../data/cat_results.csv',
                                          index=False)
        win.close()
        core.quit()

    win.flip()

pd.DataFrame(trial_record).to_csv('cat_results' + str(sub_num) + '.csv')

win.close()
core.quit()
