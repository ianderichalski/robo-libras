import queue
import threading
import streamlit as st

_DEFAULTS = {
    "arduino_ok": False,
    "spelling": False,
    "current_pose": None,
    "current_char": "",
    "current_text": "",
    "mic_active": False,
    "last_recognized": "",
    "voice_listener": None,
    "stop_flag": threading.Event(),
    "shared_state": {"char": "", "pose": None, "done": False},
    "cam_active": False,
    "cam_send_servos": True,
    "cam_finger_states": None,
    "cam_hand_detected": False,
    "cam_frame": None,
    "cam_letter": None,
    "cam_confidence": 0.0,
    "cam_stop": threading.Event(),
    "cam_queue": queue.Queue(maxsize=2),
    "voice_delay": 0.8,
    "aula_index": 0,
    "aula_vistos": set(),
    "quiz_char": "",
    "quiz_opcoes": [],
    "quiz_respondido": False,
    "quiz_acerto": False,
    "quiz_acertos": 0,
    "quiz_total": 0,
    "sinal_index": 0,
    "sinal_feitos": set(),
    "sinal_random_char": "",
    "sinal_streak": 0,
    "sinal_acerto_flag": False,
}

def init() -> None:
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default