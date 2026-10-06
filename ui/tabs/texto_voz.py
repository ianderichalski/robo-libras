import random
import streamlit as st

from src.poses import get_pose, FINGER_ORDER, POSES
from src import servo
from src.voice import VoiceListener
from ui.components import (
    render_dedos, render_char, render_badges, render_legend,
    render_sign_img, render_progress, render_steps, render_notice, section, html,
)
from ui.actions import start_spell

_MODE_ICONS = {
    "Modo Aula":  ":material/menu_book:",
    "Quiz":       ":material/quiz:",
    "Soletração": ":material/spellcheck:",
}

_LETTERS = [c for c in (chr(i) for i in range(65, 91)) if c in POSES]

def render(tab) -> None:
    with tab:
        if "aprender_mode_sel" not in st.session_state:
            st.session_state.aprender_mode_sel = "Modo Aula"

        with st.container(key="lbr_subnav"):
            mode = st.segmented_control(
                "Modo",
                list(_MODE_ICONS.keys()),
                default=st.session_state.aprender_mode_sel,
                format_func=lambda m: f"{_MODE_ICONS[m]} {m}",
                label_visibility="collapsed",
                key="aprender_mode_ctrl",
            )
        if mode is None:
            mode = st.session_state.aprender_mode_sel
        else:
            st.session_state.aprender_mode_sel = mode

        if mode == "Soletração":
            if not st.session_state.arduino_ok:
                render_notice("<strong>Mão robótica desconectada.</strong> Conecte para soletrar; "
                              "o teclado ao lado funciona sem ela.")
            col_left, col_right = st.columns([2, 3], gap="large")
            _render_left(col_left)
            _render_right(col_right)
        elif mode == "Modo Aula":
            _render_aula()
        elif mode == "Quiz":
            _render_quiz()

def _render_left(col) -> None:
    ok = st.session_state.arduino_ok
    with col:
        section("Soletrar texto")
        text_input = st.text_input(
            "Texto", placeholder="Digite uma palavra, letras ou números...",
            label_visibility="collapsed", key="input_texto"
        )
        delay = st.slider(
            "Intervalo entre letras", 0.3, 2.0,
            st.session_state.voice_delay, 0.1, format="%.1fs",
        )
        st.session_state.voice_delay = delay

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Soletrar", icon=":material/play_arrow:", width="stretch", type="primary",
                         disabled=not ok or st.session_state.spelling, key="btn_soletrar"):
                start_spell(text_input, delay)
                st.rerun()
        with c2:
            if st.button("Parar", icon=":material/stop:", width="stretch",
                         disabled=not st.session_state.spelling, key="btn_parar"):
                st.session_state.stop_flag.set()
                st.session_state.spelling = False
                st.rerun()

        slot_badges = st.empty()
        if st.session_state.spelling and st.session_state.current_text:
            with slot_badges.container():
                html('<div class="lbr-mini-label">Soletrando</div>')
                render_badges(st.session_state.current_text, st.session_state.current_char)

        section("Soletrar por voz")
        if not st.session_state.mic_active:
            if st.button("Ligar microfone", icon=":material/mic:", width="stretch",
                         disabled=not ok, key="btn_mic_on"):
                listener = VoiceListener()
                listener.start()
                st.session_state.voice_listener = listener
                st.session_state.mic_active = True
                st.rerun()
        else:
            html('<div class="lbr-mic on"><span class="pulse"></span> Ouvindo: fale uma letra ou um número</div>')
            if st.button("Desligar microfone", icon=":material/mic_off:", width="stretch", key="btn_mic_off"):
                if st.session_state.voice_listener:
                    st.session_state.voice_listener.stop()
                st.session_state.mic_active = False
                st.rerun()
        slot_rec = st.empty()
        if st.session_state.last_recognized:
            slot_rec.markdown(f'<p class="lbr-text lbr-recognized-line">{st.session_state.last_recognized}</p>',
                              unsafe_allow_html=True)

        section("Controle manual")
        ca, cb, cc = st.columns(3)
        with ca:
            if st.button("Abrir", icon=":material/back_hand:", width="stretch",
                         disabled=not ok, key="btn_abrir", help="Abre todos os dedos"):
                servo.open_hand()
                st.session_state.current_pose = None
                st.session_state.current_char = ""
                st.rerun()
        with cb:
            if st.button("Fechar", icon=":material/sports_mma:", width="stretch",
                         disabled=not ok, key="btn_fechar", help="Fecha todos os dedos"):
                servo.close_hand()
                st.session_state.current_pose = {f: 1 for f in FINGER_ORDER}
                st.session_state.current_char = ""
                st.rerun()
        with cc:
            if st.button("Testar", icon=":material/tune:", width="stretch",
                         disabled=not ok, key="btn_testar", help="Move cada dedo para testar os servos"):
                servo.test_all()

        section("Como Funciona")
        render_steps([
            "Digite um texto ou fale pelo microfone.",
            "Cada caractere vira uma <strong>pose de 5 dedos</strong> do alfabeto LIBRAS.",
            "Os ângulos vão para os <strong>servomotores</strong> pelo Arduino (protocolo Firmata).",
            "A mão robótica reproduz o sinal.",
        ])

        section("Níveis de Flexão")
        html("""
        <p class="lbr-text">Cada dedo tem 4 posições: <strong>aberto</strong> (esticado),
        <strong>pouco</strong> (leve curva), <strong>meio</strong> (meio dobrado) e
        <strong>fechado</strong> (totalmente dobrado). Combinando os 5 dedos dá para formar
        o alfabeto LIBRAS e os dígitos de 0 a 5.</p>
        """)

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

        section("Estado da Mão")
        render_char(display_char)
        render_dedos(display_pose)
        render_legend()

        section("Consultar uma letra")
        st.text_input("Consultar", max_chars=1, key="_kbd_input",
                      label_visibility="collapsed",
                      placeholder="Digite uma letra ou clique no teclado",
                      on_change=_on_type)

        with st.container(key="lbr_grid_kbd"):
            for row in [chars[i:i + 8] for i in range(0, len(chars), 8)]:
                bcols = st.columns(len(row))
                for bcol, ch in zip(bcols, row):
                    with bcol:
                        st.button(ch, key=f"kbd_{ch}", width="stretch",
                                  type="primary" if ch == active else "secondary")

        exec_label = f"Executar {char_q.upper()} na mão robótica" if char_q else "Executar na mão robótica"
        exec_disabled = not st.session_state.arduino_ok or not char_q or not get_pose(char_q)
        if st.button(exec_label, icon=":material/play_arrow:", width="stretch", disabled=exec_disabled, key="btn_executar"):
            servo.apply_pose(get_pose(char_q))
            st.session_state.current_char = char_q
            st.session_state.current_pose = get_pose(char_q)
            st.rerun()

def _render_aula() -> None:
    chars = _LETTERS

    idx = st.session_state.aula_index
    char = chars[idx]
    st.session_state.aula_vistos.add(char)

    col_left, col_right = st.columns([2, 3], gap="large")

    with col_left:
        section("Sinal Atual")
        render_sign_img(char)
        render_char(char)

        html("<div style='height:8px'></div>")
        c1, c2, c3 = st.columns(3, vertical_alignment="center")
        with c1:
            if st.button("Anterior", width="stretch", disabled=idx == 0, key="aula_prev"):
                st.session_state.aula_index -= 1
                st.rerun()
        with c2:
            html(f"<div class='lbr-counter'>{idx + 1}<span> / {len(chars)}</span></div>")
        with c3:
            if st.button("Próxima", width="stretch", type="primary",
                         disabled=idx == len(chars) - 1, key="aula_next"):
                st.session_state.aula_index += 1
                st.rerun()

        html("<div style='height:8px'></div>")
        if st.button("▶  Executar sinal na mão robótica", width="stretch",
                     disabled=not st.session_state.arduino_ok, key="aula_exec"):
            start_spell(char, st.session_state.voice_delay)
            st.rerun()

    with col_right:
        section("Progresso")
        vistos = st.session_state.aula_vistos
        render_progress("Sinais explorados", len(vistos), len(chars))

        section("Navegar no Alfabeto")
        with st.container(key="lbr_grid_aula"):
            for row in [chars[i:i + 9] for i in range(0, len(chars), 9)]:
                bcols = st.columns(9)
                for bcol, c in zip(bcols, row):
                    with bcol:
                        is_cur = c == char
                        wrap_key = f"cell_done_aula_{c}" if (c in vistos and not is_cur) else f"cell_aula_{c}"
                        with st.container(key=wrap_key):
                            if st.button(c, key=f"aula_chr_{c}", width="stretch",
                                         type="primary" if is_cur else "secondary"):
                                st.session_state.aula_index = chars.index(c)
                                st.rerun()
        html("<div class='lbr-legend' style='margin-top:10px'>"
             "<span class='meio'>Letra atual</span><span class='aberto'>Já vista</span></div>")

    section("Como Funciona")
    render_steps([
        "Navegue pelo alfabeto com <strong>Anterior</strong> e <strong>Próxima</strong>.",
        "Observe a <strong>posição dos dedos</strong> na imagem de cada sinal.",
        "Clique em <strong>Executar sinal na mão robótica</strong> para ver o sinal reproduzido fisicamente.",
        "Acompanhe seu <strong>progresso</strong>: as letras já vistas ficam verdes.",
    ])

def _new_question(chars: list[str]) -> None:
    st.session_state.quiz_char = random.choice(chars)
    st.session_state.quiz_opcoes = []
    st.session_state.quiz_respondido = False
    st.session_state.quiz_acerto = False
    st.session_state.quiz_escolha = ""

def _answer(opcao: str) -> None:
    char = st.session_state.quiz_char
    st.session_state.quiz_respondido = True
    st.session_state.quiz_escolha = opcao
    st.session_state.quiz_acerto = (opcao == char)
    if opcao == char:
        st.session_state.quiz_acertos += 1
    else:
        st.session_state.quiz_erros += 1

def _render_quiz() -> None:
    chars = _LETTERS

    if not st.session_state.quiz_char:
        _new_question(chars)
    char = st.session_state.quiz_char

    if not st.session_state.quiz_opcoes:
        erradas = random.sample([c for c in chars if c != char], 3)
        opcoes = erradas + [char]
        random.shuffle(opcoes)
        st.session_state.quiz_opcoes = opcoes

    respondido = st.session_state.quiz_respondido
    escolha = st.session_state.quiz_escolha

    col_left, col_right = st.columns([2, 3], gap="large")

    with col_left:
        section("Sinal Atual")
        render_sign_img(char)

        if not respondido:
            html("""
            <div class="lbr-char-display q">
                <div class="lbr-char-big">?</div>
                <div class="lbr-char-label">sinal atual</div>
            </div>""")
        elif st.session_state.quiz_acerto:
            html(f"""
            <div class="lbr-char-display ok">
                <div class="lbr-char-big">{char}</div>
                <div class="lbr-char-label">✓ Correto!</div>
            </div>""")
        else:
            html(f"""
            <div class="lbr-char-display bad">
                <div class="lbr-char-big">{char}</div>
                <div class="lbr-char-label">✕ Você marcou {escolha} · a certa é {char}</div>
            </div>""")

        html("<div style='height:8px'></div>")
        if st.button("▶  Executar sinal na mão robótica", width="stretch",
                     disabled=not st.session_state.arduino_ok, key="quiz_exec"):
            start_spell(char, st.session_state.voice_delay)
            st.rerun()

        section("Como Funciona")
        render_steps([
            "O sistema exibe a <strong>imagem de um sinal</strong> do alfabeto LIBRAS.",
            "Escolha entre as <strong>4 opções</strong> qual letra corresponde ao sinal.",
            "Receba <strong>feedback imediato</strong>: se errar, a resposta certa fica em verde.",
            "Acompanhe seu progresso total.",
        ])

    with col_right:
        section("Qual letra é esse sinal?")

        if not respondido:
            with st.container(key="lbr_quiz_opts"):
                bcols = st.columns(2)
                for i, opcao in enumerate(st.session_state.quiz_opcoes):
                    with bcols[i % 2]:
                        st.button(opcao, width="stretch", key=f"quiz_op_{opcao}",
                                  on_click=_answer, args=(opcao,))
        else:
            tiles = ""
            for opcao in st.session_state.quiz_opcoes:
                if opcao == char:
                    tiles += f'<div class="lbr-opt right">{opcao}<span class="ic">✓</span></div>'
                elif opcao == escolha:
                    tiles += f'<div class="lbr-opt wrong">{opcao}<span class="ic">✕</span></div>'
                else:
                    tiles += f'<div class="lbr-opt">{opcao}</div>'
            html(f'<div class="lbr-opts compact">{tiles}</div>')

            with st.container(key="lbr_go_quiz" if st.session_state.quiz_acerto else "lbr_quiz_next"):
                st.button("Próxima pergunta", width="stretch", type="primary", key="quiz_next",
                          on_click=_new_question, args=(chars,))

        section("Progresso")
        acertos = st.session_state.quiz_acertos
        erros = st.session_state.quiz_erros
        total = acertos + erros
        pct = int(acertos / total * 100) if total > 0 else 0
        html(f"""
        <div class="lbr-card">
            <div class="lbr-stats">
                <div class="lbr-stat green"><div class="v">{acertos}</div><div class="l">Acertos</div></div>
                <div class="lbr-stat red"><div class="v">{erros}</div><div class="l">Erros</div></div>
                <div class="lbr-stat orange"><div class="v">{pct}%</div><div class="l">Precisão</div></div>
            </div>
            <div class="lbr-bar"><div style="width:{pct}%"></div></div>
        </div>
        """)