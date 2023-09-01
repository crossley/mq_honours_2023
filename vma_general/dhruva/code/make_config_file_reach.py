import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

target_angle = 90
n_targets = 1

n_fam = 0
n_base = 20
n_clamp = 0
n_adaptation = 180
n_wash = 100

rot_amp = 1

n_uncertainty_condition = 45

# create necessary arrays  
cursor_vis = np.concatenate(
    (np.zeros(n_fam * n_targets), np.ones(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

midpoint_vis = np.concatenate(
    (np.zeros(n_fam * n_targets), np.ones(n_base * n_targets),
     np.ones(n_clamp * n_targets), np.ones(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

endpoint_vis = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

cursor_sig = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

cursor_mp_sig = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.ones(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

cursor_ep_sig = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

clamp = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     np.zeros(n_clamp * n_targets), np.zeros(n_adaptation * n_targets),
     np.zeros(n_wash * n_targets)))

rot = np.concatenate(
    (np.zeros(n_fam * n_targets), np.zeros(n_base * n_targets),
     rot_amp * np.zeros(n_clamp * n_targets),
     rot_amp * (np.random.normal(12, 4, 180)), np.zeros(n_wash * n_targets)))
     
# Create adaptation phase uncertainty condition arrays and randomise 
no_uncertainty = np.concatenate(
(np.ones(n_uncertainty_condition), np.zeros(n_adaptation - n_uncertainty_condition)))

low_uncertainty = np.concatenate(
    (np.zeros(n_uncertainty_condition),
    np.ones(n_uncertainty_condition), 
    np.zeros(n_adaptation - (n_uncertainty_condition * 2))))

high_uncertainty = np.concatenate(
    (np.zeros(n_uncertainty_condition * 2),
    np.ones(n_uncertainty_condition), 
    np.zeros(n_adaptation - (n_uncertainty_condition * 3))))

unlimited_uncertainty = np.concatenate(
    (np.zeros(n_uncertainty_condition * 3),
    np.ones(n_uncertainty_condition), 
    np.zeros(0))) # added to have the ensure same shape 

# create 2D array
uncertainty_conditions = np.vstack((no_uncertainty, low_uncertainty, high_uncertainty, unlimited_uncertainty))

#group and shuffle rows
num_groups = uncertainty_conditions.shape[1]
group_indices = np.arange(num_groups)
np.random.seed(1)  # For reproducibility
np.random.shuffle(group_indices)

shuffled_combined_array = uncertainty_conditions[:, group_indices]

# seperate into seperate arrays again
no_uncert, low_uncert,  high_uncert, unlimited_uncert = np.split(shuffled_combined_array.flatten(), 4)

# add baseline and washout zeros 
no_uncertainty = np.concatenate((np.zeros(n_base), no_uncert, np.zeros(n_wash)))
low_uncertainty = np.concatenate((np.zeros(n_base), low_uncert, np.zeros(n_wash)))
high_uncertainty = np.concatenate((np.zeros(n_base), high_uncert, np.zeros(n_wash)))
unlimited_uncertainty = np.concatenate((np.zeros(n_base), unlimited_uncert, np.zeros(n_wash)))

d = pd.DataFrame({
    'cursor_vis': cursor_vis,
    'midpoint_vis': midpoint_vis,
    'endpoint_vis': endpoint_vis,
    'cursor_sig': cursor_sig,
    'cursor_mp_sig': cursor_mp_sig,
    'cursor_ep_sig': cursor_ep_sig,
    'clamp': clamp,
    'rot': rot, 
    'no_uncertainty': no_uncertainty,
    'low_uncertainty': low_uncertainty,
    'high_uncertainty': high_uncertainty, 
    'unlimited_uncertainty': unlimited_uncertainty
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

#lookup_df = pd.read_excel('../condition_assignment.xls')

for sub in range(20):
#     if sub == 0:
#         d.to_csv('../config/config_reach_' + str(sub) + '.csv', index=False)
#     else:
#         condition = lookup_df.iloc[sub - 1].experimentalCondition
#         d['experimental_condition'] = condition
        d.to_csv('../config/config_reach_' + str(sub) + '.csv', index=False)

