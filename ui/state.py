import queue
import threading
import streamlit as st

TABS = ["Início", "Aprender", "Praticar", "Sobre"]

_DEFAULTS = {
    "theme": "dark",
    "nav": "Início",
    "page": "Início",
    "arduino_ok": False,
    "arduino_err": None,
    "active_tab": None,
    "active_cam_mode": None,
    "cam_index": 0,
    "cameras_list": None,
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
    "aprender_mode_sel": "Modo Aula",
    "cam_mode_sel": "Siga o Sinal",
    "aula_index": 0,
    "aula_vistos": set(),
    "quiz_char": "",
    "quiz_opcoes": [],
    "quiz_respondido": False,
    "quiz_acerto": False,
    "quiz_escolha": "",
    "quiz_acertos": 0,
    "quiz_erros": 0,
    "quiz_total": 0,
    "sinal_index": 0,
    "sinal_feitos": set(),
    "sinal_random_char": "",
    "sinal_streak": 0,
    "sinal_acerto_flag": False,
    "sinal_ok_until": 0.0,
    "sinal_ok_char": "",
    "sinal_sucesso_total": False,
}

def init() -> None:
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default

def stop_camera() -> None:
    st.session_state.cam_stop.set()
    st.session_state.cam_active = False
    st.session_state.cam_frame = None
    st.session_state.cam_finger_states = None
    st.session_state.cam_hand_detected = False
    st.session_state.cam_letter = None
    st.session_state.cam_confidence = 0.0

def go_to(page: str, mode: str | None = None) -> None:
    st.session_state.nav = page
    st.session_state.page = page
    if mode:
        if page == "Aprender":
            st.session_state.aprender_mode_sel = mode
            st.session_state.pop("aprender_mode_ctrl", None)
        elif page == "Praticar":
            st.session_state.cam_mode_sel = mode
            st.session_state.pop("cam_mode_ctrl", None)