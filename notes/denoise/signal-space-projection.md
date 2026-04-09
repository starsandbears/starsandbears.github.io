---
title: Signal Space Projection
slug: signal-space-projection
category: denoise
aliases: [SSP]
parents: []
related: [meg, eeg, ica, maxwell-filtering]
level: intermediate
status: draft
---

# Signal Space Projection (SSP)

SSP is a linear denoising method for [[meg]] and [[eeg]] that removes
**known artifact subspaces** by orthogonal projection.

## Why we need it

Many artifacts in MEG/EEG — heartbeat, eye blinks, line noise — are
stereotyped: they reproduce the same spatial topography across sensors
every time they occur. Once you have characterized that topography
from a reference channel (ECG, EOG) or a few example epochs, there is
no reason to refit it trial by trial. SSP encodes it as a **static
linear projector** that is applied cheaply to every sample, making it
the method of choice when you need **fast, deterministic, online**
denoising — for example, in real-time BCI pipelines or streaming
dashboards — and do not want the labeling overhead of [[ica]].

## How it works

1. **Identify** the spatial pattern of an artifact using reference data
   (e.g. simultaneously recorded ECG or EOG, or epochs aligned to eye
   blinks / heartbeats).
2. Compute the dominant directions of this pattern in sensor space — for
   example, by taking the top eigenvectors of the artifact covariance.
3. **Project the data onto the orthogonal complement** of those directions,
   removing the artifact subspace from every subsequent sample.
4. Apply the same projection consistently to forward models for source
   localization.

## Strengths

- **Fast and simple** — a static linear projection at each sample.
- **Deterministic**: no manual labeling of components.
- Suitable for **online / real-time** denoising.
- Effective for stereotyped, well-characterized artifacts.

## Limitations

- Removes a **fixed subspace**, which also removes any brain signal that
  happens to lie in that subspace — every projection reduces the
  effective rank of the data.
- Less flexible than [[ica]] for arbitrary artifact patterns.
- **Reference signals (ECG, EOG)** are usually needed to robustly
  identify artifact directions.
- Each additional projection further reduces the rank, which can become
  limiting if many SSPs are stacked.

## Comparison with other denoising methods

- **vs [[ica]]**: SSP is faster and deterministic but less flexible. ICA
  can pick up artifact patterns that SSP would miss, at the cost of
  manual or automated labeling.
- **vs [[maxwell-filtering|SSS]]**: SSP targets specific artifact subspaces;
  SSS removes a whole class of external interference via a physical model.
  SSS is more powerful for environmental noise; SSP is more targeted.

## See also

- [[ica]]
- [[maxwell-filtering]]
- [[meg]]
- [[eeg]]

## Sources

- [Uusitalo & Ilmoniemi 1997, Med. Biol. Eng. Comput. 35:135–140: Signal-space projection method](https://doi.org/10.1007/BF02534144)
- [Tesche et al. 1995, EEG Clin. Neurophysiol.: SSP characterization of MEG sources](https://doi.org/10.1016/0013-4694(95)00064-6)
- [MNE-Python: Background on projectors and projections](https://mne.tools/stable/auto_tutorials/preprocessing/45_projectors_background.html)
- [MNE-Python: Repairing artifacts with SSP](https://mne.tools/stable/auto_tutorials/preprocessing/50_artifact_correction_ssp.html)
