import base64
import streamlit as st

def render(tab) -> None:
    with tab:
        _render_hero()
        _render_modes()
        _render_start()
        _render_arduino()

def _render_hero() -> None:
    with open("docs/logo.png", "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
    logo = f'<img src="data:image/png;base64,{img_b64}" style="width:120px;border-radius:16px">'

    st.markdown(f"""
    <div style="text-align:center;padding:3rem 1rem 2rem">
        {logo}
        <div style="font-size:2.4rem;font-weight:700;color:#E8E9F0;margin:20px 0 8px;letter-spacing:-0.5px">RoboLibras</div>
        <div style="font-size:0.9rem;color:#9A9CB8;max-width:540px;margin:0 auto;line-height:1.8">
            Aprenda o alfabeto manual da <strong style="color:#E8E9F0">Língua Brasileira de Sinais</strong>
            de forma interativa — por texto, voz ou câmera.
        </div>
    </div>
    """, unsafe_allow_html=True)

def _render_modes() -> None:
    st.markdown("""
    <div style="font-size:0.63rem;font-weight:700;text-transform:uppercase;letter-spacing:2px;
    color:#6B6D88;margin-bottom:1rem">Modos de aprendizagem</div>
    """, unsafe_allow_html=True)

    modes = [
        {
            "titulo": "Modo Aula",
            "desc": "Explore cada letra do alfabeto com imagem do sinal e painel de dedos. Execute na mão robótica.",
            "cor": "#EF6603",
            "svg": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="36">
                <rect x="6" y="8" width="28" height="20" rx="3" stroke="#EF6603" stroke-width="2"/>
                <line x1="6" y1="32" x2="34" y2="32" stroke="#EF6603" stroke-width="2" stroke-linecap="round"/>
                <line x1="13" y1="14" x2="27" y2="14" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
                <line x1="13" y1="19" x2="27" y2="19" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
                <line x1="13" y1="24" x2="21" y2="24" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
            </svg>""",
            "aba": "Aprender",
        },
        {
            "titulo": "Quiz",
            "desc": "Veja o sinal e identifique a letra correta entre 4 opções. Teste o que aprendeu.",
            "cor": "#EF6603",
            "svg": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="36">
                <circle cx="20" cy="20" r="13" stroke="#EF6603" stroke-width="2"/>
                <path d="M16 16.5C16 14.3 17.8 13 20 13C22.2 13 24 14.5 24 16.5C24 18.5 22 19.5 20 21V22" stroke="#EF6603" stroke-width="2" stroke-linecap="round"/>
                <circle cx="20" cy="26" r="1.2" fill="#EF6603"/>
            </svg>""",
            "aba": "Aprender",
        },
        {
            "titulo": "Soletração Livre",
            "desc": "Digite ou fale uma palavra e veja a mão robótica reproduzir cada letra em LIBRAS.",
            "cor": "#EF6603",
            "svg": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="36">
                <rect x="8" y="12" width="24" height="16" rx="3" stroke="#EF6603" stroke-width="2"/>
                <line x1="13" y1="18" x2="27" y2="18" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
                <line x1="13" y1="23" x2="20" y2="23" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M24 27L24 34M20 34L28 34" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
            </svg>""",
            "aba": "Aprender",
        },
        {
            "titulo": "Siga o Sinal",
            "desc": "Use a câmera para praticar os sinais. Sequência A–Z ou aleatório com streak de acertos.",
            "cor": "#EF6603",
            "svg": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="36">
                <rect x="7" y="10" width="26" height="20" rx="3" stroke="#EF6603" stroke-width="2"/>
                <circle cx="20" cy="20" r="5" stroke="#EF6603" stroke-width="1.5"/>
                <circle cx="20" cy="20" r="2" fill="#EF6603"/>
                <line x1="7" y1="14" x2="11" y2="14" stroke="#EF6603" stroke-width="1.5" stroke-linecap="round"/>
            </svg>""",
            "aba": "Praticar",
        },
    ]

    cols = st.columns(4, gap="small")
    for col, mode in zip(cols, modes):
        with col:
            st.markdown(f"""
            <div style="background:#3D4166;border:1px solid #525680;border-top:2px solid {mode['cor']};
            border-radius:10px;padding:20px 16px;text-align:center;min-height:190px">
                <div style="margin-bottom:12px">{mode['svg']}</div>
                <div style="font-size:0.85rem;font-weight:600;color:#E8E9F0;margin-bottom:6px">{mode['titulo']}</div>
                <div style="font-size:0.74rem;color:#9A9CB8;line-height:1.6;margin-bottom:10px">{mode['desc']}</div>
                <div style="font-size:0.62rem;color:{mode['cor']};text-transform:uppercase;letter-spacing:1px;font-weight:600">
                    Aba {mode['aba']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def _render_start() -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#252840;border:1px solid #525680;border-radius:10px;padding:18px 24px">
        <div style="font-size:0.82rem;font-weight:600;color:#E8E9F0;margin-bottom:6px">Por onde começar?</div>
        <div style="font-size:0.76rem;color:#9A9CB8;line-height:1.8">
            Acesse o <strong style="color:#EF6603">Modo Aula</strong> para explorar o alfabeto,
            teste seus conhecimentos no <strong style="color:#EF6603">Quiz</strong> e
            pratique com a câmera no <strong style="color:#EF6603">Siga o Sinal</strong>.
            A maioria dos modos funciona <strong style="color:#C8CAE0">sem Arduino conectado</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

def _render_arduino() -> None:
    from ui.actions import connect, disconnect

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="lbr-section">Configuração — Arduino (opcional)</div>', unsafe_allow_html=True)

    status_html = (
        '<span class="lbr-hdr-badge on"><span class="dot"></span>Arduino conectado</span>'
        if st.session_state.arduino_ok else
        '<span class="lbr-hdr-badge off"><span class="dot"></span>Desconectado</span>'
    )

    c_left, c_right = st.columns([3, 2], gap="large")

    with c_left:
        st.markdown(f"""
        <p style="font-size:0.78rem;color:#9A9CB8;margin:0 0 10px;line-height:1.7">
            Conecte o Arduino para usar a <strong style="color:#EF6603">Soletração Livre</strong>
            e reproduzir os sinais fisicamente. Os demais modos funcionam sem conexão.
        </p>
        """, unsafe_allow_html=True)
        st.markdown(status_html, unsafe_allow_html=True)

        if not st.session_state.arduino_ok:
            c1, c2 = st.columns([2, 2])
            with c1:
                port = st.text_input("Porta serial", value="COM4", label_visibility="collapsed",
                                     placeholder="ex: COM4", key="port_input")
            with c2:
                if st.button("Conectar", key="btn_connect", width="stretch"):
                    ok, msg = connect(port)
                    if ok:
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            if st.button("Desconectar", key="btn_disconnect"):
                disconnect()
                st.rerun()

    with c_right:
        st.markdown("""
        <div class="lbr-card">
            <h4>Como conectar</h4>
            <div class="lbr-step" style="margin:6px 0">
                <div class="lbr-step-num">1</div>
                <div class="lbr-step-text">Conecte o cabo USB ao Arduino e ao PC.</div>
            </div>
            <div class="lbr-step" style="margin:6px 0">
                <div class="lbr-step-num">2</div>
                <div class="lbr-step-text">Carregue o <strong>StandardFirmata</strong> na IDE Arduino.</div>
            </div>
            <div class="lbr-step" style="margin:6px 0">
                <div class="lbr-step-num">3</div>
                <div class="lbr-step-text">Descubra a porta no Gerenciador de Dispositivos.</div>
            </div>
            <div class="lbr-step" style="margin:6px 0">
                <div class="lbr-step-num">4</div>
                <div class="lbr-step-text">Digite a porta e clique em <strong>Conectar</strong>.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)