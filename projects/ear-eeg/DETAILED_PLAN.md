# Research plan: ambulatory brain-activity earpiece

## 1. Define the claim narrowly

Start with an earpiece that records ear-EEG continuously and estimates signal quality, physiological rhythms, and predefined events. Treat sound or bone-conduction vibration as an optional controlled stimulus for evoked-response experiments.

Do not begin with a claim that the device detects fatal death, coma, or brain death. Those are high-risk clinical conclusions requiring multimodal hospital assessment. A safer first target is one of:

- long-term focal or generalized seizure screening;
- drowsiness, sleep, or vigilance tracking;
- alpha-rhythm and auditory steady-state response measurement;
- research-only neurological trend monitoring paired with clinical scalp EEG.

## 2. Proposed system

- Two earpieces where possible, because inter-ear channels can provide a larger baseline than within-ear channels.
- Multiple dry or semi-dry electrodes in the concha and ear canal, plus reference/bias electrodes.
- Low-noise, high-input-impedance differential amplifier with input protection and galvanically safe charging/data arrangements.
- Sampling at 250-500 Hz for initial EEG and EMG work, with antialias filtering and synchronized timestamps.
- Inertial measurement unit for motion-artifact context; optional PPG/ECG for multimodal event confirmation.
- Bluetooth Low Energy or another secure wireless link that can transmit raw or minimally processed data to a phone/gateway.
- Optional air-conduction speaker or bone-conduction transducer for calibrated clicks, tones, oddball stimuli, or auditory steady-state response paradigms.
- On-device signal-quality and safety checks; heavier inference on the phone or a clinical research workstation during early development.

## 3. Validation phases

### Phase A: benchtop and electrical safety

- Measure input-referred noise, common-mode rejection, input impedance, electrode offset range, wireless interference, battery life, and thermal behavior.
- Use an EEG signal simulator and ear phantom before human testing.
- Implement charge/current limiting and ensure the stimulus path cannot inject unsafe current into the recording electrodes.

Exit criterion: repeatable signal acquisition without clipping or unsafe electrical/thermal behavior.

### Phase B: healthy-volunteer feasibility

- Record ear-EEG and full scalp EEG simultaneously.
- Test eyes-open/eyes-closed alpha modulation, jaw/motion artifacts, auditory evoked potentials, and 40-Hz auditory steady-state responses.
- Compare SNR, coherence/correlation, test-retest reliability, comfort, fit, and usable wear time.

Exit criterion: prespecified ear-EEG features agree with scalp EEG above a defined threshold in an independent test subset.

### Phase C: first clinical target - seizures

- Conduct an ethics-approved study in an epilepsy monitoring unit with synchronized ear-EEG and clinical scalp or intracranial EEG.
- Obtain event labels from blinded epileptologists and include long non-seizure periods to measure false alarms per day.
- Separate focal temporal, extra-temporal, generalized tonic-clonic, motion-artifact, and poor-contact cases.

Exit criterion: prospective sensitivity and false-alarm targets are met on patients and sites not used for model training.

### Phase D: coma/outcome research only

- Use the earpiece only as an additional channel alongside standard ICU EEG and other clinical measurements.
- Test whether ear signals preserve prognostic features already observed in scalp EEG and auditory-response studies.
- Lock the model before external validation, report calibration and uncertainty, and analyze the effect of sedation, temperature management, artifacts, age, site, and care-withdrawal bias.

Exit criterion: independent multicenter evidence of incremental value over accepted clinical variables. Even then, the output should be decision support, not an autonomous death or brain-death determination.

## 4. ML pipeline

1. Synchronize raw ear-EEG, scalp EEG, stimulus markers, IMU, and optional cardiac signals.
2. Run a signal-quality gate before any clinical inference.
3. Detect clipping, electrode pops, motion, jaw EMG, mains noise, and disconnection.
4. Establish interpretable baselines using spectral power, entropy, rhythmicity, coherence, evoked-response amplitude/latency, and artifact features.
5. Compare those baselines with compact CNN/TCN/transformer models; avoid a complex model unless it improves external validation.
6. Use patient-level and site-level splits to prevent leakage.
7. Calibrate probabilities and allow the model to abstain when signal quality or confidence is insufficient.
8. Report sensitivity, specificity, positive predictive value, false alarms per day, time-to-detection, calibration, subgroup results, and confidence intervals.

## 5. Labels and endpoints

- Seizures: blinded expert consensus using the clinical reference recording.
- Auditory response: stimulus-locked scalp EEG reference plus behavioral/hearing controls where possible.
- Coma/outcome: predefined CPC or mRS time point, neurological examination, EEG background category, sedation/exposure, and center-specific treatment variables.
- Never label "fatal death" directly from ear-EEG. Mortality and brain-death determinations have different mechanisms, confounders, and legal/clinical definitions.

## 6. Safety and regulatory work

- Obtain institutional review board/ethics approval before human experiments.
- Engage a clinical neurophysiologist, ICU neurologist, biomedical engineer, audiologist, biostatistician, and medical-device regulatory specialist.
- Build a risk file covering skin injury, ear-canal pressure, infection, hearing exposure, electrical current, battery failure, data loss, false reassurance, false alarms, automation bias, and cybersecurity.
- Follow applicable medical electrical safety, biocompatibility, usability, software lifecycle, cybersecurity, and clinical-investigation standards for the intended market.
- Keep all early software labeled research-only and prevent an unvalidated model from producing a death/coma declaration.

## 7. Practical first prototype

The fastest evidence-generating prototype is a wired or short-range wireless two-ear research device with four electrodes per ear, IMU, synchronized stimulus markers, and simultaneous scalp EEG. Demonstrate alpha and auditory steady-state responses first, then pursue seizure monitoring. The coma work should come later as a paired ICU research study.
