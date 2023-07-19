# MQ Honours 2023

## generic / all
This project provides a fairly general framework that can be used as a
foundation for visuomotor adaptation experiments. It is written in Python and it
uses the Psychopy libraries.

Through the use of a configuration file it currently allows the specification of
the following experiment factors on a per trial basis:

- `cursor_vis`: whether or not the cursor is visible throught each reach (i.e.,
  continuous feedback).

- `midpoint_vis`: whether or not the cursor is visible at movement midpoint.
  This is redundant if `cursor_vis` is set to a non-zero value.

- `endpoint_vis`: whether or not the cursor is visible at movement endpoint.
  This is redundant if `cursor_vis` is set to a non-zero value.

- `cursor_sig`: The visual blur of the cursor. Set to zero for no blur.

- `cursor_mp_sig`: The visual blur of the cursor at midpoint. Set to zero for no
  blur.

- `cursor_ep_sig`: The visual blur of the cursor at endpoint. Set to zero for no
  blur.

- `clamp`: the angle in degrees that the cursor feeedback is clamped throughout
  the entire reach. Set this to zero to impose no clamp.

- `rot`: the angle in degrees that the cursor is rotated relative to the true
  hand position.

- `target_angle`: The angle of the target relative to the start position.

- `instruct_phase`: The instructions given during the `instructions` phase of
  each trial.

- `instruct_state`: Whether or not instructions are given in each state (which
  themselves are defined in the experiment code, not the config file).

## Dhruva
Dhruva is working on an experiment to follow Hewitson et al. (2023). There, we
found that including midpoint feedback -- and thereby inducing feedback
corrections to an ongoing movement -- lead to soem very bizarre behaviour. In
particular, the effect of sensory uncertainty on adaptation appeared to be
almost entirely independent of error magnitude. One possible explanation for
this rooted in explicit strategy use, and another is rooted in implicit motor
adaptation.

To adjudicate between these possibilities, we will perform an experiment that
attempts to control for explicit strategies by giving explicit instructions to
"Please reach directly to the target. Do not aim off-target in order to get the
cursor to land on-target."

- Condition 1: replication of Hewitson et al. (2023)
- COndition 2: addition of explicit aiming directions.

## Liam
Liam is working on a followup to Sandrine's project. Briefly, he is looking at
adaptation under different perturbation volatilities.

- Condition 1: low volatility (variance)
- Condition 2: high volatility (variance)

single-target block design
generalisation targets: (-45 -30, -15, 0, 15, 30, 45) + (three remaining cardinals + 2 extra) -> 12 targets total
training target: straight ahead
all CCW

400 - 500 reaching trials in total?

familiarisation (no feedback no perturbation): 3 per target X 12 targets -> 36 trials
baseline (continuous feedback no perturbation): 3 per target X 12 targets -> 36 trials
baseline (endpoint feedback no perturbation): 3 per target X 12 targets -> 36 trials
clamp (is what it is): as low as 50 or as high as 200 training trials?
generalisation (no feedback except for top-ups to training targets): 20 per target X 12 targets -> 240 trials?
washout (no feedback again): x per target?

## Laura
Laura is working on a project examining whether or not MIS training transfers to
enhanced visuomotor adaptation abilities.

- Condition 1: camera rotation condition (participants undertake the peg
  transfer task with camera rotation followed by the reaching task)

- Condition 2: no camera rotation (participants undertake the peg transfer task
  at one fixed viewpoint followed by the reaching task)

- Condition 3: no peg transfer task (participants just undertake the reaching
  task)

Each participant will undertake 4 training sessions with target direction in
the reaching task counterbalanced between participants and changed each
training session.

4 trained directions - randomised the sequence such that each participant gets
all 4 targets in random order - limiting explicit strategies.

no fb baseline: 60 (5 trials for each of 12 targets)
fb baseline: 60 (5 trials for each of 12 targets)
adaptation: 120 trials (1 target direction)
generalisation: 240 trials (10 trials to each of the 12 targets - half of each kind)
no fb washout: 60 (5 trials for each of 12 targets)
fb washout: 60 (5 trials for each of 12 targets)
