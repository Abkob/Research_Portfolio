# Sparse-camera room reconstruction

## Stage

Literature map and feasibility conclusion. No reconstruction benchmark claim.

## Question

What is technically defensible for reconstructing a static room from fixed surveillance cameras, and when is an initial moving-camera or RGB-D scan necessary?

## Methods reviewed

- Multi-camera NeRF and joint camera calibration
- Transient-object removal for static-scene reconstruction
- Indoor 3D Gaussian Splatting with plane, line, depth, normal, and SDF priors
- Sparse-view NeRF and planar surface reconstruction
- RGB-D Gaussian SLAM for dense initialization
- Hybrid mesh and Gaussian representations for architectural surfaces and objects

Representative systems include MC-NeRF, NeRF-HuGS, IndoorGS, DN-Splatter, AGS-Mesh, GaussianRoom, NerfingMVS, and SplaTAM.

## Practical conclusion

A single stationary monocular CCTV feed does not create new parallax over time and cannot reliably recover a complete room. The most practical workflow is:

1. perform a one-time moving-camera or RGB-D scan for base geometry;
2. calibrate multiple fixed cameras into that coordinate system; and
3. use the fixed views for monitoring, appearance updates, and localized change detection.

If only fixed cameras are available, they need overlapping views, reliable calibration, and preferably depth or strong geometric priors. Generative completion of unseen regions must be labeled as inferred rather than measured geometry.

## Evaluation priorities

- Camera-pose and scale accuracy
- Wall/floor/ceiling plane consistency
- Depth and surface-normal error
- Completeness versus hallucinated geometry
- Robustness to people, shadows, and lighting changes
- Mesh usability for downstream measurement or navigation

## Source boundary

The local archive contains a 13-paper reading order and integrity checksums. This public case study links the conclusion and method families without republishing those PDFs.

- [Archive reading guide](READING_GUIDE.md)
- [Source-archive SHA-256 checksums](SOURCE_ARCHIVE_SHA256SUMS.txt)
