import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

n_subs_per_cnd = 1
conditions = ["no_inst", "direct_aim"] * n_subs_per_cnd
np.random.shuffle(conditions)

# Specify the mean and standard deviation of the perturbation to be applied
# during the adapt phase.
rot_mean = 12
rot_sig = 4

# 50 dots per cloud
# sd of dot cloud in cm
# the -1 is to indicate infinite uncertainty trials
sig_mp = np.array([0.0, 0.5, 1.0, -1.0])

# state how frequently you will display phase instructions
n_trials_to_repeat_inst = 5

for i in range(len(conditions)):
    # By setting the random number generation seed we ensure that every
    # participant gets the same random sequence
    np.random.seed(0)

    # Specify possible target angles
    target_angle = np.array([0])
    target_train = target_angle[0]
    n_targets = target_angle.shape[0]

    # Specify the number of times you want to cycle through the targets. Note
    # that each phase can have a different set of targets to cycle between (see
    # below).
    n_cycle_baseline_no_fb = 0
    n_cycle_baseline_continuous_fb = 100
    n_cycle_baseline_endpoint_fb = 0
    n_cycle_baseline_mixed_fb = 0
    n_cycle_adapt = 180
    n_cycle_generalisation = 0
    n_cycle_washout_no_fb = 100
    n_cycle_washout_fb = 0

    n_gen_tops = n_targets - 1

    # Specify a single cycle's worth of targets for each phase
    targets_baseline_no_fb = target_angle
    targets_baseline_continuous_fb = target_angle
    targets_baseline_endpoint_fb = target_angle
    targets_baseline_mixed_fb = target_angle
    targets_adapt = np.array([target_train])
    targets_generalisation = np.concatenate(
        (np.tile(target_angle[0], n_gen_tops), target_angle[1:])
    )
    targets_washout_no_fb = target_angle
    targets_washout_fb = target_angle

    # Construct a target_angle array to be later added to the config dataframe
    target_angle = np.concatenate(
        (
            np.tile(targets_baseline_no_fb, n_cycle_baseline_no_fb),
            np.tile(targets_baseline_continuous_fb, n_cycle_baseline_continuous_fb),
            np.tile(targets_baseline_endpoint_fb, n_cycle_baseline_endpoint_fb),
            np.tile(targets_baseline_mixed_fb, n_cycle_baseline_mixed_fb),
            np.tile(targets_adapt, n_cycle_adapt),
            np.tile(targets_generalisation, n_cycle_generalisation),
            np.tile(targets_washout_no_fb, n_cycle_washout_no_fb),
            np.tile(targets_washout_fb, n_cycle_washout_fb),
        )
    )

    # For each phase, create an array to indicate the current cycle
    cycle_baseline_no_fb = np.repeat(
        np.arange(1, n_cycle_baseline_no_fb + 1, 1), targets_baseline_no_fb.shape[0]
    )
    cycle_baseline_continuous_fb = np.repeat(
        np.arange(1, n_cycle_baseline_continuous_fb + 1, 1),
        targets_baseline_continuous_fb.shape[0],
    )
    cycle_baseline_endpoint_fb = np.repeat(
        np.arange(1, n_cycle_baseline_endpoint_fb + 1, 1),
        targets_baseline_endpoint_fb.shape[0],
    )
    cycle_baseline_mixed_fb = np.repeat(
        np.arange(1, n_cycle_baseline_mixed_fb + 1, 1),
        targets_baseline_mixed_fb.shape[0],
    )
    cycle_adapt = np.repeat(np.arange(1, n_cycle_adapt + 1, 1), targets_adapt.shape[0])
    cycle_generalisation = np.repeat(
        np.arange(1, n_cycle_generalisation + 1, 1), targets_generalisation.shape[0]
    )
    cycle_washout_no_fb = np.repeat(
        np.arange(1, n_cycle_washout_no_fb + 1, 1), targets_washout_no_fb.shape[0]
    )
    cycle_washout_fb = np.repeat(
        np.arange(1, n_cycle_washout_fb + 1, 1), targets_washout_fb.shape[0]
    )

    # Combine the above into an array that can later be added to the config data frame
    cycle_phase = np.concatenate(
        (
            cycle_baseline_no_fb,
            cycle_baseline_continuous_fb,
            cycle_baseline_endpoint_fb,
            cycle_baseline_mixed_fb,
            cycle_adapt,
            cycle_generalisation,
            cycle_washout_no_fb,
            cycle_washout_fb,
        )
    )

    # Get the number of trials the previous two chunks yield for each phase
    n_trial_baseline_no_fb = n_cycle_baseline_no_fb * targets_baseline_no_fb.shape[0]
    n_trial_baseline_continuous_fb = (
        n_cycle_baseline_continuous_fb * targets_baseline_continuous_fb.shape[0]
    )
    n_trial_baseline_endpoint_fb = (
        n_cycle_baseline_endpoint_fb * targets_baseline_endpoint_fb.shape[0]
    )
    n_trial_baseline_mixed_fb = (
        n_cycle_baseline_mixed_fb * targets_baseline_mixed_fb.shape[0]
    )
    n_trial_adapt = n_cycle_adapt * targets_adapt.shape[0]
    n_trial_generalisation = n_cycle_generalisation * targets_generalisation.shape[0]
    n_trial_washout_no_fb = n_cycle_washout_no_fb * targets_washout_no_fb.shape[0]
    n_trial_washout_fb = n_cycle_washout_fb * targets_washout_fb.shape[0]

    # Get the full number of trials combined across all phases
    n_trial = 0
    n_trial += n_trial_baseline_no_fb
    n_trial += n_trial_baseline_continuous_fb
    n_trial += n_trial_baseline_endpoint_fb
    n_trial += n_trial_baseline_mixed_fb
    n_trial += n_trial_adapt
    n_trial += n_trial_generalisation
    n_trial += n_trial_washout_no_fb
    n_trial += n_trial_washout_fb

    # Construct a trial array to later add to the config dataframe
    trial = np.arange(1, n_trial + 1, 1)

    # Construct a phase indicator columns to be later added to the config dataframe
    phase = np.concatenate(
        (
            ["baseline_no_fb"] * n_trial_baseline_no_fb,
            ["baseline_continuous_fb"] * n_trial_baseline_continuous_fb,
            ["baseline_endpoint_fb"] * n_trial_baseline_endpoint_fb,
            ["baseline_mixed_fb"] * n_trial_baseline_mixed_fb,
            ["adapt"] * n_trial_adapt,
            ["generalisation"] * n_trial_generalisation,
            ["washout_no_fb"] * n_trial_washout_no_fb,
            ["washout_fb"] * n_trial_washout_fb,
        )
    )

    # Specify phase-specific instructions.
    instruct_phase = {}
    instruct_phase["baseline_no_fb"] = (
        "Please slice through the target as quickly and accurately as possible.\n"
        + "You will not see the cursor during this phase."
    )

    instruct_phase["baseline_continuous_fb"] = (
        "You will now only see the cursor throughout your entire reach.\n"
        + "Please continue to slice through the target as quickly and accurately as possible."
    )

    instruct_phase["baseline_continuous_fb"] = (
        "You will now only see the cursor throughout your entire reach.\n"
        + "Please continue to slice through the target as quickly and accurately as possible."
    )

    instruct_phase["baseline_endpoint_fb"] = (
        "You will now only see the cursor only at the endpoint of your reach.\n"
        + "Please continue to slice through the target as quickly and accurately as possible."
    )

    instruct_phase["baseline_mixed_fb"] = (
        "You will now only see the cursor at the endpoint of your reach on some trials.\n"
        + "On the other trials you will not recieve feedback at all.\n"
        "Please continue to slice through the target as quickly and accurately as possible."
    )

    if conditions[i] == "no_inst":
        instruct_phase[
            "adapt"
        ] = "Use the cursor to guide your reaches whenever it is available."

    elif conditions[i] == "direct_aim":
        instruct_phase[
            "adapt"
        ] = "Ignore the cursor and reach directly to the visual location of the target."

    instruct_phase["generalisation"] = (
        "You will now be asked to reach to targets that you have not yet reached to.\n"
        + "You will not receive feedback of any kind for these reaches."
        + "Please continue to slice through the target as quickly and accurately as possible."
    )

    instruct_phase["washout_no_fb"] = (
        "You will not receive feedback of any kind for the following reaches."
        + "Please continue to slice through the target as quickly and accurately as possible."
    )

    instruct_phase["washout_fb"] = (
        "You will now only see the cursor throughout your entire reach.\n"
        + "Please continue to slice through the target as quickly and accurately as possible."
    )

    # Create arrays that contain the phase-specific instructions once at the
    # start of each phase and nowhere else.
    if n_trial_baseline_no_fb > 0:
        inst_inds = np.arange(0, n_trial_baseline_no_fb, n_trials_to_repeat_inst)
        instruct_baseline_no_fb = np.empty(
            shape=(n_trial_baseline_no_fb,), dtype=object
        )
        instruct_baseline_no_fb[inst_inds] = instruct_phase["baseline_no_fb"]
    else:
        instruct_baseline_no_fb = []

    if n_trial_baseline_continuous_fb > 0:
        inst_inds = np.arange(
            0, n_trial_baseline_continuous_fb, n_trials_to_repeat_inst
        )
        instruct_baseline_continuous_fb = np.empty(
            shape=(n_trial_baseline_continuous_fb,), dtype=object
        )
        instruct_baseline_continuous_fb[inst_inds] = instruct_phase[
            "baseline_continuous_fb"
        ]
    else:
        instruct_baseline_continuous_fb = []

    if n_trial_baseline_endpoint_fb > 0:
        inst_inds = np.arange(0, n_trial_baseline_endpoint_fb, n_trials_to_repeat_inst)
        instruct_baseline_endpoint_fb = np.empty(
            shape=(n_trial_baseline_endpoint_fb,), dtype=object
        )
        instruct_baseline_endpoint_fb[inst_inds] = instruct_phase[
            "baseline_endpoint_fb"
        ]
    else:
        instruct_baseline_endpoint_fb = []

    if n_trial_baseline_mixed_fb > 0:
        inst_inds = np.arange(0, n_trial_baseline_mixed_fb, n_trials_to_repeat_inst)
        instruct_baseline_mixed_fb = np.empty(
            shape=(n_trial_baseline_mixed_fb,), dtype=object
        )
        instruct_baseline_mixed_fb[inst_inds] = instruct_phase["baseline_mixed_fb"]
    else:
        instruct_baseline_mixed_fb = []

    if n_trial_adapt > 0:
        inst_inds = np.arange(0, n_trial_adapt, n_trials_to_repeat_inst)
        instruct_adapt = np.empty(shape=(n_trial_adapt,), dtype=object)
        instruct_adapt[inst_inds] = instruct_phase["adapt"]
    else:
        instruct_adapt = []

    if n_trial_generalisation > 0:
        inst_inds = np.arange(0, n_trial_generalisation, n_trials_to_repeat_inst)
        instruct_generalisation = np.empty(
            shape=(n_trial_generalisation,), dtype=object
        )
        instruct_generalisation[inst_inds] = instruct_phase["generalisation"]
    else:
        instruct_generalisation = []

    if n_trial_washout_no_fb > 0:
        inst_inds = np.arange(0, n_trial_washout_no_fb, n_trials_to_repeat_inst)
        instruct_washout_no_fb = np.empty(shape=(n_trial_washout_no_fb,), dtype=object)
        instruct_washout_no_fb[inst_inds] = instruct_phase["washout_no_fb"]
    else:
        instruct_washout_no_fb = []

    if n_trial_washout_fb > 0:
        inst_inds = np.arange(0, n_trial_washout_fb, n_trials_to_repeat_inst)
        instruct_washout_fb = np.empty(shape=(n_trial_washout_fb,), dtype=object)
        instruct_washout_fb[inst_inds] = instruct_phase["washout_fb"]
    else:
        instruct_washout_fb = []

    # Combine each phase-specific array defined above into a larger array that
    # can later be added to the config dataframe.
    instruct_phase = np.concatenate(
        (
            instruct_baseline_no_fb,
            instruct_baseline_continuous_fb,
            instruct_baseline_endpoint_fb,
            instruct_baseline_mixed_fb,
            instruct_adapt,
            instruct_generalisation,
            instruct_washout_no_fb,
            instruct_washout_fb,
        )
    )

    # The experiment code also defines instructions that are displayed for
    # every state. The following is an indicator column that should be used to
    # switch them on or off.
    instruct_state = 0 * np.ones(instruct_phase.shape)

    # Continuous cursor feedback
    cursor_vis = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            1 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.ones(n_trial_baseline_mixed_fb),
            0 * np.ones(n_trial_adapt),
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # midpoint feedback
    midpoint_vis = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            0 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.ones(n_trial_baseline_mixed_fb),
            1 * np.ones(n_trial_adapt),
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # endpoint feedback
    endpoint_vis = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            0 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.random.permutation([0, 1] * (n_trial_baseline_mixed_fb // 2)),
            0 * np.ones(n_trial_adapt),
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # continuous cursor cloud standard deviation
    cursor_sig = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            0 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.ones(n_trial_baseline_mixed_fb),
            0 * np.ones(n_trial_adapt),
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # midpoint cursor cloud standard deviation
    cursor_mp_sig = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            0 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.ones(n_trial_baseline_mixed_fb),
            1 * sig_mp[np.random.randint(0, 4, n_trial_adapt)],
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # endpoint cursor cloud standard deviation
    cursor_ep_sig = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            0 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.ones(n_trial_baseline_mixed_fb),
            0 * np.ones(n_trial_adapt),
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # whether or not cursor feedback of any kind is clamped
    clamp = np.concatenate(
        (
            0 * np.ones(n_trial_baseline_no_fb),
            0 * np.ones(n_trial_baseline_continuous_fb),
            0 * np.ones(n_trial_baseline_endpoint_fb),
            0 * np.ones(n_trial_baseline_mixed_fb),
            0 * np.ones(n_trial_adapt),
            0 * np.ones(n_trial_generalisation),
            0 * np.ones(n_trial_washout_no_fb),
            0 * np.ones(n_trial_washout_fb),
        )
    )

    # cursor rotation
    rot = np.concatenate(
        (
            np.random.normal(0, rot_sig, n_trial_baseline_no_fb),
            np.random.normal(0, rot_sig, n_trial_baseline_continuous_fb),
            np.random.normal(0, rot_sig, n_trial_baseline_endpoint_fb),
            np.random.normal(0, rot_sig, n_trial_baseline_mixed_fb),
            np.random.normal(rot_mean, rot_sig, n_trial_adapt),
            np.random.normal(rot_mean, rot_sig, n_trial_generalisation),
            np.random.normal(0, rot_sig, n_trial_washout_no_fb),
            np.random.normal(0, rot_sig, n_trial_washout_fb),
        )
    )

    # Construct the config dataframe
    d = pd.DataFrame(
        {
            "condition": conditions[i],
            "subject": i,
            "trial": trial,
            "phase": phase,
            "cycle_phase": cycle_phase,
            "target_angle": target_angle,
            "cursor_vis": cursor_vis,
            "midpoint_vis": midpoint_vis,
            "endpoint_vis": endpoint_vis,
            "cursor_sig": cursor_sig,
            "cursor_mp_sig": cursor_mp_sig,
            "cursor_ep_sig": cursor_ep_sig,
            "clamp": clamp,
            "rot": rot,
            "instruct_phase": instruct_phase,
            "instruct_state": instruct_state,
        }
    )

    # Randomise target order within each phase and cycle_phase
    d["target_angle"] = (
        d.groupby(["phase", "cycle_phase"])["target_angle"]
        .sample(frac=1)
        .reset_index(drop=True)
    )

    # Turn on endpoint feedback for training target during the generalisation
    # phase
    d.loc[
        (d["phase"] == "generalisation") & (d["target_angle"] == target_train),
        "endpoint_vis",
    ] = 1

    # NOTE: plot design
    nn = [
        n_trial_baseline_no_fb,
        n_trial_baseline_continuous_fb,
        n_trial_baseline_endpoint_fb,
        n_trial_baseline_mixed_fb,
        n_trial_adapt,
        n_trial_generalisation,
        n_trial_washout_no_fb,
        n_trial_washout_fb,
    ]
    labels = np.concatenate(
        (
            ["baseline_no_fb"] if n_trial_baseline_no_fb != 0 else [""],
            ["baseline_continuous_fb"] if n_trial_baseline_continuous_fb != 0 else [""],
            ["baseline_endpoint_fb"] if n_trial_baseline_endpoint_fb != 0 else [""],
            ["baseline_mixed_fb"] if n_trial_baseline_mixed_fb != 0 else [""],
            ["adapt"] if n_trial_adapt != 0 else [""],
            ["generalisation"] if n_trial_generalisation != 0 else [""],
            ["washout_no_fb"] if n_trial_washout_no_fb != 0 else [""],
            ["washout_fb"] if n_trial_washout_fb != 0 else [""],
        )
    )
    labels_x = np.concatenate(([0], np.cumsum(nn)[:-1]))
    fig, ax = plt.subplots(1, 1, squeeze=False)
    ax[0, 0].scatter(
        trial, rot, c=d["target_angle"], alpha=d["endpoint_vis"] * 0.5 + 0.25
    )
    ax[0, 0].vlines(labels_x, np.min(rot), np.max(rot), "k", "--")
    for j in range(len(labels)):
        ax[0, 0].text(labels_x[j], np.max(rot) + 1, labels[j], rotation=30)
    ax[0, 0].set_ylabel("Rotation (degrees)")
    ax[0, 0].set_xlabel("Trial")
    ax[0, 0].set_xticks(np.arange(0, n_trial + 1, 20))
    plt.show()

    dd = d[
        [
            "condition",
            "subject",
            "trial",
            "phase",
            "cycle_phase",
            "target_angle",
            "cursor_vis",
            "midpoint_vis",
            "endpoint_vis",
            "cursor_sig",
            "cursor_mp_sig",
            "cursor_ep_sig",
            "clamp",
            "rot",
            "instruct_phase",
            "instruct_state",
        ]
    ]
    dd.plot(subplots=True, layout=(4, 4))
    plt.show()

    d.to_csv("../config/config_reach_" + str(i) + ".csv", index=False)
