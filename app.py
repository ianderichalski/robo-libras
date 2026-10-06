import time
import streamlit as st

from ui import styles, state
from ui.actions import process_voice
from ui.tabs import inicio, texto_voz, camera, sobre

# inicialização
st.set_page_config(page_title="RoboLibras", page_icon="docs/logo.png", layout="wide")
state.init()
styles.inject()

PAGES = {
    "Início":   (":material/home:",     inicio),
    "Aprender": (":material/school:",   texto_voz),
    "Praticar": (":material/videocam:", camera),
    "Sobre":    (":material/info:",     sobre),
}

def _on_nav() -> None:
    # segmented_control permite "desmarcar" clicando no item ativo; aqui isso não faz sentido
    if st.session_state.nav is None:
        st.session_state.nav = st.session_state.page
    else:
        st.session_state.page = st.session_state.nav

with st.container(key="lbr_header"):
    _, c_nav, c_right = st.columns([1, 2.4, 1], vertical_alignment="center")

    with c_nav:
        with st.container(horizontal=True, horizontal_alignment="center"):
            st.segmented_control(
                "Navegação",
                list(PAGES.keys()),
                format_func=lambda p: f"{PAGES[p][0]} {p}",
                label_visibility="collapsed",
                key="nav",
                on_change=_on_nav,
            )

    with c_right:
        with st.container(horizontal=True, horizontal_alignment="right", vertical_alignment="center"):
            ligado = st.session_state.arduino_ok
            st.button(
                "",
                icon=":material/usb:" if ligado else ":material/usb_off:",
                key="btn_arduino_on" if ligado else "btn_arduino_off",
                help="Arduino conectado" if ligado else "Arduino desconectado · clique para conectar",
                on_click=state.go_to,
                args=("Início",),
            )
            dark = st.session_state.theme == "dark"
            st.button(
                "",
                icon=":material/light_mode:" if dark else ":material/dark_mode:",
                key="btn_theme",
                help="Tema claro" if dark else "Tema escuro",
                on_click=styles.toggle,
            )

page = st.session_state.page

if page != "Praticar" and st.session_state.cam_active:
    state.stop_camera()

# processar fila de voz
process_voice(st.session_state.voice_delay)

# página ativa
PAGES[page][1].render(st.container())

# sync & auto-refresh
if st.session_state.spelling:
    shared = st.session_state.shared_state
    st.session_state.current_char = shared.get("char", "")
    st.session_state.current_pose = shared.get("pose", None)
    if shared.get("done", False):
        st.session_state.spelling = False
        shared["done"] = False

if st.session_state.spelling or st.session_state.mic_active:
    time.sleep(0.5)
    st.rerun()

if st.session_state.cam_active:
    time.sleep(0.08)
    st.rerun()