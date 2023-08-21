from imports import *


def load_all_data():
    d_list = []
    for sub_num in np.arange(1, 8, 1):
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

        # d = d[np.isin(d["phase"], ["adapt_1", "adapt_2", "adapt_3", "adapt_4"])]

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


def compute_vel(d):
    t = d["time"].to_numpy()
    x = d["x"].to_numpy()
    y = d["y"].to_numpy()
    vx = np.gradient(x, t)
    vy = np.gradient(y, t)
    v = np.sqrt(vx**2 + vy**2)
    d["v"] = v
    return d


def compute_mv(d):
    t = d["time"].to_numpy()
    x = d["x"].to_numpy()
    y = d["y"].to_numpy()
    target_angle = d["target_angle"]
    t = t - t.min()
    theta = np.arctan2(y, x) * (180 / np.pi)
    theta, radius = cart2pol(x, y, units="deg")
    imv = theta[radius < 5].mean() - target_angle
    emv = theta[-1] - target_angle
    d["imv"] = -imv
    d["emv"] = -emv
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

    return dd
