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

sub_num = 0

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

search_circle = visual.Circle(win,
                              radius=0.5,
                              lineColor='white',
                              fillColor='gray')
cursor_circle = visual.Circle(win, radius=0.4, fillColor='white')
start_circle = visual.Circle(win, radius=0.5, fillColor='blue')
target_circle = visual.Circle(win, radius=0.5, fillColor='blue')
feedback_circle = visual.Circle(win, radius=0.5, fillColor='white')

mouse = event.Mouse(visible=False, win=win)

state = 'search'

t_instruct = 5.0
t_hold = 1.0
t_iti = 1.0
t_feedback = 1.0

experiment_clock = core.Clock()
state_clock = core.Clock()

target_distance = 6
target_circle.pos = (0, target_distance)

config = pd.read_csv('../config/config_reach_' + str(sub_num) + '.csv')

cursor_vis = config['cursor_vis']
midpoint_vis = config['midpoint_vis']
endpoint_vis = config['endpoint_vis']
cursor_sig = config['cursor_sig']
cursor_mp_sig = config['cursor_mp_sig']
cursor_ep_sig = config['cursor_ep_sig']
clamp = config['clamp']
rot = config['rot']
trial = config['trial']
cycle = config['cycle']
target_angle = config['target_angle']
instruct = config['instruct']

num_trials = config.shape[0]

trial_data = {
    'cursor_vis': [],
    'midpoint_vis': [],
    'endpoint_vis': [],
    'cursor_sig': [],
    'cursor_mp_sig': [],
    'cursor_ep_sig': [],
    'clamp': [],
    'rot': [],
    'trial': [],
    'cycle': [],
    'target_angle': [],
    'instruct': [],
    'endpoint_theta': []
}

# TODO: record movement trajectories
trial_move = {
    'trial': [],
    'state': [],
    'sample': [],
    'time': [],
    'x': [],
    'y': []
}

# TODO: add instruct state
# TODO: I'm apparently using deprecated arguments here.
text_instruct = visual.TextStim(win=win,
                                ori=0,
                                name='text',
                                text='',
                                font='Arial',
                                pos=(0.0),
                                height=1,
                                wrapWidth=None,
                                color='white',
                                colorSpace='rgb',
                                opacity=1,
                                bold=False,
                                alignHoriz='center',
                                alignVert='center')

current_trial = 0
current_sample = 0
while current_trial < num_trials:

    resp = event.getKeys(keyList=['d', 'k', 'escape'])
    rt = state_clock.getTime()

    x, y = mouse.getPos()
    theta, r = coordinatetools.cart2pol(cursor_circle.pos[0],
                                        cursor_circle.pos[1])

    cursor_circle.pos = (x, y)

    if state == 'search':
        search_circle.radius = r
        search_circle.draw()

        if mathtools.distance(start_circle.pos, cursor_circle.pos) < 0.2:
            state = 'instruct'
            state_clock.reset()

    if state == 'instruct':
        print(instruct[current_trial])
        if instruct[current_trial] != 'NaN':
            text_instruct.text = instruct[current_trial]
            text_instruct.draw()
            if state_clock.getTime() >= t_instruct:
                state = 'hold'
                state_clock.reset()
        else:
            state = 'hold'
            state_clock.reset()

    # TODO: This advances out of the hold state after t_hold seconds. We
    # want the time constraint but we also only want to advance after a
    # reach has been initiated.
    if state == 'hold':
        start_circle.draw()
        cursor_circle.draw()
        if state_clock.getTime() >= t_hold:
            state = 'reach'
            state_clock.reset()
            target_circle.pos = coordinatetools.pol2cart(
                target_angle[current_trial], target_distance)

    if state == 'reach':
        if clamp[current_trial] == True:
            cursor_circle.pos = coordinatetools.pol2cart(
                target_angle[current_trial] + rot[current_trial], r)
        else:
            cursor_circle.pos = coordinatetools.pol2cart(
                theta + rot[current_trial], r)

        start_circle.draw()
        target_circle.draw()

        if cursor_vis[current_trial]:
            cursor_circle.draw()

        if midpoint_vis[current_trial]:
            if r > target_distance * 0.9 / 2 and r < target_distance * 1.1 / 2:
                cursor_circle.draw()

        if mathtools.distance(start_circle.pos,
                              cursor_circle.pos) >= target_distance:
            if clamp[current_trial] == True:
                feedback_circle.pos = coordinatetools.pol2cart(
                    target_angle[current_trial] + rot[current_trial],
                    target_distance)
            else:
                feedback_circle.pos = coordinatetools.pol2cart(
                    theta + rot[current_trial], target_distance)
            endpoint_theta = coordinatetools.cart2pol(mouse.getPos()[0],
                                                      mouse.getPos()[1])[0]
            state = 'feedback'
            state_clock.reset()

    if state == 'feedback':
        start_circle.draw()
        target_circle.draw()
        if endpoint_vis[current_trial]:
            feedback_circle.draw()
        if state_clock.getTime() > t_feedback:
            state = 'iti'
            state_clock.reset()

    if state == 'iti':
        if state_clock.getTime() > t_iti:
            state = 'search'

            trial_data['cursor_vis'].append(cursor_vis[current_trial])
            trial_data['midpoint_vis'].append(midpoint_vis[current_trial])
            trial_data['endpoint_vis'].append(endpoint_vis[current_trial])
            trial_data['cursor_sig'].append(cursor_sig[current_trial])
            trial_data['cursor_mp_sig'].append(cursor_mp_sig[current_trial])
            trial_data['cursor_ep_sig'].append(cursor_ep_sig[current_trial])
            trial_data['clamp'].append(clamp[current_trial])
            trial_data['rot'].append(rot[current_trial])
            trial_data['trial'].append(trial[current_trial])
            trial_data['cycle'].append(cycle[current_trial])
            trial_data['target_angle'].append(target_angle[current_trial])
            trial_data['instruct'].append(instruct[current_trial])
            trial_data['endpoint_theta'].append(endpoint_theta)

            pd.DataFrame(trial_data).to_csv('../data/data_' + str(sub_num) +
                                            '.csv')

            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        win.close()
        core.quit()
        pd.DataFrame(trial_data).to_csv('../data/data_' + str(sub_num) +
                                        '.csv')

    # trajectories recorded every sample
#    trial_move['trial'] = current_trial
#    trial_move['state'] = state
#    trial_move['sample'] = current_sample
#    trial_move['time'] = experiment_clock.getTime()
#    trial_move['x'] = x
#    trial_move['y'] = y
    current_sample += 1
    win.flip()

win.close()
core.quit()
