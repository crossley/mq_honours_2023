from imports import *
from util_func import *

d = load_all_data()

# NOTE: grab a subset to play with
d = d[d.subject == 1]
d = d[d.trial < 10]

def inspect_move(d):
    t = d["time"].to_numpy()
    x = d["x"].to_numpy()
    y = d["y"].to_numpy()

    vx = np.gradient(x, t)
    vy = np.gradient(y, t)
    v = np.sqrt(vx**2 + vy**2)
    d['v'] = v

    radius = np.sqrt(x**2 + y**2)
    theta = (np.arctan2(y, x) + np.pi) * 180 / np.pi
    imv = theta[v > 0.05 * v.max()][0]
    emv = theta[-1]
    d["imv"] = imv
    d["emv"] = emv
    # print(d.target_angle.unique()[0], imv, emv)

    xs = CubicSpline(t, x)
    ys = CubicSpline(t, y)
    vs = CubicSpline(t, v)

    tt = np.linspace(t.min(), t.max(), 100)
    xx = xs(tt)
    yy = ys(tt)
    vv = vs(tt)

    relsamp = np.arange(0, tt.shape[0], 1)

    dd = pd.DataFrame({
        "relsamp": relsamp,
        "time": tt,
        "x": xx,
        "y": yy,
        "v": vv
    })

    fig, ax = plt.subplots(2, 2, squeeze=False, figsize=(8, 8))
    sns.scatterplot(data=d, x='x', y='y', hue='time', legend=None, ax=ax[0, 0])
    sns.scatterplot(data=d,
                    x='time',
                    y='v',
                    hue='time',
                    legend=None,
                    ax=ax[0, 1])
    sns.scatterplot(data=dd,
                    x='x',
                    y='y',
                    hue='time',
                    legend=None,
                    ax=ax[1, 0])
    sns.scatterplot(data=dd,
                    x='time',
                    y='v',
                    hue='time',
                    legend=None,
                    ax=ax[1, 1])
    ax[0, 0].set_xlim(-11, 11)
    ax[1, 0].set_xlim(-11, 11)
    plt.tight_layout()
    plt.show()


d.groupby(["condition", "subject", "trial"]).apply(inspect_move)


# d = d.groupby(["subject", "trial"], group_keys=False).apply(compute_vel)
# d = d.groupby(["subject", "trial"], group_keys=False).apply(compute_mv)
# d = d.sort_values(["condition", "subject", "trial"])

# # TODO: interpoloate / smooth before or after?

# fig, ax = plt.subplots(2, 2, squeeze=False)
# [x.set_ylim(-20, 20) for x in ax.flatten()]
# sns.lineplot(
#     data=d[d["condition"] == 1],
#     x="trial",
#     y="imv",
#     hue="sig_mp",
#     style="phase",
#     markers=True,
#     legend=False,
#     ax=ax[0, 0],
# )
# sns.lineplot(
#     data=d[d["condition"] == 1],
#     x="trial",
#     y="emv",
#     hue="sig_mp",
#     style="phase",
#     markers=True,
#     legend=False,
#     ax=ax[0, 1],
# )
# sns.lineplot(
#     data=d[d["condition"] == 0],
#     x="trial",
#     y="imv",
#     hue="sig_mp",
#     style="phase",
#     markers=True,
#     legend=False,
#     ax=ax[1, 0],
# )
# sns.lineplot(
#     data=d[d["condition"] == 0],
#     x="trial",
#     y="emv",
#     hue="sig_mp",
#     style="phase",
#     markers=True,
#     legend=False,
#     ax=ax[1, 1],
# )
# [x.set_xlabel("Trial") for x in ax.flatten()]
# [x.set_ylabel("Initial Movement Vector") for x in ax[:, 0].flatten()]
# [x.set_ylabel("Endpoint Movement Vector") for x in ax[:, 1].flatten()]
# plt.tight_layout()
# plt.show()


# # dd = (
# #     d.groupby(["subject", "phase", "trial", "sig_mp"])[["time", "x", "y", "v"]]
# #     .apply(interpolate_movements)
# #     .droplevel(-1)
# #     .reset_index(drop=False)
# # )

# # dd = dd.sort_values(["trial", "relsamp"])

# # dd.plot(subplots=True)
# # plt.show()

# # ddd = (
# #     dd.groupby(["subject", "phase", "sig_mp", "relsamp"])[["time", "x", "y", "v"]]
# #     .mean()
# #     .reset_index()
# # )

# # ddd.plot(subplots=True)
# # plt.show()

# # fig, ax = plt.subplots(2, 2, squeeze=False)
# # sns.scatterplot(
# #     data=ddd[ddd["phase"] == "adapt_1"], x="x", y="y", hue="sig_mp", ax=ax[0, 0]
# # )
# # sns.scatterplot(
# #     data=ddd[ddd["phase"] == "adapt_2"], x="x", y="y", hue="sig_mp", ax=ax[0, 1]
# # )
# # sns.scatterplot(
# #     data=ddd[ddd["phase"] == "adapt_3"], x="x", y="y", hue="sig_mp", ax=ax[1, 0]
# # )
# # sns.scatterplot(
# #     data=ddd[ddd["phase"] == "adapt_4"], x="x", y="y", hue="sig_mp", ax=ax[1, 1]
# # )
# # ax[0, 0].set_title("adapt 1")
# # ax[0, 1].set_title("adapt 2")
# # ax[1, 0].set_title("adapt 3")
# # ax[1, 1].set_title("adapt 4")
# # plt.tight_layout()
# # plt.show()


# # dddd = dd.groupby(["subject", "relsamp"])[["time", "x", "y", "v"]].mean().reset_index()

# # dddd.plot(subplots=True)
# # plt.show()
