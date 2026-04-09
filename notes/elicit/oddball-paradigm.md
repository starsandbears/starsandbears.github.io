---
title: Oddball Paradigm
slug: oddball-paradigm
category: elicit
aliases: [Oddball Task]
parents: []
related: [p300, erp, eeg, bci-speller]
level: beginner
status: draft
---

# Oddball Paradigm

The oddball paradigm is an experimental design in which rare "target"
stimuli are interspersed within a stream of frequent "standard" stimuli,
and the participant's task is to detect or count the targets. It is the
simplest, most reliable way to evoke a measurable, labeled brain
response — and for that reason it is the **foundation of most
stimulus-driven BCIs**.

## Why we need it

BCIs that rely on discrete selections (picking a letter, a direction, a
menu item) need a way to make one stimulus in a set stand out
**neurally** from all the others, so that a classifier can identify
which stimulus the user was attending to. The oddball paradigm is the
textbook solution: by making the target rare and task-relevant, it
reliably elicits a [[p300]] response that is time-locked to the target
and, with enough trials, statistically separable from the non-target
responses. Every
P300-based [[bci-speller]] is an oddball paradigm in disguise.

## How to use it in a BCI

1. **Define target and standards.** Decide which stimuli the user is
   being asked to detect, and make them rare — typically **10–20%** of
   all presentations.
2. **Present rapidly.** Stimuli are shown at **2–8 Hz** (stimulus onset
   asynchrony ~125–500 ms), fast enough to collect many trials per
   minute but slow enough that responses don't overlap destructively.
3. **Randomize.** Target positions must be unpredictable; a predictable
   target attenuates the P300.
4. **Give the user a task.** Silent counting, mental note-taking, or a
   discrete response — the target must be **task-relevant**, not just
   rare. An irrelevant rare stimulus elicits a P3a, not the P3b that BCI
   classifiers rely on.
5. **Epoch and classify.** Extract epochs time-locked to each stimulus
   and train a single-trial classifier to separate target from standard
   epochs.

## Variants

- **Visual oddball** — flashed letters, shapes, or icons. Used in
  matrix spellers.
- **Auditory oddball** — tones or spoken words of different pitch or
  identity. Used for gaze-independent BCIs (patients who cannot fixate).
- **Tactile oddball** — vibrotactile stimulators on different body
  sites. Robust for users with severe visual or attention impairment.
- **Three-stimulus oddball** — adds a rare distractor alongside the
  target to separately evoke P3a (distractor) and P3b (target).

## Limitations

- **Slow** for classification BCIs: reliable detection typically needs
  multiple target presentations to average out noise.
- **Requires sustained attention** — the target has to stay salient to
  the user for the whole session.
- **Habituation** — after many trials the response shrinks; stimulus
  parameters must be varied to keep users engaged.
- **Eye movements** — visual oddball BCIs are often confounded with
  gaze; gaze-independent variants (auditory/tactile) are slower.

## See also

- [[p300]]
- [[erp]]
- [[bci-speller]]

## Sources

- [Wikipedia: Oddball paradigm](https://en.wikipedia.org/wiki/Oddball_paradigm)
- Farwell & Donchin (1988). *Talking off the top of your head: toward a mental prosthesis utilizing event-related brain potentials.* Electroencephalography and Clinical Neurophysiology 70(6): 510–523.
- Polich (2007). *Updating P300: An integrative theory of P3a and P3b.* Clinical Neurophysiology 118(10): 2128–2148.
