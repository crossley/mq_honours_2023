from imports import *
from util_func import *

d = load_all_data()

d = d.groupby(["subject", "trial"], group_keys=False).apply(compute_vel)
d = d.groupby(["subject", "trial"], group_keys=False).apply(compute_mv)
d = d.sort_values(["condition", "subject", "trial"])

# TODO: sub 0 data file is whack
# TODO: interpoloate / smooth before or after?

d["target_angle"] = d["target_angle"].astype("category")
fig, ax = plt.subplots(2, 1, squeeze=False)
sns.scatterplot(
    data=d[(d["condition"] == "high") & (d["target_angle"] == 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    ax=ax[0, 0],
)
sns.scatterplot(
    data=d[(d["condition"] == "low") & (d["target_angle"] == 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    ax=ax[1, 0],
)
sns.scatterplot(
    data=d[(d["condition"] == "high") & (d["target_angle"] != 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    alpha=0.01,
    ax=ax[0, 0],
)
sns.scatterplot(
    data=d[(d["condition"] == "low") & (d["target_angle"] != 90)],
    x="trial",
    y="endpoint_theta",
    hue="target_angle",
    style="phase",
    markers=True,
    legend=False,
    alpha=0.01,
    ax=ax[1, 0],
)
[x.set_xlabel("Trial") for x in ax.flatten()]
[x.set_ylabel("Initial Movement Vector") for x in ax[:, 0].flatten()]
plt.tight_layout()
plt.show()
