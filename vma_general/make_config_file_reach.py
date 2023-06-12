import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

target_angle = np.arange(0, 180, 60)
n_targets = target_angle.shape[0]

# n_fam = 4
# n_base = 4
# n_clamp = 20
# n_general = 20
# n_wash = 20

n_fam = 1
n_base = 1
n_clamp = 1
n_general = 1
n_wash = 1

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

clamp = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.ones(n_clamp * n_targets), np.zeros(n_general * n_targets),
     np.zeros(n_wash * n_targets)))

rot_amp = 30
rot = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     rot_amp * np.ones(n_clamp * n_targets),
     rot_amp * np.ones(n_general * n_targets), np.zeros(n_wash * n_targets)))

d = pd.DataFrame({
    'cursor_vis': cursor_vis,
    'midpoint_vis': cursor_vis,
    'endpoint_vis': cursor_vis,
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

nn = [n_fam, n_base, n_clamp, n_general, n_wash]
nn = [x * n_targets for x in nn]
fig, ax = plt.subplots(1, 1, squeeze=False)
ax[0, 0].plot(rot, '.')
ax[0, 0].vlines(np.cumsum(nn), 0, rot_amp + 5, 'k', '--')
plt.show()

d.to_csv('config_reach.csv', index=False)
