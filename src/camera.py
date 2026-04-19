import os
import cv2
import numpy as np

from src.config import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT, FINGER_PINS
from src.recognizer import recognize
from src import servo

# caminhos do modelo
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)
_MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
_MODEL_PATH = os.path.join(_MODEL_DIR, "hand_landmarker.task")

_detector = None

def _ensure_model() -> str:
    """Baixa o modelo se não existir e retorna o caminho."""
    if os.path.exists(_MODEL_PATH):
        return _MODEL_PATH

    os.makedirs(_MODEL_DIR, exist_ok=True)
    print("Baixando modelo hand_landmarker.task...")

    import urllib.request
    urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
    print(f"Modelo salvo em {_MODEL_PATH}")
    return _MODEL_PATH

def _get_detector():
    """Cria o HandLandmarker usando a Tasks API."""
    global _detector
    if _detector is not None:
        return _detector

    import mediapipe as mp

    model_path = _ensure_model()
    base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )
    _detector = mp.tasks.vision.HandLandmarker.create_from_options(options)
    return _detector

# desenho dos landmarks
_HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # polegar
    (0, 5), (5, 6), (6, 7), (7, 8),          # indicador
    (0, 9), (9, 10), (10, 11), (11, 12),     # médio
    (0, 13), (13, 14), (14, 15), (15, 16),   # anelar
    (0, 17), (17, 18), (18, 19), (19, 20),   # mínimo
    (5, 9), (9, 13), (13, 17),               # palma
]

def _draw_landmarks(frame, landmarks, h, w):
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    for i, j in _HAND_CONNECTIONS:
        cv2.line(frame, points[i], points[j], (3, 102, 239), 1)

    for pt in points:
        cv2.circle(frame, pt, 3, (3, 102, 239), -1)

# mapeamento landmarks → estado dos dedos
def _flex_level(dist: float, thresholds: tuple[float, float, float]) -> float:
    """
    Converte distância normalizada em 4 níveis discretos.
    thresholds: (aberto, pouco, meio)
    """
    t_aberto, t_pouco, t_meio = thresholds
    if dist >= t_aberto:
        return 0
    elif dist >= t_pouco:
        return 0.33
    elif dist >= t_meio:
        return 0.66
    else:
        return 1

def _landmarks_to_finger_states(landmarks, h: int, w: int) -> dict[str, float]:
    """
    Converte 21 landmarks em estados dos 5 dedos.

    Usa coordenadas normalizadas (0.0–1.0) para que os thresholds sejam
    independentes da resolução do frame.
    """
    lx = [lm.x for lm in landmarks]
    ly = [lm.y for lm in landmarks]

    # Polegar: distância horizontal entre base do mínimo (17) e ponta (4)
    dist_polegar = abs(lx[17] - lx[4])

    # Dedos: diferença vertical entre MCP (base) e ponta
    # Positivo = ponta acima da base = dedo estendido
    dist_indicador = ly[5] - ly[8]
    dist_medio = ly[9] - ly[12]
    dist_anelar = ly[13] - ly[16]
    dist_minimo = ly[17] - ly[20]

    finger_thresh = (0.17, 0.05, -0.02)

    return {
        "polegar":   _flex_level(dist_polegar,   (0.17, 0.10, 0.05)),
        "indicador": _flex_level(dist_indicador, finger_thresh),
        "medio":     _flex_level(dist_medio,     finger_thresh),
        "anelar":    _flex_level(dist_anelar,    finger_thresh),
        "minimo":    _flex_level(dist_minimo,    finger_thresh),
    }

def _landmarks_to_vector(landmarks) -> list[float]:
    ox, oy = landmarks[0].x, landmarks[0].y
    vector = []
    for lm in landmarks:
        vector.extend([lm.x - ox, lm.y - oy])
    return vector

def _send_to_servos(states):
    for name, state in states.items():
        pin = FINGER_PINS.get(name)
        if pin is not None:
            servo.set_finger(pin, state)

# processar um frame (para streamlit)
def process_frame(
    frame_bgr: np.ndarray,
    send_servos: bool = False,
) -> tuple[np.ndarray, dict[str, float] | None, bool, str | None, float]:
    """
    Processa um frame BGR e retorna:
      - frame anotado com landmarks
      - dict dos estados dos dedos (ou None)
      - se mão foi detectada
      - letra LIBRAS reconhecida (ou None se sem mão)
      - confiança do reconhecimento (0.0–1.0)
    """
    import mediapipe as mp

    detector = _get_detector()
    h, w, _ = frame_bgr.shape

    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = detector.detect(mp_image)

    finger_states = None
    hand_detected = False
    letter = None
    confidence = 0.0

    if result.hand_landmarks:
        for landmarks in result.hand_landmarks:
            hand_detected = True
            _draw_landmarks(frame_bgr, landmarks, h, w)
            finger_states = _landmarks_to_finger_states(landmarks, h, w)
            letter, confidence = recognize(finger_states, _landmarks_to_vector(landmarks))
            if send_servos:
                _send_to_servos(finger_states)

    return frame_bgr, finger_states, hand_detected, letter, confidence

# loop cli
def run():
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    print("Modo câmera ativo. Pressione Q para sair.")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue

            annotated, _, _, letter, confidence = process_frame(frame, send_servos=True)
            if letter is not None:
                print(f"[CÂMERA] Letra reconhecida: {letter} ({int(confidence * 100)}%)")

            cv2.imshow("RoboLibras — Câmera", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()