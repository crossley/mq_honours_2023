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

use_liberty = True

# This method grabs the position of the sensor
def getPosition(ser, recordsize, averager):
    ser.reset_input_buffer()

    # Set variables
    # This defines the length of the binary header (bytes 0-7)
    header = 8
    # This defines the bytesize of IEEE floating point
    byte_size = 4

    # Obtain data
    ser.write(b"P")
    # time.sleep(0.1)
    # print("inWaiting " + str(ser.inWaiting()))
    # print("recorded size " + str(recordsize))

    # Read header to remove it from the input buffer
    ser.read(header)

    positions = []

    # Read the three coordinates
    for x in range(3):
        # Read the coordinate
        coord = ser.read(byte_size)

        # Convert hex to floating point (little endian order)
        coord = struct.unpack("<f", coord)[0]

        positions.append(coord)

    return positions


if use_liberty:
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = "COM1"

    print(ser)
    ser.open()

    # Checks serial port if open
    if ser.is_open == False:
        print("Error! Serial port is not open")
        exit()

    # Send command to receive data through port
    ser.write(b"P")
    time.sleep(1)

    # Checks if Liberty is responding(e.g on)
    if ser.inWaiting() < 1:
        print("Error! Check if liberty is on!")
        exit()

    # Set liberty output mode to binary
    ser.write(b"F1\r")
    time.sleep(1)

    # Set distance unit to centimeters
    ser.write(b"U1\r")
    time.sleep(0.1)

    # Set hemisphere to +Z
    ser.write(b"H1,0,0,1\r")
    time.sleep(0.1)

    # Set sample rate to 240hz
    ser.write(b"R4\r")
    time.sleep(0.1)

    # Reset frame count
    ser.write(b"Q1\r")
    time.sleep(0.1)

    # Set output to only include position (no orientation)
    ser.write(b"O1,3,9\r")
    time.sleep(0.1)
    ser.reset_input_buffer()

    # Obtain data
    ser.write(b"P")
    time.sleep(0.1)

    # Size of response
    recordsize = ser.inWaiting()
    ser.reset_input_buffer()
    averager = 4

win = visual.Window(size=(700, 700),
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

search_circle = visual.Circle(win, radius=1,lineColor='white', fillColor=None, edges = 200)
start_circle = visual.Circle(win, radius=1, fillColor='blue', edges = 100)
target_circle = visual.Circle(win, radius=1, fillColor='blue', edges = 100)
feedback_circle = visual.Circle(win, radius=0.7, fillColor='white', edges = 100)
cursor_circle = visual.Circle(win, radius=0.7, fillColor='white', edges = 100)

text_stim = visual.TextStim(win=win,
                            ori=0,
                            name='text',
                            text='',
                            font='Arial',
                            pos=(0, 12),
                            height=1,
                            wrapWidth=None,
                            color='black',
                            colorSpace='rgb',
                            opacity=1,
                            bold=False,
                            anchorHoriz='center',
                            anchorVert='center')

mouse = event.Mouse(visible=False, win=win)

target_distance = 10
target_circle.pos = (0, target_distance)

config = pd.read_csv(r"C:\Users\laura\OneDrive\Desktop\mq_honours_2023-main\vma_general\laura\config\config_test_" + str(sub_num) + '.csv')

cursor_vis = config['cursor_vis']
endpoint_vis = config['endpoint_vis']
cycle = config['cycle_phase']
clamp = config['clamp']
rot = config['rot']
trial = config['trial']
target_angle = config['target_angle']
instruct_phase = config['instruct_phase']
instruct_state = config['instruct_state']

num_trials = config.shape[0]

state = 'trial_init'

t_instruct = 1.0
t_hold = 0.3
t_move_prep = 0.0  # TODO if we choose to use this then we need some go cue
t_iti = 0.3
t_feedback = 0.5
t_too_fast = 0.04
t_too_slow = 0.6

search_near_thresh = 0.25
search_ring_thresh = 1.0

current_trial = 0
current_sample = 0

experiment_clock = core.Clock()
state_clock = core.Clock()

while current_trial < num_trials:

    resp = event.getKeys(keyList=['escape'])
    rt = state_clock.getTime()

    x, y = mouse.getPos()
    theta, r = coordinatetools.cart2pol(x, y)

    cursor_circle.pos = (x, y)

    if state == 'trial_init':

        trial_data = {
            'cursor_vis': [],
            'endpoint_vis': [],
            'clamp': [],
            'rot': [],
            'trial': [],
            'cycle_phase': [],
            'target_angle': [],
            'instruct_phase': [],
            'instruct_state': [],
            'endpoint_theta': [],
            'movement_time': [],
            'movement_initiation_time': []
        }
      
        trial_move = {
            'trial': [],
            'state': [],
            'sample': [],
            'time': [],
            'x': [],
            'y': []
        }

        endpoint_theta = -1
        movement_time = -1
        movement_initiation_time = -1

        state = 'search_ring'

    if state == 'search_ring':
        if instruct_state[current_trial]:
            text_stim.text = 'Move your hand to make the diameter of the ring shrink'
            text_stim.draw()
        search_circle.radius = r
        search_circle.draw()
        if mathtools.distance(start_circle.pos,
                              cursor_circle.pos) < search_ring_thresh:
            state = 'search_near'
            state_clock.reset()

    if state == 'search_near':
        if instruct_state[current_trial]:
            text_stim.text = 'Move the cursor all the way inside the start circle'
            text_stim.draw()

        start_circle.draw()
        cursor_circle.draw()

        if mathtools.distance(start_circle.pos,
                              cursor_circle.pos) >= search_ring_thresh:
            state = 'search_ring'
            state_clock.reset()
        elif mathtools.distance(start_circle.pos,
                                cursor_circle.pos) < search_near_thresh:
            state = 'hold'
            state_clock.reset()

    if state == 'instruct':
        if instruct[current_trial] != 'NaN':
            text_stim.text = instruct[current_trial]
            text_stim.draw()

            if mathtools.distance(start_circle.pos,
                                  cursor_circle.pos) >= search_near_thresh:
                state = 'search_near'
                state_clock.reset()
            elif state_clock.getTime() >= t_instruct:
                state = 'hold'
                state_clock.reset()
        else:
            state = 'hold'
            state_clock.reset()

    if state == 'hold':
        if instruct_state[current_trial]:
            text_stim.text = 'Hold the cursor steady inside the start circle'
            text_stim.draw()

        start_circle.draw()
        cursor_circle.draw()
        if mathtools.distance(start_circle.pos, cursor_circle.pos) >= 0.25:
            state = 'search_near'
            state_clock.reset()
        elif state_clock.getTime() >= t_hold:
            state = 'move_prep'
            state_clock.reset()

        if state == 'move_prep':
        if instruct_state[current_trial] == True and clamp[current_trial]:
            text_stim.text = 'The cursor is now clamped. Ignore the cursor feedback and and continue slicing directly through the target.'
            text_stim.draw()

        elif instruct_state[current_trial]:
            text_stim.text = 'Slice through the target as quickly and accurately as possible'
            text_stim.draw()

        start_circle.draw()
        cursor_circle.draw()
        target_circle.pos = coordinatetools.pol2cart(
            target_angle[current_trial], target_distance)
        target_circle.draw()

        if state_clock.getTime() >= t_move_prep:
            if mathtools.distance(start_circle.pos,
                                  cursor_circle.pos) >= search_near_thresh:
                movement_initiation_time = state_clock.getTime()
                state = 'reach'
                state_clock.reset()
        else:
            if mathtools.distance(start_circle.pos,
                                  cursor_circle.pos) >= search_near_thresh:
                state = 'search_near'
                state_clock.reset()

    if state == 'reach':
        if instruct_state[current_trial]:
            text_stim.draw()

        target_circle.draw()
        start_circle.draw()
      
        if clamp[current_trial] == True:
            cursor_circle.pos = coordinatetools.pol2cart(
                target_angle[current_trial] + rot[current_trial], r)
        else:
            cursor_circle.pos = coordinatetools.pol2cart(
                theta + rot[current_trial], r)

        if cursor_vis[current_trial]:
            cursor_circle.draw()

        if mathtools.distance(start_circle.pos, (x, y)) >= target_distance:
            if clamp[current_trial] == True:
                feedback_circle.pos = coordinatetools.pol2cart(
                    target_angle[current_trial] + rot[current_trial],
                    target_distance)
            else:
                feedback_circle.pos = coordinatetools.pol2cart(
                    theta + rot[current_trial], target_distance)

            endpoint_theta = coordinatetools.cart2pol(mouse.getPos()[0],
                                                      mouse.getPos()[1])[0]
            movement_time = state_clock.getTime()
            state = 'feedback'
            state_clock.reset()

    if state == 'feedback':
        if movement_time > t_too_slow:
            text_stim.text = 'Please execute your movement more quickly'
            text_stim.draw()

        elif movement_time < t_too_fast:
            text_stim.text = 'Please execute your movement more slowly'
            text_stim.draw()

        else:
            start_circle.draw()
            target_circle.draw()

            if clamp[current_trial] == True and endpoint_vis[current_trial]:
                if instruct_state[current_trial]:
                    text_stim.text = 'The cursor feedback is does not show how accurate your reach was for this trial.'
                    text_stim.draw()
                feedback_circle.draw()
  
            elif endpoint_vis[current_trial]:
                if instruct_state[current_trial]:
                    text_stim.text = 'The on screen cursor shows you how accurate your reach was'
                    text_stim.draw()
                feedback_circle.draw()

            else:
                if instruct_state[current_trial]:
                    text_stim.text = 'This is a no-feedback trial '
                    text_stim.text += 'so you do not get to see how accurate your reach was.'

                text_stim.draw()

        if state_clock.getTime() > t_feedback:
            state = 'iti'
            state_clock.reset()

        if state_clock.getTime() > t_iti:
            state = 'trial_init'

            trial_data = {
                'cursor_vis': [cursor_vis[current_trial]],
                'endpoint_vis': [endpoint_vis[current_trial]],
                'clamp': [clamp[current_trial]],
                'rot': [rot[current_trial]],
                'trial': [trial[current_trial]],
                'cycle_phase': [cycle[current_trial]],
                'target_angle': [target_angle[current_trial]],
                'instruct_phase': [instruct_phase[current_trial]],
                'instruct_state': [instruct_state[current_trial]],
                'endpoint_theta': [endpoint_theta],
                'movement_time': [movement_time],
                'movement_initiation_time': [movement_initiation_time]
            }

            f_trial = '../data/data_trials_' + str(sub_num) + '.csv'
            pd.DataFrame(trial_data).to_csv(f_trial,
                                            header=not os.path.isfile(f_trial),
                                            mode='a')

            f_move = '../data/data_movements_' + str(sub_num) + '.csv'
            pd.DataFrame(trial_move).to_csv(f_move,
                                            header=not os.path.isfile(f_move),
                                            mode='a')

            current_trial += 1
            state_clock.reset()

    # trajectories recorded every sample
    trial_move['trial'].append(current_trial)
    trial_move['state'].append(state)
    trial_move['sample'].append(current_sample)
    trial_move['time'].append(experiment_clock.getTime())
    trial_move['x'].append(x)
    trial_move['y'].append(y)
    current_sample += 1
    win.flip()

    if 'escape' in resp:
        win.close()
        core.quit()

win.close()
core.quit()
