import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TODO: These numbers correspond to Laura... double them for Liam
# no_fb_baseline: 60 (5 trials for each of 12 targets)
# fb_baseline: 60 (5 trials for each of 12 targets)
# clamp: 120 trials (1 target direction)
# generalisation: 240 trials (10 trials to each of the 12 targets - half of each kind)
# no_fb_washout: 60 (5 trials for each of 12 targets)
# fb_washout: 60 (5 trials for each of 12 targets)

target_angle = np.arange(0, 180, 15)
n_targets = target_angle.shape[0]

n_baseline_no_fb = 2
n_baseline_continuous_fb = 2
n_baseline_endpoint_fb = 2
n_baseline_mixed_fb = 2
n_clamp = 10
n_generalisation = 3
n_washout_no_fb = 5
n_washout_fb = 5

rot_mean = 30
rot_sig = 1

instruct_phase = {
    'baseline_no_fb':
    'Please slice through the target as quickly and accurately as possible.\n'
    + 'You will not see the cursor during this phase.',
    'baseline_continuous_fb':
    'You will now only see the cursor throughout your entire reach.\n' +
    'Please continue to slice through the target as quickly and accurately as possible.',
    'baseline_endpoint_fb':
    'You will now only see the cursor only at the endpoint of your reach.\n' +
    'Please continue to slice through the target as quickly and accurately as possible.',
    'baseline_mixed_fb':
    'You will now only see the cursor at the endpoint of your reach on some trials.\n'
    + 'On the other trials you will not recieve feedback at all.\n'
    'Please continue to slice through the target as quickly and accurately as possible.',
    'clamp':
    'The cursor feedback is now clamped.\n' +
    'The location of the endpoint feedback is random.\n' +
    'It  has nothing to do with how accurately you reach.\n' +
    'Please do your best to ignore the cursor feedback and continue slicing directly through the target.',
    'generalisation':
    'You will now be asked to reach to targets that you have not yet reached to.\n'
    + 'You will not receive feedback of any kind for these reaches.' +
    'Please continue to slice through the target as quickly and accurately as possible.',
    'washout_no_fb':
    'You will not receive feedback of any kind for the following reaches.' +
    'Please continue to slice through the target as quickly and accurately as possible.',
    'washout_fb':
    'You will now only see the cursor throughout your entire reach.\n' +
    'Please continue to slice through the target as quickly and accurately as possible.',
}

# NOTE: The following places the instructions listed above only once at the
# beginning of each phase.
instruct_baseline_no_fb = [instruct_phase['baseline_no_fb']
                           ] + [''] * (n_baseline_no_fb * n_targets - 1)
instruct_baseline_continuous_fb = [
    instruct_phase['baseline_continuous_fb']
] + [''] * (n_baseline_continuous_fb * n_targets - 1)
instruct_baseline_endpoint_fb = [
    instruct_phase['baseline_endpoint_fb']
] + [''] * (n_baseline_endpoint_fb * n_targets - 1)
instruct_baseline_mixed_fb = [instruct_phase['baseline_mixed_fb']
                              ] + [''] * (n_baseline_mixed_fb * n_targets - 1)
instruct_clamp = [instruct_phase['clamp']] + [''] * (n_clamp * n_targets - 1)
instruct_generalisation = [instruct_phase['generalisation']
                           ] + [''] * (n_generalisation * n_targets - 1)
instruct_washout_no_fb = [instruct_phase['washout_no_fb']
                          ] + [''] * (n_washout_no_fb * n_targets - 1)
instruct_washout_fb = [instruct_phase['washout_fb']
                       ] + [''] * (n_washout_fb * n_targets - 1)

instruct_phase = np.concatenate(
    (instruct_baseline_no_fb, instruct_baseline_continuous_fb,
     instruct_baseline_endpoint_fb, instruct_baseline_mixed_fb, instruct_clamp,
     instruct_generalisation, instruct_washout_no_fb, instruct_washout_fb))

# NOTE: The experiment code also defines instructions that are displayed for
# every state. The following is an indicator column that should be used to
# switch them on or off.
instruct_state = np.ones(instruct_phase.shape)

cursor_vis = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     1 * np.ones(n_baseline_continuous_fb * n_targets),
     0 * np.ones(n_baseline_endpoint_fb * n_targets),
     0 * np.ones(n_baseline_mixed_fb * n_targets), 0 *
     np.ones(n_clamp * n_targets), 0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

midpoint_vis = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     0 * np.ones(n_baseline_continuous_fb * n_targets),
     0 * np.ones(n_baseline_endpoint_fb * n_targets),
     0 * np.ones(n_baseline_mixed_fb * n_targets), 0 *
     np.ones(n_clamp * n_targets), 0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

endpoint_vis = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     1 * np.ones(n_baseline_continuous_fb * n_targets),
     1 * np.ones(n_baseline_endpoint_fb * n_targets),
     np.random.permutation([0, 1] * (n_baseline_mixed_fb // 2) * n_targets),
     1 * np.ones(n_clamp * n_targets),
     0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

cursor_sig = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     0 * np.ones(n_baseline_continuous_fb * n_targets),
     0 * np.ones(n_baseline_endpoint_fb * n_targets),
     0 * np.ones(n_baseline_mixed_fb * n_targets), 0 *
     np.ones(n_clamp * n_targets), 0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

cursor_mp_sig = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     0 * np.ones(n_baseline_continuous_fb * n_targets),
     0 * np.ones(n_baseline_endpoint_fb * n_targets),
     0 * np.ones(n_baseline_mixed_fb * n_targets), 0 *
     np.ones(n_clamp * n_targets), 0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

cursor_ep_sig = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     0 * np.ones(n_baseline_continuous_fb * n_targets),
     0 * np.ones(n_baseline_endpoint_fb * n_targets),
     0 * np.ones(n_baseline_mixed_fb * n_targets), 0 *
     np.ones(n_clamp * n_targets), 0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

clamp = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     0 * np.ones(n_baseline_continuous_fb * n_targets),
     0 * np.ones(n_baseline_endpoint_fb * n_targets),
     0 * np.ones(n_baseline_mixed_fb * n_targets), 1 *
     np.ones(n_clamp * n_targets), 0 * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     0 * np.ones(n_washout_fb * n_targets)))

rot = np.concatenate(
    (0 * np.ones(n_baseline_no_fb * n_targets),
     np.random.normal(0, rot_sig, n_baseline_continuous_fb * n_targets),
     np.random.normal(0, rot_sig, n_baseline_endpoint_fb * n_targets),
     np.random.normal(0, rot_sig, n_baseline_mixed_fb * n_targets),
     np.random.normal(rot_mean, rot_sig, n_clamp * n_targets),
     rot_mean * np.ones(n_generalisation * n_targets),
     0 * np.ones(n_washout_no_fb * n_targets),
     np.random.normal(0, rot_sig, n_washout_fb * n_targets),
     ))

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

nn = [
    n_baseline_no_fb, n_baseline_continuous_fb, n_baseline_endpoint_fb,
    n_baseline_mixed_fb, n_clamp, n_generalisation, n_washout_no_fb,
    n_washout_fb
]
nn = [x * n_targets for x in nn]
labels = [
    'baseline_no_feedback', 'baseline_continuous_fb', 'baseline_endpoint_fb',
    'baseline_mixed_fb', 'clamp', 'generalisation', 'washout_no_fb',
    'washout_fb'
]
labels_x = np.concatenate(([0], np.cumsum(nn)[:-1]))
fig, ax = plt.subplots(1, 1, squeeze=False)
ax[0, 0].scatter(trial, rot, c=d['target_angle'])
ax[0, 0].vlines(labels_x, 0, rot_mean + 5, 'k', '--')
for i in range(len(labels)):
    ax[0, 0].text(labels_x[i], np.max(rot) + 5, labels[i], rotation=30)
ax[0, 0].set_ylabel('Rotation (degrees)')
ax[0, 0].set_xlabel('Trial')
plt.show()

# TODO: need to sort out how this all pans out with top ups etc

# n_subs_per_cnd = 1
# conditions = ['explicit_instruct'] * n_subs_per_cnd
# np.random.shuffle(conditions)

# for sub in range(len(conditions)):
#     d.to_csv('../config/config_reach_' + str(sub) + '.csv', index=False)
