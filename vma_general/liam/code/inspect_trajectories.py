import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

d_config = pd.read_csv("../config/config_reach_0.csv")
d_move = pd.read_csv(
    "../data/data_movements_0.csv",
    index_col=0
)

d_config = d_config.sort_values(["trial"])
d_move = d_move.sort_values(["sample", "time", "trial"])
d_move = d_move[d_move["state"] == "reach"]


d = pd.merge(d_move, d_config, on="trial")
d = d.sort_values(["sample", "time", "trial"])
d = d[d["state"] == "reach"]
d["target_angle"] = d["target_angle"].astype("category")

fig, ax = plt.subplots(2, 1, squeeze=False)
sns.scatterplot(data=d, x="trial", y="rot", hue="phase", ax=ax[0, 0])
sns.scatterplot(data=d, x="trial", y="target_angle", hue="phase", ax=ax[1, 0])
plt.show()

# inspect d_config
d_config.plot(subplots=True)
plt.show()

# inspect d_move
fig, ax = plt.subplots(2, 2, squeeze=False)
sns.scatterplot(data=d_move, x="sample", y="time", hue="trial", ax=ax[0, 0])
sns.scatterplot(data=d_move, x="time", y="x", hue="trial", ax=ax[0, 1])
sns.scatterplot(data=d_move, x="time", y="y", hue="trial", ax=ax[1, 0])
sns.scatterplot(data=d_move, x="x", y="y", hue="trial", ax=ax[1, 1])
plt.show()


fig, ax = plt.subplots(3, 4, squeeze=False)
ax = ax.flatten()
for i, ta in enumerate(d["target_angle"].unique()):
    sns.scatterplot(
        data=d[d["target_angle"] == ta],
        x="x",
        y="y",
        hue="trial",
        legend=False,
        ax=ax[i],
    )
    ax[i].set_title(ta)
plt.tight_layout()
plt.show()


def interpolate_movements(d):
    t = d["time"]
    x = d["x"]
    y = d["y"]

    print(d)
    print(t)

    xs = CubicSpline(t, x)
    ys = CubicSpline(t, y)

    tt = np.linspace(t.min(), t.max(), 150)
    xx = xs(tt)
    yy = ys(tt)

    relsamp = np.arange(0, tt.shape[0], 1)

    fig, ax = plt.subplots(2, 3, squeeze=False)
    ax[0, 0].scatter(t, x, c=t)
    ax[0, 1].scatter(t, y, c=t)
    ax[0, 2].scatter(x, y, c=t)
    ax[1, 0].scatter(tt, xx, c=tt)
    ax[1, 1].scatter(tt, yy, c=tt)
    ax[1, 2].scatter(xx, yy, c=tt)
    plt.show()

    dd = pd.DataFrame({"relsamp": relsamp, "time": tt, "x": xx, "y": yy})

    return dd


dd = (
    d.groupby(["trial"])[["time", "x", "y"]].apply(interpolate_movements)
    # .droplevel(2)
    # .reset_index(drop=False)
)

# dd = dd.sort_values(["trial", "relsamp"])

# fig, ax = plt.subplots(2, 2, squeeze=False)
# ax = ax.flatten()
# for i, smp in enumerate(dd["sig_mp_cat"].unique()):
#     sns.scatterplot(
#         data=dd[dd["sig_mp_cat"] == smp],
#         x="x",
#         y="y",
#         hue="trial",
#         ax=ax[i],
#     )
#     ax[i].set_title(smp)
# plt.tight_layout()
# plt.show()


# ddd = dd.groupby(["sig_mp_cat", "relsamp"])[["time", "x", "y"]].mean().reset_index()

# fig, ax = plt.subplots(2, 2, squeeze=False)
# ax = ax.flatten()
# for i, smp in enumerate(dd["sig_mp_cat"].unique()):
#     sns.scatterplot(
#         data=ddd[ddd["sig_mp_cat"] == smp], x="x", y="y", hue="time", ax=ax[i]
#     )
#     ax[i].set_title(smp)
# plt.tight_layout()
# plt.show()


# # vx = np.diff(ddd["x"]) / np.diff(ddd["time"])
# # vy = np.diff(ddd["y"]) / np.diff(ddd["time"])
# # vel = np.sqrt(vx**2 + vy**2)
# # vt = ddd["time"].to_numpy()[:-1]

# # fig, ax = plt.subplots(1, 2, squeeze=False)
# # ax[0, 0].plot(vt, vel)
# # plt.show()
