# Ambulatory brain-activity earpiece

## Stage

Evidence map and staged research plan. No diagnostic or product-validation claim.

## Question

Can ear-centered EEG support unobtrusive longitudinal monitoring while an integrated air- or bone-conduction transducer provides controlled auditory stimuli for evoked-response experiments?

## Evidence synthesis

- Ear-EEG can measure electrical activity from electrodes in or around the ear, although signal amplitude and spatial coverage are lower than conventional scalp EEG.
- Prior work supports alpha rhythms and auditory steady-state or event-related responses from ear-centered recordings.
- Small clinical studies support detecting focal/temporal and generalized tonic-clonic seizure activity from ear-centered channels.
- Deep-learning outcome models developed on multichannel clinical scalp EEG motivate methodology, but do not validate autonomous coma, death, or brain-death decisions from an earpiece.

## Proposed system

- Bilateral earpieces with multiple dry or semi-dry sensing electrodes
- Low-noise differential acquisition at an initial 250-500 Hz
- IMU context for motion and jaw artifacts
- Optional PPG/ECG for multimodal confirmation
- Synchronized air- or bone-conduction stimulation markers
- On-device quality/safety checks and heavier inference on a phone or research workstation

## Validation sequence

1. **Benchtop:** input noise, impedance, common-mode rejection, offset range, interference, battery, and temperature.
2. **Healthy volunteers:** simultaneous ear and scalp EEG for alpha modulation, motion, evoked potentials, and auditory steady-state responses.
3. **Epilepsy monitoring:** ethics-approved synchronized ear-EEG and clinical reference EEG with blinded event labels and long negative periods.
4. **Outcome research:** only as an additional ICU research channel, with locked external validation and explicit confound analysis.

## Safety boundary

Sound or vibration is a stimulus, not the sensing mechanism. The device must not independently declare coma, death, or brain death. Early software should remain research-only and abstain when signal quality or confidence is insufficient.

## Archived planning files

- [Detailed research plan](DETAILED_PLAN.md)
- [Original source-archive guide](SOURCE_ARCHIVE.md)
- [Structured source index](SOURCES.csv)
- [I-CARE dataset access notes](I_CARE_DATASET_ACCESS.md)

The archive's downloaded papers are not redistributed here; the source index preserves the evidence trail.

## Selected primary sources

- Kidmose et al. (2013), *A Study of Evoked Potentials From Ear-EEG*, DOI: [10.1109/TBME.2013.2264956](https://doi.org/10.1109/TBME.2013.2264956)
- Mikkelsen et al. (2015), *EEG Recorded from the Ear*, DOI: [10.3389/fnins.2015.00438](https://doi.org/10.3389/fnins.2015.00438)
- Joyner et al. (2024), *Using a standalone ear-EEG device for focal-onset seizure detection*, DOI: [10.1186/s42234-023-00135-0](https://doi.org/10.1186/s42234-023-00135-0)
- Zibrandtsen et al. (2017), ear-EEG comparison with scalp EEG, DOI: [10.1016/j.clinph.2017.09.115](https://doi.org/10.1016/j.clinph.2017.09.115)
- Greer et al. (2023), brain-death/death-by-neurologic-criteria guideline, DOI: [10.1212/WNL.0000000000207740](https://doi.org/10.1212/WNL.0000000000207740)
