# Parkinson's UPDRS Prediction Pipeline — Build Guide

## What We Have and What Each Notebook Does

### Notebook Roles

| Notebook | Role | Output artifact |
|---|---|---|
| `EDA+model_exploration.ipynb` | Extracts voice features from `.wav`, trains and evaluates multiple models, **saves the deployed model** | `tf_model.h5`, `ridge_model.pkl` |
| `parkinson-telemonitoring-regression-with-keras.ipynb` | Separate, more advanced experiment with 19 features + log transforms + PCA | `model_1.h5` (NOT used in deployment) |
| `deploying_model.ipynb` | Loads `tf_model.h5` + `ridge_model.pkl`, wraps them in a scoring script, registers and deploys to Azure ML ACI | Azure ML web service endpoint |

> **Important**: The model actually deployed is the one from the EDA notebook (12-feature, no PCA), not the telemonitoring training notebook (19-feature + PCA). These are two separate experiments.

---

## Current State of the Pipeline

### What exists

- `parkinsons_updrs.data` — telemonitoring dataset (5875 rows, 22 columns) inside `parkinsons+telemonitoring.zip`
- `EDA+model_exploration.ipynb` — trains the Keras model on 12 voice features extracted from `.wav` using Praat/parselmouth
- `tf_model.h5` — **saved by the EDA notebook** (`model.save('tf_model.h5')` at cell ~1092)
- `ridge_model.pkl` — saved by the EDA notebook (`joblib.dump(ridge, 'ridge_model.pkl')`)

### What is missing

- `scaler.pkl` — the `StandardScaler` fitted during EDA training was **never saved**. This is the single most critical missing artifact. Without it, inference on new `.wav` files will use a different scale than what the model was trained on.

---

## Feature Schema (12 features, in exact order)

These are what `measurePitch()` returns and what the model expects as input columns:

```
Index  Column name       Praat measurement
  0    Jitter(%)         localJitter
  1    Jitter(Abs)       localabsoluteJitter
  2    Jitter:RAP        rapJitter
  3    Jitter:PPQ5       ppq5Jitter
  4    Jitter:DDP        ddpJitter
  5    Shimmer           localShimmer
  6    Shimmer(dB)       localdbShimmer
  7    Shimmer:APQ3      apq3Shimmer
  8    Shimmer:APQ5      aqpq5Shimmer
  9    Shimmer:APQ11     apq11Shimmer
  10   Shimmer:DDA       ddaShimmer
  11   HNR               hnr
```

Note: `NHR` is explicitly **dropped** from the dataset (`df.drop('NHR', axis=1)`). Do not include it.

---

## Target Variable

- `total_UPDRS` — unified Parkinson's severity score (the simple Keras model predicts a single scalar)
- The telemonitoring notebook predicts both `motor_UPDRS` and `total_UPDRS` as a 2-output model, but that model (`model_1.h5`) is not the deployed one.

---

## Step-by-Step: Build the Unified Pipeline

The goal is one clean function:

```python
predict_updrs_from_wav("path/to/recording.wav") -> float
```

---

### Step 1 — Extract and verify the dataset

**Task:** Unzip the data and confirm it loads correctly.

```bash
cd Hackathon_MedSystems
unzip parkinsons+telemonitoring.zip
```

**Checklist:**
- [ ] `parkinsons_updrs.data` exists in the folder
- [ ] `pd.read_csv('parkinsons_updrs.data').shape` returns `(5875, 22)`
- [ ] Columns include: `total_UPDRS`, `Jitter(%)`, `Jitter(Abs)`, `Jitter:RAP`, `Jitter:PPQ5`, `Jitter:DDP`, `Shimmer`, `Shimmer(dB)`, `Shimmer:APQ3`, `Shimmer:APQ5`, `Shimmer:APQ11`, `Shimmer:DDA`, `NHR`, `HNR`

**Test:**
```python
import pandas as pd
df = pd.read_csv('parkinsons_updrs.data')
assert df.shape == (5875, 22), f"Expected (5875,22), got {df.shape}"
required = ['total_UPDRS','Jitter(%)','Jitter(Abs)','Jitter:RAP','Jitter:PPQ5',
            'Jitter:DDP','Shimmer','Shimmer(dB)','Shimmer:APQ3','Shimmer:APQ5',
            'Shimmer:APQ11','Shimmer:DDA','NHR','HNR']
assert all(c in df.columns for c in required), "Missing columns"
print("PASS: dataset OK")
```

---

### Step 2 — Install dependencies

**Task:** Ensure all required packages are available.

```bash
pip install parselmouth scikit-learn tensorflow keras numpy pandas joblib
```

**Checklist:**
- [ ] `import parselmouth` works without error
- [ ] `from parselmouth.praat import call` works
- [ ] `import tensorflow as tf; tf.__version__` prints a version
- [ ] `from sklearn.preprocessing import StandardScaler` works
- [ ] `from sklearn.externals import joblib` works (or `import joblib` for newer sklearn)

**Test:**
```python
import parselmouth
from parselmouth.praat import call
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib
print("PASS: all imports OK")
print("TF version:", tf.__version__)
print("parselmouth version:", parselmouth.__version__)
```

> **Note on joblib import**: In scikit-learn >= 0.23, use `import joblib` directly instead of `from sklearn.externals import joblib`. The EDA notebook uses the old form — update it if you get an ImportError.

---

### Step 3 — Re-run the EDA notebook training section and save the scaler

**Task:** This is the critical missing step. Re-run the training portion of `EDA+model_exploration.ipynb` and save the fitted scaler alongside the model.

In `EDA+model_exploration.ipynb`, find the cell that looks like this:

```python
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)
jack = ss.transform(jack)
```

Immediately after this cell, add and run:

```python
import joblib
joblib.dump(ss, 'scaler.pkl')
print("Scaler saved to scaler.pkl")
```

Then confirm that the model is also saved (cell ~1092 should already do this):

```python
model.save('tf_model.h5')
```

**Checklist:**
- [ ] `scaler.pkl` exists in the folder after running this
- [ ] `tf_model.h5` exists in the folder after running this
- [ ] Both files were produced in the **same notebook run** (same train/test split, same scaler fit)

**Test:**
```python
import joblib
import numpy as np
ss_loaded = joblib.load('scaler.pkl')
# scaler should have 12 feature means and stds
assert hasattr(ss_loaded, 'mean_'), "Scaler not fitted"
assert ss_loaded.mean_.shape == (12,), f"Expected 12 features, got {ss_loaded.mean_.shape}"
print("PASS: scaler has 12 features, is fitted")
print("Feature means:", ss_loaded.mean_)
```

---

### Step 4 — Verify the saved Keras model

**Task:** Load `tf_model.h5` and confirm its input/output shape matches the 12-feature schema.

```python
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform

with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
    tf_model = load_model('tf_model.h5')

tf_model.summary()
```

**Checklist:**
- [ ] Model loads without error
- [ ] `tf_model.input_shape` is `(None, 12)`
- [ ] `tf_model.output_shape` is `(None, 1)`
- [ ] Layer count is 3 Dense layers (10 → 10 → 1, matching `build_model()` in EDA notebook)

**Test:**
```python
assert tf_model.input_shape == (None, 12), f"Expected input (None,12), got {tf_model.input_shape}"
assert tf_model.output_shape == (None, 1), f"Expected output (None,1), got {tf_model.output_shape}"
print("PASS: model shape OK")
```

---

### Step 5 — Implement the `measurePitch` feature extractor

**Task:** Copy the exact function from `EDA+model_exploration.ipynb` into a standalone file `feature_extraction.py`. Do not change parameter values — `f0min=75`, `f0max=400` must match what was used during training.

```python
# feature_extraction.py
import numpy as np
import parselmouth
from parselmouth.praat import call

FEATURE_NAMES = [
    'Jitter(%)', 'Jitter(Abs)', 'Jitter:RAP', 'Jitter:PPQ5', 'Jitter:DDP',
    'Shimmer', 'Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'Shimmer:APQ11',
    'Shimmer:DDA', 'HNR'
]

def extract_features(wav_path, f0min=75, f0max=400):
    sound = parselmouth.Sound(wav_path)
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)

    localJitter          = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter  = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter            = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter           = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter            = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer         = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer       = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer          = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer         = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer         = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer           = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return np.array([
        localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter,
        localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer,
        ddaShimmer, hnr
    ])
```

**Checklist:**
- [ ] File saved as `feature_extraction.py` in the same folder
- [ ] `f0min=75`, `f0max=400` match the EDA notebook exactly
- [ ] Returns a numpy array of shape `(12,)`
- [ ] Feature order matches the table in the Feature Schema section above

**Test** (requires any `.wav` file — even a short one):
```python
from feature_extraction import extract_features, FEATURE_NAMES
import numpy as np

features = extract_features('data/Pd1.wav')  # use any available wav
assert features.shape == (12,), f"Expected (12,), got {features.shape}"
assert not np.any(np.isnan(features)), "NaN values in features — check wav file"
print("PASS: feature extraction returns 12 values")
for name, val in zip(FEATURE_NAMES, features):
    print(f"  {name}: {val:.6f}")
```

---

### Step 6 — Implement the unified inference function

**Task:** Create `predict.py` that ties everything together.

```python
# predict.py
import numpy as np
import joblib
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from feature_extraction import extract_features

def load_pipeline(model_path='tf_model.h5', scaler_path='scaler.pkl'):
    ss = joblib.load(scaler_path)
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model(model_path)
    return model, ss

def predict_updrs_from_wav(wav_path, model=None, scaler=None):
    if model is None or scaler is None:
        model, scaler = load_pipeline()
    features = extract_features(wav_path)          # shape (12,)
    X = features.reshape(1, -1)                    # shape (1, 12)
    X_scaled = scaler.transform(X)                 # apply training scaler
    prediction = model.predict(X_scaled)           # shape (1, 1)
    return float(prediction[0][0])

if __name__ == '__main__':
    import sys
    wav = sys.argv[1] if len(sys.argv) > 1 else 'data/Pd1.wav'
    score = predict_updrs_from_wav(wav)
    print(f"Predicted total_UPDRS: {score:.2f}")
```

**Checklist:**
- [ ] `predict.py` saved in the same folder as `tf_model.h5` and `scaler.pkl`
- [ ] `load_pipeline()` loads both artifacts without error
- [ ] `predict_updrs_from_wav()` accepts a path string, returns a float
- [ ] Output is a single UPDRS score (not a list, not a nested array)

**Test:**
```python
from predict import predict_updrs_from_wav, load_pipeline

model, scaler = load_pipeline()

# shape/type checks
score = predict_updrs_from_wav('data/Pd1.wav', model, scaler)
assert isinstance(score, float), f"Expected float, got {type(score)}"
assert 0 <= score <= 100, f"Score {score} is outside plausible UPDRS range (sanity check)"
print(f"PASS: predicted UPDRS = {score:.2f}")
```

---

### Step 7 — Validate against known training data

**Task:** Run the pipeline on a slice of the training dataset and compare against the model's known MAE from notebook outputs.

The EDA notebook reported MAE of approximately **10.3** on the test set. Your reconstructed pipeline should be in the same ballpark.

```python
import pandas as pd
import numpy as np
import joblib
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load saved artifacts
ss = joblib.load('scaler.pkl')
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
    model = load_model('tf_model.h5')

# Replicate EDA notebook preprocessing exactly
df = pd.read_csv('parkinsons_updrs.data')
df = df.loc[:, 'total_UPDRS':'HNR']
df = df.drop('NHR', axis=1)

X = df.loc[:, 'Jitter(%)':'HNR']
y = df['total_UPDRS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
X_test_scaled = ss.transform(X_test)

preds = model.predict(X_test_scaled).reshape(-1)
mae = mean_absolute_error(y_test, preds)
print(f"Reconstructed MAE: {mae:.2f}")
```

**Checklist:**
- [ ] MAE is within ±2 of the notebook's reported value (~10.3)
- [ ] If MAE is very high (>20), the scaler was probably not saved from the same run as the model — redo Step 3

**Test:**
```python
assert mae < 15, f"MAE {mae:.2f} is too high — scaler/model mismatch likely"
print("PASS: MAE within acceptable range")
```

> **If this test fails**: The scaler was saved from a different run than the model. The only fix is to re-run the full EDA training section in one session and save both `scaler.pkl` and `tf_model.h5` together.

---

### Step 8 — Update `score.py` for deployment (fix the missing scaler)

**Task:** The original `score.py` in `deploying_model.ipynb` had no scaler. Update it to load and apply `scaler.pkl`.

```python
# score.py (corrected)
import tensorflow as tf
import keras
import joblib
from tensorflow.keras import layers
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from azureml.core.model import Model
import numpy as np
import json
import ast

def init():
    global model, scaler
    model_path = Model.get_model_path('tf_model.h5')
    scaler_path = Model.get_model_path('scaler.pkl')

    scaler = joblib.load(scaler_path)
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)['data'][0]
        data = ast.literal_eval(data)
        data = np.array(data).reshape(1, -1)   # shape (1, 12)
        data = scaler.transform(data)           # apply scaler before predict
        result = model.predict(data)
        return result.tolist()
    except Exception as e:
        return str(e)
```

**Checklist:**
- [ ] `scaler.pkl` is registered as an Azure ML model (same as `tf_model.h5`)
- [ ] `init()` loads both model and scaler
- [ ] `run()` applies `scaler.transform()` before `model.predict()`
- [ ] Input to `run()` is raw (unscaled) feature values — client does NOT pre-scale

---

## Final Folder State (what should exist when done)

```
Hackathon_MedSystems/
├── parkinsons_updrs.data          # dataset (unzipped from .zip)
├── tf_model.h5                    # trained Keras model (12 inputs → 1 UPDRS output)
├── scaler.pkl                     # StandardScaler fitted on same training run as tf_model.h5
├── ridge_model.pkl                # Ridge regression alternative (optional)
├── feature_extraction.py          # measurePitch() as a standalone importable module
├── predict.py                     # predict_updrs_from_wav() end-to-end function
├── score.py                       # corrected Azure ML scoring script
├── EDA+model_exploration.ipynb
├── parkinson-telemonitoring-regression-with-keras.ipynb
├── deploying_model.ipynb
└── parkinsons+telemonitoring.zip
```

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| `scaler.pkl` missing from original repo | Pipeline cannot be reconstructed without re-training | Re-run EDA notebook Step 3 once |
| EDA uses a random `train_test_split` with no fixed seed | MAE varies slightly between runs | Add `random_state=42` to the split when re-running |
| `measurePitch()` has no silence/noise guard | Silent or noisy `.wav` files return NaN features | Add `assert not np.any(np.isnan(features))` before predict |
| The telemonitoring notebook (`model_1.h5`) is a better model but not wired up | A more accurate pipeline exists but would need a new feature contract including RPDE, DFA, PPE | Future improvement — would require Octave/MATLAB for those features |
| `deploying_model.ipynb` had `auth_enabled` error | Original deploy code fails; use the corrected `score.py` above | Fixed in Step 8 |
