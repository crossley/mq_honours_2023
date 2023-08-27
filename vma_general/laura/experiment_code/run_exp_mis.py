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
num_trials = 36
use_liberty = False


def set_up(use_liberty):

    if use_liberty:
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = 'COM1'

        print(ser)
        ser.open()

        # Checks serial port if open
        if (ser.is_open == False):
            print("Error! Serial port is not open")
            exit()

        # Send command to receive data through port
        ser.write(b'P')
        time.sleep(1)

        # Checks if Liberty is responding(e.g on)
        if (ser.inWaiting() < 1):
            print("Error! Check if liberty is on!")
            exit()

        # Set liberty output mode to binary
        ser.write(b'F1\r')
        time.sleep(1)

        # Set distance unit to centimeters
        ser.write(b'U1\r')
        time.sleep(0.1)

        # Set hemisphere to +Z
        ser.write(b'H1,0,0,1\r')
        time.sleep(0.1)

        # Set sample rate to 240hz
        ser.write(b'R4\r')
        time.sleep(0.1)

        # Reset frame count
        ser.write(b'Q1\r')
        time.sleep(0.1)

        # Set output to only include position (no orientation)
        ser.write(b'O1,3,9\r')
        time.sleep(0.1)
        ser.reset_input_buffer()

        # Obtain data
        ser.write(b'P')
        time.sleep(0.1)

        # Size of response
        recordsize = ser.inWaiting()
        ser.reset_input_buffer()
        averager = 4


def getPosition(ser, recordsize, averager):
    ser.reset_input_buffer()

    # Set variables
    # This defines the length of the binary header (bytes 0-7)
    header = 8
    # This defines the bytesize of IEEE floating point
    byte_size = 4

    # Obtain data
    ser.write(b'P')
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
        coord = struct.unpack('<f', coord)[0]

        positions.append(coord)

    return positions

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

cursor_circle = visual.Circle(win, radius=0.35, fillColor='white')

text_stim = visual.TextStim(win=win,
                            ori=0,
                            name='text',
                            text='',
                            font='Arial',
                            pos=(0, 8),
                            height=1,
                            wrapWidth=None,
                            color='white',
                            colorSpace='rgb',
                            opacity=1,
                            bold=False,
                            anchorHoriz='center',
                            anchorVert='center')

mouse = event.Mouse(visible=False, win=win)

experiment_clock = core.Clock()
state_clock = core.Clock()

current_trial = 0
current_sample = 0
state = 'init'

while current_trial < num_trials:

    resp = event.getKeys(keyList=['escape', 'space'])

    if use_liberty:
        c_position = getPosition(ser, recordsize, averager)
    else:
        c_position = mouse.getPos()

    x = c_position[0]
    y = c_position[1]
    z = c_position[2]

    text_stim.text = 'current trial: ' + str(
        current_trial) + '\ncurrent state: ' + str(state)
    text_stim.draw()

    #visually represent the x, y and z coordinates of the tool
    cursor_circle.pos = (x, y)
    cursor_circle.radius = (abs(z) - 10)
    cursor_circle.draw()

    if state == 'init':

        trial_move = {
            'trial': [],
            'state': [],
            'sample': [],
            'time': [],
            'x': [],
            'y': [],
            'z': []
        }

        if len(resp) > 0:
            if resp[0] == 'space':
                resp = []
                state = 'move'
                state_clock.reset()

    if state == 'move':

        if len(resp) > 0:
            if resp[0] == 'space':
                resp = []
                state = 'save'
                state_clock.reset()

    if state == 'save':
        state = 'init'
        f_move = '../data/data_movements_mis_' + str(sub_num) + '.csv'
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
    trial_move['z'].append(z)

    current_sample += 1
    win.flip()

    if 'escape' in resp:
        win.close()
        core.quit()

win.close()
core.quit()
