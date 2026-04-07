---
title: Homogeneous Field Correction
slug: homogeneous-field-correction
category: denoise
aliases: [HFC]
parents: []
related: [opm-meg, maxwell-filtering, magnetic-shielding]
level: advanced
status: draft
---

# Homogeneous Field Correction (HFC)

HFC is a lightweight denoising technique developed for [[opm-meg]]. It
models the residual environmental magnetic field across the OPM array as
**spatially uniform** (a single 3-component vector) and projects that
component out of the data. Despite its simplicity it is highly effective
because OPM helmets cover a small enough volume that ambient fields are
approximately homogeneous across the sensors. It was introduced by Tierney
et al. (2021, *NeuroImage* 244:118484), who showed that simply removing
this homogeneous component improved sensor-level SNR by roughly a factor
of three in an auditory-evoked-response paradigm.

## How it works

1. At each time point, the field measured by all OPM sensors is fit to a
   uniform (homogeneous) field vector.
2. The projection of each sensor's measurement onto that uniform field is
   subtracted, leaving only the spatially structured (brain) component.
3. Optionally extended to include **first-order spatial gradients** of
   the field, giving a richer model at the cost of removing more
   degrees of freedom.

## Strengths

- **Computationally cheap** — a small linear projection at each sample.
- **Robust to sensor geometry**: unlike [[maxwell-filtering|SSS]], HFC
  does not require a closed spherical sensor arrangement.
- Works well even with **sparse OPM arrays** (a few dozen sensors).
- Allows subjects to make **modest head movements** within a shielded
  environment without saturating the sensors.
- Compatible with downstream source-localization pipelines.

## Limitations

- Removes **only spatially uniform interference**. Higher-order spatial
  structure (e.g. from a person walking past the room) is not fully
  suppressed.
- Implicitly assumes brain signals are **not approximately uniform** —
  generally true for real cortical sources but worth verifying in unusual
  setups.
- **Newer than SSS**, with less validation across vendors and clinical
  conditions.
- Less effective on its own for **strongly inhomogeneous** environments;
  often combined with active field nulling and improved
  [[magnetic-shielding|magnetic shielding]].

## Comparison with Maxwell filtering (SSS)

| | HFC | SSS / tSSS |
|---|---|---|
| Sensor geometry | Any | Roughly spherical |
| Interference model | Uniform field | Multipole expansion |
| Computational cost | Very low | Higher |
| Best for | OPM-MEG | SQUID-MEG |
| Maturity | Recent (2021+) | Mature (2005+) |

## Extensions

- **Adaptive Multipole Models (AMM)** generalize HFC to higher-order
  multipoles, recovering more of the SSS-like power while remaining
  applicable to OPM array geometries.

## See also

- [[opm-meg]]
- [[maxwell-filtering]]
- [[magnetic-shielding]]

## Sources

- [Tierney et al. 2021, NeuroImage 244:118484: Modelling OPM interference as a homogeneous field](https://doi.org/10.1016/j.neuroimage.2021.118484)
- [Brookes et al. 2022, PMC: OPM interference suppression review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8803550/)
- [MNE-Python: OPM data preprocessing tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/80_opm_processing.html)
- [Tierney et al. 2024, NeuroImage: Adaptive Multipole Models for OPM-MEG](https://doi.org/10.1016/j.neuroimage.2024.120454)
