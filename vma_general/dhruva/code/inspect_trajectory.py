import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

d_move = pd.read_csv('../data/data_movements_0.csv')
d_move = d.sort_values(['sample', 'trial'])
d_move = d[d['state'] == 'reach']

d_trial = pd.read_csv('../data/data_trials_0.csv')

fig, ax = plt.subplots(1, 1, squeeze=False)
sns.scatterplot(data=d, x='x', y='y')
plt.show()
