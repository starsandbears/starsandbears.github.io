---
title: Motor Imagery
slug: motor-imagery
category: elicit
aliases: [MI, Mental Movement, Imagined Movement]
parents: []
related: [eeg, bci-speller]
level: intermediate
status: draft
---

# Motor Imagery

Motor imagery (MI) is the mental simulation of a movement without any
actual motor output. The imagined movement modulates sensorimotor
rhythms in [[eeg]] — specifically, mu (8–13 Hz) and beta (13–30 Hz)
power drops over contralateral motor cortex — producing an
**event-related desynchronization (ERD)** that a classifier can detect.

## Why we need it

Motor imagery is one of the few BCI control signals that is **voluntary,
asynchronous, and self-paced**. Unlike evoked-response BCIs (P300,
SSVEP), motor imagery doesn't require an external stimulus train: the
user can issue commands whenever they choose, on their own timeline.
This makes it the dominant paradigm for **continuous control** —
cursors, wheelchairs, exoskeletons, robotic arms — especially for users
with intact cognitive function but impaired movement (stroke, spinal
cord injury, ALS).

## How to use it in a BCI

1. **Pick imagery classes.** The standard set is left-hand vs. right-hand
   vs. feet vs. tongue — these produce the most spatially separable ERD
   patterns over primary motor cortex.
2. **Cue the user.** Show a cue (e.g. an arrow) telling the user which
   movement to imagine for a fixed window (typically 2–4 seconds).
3. **Extract spatial filters.** **Common Spatial Patterns (CSP)** is the
   canonical feature extractor: it finds projections that maximize the
   band-power difference between classes.
4. **Classify.** LDA on CSP features is the classical baseline.
   **Riemannian geometry** on covariance matrices has become the
   state-of-the-art for robustness across sessions.
5. **Map to control.** Classifier output drives the application — e.g.
   left vs. right imagery moves a cursor left or right.

## Strengths

- **Self-paced and voluntary** — no stimulus train required.
- **Intuitive for users with motor intent intact** — patients can map
  imagined movements onto device control naturally.
- **Well-supported** by open toolkits (MNE-Python, BCILAB, PyRiemann).

## Limitations

- **User training is heavy.** Reliable MI control typically requires
  hours of practice per user; a non-trivial fraction of users — "BCI
  illiterates" — never achieve reliable control.
- **Low bit rate.** Typically 2–4 classes with multi-second decision
  windows, giving information transfer rates in the low tens of
  bits/min — far slower than stimulus-driven spellers for categorical
  selection.
- **High inter-subject variability.** CSP filters learned on one user
  rarely transfer cleanly to another.
- **Session-to-session drift.** Electrode placement, impedance, and
  user state all shift the ERD topography, so most systems require
  recalibration at the start of each session.
- **Fatigue and concentration sensitive.** ERD strength degrades with
  tiredness or distraction.

## See also

- [[eeg]]
- [[bci-speller]]
- [[erp]]

## Sources

- [Wikipedia: Motor imagery](https://en.wikipedia.org/wiki/Motor_imagery)
- Pfurtscheller & Neuper (2001). *Motor imagery and direct brain-computer communication.* Proc. IEEE 89(7): 1123–1134.
- Blankertz et al. (2008). *Optimizing spatial filters for robust EEG single-trial analysis.* IEEE SPM 25(1): 41–56.
- Barachant et al. (2012). *Multiclass brain-computer interface classification by Riemannian geometry.* IEEE TBME 59(4): 920–928.
