from util_funcs_config import *

# save_instruction_stim()

# NOTE: RB CJ
# meanA = [25, 50]
# meanB = [35, 60]
# varx = 5
# vary = 100
# cov = 0
# cm = np.array([[varx, cov], [cov, vary]])

# meanA = [50, 25]
# meanB = [60, 35]
# varx = 150
# vary = 5
# cov = 0
# cm = np.array([[varx, cov], [cov, vary]])

# NOTE: II
meanA = [43, 57]
meanB = [57, 43]
varx = 100
vary = 100
cov = 90
cm = np.array([[varx, cov], [cov, vary]])

n_subs_per_cnd = 1
# conditions = ['two_finger_four_key', 'four_finger_four_key'] * n_subs_per_cnd
conditions = ['2F4K', '4F4K'] * n_subs_per_cnd
np.random.shuffle(conditions)

# n_trial_total = 560
n_trial_total = 6
n_trial_per_sub_task = n_trial_total // 2

block_size = 2

for sub in range(len(conditions)):

    d1 = gen_II_cats(n_trial_total)
    d1 = d1.sample(frac=1).reset_index(drop=True)

    stay = ['stay'] * (n_trial_total // 2)
    switch = ['switch'] * (n_trial_total // 2)
    trial_type = np.array(stay + switch)
    np.random.shuffle(trial_type)
    trial_type[0] = '0'

    sub_task = np.random.choice([1, 2], 2, False)
    dd = d1.copy().iloc[[0]]
    dd['trial_type'] = 'trial_zero'
    dd['sub_task'] = sub_task[0]
    d = [dd]
    for i in range(1, n_trial_total):
        if trial_type[i] == 'stay':
            dd = d1.iloc[[i]].copy()
            dd['trial_type'] = 'stay'
            dd['sub_task'] = d[i - 1]['sub_task'].to_numpy()[0]
            d.append(dd)
        if trial_type[i] == 'switch':
            dd = d1.iloc[[i]].copy()
            dd['trial_type'] = 'switch'
            dd['sub_task'] = np.abs(d[i - 1]['sub_task'].to_numpy()[0] - 3)
            d.append(dd)

    d = pd.concat(d)

    # TODO: how balanced did we get things?
    # We balance switch and stay trial counts but the subtask 1 vs 2 counts are
    # a bit out of balance. It's not obvious to me how to prevent this (or if
    # it can be prevented). Since it seems like a very minor detail I'll leave
    # it at this.
    print(d.groupby(['trial_type', 'sub_task']).count())

    d.loc[d['sub_task'] == 2,
          'cat'] = np.abs(d.loc[d['sub_task'] == 2, 'cat'] - 3)

    d['cat'] = d['cat'].astype('category')
    d['sub_task'] = d['sub_task'].astype('category')
    d['condition'] = conditions[sub]

    d['trial'] = np.arange(1, d.shape[0] + 1, 1)

    d['message'] = ['None'] * d.shape[0]

    d.loc[(0 + block_size)::block_size,
          'message'] = 'Nice work! Press any key to continue.'

    fig, ax = plt.subplots(2, 2, squeeze=False)

    xA = d.loc[(d['sub_task'] == 1) & (d['cat'] == 1), 'x']
    yA = d.loc[(d['sub_task'] == 1) & (d['cat'] == 1), 'y']
    xB = d.loc[(d['sub_task'] == 1) & (d['cat'] == 2), 'x']
    yB = d.loc[(d['sub_task'] == 1) & (d['cat'] == 2), 'y']
    ax[0, 0].scatter(xA, yA, marker='x', color='C0')
    ax[0, 0].scatter(xB, yB, marker='o', color='C1')

    xA = d.loc[(d['sub_task'] == 1) & (d['cat'] == 1), 'xt']
    yA = d.loc[(d['sub_task'] == 1) & (d['cat'] == 1), 'yt']
    xB = d.loc[(d['sub_task'] == 1) & (d['cat'] == 2), 'xt']
    yB = d.loc[(d['sub_task'] == 1) & (d['cat'] == 2), 'yt']
    ax[0, 1].scatter(xA, yA, marker='x', color='C0')
    ax[0, 1].scatter(xB, yB, marker='o', color='C1')

    xA = d.loc[(d['sub_task'] == 2) & (d['cat'] == 1), 'x']
    yA = d.loc[(d['sub_task'] == 2) & (d['cat'] == 1), 'y']
    xB = d.loc[(d['sub_task'] == 2) & (d['cat'] == 2), 'x']
    yB = d.loc[(d['sub_task'] == 2) & (d['cat'] == 2), 'y']
    ax[1, 0].scatter(xA, yA, marker='x', color='C0')
    ax[1, 0].scatter(xB, yB, marker='o', color='C1')

    xA = d.loc[(d['sub_task'] == 2) & (d['cat'] == 1), 'xt']
    yA = d.loc[(d['sub_task'] == 2) & (d['cat'] == 1), 'yt']
    xB = d.loc[(d['sub_task'] == 2) & (d['cat'] == 2), 'xt']
    yB = d.loc[(d['sub_task'] == 2) & (d['cat'] == 2), 'yt']
    ax[1, 1].scatter(xA, yA, marker='x', color='C0')
    ax[1, 1].scatter(xB, yB, marker='o', color='C1')

    plt.show()

    d.to_csv('../config/config_cat_learn_' + str(sub) + '.csv', index=False)
