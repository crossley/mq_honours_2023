from imports import *
from util_func import *

# TODO: sub 0 data file is whack
d = load_all_data()

# # NOTE: grab a subset to play with
# d = d[d.subject == 1]
# d = d[d.trial < 10]


# def inspect_move(d):
#     t = d["time"].to_numpy()
#     x = d["x"].to_numpy()
#     y = d["y"].to_numpy()

#     vx = np.gradient(x, t)
#     vy = np.gradient(y, t)
#     v = np.sqrt(vx**2 + vy**2)
#     d['v'] = v

#     radius = np.sqrt(x**2 + y**2)
#     theta = (np.arctan2(y, x) + np.pi) * 180 / np.pi
#     imv = theta[v > 0.05 * v.max()][0]
#     emv = theta[-1]
#     d["imv"] = imv
#     d["emv"] = emv
#     # print(d.target_angle.unique()[0], imv, emv)

#     xs = CubicSpline(t, x)
#     ys = CubicSpline(t, y)
#     vs = CubicSpline(t, v)

#     tt = np.linspace(t.min(), t.max(), 100)
#     xx = xs(tt)
#     yy = ys(tt)
#     vv = vs(tt)

#     relsamp = np.arange(0, tt.shape[0], 1)

#     dd = pd.DataFrame({
#         "relsamp": relsamp,
#         "time": tt,
#         "x": xx,
#         "y": yy,
#         "v": vv
#     })

#     fig, ax = plt.subplots(2, 2, squeeze=False, figsize=(8, 8))
#     sns.scatterplot(data=d, x='x', y='y', hue='time', legend=None, ax=ax[0, 0])
#     sns.scatterplot(data=d,
#                     x='time',
#                     y='v',
#                     hue='time',
#                     legend=None,
#                     ax=ax[0, 1])
#     sns.scatterplot(data=dd,
#                     x='x',
#                     y='y',
#                     hue='time',
#                     legend=None,
#                     ax=ax[1, 0])
#     sns.scatterplot(data=dd,
#                     x='time',
#                     y='v',
#                     hue='time',
#                     legend=None,
#                     ax=ax[1, 1])
#     ax[0, 0].set_xlim(-11, 11)
#     ax[1, 0].set_xlim(-11, 11)
#     plt.tight_layout()
#     plt.show()


# d.groupby(["condition", "subject", "trial"]).apply(inspect_move)

d = (d.groupby(["condition", "subject", "trial"],
               group_keys=False).apply(compute_vel).reset_index())
# d = (
#     d.groupby(["condition", "subject", "trial"], group_keys=False)
#     .apply(interpolate_movements)
#     .reset_index()
# )
d = (d.groupby(["condition", "subject", "trial"],
               group_keys=False).apply(compute_mv).reset_index())
d = d.sort_values(["condition", "subject", "trial"])

dd = d.groupby(["time"], group_keys=False)[["v"]].mean().reset_index()
fig, ax = plt.subplots(1, 1, squeeze=False)
sns.scatterplot(data=dd, x="time", y="v")
plt.show()

print(d.groupby(["condition"])["subject"].unique())

dd = d[[
    "condition",
    "subject",
    "phase",
    "trial",
    "target_angle",
    "endpoint_theta",
    "rot",
    "emv",
]].drop_duplicates()

# TODO: fix up weird target angle stuff
# print(dd.target_angle.unique())
dd.loc[dd["target_angle"] > 180, "target_angle"] -= 360
dd.loc[(dd["target_angle"] == 180) & (dd["endpoint_theta"] < 0),
       "endpoint_theta"] += 360
dd["endpoint_theta"] = -dd["endpoint_theta"] + dd["target_angle"]

dd = (dd.groupby(["condition", "phase", "trial",
                  "target_angle"])[["endpoint_theta",
                                    "rot"]].mean().reset_index())

dd["target_angle"] = dd["target_angle"].astype("category")
fig, ax = plt.subplots(2, 1, squeeze=False)
sns.scatterplot(
    data=dd[(dd["condition"] == "high") & (dd["target_angle"] == 90)],
    x="trial",
    y="rot",
    color="black",
    markers=True,
    legend=False,
    ax=ax[0, 0],
)
sns.scatterplot(
    data=dd[(dd["condition"] == "low") & (dd["target_angle"] == 90)],
    x="trial",
    y="rot",
    color="black",
    markers=True,
    legend=False,
    ax=ax[1, 0],
)
sns.scatterplot(
    data=dd[(dd["condition"] == "high") & (dd["target_angle"] == 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    ax=ax[0, 0],
)
sns.scatterplot(
    data=dd[(dd["condition"] == "low") & (dd["target_angle"] == 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    ax=ax[1, 0],
)
sns.scatterplot(
    data=dd[(dd["condition"] == "high") & (dd["target_angle"] != 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    alpha=0.1,
    ax=ax[0, 0],
)
sns.scatterplot(
    data=dd[(dd["condition"] == "low") & (dd["target_angle"] != 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    alpha=0.1,
    ax=ax[1, 0],
)

# for i in range(dd.target_angle.unique().size):
#     ax[0, 0].plot(
#         [dd.trial.min(), dd.trial.max()],
#         [dd.target_angle.unique()[i],
#          dd.target_angle.unique()[i]],
#         "--k",
#         alpha=0.5,
#     )
#     ax[1, 0].plot(
#         [dd.trial.min(), dd.trial.max()],
#         [dd.target_angle.unique()[i],
#          dd.target_angle.unique()[i]],
#         "--k",
#         alpha=0.5,
#     )

[xx.set_ylim((-50, 50)) for xx in ax.flatten()]
[x.set_xlabel("Trial") for x in ax.flatten()]
[x.set_ylabel("Endpoint Hand Angle") for x in ax[:, 0].flatten()]
plt.tight_layout()
# plt.savefig("../figures/fig_1.pdf")
plt.show()
plt.close()

fig, ax = plt.subplots(2, 1, squeeze=False)
sns.scatterplot(
    data=dd[(dd["condition"] == "high") & (dd["target_angle"] == 90)],
    x="trial",
    y="endpoint_theta",
    hue="phase",
    style="phase",
    markers=True,
    legend=False,
    ax=ax[0, 0],
)
sns.scatterplot(
    data=dd[(dd["condition"] == "low") & (dd["target_angle"] == 90)],
    x="trial",
    y="endpoint_theta",
    hue="phase",
    style="phase",
    markers=True,
    legend=False,
    ax=ax[1, 0],
)
[x.set_xlabel("Trial") for x in ax.flatten()]
[x.set_ylabel("Endpoint Hand Angle") for x in ax[:, 0].flatten()]
plt.tight_layout()
# plt.savefig("../figures/fig_2.pdf")
plt.show()
plt.close()
