import time
import streamlit as st

from ui import styles, state
from ui.actions import connect, disconnect, process_voice
from ui.tabs import texto_voz, camera, sobre

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

hcol_main, hcol_conn = st.columns([5, 2], gap="large")

with hcol_main:
    st.markdown('''
    <div class="lbr-hero">
        <div class="lbr-hero-eyebrow">Tecnologia Assistiva</div>
        <div class="lbr-hero-title">🤟 RoboLibras</div>
        <div class="lbr-hero-sub">
            Sistema multimodal de mão robótica para reprodução do alfabeto manual da
            <strong>Língua Brasileira de Sinais</strong> em tempo real
            via texto, voz ou espelhamento por câmera.
        </div>
    </div>
    ''', unsafe_allow_html=True)

with hcol_conn:
    if not st.session_state.arduino_ok:
        c_badge, c_pop = st.columns([4, 1])
        with c_badge:
            st.markdown(status_html, unsafe_allow_html=True)
        with c_pop:
            with st.popover("🛈"):
                st.markdown("**Como conectar o Arduino**")
                st.markdown(
                    "**1.** Conecte o cabo USB ao Arduino e ao PC.\n\n"
                    "**2.** Carregue o firmware **StandardFirmata** pela IDE Arduino "
                    "*(Arquivo → Exemplos → Firmata → StandardFirmata)*.\n\n"
                    "**3.** Descubra a porta no **Gerenciador de Dispositivos** "
                    "*(Windows: COMx · Linux/Mac: /dev/ttyUSB0)*.\n\n"
                    "**4.** Digite a porta abaixo e clique em **Conectar**."
                )
        port = st.text_input("Porta serial", value="COM4", label_visibility="collapsed",
                             placeholder="ex: COM4 ou /dev/ttyUSB0", key="port_input")
        if st.button("Conectar", key="btn_connect", width='stretch'):
            ok, msg = connect(port)
            if ok:
                st.rerun()
            else:
                st.error(msg)
    else:
        st.markdown(status_html, unsafe_allow_html=True)
        if st.button("Desconectar", key="btn_disconnect", width='stretch'):
            disconnect()
            st.rerun()

# processar fila de voz (roda sempre, independente da aba ativa)
process_voice(st.session_state.voice_delay)

# abas
tab_texto, tab_camera, tab_about = st.tabs(["Texto / Voz", "Câmera", "Sobre"])

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