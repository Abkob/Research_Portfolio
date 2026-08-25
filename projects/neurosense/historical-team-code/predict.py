from __future__ import annotations

import argparse
import json
from pathlib import Path

from feature_extraction import FEATURE_COUNT, FEATURE_NAMES, extract_features


ARTIFACT_DIR = Path(__file__).resolve().parent
TRAINING_TARGET_MIN = 7.0
TRAINING_TARGET_MAX = 54.992


def _resolve_artifact_path(default_name: str, override: str | None = None) -> Path:
    if override is not None:
        return Path(override).expanduser().resolve()
    return ARTIFACT_DIR / default_name


def load_pipeline(
    model_path: str | None = None,
    scaler_path: str | None = None,
):
    try:
        import joblib
        import tensorflow as tf
    except ImportError as exc:
        raise ImportError(
            "load_pipeline requires joblib and tensorflow. "
            "Install the runtime dependencies first."
        ) from exc

    resolved_model_path = _resolve_artifact_path("tf_model.h5", model_path)
    resolved_scaler_path = _resolve_artifact_path("scaler.pkl", scaler_path)

    scaler = joblib.load(resolved_scaler_path)
    with tf.keras.utils.custom_object_scope(
        {"GlorotUniform": tf.keras.initializers.GlorotUniform}
    ):
        model = tf.keras.models.load_model(resolved_model_path, compile=False)
    return model, scaler


def predict_updrs_from_wav(
    wav_path: str,
    model=None,
    scaler=None,
) -> float:
    try:
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            "predict_updrs_from_wav requires numpy. Install the runtime dependencies first."
        ) from exc

    if model is None or scaler is None:
        model, scaler = load_pipeline()

    features = extract_features(wav_path)
    return predict_updrs_from_features(features, model=model, scaler=scaler)


def predict_updrs_from_features(
    features,
    model=None,
    scaler=None,
) -> float:
    try:
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            "predict_updrs_from_features requires numpy. Install the runtime dependencies first."
        ) from exc

    if model is None or scaler is None:
        model, scaler = load_pipeline()

    features = np.asarray(features, dtype=float)
    if features.shape != (FEATURE_COUNT,):
        raise ValueError(
            f"Expected {FEATURE_COUNT} extracted features, got shape {features.shape}."
        )
    if not np.isfinite(features).all():
        raise ValueError(
            "Feature extraction produced NaN/inf values. "
            "The input audio may be silent or too noisy."
        )

    unscaled = features.reshape(1, -1)
    scaled = scaler.transform(unscaled)
    prediction = model.predict(scaled, verbose=0)
    return float(prediction[0][0])


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def updrs_to_severity_score(
    estimated_total_updrs: float,
    min_updrs: float = TRAINING_TARGET_MIN,
    max_updrs: float = TRAINING_TARGET_MAX,
) -> int:
    normalized = (estimated_total_updrs - min_updrs) / (max_updrs - min_updrs)
    score = _clamp(normalized * 100.0, 0.0, 100.0)
    return int(round(score))


def severity_label_from_score(severity_score: int) -> str:
    if severity_score <= 25:
        return "Mild"
    if severity_score <= 50:
        return "Moderate"
    if severity_score <= 75:
        return "High"
    return "Very High"


def summary_from_label(severity_label: str) -> str:
    summaries = {
        "Mild": "Voice analysis suggests mild symptom severity. This is a screening-style estimate, not a diagnosis.",
        "Moderate": "Voice analysis suggests moderate symptom severity. This is a screening-style estimate, not a diagnosis.",
        "High": "Voice analysis suggests high symptom severity. This is a screening-style estimate, not a diagnosis.",
        "Very High": "Voice analysis suggests very high symptom severity. This is a screening-style estimate, not a diagnosis.",
    }
    return summaries[severity_label]


def format_app_output(
    estimated_total_updrs: float,
    features: dict[str, float],
) -> dict:
    rounded_updrs = round(float(estimated_total_updrs), 2)
    severity_score = updrs_to_severity_score(rounded_updrs)
    severity_label = severity_label_from_score(severity_score)

    return {
        "patient_view": {
            "severity_score": severity_score,
            "severity_label": severity_label,
            "estimated_total_updrs": rounded_updrs,
            "summary": summary_from_label(severity_label),
        },
        "doctor_report": {
            "estimated_total_updrs": rounded_updrs,
            "features": {name: round(float(value), 6) for name, value in features.items()},
        },
    }


def predict_app_output_from_wav(
    wav_path: str,
    model=None,
    scaler=None,
) -> dict:
    try:
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            "predict_app_output_from_wav requires numpy. Install the runtime dependencies first."
        ) from exc

    if model is None or scaler is None:
        model, scaler = load_pipeline()

    features = extract_features(wav_path)
    if features.shape != (FEATURE_COUNT,):
        raise ValueError(
            f"Expected {FEATURE_COUNT} extracted features, got shape {features.shape}."
        )
    if not np.isfinite(features).all():
        raise ValueError(
            "Feature extraction produced NaN/inf values. "
            "The input audio may be silent or too noisy."
        )

    estimated_total_updrs = predict_updrs_from_features(
        features,
        model=model,
        scaler=scaler,
    )
    feature_map = dict(zip(FEATURE_NAMES, features))
    return format_app_output(estimated_total_updrs, feature_map)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict total_UPDRS from a WAV recording."
    )
    parser.add_argument("wav_path", help="Path to a WAV file")
    parser.add_argument("--model-path", default=None, help="Path to tf_model.h5")
    parser.add_argument("--scaler-path", default=None, help="Path to scaler.pkl")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print only the raw predicted total_UPDRS float.",
    )
    args = parser.parse_args()

    model, scaler = load_pipeline(
        model_path=args.model_path,
        scaler_path=args.scaler_path,
    )
    if args.raw:
        score = predict_updrs_from_wav(args.wav_path, model=model, scaler=scaler)
        print(f"{score:.2f}")
        return

    result = predict_app_output_from_wav(args.wav_path, model=model, scaler=scaler)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
