# Room Reconstruction Papers

Collected for research on reconstructing rooms and static environments from surveillance cameras, sparse fixed-camera networks, 3D Gaussian Splatting (3DGS), Neural Radiance Fields (NeRF), and related geometric reconstruction methods.

## Reading order

1. **EDeRF: Updating Local Scenes and Editing Across Fields for Real-Time Dynamic Reconstruction of Road Scene** - The closest literal fixed-surveillance-camera paper. It targets traffic scenes rather than rooms.
   - Source: https://openaccess.thecvf.com/content/ACCV2024/html/Liang_EDeRF_Updating_Local_Scenes_and_Editing_Across_Fields_for_Real-Time_ACCV_2024_paper.html

2. **MC-NeRF: Multi-Camera Neural Radiance Fields for Multi-Camera Image Acquisition Systems** - Joint NeRF reconstruction and calibration for heterogeneous multi-camera systems.
   - Source: https://arxiv.org/abs/2309.07846
   - Project/code/data: https://in2-viaun.github.io/MC-NeRF/

3. **NeRF-HuGS: Improved Neural Radiance Fields in Non-static Scenes Using Heuristics-Guided Segmentation** - Removes transient people, vehicles, and shadows to reconstruct a static background.
   - Source: https://openaccess.thecvf.com/content/CVPR2024/html/Chen_NeRF-HuGS_Improved_Neural_Radiance_Fields_in_Non-static_Scenes_Using_Heuristics-Guided_CVPR_2024_paper.html

4. **IndoorGS: Geometric Cues Guided Gaussian Splatting for Indoor Scene Reconstruction** - Uses lines, planes, and SfM points to improve indoor structural geometry.
   - Source: https://openaccess.thecvf.com/content/CVPR2025/html/Ruan_IndoorGS_Geometric_Cues_Guided_Gaussian_Splatting_for_Indoor_Scene_Reconstruction_CVPR_2025_paper.html

5. **DN-Splatter: Depth and Normal Priors for Gaussian Splatting and Meshing** - Adds depth and normal constraints for indoor reconstruction and mesh extraction.
   - Source: https://arxiv.org/abs/2403.17822
   - Code: https://github.com/maturk/dn-splatter

6. **AGS-Mesh: Adaptive Gaussian Splatting and Meshing with Geometric Priors for Indoor Room Reconstruction Using Smartphones** - Improves depth, normals, and detailed mesh extraction.
   - Source: https://arxiv.org/abs/2411.19271
   - Code: https://github.com/maturk/dn-splatter

7. **GaussianRoom: Improving 3D Gaussian Splatting with SDF Guidance and Monocular Cues for Indoor Scene Reconstruction** - Combines an SDF with 3DGS to handle textureless walls and detailed surfaces.
   - Source: https://arxiv.org/abs/2405.19671
   - Code: https://github.com/xhd0612/GaussianRoom

8. **Integrating Meshes and 3D Gaussians for Indoor Scene Reconstruction with SAM Mask Guidance** - Represents walls, floors, and ceilings as meshes while using Gaussians for objects.
   - Source: https://arxiv.org/abs/2407.16173

9. **PanoPlane: Plane-Aware Panoramic Completion for Sparse-View Indoor 3D Gaussian Splatting** - A 2026 preprint for extremely sparse indoor views. Unobserved areas are generatively completed, not directly measured.
   - Source: https://arxiv.org/abs/2605.14135

10. **Dense Depth Priors for Neural Radiance Fields from Sparse Input Views** - Whole-room NeRF reconstruction with as few as 18 images.
    - Source: https://openaccess.thecvf.com/content/CVPR2022/html/Roessle_Dense_Depth_Priors_for_Neural_Radiance_Fields_From_Sparse_Input_CVPR_2022_paper.html

11. **NerfingMVS: Guided Optimization of Neural Radiance Fields for Indoor Multi-View Stereo** - Focuses on indoor depth and geometry using SfM and learned depth priors.
    - Source: https://openaccess.thecvf.com/content/ICCV2021/html/Wei_NerfingMVS_Guided_Optimization_of_Neural_Radiance_Fields_for_Indoor_Multi-View_ICCV_2021_paper.html
    - Project/code: https://weiyithu.github.io/NerfingMVS/

12. **Planar Surface Reconstruction From Sparse Views** - Reconstructs dominant indoor planes from two views with unknown camera poses.
    - Source: https://openaccess.thecvf.com/content/ICCV2021/html/Jin_Planar_Surface_Reconstruction_From_Sparse_Views_ICCV_2021_paper.html

13. **SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM** - A strong alternative when a moving RGB-D camera or phone can be used for an initial room scan.
    - Source: https://openaccess.thecvf.com/content/CVPR2024/html/Keetha_SplaTAM_Splat_Track__Map_3D_Gaussians_for_Dense_RGB-D_CVPR_2024_paper.html

## Practical conclusion

A single stationary monocular CCTV feed does not provide new parallax over time, so it cannot reliably recover a complete room. The most practical setup is a one-time moving-camera or RGB-D scan for the base geometry, followed by calibration of multiple fixed surveillance cameras for monitoring and updates. If only fixed cameras are available, they need overlapping fields of view, reliable calibration, and preferably depth or strong geometric priors.

`SHA256SUMS.txt` contains a checksum for every PDF so file integrity can be checked later.
