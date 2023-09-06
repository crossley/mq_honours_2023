from imports import *
from util_func import *

# TODO: sub 0 data file is whack
d = load_all_data()
d = d.sort_values(["condition", "subject", "trial"])

# d.loc[d["target_angle"] > 180, "target_angle"] -= 360
# d.loc[(d["target_angle"] == 180) & (d["endpoint_theta"] < 0), "endpoint_theta"] += 360
# d["endpoint_theta"] = -d["endpoint_theta"] + d["target_angle"]

d = d.groupby(["condition", "subject", "trial"], group_keys=False).apply(
    compute_kinematics
)
# d.loc[d["target_angle"] > 180, "target_angle"] -= 360
# d.loc[(d["target_angle"] == 180) & (d["endpoint_theta"] < 0), "endpoint_theta"] += 360
# d["endpoint_theta"] = -d["endpoint_theta"] + d["target_angle"]

for s in d["subject"].unique()[:2]:
    fig, ax = plt.subplots(3, 4, squeeze=False, figsize=(12, 8))
    for i, ta in enumerate(np.sort(d["target_angle"].unique())):
        color = plt.cm.viridis(i / d["target_angle"].unique().shape[0])
        dd = d[(d["target_angle"] == ta) & (d["subject"] == s)]
        ax.flatten()[i].scatter(dd["trial"], dd["emv"], color="C0")
        ax.flatten()[i].scatter(dd["trial"], dd["endpoint_theta"], color="C1")
        ax.flatten()[i].plot(dd["trial"], [ta] * dd.shape[0], "--k")
        ax.flatten()[i].legend()
    plt.tight_layout()
    plt.show()




# dd = d.groupby(
#     ["condition", "subject", "phase", "trial", "target_angle"], group_keys=False
# ).apply(interpolate_movements)
#
# ddd = (
#     dd.groupby(["condition", "subject", "phase", "target_angle", "relsamp"])[
#         ["time", "x", "y", "v"]
#     ]
#     .mean()
#     .reset_index()
# )

# d.plot(subplots=True)
# plt.show()
# dd.plot(subplots=True)
# plt.show()
# ddd.plot(subplots=True)
# plt.show()

# print(d.groupby(["condition"])["subject"].unique())

# d = (
#     d.groupby(["condition", "phase", "trial", "target_angle"])[["emv", "rot"]]
#     .mean()
#     .reset_index()
# )


# TODO: sort this mess out
# target_angle is coded as [0, 360]
# emv is coded as [-180, 180]
# d["target_angle"] -= 180
