import streamlit as st

from ui.state import go_to
from ui.components import img_b64, html, section, steps_html

def render(tab) -> None:
    with tab:
        _render_hero()
        _render_modes()
        _render_start()
        _render_arduino()

def _render_hero() -> None:
    html(f"""
    <div class="lbr-home-hero">
        <img src="{img_b64('docs/logo.png')}" alt="Logo RoboLibras">
        <div class="t">Robo<span>Libras</span></div>
        <div class="s">
            Aprenda o alfabeto manual da <strong>Língua Brasileira de Sinais</strong>
            de forma interativa: por texto, voz ou câmera.
        </div>
    </div>
    """)

_MODES = [
    {
        "key": "aula", "titulo": "Modo Aula", "aba": "Aprender", "mode": "Modo Aula", "cor": "accent",
        "desc": "Explore cada letra do alfabeto com imagem do sinal e painel de dedos. Execute na mão robótica.",
        "svg": """<svg viewBox="0 0 40 40" fill="none" width="34" height="34">
            <rect x="6" y="8" width="28" height="20" rx="3" stroke="currentColor" stroke-width="2.4"/>
            <line x1="6" y1="32" x2="34" y2="32" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
            <line x1="13" y1="14" x2="27" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <line x1="13" y1="19" x2="27" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <line x1="13" y1="24" x2="21" y2="24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>""",
    },
    {
        "key": "quiz", "titulo": "Quiz", "aba": "Aprender", "mode": "Quiz", "cor": "accent",
        "desc": "Veja o sinal e identifique a letra correta entre 4 opções. Teste o que aprendeu.",
        "svg": """<svg viewBox="0 0 40 40" fill="none" width="34" height="34">
            <circle cx="20" cy="20" r="13" stroke="currentColor" stroke-width="2.4"/>
            <path d="M16 16.5C16 14.3 17.8 13 20 13C22.2 13 24 14.5 24 16.5C24 18.5 22 19.5 20 21V22" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
            <circle cx="20" cy="26" r="1.5" fill="currentColor"/>
        </svg>""",
    },
    {
        "key": "soletra", "titulo": "Soletração Livre", "aba": "Aprender", "mode": "Soletração", "cor": "accent",
        "desc": "Digite ou fale uma palavra e veja a mão robótica reproduzir cada letra em LIBRAS.",
        "svg": """<svg viewBox="0 0 40 40" fill="none" width="34" height="34">
            <rect x="8" y="12" width="24" height="16" rx="3" stroke="currentColor" stroke-width="2.4"/>
            <line x1="13" y1="18" x2="27" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <line x1="13" y1="23" x2="20" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M24 27L24 34M20 34L28 34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>""",
    },
    {
        "key": "siga", "titulo": "Siga o Sinal", "aba": "Praticar", "mode": "Siga o Sinal", "cor": "accent",
        "desc": "Use a câmera para praticar os sinais. Sequência A–Z ou aleatório com streak de acertos.",
        "svg": """<svg viewBox="0 0 40 40" fill="none" width="34" height="34">
            <rect x="7" y="10" width="26" height="20" rx="3" stroke="currentColor" stroke-width="2.4"/>
            <circle cx="20" cy="20" r="5" stroke="currentColor" stroke-width="2"/>
            <circle cx="20" cy="20" r="2" fill="currentColor"/>
            <line x1="7" y1="14" x2="11" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>""",
    },
]

def _render_modes() -> None:
    html('<div class="lbr-home-label">Modos de aprendizagem</div>')

    cols = st.columns(4, gap="small")
    for col, m in zip(cols, _MODES):
        with col:
            with st.container(key=f"lbr_mode_{m['key']}"):
                html(f"""
                <div class="lbr-mode-center" style="--c: var(--lbr-{m['cor']}); --c-soft: var(--lbr-{m['cor']}-soft);">
                    <div class="lbr-mode-icon">{m['svg']}</div>
                    <div class="lbr-mode-title">{m['titulo']}</div>
                    <div class="lbr-mode-desc">{m['desc']}</div>
                </div>""")
                st.button("Abrir", key=f"open_{m['key']}", width="stretch",
                          on_click=go_to, args=(m["aba"], m["mode"]))

def _render_start() -> None:
    html("""
    <div class="lbr-card lbr-start">
        <h4>Por onde começar?</h4>
        <p>
            Acesse o <strong class="hl">Modo Aula</strong> para explorar o alfabeto,
            teste seus conhecimentos no <strong class="hl">Quiz</strong> e
            pratique com a câmera no <strong class="hl">Siga o Sinal</strong>.
            A maioria dos modos funciona <strong>sem Arduino conectado</strong>.
        </p>
    </div>
    """)

def _render_arduino() -> None:
    from ui.actions import connect, disconnect

    section("Configuração · Arduino (opcional)")

    status_html = (
        '<span class="lbr-hdr-badge on"><span class="dot"></span>Arduino conectado</span>'
        if st.session_state.arduino_ok else
        '<span class="lbr-hdr-badge off"><span class="dot"></span>Desconectado</span>'
    )

    c_left, c_right = st.columns([3, 2], gap="large")

    with c_left:
        html("""
        <p class="lbr-text">
            Conecte o Arduino para usar a <strong class="hl">Soletração Livre</strong>
            e reproduzir os sinais fisicamente. Os demais modos funcionam sem conexão.
        </p>
        """)
        html(f'<div class="lbr-conn-badge">{status_html}</div>')

        if not st.session_state.arduino_ok:
            from ui.actions import list_serial_ports, get_default_port

            ports = list_serial_ports()
            default = get_default_port()

            c1, c2 = st.columns([3, 2])
            with c1:
                if ports:
                    default_idx = 0
                    for i, pt in enumerate(ports):
                        if default.lower() in pt.lower():
                            default_idx = i
                            break
                    port = st.selectbox(
                        "Porta serial",
                        options=ports,
                        index=default_idx,
                        label_visibility="collapsed",
                        key="port_select",
                    )
                else:
                    port = st.text_input(
                        "Porta serial",
                        value=default,
                        label_visibility="collapsed",
                        placeholder="ex: COM4",
                        key="port_input",
                    )
                    st.caption("Nenhuma porta detectada. Digite manualmente.")
            with c2:
                cb, cc = st.columns([1, 3])
                with cb:
                    if st.button("↺", key="btn_refresh", help="Atualizar lista de portas", width="stretch"):
                        st.rerun()
                with cc:
                    if st.button("Conectar", key="btn_connect", type="primary", width="stretch"):
                        with st.spinner("Procurando o Arduino…"):
                            ok, msg = connect(port)
                        st.session_state.arduino_err = None if ok else msg
                        if ok:
                            st.rerun()

            _render_connect_error()
        else:
            st.session_state.arduino_err = None
            if st.button("Desconectar", key="btn_disconnect"):
                disconnect()
                st.rerun()

    with c_right:
        passos = steps_html([
            "Conecte o cabo USB ao Arduino e ao PC.",
            "Carregue o <strong>StandardFirmata</strong> na IDE Arduino.",
            "Descubra a porta no Gerenciador de Dispositivos.",
            "Digite a porta e clique em <strong>Conectar</strong>.",
        ])
        html(f'<div class="lbr-card"><h4>Como conectar</h4>{passos}</div>')

def _render_connect_error() -> None:
    """Aviso curto quando a conexão com o Arduino falha."""
    err = st.session_state.get("arduino_err")
    if not err:
        return
    html(f"""
    <div class="lbr-alert">
        <div class="ic">🔌</div>
        <div>
            <div class="t">{err['titulo']}</div>
            <p>{err['dica']} Sem Arduino, os outros modos funcionam normalmente.</p>
        </div>
    </div>""")