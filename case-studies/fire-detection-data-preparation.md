# Fire-detection data-preparation study

## Status

**Small exploratory notebook — documented as a study note, not promoted as a standalone detector.**

## Question

How should COCO-style annotations be inspected and filtered before training an image model on the `fire` category?

## Implemented scope

The archived notebook contains a compact workflow that:

1. opens COCO annotation metadata;
2. resolves the category identifier for `fire`;
3. selects image and annotation records;
4. reads image/mask examples; and
5. sketches Keras image-augmentation setup.

The code is useful as a data-ingestion experiment, but it does not implement or validate a complete detection model.

## Curation decision

The public portfolio keeps this concise case-study record instead of manufacturing a large repository around 43 lines of exploratory code. Raw images, COCO annotations, dataset folders, trained models, and weights are excluded.

## Next valid step

Define the dataset source/license, create train/validation/test splits with near-duplicate checks, implement a reproducible detector baseline, and report class-specific precision/recall plus false-positive behavior on non-fire scenes.
