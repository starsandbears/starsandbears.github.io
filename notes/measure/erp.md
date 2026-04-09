---
title: Event-Related Potential
slug: erp
category: measure
aliases: [ERP, Evoked Potential]
parents: []
related: [eeg, p300, oddball-paradigm]
level: intermediate
status: draft
---

# Event-Related Potential (ERP)

An ERP is the brain's electrical response to a discrete sensory,
cognitive, or motor event, isolated from ongoing [[eeg]] by averaging
many trials time-locked to the event onset. ERPs matter for BCI
because they are the most reliable way to pull a **categorical,
labeled brain response** out of noisy scalp recordings — P300 spellers
and error-potential monitors are, at their core, ERP classifiers.

## Why we need them

Single-trial EEG is dominated by background rhythms and noise that dwarf
the ~1–20 μV response to a single event. Without time-locked averaging,
the brain's reaction to a specific stimulus is invisible. ERPs solve
this by stacking many trials so that the time-locked response sums
constructively while uncorrelated background noise averages toward zero.
This gives a clean waveform with **known components at known latencies**,
which a classifier can then exploit.

## How to use them in a BCI

1. **Define the event.** Choose a stimulus or action whose timing you
   control precisely (a flash, tone, button press, error signal).
2. **Time-lock and epoch.** Extract fixed-length EEG windows (e.g.
   −200 to +800 ms) around each event onset.
3. **Average (or train a classifier).** For offline analysis, average
   trials per condition. For BCI, train a single-trial classifier
   (LDA, xDAWN, Riemannian) on the epoched data — BCIs cannot wait for
   hundreds of trials to average.
4. **Extract features.** Latency, amplitude, and scalp topography of
   known components (e.g. the [[p300]]) are the standard features.

## Components commonly used in BCI

- **[[p300]] (P3b)** — ~300–500 ms parietal positivity evoked by rare
  task-relevant stimuli. Drives the Farwell–Donchin speller.
- **N200 / N2pc** — ~200 ms negativity reflecting attention and target
  selection.
- **N400** — ~400 ms negativity to semantic violations; used in research
  rather than deployed BCIs.
- **ErrP (error-related potential)** — negativity + later positivity
  when the user observes a mistake; used as a correction signal in
  closed-loop BCIs.

Note: SSVEP and motor-imagery responses are *not* strictly ERPs — they
are oscillatory rather than transient — but the BCI community often
treats them with the same epoch-and-classify pipeline.

## Limitations

- **Requires many trials.** Classifiers need either averaging or
  single-trial methods that are more fragile.
- **Sensitive to attention and fatigue.** Amplitudes drop when users
  disengage.
- **Stimulus timing must be precise.** Jitter smears the averaged
  waveform and blurs latency features.
- **Artifacts align with events.** Blinks or EMG triggered by the
  stimulus itself bleed into the ERP and must be removed ([[ica]], SSP).

## See also

- [[eeg]]
- [[p300]]
- [[oddball-paradigm]]

## Sources

- [Wikipedia: Event-related potential](https://en.wikipedia.org/wiki/Event-related_potential)
- Luck (2014). *An Introduction to the Event-Related Potential Technique* (2nd ed.), MIT Press.
- Blankertz et al. (2011). *Single-trial analysis and classification of ERP components — a tutorial.* NeuroImage 56(2): 814–825.
