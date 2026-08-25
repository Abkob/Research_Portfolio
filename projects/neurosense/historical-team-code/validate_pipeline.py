from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from feature_extraction import FEATURE_COUNT, FEATURE_NAMES, extract_features
from predict import load_pipeline, predict_updrs_from_wav


ARTIFACT_DIR = Path(__file__).resolve().parent
DATASET_PATH = ARTIFACT_DIR / "parkinsons_updrs.data"
MODEL_PATH = ARTIFACT_DIR / "tf_model.h5"
SCALER_PATH = ARTIFACT_DIR / "scaler.pkl"
SMOKE_WAV_PATH = ARTIFACT_DIR / "_synthetic_validation.wav"

REQUIRED_DATASET_COLUMNS = [
    "total_UPDRS",
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
    "NHR",
    "HNR",
]


def _build_synthetic_wav(target_path: Path, sample_rate: int = 16000, seconds: float = 2.0) -> Path:
    t = np.linspace(0, seconds, int(sample_rate * seconds), endpoint=False)

    # A lightly modulated voiced-like tone gives parselmouth a more realistic signal
    # than a perfectly pure sine wave and avoids NaN-heavy smoke tests.
    freq = 170 + 6 * np.sin(2 * math.pi * 2.1 * t)
    phase = 2 * math.pi * np.cumsum(freq) / sample_rate
    amplitude = 0.35 + 0.07 * np.sin(2 * math.pi * 3.7 * t)

    signal = (
        amplitude * np.sin(phase)
        + 0.12 * np.sin(2 * phase)
        + 0.04 * np.sin(3 * phase)
        + 0.003 * np.random.default_rng(42).normal(size=t.shape[0])
    )

    pcm = np.clip(signal, -1.0, 1.0)
    pcm = (pcm * 32767).astype(np.int16)

    with wave.open(str(target_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm.tobytes())

    return target_path


def validate_dataset(dataset_path: Path = DATASET_PATH) -> dict:
    df = pd.read_csv(dataset_path)
    missing_columns = [col for col in REQUIRED_DATASET_COLUMNS if col not in df.columns]
    if df.shape != (5875, 22):
        raise AssertionError(f"Expected dataset shape (5875, 22), got {df.shape}")
    if missing_columns:
        raise AssertionError(f"Dataset is missing expected columns: {missing_columns}")

    return {
        "dataset_shape": list(df.shape),
        "required_columns_present": True,
    }


def validate_artifacts(
    model_path: Path = MODEL_PATH,
    scaler_path: Path = SCALER_PATH,
) -> dict:
    scaler = joblib.load(scaler_path)
    model = tf.keras.models.load_model(model_path)

    if not hasattr(scaler, "mean_"):
        raise AssertionError("Loaded scaler is not fitted.")
    if tuple(scaler.mean_.shape) != (FEATURE_COUNT,):
        raise AssertionError(
            f"Expected scaler mean shape ({FEATURE_COUNT},), got {scaler.mean_.shape}"
        )
    if model.input_shape != (None, FEATURE_COUNT):
        raise AssertionError(
            f"Expected model input shape (None, {FEATURE_COUNT}), got {model.input_shape}"
        )
    if model.output_shape != (None, 1):
        raise AssertionError(f"Expected model output shape (None, 1), got {model.output_shape}")

    return {
        "scaler_mean_shape": list(scaler.mean_.shape),
        "model_input_shape": list(model.input_shape),
        "model_output_shape": list(model.output_shape),
    }


def validate_mae(
    dataset_path: Path = DATASET_PATH,
    model_path: Path = MODEL_PATH,
    scaler_path: Path = SCALER_PATH,
    random_state: int = 42,
) -> dict:
    df = pd.read_csv(dataset_path)
    df = df.loc[:, "total_UPDRS":"HNR"].copy()
    df = df.drop(columns=["NHR"])

    X = df.loc[:, FEATURE_NAMES]
    y = df["total_UPDRS"]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.33,
        random_state=random_state,
    )

    scaler = joblib.load(scaler_path)
    model = tf.keras.models.load_model(model_path)

    preds = model.predict(scaler.transform(X_test), verbose=0).reshape(-1)
    mae = float(mean_absolute_error(y_test, preds))
    if mae >= 15:
        raise AssertionError(f"MAE {mae:.4f} is too high; scaler/model mismatch likely.")

    return {
        "random_state": random_state,
        "test_mae": mae,
        "test_rows": int(len(X_test)),
    }


def validate_predict_smoke() -> dict:
    model, scaler = load_pipeline()

    wav_path = SMOKE_WAV_PATH
    try:
        _build_synthetic_wav(wav_path)

        features = np.asarray(extract_features(wav_path), dtype=float)
        if features.shape != (FEATURE_COUNT,):
            raise AssertionError(f"Expected feature shape ({FEATURE_COUNT},), got {features.shape}")
        if not np.isfinite(features).all():
            raise AssertionError("Synthetic WAV produced NaN/inf features.")

        score = predict_updrs_from_wav(str(wav_path), model=model, scaler=scaler)
        if not isinstance(score, float):
            raise AssertionError(f"Expected float prediction, got {type(score)}")
        if not math.isfinite(score):
            raise AssertionError("Prediction is not finite.")
    finally:
        if wav_path.exists():
            wav_path.unlink()

    return {
        "feature_count": int(features.shape[0]),
        "prediction": score,
    }


def run_all_checks(include_smoke: bool = True) -> dict:
    results = {
        "dataset": validate_dataset(),
        "artifacts": validate_artifacts(),
        "mae": validate_mae(),
    }
    if include_smoke:
        results["smoke_test"] = validate_predict_smoke()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the UPDRS inference pipeline.")
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="Skip the synthetic WAV end-to-end smoke test.",
    )
    args = parser.parse_args()

    results = run_all_checks(include_smoke=not args.skip_smoke)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
