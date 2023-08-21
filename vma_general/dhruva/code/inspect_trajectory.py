import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

d_move = pd.read_csv("../data/data_movements_1.csv")
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

d_config["phase"] = (
    ["base"] * 20
    + ["adapt_1"] * 45
    + ["adapt_2"] * 45
    + ["adapt_3"] * 45
    + ["adapt_4"] * 45
    + ["wash"] * 100
)

d_config.plot(subplots=True)
plt.show()

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
        "phase",
        "no_uncertainty",
        "low_uncertainty",
        "high_uncertainty",
        "unlimited_uncertainty",
    ]
]

d = d[np.isin(d["phase"], ["adapt_1", "adapt_2", "adapt_3", "adapt_4"])]

d["sig_mp"] = (
    d["no_uncertainty"]
    + 2 * d["low_uncertainty"]
    + 3 * d["high_uncertainty"]
    + 4 * d["unlimited_uncertainty"]
).astype("category")
d["sig_mp"] = d["sig_mp"].cat.rename_categories(["low", "med", "high", "Inf"])

fig, ax = plt.subplots(2, 2, squeeze=False)
sns.scatterplot(
    data=d[d["phase"] == "adapt_1"], x="x", y="y", hue="sig_mp", ax=ax[0, 0]
)
sns.scatterplot(
    data=d[d["phase"] == "adapt_2"], x="x", y="y", hue="sig_mp", ax=ax[0, 1]
)
sns.scatterplot(
    data=d[d["phase"] == "adapt_3"], x="x", y="y", hue="sig_mp", ax=ax[1, 0]
)
sns.scatterplot(
    data=d[d["phase"] == "adapt_4"], x="x", y="y", hue="sig_mp", ax=ax[1, 1]
)
ax[0, 0].set_title("adapt 1")
ax[0, 1].set_title("adapt 2")
ax[1, 0].set_title("adapt 3")
ax[1, 1].set_title("adapt 4")
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

    dd = pd.DataFrame({"relsamp": relsamp, "time": tt, "x": xx, "y": yy})

    return dd


dd = (
    d.groupby(["phase", "trial", "sig_mp"])[["time", "x", "y"]]
    .apply(interpolate_movements)
    .droplevel(-1)
    .reset_index(drop=False)
)

dd = dd.sort_values(["trial", "relsamp"])

fig, ax = plt.subplots(2, 2, squeeze=False)
sns.scatterplot(
    data=dd[dd["phase"] == "adapt_1"], x="x", y="y", hue="sig_mp", ax=ax[0, 0]
)
sns.scatterplot(
    data=dd[dd["phase"] == "adapt_2"], x="x", y="y", hue="sig_mp", ax=ax[0, 1]
)
sns.scatterplot(
    data=dd[dd["phase"] == "adapt_3"], x="x", y="y", hue="sig_mp", ax=ax[1, 0]
)
sns.scatterplot(
    data=dd[dd["phase"] == "adapt_4"], x="x", y="y", hue="sig_mp", ax=ax[1, 1]
)
ax[0, 0].set_title("adapt 1")
ax[0, 1].set_title("adapt 2")
ax[1, 0].set_title("adapt 3")
ax[1, 1].set_title("adapt 4")
plt.tight_layout()
plt.show()


ddd = (
    dd.groupby(["phase", "sig_mp", "relsamp"])[["time", "x", "y"]].mean().reset_index()
)

fig, ax = plt.subplots(2, 2, squeeze=False)
sns.scatterplot(
    data=ddd[ddd["phase"] == "adapt_1"], x="x", y="y", hue="sig_mp", ax=ax[0, 0]
)
sns.scatterplot(
    data=ddd[ddd["phase"] == "adapt_2"], x="x", y="y", hue="sig_mp", ax=ax[0, 1]
)
sns.scatterplot(
    data=ddd[ddd["phase"] == "adapt_3"], x="x", y="y", hue="sig_mp", ax=ax[1, 0]
)
sns.scatterplot(
    data=ddd[ddd["phase"] == "adapt_4"], x="x", y="y", hue="sig_mp", ax=ax[1, 1]
)
ax[0, 0].set_title("adapt 1")
ax[0, 1].set_title("adapt 2")
ax[1, 0].set_title("adapt 3")
ax[1, 1].set_title("adapt 4")
plt.tight_layout()
plt.show()


# TODO: this should be velocity based
def compute_imv(d):
    t = d["time"].to_numpy()
    x = d["x"].to_numpy()
    y = d["y"].to_numpy()
    t = t - t.min()
    theta = np.arctan2(y, x) * (180 / np.pi)
    imv = theta.mean()
    print(imv)
    return imv


dd["imv"] = dd.groupby(["trial"]).apply(compute_imv)

fig, ax = plt.subplots(1, 1, squeeze=False)
sns.scatterplot(data=dd, x="trial", y="imv", hue="sig_mp", ax=ax[0, 0])
plt.show()

# vx = np.diff(ddd["x"]) / np.diff(ddd["time"])
# vy = np.diff(ddd["y"]) / np.diff(ddd["time"])
# vxy = np.sqrt(vx**2 + vy**2)
# vt = ddd["time"].to_numpy()[:-1]

# fig, ax = plt.subplots(3, 1, squeeze=False)
# ax[0, 0].scatter(vt, vx)
# ax[1, 0].scatter(vt, vy)
# ax[2, 0].scatter(vt, vxy)
# plt.show()
