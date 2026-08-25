# Research Portfolio

A public, project-by-project archive of my research questions, evidence maps, code, reports, presentations, and engineering artifacts.

The folders are intentionally segregated. Authored or team-attributed project work lives under `projects/`; books and course references live in [REFERENCE_LIBRARY.md](REFERENCE_LIBRARY.md); downloaded journal and commercial-book files are not redistributed.

Every project listed below has at least one inspectable public artifact. Authored or clearly team-attributed PDFs are linked when available; publisher PDFs, private data, and internal records are indexed or described rather than re-hosted.

## Biomedical signals and assistive technology

| Project | Stage | Artifacts in this repository |
|---|---|---|
| [Smart multimodal prosthetic liner](projects/smart-prosthetic-liner/) | Team design and literature-to-engineering study | Team report, two review PDFs, TeX sources, CAD/PCB files, original renders |
| [Ear-EEG research plan](projects/ear-eeg/) | Evidence map and staged validation plan | Detailed plan, source index, dataset-access notes |
| [NeuroSense Parkinson's monitoring](projects/neurosense/) | Team digital-health design study | Concept note and classifier-plan PDFs/DOCX, anonymized interface, historical team-code snapshot |
| [ECG feature detector](https://github.com/Abkob/ECG_FE_Detector_Interface) | Implemented research software | Package, tests, notebooks, reports, ECG/EEG literature review |
| [BCI and epilepsy research](https://github.com/Abkob/Research_BCI) | Exploratory implementation | EEG/ECoG notebooks, patient-aware experiments, provenance notes |
| [MotorBrace](https://github.com/Abkob/MotorBrace_BCI_EMG) | Team research prototype | Sanitized notebooks, proposal and mechanical-design reports |

## Computer vision, robotics, and imaging

| Project | Stage | Artifacts in this repository |
|---|---|---|
| [Rubble navigation](projects/rubble-navigation/) | Literature and system-architecture map | Case study, access notes, dataset links |
| [Sparse-camera room reconstruction](projects/room-reconstruction/) | Literature map and feasibility conclusion | Case study, reading guide, source-archive checksums |
| [Brain-tumor segmentation](projects/brain-tumor-segmentation/) | Provenance-bounded reproduction study | Experiment log; unclear-license derivative code excluded |
| [Fire-detection data preparation](projects/fire-detection/) | Small exploratory implementation | Data-preparation case study |
| [AARS Agro-Remediation](https://github.com/Abkob/AARS_Agro_Remediation) | Multidisciplinary prototype research | Segmentation notebooks and selected team reports |

## Research infrastructure

| Project | Stage | Public repository |
|---|---|---|
| Amina OS | Implemented local-first evidence and project system | [Amina](https://github.com/Abkob/Amina) |
| WSP Offline System | Implemented privacy-first local analytics application | [WSP_automationexcel](https://github.com/Abkob/WSP_automationexcel) |

## How to read the stage labels

- **Evidence map:** sources are organized around a research question; no implementation claim.
- **Design study:** literature is translated into requirements and a proposed validation plan.
- **Exploratory implementation:** code exists, but evaluation is not a locked external benchmark.
- **Implemented research software:** code, tests, and documentation exist; clinical or deployment validity remains bounded.
- **Validated system:** reserved for prespecified evaluation on appropriate independent data.

## Repository map

```text
Research_Portfolio/
├── projects/                  # one directory per project
│   ├── smart-prosthetic-liner/
│   ├── ear-eeg/
│   ├── neurosense/
│   ├── rubble-navigation/
│   ├── room-reconstruction/
│   ├── brain-tumor-segmentation/
│   └── fire-detection/
├── REFERENCE_LIBRARY.md       # extracurricular reference catalog
└── INVENTORY.md               # inclusion, attribution, and safety boundary
```

See [INVENTORY.md](INVENTORY.md) for the curation decisions and exclusions.
