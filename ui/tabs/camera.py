import queue
import threading
import cv2
import streamlit as st
import os
import time
import random

from ui.components import render_dedos, render_legend
from ui.actions import camera_thread

def render(tab) -> None:
    # Injeta a animação do Streak
    st.markdown("""
        <style>
        @keyframes lbr-glow {
            0%, 100% { box-shadow: 0 0 5px rgba(239, 102, 3, 0.2); }
            50% { box-shadow: 0 0 18px rgba(239, 102, 3, 0.55); }
        }
        .streak-glow {
            animation: lbr-glow 1.5s infinite ease-in-out !important;
            border-color: #EF6603 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with tab:
        mode = st.segmented_control(
            "Modo",
            ["Siga o Sinal", "Espelhamento"],
            default="Siga o Sinal",
            label_visibility="collapsed",
        )

        if mode == "Siga o Sinal":
            submodo = st.segmented_control(
                "Submodo",
                ["A → Z", "Aleatório"],
                default="A → Z",
                label_visibility="collapsed",
                key="sinal_submodo",
                disabled=st.session_state.cam_active,
            )
            if st.session_state.cam_active:
                st.caption("Pare a câmera para trocar o modo.")
        else:
            submodo = None

        col_cam, col_cam_info = st.columns([3, 2], gap="large")

        if mode == "Espelhamento":
            _render_video(col_cam)
            _render_info(col_cam_info)
        else:
            _render_siga_sinal(col_cam, col_cam_info, submodo)

def _render_video(col) -> None:
    with col:
        st.markdown('<div class="lbr-section">Câmera - Espelhamento</div>', unsafe_allow_html=True)
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
                    args=(st.session_state.cam_send_servos, st.session_state.arduino_ok, new_stop, st.session_state.cam_queue),
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
                    letter = st.session_state.cam_letter
                    confidence_pct = int(st.session_state.cam_confidence * 100)
                    if confidence_pct >= 50:
                        st.markdown(
                            f'<div class="lbr-cam-status detecting">Você sinalizou <strong>{letter}</strong> — {confidence_pct}% de confiança</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div class="lbr-cam-status waiting"><span class="cam-dot"></span> Reconhecendo... {confidence_pct}%</div>',
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
        st.markdown('<div class="lbr-section">Estado da Mão</div>', unsafe_allow_html=True)
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

def _render_siga_sinal(col_cam, col_info, submodo) -> None:
    from src.poses import POSES
    from ui.components import render_dedos, render_legend

    _KNN_ONLY = {"H", "J", "K", "X", "Z"}
    chars = [chr(i) for i in range(65, 91)]
    chars = [c for c in chars if c in POSES and c not in _KNN_ONLY]

    # Estado A→Z
    if "sinal_index" not in st.session_state:
        st.session_state.sinal_index = 0
    if "sinal_feitos" not in st.session_state:
        st.session_state.sinal_feitos = set()

    # Estado Aleatório
    if "sinal_random_char" not in st.session_state or not st.session_state.sinal_random_char:
        st.session_state.sinal_random_char = random.choice(chars)
    if "sinal_streak" not in st.session_state:
        st.session_state.sinal_streak = 0
    
    # Controle de feedback
    if "sinal_acerto_flag" not in st.session_state:
        st.session_state.sinal_acerto_flag = False
    if "sinal_sucesso_total" not in st.session_state:
        st.session_state.sinal_sucesso_total = False

    if submodo == "A → Z":
        idx = st.session_state.sinal_index
        target = chars[idx]
    else:
        target = st.session_state.sinal_random_char

    with col_cam:
        st.markdown('<div class="lbr-section">Câmera — Siga o Sinal</div>', unsafe_allow_html=True)

        if not st.session_state.cam_active:
            if st.button("▶  Iniciar câmera", width="stretch", key="sinal_cam_start"):
                st.session_state.cam_active = True
                st.session_state.cam_frame = None
                st.session_state.cam_finger_states = None
                st.session_state.cam_hand_detected = False
                new_stop = threading.Event()
                st.session_state.cam_stop = new_stop
                st.session_state.cam_queue = queue.Queue(maxsize=2)
                threading.Thread(
                    target=camera_thread,
                    args=(False, False, new_stop, st.session_state.cam_queue),
                    daemon=True,
                ).start()
                st.rerun()
        else:
            if st.button("⏹  Parar câmera", width="stretch", key="sinal_cam_stop"):
                st.session_state.cam_stop.set()
                st.session_state.cam_active = False
                st.session_state.cam_frame = None
                st.session_state.cam_finger_states = None
                st.session_state.cam_letter = None
                st.session_state.cam_confidence = 0.0
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

            if st.session_state.cam_frame is not None:
                _, jpg_buf = cv2.imencode(
                    ".jpg",
                    cv2.cvtColor(st.session_state.cam_frame, cv2.COLOR_RGB2BGR),
                    [cv2.IMWRITE_JPEG_QUALITY, 85],
                )
                st.image(jpg_buf.tobytes(), width="stretch")

            letter = st.session_state.cam_letter
            confidence_pct = int(st.session_state.cam_confidence * 100)
            acertou = (
                st.session_state.cam_hand_detected
                and letter
                and confidence_pct >= 50
                and letter == target
            )

            if acertou and not st.session_state.sinal_acerto_flag:
                st.session_state.sinal_acerto_flag = True
                st.rerun()
        else:
            st.markdown("""
            <div class="lbr-card" style="text-align:center;padding:40px 20px;">
                <p style="font-size:0.85rem;color:#8E90A8;">Clique em <strong>Iniciar câmera</strong> para começar.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="lbr-section">Como Funciona</div>', unsafe_allow_html=True)
        if submodo == "A → Z":
            st.markdown("""
            <div class="lbr-step"><div class="lbr-step-num">1</div><div class="lbr-step-text">O sistema exibe a <strong>letra-alvo</strong> e a <strong>posição dos dedos.</strong></div></div>
            <div class="lbr-step"><div class="lbr-step-num">2</div><div class="lbr-step-text"><strong>Faça o sinal</strong> para a câmera com boa iluminação.</div></div>
            <div class="lbr-step"><div class="lbr-step-num">3</div><div class="lbr-step-text">O sistema avança <strong>automaticamente</strong> ao reconhecer o gesto.</div></div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="lbr-step"><div class="lbr-step-num">1</div><div class="lbr-step-text">Uma letra aleatória é exibida para <strong>testar sua memória</strong>.</div></div>
            <div class="lbr-step"><div class="lbr-step-num">2</div><div class="lbr-step-text">Acertos consecutivos <strong>aumentam seu streak</strong> visual.</div></div>
            <div class="lbr-step"><div class="lbr-step-num">3</div><div class="lbr-step-text">Mudar a letra manualmente <strong>zera seu streak</strong>.</div></div>
            """, unsafe_allow_html=True)

    with col_info:
        # Sucesso total
        if st.session_state.sinal_sucesso_total:
            st.markdown("""
                <div class="lbr-card" style="text-align: center; padding: 35px 20px; border-top: 3px solid #EF6603;">
                    <h4 style="font-size: 1.1rem; color: #E8E9F0; margin-bottom: 12px;">Alfabeto Concluído</h4>
                    <p style="color: #9A9CB8; line-height: 1.6; font-size: 0.85rem;">Todos os sinais foram concluídos com sucesso.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Reiniciar Alfabeto", width="stretch"):
                st.session_state.sinal_index = 0
                st.session_state.sinal_feitos = set()
                st.session_state.sinal_sucesso_total = False
                st.rerun()
            st.stop()

        # Feedback de acerto
        if st.session_state.sinal_acerto_flag:
            st.markdown(f"""
            <div class="lbr-sinal-acerto lbr-flash">
                <div class="letra">{target}</div>
                <div class="instrucao">✅ Correto!</div>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1.2)
            
            if st.session_state.arduino_ok:
                from src import servo
                servo.apply_pose(POSES[target])
            
            if submodo == "Aleatório":
                st.session_state.sinal_streak += 1
                st.session_state.sinal_random_char = random.choice(chars)
            else:
                st.session_state.sinal_feitos.add(target)
                if len(st.session_state.sinal_feitos) >= len(chars):
                    st.session_state.sinal_sucesso_total = True
                else:
                    if idx < len(chars) - 1:
                        st.session_state.sinal_index += 1
                    else:
                        for i, c in enumerate(chars):
                            if c not in st.session_state.sinal_feitos:
                                st.session_state.sinal_index = i
                                break
            
            st.session_state.sinal_acerto_flag = False
            st.rerun()
        else:
            st.markdown(f"""
            <div class="lbr-sinal-target">
                <div class="letra">{target}</div>
                <div class="instrucao">Faça esse sinal!</div>
            </div>
            """, unsafe_allow_html=True)

        # Streak visual dinâmico
        if submodo == "Aleatório" and st.session_state.sinal_streak > 0:
            s = st.session_state.sinal_streak
            if s < 3:
                color, label, extra_class = "#9A9CB8", "⚡ Começando...", ""
            elif s < 7:
                color, label, extra_class = "#FF8533", "🔥 No ritmo!", ""
            else:
                color, label, extra_class = "#EF6603", "💥 EXCELENTE!", "streak-glow"

            st.markdown(f"""
                <div class="lbr-card {extra_class}" style="background: #424566; border-left: 4px solid {color}; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; transition: all 0.25s ease;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div>
                            <h4 style="margin: 0; font-size: 0.65rem; color: #9A9CB8; text-transform: uppercase; letter-spacing: 1.5px;">Sequência Atual</h4>
                            <p style="margin: 0; font-size: 0.78rem; color: {color}; font-weight: 600;">{label}</p>
                        </div>
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 800; color: {color}; line-height: 1; text-shadow: 0 2px 8px rgba(0,0,0,0.25);">
                        {s:02d}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Dica visual (A→Z)
        if submodo == "A → Z":
            with st.expander("💡 Ver dica — posição dos dedos"):
                img_path = os.path.join("docs", "alphabet", f"{target}.jpg")
                if os.path.exists(img_path):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(img_path, width=200)

        # Progresso (A→Z)
        if submodo == "A → Z":
            st.markdown('<div class="lbr-section">Progresso</div>', unsafe_allow_html=True)
            feitos = st.session_state.sinal_feitos
            pct = int(len(feitos) / len(chars) * 100)
            st.markdown(f"""
            <div class="lbr-card" style="margin-bottom:8px">
                <h4>{len(feitos)} de {len(chars)} sinais completados ({pct}%)</h4>
                <div style="background:#525680;border-radius:4px;height:8px;margin-top:8px">
                    <div style="background:#EF6603;width:{pct}%;height:8px;border-radius:4px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            all_letters = [chr(i) for i in range(65, 91) if chr(i) in POSES]
            rows = [all_letters[i:i+9] for i in range(0, len(all_letters), 9)]
            for row in rows:
                gcols = st.columns(9)
                for gcol, c in zip(gcols, row):
                    with gcol:
                        if c in _KNN_ONLY:
                            st.markdown(f'<div class="lbr-grid-cell" style="opacity:0.3">{c}</div>', unsafe_allow_html=True)
                        else:
                            cls = "lbr-grid-cell"
                            if c in feitos: cls += " lbr-grid-done"
                            elif c == target: cls += " active"
                            st.markdown(f'<div class="{cls}">{c}</div>', unsafe_allow_html=True)

        # Navegação
        st.markdown("<br>", unsafe_allow_html=True)
        if submodo == "A → Z":
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Anterior", width="stretch", disabled=st.session_state.sinal_index == 0, key="sinal_prev"):
                    st.session_state.sinal_index -= 1
                    st.rerun()
            with c2:
                if st.button("Pular →", width="stretch", disabled=st.session_state.sinal_index == len(chars) - 1, key="sinal_skip"):
                    st.session_state.sinal_index += 1
                    st.rerun()
        else:
            if st.button("Desistir / Mudar Letra", width="stretch", key="sinal_skip_random"):
                st.session_state.sinal_streak = 0 
                st.session_state.sinal_random_char = random.choice(chars)
                st.rerun()