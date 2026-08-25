from __future__ import annotations

import ast
import json
from pathlib import Path

from feature_extraction import FEATURE_NAMES
from predict import format_app_output


ARTIFACT_DIR = Path(__file__).resolve().parent
FEATURE_COUNT = 12
MODEL_NAME = "tf_model.h5"
SCALER_NAME = "scaler.pkl"

_MODEL = None
_SCALER = None


def init():
    global _MODEL, _SCALER

    try:
        import joblib
        import tensorflow as tf
    except ImportError as exc:
        raise ImportError("Scoring init requires tensorflow and joblib.") from exc

    model_path = ARTIFACT_DIR / MODEL_NAME
    scaler_path = ARTIFACT_DIR / SCALER_NAME

    try:
        from azureml.core.model import Model
    except ImportError:
        pass
    else:
        model_path = Model.get_model_path(MODEL_NAME)
        scaler_path = Model.get_model_path(SCALER_NAME)

    _SCALER = joblib.load(scaler_path)
    with tf.keras.utils.custom_object_scope(
        {"GlorotUniform": tf.keras.initializers.GlorotUniform}
    ):
        _MODEL = tf.keras.models.load_model(model_path, compile=False)


def _coerce_request_to_array(raw_data):
    try:
        import numpy as np
    except ImportError as exc:
        raise ImportError("Azure scoring run requires numpy.") from exc

    payload = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    if "data" not in payload or not payload["data"]:
        raise ValueError("Request payload must contain a non-empty 'data' field.")

    sample = payload["data"][0]
    if isinstance(sample, str):
        sample = ast.literal_eval(sample)

    array = np.asarray(sample, dtype=float)
    if array.ndim == 1:
        array = array.reshape(1, -1)

    if array.shape[1] != FEATURE_COUNT:
        raise ValueError(
            f"Expected {FEATURE_COUNT} raw feature values, got shape {array.shape}."
        )

    return array


def run(raw_data):
    try:
        if _MODEL is None or _SCALER is None:
            raise RuntimeError("Model not initialized. Call init() before run().")

        data = _coerce_request_to_array(raw_data)
        scaled = _SCALER.transform(data)
        result = _MODEL.predict(scaled, verbose=0)
        estimated_total_updrs = float(result[0][0])
        feature_map = dict(zip(FEATURE_NAMES, data[0]))
        return format_app_output(estimated_total_updrs, feature_map)
    except Exception as exc:
        return str(exc)
