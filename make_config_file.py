import numpy as np
import pandas as pd

n_trials = 5

trial = np.arange(1, n_trials + 1, 1)
stim_colour = ['red', 'blue', 'green', 'red', 'blue']

config = pd.DataFrame({'trial': trial, 'stim_colour': stim_colour})

config.to_csv('config.csv', index=False)
