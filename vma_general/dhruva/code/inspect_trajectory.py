import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

d_move = pd.read_csv("../data/data_movements_demo.csv")
d_move = d_move[d_move["state"] == "reach"]

fig, ax = plt.subplots(2, 4, squeeze=False)
ax = ax.flatten()
for i in d.trial.unique():
    print(d[d["trial"] == i].shape)
    sns.scatterplot(
        data=d[d["trial"] == i], x="x", y="y", hue="time", ax=ax[i], legend=False
    )
plt.show()

d_move = pd.read_csv("../data/data_movements_demo.csv")
d = d_move

d = d_move
d["trial"] = d["trial"].astype("category")
fig, ax = plt.subplots(1, 1, squeeze=False)
sns.scatterplot(data=d, x="time", y="state", hue="trial")
plt.show()


# d_config = pd.read_csv("../config/config_reach_0.csv")
# d_config = d_config[
#     [
#         "trial",
#         "no_uncertainty",
#         "low_uncertainty",
#         "high_uncertainty",
#         "unlimited_uncertainty",
#     ]
# ]

# d = pd.merge(d_move, d_config, on="trial")
# d = d.sort_values(["sample", "trial"])
# d = d[
#     [
#         "sample",
#         "time",
#         "x",
#         "y",
#         "trial",
#         "no_uncertainty",
#         "low_uncertainty",
#         "high_uncertainty",
#         "unlimited_uncertainty",
#     ]
# ]

# dd = pd.melt(
#     d,
#     id_vars=["sample", "time", "x", "y", "trial"],
#     var_name="sig_mp_ind",
#     value_name="sig_mp_val",
# )


# fig, ax = plt.subplots(1, 1, squeeze=False)
# sns.scatterplot(data=dd, x="x", y="y", hue="sig_mp_ind", ax=ax[0, 0])
# plt.show()
