---
title: Maxwell Filtering
slug: maxwell-filtering
category: denoise
aliases: [SSS, tSSS, Signal Space Separation, Temporal Signal Space Separation]
parents: []
related: [meg, squid-meg, signal-space-projection, homogeneous-field-correction, ica]
level: advanced
status: draft
---

# Maxwell Filtering (SSS / tSSS)

Maxwell filtering is a denoising method for [[meg]] data that
decomposes the measured magnetic field into components originating
**inside** versus **outside** the sensor array using a multipole
(spherical harmonic) expansion. Internal components — assumed to be
brain signals — are kept; external components — environmental
interference — are subtracted.

The basic version is **Signal Space Separation (SSS)**. **Spatiotemporal
SSS (tSSS)** adds a temporal extension that further suppresses
interference sources very close to the array (dental work, pacemakers,
vagus nerve stimulators) that the spatial decomposition alone cannot
fully separate. Both are most associated with **Elekta / MEGIN**
[[squid-meg]] systems.

## Why we need it

Cortical magnetic fields at the scalp are on the order of tens to
hundreds of femtotesla, while the ambient magnetic environment of an
urban building (Earth's field, mains hum, traffic, elevators, HVAC)
is many orders of magnitude larger. Even inside a shielded room,
residual external fields swamp the cortical signal. Maxwell filtering
exploits a physical fact no statistical method can: in a source-free
region around the sensor array, the magnetic field can be uniquely
decomposed into a component from sources **inside** an enclosing
sphere (the brain) and a component from sources **outside** (the
environment). This gives a principled way to suppress environmental
noise **without** reference channels or manual labeling, and makes
SSS the standard first-stage denoiser in SQUID-MEG pipelines.

## How it works

1. The magnetic field on a closed surface around the brain can be
   expressed as a series of **spherical harmonics**, with one set of basis
   functions for sources inside the surface and another for sources
   outside.
2. With enough sensors arranged in roughly spherical coverage, the
   recorded field can be projected onto these two orthogonal subspaces.
3. The **outside (external interference) subspace** is discarded; the
   **inside subspace** is reconstructed and used as the cleaned signal.
4. tSSS additionally identifies time-correlated components shared between
   the two subspaces — typically near-but-still-external sources — and
   removes them.

## Strengths

- **Very effective** at suppressing environmental noise (vehicles,
  elevators, mains) without needing reference signals.
- **Physically motivated**: the decomposition is based on Maxwell's
  equations, not statistical assumptions.
- Improves **source localization** accuracy by reducing noise.
- Allows **head-position correction** when combined with continuous
  head-position tracking, supporting limited subject motion in SQUID-MEG.

## Limitations

- Designed for **roughly spherical, closely spaced sensor arrays** — works
  best with the helmet geometries of commercial SQUID-MEG systems.
- **Less suited to [[opm-meg]]**, where arrays may be sparse, custom-fit,
  and non-spherical. Adapted variants (e.g. **Adaptive Multipole Models**,
  **Homogeneous Field Correction**) have been developed for OPM data.
- Computationally heavier than [[signal-space-projection|SSP]].
- tSSS can introduce subtle **signal distortion** if temporal correlation
  windows are mis-tuned.
- The method was historically **patent-protected** and tightly coupled
  to MEGIN's MaxFilter software, though open-source implementations now
  exist (e.g. in **MNE-Python**).

## Comparison with other denoising methods

- **vs [[signal-space-projection|SSP]]**: SSS removes external noise via a
  physics-based decomposition; SSP removes specific artifact subspaces
  identified from reference signals. SSS is more powerful for environmental
  noise; SSP is faster and simpler for stereotyped artifacts.
- **vs [[ica]]**: SSS is deterministic and physical; ICA is statistical
  and requires labeling. Often used together: SSS for environment, ICA
  for physiology.
- **vs [[homogeneous-field-correction]]**: HFC is a much simpler model
  that assumes uniform fields across the array — appropriate for small
  OPM arrays but less powerful than SSS.

## See also

- [[signal-space-projection]]
- [[ica]]
- [[homogeneous-field-correction]]
- [[meg]]
- [[squid-meg]]

## Sources

- [Taulu, Kajola & Simola 2004/2005, Brain Topogr. / J. Appl. Phys.: Signal Space Separation method](https://arxiv.org/abs/physics/0401166)
- [Taulu & Simola 2006, Phys. Med. Biol.: Spatiotemporal SSS (tSSS)](https://pubmed.ncbi.nlm.nih.gov/16552102/)
- [MNE-Python: Signal-space separation (SSS) and Maxwell filtering tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/60_maxwell_filtering_sss.html)
- [Tierney et al. 2021, NeuroImage: HFC for OPM data](https://doi.org/10.1016/j.neuroimage.2021.118484)
