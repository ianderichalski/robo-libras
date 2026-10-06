import os
import queue
import random
import threading
import time

import cv2
import streamlit as st

from src.poses import POSES
from ui.components import (
    img_b64,
    render_dedos, render_legend, render_progress,
    render_steps, render_empty, render_tips, render_notice, section, html,
)
from ui.actions import camera_thread, list_cameras
from ui.state import stop_camera

_MODE_ICONS = {
    "Siga o Sinal": ":material/back_hand:",
    "Espelhamento": ":material/flip:",
}
_SUB_ICONS = {
    "A → Z":     ":material/sort_by_alpha:",
    "Aleatório": ":material/shuffle:",
}

_KNN_ONLY = {"H", "J", "K", "X", "Z"}

_OK_FEEDBACK_SECS = 1.2


def render(tab) -> None:
    with tab:
        with st.container(key="lbr_subnav"):
            mode = st.segmented_control(
                "Modo",
                list(_MODE_ICONS.keys()),
                default=st.session_state.cam_mode_sel,
                format_func=lambda m: f"{_MODE_ICONS[m]} {m}",
                label_visibility="collapsed",
                disabled=st.session_state.cam_active,
                key="cam_mode_ctrl",
            )
        if mode is None:
            mode = st.session_state.cam_mode_sel
        else:
            st.session_state.cam_mode_sel = mode

        # encerra câmera automaticamente ao trocar de modo
        if st.session_state.get("active_cam_mode") != mode:
            if st.session_state.cam_active:
                stop_camera()
            st.session_state.active_cam_mode = mode

        if mode == "Siga o Sinal":
            if "cam_submodo_sel" not in st.session_state:
                st.session_state.cam_submodo_sel = "A → Z"

            with st.container(key="lbr_subnav2"):
                submodo = st.segmented_control(
                    "Ordem das letras",
                    list(_SUB_ICONS.keys()),
                    default=st.session_state.cam_submodo_sel,
                    format_func=lambda m: f"{_SUB_ICONS[m]} {m}",
                    label_visibility="collapsed",
                    key="sinal_submodo",
                    disabled=st.session_state.cam_active,
                )
            if submodo is None:
                submodo = st.session_state.cam_submodo_sel
            else:
                st.session_state.cam_submodo_sel = submodo

            if st.session_state.cam_active:
                st.caption("Pare a câmera para trocar o modo.")
        else:
            submodo = None

        if mode == "Espelhamento" and not st.session_state.arduino_ok:
            render_notice("<strong>Mão robótica desconectada.</strong> Conecte para a mão copiar seus gestos; "
                          "a câmera e o estado da mão funcionam sem ela.")

        col_cam, col_cam_info = st.columns([3, 2], gap="large")

        if mode == "Espelhamento":
            _render_video(col_cam)
            _render_info(col_cam_info)
        else:
            _render_siga_sinal(col_cam, col_cam_info, submodo)

def _camera_controls(prefix: str, send_servos: bool, arduino_ok: bool) -> None:
    """Seleção de câmera + botões iniciar/parar. `prefix` mantém as keys únicas por modo."""
    if not st.session_state.cam_active:
        if not st.session_state.get("cameras_list"):
            st.session_state.cameras_list = list_cameras()
        cameras = st.session_state.cameras_list
        if len(cameras) > 1:
            cam_options = {c["label"]: c["index"] for c in cameras}
            current = st.session_state.get("cam_index", 0)
            values = list(cam_options.values())
            current_idx = values.index(current) if current in values else 0
            c1, c2 = st.columns([5, 1], vertical_alignment="bottom")
            with c1:
                cam_label = st.selectbox("Câmera", options=list(cam_options.keys()),
                                         key=f"{prefix}_cam_selector", index=current_idx)
                st.session_state.cam_index = cam_options[cam_label]
            with c2:
                if st.button("↺", key=f"{prefix}_cam_refresh", help="Atualizar lista de câmeras", width="stretch"):
                    del st.session_state.cameras_list
                    st.rerun()
        elif cameras:
            st.session_state.cam_index = cameras[0]["index"]

        if st.button("▶  Iniciar câmera", width="stretch", type="primary", key=f"{prefix}_cam_start"):
            st.session_state.cam_active = True
            st.session_state.cam_frame = None
            st.session_state.cam_finger_states = None
            st.session_state.cam_hand_detected = False
            new_stop = threading.Event()
            st.session_state.cam_stop = new_stop
            st.session_state.cam_queue = queue.Queue(maxsize=2)
            threading.Thread(
                target=camera_thread,
                args=(send_servos, arduino_ok, new_stop, st.session_state.cam_queue,
                      st.session_state.get("cam_index", 0)),
                daemon=True,
            ).start()
            st.rerun()
    else:
        if st.button("⏹  Parar câmera", width="stretch", key=f"{prefix}_cam_stop"):
            stop_camera()
            st.rerun()

def _pull_camera_data() -> None:
    """Pega o dado mais recente da fila da thread da câmera."""
    latest = None
    try:
        while True:
            latest = st.session_state.cam_queue.get_nowait()
    except Exception:
        pass
    if latest is not None:
        st.session_state.cam_frame = latest["frame"]
        st.session_state.cam_finger_states = latest["finger_states"]
        st.session_state.cam_hand_detected = latest["hand_detected"]
        st.session_state.cam_letter = latest["letter"]
        st.session_state.cam_confidence = latest["confidence"]

def _show_frame() -> bool:
    frame = st.session_state.cam_frame
    if frame is None:
        return False
    _, jpg_buf = cv2.imencode(".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
                              [cv2.IMWRITE_JPEG_QUALITY, 85])
    st.image(jpg_buf.tobytes(), width="stretch")
    return True

def _render_video(col) -> None:
    with col:
        html("""<p class="lbr-text">Sua mão é detectada pelo <strong>MediaPipe Hand Landmarker</strong>.
            A posição de cada dedo é calculada em tempo real e copiada pelos servomotores.</p>""")

        cam_send = st.checkbox(
            "Enviar para a mão robótica (Arduino)",
            value=st.session_state.cam_send_servos,
            disabled=not st.session_state.arduino_ok,
            key="chk_cam_send",
        )
        if cam_send != st.session_state.cam_send_servos:
            st.session_state.cam_send_servos = cam_send
            if st.session_state.cam_active:
                stop_camera()
                st.session_state.cam_queue = queue.Queue(maxsize=2)
                st.session_state.cam_stop = threading.Event()
                st.rerun()

        _camera_controls("btn", st.session_state.cam_send_servos, st.session_state.arduino_ok)

        if st.session_state.cam_active:
            _pull_camera_data()
            if not _show_frame():
                render_empty("loading", "Inicializando câmera…")

            if st.session_state.cam_hand_detected:
                html('<div class="lbr-cam-status detecting"><span class="cam-dot"></span> Mão detectada: replicando movimentos</div>')
                if st.session_state.cam_letter is not None:
                    letter = st.session_state.cam_letter
                    confidence_pct = int(st.session_state.cam_confidence * 100)
                    if confidence_pct >= 50:
                        html(f'<div class="lbr-cam-status ok">✋ Você sinalizou <strong>&nbsp;{letter}&nbsp;</strong> ({confidence_pct}% de confiança)</div>')
                    else:
                        html(f'<div class="lbr-cam-status waiting"><span class="cam-dot"></span> Reconhecendo… {confidence_pct}%</div>')
            else:
                html('<div class="lbr-cam-status waiting"><span class="cam-dot"></span> Mostre a mão para a câmera…</div>')
        else:
            render_empty("camera", "Clique em <strong>Iniciar câmera</strong> para começar a detecção.")

def _render_info(col) -> None:
    with col:
        section("Estado da Mão")
        cam_states = st.session_state.cam_finger_states
        render_dedos(cam_states if cam_states else None)
        render_legend()

        section("Pipeline de Processamento")
        render_steps([
            "A webcam captura vídeo a <strong>30 fps</strong>.",
            "O <strong>MediaPipe Hand Landmarker</strong> detecta 21 pontos da mão.",
            "A distância entre os pontos define quanto cada dedo está dobrado.",
            "Comandos via <strong>PyFirmata</strong> replicam o gesto na mão robótica.",
        ])

        section("Dicas de Uso")
        render_tips([
            ("sun",  "Boa iluminação", "Deixe a mão bem iluminada e visível."),
            ("hand", "Palma para a câmera", "Mostre a palma de frente, sem cortar os dedos."),
            ("slow", "Sem pressa", "Movimentos lentos são reconhecidos melhor."),
            ("usb",  "Sem Arduino?", "Desmarque <em>Enviar para a mão robótica</em> para testar só com a câmera."),
        ])

def _register_hit(target: str, submodo: str, chars: list[str]) -> None:
    """Conta o acerto, avança para a próxima letra e liga o feedback visual (sem bloquear)."""
    st.session_state.sinal_ok_char = target
    st.session_state.sinal_ok_until = time.time() + _OK_FEEDBACK_SECS

    if st.session_state.arduino_ok:
        from src import servo
        servo.apply_pose(POSES[target])

    if submodo == "Aleatório":
        st.session_state.sinal_streak += 1
        opcoes = [c for c in chars if c != target] or chars
        st.session_state.sinal_random_char = random.choice(opcoes)
        return

    st.session_state.sinal_feitos.add(target)
    if len(st.session_state.sinal_feitos) >= len(chars):
        st.session_state.sinal_sucesso_total = True
        st.session_state.sinal_ok_until = 0.0
        stop_camera()
        return
    idx = st.session_state.sinal_index
    if idx < len(chars) - 1:
        st.session_state.sinal_index += 1
    else:
        for i, c in enumerate(chars):
            if c not in st.session_state.sinal_feitos:
                st.session_state.sinal_index = i
                break

def _render_siga_sinal(col_cam, col_info, submodo) -> None:
    chars = [c for c in (chr(i) for i in range(65, 91)) if c in POSES and c not in _KNN_ONLY]

    if not st.session_state.sinal_random_char:
        st.session_state.sinal_random_char = random.choice(chars)

    def _target() -> str:
        if submodo == "A → Z":
            return chars[st.session_state.sinal_index]
        return st.session_state.sinal_random_char

    in_feedback = time.time() < st.session_state.sinal_ok_until

    if st.session_state.cam_active:
        _pull_camera_data()
        target = _target()
        letter = st.session_state.cam_letter
        confidence_pct = int(st.session_state.cam_confidence * 100)
        acertou = (
            st.session_state.cam_hand_detected
            and letter
            and confidence_pct >= 50
            and letter == target
        )
        if acertou and not in_feedback and not st.session_state.sinal_sucesso_total:
            _register_hit(target, submodo, chars)
            in_feedback = True
            if st.session_state.sinal_sucesso_total:
                st.rerun()

    target = _target()

    with col_cam:
        _camera_controls("sinal", False, False)

        if st.session_state.cam_active:
            if not _show_frame():
                render_empty("loading", "Inicializando câmera…")
            if not st.session_state.cam_hand_detected:
                html('<div class="lbr-cam-status waiting"><span class="cam-dot"></span> Mostre a mão para a câmera…</div>')
            else:
                html('<div class="lbr-cam-status detecting"><span class="cam-dot"></span> Mão detectada: segure o sinal</div>')
        else:
            render_empty("camera", "Clique em <strong>Iniciar câmera</strong> e faça o sinal da letra mostrada ao lado.")

        section("Como Funciona")
        if submodo == "A → Z":
            render_steps([
                "O sistema mostra a <strong>letra-alvo</strong>. Abra a dica se precisar ver o sinal.",
                "<strong>Faça o sinal</strong> para a câmera com boa iluminação.",
                "Ao reconhecer o gesto, o sistema <strong>avança sozinho</strong> para a próxima letra.",
            ])
        else:
            render_steps([
                "Uma letra aleatória aparece para <strong>testar sua memória</strong>.",
                "Acertos seguidos <strong>aumentam sua sequência</strong>.",
                "Trocar a letra manualmente <strong>zera a sequência</strong>.",
            ])

    with col_info:
        concluido = st.session_state.sinal_sucesso_total and submodo == "A → Z"

        if concluido:
            html("""
            <div class="lbr-card lbr-celebrate">
                <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
                    stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4z"/>
                    <path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/></svg></div>
                <h4>Alfabeto concluído!</h4>
                <p>Você fez todos os sinais com sucesso. Parabéns!</p>
            </div>""")
        elif in_feedback:
            html(f"""
            <div class="lbr-sinal-acerto">
                <div class="letra">{st.session_state.sinal_ok_char}</div>
                <div class="instrucao">✓ Correto!</div>
            </div>""")
        else:
            html(f"""
            <div class="lbr-sinal-target">
                <div class="letra">{target}</div>
                <div class="instrucao">Faça esse sinal!</div>
            </div>""")

        slot_extra = st.empty()
        if concluido:
            with slot_extra.container(key="lbr_go_restart"):
                if st.button("Reiniciar Alfabeto", width="stretch", type="primary", key="sinal_restart"):
                    st.session_state.sinal_index = 0
                    st.session_state.sinal_feitos = set()
                    st.session_state.sinal_sucesso_total = False
                    st.rerun()
        elif submodo == "Aleatório" and st.session_state.sinal_streak > 0:
            s = st.session_state.sinal_streak
            if s < 3:
                cls, label = "", "Começando"
            elif s < 7:
                cls, label = "warm", "No ritmo!"
            else:
                cls, label = "hot", "Excelente!"
            slot_extra.markdown(f"""
            <div class="lbr-streak {cls}">
                <div><div class="k">Sequência</div><div class="l">{label}</div></div>
                <div class="n">{s:02d}</div>
            </div>""", unsafe_allow_html=True)

        if submodo == "A → Z":
            # dica (some na conclusão, mas o espaço continua reservado)
            slot_dica = st.empty()
            if not concluido:
                with slot_dica.container():
                    _render_dica(target)

            section("Progresso")
            feitos = st.session_state.sinal_feitos
            render_progress("Sinais completados", len(feitos), len(chars), color="green")

            cells = ""
            for c in (chr(i) for i in range(65, 91)):
                if c not in POSES:
                    continue
                if c in _KNN_ONLY:
                    cells += f'<div class="lbr-grid-cell off" title="Letra com movimento: não reconhecida pela câmera">{c}</div>'
                elif c in feitos:
                    cells += f'<div class="lbr-grid-cell lbr-grid-done">{c}</div>'
                elif c == target:
                    cells += f'<div class="lbr-grid-cell active">{c}</div>'
                else:
                    cells += f'<div class="lbr-grid-cell">{c}</div>'
            html(f'<div class="lbr-grid">{cells}</div>')
            st.caption("Letras tracejadas (H, J, K, X, Z) têm movimento e não são reconhecidas pela câmera.")

        # navegação (some na conclusão)
        slot_nav = st.empty()
        if concluido:
            pass
        elif submodo == "A → Z":
            with slot_nav.container():
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Anterior", width="stretch", disabled=st.session_state.sinal_index == 0, key="sinal_prev"):
                        st.session_state.sinal_index -= 1
                        st.session_state.sinal_ok_until = 0.0
                        st.rerun()
                with c2:
                    if st.button("Pular", width="stretch", disabled=st.session_state.sinal_index == len(chars) - 1, key="sinal_skip"):
                        st.session_state.sinal_index += 1
                        st.session_state.sinal_ok_until = 0.0
                        st.rerun()
        else:
            with slot_nav.container():
                if st.button("Desistir / Mudar Letra", width="stretch", key="sinal_skip_random"):
                    st.session_state.sinal_streak = 0
                    st.session_state.sinal_ok_until = 0.0
                    st.session_state.sinal_random_char = random.choice(chars)
                    st.rerun()

def _toggle_dica(target: str) -> None:
    # guarda a letra da dica: ao avançar para outra letra, a dica fecha sozinha
    st.session_state.sinal_dica = None if st.session_state.get("sinal_dica") == target else target

def _render_dica(target: str) -> None:
    """Botão com lâmpada que mostra/esconde a foto do sinal da letra-alvo."""
    aberta = st.session_state.get("sinal_dica") == target
    st.button(
        "Esconder dica" if aberta else "Ver dica",
        icon=":material/lightbulb:",
        key="sinal_dica_btn",
        width="stretch",
        on_click=_toggle_dica,
        args=(target,),
    )
    slot = st.empty()
    if aberta:
        src = img_b64(os.path.join("docs", "alphabet", f"{target}.jpg"))
        slot.markdown(f"""
        <div class="lbr-dica">
            <img src="{src}" alt="Sinal da letra {target}">
            <div>
                <div class="t">Dica</div>
                <div class="l">{target}</div>
                <p>Copie a posição dos dedos da foto e mostre para a câmera.</p>
            </div>
        </div>""", unsafe_allow_html=True)