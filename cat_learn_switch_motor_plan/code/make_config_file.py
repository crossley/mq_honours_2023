import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import distance
from util_funcs_config import *

# # NOTE: RB
# n = 100

# meanA = [25, 50]
# meanB = [35, 60]
# varx = 5
# vary = 100
# cov = 0
# cm = np.array([[varx, cov], [cov, vary]])
# xA1, yA1 = np.random.multivariate_normal(meanA, cm, n).T
# xB1, yB1 = np.random.multivariate_normal(meanB, cm, n).T

# meanA = [50, 25]
# meanB = [60, 35]
# varx = 150
# vary = 5
# cov = 0
# cm = np.array([[varx, cov], [cov, vary]])
# xA2, yA2 = np.random.multivariate_normal(meanA, cm, n).T
# xB2, yB2 = np.random.multivariate_normal(meanB, cm, n).T


def gen_II_cats(n):

    meanA = [43, 57]
    meanB = [57, 43]

    varx = 100
    vary = 100
    cov = 90

    cm = np.array([[varx, cov], [cov, vary]])

    xA, yA = np.random.multivariate_normal(meanA, cm, n).T
    xB, yB = np.random.multivariate_normal(meanB, cm, n).T

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


n_subs_per_cnd = 2
n_stim_per_cat = 100
conditions = ['fingers', 'buttons'] * n_subs_per_cnd
np.random.shuffle(conditions)

for sub in range(len(conditions)):

    d1 = gen_II_cats(n_stim_per_cat)
    d1['cue'] = 1

    d2 = d1.copy()
    d2['cue'] = 2
    d2['cat'] = np.abs(d2['cat'] - 3)

    d = pd.concat((d1, d2))
    d['cat'] = d['cat'].astype('category')
    d['cue'] = d['cue'].astype('category')
    d['condition'] = conditions[sub]

    d = d.sample(frac=1).reset_index(drop=True)
    d['trial'] = np.arange(1, d.shape[0] + 1, 1)

    # fig, ax = plt.subplots(2, 2, squeeze=False)

    # xA = d.loc[(d['cue'] == 1) & (d['cat'] == 1), 'x']
    # yA = d.loc[(d['cue'] == 1) & (d['cat'] == 1), 'y']
    # xB = d.loc[(d['cue'] == 1) & (d['cat'] == 2), 'x']
    # yB = d.loc[(d['cue'] == 1) & (d['cat'] == 2), 'y']
    # ax[0, 0].scatter(xA, yA, marker='x', color='C0')
    # ax[0, 0].scatter(xB, yB, marker='o', color='C1')

    # xA = d.loc[(d['cue'] == 1) & (d['cat'] == 1), 'xt']
    # yA = d.loc[(d['cue'] == 1) & (d['cat'] == 1), 'yt']
    # xB = d.loc[(d['cue'] == 1) & (d['cat'] == 2), 'xt']
    # yB = d.loc[(d['cue'] == 1) & (d['cat'] == 2), 'yt']
    # ax[0, 1].scatter(xA, yA, marker='x', color='C0')
    # ax[0, 1].scatter(xB, yB, marker='o', color='C1')

    # xA = d.loc[(d['cue'] == 2) & (d['cat'] == 1), 'x']
    # yA = d.loc[(d['cue'] == 2) & (d['cat'] == 1), 'y']
    # xB = d.loc[(d['cue'] == 2) & (d['cat'] == 2), 'x']
    # yB = d.loc[(d['cue'] == 2) & (d['cat'] == 2), 'y']
    # ax[1, 0].scatter(xA, yA, marker='x', color='C0')
    # ax[1, 0].scatter(xB, yB, marker='o', color='C1')

    # xA = d.loc[(d['cue'] == 2) & (d['cat'] == 1), 'xt']
    # yA = d.loc[(d['cue'] == 2) & (d['cat'] == 1), 'yt']
    # xB = d.loc[(d['cue'] == 2) & (d['cat'] == 2), 'xt']
    # yB = d.loc[(d['cue'] == 2) & (d['cat'] == 2), 'yt']
    # ax[1, 1].scatter(xA, yA, marker='x', color='C0')
    # ax[1, 1].scatter(xB, yB, marker='o', color='C1')

    # plt.show()

    d.to_csv('../config/config_cat_learn' + str(sub) + '.csv', index=False)
