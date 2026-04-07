---
title: OPM Sensor
slug: opm-sensor
category: sense
aliases: [Optically Pumped Magnetometer, OPM]
parents: []
related: [opm-meg, magnetic-shielding]
level: advanced
status: draft
---

# Optically Pumped Magnetometer (OPM)

An OPM is a quantum magnetometer that measures magnetic field strength
through the interaction of polarized light with an alkali vapor. Modern
miniaturized OPMs achieve sub-15 fT/√Hz sensitivity at room temperature
and have enabled wearable [[opm-meg]] systems.

## How it works

1. A small glass cell contains an **atomic vapour** — most commercial
   SERF OPMs use **rubidium-87** or **caesium-133** (alkali atoms),
   heated to roughly 150 °C to provide sufficient atom density. A
   minority of designs use **helium-4** instead, which can run at room
   temperature (e.g. MAG4Health).
2. A **circularly polarized pump laser** (resonant with the D1 transition)
   spin-polarizes the alkali atoms along the laser axis.
3. An external magnetic field causes the atomic spins to precess, which
   reduces the effective polarization.
4. A **probe beam** (or modulated pump-only scheme) measures the change in
   absorption or polarization rotation, which is proportional to the field
   strength along a chosen axis.

Operating in the **spin-exchange relaxation-free (SERF) regime** — only
possible at very low residual magnetic fields and high atom densities —
suppresses the dominant noise source (spin-exchange collisions) and yields
the best sensitivity.

## Strengths

- **Sensitivity** comparable to SQUIDs (~7–15 fT/√Hz for commercial
  units; lab prototypes have reached <1 fT/√Hz).
- **No cryogenics** — operates near room temperature.
- **Compact**: cm-scale sensor heads, suitable for dense on-scalp arrays.
- **Multi-axis** measurement: many designs report two or three orthogonal
  field components per sensor.

## Limitations

- **Narrow dynamic range** (~±5 nT for SERF OPMs); sensors saturate
  outside a magnetically shielded environment.
- **Limited bandwidth** (~0–150 Hz for SERF designs).
- **Heating power** and **laser stability** add complexity and cost.
- **Cross-talk** when sensors are placed close together.
- **Calibration drift** with temperature and aging of the vapor cell.

## Sensor manufacturers (illustrative, non-exhaustive)

- **QuSpin** (US) — alkali (Rb) SERF OPMs (QZFM)
- **FieldLine** (US) — alkali SERF OPMs (HEDscan / smart sensors)
- **MAG4Health** (France) — helium-4 OPMs, room-temperature
- **Twinleaf** (US) — research-grade alkali OPMs / gradiometers
- **Cerca Magnetics** (UK) — turnkey OPM-MEG systems integrating
  third-party sensors (rather than a sensor manufacturer)

## See also

- [[opm-meg]]
- [[magnetic-shielding]]

## Sources

- [Wikipedia: SERF (atomic physics)](https://en.wikipedia.org/wiki/SERF)
- [Wikipedia: Atomic magnetometer](https://en.wikipedia.org/wiki/Atomic_magnetometer)
- [Allred, Lyman, Kornack & Romalis 2002, PRL: SERF magnetometer](https://doi.org/10.1103/PhysRevLett.89.130801)
- [Brookes et al. 2022, PMC: OPM interference suppression review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8803550/)
- [QuSpin technology page](https://quspin.com/technology/)
- [MAG4Health 4He OPM product page](https://www.mag4health.com/product/)
