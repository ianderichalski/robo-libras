import os
import pickle

from src.poses import FINGER_ORDER, POSES

_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "rf_libras.pkl")
_KNN_ONLY = {"0", "1", "2", "3", "4", "5", "H", "J", "K", "X", "Z"}

_model = None

def _load_model():
    global _model
    if _model is not None:
        return
    if not os.path.exists(_MODEL_PATH):
        return
    with open(_MODEL_PATH, "rb") as f:
        _model = pickle.load(f)["model"]

def _knn_recognize(finger_states):
    vector = [finger_states[f] for f in FINGER_ORDER]
    distances = {}
    for char, pose in POSES.items():
        pose_vec = [pose[f] for f in FINGER_ORDER]
        dist = sum((a - b) ** 2 for a, b in zip(vector, pose_vec)) ** 0.5
        distances[char] = dist
    best = min(distances, key=distances.get)
    return best, max(0.0, 1.0 - distances[best])

def recognize(finger_states, landmarks_vector=None):
    """Retorna a letra LIBRAS mais próxima e a confiança (0.0–1.0)."""
    _load_model()

    if _model is None or landmarks_vector is None:
        return _knn_recognize(finger_states)

    probs = _model.predict_proba([landmarks_vector])[0]
    idx = probs.argmax()
    letter = _model.classes_[idx]
    confidence = float(probs[idx])

    if letter in _KNN_ONLY:
        return _knn_recognize(finger_states)

    return letter, confidence

_load_model()