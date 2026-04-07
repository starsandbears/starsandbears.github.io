---
title: MEG
slug: meg
category: sense
aliases: [Magnetoencephalography]
parents: []
related: [eeg, opm-meg, squid-meg, magnetic-shielding]
level: intermediate
status: draft
---

# Magnetoencephalography (MEG)

MEG is a non-invasive functional neuroimaging technique that measures the
extremely weak magnetic fields produced by electrical currents in neurons.
Typical neuromagnetic signals are on the order of 10 fT to a few pT —
roughly a billion times smaller than Earth's geomagnetic field — which makes
MEG one of the most demanding bio-instrumentation problems in clinical
neuroscience.

## How it works

Synchronized post-synaptic currents in cortical pyramidal cells generate
small dipolar magnetic fields that pass through the skull and scalp with
almost no distortion (unlike electric potentials in [[eeg]]). An array of
sensitive magnetometers placed near the head records these fields. Source
localization algorithms then attempt to reconstruct the underlying neural
generators from the measured field topography.

## Strengths

- **Millisecond temporal resolution**, like EEG.
- **Better source localization** than EEG, because magnetic fields are not
  smeared by the conductivity of skull and scalp.
- **Direct measure** of neural activity (no hemodynamic delay as in fMRI).
- Particularly sensitive to **tangential currents** in cortical sulci.

## Limitations

- **Expensive** instrumentation and infrastructure.
- Traditional [[squid-meg]] systems require **cryogenic cooling** and a
  **magnetically shielded room**.
- Subjects must remain still inside a fixed helmet (alleviated by
  [[opm-meg]]).
- Less sensitive to **radial sources** (perpendicular to the scalp).
- Picks up **environmental magnetic noise** (vehicles, elevators, mains
  hum), requiring [[magnetic-shielding]] and software denoising.

## Comparison with EEG

| | MEG | EEG |
|---|---|---|
| Signal | Magnetic fields (fT) | Electric potentials (μV) |
| Spatial resolution | Better (no smearing) | Worse |
| Temporal resolution | ms | ms |
| Cost | Very high | Low |
| Portability | Low (traditional) / Medium (OPM) | High |
| Setup time | Low | Medium |

## See also

- [[opm-meg]]
- [[squid-meg]]
- [[eeg]]
- [[magnetic-shielding]]

## Sources

- [Wikipedia: Magnetoencephalography](https://en.wikipedia.org/wiki/Magnetoencephalography)
- [Wikipedia: SQUID](https://en.wikipedia.org/wiki/SQUID)
- [Hämäläinen et al. 1993, Rev. Mod. Phys. (MEG review)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.65.413)
- [Tierney et al. 2021, NeuroImage](https://doi.org/10.1016/j.neuroimage.2021.118484)
