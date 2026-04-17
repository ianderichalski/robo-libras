import streamlit as st

from src.poses import get_pose, normalize_text, FINGER_ORDER
from src import servo
from src.voice import VoiceListener
from ui.components import render_dedos, render_char, render_badges, render_legend
from ui.actions import start_spell

def render(tab) -> None:
    with tab:
        col_left, col_right = st.columns([2, 3], gap="large")

        _render_left(col_left)
        _render_right(col_right)

def _render_left(col) -> None:
    with col:

        st.markdown('<div class="lbr-section">Praticar Soletração</div>', unsafe_allow_html=True)
        text_input = st.text_input(
            "Texto", placeholder="Digite letras, números ou palavras...",
            label_visibility="collapsed", key="input_texto"
        )
        delay = st.slider(
            "Intervalo entre letras (s)", 0.3, 2.0,
            st.session_state.voice_delay, 0.1, format="%.1fs",
        )
        st.session_state.voice_delay = delay

        c1, c2 = st.columns(2)
        with c1:
            if st.button("▶  Soletrear", width='stretch',
                         disabled=not st.session_state.arduino_ok or st.session_state.spelling):
                start_spell(text_input, delay)
                st.rerun()
        with c2:
            if st.button("⏹  Parar", width='stretch', disabled=not st.session_state.spelling):
                st.session_state.stop_flag.set()
                st.session_state.spelling = False
                st.rerun()

        if st.session_state.spelling and st.session_state.current_text:
            st.markdown(
                "<div style='margin-top:10px; font-size:0.78rem; color:#9A9CB8; "
                "font-weight:600; text-transform:uppercase; letter-spacing:1px'>Soletreando</div>",
                unsafe_allow_html=True,
            )
            render_badges(st.session_state.current_text, st.session_state.current_char)

        st.markdown('<div class="lbr-section">Praticar por Voz</div>', unsafe_allow_html=True)
        if not st.session_state.mic_active:
            st.markdown('<div class="lbr-mic idle">🎙  Microfone desligado</div>', unsafe_allow_html=True)
            if st.button("🎙  Ligar microfone", width='stretch', disabled=not st.session_state.arduino_ok):
                listener = VoiceListener()
                listener.start()
                st.session_state.voice_listener = listener
                st.session_state.mic_active = True
                st.rerun()
        else:
            st.markdown(
                '<div class="lbr-mic on"><span class="pulse"></span> Ouvindo — fale um número ou letra</div>',
                unsafe_allow_html=True,
            )
            if st.button("⏹  Desligar microfone", width='stretch'):
                if st.session_state.voice_listener:
                    st.session_state.voice_listener.stop()
                st.session_state.mic_active = False
                st.rerun()
        if st.session_state.last_recognized:
            st.markdown(
                f'<div class="lbr-recognized">{st.session_state.last_recognized}</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="lbr-section">Exploração Livre</div>', unsafe_allow_html=True)
        ca, cb, cc = st.columns(3)
        with ca:
            if st.button("🖐  Abrir", width='stretch',
                         disabled=not st.session_state.arduino_ok, key="btn_abrir"):
                servo.open_hand()
                st.session_state.current_pose = None
                st.session_state.current_char = ""
                st.rerun()
        with cb:
            if st.button("✊  Fechar", width='stretch',
                         disabled=not st.session_state.arduino_ok, key="btn_fechar"):
                servo.close_hand()
                st.session_state.current_pose = {f: 1 for f in FINGER_ORDER}
                st.session_state.current_char = ""
                st.rerun()
        with cc:
            if st.button("🔧  Testar", width='stretch',
                         disabled=not st.session_state.arduino_ok, key="btn_testar"):
                servo.test_all()

        st.markdown('<div class="lbr-section">Como Funciona</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lbr-step">
            <div class="lbr-step-num">1</div>
            <div class="lbr-step-text">O usuário digita texto ou fala pelo microfone.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">2</div>
            <div class="lbr-step-text">Cada caractere é mapeado a uma <strong>pose de 5 dedos</strong> do alfabeto LIBRAS.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">3</div>
            <div class="lbr-step-text">Os ângulos são enviados aos <strong>servomotores</strong> via Arduino (protocolo Firmata).</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">4</div>
            <div class="lbr-step-text">A mão robótica reproduz o sinal fisicamente.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="lbr-card">
            <h4>Níveis de Flexão</h4>
            <p>Cada dedo possui 4 posições discretas: <strong>aberto</strong> (estendido),
            <strong>pouco</strong> (leve curva), <strong>meio</strong> (meio dobrado) e
            <strong>fechado</strong> (totalmente dobrado). Combinando os 5 dedos
            cobre-se todo o alfabeto LIBRAS e dígitos 0–5.</p>
        </div>
        """, unsafe_allow_html=True)

def _render_right(col) -> None:
    with col:

        if "kbd_selected" not in st.session_state:
            st.session_state.kbd_selected = ""

        def _on_type():
            st.session_state.kbd_selected = st.session_state._kbd_input

        char_q = st.session_state.kbd_selected

        chars = [str(i) for i in range(6)] + [chr(i) for i in range(65, 91)]
        active = char_q.upper()
        kbd_clicked = None
        for ch in chars:
            if st.session_state.get(f"kbd_{ch}"):
                kbd_clicked = ch
                break
        if kbd_clicked and kbd_clicked != st.session_state.kbd_selected:
            st.session_state.kbd_selected = kbd_clicked
            char_q = kbd_clicked
            active = kbd_clicked

        if char_q:
            pose_q = get_pose(char_q)
            display_char = char_q if pose_q else st.session_state.current_char
            display_pose = pose_q if pose_q else st.session_state.current_pose
            if not pose_q:
                st.caption(f"'{char_q}' não possui pose mapeada.")
        else:
            display_char = st.session_state.current_char
            display_pose = st.session_state.current_pose

        st.markdown('<div class="lbr-section">Estado da Mão</div>', unsafe_allow_html=True)
        render_char(display_char)
        render_dedos(display_pose)
        render_legend()

        st.markdown('<div class="lbr-section">Explorar Alfabeto</div>', unsafe_allow_html=True)

        st.text_input("Consultar", max_chars=1, key="_kbd_input",
                      label_visibility="collapsed",
                      placeholder="Digite ou clique no teclado abaixo...",
                      on_change=_on_type)

        for row in [chars[i:i+8] for i in range(0, len(chars), 8)]:
            bcols = st.columns(len(row))
            for bcol, ch in zip(bcols, row):
                with bcol:
                    st.button(ch, key=f"kbd_{ch}",
                              type="primary" if ch == active else "secondary")

        exec_label = f"▶  Executar  {char_q.upper()}" if char_q else "▶  Executar"
        exec_disabled = not st.session_state.arduino_ok or not char_q or not get_pose(char_q)
        if st.button(exec_label, width='stretch', disabled=exec_disabled, key="btn_executar"):
            servo.apply_pose(get_pose(char_q))
            st.session_state.current_char = char_q
            st.session_state.current_pose = get_pose(char_q)
            st.rerun()