# MQ Honours 2023

## vma general
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

- `instruct`: The instructions given on each trial.

## Dhruva
Dhruva is working on an experiment to followup Hewitson et al. (2023). There, we
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

- Condition 1: low volatility
- Condition 2: high volatility

## Laura
Laura is working on a project examining whether or not MIS training transfers to
enhanced visuomotor adaptation abilities.

- Condition 1: ???
- Condition 2: ???
- Condition 3: ???
