# Research Portfolio

**A curated index of research questions, evidence maps, implementations, and engineering case studies across biomedical signals, assistive sensing, and computer vision.**

This repository makes the boundary between research stages explicit. Some projects have tested code; others are literature maps or design studies. Raw datasets, patient records, business databases, copyrighted PDFs, and collaborators' unpublished material are not redistributed.

## Portfolio at a glance

| Area | Project | Stage | Public evidence |
|---|---|---|---|
| ECG/EEG | Automated peri-ictal ECG feature extraction | Implemented research software | [ECG_FE_Detector_Interface](https://github.com/Abkob/ECG_FE_Detector_Interface) |
| EEG/ECoG | Patient-aware seizure feature studies | Exploratory implementation | [Research_BCI](https://github.com/Abkob/Research_BCI) |
| Ear-EEG | Ambulatory sensing and stimulation concept | Evidence map and staged research plan | [Case study](case-studies/ear-eeg-research-plan.md) |
| Mobile health / IMU | NeuroSense Parkinson's monitoring | Team design study and clinician-dashboard prototype | [Case study](case-studies/neurosense-parkinsons-monitoring.md) |
| Assistive sensing | Multimodal prosthetic-liner sensor slab | Team design and literature-to-requirements study | [Case study](case-studies/smart-prosthetic-liner.md) |
| Robotics / CV | Vision-guided movement through rubble | Literature and system-architecture map | [Case study](case-studies/rubble-guided-movement.md) |
| 3D vision | Sparse-camera room reconstruction | Literature map and feasibility conclusion | [Case study](case-studies/room-reconstruction.md) |
| Research systems | Evidence-centric project and resource management | Implemented application | [Amina OS](https://github.com/Abkob/Amina) |
| Privacy-first analytics | Local student-record ingestion and semantic matching | Implemented application | [WSP Offline System](https://github.com/Abkob/WSP_automationexcel) |

## Stage vocabulary

- **Evidence map:** sources are organized around a research question; no implementation claim.
- **Design study:** literature is translated into requirements and a proposed validation plan.
- **Exploratory implementation:** code exists, but the evaluation is not a locked external benchmark.
- **Implemented research software:** code, tests, and documentation exist; clinical or deployment validity is still bounded.
- **Validated system:** reserved for a prespecified evaluation on appropriate independent data.

## Research themes

### Biomedical signals

Signal quality comes before inference. My ECG and EEG work emphasizes domain-specific quality masks, patient-aware baselines, leakage-resistant evaluation, and interpretable features before black-box scoring.

### Literature-to-engineering translation

I use literature to define what should be measured, which geometry or method is transferable, what performance is only source-reported, and what must be revalidated in a new material, device, cohort, or site.

### Reproducible systems

Research code should expose its data boundary, configuration, tests, limitations, and claim status. Operational data and copyrighted sources stay outside public Git history.

## Source boundary

See [INVENTORY.md](INVENTORY.md) for what was intentionally included, summarized, linked, or excluded when curating material from local project archives.

## Research identity

[Abdulrahman Kobeissi](https://github.com/Abkob) · [ORCID 0009-0007-3870-4619](https://orcid.org/0009-0007-3870-4619)
