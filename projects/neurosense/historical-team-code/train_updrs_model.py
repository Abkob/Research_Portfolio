from __future__ import annotations

import argparse
from pathlib import Path

from feature_extraction import FEATURE_NAMES


ARTIFACT_DIR = Path(__file__).resolve().parent
TARGET_COLUMN = "total_UPDRS"


def load_training_frame(csv_path: str | Path):
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "load_training_frame requires pandas. Install the training dependencies first."
        ) from exc

    df = pd.read_csv(csv_path)
    df = df.loc[:, "total_UPDRS":"HNR"].copy()
    df = df.drop(columns=["NHR"])

    expected_columns = [TARGET_COLUMN, *FEATURE_NAMES]
    missing_columns = [column for column in expected_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Training dataset is missing expected columns: {missing_columns}")

    return df[expected_columns]


def build_model(input_dim: int):
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise ImportError(
            "build_model requires tensorflow. Install the training dependencies first."
        ) from exc

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=[input_dim]),
            tf.keras.layers.Dense(10, activation=tf.nn.relu),
            tf.keras.layers.Dense(1),
        ]
    )

    optimizer = tf.keras.optimizers.RMSprop(0.001)
    model.compile(
        loss="mean_squared_error",
        optimizer=optimizer,
        metrics=["mean_absolute_error", "mean_squared_error"],
    )
    return model


def train_pipeline(
    csv_path: str | Path = ARTIFACT_DIR / "parkinsons_updrs.data",
    model_path: str | Path = ARTIFACT_DIR / "tf_model.h5",
    scaler_path: str | Path = ARTIFACT_DIR / "scaler.pkl",
    ridge_path: str | Path = ARTIFACT_DIR / "ridge_model.pkl",
    random_state: int = 42,
    test_size: float = 0.33,
    epochs: int = 250,
    batch_size: int = 32,
    validation_split: float = 0.2,
    patience: int = 20,
    ridge_alpha: float = 0.001,
    verbose: int = 0,
):
    try:
        import joblib
        import numpy as np
        import tensorflow as tf
        from sklearn.linear_model import Ridge
        from sklearn.metrics import mean_absolute_error
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
    except ImportError as exc:
        raise ImportError(
            "train_pipeline requires tensorflow, numpy, joblib, and scikit-learn."
        ) from exc

    tf.keras.utils.set_random_seed(random_state)
    np.random.seed(random_state)

    df = load_training_frame(csv_path)
    X = df.loc[:, FEATURE_NAMES]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, scaler_path)

    ridge = Ridge(alpha=ridge_alpha)
    ridge.fit(X_train_scaled, y_train)
    joblib.dump(ridge, ridge_path)

    model = build_model(X_train_scaled.shape[1])
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=patience,
            restore_best_weights=True,
        )
    ]
    model.fit(
        X_train_scaled,
        y_train,
        validation_split=validation_split,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=verbose,
    )
    model.save(model_path)

    predictions = model.predict(X_test_scaled, verbose=0).reshape(-1)
    mae = mean_absolute_error(y_test, predictions)

    return {
        "dataset_shape": tuple(df.shape),
        "feature_count": X_train_scaled.shape[1],
        "test_mae": float(mae),
        "model_path": str(Path(model_path).resolve()),
        "scaler_path": str(Path(scaler_path).resolve()),
        "ridge_path": str(Path(ridge_path).resolve()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train the 12-feature total_UPDRS pipeline and save its artifacts."
    )
    parser.add_argument(
        "--csv-path",
        default=str(ARTIFACT_DIR / "parkinsons_updrs.data"),
        help="Path to parkinsons_updrs.data",
    )
    parser.add_argument("--model-path", default=str(ARTIFACT_DIR / "tf_model.h5"))
    parser.add_argument("--scaler-path", default=str(ARTIFACT_DIR / "scaler.pkl"))
    parser.add_argument("--ridge-path", default=str(ARTIFACT_DIR / "ridge_model.pkl"))
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=250)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--verbose", type=int, default=1)
    args = parser.parse_args()

    metrics = train_pipeline(
        csv_path=args.csv_path,
        model_path=args.model_path,
        scaler_path=args.scaler_path,
        ridge_path=args.ridge_path,
        random_state=args.random_state,
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=args.verbose,
    )

    print("Training complete")
    print(f"Dataset shape: {metrics['dataset_shape']}")
    print(f"Feature count: {metrics['feature_count']}")
    print(f"Test MAE: {metrics['test_mae']:.4f}")
    print(f"Saved model: {metrics['model_path']}")
    print(f"Saved scaler: {metrics['scaler_path']}")
    print(f"Saved ridge model: {metrics['ridge_path']}")


if __name__ == "__main__":
    main()
