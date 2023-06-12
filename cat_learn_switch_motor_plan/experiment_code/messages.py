from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
import datetime
import numpy as np
import pandas as pd
import os
import sys

# allocate window and graphics
win = visual.Window(
#    size=(1920, 1080),
    fullscr=True,
#    size=(1200, 800),
#    fullscr=False,
    screen=0,
    allowGUI=False,
    allowStencil=False,
    monitor='testMonitor',
    color=[0, 0, 0],
    colorSpace='rgb',
    blendMode='avg',
    useFBO=False,
)

h = 0.07

text_correct = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Correct!',
    font='Arial',
    pos=(0, 0),
    height=h,
    wrapWidth=None,
    color='green',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_incorrect = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Incorrect',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='red',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_between_blocks = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Nice work! Press any key to continue.',
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

text_faster = visual.TextStim(
    win=win,
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

text_outro = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='You\'re finished! Thanks for being awesome.',
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

text_problem_solved = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text=
    'You solved the problem! Press any key to proceed to the next problem.',
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

text_problem_failed = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text=
    'This problem seems tough. Lets try a different one. Press any key to proceed to the next problem.',
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
