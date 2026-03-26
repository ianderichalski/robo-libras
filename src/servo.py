import time

from pyfirmata import Arduino, SERVO
from src.config import (
    FINGER_PINS,
    SERVO_ANGLES,
    SERVO_STEP_DELAY,
    FINGER_TRANSITION_DELAY,
    POSE_SETTLE_DELAY,
    OPEN_HAND_DELAY,
    SERVO_TEST_DELAY,
)

# estado do módulo
_board = None
_ALL_PINS = list(FINGER_PINS.values())

# conexão
def connect(port: str) -> Arduino:
    """Abre a porta serial e configura os pinos como SERVO."""
    global _board
    _board = Arduino(port)
    for pin in _ALL_PINS:
        _board.digital[pin].mode = SERVO
    return _board

def disconnect():
    global _board
    if _board is not None:
        try:
            _board.exit()
        except Exception:
            pass
        _board = None

def _require_board():
    if _board is None:
        raise RuntimeError(
            "Arduino não conectado. Chame servo.connect(port) antes de usar."
        )

# controle de baixo nível
def write_angle(pin: int, angle: int) -> None:
    """Escreve um ângulo (0–180) diretamente em um pino servo."""
    _require_board()
    _board.digital[pin].write(max(0, min(180, int(angle))))
    time.sleep(SERVO_STEP_DELAY)

# controle de alto nível
def set_finger(pin: int, position: float) -> None:
    """
    Posiciona um dedo.

    position: 0 (aberto), 0.33 (pouco), 0.66 (meio), 1 (fechado),
              ou qualquer float 0–1 para interpolação linear.
    """
    angles = SERVO_ANGLES[pin]

    if position == 0:
        write_angle(pin, angles["aberto"])
    elif abs(position - 0.33) <= 0.1:
        write_angle(pin, angles["pouco"])
    elif abs(position - 0.66) <= 0.1:
        write_angle(pin, angles["meio"])
    elif position >= 1:
        write_angle(pin, angles["fechado"])
    else:
        interpolated = angles["aberto"] + (angles["fechado"] - angles["aberto"]) * position
        write_angle(pin, int(interpolated))

def apply_pose(pose):
    for name, position in pose.items():
        pin = FINGER_PINS.get(name)
        if pin is not None:
            set_finger(pin, position)
            time.sleep(FINGER_TRANSITION_DELAY)
    time.sleep(POSE_SETTLE_DELAY)

def open_hand():
    _require_board()
    for pin in _ALL_PINS:
        write_angle(pin, SERVO_ANGLES[pin]["aberto"])
    time.sleep(OPEN_HAND_DELAY)

def close_hand():
    _require_board()
    for pin in _ALL_PINS:
        write_angle(pin, SERVO_ANGLES[pin]["fechado"])
    time.sleep(OPEN_HAND_DELAY)

def test_all():
    _require_board()
    for pin in _ALL_PINS:
        for pos in (0, 0.33, 0.66, 1, 0):
            set_finger(pin, pos)
            time.sleep(SERVO_TEST_DELAY)