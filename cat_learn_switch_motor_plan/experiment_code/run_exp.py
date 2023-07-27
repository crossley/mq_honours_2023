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
from instructions import *
from consent import *

sub_num = 0

# allocate window and graphics
win = visual.Window(size=(1200, 800),
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

# stimuli
sub_task_stim = visual.Rect(win, width=10, height=10, fillColor='gray', ori=0)

grating_stim = visual.GratingStim(win,
                                  size=5,
                                  mask='circle',
                                  colorSpace='rgb',
                                  texRes=512)

fb_stim_correct = visual.Circle(win,
                                radius=3,
                                fillColor=None,
                                lineColor='green',
                                lineWidth=8)

fb_stim_incorrect = visual.Circle(win,
                                  radius=3,
                                  fillColor=None,
                                  lineColor='red',
                                  lineWidth=8)

# messages
h = 1.5
one_key_per_trial_msg = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Please press only one key per trial',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='white',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

too_slow_msg = visual.TextStim(win=win,
                               ori=0,
                               name='text',
                               text='Please respond faster.',
                               font='Arial',
                               pos=(0.0),
                               height=h,
                               wrapWidth=None,
                               color='white',
                               colorSpace='rgb',
                               opacity=1,
                               bold=False,
                               alignHoriz='center',
                               alignVert='center')

config_msg = visual.TextStim(win=win,
                             ori=0,
                             name='text',
                             text='',
                             font='Arial',
                             pos=(0.0),
                             height=h,
                             wrapWidth=None,
                             color='white',
                             colorSpace='rgb',
                             opacity=1,
                             bold=False,
                             alignHoriz='center',
                             alignVert='center')

mouse = event.Mouse(visible=False, win=win)

fb_acc = 'NA'

config = pd.read_csv('../config/config_cat_learn_' + str(sub_num) + '.csv')

x = config['x'].to_numpy()
y = config['y'].to_numpy()
xt = config['xt'].to_numpy()
yt = config['yt'].to_numpy()
cat = config['cat'].to_numpy()
sub_task = config['sub_task'].to_numpy()
condition = config['condition'].to_numpy()
trial = config['trial'].to_numpy()
message = config['message'].to_numpy()

num_trials = config.shape[0]

if np.unique(condition).shape[0] > 1:
    print('Error in condition assignment 1')
    win.close()
    core.quit()

else:
    # NOTE: The order that these keys are listed matters (see state='response')
    if np.unique(condition)[0] == '2F2K':
        resp_keys = ['c', 'n', 'escape', 'space']
    elif np.unique(condition)[0] == '2F4K':
        resp_keys = ['c', 'n', 'v', 'b', 'escape', 'space']
    elif np.unique(condition)[0] == '4F2K':
        resp_keys = ['c', 'n', 'escape', 'space']
    elif np.unique(condition)[0] == '4F4K':
        resp_keys = ['c', 'n', 'v', 'b', 'escape', 'space']
    else:
        print('Error in condition assignment 2')
        win.close()
        core.quit()

# subtask cue img
if condition[0] == '4F4K':
    sub_task_1_img = visual.ImageStim(win,
                                      image='../img/4F4K/cue_1.png',
                                      pos=(0, 0),
                                      size=(5, 3))
    sub_task_2_img = visual.ImageStim(win,
                                      image='../img/4F4K/cue_2.png',
                                      pos=(0, 0),
                                      size=(5, 3))
elif condition[0] == '2F4K':
    sub_task_1_img = visual.ImageStim(win,
                                      image='../img/2F4K/cue_1.png',
                                      pos=(0, 0),
                                      size=(5, 3))
    sub_task_2_img = visual.ImageStim(win,
                                      image='../img/2F4K/cue_2.png',
                                      pos=(0, 0),
                                      size=(5, 3))

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

# state durations
t_iti = 0.75
t_fb_delay = 0.0
t_fb_dur = 1.0
t_too_slow = 5.0
t_one_key_per_trial_msg = 1.5
t_too_slow_msg = 1.5
t_subtask_cue = 0.75

# initial state
state = 'message'
current_trial = 0

# display instructions
give_instructions(win, np.unique(condition)[0])

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

while current_trial < num_trials:

    resp = event.getKeys(keyList=resp_keys)
    mouse_position = mouse.getPos()

    if sub_task[current_trial] == 1:
        sub_task_stim.ori = 45
    elif sub_task[current_trial] == 2:
        sub_task_stim.ori = 0

    if state == 'message':
        if message[current_trial] != 'None':
            config_msg.text = message[current_trial]
            config_msg.draw()
            if len(resp) > 0:
                if resp[0] == 'space':
                    state = 'stim'
                    state_clock.reset()
        else:
            state = 'subtask_cue'
            state_clock.reset()

    if state == 'subtask_cue':
        # sub_task_stim.draw()
        if sub_task[current_trial] == 1:
            sub_task_1_img.draw()
        elif sub_task[current_trial] == 2:
            sub_task_2_img.draw()
        if state_clock.getTime() > t_subtask_cue:
            state = 'stim'
            state_clock.reset()

    if state == 'stim':
        sub_task_stim.draw()
        grating_stim.sf = xt[current_trial]
        grating_stim.ori = yt[current_trial]
        grating_stim.draw()
        if sub_task[current_trial] == 1:
            resp_keys_sub_task = ['c', 'n']
        elif sub_task[current_trial] == 2:
            resp_keys_sub_task = ['v', 'b']
        if len(resp) > 0:
            if len(resp) > 1:
                state = 'one_key_per_trial'
                key_pressed = 'many'
                state_clock.reset()
            else:
                if resp[0] in resp_keys_sub_task:
                    state = 'response'
                    rt = state_clock.getTime()
                    key_pressed = resp[0]
                    state_clock.reset()
                    if rt > t_too_slow:
                        state = 'too_slow'
                        rt = t_too_slow
                        key_pressed = resp[0]
                        state_clock.reset()

    if state == 'response':
        sub_task_stim.draw()
        if state_clock.getTime() > t_fb_delay:
            state = 'feedback'
            # NOTE: The purpose of the -1 in the following line of code is to
            # convert cat[current_trial] from (1, 2) into (0, 1) so that it can
            # be used as an appropriate index into resp_keys.
            if sub_task[current_trial] == 1:
                if resp[0] == resp_keys[cat[current_trial] - 1]:
                    fb_acc = 'correct'
                else:
                    fb_acc = 'incorrect'
            elif sub_task[current_trial] == 2:
                # NOTE: The +2 in the following line comes from how resp_keys is
                # defined at the top of the experiment and is why the order of key
                # listings there matters.
                if resp[0] == resp_keys[cat[current_trial] - 1 + 2]:
                    fb_acc = 'correct'
                else:
                    fb_acc = 'incorrect'

            state_clock.reset()

    if state == 'one_key_per_trial':
        one_key_per_trial_msg.draw()
        if state_clock.getTime() > t_one_key_per_trial_msg:
            state = 'iti'
            current_trial = current_trial - 1  # do trial again
            state_clock.reset()

    if state == 'too_slow':
        too_slow_msg.draw()
        if state_clock.getTime() > t_too_slow_msg:
            state = 'iti'
            state_clock.reset()

    if state == 'feedback':
        sub_task_stim.draw()
        grating_stim.draw()

        #        if sub_task[current_trial] == 1:
        #            sub_task_1_img.draw()
        #        elif sub_task[current_trial] == 2:
        #            sub_task_2_img.draw()

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

            state = 'message'
            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        pd.DataFrame(trial_record).to_csv('../data/cat_results_' +
                                          str(sub_num) + '.csv',
                                          index=False)
        win.close()
        core.quit()

    win.flip()

print(trial_record)
pd.DataFrame(trial_record).to_csv('../data/cat_results_' + str(sub_num) +
                                  '.csv')

# give_debrief(win, np.unique(condition)[0])

win.close()
core.quit()
