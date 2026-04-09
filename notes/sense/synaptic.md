---
title: Synaptic Activity
slug: synaptic
category: sense
aliases: [synapse, post-synaptic potential, PSP, synaptic current]
parents: []
related: [eeg, meg]
level: beginner
status: draft
---

# Synaptic Activity

A synapse is the junction where one neuron communicates with another.
"Synaptic activity" refers to the ionic currents and voltage changes that
occur when neurotransmitter release at a presynaptic terminal opens
receptor-gated channels on the postsynaptic membrane. These graded,
relatively slow (~10–100 ms) currents — rather than the fast action
potentials of individual axons — are the dominant source of the
extracranial signals measured by non-invasive neuroimaging.

## Why it matters for BCI

Both [[eeg]] and [[meg]] are driven almost entirely by the **summed
post-synaptic currents of cortical pyramidal neurons**, not by action
potentials:

- Action potentials are brief (~1 ms) and asynchronous across a
  population, so their contributions cancel out at the scalp.
- Post-synaptic potentials are longer-lasting and tend to be synchronized
  across neighboring neurons receiving common input, so their dipolar
  fields add constructively and become detectable outside the head.
- Cortical pyramidal cells are aligned perpendicular to the cortical
  surface, giving the population an open-field geometry that projects a
  measurable dipole to the sensors.

Understanding this is load-bearing for BCI design: it explains why EEG/MEG
reflect **synchronous input to a region** rather than its spiking output,
why spatial resolution is fundamentally limited (many small dipoles sum
into one large one), and why signals are strongest over sulcal walls
(tangential sources) for MEG and gyral crowns (radial sources) for EEG.

## Excitatory vs. inhibitory synapses

- **EPSPs** (excitatory post-synaptic potentials) depolarize the
  postsynaptic neuron, typically via glutamate opening AMPA/NMDA
  receptors.
- **IPSPs** (inhibitory post-synaptic potentials) hyperpolarize it,
  typically via GABA opening Cl⁻ or K⁺ channels.

Both produce extracellular current flow and therefore contribute to EEG
and MEG signals. The net dipole at any moment is the vector sum of
thousands of EPSPs and IPSPs across the local population.

## Temporal and spatial scale

| Scale        | Approx value                                   |
|--------------|------------------------------------------------|
| Duration     | 10–100 ms (vs. ~1 ms for an action potential)  |
| Amplitude    | A few mV at the membrane                       |
| Cells needed | 10,000+ synchronously active pyramidal neurons |
| Area needed  | ~1–10 cm² of cortex for a detectable M/EEG signal |

## See also

- [[eeg]]
- [[meg]]

## Sources

- [Wikipedia: Postsynaptic potential](https://en.wikipedia.org/wiki/Postsynaptic_potential)
- [Wikipedia: Synapse](https://en.wikipedia.org/wiki/Synapse)
- [Buzsáki et al. 2012, Nature Reviews Neuroscience — The origin of extracellular fields and currents](https://www.nature.com/articles/nrn3241)
- [Hämäläinen et al. 1993, Rev. Mod. Phys. (MEG review)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.65.413)
