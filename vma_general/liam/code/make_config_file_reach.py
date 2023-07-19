import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

target_angle = np.arange(0, 180, 60)
n_targets = target_angle.shape[0]

n_fam = 4
n_base = 4
n_clamp = 20
n_general = 20
n_wash = 20

rot_amp = 30

instruct_phase = {
    'fam':
    'Please slice through the target as quickly and accurately as possible.',
    'base':
    'You will now only see your cursor at reach midpoint.\n' +
    'Please continue to slice through the target as quickly and accurately as possible.',
    'clamp':
    'The cursor feedback is now clamped.\n' + 'It will always appear ' +
    str(rot_amp) +
    ' degrees away from the target no matter how accurately you move.\n' +
    'Please do your best to ignore the cursor feedback and continue slicing directly through the target.',
    'rot':
    'Please slice directly through the target.' +
    'Do not aim off-target in order to get the cursor to land on the target.',
    'general':
    'You will now be asked to reach to targets that you have not yet reached to.\n'
    + 'You will not receive feedback of any kind for these reaches.' +
    'Please continue to slice through the target as quickly and accurately as possible.',
    'wash':
    'You will not receive feedback of any kind for the following reaches.' +
    'Please continue to slice through the target as quickly and accurately as possible.'
}

# NOTE: The following places the instructions listed above only once at the
# beginning of each phase.
instruct_fam = [instruct_phase['fam']] + [''] * (n_fam * n_targets - 1)
instruct_base = [instruct_phase['base']] + [''] * (n_base * n_targets - 1)
instruct_clamp = [instruct_phase['clamp']] + [''] * (n_clamp * n_targets - 1)
instruct_general = [instruct_phase['general']] + [''] * (n_general * n_targets - 1)
instruct_wash = [instruct_phase['wash']] + [''] * (n_wash * n_targets - 1)

instruct_phase = np.concatenate((instruct_fam, instruct_base, instruct_clamp,
                           instruct_general, instruct_wash))

# NOTE: The experiment code also defines instructions that are displayed for
# every state. The following is an indicator column that should be used to
# switch them on or off.
instruct_state = np.ones(instruct_phase.shape)

cursor_vis = np.concatenate(
    (np.zeros(n_fam * n_targets), np.ones(n_base * n_targets),
     np.ones(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

midpoint_vis = np.concatenate(
    (np.zeros(n_fam * n_targets), np.ones(n_base * n_targets),
     np.ones(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

endpoint_vis = np.concatenate(
    (np.zeros(n_fam * n_targets), np.ones(n_base * n_targets),
     np.ones(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

cursor_sig = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

cursor_mp_sig = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

cursor_ep_sig = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

clamp = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.ones(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

rot = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     rot_amp * np.ones(n_clamp * n_targets),
     rot_amp * np.ones(n_general * n_targets), np.zeros(n_wash * n_targets)))

d = pd.DataFrame({
    'cursor_vis': cursor_vis,
    'midpoint_vis': midpoint_vis,
    'endpoint_vis': endpoint_vis,
    'cursor_sig': cursor_sig,
    'cursor_mp_sig': cursor_mp_sig,
    'cursor_ep_sig': cursor_ep_sig,
    'clamp': clamp,
    'rot': rot
})

n_trials = d.shape[0]
n_cycles = n_trials // n_targets
cycle = np.arange(0, n_cycles, 1)
cycle = np.repeat(cycle, n_targets)
target_angle = np.tile(target_angle, n_cycles)

trial = np.arange(1, d.shape[0] + 1, 1)
d['trial'] = trial
d['cycle'] = cycle
d['target_angle'] = target_angle
d['target_angle'] = d.groupby(
    ['cycle'])['target_angle'].sample(frac=1).reset_index(drop=True)
d['instruct_phase'] = instruct_phase
d['instruct_state'] = instruct_state

nn = [n_fam, n_base, n_clamp, n_general, n_wash]
nn = [x * n_targets for x in nn]
labels = ['Familiarisation', 'Baseline', 'Clamp', 'Generalisation', 'Washout']
labels_x = np.concatenate(([0], np.cumsum(nn)[:-1]))
fig, ax = plt.subplots(1, 1, squeeze=False)
ax[0, 0].scatter(trial, rot, c=target_angle)
ax[0, 0].vlines(labels_x, 0, rot_amp + 5, 'k', '--')
for i in range(len(labels)):
    ax[0, 0].text(labels_x[i], np.max(rot) + 5, labels[i], rotation=30)
ax[0, 0].set_ylabel('Rotation (degrees)')
ax[0, 0].set_xlabel('Trial')
plt.show()

n_subs_per_cnd = 1
conditions = ['explicit_instruct'] * n_subs_per_cnd
np.random.shuffle(conditions)

for sub in range(len(conditions)):
    d.to_csv('../config/config_reach_' + str(sub) + '.csv', index=False)
