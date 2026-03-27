import queue
import time
import threading
import cv2
import streamlit as st

from src import servo
from src.config import CAMERA_WIDTH, CAMERA_HEIGHT, CAM_SKIP_FRAMES, CAM_HYSTERESIS, CAM_PUSH_INTERVAL
from src.speller import spell
from src.voice import VoiceListener

# conexão arduino
def _friendly_serial_error(port, e):
    msg = str(e).lower()
    if "filenotfounderror" in msg or "could not open port" in msg or "o sistema não pode encontrar" in msg:
        return f"❌ Porta **{port}** não encontrada. Verifique o cabo USB e a porta no Gerenciador de Dispositivos."
    if "access is denied" in msg or "permissionerror" in msg:
        return f"❌ Porta **{port}** em uso. Feche o Serial Monitor da IDE Arduino e tente novamente."
    if "serialexception" in msg or "serial" in msg:
        return f"❌ Erro serial em **{port}**. Verifique se o firmware **StandardFirmata** está no Arduino. (`{e}`)"
    return f"❌ Erro ao conectar em **{port}**: `{e}`"

def connect(port: str) -> tuple[bool, str]:
    try:
        servo.connect(port)
        st.session_state.arduino_ok = True
        return True, "Conectado!"
    except Exception as e:
        st.session_state.arduino_ok = False
        return False, _friendly_serial_error(port, e)

def disconnect() -> None:
    try:
        servo.disconnect()
    except Exception:
        pass
    st.session_state.arduino_ok = False

# soletração
def _spell_thread(text: str, delay: float, stop_flag: threading.Event, shared: dict) -> None:
    def on_char(c, p):
        shared["char"] = c
        shared["pose"] = p

    spell(
        text,
        apply_fn=servo.apply_pose,
        rest_fn=servo.open_hand,
        letter_delay=delay,
        should_stop=lambda: stop_flag.is_set(),
        on_char=on_char,
    )
    shared["char"] = ""
    shared["pose"] = None
    shared["done"] = True

def start_spell(text: str, delay: float) -> None:
    if not text.strip():
        return
    if not st.session_state.arduino_ok:
        st.warning("Arduino não conectado.")
        return
    st.session_state.spelling = True
    st.session_state.current_text = text.strip()

    stop_flag = st.session_state.stop_flag
    stop_flag.clear()

    shared = st.session_state.shared_state
    shared["char"] = ""
    shared["pose"] = None
    shared["done"] = False

    threading.Thread(
        target=_spell_thread,
        args=(text.strip(), delay, stop_flag, shared),
        daemon=True,
    ).start()

# voz
def process_voice(delay: float) -> None:
    listener: VoiceListener | None = st.session_state.get("voice_listener")
    if not listener:
        return
    for t, content in listener.poll():
        if t == "text":
            st.session_state.last_recognized = f"Reconhecido: {content}"
            if not st.session_state.spelling:
                start_spell(content, delay)
        elif t == "ready":
            st.session_state.last_recognized = "Microfone pronto — fale algo"
        elif t == "warning":
            st.session_state.last_recognized = f"Aviso: {content}"
        elif t == "error":
            st.session_state.last_recognized = f"Erro: {content}"

# thread da câmera
def camera_thread(send_servos: bool, arduino_ok: bool, stop: threading.Event, q: queue.Queue) -> None:
    import platform
    import mediapipe as mp
    from src.camera import _get_detector, _landmarks_to_finger_states, _send_to_servos, _draw_landmarks

    backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY
    cap = cv2.VideoCapture(0, backend)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    raw_q = queue.Queue(maxsize=2)

    def capture_loop():
        while not stop.is_set():
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            frame = cv2.flip(frame, 1)
            if raw_q.full():
                try:
                    raw_q.get_nowait()
                except queue.Empty:
                    pass
            raw_q.put_nowait(frame)

    capture_thr = threading.Thread(target=capture_loop, daemon=True)
    capture_thr.start()

    skip_frames = CAM_SKIP_FRAMES
    frame_count = 0
    last_finger_states = None
    last_hand_detected = False
    last_landmarks_norm = None

    _HYSTERESIS = CAM_HYSTERESIS
    _pending = {}

    def _apply_hysteresis(raw, confirmed):
        nonlocal _pending
        if confirmed is None:
            _pending = {}
            return raw.copy()
        result = confirmed.copy()
        for dedo, val in raw.items():
            if val == result.get(dedo):
                _pending.pop(dedo, None)
            else:
                cand, cnt = _pending.get(dedo, (val, 0))
                if cand == val:
                    cnt += 1
                else:
                    cand, cnt = val, 1
                if cnt >= _HYSTERESIS:
                    result[dedo] = val
                    _pending.pop(dedo, None)
                else:
                    _pending[dedo] = (cand, cnt)
        return result

    try:
        last_push = 0.0
        while not stop.is_set():
            try:
                frame = raw_q.get(timeout=0.5)
            except queue.Empty:
                continue

            frame_count += 1

            if frame_count % skip_frames == 0:
                small = cv2.resize(frame, (240, 180))
                rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
                mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_small)
                result = _get_detector().detect(mp_img)

                if result.hand_landmarks:
                    last_hand_detected = True
                    last_landmarks_norm = result.hand_landmarks[0]
                    sh, sw = small.shape[:2]
                    raw_states = _landmarks_to_finger_states(last_landmarks_norm, sh, sw)
                    last_finger_states = _apply_hysteresis(raw_states, last_finger_states)
                    if send_servos and arduino_ok:
                        _send_to_servos(last_finger_states)
                else:
                    last_hand_detected = False
                    last_landmarks_norm = None
                    _pending = {}

            annotated = frame.copy()
            if last_hand_detected and last_landmarks_norm is not None:
                fh, fw = annotated.shape[:2]
                _draw_landmarks(annotated, last_landmarks_norm, fh, fw)

            rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

            now = time.time()
            if now - last_push < CAM_PUSH_INTERVAL:
                continue
            last_push = now

            while not q.empty():
                try:
                    q.get_nowait()
                except queue.Empty:
                    break
            q.put_nowait({
                "frame": rgb,
                "finger_states": last_finger_states,
                "hand_detected": last_hand_detected,
            })

    finally:
        stop.set()
        capture_thr.join(timeout=1.0)
        cap.release()