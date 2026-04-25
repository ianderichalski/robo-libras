import time
import streamlit as st

from ui import styles, state
from ui.actions import connect, disconnect, process_voice
from ui.tabs import inicio, texto_voz, camera, sobre

# inicialização
st.set_page_config(page_title="RoboLibras", page_icon="docs/logo.png", layout="wide")
styles.inject()
state.init()

# cabeçalho + conexão arduino
tooltip_on = "Arduino conectado via Firmata. Clique em Desconectar para encerrar a conexão serial."
tooltip_off = "Arduino desconectado. Informe a porta serial (ex: COM4) e clique em Conectar."

status_html = (
    f'<span class="lbr-hdr-badge on"  title="{tooltip_on}"><span class="dot"></span>Arduino conectado</span>'
    if st.session_state.arduino_ok else
    f'<span class="lbr-hdr-badge off" title="{tooltip_off}"><span class="dot"></span>Desconectado</span>'
)

# processar fila de voz (roda sempre, independente da aba ativa)
process_voice(st.session_state.voice_delay)

# abas
tab_inicio, tab_texto, tab_camera, tab_about = st.tabs(["Início", "Aprender", "Praticar", "Sobre"])
inicio.render(tab_inicio)
texto_voz.render(tab_texto)
camera.render(tab_camera)
sobre.render(tab_about)

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