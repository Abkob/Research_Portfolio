from __future__ import annotations

from os import PathLike


FEATURE_NAMES = [
    "Jitter(%)",
    "Jitter(Abs)",
    "Jitter:RAP",
    "Jitter:PPQ5",
    "Jitter:DDP",
    "Shimmer",
    "Shimmer(dB)",
    "Shimmer:APQ3",
    "Shimmer:APQ5",
    "Shimmer:APQ11",
    "Shimmer:DDA",
    "HNR",
]

FEATURE_COUNT = len(FEATURE_NAMES)


def extract_features(
    wav_path: str | PathLike[str],
    f0min: float = 75,
    f0max: float = 400,
):
    """Extract the 12 deployed Praat/parselmouth voice features from a WAV file."""

    try:
        import numpy as np
        import parselmouth
        from parselmouth.praat import call
    except ImportError as exc:
        raise ImportError(
            "extract_features requires numpy and parselmouth. "
            "Install the runtime dependencies first."
        ) from exc

    sound = parselmouth.Sound(str(wav_path))
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    point_process = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)

    local_jitter = call(
        point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3
    )
    localabsolute_jitter = call(
        point_process, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3
    )
    rap_jitter = call(point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5_jitter = call(
        point_process, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3
    )
    ddp_jitter = call(point_process, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    local_shimmer = call(
        [sound, point_process],
        "Get shimmer (local)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )
    localdb_shimmer = call(
        [sound, point_process],
        "Get shimmer (local_dB)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )
    apq3_shimmer = call(
        [sound, point_process],
        "Get shimmer (apq3)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )
    aqpq5_shimmer = call(
        [sound, point_process],
        "Get shimmer (apq5)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )
    apq11_shimmer = call(
        [sound, point_process],
        "Get shimmer (apq11)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )
    dda_shimmer = call(
        [sound, point_process],
        "Get shimmer (dda)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )

    return np.asarray(
        [
            local_jitter,
            localabsolute_jitter,
            rap_jitter,
            ppq5_jitter,
            ddp_jitter,
            local_shimmer,
            localdb_shimmer,
            apq3_shimmer,
            aqpq5_shimmer,
            apq11_shimmer,
            dda_shimmer,
            hnr,
        ],
        dtype=float,
    )
