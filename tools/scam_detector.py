import logging
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

_MODEL = None
_VECTORIZER = None
_FAILED = False
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "guardian_model_v1.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "vectorizer_v1.pkl"


def _load_artifacts():
    global _MODEL, _VECTORIZER, _FAILED

    if _FAILED:
        return None, None

    if _MODEL is None or _VECTORIZER is None:
        try:
            with MODEL_PATH.open("rb") as model_file:
                _MODEL = pickle.load(model_file)
            with VECTORIZER_PATH.open("rb") as vectorizer_file:
                _VECTORIZER = pickle.load(vectorizer_file)
        except FileNotFoundError:
            logger.warning(
                "Scam detector artifacts missing at %s / %s. Falling back to SAFE.",
                MODEL_PATH,
                VECTORIZER_PATH,
            )
            _FAILED = True
            return None, None
        except Exception as exc:
            logger.exception("Unable to load scam detector artifacts: %s", exc)
            _FAILED = True
            return None, None

    return _MODEL, _VECTORIZER


def detect_scam(message):
    model, vectorizer = _load_artifacts()
    if not model or not vectorizer:
        return "SAFE"

    vec = vectorizer.transform([message])
    prediction = model.predict(vec)[0]

    if prediction == 1:
        return "SCAM"
    return "SAFE"
