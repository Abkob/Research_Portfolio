# Brain-tumor segmentation experiment log

## Status

**Exploratory reproduction and ensemble-design study — code not republished pending provenance/license clarification.**

## Research question

Can several segmentation views—U-Net variants, watershed-assisted masks, focal-loss training, test-time augmentation, pseudo-labeling, and a learned ensemble—be organized into a more robust brain-tumor segmentation workflow?

## Archive inventory

The Drive archive contained notebooks for:

- a baseline U-Net/watershed workflow;
- focal-loss and test-time-augmentation experiments;
- pseudo-label generation and augmentation;
- multiple training runs; and
- an XGBoost-style ensemble over segmentation outputs.

A Mask R-CNN notebook in the same folder was actually a DeepFashion2 clothing-segmentation study, so it was classified as unrelated and excluded.

## Provenance decision

Several notebooks link back to the public project [Brain Tumor Segmentation and Detection using U-Net and Watershed](https://github.com/Engineer-Ayesha-Shafique/Brain-Tumor-Segmentation-and-Detection-using-UNET-and-Watershed-in-Python). The upstream repository did not show a root license file during this curation pass. Because public availability alone does not grant redistribution rights, the derivative notebooks are not being uploaded as original code.

The ensemble and augmentation work may contain substantial new experimentation, but separating original contributions from inherited cells requires a source-by-source diff and a clear license or permission. Until that is done, this portfolio records the research process without copying the implementation.

## What the study demonstrates

- comparing segmentation architectures and loss functions;
- reasoning about augmentation, pseudo-labeling, and test-time augmentation;
- designing an ensemble over heterogeneous model outputs; and
- recognizing that experiment provenance is part of reproducibility.

## Evidence boundary

- No MRI data, annotations, model weights, or checkpoints are published.
- No performance number is presented because the experiments were not rerun under a locked protocol during curation.
- This is not a clinical segmentation system.
- The source method and inherited code remain credited to their original authors.

## Next valid step

Reimplement the ensemble layer against clearly licensed model interfaces, record exact dataset/split provenance, run repeated patient-level evaluation, and publish only code that is demonstrably original or permissibly licensed.
