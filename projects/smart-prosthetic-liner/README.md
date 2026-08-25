# Smart multimodal prosthetic-liner sensing

## Stage

Team research and engineering design study. Source-reported sensor performance has not been claimed as reproduced performance.

## Design objective

Translate evidence on socket-limb interface mechanics and printed sensors into a controlled silicone slab that can test whether pressure, shear, temperature, and humidity sensing can coexist without unacceptable thickness, cross-sensitivity, or encapsulation losses.

## Proposed demonstrator

- Footprint: 56 mm × 55 mm
- Total slab thickness: 5.2 mm
- One four-capacitor normal/biaxial-shear sensor
- Two embedded TMP36 temperature devices
- Four printed resistive temperature sensors
- Four printed capacitive humidity sensors
- Layered silicone carrier and encapsulation architecture

The target is a controlled demonstrator, not yet a complete wearable liner or a clinical risk detector.

## Literature-to-design method

Each source was evaluated against four questions:

1. What variable must be measured at the prosthetic interface?
2. Which sensor geometry is transferable to the slab?
3. What performance was demonstrated by the source itself?
4. What must be revalidated after printing, embedding, wiring, and silicone encapsulation?

## Validation plan

- Calibrate each modality separately before integration.
- Characterize normal/shear decoupling and cross-axis response.
- Measure temperature and humidity sensitivity before and after encapsulation.
- Apply repeated mechanical loading and inspect drift, hysteresis, delamination, and trace damage.
- Test multiplexing, shielding, thermal coupling, and signal separation.
- Build real-time spatial maps only after channel-level calibration is stable.

## Public project artifacts

| Artifact | Description |
|---|---|
| [Team report](reports/smart-liner-team-report.pdf) | 58-page BMEN502 project report covering prototype questions, validation, requirements, bench methods, and individual sections |
| [Evidence-led sensor architecture](reports/evidence-led-sensor-architecture.pdf) | Focused literature-to-engineering review for the multimodal slab |
| [Analysis, design, and fabrication review](reports/analysis-design-fabrication-review.pdf) | Longer working review retained as a research-process artifact |
| [TeX source](source/) | Archival report modules, individual sections, review sources, and references; the final PDF above is the canonical rendered artifact |
| [CAD and PCB artifacts](cad/) | DXF sensor artwork, PCB/Gerber exports, and print masks |
| [Original project renders](assets/) | Slab layout, sensor SVG, and prosthetic-liner concept renders |

## My documented contribution area

The report explicitly labels Q6 as **Individual Assignment — Abdulrahman Kobeissi**. It records my contribution area as printed-sensor CAD and print work, sensor proportions and placement, the 5.2 mm slab and circuit layout, and software for calibration, coordinate mapping, interpolation, and interface-condition visualization. The individual research section also covers comparator systems, materials and printing challenges, sensor physics, integration, mapping, durability, team capability gaps, and the integrated liner architecture.

Other sections are team artifacts. Collaborator source modules are preserved for report provenance and are not claimed as my sole work.

## Boundary

Raw human-subject data, downloaded papers, extracted publisher figures, and unverified performance claims remain outside this repository. Because some figure assets are intentionally excluded, the TeX source is an archival snapshot rather than a self-contained build. CAD and report artifacts document a design/prototyping study; they are not evidence of clinical validation or a production-ready medical device.
