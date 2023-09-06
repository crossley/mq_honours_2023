from imports import *


def load_all_data():
    d_list = []
    for sub_num in np.arange(1, 12, 1):
        if sub_num % 2 == 0:
            condition = 1
        else:
            condition = 0

        d_move = pd.read_csv("../data/data_movements_" + str(sub_num) + ".csv")
        d_config = pd.read_csv("../config/config_reach_" + str(sub_num) + ".csv")

        d_config = d_config[
            [
                "trial",
                "no_uncertainty",
                "low_uncertainty",
                "high_uncertainty",
                "unlimited_uncertainty",
                "rot",
                "target_angle",
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

        d = pd.merge(d_move, d_config, on="trial")
        d = d.sort_values(["sample", "time", "trial"])
        d = d[d["state"] == "reach"]
        d["subject"] = sub_num
        d["condition"] = condition

        d = d[
            [
                "sample",
                "time",
                "x",
                "y",
                "trial",
                "phase",
                "subject",
                "condition",
                "no_uncertainty",
                "low_uncertainty",
                "high_uncertainty",
                "unlimited_uncertainty",
                "rot",
                "target_angle",
            ]
        ]

        d["sig_mp"] = (
            1 * d["no_uncertainty"]
            + 2 * d["low_uncertainty"]
            + 3 * d["high_uncertainty"]
            + 4 * d["unlimited_uncertainty"]
        ).astype("category")

        d["sig_mp"] = d["sig_mp"].cat.rename_categories(
            ["basewash", "low", "med", "high", "Inf"]
        )

        d_list.append(d)

    d = pd.concat(d_list)

    return d


def interpolate_movements(d):
    t = d["time"]
    x = d["x"]
    y = d["y"]
    v = d["v"]

    xs = CubicSpline(t, x)
    ys = CubicSpline(t, y)
    vs = CubicSpline(t, v)

    tt = np.linspace(t.min(), t.max(), 100)
    xx = xs(tt)
    yy = ys(tt)
    vv = vs(tt)

    relsamp = np.arange(0, tt.shape[0], 1)

    dd = pd.DataFrame({"relsamp": relsamp, "time": tt, "x": xx, "y": yy, "v": vv})
    dd["condition"] = d["condition"].unique()[0]
    dd["subject"] = d["subject"].unique()[0]
    dd["trial"] = d["trial"].unique()[0]
    dd["phase"] = d["phase"].unique()[0]
    dd["sig_mp"] = d["sig_mp"].unique()[0]

    return dd


def compute_kinematics(d):
    t = d["time"].to_numpy()
    x = d["x"].to_numpy()
    y = d["y"].to_numpy()

    vx = np.gradient(x, t)
    vy = np.gradient(y, t)
    v = np.sqrt(vx**2 + vy**2)
    d["v"] = v

    v_peak = v.max()
    ts = t[v > (0.05 * v_peak)][0]

    radius = np.sqrt(x**2 + y**2)
    theta = (np.arctan2(y, x)) * 180 / np.pi

    imv = theta[(t >= ts) & (t <= ts + 0.1)].mean()
    emv = theta[-1]

    d["imv"] = imv
    d["emv"] = emv

    return d


def plot_mpep(d):
    fig, ax = plt.subplots(2, 2, squeeze=False)
    sns.lineplot(
        data=d[d["condition"] == 1],
        x="trial",
        y="imv",
        hue="sig_mp",
        style="phase",
        markers=True,
        legend=False,
        ax=ax[0, 0],
    )
    sns.lineplot(
        data=d[d["condition"] == 1],
        x="trial",
        y="emv",
        hue="sig_mp",
        style="phase",
        markers=True,
        legend=False,
        ax=ax[0, 1],
    )
    sns.lineplot(
        data=d[d["condition"] == 0],
        x="trial",
        y="imv",
        hue="sig_mp",
        style="phase",
        markers=True,
        legend=False,
        ax=ax[1, 0],
    )
    sns.lineplot(
        data=d[d["condition"] == 0],
        x="trial",
        y="emv",
        hue="sig_mp",
        style="phase",
        markers=True,
        legend=False,
        ax=ax[1, 1],
    )
    [x.set_xlabel("Trial") for x in ax.flatten()]
    [x.set_ylabel("Initial Movement Vector") for x in ax[:, 0].flatten()]
    [x.set_ylabel("Endpoint Movement Vector") for x in ax[:, 1].flatten()]
    plt.tight_layout()
    plt.show()
