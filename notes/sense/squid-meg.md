---
title: SQUID-MEG
slug: squid-meg
category: sense
aliases: [SQUID Magnetoencephalography, Cryogenic MEG]
parents: [meg]
related: [opm-meg, magnetic-shielding, maxwell-filtering]
level: advanced
status: draft
---

# SQUID-MEG

SQUID-MEG is the traditional form of [[meg]] in which neuromagnetic
fields are detected by **Superconducting QUantum Interference
Devices** — the most sensitive magnetometers ever built. SQUID arrays
are the clinical and research reference standard for MEG.

## Why we need it

Detecting neuromagnetic signals on the order of tens of femtotesla
requires sensors with noise floors in the low fT/√Hz range, and for
decades SQUIDs were the only technology with that sensitivity. That
sensitivity is why SQUID-MEG became the clinical workhorse for
**presurgical localization of epileptiform activity** and
**functional mapping of eloquent cortex** before neurosurgery —
applications that need both good source localization and millisecond
timing. Any BCI or neuroimaging project with access to a SQUID-MEG
system inherits decades of validated pipelines, normative data, and
clinical credibility that newer modalities like [[opm-meg]] are still
accumulating.

## How it works

SQUIDs exploit two quantum effects — flux quantization and the Josephson
effect — to convert tiny magnetic flux changes into measurable voltage
changes. The sensors only superconduct at extremely low temperatures, so
they are immersed in **liquid helium** (~4 K) inside a thermally insulated
**dewar**. The dewar shape is fixed (a one-size-fits-most adult helmet),
and sensors sit roughly 2–4 cm from the scalp because of the necessary
vacuum gap.

Whole-head systems typically have on the order of **250–300 channels**
(e.g. 248 for 4D/BTi, 275 for CTF, 306 for MEGIN/Elekta Neuromag, where
the 306 comprises 102 magnetometers and 204 planar gradiometers).

## Strengths

- **Very low noise floor** (~2–3 fT/√Hz with modern systems, above ~1 Hz).
- **Wide bandwidth** (DC to >1 kHz).
- **Mature ecosystem**: decades of validated clinical use, normative data,
  and a rich analysis-software stack (MNE, FieldTrip, Brainstorm).
  Clinically established applications include **presurgical localization
  of epileptiform activity** and **functional mapping of eloquent cortex**
  (e.g. somatomotor and language areas) before neurosurgery; MEG carries
  CPT reimbursement codes in the US for these uses.
- Excellent **stability** and reproducibility.

## Limitations

- **Cost**: typical whole-head systems cost several million USD, plus a
  shielded room.
- **Helium consumption**: continuous helium boil-off; supply chain and
  cost have become significant problems as global helium reserves decline.
- **Fixed helmet**: subjects must keep their head still inside the dewar;
  poor fit for **children and infants**.
- **Sensor-to-scalp distance** of ~2–4 cm reduces signal amplitude
  compared to on-scalp [[opm-meg]].
- Requires a **magnetically shielded room** (see [[magnetic-shielding]]).

## Comparison with OPM-MEG

| | SQUID-MEG | OPM-MEG |
|---|---|---|
| Sensor temperature | ~4 K (liquid He) | ~150 °C (vapor cell) |
| Sensor-to-scalp distance | 2–4 cm | mm |
| Dynamic range | Wide | Narrow (~±5 nT) |
| Bandwidth | DC to >1 kHz | ~0–150 Hz |
| Subject motion | None | Limited / supported |
| Cost | Very high | Lower (still expensive) |
| Maturity | Mature | Emerging |
| Clinical validation | Extensive | Early |

## See also

- [[opm-meg]]
- [[meg]]
- [[magnetic-shielding]]
- [[maxwell-filtering]]

## Sources

- [Wikipedia: Magnetoencephalography](https://en.wikipedia.org/wiki/Magnetoencephalography)
- [Wikipedia: SQUID](https://en.wikipedia.org/wiki/SQUID)
- [MEGIN TRIUX neo product page](https://www.megin.com/triux-neo/)
- [Hari & Salmelin 2012, NeuroImage (MEG clinical review)](https://doi.org/10.1016/j.neuroimage.2011.12.074)
