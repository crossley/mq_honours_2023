from imports import *
from util_funcs_analysis import *

block_size = 28

dir_data = '../data/pilot_data/'
d = []
for i, f in enumerate(os.listdir(dir_data)):
    if f.endswith('csv'):
        dd = pd.read_csv(dir_data + f)
        dd['subject'] = i
        d.append(dd)

d = pd.concat(d)

n_trials = d['trial'].max()
block_size = 20
n_blocks = n_trials // block_size
n_subs = d['subject'].unique().shape[0]

block = np.arange(0, n_blocks, 1)
block = np.repeat(block, block_size)
block = np.tile(block, n_subs)
d['block'] = block

d['acc'] = d['acc'] == 'correct'
d['sub_task'] = d['sub_task'].astype('category')
d['subject'] = d['subject'].astype('category')

fig, ax = plt.subplots(1, 1, squeeze=False)
sns.lineplot(data=d,
             x='block',
             y='acc',
             hue='sub_task',
             ax=ax[0, 0])
plt.show()
