# porta serial
SERIAL_PORT = "COM4"

# mapeamento de pinos
FINGER_PINS = {
    "polegar": 10,
    "indicador": 9,
    "medio": 8,
    "anelar": 7,
    "minimo": 6,
}

# ângulos dos servos (graus) — ajuste com `python -m tools.calibrate`
SERVO_ANGLES = {
    10: {"aberto": 0, "pouco": 90,  "meio": 130, "fechado": 150},  # polegar
    9:  {"aberto": 0, "pouco": 90,  "meio": 130, "fechado": 180},  # indicador
    8:  {"aberto": 0, "pouco": 110, "meio": 120, "fechado": 160},  # medio
    7:  {"aberto": 0, "pouco": 70,  "meio": 100, "fechado": 160},  # anelar
    6:  {"aberto": 0, "pouco": 90,  "meio": 130, "fechado": 160},  # minimo
}

# timing (segundos)
SERVO_STEP_DELAY = 0.015
FINGER_TRANSITION_DELAY = 0.02
POSE_SETTLE_DELAY = 0.05
SPELL_START_DELAY = 0.3
SPELL_LETTER_DELAY = 0.8
SPELL_SPACE_DELAY = 0.5
OPEN_HAND_DELAY = 0.3
SERVO_TEST_DELAY = 0.6

# reconhecimento de voz
VOICE_LANGUAGE = "pt-BR"
VOICE_ENERGY_THRESHOLD = 150
VOICE_PAUSE_THRESHOLD = 0.8
VOICE_LISTEN_TIMEOUT = 8
VOICE_PHRASE_TIME_LIMIT = 8
VOICE_CALIBRATION_DURATION = 1.0

# câmera
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAM_SKIP_FRAMES = 3
CAM_HYSTERESIS = 3
CAM_PUSH_INTERVAL = 0.033