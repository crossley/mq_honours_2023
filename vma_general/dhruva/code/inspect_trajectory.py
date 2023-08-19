import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

d_config = pd.read_csv("../config/config_reach_1.csv")
d_config = d_config[
    [
        "trial",
        "no_uncertainty",
        "low_uncertainty",
        "high_uncertainty",
        "unlimited_uncertainty",
    ]
]

d_move = pd.read_csv("../data/data_movements_1.csv")

d = pd.merge(d_move, d_config, on="trial")
d = d.sort_values(["sample", "time", "trial"])
d = d[d["state"] == "reach"]

d = d[
    [
        "sample",
        "time",
        "x",
        "y",
        "trial",
        "no_uncertainty",
        "low_uncertainty",
        "high_uncertainty",
        "unlimited_uncertainty",
    ]
]

d["sig_mp"] = (
    d["no_uncertainty"]
    + d["low_uncertainty"]
    + d["high_uncertainty"]
    + d["unlimited_uncertainty"]
)

d["sig_mp_cat"] = pd.from_dummies(
    d[
        [
            "no_uncertainty",
            "low_uncertainty",
            "high_uncertainty",
            "unlimited_uncertainty",
        ]
    ],
    default_category="WHAT?",
)

fig, ax = plt.subplots(2, 3, squeeze=False)
ax = ax.flatten()
for i, smp in enumerate(d["sig_mp_cat"].unique()):
    sns.scatterplot(
        data=d[d["sig_mp_cat"] == smp],
        x="x",
        y="y",
        hue="trial",
        ax=ax[i],
    )
    ax[i].set_title(smp)
plt.tight_layout()
plt.show()


def interpolate_movements(d):

    t = d["time"]
    x = d["x"]
    y = d["y"]

    xs = CubicSpline(t, x)
    ys = CubicSpline(t, y)

    tt = np.linspace(t.min(), t.max(), 150)
    xx = xs(tt)
    yy = ys(tt)

    relsamp = np.arange(0, tt.shape[0], 1)

    # fig, ax = plt.subplots(2, 3, squeeze=False)
    # ax[0, 0].scatter(t, x, c=t)
    # ax[0, 1].scatter(t, y, c=t)
    # ax[0, 2].scatter(x, y, c=t)
    # ax[1, 0].scatter(tt, xx, c=tt)
    # ax[1, 1].scatter(tt, yy, c=tt)
    # ax[1, 2].scatter(xx, yy, c=tt)
    # plt.show()

    dd = pd.DataFrame({"relsamp": relsamp, "time": tt, "x": xx, "y": yy})

    return dd


dd = (
    d.groupby(["trial", "sig_mp_cat"])[["time", "x", "y"]]
    .apply(interpolate_movements)
    .droplevel(2)
    .reset_index(drop=False)
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
