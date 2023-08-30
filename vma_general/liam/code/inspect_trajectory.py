from imports import *
from util_func import *

# TODO: sub 0 data file is whack
d = load_all_data()

d = d.sort_values(["condition", "subject", "trial"])

d = d.groupby(["condition", "subject", "trial"], group_keys=False).apply(
    compute_kinematics
)

dd = d.groupby(["condition", "subject", "phase", "trial"], group_keys=False).apply(
    interpolate_movements
)

ddd = (
    dd.groupby(["condition", "subject", "phase", "relsamp"])[["time", "x", "y", "v"]]
    .mean()
    .reset_index()
)

# d.plot(subplots=True)
# plt.show()
# dd.plot(subplots=True)
# plt.show()
# ddd.plot(subplots=True)
# plt.show()

print(d.groupby(["condition"])["subject"].unique())

dd = d[
    [
        "condition",
        "subject",
        "phase",
        "trial",
        "target_angle",
        "endpoint_theta",
        "rot",
        "emv",
    ]
].drop_duplicates()

dd.loc[dd["target_angle"] > 180, "target_angle"] -= 360
dd.loc[
    (dd["target_angle"] == 180) & (dd["endpoint_theta"] < 0), "endpoint_theta"
] += 360
dd["endpoint_theta"] = -dd["endpoint_theta"] + dd["target_angle"]

dd = (
    dd.groupby(["condition", "phase", "trial", "target_angle"])[
        ["endpoint_theta", "rot"]
    ]
    .mean()
    .reset_index()
)

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

for i in range(dd.target_angle.unique().size):
    ax[0, 0].plot(
        [dd.trial.min(), dd.trial.max()],
        [dd.target_angle.unique()[i],
         dd.target_angle.unique()[i]],
        "--k",
        alpha=0.5,
    )
    ax[1, 0].plot(
        [dd.trial.min(), dd.trial.max()],
        [dd.target_angle.unique()[i],
         dd.target_angle.unique()[i]],
        "--k",
        alpha=0.5,
    )

[xx.set_ylim((-50, 50)) for xx in ax.flatten()]
[x.set_xlabel("Trial") for x in ax.flatten()]
[x.set_ylabel("Endpoint Hand Angle") for x in ax[:, 0].flatten()]
plt.tight_layout()
# plt.savefig("../figures/fig_1.pdf")
plt.show()
plt.close()
