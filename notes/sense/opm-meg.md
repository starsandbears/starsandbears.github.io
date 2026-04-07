---
title: OPM-MEG
slug: opm-meg
category: sense
aliases: [Optically Pumped Magnetometer MEG, Wearable MEG]
parents: [meg]
related: [squid-meg, opm-sensor, magnetic-shielding, homogeneous-field-correction, maxwell-filtering]
level: advanced
status: draft
---

# OPM-MEG

OPM-MEG is [[meg]] performed with **optically pumped magnetometers** instead
of the cryogenic SQUID sensors used in traditional systems. Because OPM
sensors operate at near-body temperature and are millimeter- to centimeter-
scale, they can be mounted in a lightweight helmet placed directly on the
scalp, enabling **wearable, on-scalp MEG** for the first time.

## How it works

Each [[opm-sensor]] contains a small alkali vapor cell (typically rubidium
or caesium) interrogated by a laser. In the presence of a magnetic field,
the spin precession of the alkali atoms changes the optical absorption of
the laser beam, providing a direct measurement of field strength. Modern
OPMs operate in the **spin-exchange relaxation-free (SERF) regime**, which
gives noise floors of roughly 7–15 fT/√Hz — comparable to SQUIDs.

A wearable OPM-MEG helmet typically holds 30–128 sensors a few millimetres
from the scalp.

## Strengths over SQUID-MEG

- **On-scalp placement**: signal amplitude scales steeply with distance,
  so on-scalp OPMs yield substantially higher signal than SQUID arrays
  positioned ~2–4 cm above the head inside a dewar — modelling and
  empirical work report on the order of a **2–5× gain** in cortical signal
  amplitude (with even larger gains in information content when many
  closely spaced sensors are used).
- **No cryogenics**: no liquid helium, no expensive recovery system, lower
  operating cost.
- **Subject motion**: with active field nulling and [[homogeneous-field-correction]],
  subjects can move their heads (and even walk in some setups).
- **Adaptable to head size**: especially valuable for **infants and
  children**, who do not fit adult-sized SQUID dewars.

## Limitations

- **Narrow dynamic range**: open-loop SERF OPMs (e.g. QuSpin QZFM) have a
  linear range of only a few nT (around ±5 nT), so a
  [[magnetic-shielding|shielded environment]] with active field nulling
  is still required. Newer closed-loop sensors (e.g. FieldLine HEDscan)
  extend the operating range substantially (hundreds of nT).
- **Bandwidth** for SERF OPMs is typically a DC-to-~100–150 Hz band,
  narrower than the >1 kHz SQUIDs achieve; closed-loop designs push this
  toward ~300 Hz.
- **Heating**: vapor cells are warmed (often >100 °C), requiring careful
  thermal isolation from the scalp.
- **Cross-talk** between adjacent sensors and **calibration drift** are
  active areas of research.
- The technology is **young**: pipelines, normative data, and clinical
  validation lag behind those for SQUID-MEG.
- A small number of commercial vendors — sensor makers such as **QuSpin**
  (US), **FieldLine** (US) and **MAG4Health** (France, helium-4 based
  rather than alkali-vapour), and turnkey OPM-MEG system integrators such
  as **Cerca Magnetics** (UK) — still maturing.

## Denoising

Because OPM arrays are often non-spherical and sparse, traditional
[[maxwell-filtering|Maxwell filtering (SSS)]] does not directly apply.
[[homogeneous-field-correction]] (HFC) and adaptive multipole models (AMM)
have been developed specifically for OPM geometries.

## See also

- [[squid-meg]]
- [[opm-sensor]]
- [[meg]]
- [[homogeneous-field-correction]]
- [[magnetic-shielding]]

## Sources

- [Boto et al. 2018, Nature: Moving brain imaging towards real-world applications](https://www.nature.com/articles/nature26147)
- [Tierney et al. 2021, NeuroImage 244: Modelling OPM interference as a homogeneous field](https://doi.org/10.1016/j.neuroimage.2021.118484)
- [Brookes et al. 2022, NeuroImage: Interference suppression for OPM-MEG (review)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8803550/)
- [Hill et al. 2020, NeuroImage: Multi-channel whole-head OPM-MEG](https://doi.org/10.1016/j.neuroimage.2020.116995)
- [QuSpin QZFM product page](https://quspin.com/products-qzfm/)
