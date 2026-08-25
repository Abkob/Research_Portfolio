# Vision-guided movement through rubble

## Stage

Literature and system-architecture map. No deployed navigation claim.

## Question

How can a robot or UAV guide movement through rubble and rough terrain using cameras, with graceful options both when a prior map exists and when it does not?

## Evidence tracks

| Track | Representative methods |
|---|---|
| Search and rescue | Vision-based UAV navigation, semantic RGB-D SLAM |
| Traversability | BADGR, GANav, WayFAST, fast visual traversability estimation |
| Depth without LiDAR | RAFT-Stereo, IGEV-Stereo, UniDepth, Depth Anything V2 |
| Prior map | HF-Net hierarchical localization, ViKiNG geographic hints |
| No prior map | ORB-SLAM3, DROID-SLAM, RECON, ViNG |
| Evaluation | RUGD and RELLIS-3D rough-terrain datasets |

## Candidate architecture

```text
stereo / monocular images
          |
          +--> depth or geometric reconstruction
          +--> semantic terrain segmentation
          +--> visual odometry / localization
                         |
                         v
             traversability cost map
                         |
                         v
               risk-aware local planner
```

With a prior map, hierarchical visual localization can constrain the search and use geographic hints. Without one, visual SLAM and exploration must build a local representation online. In both cases, the navigation layer should retain an explicit unknown/unsafe state instead of forcing every pixel into a traversable class.

## Evaluation priorities

- Patient/operator safety and conservative stopping behavior
- Depth and localization failure under dust, blur, smoke, darkness, and repeated textures
- Traversability errors on unstable, deformable, or discontinuous surfaces
- Domain shift between benchmark terrain and real disaster scenes
- Latency, energy use, and compute limits on the target robot

## Source boundary

The local archive contains a structured set of primary papers and dataset links. Copyrighted PDFs are not redistributed here. Public-safe archive notes are preserved as:

- [Dataset and benchmark links](06_Datasets_and_Benchmarks__DATASET_DOWNLOAD_LINKS.txt)
- [SAR-Nets access note](01_Rubble_and_Search_Rescue__2023_Salas_Espinales_SAR_Nets_ACCESS_NOTE.txt)
- [Rough-terrain DRL access note](01_Rubble_and_Search_Rescue__2023_Matsuo_Rough_Terrain_DRL_ACCESS_NOTE.txt)
