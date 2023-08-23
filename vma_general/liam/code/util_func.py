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
        d_trial = pd.read_csv("../data/data_trials_" + str(sub_num) + ".csv")

        d_config = d_config[
            [
                "condition",
                "subject",
                "phase",
                "trial",
                "rot",
                "target_angle",
            ]
        ]

        d_trial = d_trial[["trial", "endpoint_theta"]]

        d = pd.merge(d_move, d_config, on="trial")
        d = pd.merge(d, d_trial, on="trial")

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
                "subject",
                "condition",
                "rot",
                "target_angle",
                "endpoint_theta",
            ]
        ]

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
    theta, radius = cart2pol(x, y, units="deg")
    imv = theta[radius < 5].mean()
    emv = theta[-1]
    d["imv"] = imv - target_angle
    d["emv"] = emv - target_angle
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
