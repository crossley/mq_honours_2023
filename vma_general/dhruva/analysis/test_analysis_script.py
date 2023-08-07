import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

# participant number 
sub = 0 #test data

# import trial data csv 
trial_data = pd.read_csv('/Users/dhruvadave/mq_honours_2023_code/vma_general/dhruva/data/data_trials_' + str(sub) + '.csv')
# import config csv 
config_data = pd.read_csv('/Users/dhruvadave/mq_honours_2023_code/vma_general/dhruva/config/config_reach_' + str(sub) + '.csv') 

# combine datasets 
joined_data = pd.merge(trial_data, config_data, on = 'trial', how = 'left') 
#joined_data = pd.concat([trial_data, config_data], axis = 1)
'''better to just include uncertainty condition to data recorded during the exp.
Will save a lot of cleaning and/or redundant data being concatenated. 
Might also want to add back the duration it took to complete the trial and the total duration taken for the experiment back in as good to have data. 
Also considered recording the previous uncertainty condition during the experiment? Might be too messy and time consuming for the code to run :/'''

# create a new column for uncertainty condition on previous trial
'''1. want to loop through the 4 uncertainty condition rows for each trial 
2. and evaluate booleens then
3. plug them into the new column in the joined_data df. Want to make this a variable so it's easy to plug in. ''' 

previous_uncertainty = ['no_uncertainty'] * 21
columns_to_iterate = ['cursor_vis', 'no_uncertainty', 'low_uncertainty', 'high_uncertainty', 'unlimited_uncertainty']

# iterate through each row of the specified columns
for i in range(21, len(joined_data)):
    prev_row = joined_data.iloc[i - 1]
    if prev_row.no_uncertainty == True:
        previous_uncertainty.append('no_uncertainty')
    elif prev_row.low_uncertainty == True: 
        previous_uncertainty.append('low_uncertainty')
    elif prev_row.high_uncertainty == True: 
        previous_uncertainty.append('high_uncertainty')
    elif prev_row.unlimited_uncertainty == True: 
        previous_uncertainty.append('unlimited_uncertainty')
    else: 
        previous_uncertainty.append('unlimited_uncertainty')
         

# make previous_uncertainty a new column in the joined_data df
joined_data['previous_uncertainty'] = previous_uncertainty
joined_data.to_csv('joined_data.csv', index=False)

# plot 
sns.lineplot(data=joined_data, x='trial', y='endpoint_theta', hue = 'previous_uncertainty')
plt.show()