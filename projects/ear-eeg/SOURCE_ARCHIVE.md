# Ambulatory Monitoring Brain-Activity Earpiece

Research archive assembled on 2026-08-18 for a concept combining unobtrusive ear-EEG, optional auditory or bone-conduction stimulation, wireless ambulatory monitoring, and machine-learning interpretation.

## What the literature supports

- Electrical brain activity can be recorded from electrodes in or around the ear. The signal is generally smaller and has less spatial coverage than conventional scalp EEG.
- Ear-EEG can capture alpha rhythm and auditory steady-state or event-related responses, including responses generated while sound is delivered through an earpiece.
- Small clinical studies support detection of temporal/focal seizures and generalized tonic-clonic seizures from ear-centered signals.
- Deep-learning models have predicted neurological outcome after cardiac arrest from multichannel clinical scalp EEG, sometimes using auditory stimulation. This is relevant methodology, but it is not proof that a standalone ear device can diagnose coma or predict death.

Vibration or sound is a stimulus, not the sensing mechanism. The sensing mechanism is differential voltage measurement through EEG electrodes. A bone-conduction or air-conduction transducer could provide controlled stimuli while the electrodes measure evoked responses.

## Critical clinical limitation

This archive is for research and product discovery only. An ear-EEG device must not independently declare coma, death, or brain death, and an ML score must not be treated as a diagnosis. The 2023 AAN/AAP/CNS/SCCM guideline requires a defined clinical process for brain-death/death-by-neurologic-criteria determination; EEG and evoked potentials do not assess brainstem function and are not acceptable substitutes for that process.

## Folder guide

### 01_Ear_EEG_Foundations_and_Stimulus

1. Kidmose et al. (2013), *A Study of Evoked Potentials From Ear-EEG*. IEEE Transactions on Biomedical Engineering. DOI: 10.1109/TBME.2013.2264956.
2. Mikkelsen et al. (2015), *EEG Recorded from the Ear: Characterizing the Ear-EEG Method*. Frontiers in Neuroscience. DOI: 10.3389/fnins.2015.00438.
3. Kaveh et al. (2020), *Wireless User-Generic Ear EEG*. IEEE Transactions on Biomedical Circuits and Systems. DOI: 10.1109/TBCAS.2020.3001265.
4. Lee et al. (2026), *Earable Platform with Integrated Simultaneous EEG Sensing and Auditory Stimulation*. arXiv:2604.22137. **Preprint; not peer reviewed.**

### 02_Seizure_Detection

1. Joyner et al. (2024), *Using a standalone ear-EEG device for focal-onset seizure detection*. Bioelectronic Medicine. DOI: 10.1186/s42234-023-00135-0.
2. Zibrandtsen et al. (2017), *Ear-EEG detects ictal and interictal abnormalities in focal and generalized epilepsy - A comparison with scalp EEG monitoring*. Clinical Neurophysiology. DOI: 10.1016/j.clinph.2017.09.115.
3. Zibrandtsen et al. (2018), *Detection of generalized tonic-clonic seizures from ear-EEG based on EMG analysis*. Seizure. DOI: 10.1016/j.seizure.2018.05.001.

### 03_Coma_and_Outcome_ML

1. Aellen et al. (2023), *Auditory stimulation and deep learning predict awakening from coma after cardiac arrest*. Brain. DOI: 10.1093/brain/awac340.
2. Zheng et al. (2022), *Predicting Neurological Outcome From Electroencephalogram Dynamics in Comatose Patients After Cardiac Arrest With Deep Learning*. IEEE Transactions on Biomedical Engineering. DOI: 10.1109/TBME.2021.3139007.
3. Tjepkema-Cloostermans et al. (2019), *Outcome Prediction in Postanoxic Coma With Deep Learning*. Critical Care Medicine. DOI: 10.1097/CCM.0000000000003854.
4. Amorim et al. (2023), *The International Cardiac Arrest Research Consortium Electroencephalography Database*. Critical Care Medicine. DOI: 10.1097/CCM.0000000000006074.

The raw I-CARE dataset is not included because it is approximately 2.63 TB and has separate access terms. See `03_Coma_and_Outcome_ML/I_CARE_DATASET_ACCESS.md`.

### 04_Clinical_Safety_and_Guidelines

1. Greer et al. (2023), *Pediatric and Adult Brain Death/Death by Neurologic Criteria Consensus Guideline*. Neurology. DOI: 10.1212/WNL.0000000000207740.

## Other files

- `plan.md` turns the idea into a staged, safety-conscious research plan.
- `SOURCES.csv` records DOI, status, topic, and source URL for every bundled PDF.
- All 12 PDFs were checked for a valid PDF signature, successful parsing, nonzero page count, and a matching first-page title. SHA-256 values are listed in `SOURCES.csv`.

Licensing remains with each paper's copyright holder. Use the material under the terms shown in each paper and at its source URL.
