import queue
import threading
import cv2
import streamlit as st

from ui.components import render_dedos, render_legend
from ui.actions import camera_thread

def render(tab) -> None:
    with tab:
        col_cam, col_cam_info = st.columns([3, 2], gap="large")

        _render_video(col_cam)
        _render_info(col_cam_info)

def _render_video(col) -> None:
    with col:
        st.markdown('<div class="lbr-section">Câmera — Visão Computacional</div>', unsafe_allow_html=True)
        st.markdown("""<p style='font-size:0.8rem;color:#9A9CB8;margin:0 0 10px'>
            Sua mão é detectada via <strong>MediaPipe Hand Landmarker</strong>. Os estados
            dos dedos são mapeados em tempo real e replicados nos servomotores.
        </p>""", unsafe_allow_html=True)

        cam_send = st.checkbox(
            "Enviar para servos (Arduino)",
            value=st.session_state.cam_send_servos,
            disabled=not st.session_state.arduino_ok,
            key="chk_cam_send",
        )
        if cam_send != st.session_state.cam_send_servos:
            st.session_state.cam_send_servos = cam_send
            if st.session_state.cam_active:
                st.session_state.cam_stop.set()
                st.session_state.cam_active = False
                st.session_state.cam_frame = None
                st.session_state.cam_finger_states = None
                st.session_state.cam_hand_detected = False
                st.session_state.cam_letter = None
                st.session_state.cam_confidence = 0.0
                st.session_state.cam_queue = queue.Queue(maxsize=2)
                st.session_state.cam_stop = threading.Event()
                st.rerun()
        st.session_state.cam_send_servos = cam_send

        if not st.session_state.cam_active:
            if st.button("▶  Iniciar câmera", width='stretch', key="btn_cam_start"):
                st.session_state.cam_active = True
                st.session_state.cam_frame = None
                st.session_state.cam_finger_states = None
                st.session_state.cam_hand_detected = False
                new_stop = threading.Event()
                st.session_state.cam_stop = new_stop
                st.session_state.cam_queue = queue.Queue(maxsize=2)
                threading.Thread(
                    target=camera_thread,
                    args=(cam_send, st.session_state.arduino_ok, new_stop, st.session_state.cam_queue),
                    daemon=True,
                ).start()
                st.rerun()
        else:
            if st.button("⏹  Parar câmera", width='stretch', key="btn_cam_stop"):
                st.session_state.cam_stop.set()
                st.session_state.cam_active = False
                st.session_state.cam_finger_states = None
                st.session_state.cam_hand_detected = False
                st.session_state.cam_letter = None
                st.session_state.cam_confidence = 0.0
                st.session_state.cam_frame = None
                st.rerun()

        if st.session_state.cam_active:
            latest_data = None
            try:
                while True:
                    latest_data = st.session_state.cam_queue.get_nowait()
            except Exception:
                pass

            if latest_data is not None:
                st.session_state.cam_frame = latest_data["frame"]
                st.session_state.cam_finger_states = latest_data["finger_states"]
                st.session_state.cam_hand_detected = latest_data["hand_detected"]
                st.session_state.cam_letter = latest_data["letter"]
                st.session_state.cam_confidence = latest_data["confidence"]

            frame_data = st.session_state.cam_frame
            if frame_data is not None:
                _, jpg_buf = cv2.imencode(
                    ".jpg",
                    cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR),
                    [cv2.IMWRITE_JPEG_QUALITY, 85],
                )
                st.image(jpg_buf.tobytes(), width='stretch')
            else:
                st.markdown("""
                <div class="lbr-card" style="text-align:center; padding: 30px 20px;">
                    <p style="font-size: 0.85rem; color:#8E90A8; letter-spacing:1px;">Inicializando câmera...</p>
                </div>""", unsafe_allow_html=True)

            if st.session_state.cam_hand_detected:
                st.markdown(
                    '<div class="lbr-cam-status detecting"><span class="cam-dot"></span> Mão detectada — replicando movimentos</div>',
                    unsafe_allow_html=True,
                )
                if st.session_state.cam_letter is not None:
                    confidence_pct = int(st.session_state.cam_confidence * 100)
                    st.markdown(
                        f'<div class="lbr-cam-status detecting">Letra reconhecida: <strong>{st.session_state.cam_letter}</strong> — {confidence_pct}% de confiança</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<div class="lbr-cam-status waiting"><span class="cam-dot"></span> Aguardando detecção...</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("""
            <div class="lbr-card" style="text-align:center; padding: 40px 20px;">
                <p style="font-size: 0.85rem; color:#8E90A8;">Clique em <strong>"Iniciar câmera"</strong> para começar a detecção.</p>
            </div>
            """, unsafe_allow_html=True)

def _render_info(col) -> None:
    with col:

        st.markdown('<div class="lbr-section">Estado da Mão (Câmera)</div>', unsafe_allow_html=True)
        cam_states = st.session_state.cam_finger_states
        render_dedos(cam_states if cam_states else None)
        render_legend()

        st.markdown('<div class="lbr-section">Pipeline de Processamento</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lbr-step">
            <div class="lbr-step-num">1</div>
            <div class="lbr-step-text">Webcam captura vídeo a <strong>30 fps</strong>.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">2</div>
            <div class="lbr-step-text"><strong>MediaPipe Hand Landmarker</strong> detecta 21 landmarks da mão.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">3</div>
            <div class="lbr-step-text">Razões de distância determinam o estado de flexão de cada dedo.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">4</div>
            <div class="lbr-step-text">Comandos enviados via <strong>PyFirmata</strong> replicam o gesto na mão robótica.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="lbr-section">Dicas de Uso</div>', unsafe_allow_html=True)
        st.markdown("""<p style='font-size:0.78rem;color:#9A9CB8;line-height:1.8;margin:0'>
            · Mantenha a mão bem iluminada e visível para a câmera.<br>
            · Posicione a palma voltada para a câmera.<br>
            · Movimentos lentos e deliberados dão melhores resultados.<br>
            · Desmarque <em>Enviar para servos</em> para testar sem o Arduino.
        </p>""", unsafe_allow_html=True)