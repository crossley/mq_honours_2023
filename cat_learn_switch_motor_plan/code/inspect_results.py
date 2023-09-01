from imports import *
from util_funcs_analysis import *

# dir_data = '../data/pilot_data/'
dir_data = "../data/data/"
d = load_data(dir_data)

# fig, ax = plt.subplots(1, 1, squeeze=False)
# sns.scatterplot(data=d, x="x", y="y", hue="cat")
# plt.show()

# dd = (
# d.groupby(["condition", "subject", "sub_task", "block"], group_keys=False)
# .mean()
# .reset_index()
# )
# print(dd)

d = d.groupby(["condition", "subject", "sub_task"], group_keys=False).apply(
    fit_func, "acc", tanh_func
)
d = d.sort_values(["condition", "subject", "sub_task"])
d.to_csv("../data_summary/data_summary.csv")

d = d.groupby(["condition", "subject"], group_keys=False).apply(compute_switch_cost)

inspect_interaction_switch_costs(d)
inspect_interaction_threeway(d)
inspect_learning_curves(d)

plt.close("all")

# inspect_interaction(dd, 'fit_a')
# inspect_interaction(dd, 'fit_b')
# inspect_interaction(dd, 'fit_c')
# inspect_interaction(dd, 'fit_ac')
# inspect_interaction(dd, 'switch_cost_acc')
# inspect_interaction(dd, 'switch_cost_rt')
# inspect_interaction(dd, 'switch_cost_acc_diff')
# inspect_interaction(dd, 'switch_cost_rt_diff')
# inspect_interaction(dd, 'switch_cost_acc_cue_diff')
# inspect_interaction(dd, 'switch_cost_rt_cue_diff')
