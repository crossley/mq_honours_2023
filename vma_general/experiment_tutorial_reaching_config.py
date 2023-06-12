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

sub_num = 1

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
search_circle = visual.Circle(win,
                              radius=0.5,
                              lineColor='white',
                              fillColor='gray')
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

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()
midpoint_clock = core.Clock()

target_distance = 6
target_circle.pos = (0, target_distance)

config = pd.read_csv('config_reach_' + str(sub_num) + '.csv')

trial = config['trial'].to_numpy()
cycle = config['cycle'].to_numpy()
cursor_vis = config['cursor_vis'].to_numpy()
midpoint_vis = config['cursor_vis'].to_numpy()
endpoint_vis = config['cursor_vis'].to_numpy()
clamp = config['clamp'].to_numpy()
rot = config['rot'].to_numpy()
target_angle = config['target_angle'].to_numpy()

num_trials = config.shape[0]
current_trial = 0

trial_data = {
    'trial': [],
    'cycle': [],
    'cursor_vis': [],
    'midpoint_vis':[],
    'endpoint_vis': [],
    'clamp': [],
    'rot': [],
    'target_angle': [],
    'endpoint_theta': []
}

while current_trial < num_trials:

    resp = event.getKeys(keyList=['d', 'k', 'escape'])
    rt = state_clock.getTime()

    cursor_circle.pos = mouse.getPos()
    theta, r = coordinatetools.cart2pol(cursor_circle.pos[0],
                                        cursor_circle.pos[1])

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

        if mathtools.distance(start_circle.pos, cursor_circle.pos) >= target_distance:
            if clamp[current_trial] == True:
                feedback_circle.pos = coordinatetools.pol2cart(target_angle[current_trial] + rot[current_trial], target_distance)
            else:
                feedback_circle.pos = coordinatetools.pol2cart(theta + rot[current_trial], target_distance)
            endpoint_theta = coordinatetools.cart2pol(mouse.getPos()[0],mouse.getPos()[1])[0]
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

            trial_data['trial'].append(current_trial)
            trial_data['cycle'].append(cycle[current_trial])
            trial_data['cursor_vis'].append(cursor_vis[current_trial])
            trial_data['midpoint_vis'].append(cursor_vis[current_trial])
            trial_data['endpoint_vis'].append(cursor_vis[current_trial])
            trial_data['clamp'].append(clamp[current_trial])
            trial_data['rot'].append(rot[current_trial])
            trial_data['target_angle'].append(target_angle[current_trial])
            trial_data['endpoint_theta'].append(endpoint_theta)

            pd.DataFrame(trial_data).to_csv('./test_data_clamp.csv')

            current_trial += 1
            state_clock.reset()

    if 'escape' in resp:
        win.close()
        core.quit()
        pd.DataFrame(trial_data).to_csv('./test_data_clamp' + str(sub_num)' + '.csv')

    win.flip()

win.close()
core.quit()
