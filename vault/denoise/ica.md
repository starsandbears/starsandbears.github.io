---
title: ICA
slug: ica
category: denoise
aliases: [Independent Component Analysis]
parents: []
related: [meg, eeg, signal-space-projection, maxwell-filtering]
level: intermediate
status: draft
---

# Independent Component Analysis (ICA)

ICA is a **blind source separation** technique that decomposes a multi-
channel signal into a set of statistically independent components. In
MEG and [[eeg]] preprocessing it is one of the most widely used tools for
separating brain activity from physiological and environmental artifacts.

## How it works

Given an N-channel recording, ICA finds an N×N unmixing matrix such that
the resulting components are as **statistically independent** as possible
(typically maximizing non-Gaussianity or minimizing mutual information).
Common algorithms include **FastICA**, **Infomax**, **JADE**, and
**AMICA**.

After decomposition, the analyst (or an automated classifier such as
ICLabel or MNE's ICA labeling) identifies components that correspond to
**eye blinks**, **horizontal eye movements**, **heartbeat (ECG)**, **muscle
artifacts**, or **line noise**, and removes them before reconstructing the
cleaned signal.

## Strengths

- **Powerful** for stereotyped artifacts that have consistent topography
  (ocular, cardiac).
- **Does not require reference signals** — though ECG/EOG channels make
  component identification more reliable.
- Many mature open-source implementations (**MNE-Python**, **EEGLAB**,
  **FieldTrip**).
- Works on a single recording without prior training data.

## Limitations

- **Requires labeling** of components — manual review or automated
  classifiers, both imperfect.
- Assumes **statistical independence** of underlying sources, which is
  only approximately true for brain signals.
- Assumes **stationarity** within the analyzed segment.
- The number of recoverable components is bounded by the number of
  channels (and effective rank, which is reduced by previous projections
  such as [[signal-space-projection|SSP]] or [[maxwell-filtering|SSS]]).
- Can **remove brain signal** if applied carelessly or if a brain
  component is misclassified as artifact.
- Sensitive to high-amplitude transient artifacts; pre-cleaning helps.

## Comparison with other denoising methods

- **vs [[signal-space-projection]]**: ICA is more flexible (handles
  arbitrary artifact patterns) but slower and requires labeling. SSP is
  faster, deterministic, and ideal when reference channels are available.
- **vs [[maxwell-filtering]]**: SSS targets external environmental noise
  via a physical model; ICA targets physiological artifacts via
  statistical structure. They are **complementary** and often used
  together (SSS first, then ICA).

## See also

- [[signal-space-projection]]
- [[maxwell-filtering]]
- [[meg]]
- [[eeg]]

## Sources

- [Wikipedia: Independent component analysis](https://en.wikipedia.org/wiki/Independent_component_analysis)
- [Hyvärinen & Oja 2000, Neural Networks: ICA algorithms and applications](https://doi.org/10.1016/S0893-6080(00)00026-5)
- [MNE-Python: Repairing artifacts with ICA tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html)
- [Pion-Tonachini, Kreutz-Delgado & Makeig 2019, NeuroImage: ICLabel](https://doi.org/10.1016/j.neuroimage.2019.05.026)
- [EEGLAB ICA documentation](https://eeglab.org/tutorials/06_RejectArtifacts/RunICA.html)
