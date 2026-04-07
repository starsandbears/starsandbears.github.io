---
title: Magnetic Shielding
slug: magnetic-shielding
category: sense
aliases: [Magnetically Shielded Room, MSR]
parents: []
related: [meg, opm-meg, squid-meg]
level: intermediate
status: draft
---

# Magnetic Shielding for MEG

Bio-magnetic signals from the brain are roughly 10 fT–10 pT, while the
ambient magnetic environment of a typical urban building includes the
**Earth's field (~50 μT)**, mains hum, vehicles, elevators, and other
sources that are many orders of magnitude larger. Some form of magnetic
shielding is therefore an essential prerequisite for [[meg]].

## Approaches

### Passive shielding

A **magnetically shielded room (MSR)** is built from multiple nested
layers of high-permeability **mu-metal** (a nickel-iron alloy) and often
an inner layer of high-conductivity **aluminium** for eddy-current
attenuation of higher-frequency noise.

- Two-layer rooms achieve ~40 dB attenuation at low frequencies.
- Three- to four-layer rooms can exceed 80–100 dB.
- High-end research MSRs (e.g. **BMSR-2** at PTB Berlin, with seven
  mu-metal layers plus an aluminium eddy-current layer) reach a passive
  shielding factor on the order of 10⁶–10⁷ at low frequencies — roughly
  120–140 dB — which was a world record at the time of its 2004
  commissioning.

### Active shielding

**Compensation coils** wrapped around the room or sensor array generate
fields that cancel residual ambient fields. Feedback is driven by
reference magnetometers or, increasingly, by the OPMs themselves.

For [[opm-meg]], active nulling is critical because OPM sensors saturate
outside a narrow operating range (~±5 nT).

### Combined / lightweight rooms

OPM-MEG has motivated research into **lighter, cheaper shielded
environments** that combine modest passive shielding with strong active
compensation, lowering the cost barrier compared to a full clinical MSR.

## Strengths

- Essential and well-understood; the **enabling infrastructure** of MEG.
- High-performance MSRs can isolate fT-level brain signals from urban
  magnetic backgrounds.

## Limitations

- **Cost**: a clinical MSR ranges from roughly $0.5M to $2M+ installed.
- **Footprint**: rooms are heavy (tonnes of mu-metal) and require
  structural reinforcement.
- **Site-dependent performance**: nearby trains, machinery, and even
  passing trucks can degrade MEG quality.
- Passive shielding does **not** attenuate vibrations or seismic noise,
  which still couple into sensor readings.
- Mu-metal **degrades over time** if exposed to mechanical shock and may
  need periodic re-annealing.

## See also

- [[meg]]
- [[opm-meg]]
- [[squid-meg]]
- [[homogeneous-field-correction]]

## Sources

- [Wikipedia: Magnetoencephalography](https://en.wikipedia.org/wiki/Magnetoencephalography)
- [Bork et al. 2001: The 8-layered magnetically shielded room of the PTB (BMSR-2 design paper, PDF)](https://www.ptb.de/cms/fileadmin/internet/fachabteilungen/abteilung_8/8.2_biosignale/8.21/mssr.pdf)
- [PTB: Berlin Magnetically Shielded Room overview](https://www.ptb.de/cms/en/research-development/innovation-and-technology-transfer/large-scale-equipment/schluesseleinrichtungen-einzelansicht.html)
- [Brookes et al. 2022, PMC: OPM-MEG interference review (active shielding)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8803550/)
