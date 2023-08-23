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
d.to_csv("../data_summary/data_summary.csv")

inspect_interaction_threeway(d)
inspect_learning_curves(d)
