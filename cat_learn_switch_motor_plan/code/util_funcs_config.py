from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
from psychopy.tools.monitorunittools import pix2cm
from psychopy.monitors import Monitor
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import mahalanobis
import os
import sys
import csv


def gen_II_cats(n):

    meanA = [43, 57]
    meanB = [57, 43]

    varx = 100
    vary = 100
    cov = 90

    cm = np.array([[varx, cov], [cov, vary]])

    xyA = multivariate_normal_m_dist(meanA, cm, n // 2, 2.5)
    xyB = multivariate_normal_m_dist(meanB, cm, n // 2, 2.5)

    xA = xyA[:, 0]
    yA = xyA[:, 1]
    xB = xyB[:, 0]
    yB = xyB[:, 1]

    x = np.concatenate((xA, xB))
    y = np.concatenate((yA, yB))

    cat = np.concatenate((1 * np.ones(xA.shape[0]), 2 * np.ones(xB.shape[0])))
    cat = cat.astype('int')

    xAt, yAt = TransformStim(xA, yA)
    xBt, yBt = TransformStim(xB, yB)
    xt, yt = TransformStim(x, y)

    # fig, ax = plt.subplots(1, 2, squeeze=False)
    # ax[0, 0].plot(xA, yA, 'x')
    # ax[0, 0].plot(xB, yB, 'x')
    # ax[0, 1].plot(xAt, yAt, 'x')
    # ax[0, 1].plot(xBt, yBt, 'x')
    # plt.show()

    # plot_category_exemplars_2(cat, xt, yt, x, y)

    return pd.DataFrame({'x': x, 'y': y, 'xt': xt, 'yt': yt, 'cat': cat})


def multivariate_normal_m_dist(mean, cov_mat, n, m_dist_max):
    # NOTE: initialise success markers
    success = False

    # NOTE: draw initial random sample
    xy = np.random.multivariate_normal(mean, cov_mat, n)

    stop = False
    while not success:
        # NOTE: transform sample statistics to match population parameters
        cov_mat_samp = np.cov(xy.T)
        cholesky_sample = np.linalg.cholesky(cov_mat_samp)
        cholesky_sample_inverse = np.linalg.inv(cholesky_sample)
        cholesky_population = np.linalg.cholesky(cov_mat)
        for i in range(n):
            xy[i] = np.matmul(
                np.matmul(cholesky_sample_inverse, cholesky_population),
                (xy[i, :] - np.mean(xy, axis=0))) + mean

        # NOTE: remove outliers
        for i in range(n):
            m_dist = mahalanobis(xy[i, :], mean, np.linalg.inv(cov_mat))
            while m_dist > m_dist_max:
                xy[i, :] = np.random.multivariate_normal(mean, cov_mat, 1)
                m_dist = mahalanobis(xy[i, :], mean, np.linalg.inv(cov_mat))
            outliers_removed = True

        tol = 10.0
        sample_mean = np.mean(xy, axis=0)
        sample_cov_mat = np.all(np.cov(xy.T))
        if np.all(sample_mean - mean < tol) and np.all(sample_cov_mat -
                                                       cov_mat < tol):
            success = True

    return (xy)


def TransformStim(xin, yin):

    #initialize variable, transfer labels
    trans_y = np.zeros(np.shape(xin)[0])

    # Convert x values; as long as input's x-values are in 0-100 space, this
    # line linearly transforms those values to -1:2 space; to choose
    # a different range, simply change the linear scaling, but be sure to
    # change the scaling for the y transformation as well so the ratio of the
    # axes remains the same.
    trans_x = xin / 100 * 3 - 1
    # trans_x = (xin / 100 * 3 - 1) * 2

    # Nonlinear conversion of x values: trans_x exponentiated, resulting in a
    # range of .5-4 for CPD. DO NOT CHANGE.
    trans_x = 2**trans_x

    # Y values should also be in 0-100; negative values in particular cause
    # problems.
    if np.any(xin < 0) or np.any(yin < 0):
        print('Negative value for input!')

    # Linear conversion of y values to pi/11:(3*pi/8+pi/11) space. Again,
    # different ranges and bounds can be chosen at this step.
    # y = (yin / 100) * ((3 * np.pi / 8) + (np.pi / 11))
    y = (yin / 100) * (np.pi / 2 - np.pi / 16) + (np.pi / 16)

    # The remainder of the code performs the nonlinear transformation on the y
    # values, which remain in the same space, but warped. DO NOT CHANGE.
    ind = np.argsort(y)
    sort_y = y[ind]
    z = 4.7 * np.sin(sort_y)**2

    trans_y[0] = np.sqrt(sort_y[0]**2 + z[0]**2)

    for i in range(1, np.shape(sort_y)[0]):
        trans_y[i] = trans_y[i - 1] + np.sqrt(
            np.power(sort_y[i] - sort_y[i - 1], 2) +
            np.power(z[i] - z[i - 1], 2))

    range_trans_y = np.amax(trans_y) - np.amin(trans_y)
    range_sort_y = np.amax(sort_y) - np.amin(sort_y)

    trans_y = trans_y / range_trans_y * range_sort_y
    trans_y = trans_y - np.min(trans_y) + np.min(sort_y)
    trans_y = trans_y * 180 / np.pi

    xout = trans_x
    yout = np.zeros(np.shape(xin)[0])
    for i in range(0, len(ind)):
        yout[ind[i]] = trans_y[i]

    return ([xout, yout])


def plot_category_exemplars(cat, x, y):
    '''plot sine-wave gratings at x CPD and at y degrees orientation in
    stimulus space --- cat, x, and y should be lists of the same length.'''

    # NOTE: Screen coordinate system has origin in the middle of the screen with
    # positive numbers going right and negative number going left
    screen_size = 300

    x_max = np.max(x)
    y_max = np.max(y)

    x_min = np.min(x)
    y_min = np.min(y)

    # NOTE: convert stimulus coordinates into screen coordinates
    xp = ((x - np.min(x)) /
          np.max(x - np.min(x))) * (screen_size) - screen_size / 2.0
    yp = ((y - np.min(y)) /
          np.max(y - np.min(y))) * (screen_size) - screen_size / 2.0

    win = visual.Window(size=(screen_size + 150, screen_size + 150),
                        fullscr=False,
                        screen=0,
                        allowGUI=False,
                        allowStencil=False,
                        monitor='testMonitor',
                        color=[0, 0, 0],
                        colorSpace='rgb',
                        blendMode='avg',
                        useFBO=False)

    mon = Monitor('testMonitor')
    cm_per_pix = pix2cm(1, mon)

    n = len(x)
    stim = []
    for i in range(n):
        grating = visual.GratingStim(win,
                                     units='pix',
                                     mask='circle',
                                     sf=x[i] * cm_per_pix,
                                     ori=y[i],
                                     pos=(xp[i], yp[i]),
                                     size=(50, 50))

        stim.append(grating)

    [i.draw() for i in stim]
    win.flip()

    event.waitKeys(keyList=['escape'])


def plot_category_exemplars_2(cat, x, y, xpos, ypos):
    '''plot sine-wave gratings at x CPD and at y degrees orientation in
    stimulus space --- cat, x, and y should be lists of the same length.'''

    # NOTE: Screen coordinate system has origin in the middle of the screen with
    # positive numbers going right and negative number going left
    screen_size = 600

    x_max = np.max(xpos)
    y_max = np.max(ypos)

    x_min = np.min(xpos)
    y_min = np.min(ypos)

    # NOTE: convert stimulus coordinates into screen coordinates
    xp = ((xpos - np.min(xpos)) /
          np.max(xpos - np.min(xpos))) * (screen_size) - screen_size / 2.0
    yp = -((ypos - np.min(ypos)) / np.max(ypos - np.min(ypos))) * (
        screen_size) - screen_size / 2.0

    win = visual.Window(pos=(50, 50),
                        size=(screen_size + 150, screen_size + 150),
                        fullscr=False,
                        screen=0,
                        allowGUI=False,
                        allowStencil=False,
                        monitor='testMonitor',
                        color=[0, 0, 0],
                        colorSpace='rgb',
                        blendMode='avg',
                        useFBO=False)

    # win.viewPos = [0, 0]
    # print(win.viewPos)

    mon = Monitor('testMonitor')
    mon.setWidth(29.0)
    mon.setSizePix((1440, 900))
    cm_per_pix = pix2cm(1, mon)

    n = len(x)
    stim = []
    for i in range(n):
        grating = visual.GratingStim(
            win,
            units='pix',
            mask='circle',
            sf=x[i] * cm_per_pix,
            ori=y[i],
            # pos=(xp[i], yp[i] + screen_size),
            pos=(xp[i], -(yp[i] + screen_size)),
            size=(2 / cm_per_pix, 2 / cm_per_pix))

        stim.append(grating)

    [i.draw() for i in stim]
    win.flip()

    event.waitKeys(keyList=['escape'])


def save_stim(x, y, fb, sub_task, name):
    screen_size = 300

    win = visual.Window(size=(screen_size, screen_size),
                        fullscr=False,
                        screen=0,
                        allowGUI=False,
                        allowStencil=False,
                        monitor='testMonitor',
                        color='black',
                        colorSpace='rgb',
                        blendMode='avg',
                        useFBO=False)

    mon = Monitor('testMonitor')
    mon.setWidth(29.0)
    mon.setSizePix((1440, 900))
    cm_per_pix = pix2cm(1, mon)
    # cm_per_pix = 0.01

    cont = 1.0

    grating = visual.GratingStim(win,
                                 units='pix',
                                 mask='circle',
                                 sf=x * cm_per_pix,
                                 ori=y,
                                 pos=(0, 0),
                                 contrast=cont,
                                 size=(2 / cm_per_pix, 2 / cm_per_pix),
                                 interpolate=True,
                                 texRes=2048)

    fb_stim_correct = visual.Circle(win,
                                    units='pix',
                                    pos=(0, 0),
                                    radius=(1.1 / cm_per_pix,
                                            1.1 / cm_per_pix),
                                    fillColor=None,
                                    lineColor='green',
                                    lineWidth=8,
                                    interpolate=True)

    fb_stim_incorrect = visual.Circle(win,
                                      units='pix',
                                      pos=(0, 0),
                                      radius=(1.1 / cm_per_pix,
                                              1.1 / cm_per_pix),
                                      fillColor=None,
                                      lineColor='red',
                                      lineWidth=8,
                                      interpolate=True)

    sub_task_stim_1 = visual.Rect(win,
                                  units='pix',
                                  width=3 / cm_per_pix,
                                  height=3 / cm_per_pix,
                                  fillColor='gray',
                                  ori=0)
    sub_task_stim_2 = visual.Rect(win,
                                  units='pix',
                                  width=3 / cm_per_pix,
                                  height=3 / cm_per_pix,
                                  fillColor='gray',
                                  ori=45)

    if sub_task == 1:
        sub_task_stim_1.draw()
    elif sub_task == 2:
        sub_task_stim_2.draw()

    grating.draw()
    if fb == 'correct':
        fb_stim_correct.draw()
    elif fb == 'incorrect':
        fb_stim_incorrect.draw()

    win.flip()
    win.getMovieFrame()
    win.saveMovieFrames(name)


def save_instruction_stim():

    x = np.linspace(10, 90, 5)
    y = np.linspace(10, 90, 5)

    xt, yt = TransformStim(x, y)

    for i in range(x.shape[0]):
        for j in range(y.shape[0]):

            save_stim(
                xt[i], yt[j], 'correct', 1,
                '../example_stim/example_stim_correct_' + str(round(i, 3)) +
                '_' + str(round(j, 2)) + '.png')

            save_stim(
                xt[i], yt[j], 'incorrect', 1,
                '../example_stim/example_stim_incorrect_' + str(round(i, 2)) +
                '_' + str(round(j, 2)) + '.png')

            save_stim(
                xt[i], yt[j], None, 1, '../example_stim/example_stim_none_' +
                str(round(i, 2)) + '_' + str(round(j, 2)) + '.png')
