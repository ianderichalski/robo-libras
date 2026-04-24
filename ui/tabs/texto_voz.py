import streamlit as st
import os

from src.poses import get_pose, normalize_text, FINGER_ORDER
from src import servo
from src.voice import VoiceListener
from ui.components import render_dedos, render_char, render_badges, render_legend
from ui.actions import start_spell

def render(tab) -> None:
    with tab:
        mode = st.radio(
            "Modo",
            ["Soletração Livre", "Modo Aula", "Quiz"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if mode == "Soletração Livre":
            col_left, col_right = st.columns([2, 3], gap="large")
            _render_left(col_left, mode)
            _render_right(col_right)
        elif mode == "Modo Aula":
            _render_aula()
        elif mode == "Quiz":
            _render_quiz()

def _render_left(col, mode="Soletração Livre") -> None:
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

def _render_aula() -> None:
    from src.poses import POSES

    chars = [chr(i) for i in range(65, 91)]
    chars = [c for c in chars if c in POSES]

    if "aula_index" not in st.session_state:
        st.session_state.aula_index = 0
    if "aula_vistos" not in st.session_state:
        st.session_state.aula_vistos = set()

    idx = st.session_state.aula_index
    char = chars[idx]
    st.session_state.aula_vistos.add(char)

    col_left, col_right = st.columns([2, 3], gap="large")

    with col_left:
        st.markdown('<div class="lbr-section">Sinal Atual</div>', unsafe_allow_html=True)
        
        img_path = os.path.join("docs", "alphabet", f"{char}.jpg")
        if os.path.exists(img_path):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(img_path, width=200)
                st.markdown(
                    "<p style='font-size:0.65rem;color:#6B6D88;text-align:center;margin:2px 0 8px'><a href='https://dicionario.ines.gov.br' target='_blank' style='color:#6B6D88'>Ver movimento no Dicionário INES/MEC</a></p>",
                    unsafe_allow_html=True,
                )

        render_char(char)

        render_dedos(POSES[char])
        render_legend()

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("← Anterior", width="stretch", disabled=idx == 0, key="aula_prev"):
                st.session_state.aula_index -= 1
                st.rerun()
        with c2:
            st.markdown(
                f"<div style='text-align:center;font-size:0.8rem;color:#9A9CB8;padding-top:8px'>"
                f"{idx + 1} / {len(chars)}</div>",
                unsafe_allow_html=True,
            )
        with c3:
            if st.button("Próxima →", width="stretch", disabled=idx == len(chars) - 1, key="aula_next"):
                st.session_state.aula_index += 1
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶  Executar na mão robótica", width="stretch",
                     disabled=not st.session_state.arduino_ok, key="aula_exec"):
            start_spell(char, st.session_state.voice_delay)
            st.rerun()

    with col_right:
        st.markdown('<div class="lbr-section">Progresso</div>', unsafe_allow_html=True)
        vistos = len(st.session_state.aula_vistos)
        total = len(chars)
        pct = int(vistos / total * 100)
        st.markdown(f"""
        <div class="lbr-card">
            <h4>{vistos} de {total} sinais explorados ({pct}%)</h4>
            <div style="background:#525680;border-radius:4px;height:8px;margin-top:8px">
                <div style="background:#EF6603;width:{pct}%;height:8px;border-radius:4px"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="lbr-section">Navegar no Alfabeto</div>', unsafe_allow_html=True)
        for row in [chars[i:i+9] for i in range(0, len(chars), 9)]:
            bcols = st.columns(9)
            for bcol, c in zip(bcols, row):
                with bcol:
                    if st.button(c, key=f"aula_chr_{c}",
                                type="primary" if c == char else "secondary"):
                        st.session_state.aula_index = chars.index(c)
                        st.rerun()
    st.markdown('<div class="lbr-section">Como Funciona</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lbr-step">
        <div class="lbr-step-num">1</div>
        <div class="lbr-step-text">Navegue pelo alfabeto com <strong>Anterior</strong> e <strong>Próxima</strong>.</div>
    </div>
    <div class="lbr-step">
        <div class="lbr-step-num">2</div>
        <div class="lbr-step-text">Observe a <strong>posição dos dedos</strong> no painel ao lado para cada sinal.</div>
    </div>
    <div class="lbr-step">
        <div class="lbr-step-num">3</div>
        <div class="lbr-step-text">Clique em <strong>Executar na mão robótica</strong> para ver o sinal reproduzido fisicamente.</div>
    </div>
    <div class="lbr-step">
        <div class="lbr-step-num">4</div>
        <div class="lbr-step-text">Acompanhe seu <strong>progresso</strong> — quantos sinais já explorou nessa sessão.</div>
    </div>
    """, unsafe_allow_html=True)

def _render_quiz() -> None:
    import random
    from src.poses import POSES

    chars = [chr(i) for i in range(65, 91)]
    chars = [c for c in chars if c in POSES]

    if not st.session_state.quiz_char:
        st.session_state.quiz_char = random.choice(chars)
        st.session_state.quiz_opcoes = []
        st.session_state.quiz_respondido = False
        st.session_state.quiz_acerto = False

    char = st.session_state.quiz_char

    if not st.session_state.quiz_opcoes:
        erradas = random.sample([c for c in chars if c != char], 3)
        opcoes = erradas + [char]
        random.shuffle(opcoes)
        st.session_state.quiz_opcoes = opcoes

    col_left, col_right = st.columns([2, 3], gap="large")

    with col_left:
        st.markdown('<div class="lbr-section">Sinal na Mão Robótica</div>', unsafe_allow_html=True)
        img_path = os.path.join("docs", "alphabet", f"{char}.jpg")
        if os.path.exists(img_path):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(img_path, width=200)
                st.markdown(
                    "<p style='font-size:0.65rem;color:#6B6D88;text-align:center;margin:2px 0 8px'><a href='https://dicionario.ines.gov.br' target='_blank' style='color:#6B6D88'>Ver movimento no Dicionário INES/MEC</a></p>",
                    unsafe_allow_html=True,
                )
        if not st.session_state.quiz_respondido:
            render_char("?")
        else:
            render_char(char)
        render_dedos(POSES[char])
        render_legend()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶  Executar sinal", width="stretch",
                     disabled=not st.session_state.arduino_ok, key="quiz_exec"):
            start_spell(char, st.session_state.voice_delay)
            st.rerun()

        st.markdown('<div class="lbr-section">Como Funciona</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lbr-step">
            <div class="lbr-step-num">1</div>
            <div class="lbr-step-text">O sistema exibe a <strong>posição dos dedos</strong> de um sinal do alfabeto LIBRAS.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">2</div>
            <div class="lbr-step-text">Escolha entre as <strong>4 opções</strong> qual letra corresponde ao sinal.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">3</div>
            <div class="lbr-step-text">Receba <strong>feedback imediato</strong> — acerto ou erro com a resposta correta.</div>
        </div>
        <div class="lbr-step">
            <div class="lbr-step-num">4</div>
            <div class="lbr-step-text">Acompanhe sua <strong>pontuação</strong> ao longo da sessão.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="lbr-section">Qual letra é esse sinal?</div>', unsafe_allow_html=True)

        if not st.session_state.quiz_respondido:
            bcols = st.columns(2)
            for i, opcao in enumerate(st.session_state.quiz_opcoes):
                with bcols[i % 2]:
                    if st.button(opcao, width="stretch", key=f"quiz_op_{opcao}"):
                        st.session_state.quiz_respondido = True
                        st.session_state.quiz_acerto = opcao == char
                        st.session_state.quiz_total += 1
                        if opcao == char:
                            st.session_state.quiz_acertos += 1
                        st.rerun()
        else:
            if st.session_state.quiz_acerto:
                st.markdown(
                    '<div class="lbr-recognized">✅  Correto!</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="lbr-recognized">❌  Errado! O sinal era <strong>{char}</strong>.</div>',
                    unsafe_allow_html=True,
                )

            if st.button("Próxima →", width="stretch", key="quiz_next"):
                st.session_state.quiz_char = random.choice(chars)
                st.session_state.quiz_opcoes = []
                st.session_state.quiz_respondido = False
                st.session_state.quiz_acerto = False
                st.rerun()

        st.markdown('<div class="lbr-section">Pontuação</div>', unsafe_allow_html=True)
        acertos = st.session_state.quiz_acertos
        total = st.session_state.quiz_total
        pct = int(acertos / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div class="lbr-card">
            <h4>{acertos} de {total} corretos ({pct}%)</h4>
            <div style="background:#525680;border-radius:4px;height:8px;margin-top:8px">
                <div style="background:#EF6603;width:{pct}%;height:8px;border-radius:4px"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)