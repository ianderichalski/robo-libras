import streamlit as st

def inject() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Esconde barra superior do Streamlit */
[data-testid="stToolbar"]       { display: none !important; }
[data-testid="stDecoration"]    { display: none !important; }
[data-testid="stStatusWidget"]  { display: none !important; }
header[data-testid="stHeader"]  { display: none !important; }

/* paleta
   #2F324D fundo | #3D4166 superficie | #424566 superficie-alta | #525680 borda
   #EF6603 acento | #FF8533 acento-suave
   #E8E9F0 texto | #9A9CB8 texto-sec | #6B6D88 muted
*/

[data-testid="stAppViewContainer"] { background: #2F324D; }
[data-testid="stSidebar"]          { background: #252840; }
.block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1380px; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 4px; border-bottom: 2px solid #525680; background: transparent;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-size: 0.82rem !important; font-weight: 600 !important;
    padding: 8px 20px !important; color: #6B6D88 !important;
    border-radius: 6px 6px 0 0 !important;
    border: none !important; background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #EF6603 !important;
    border-bottom: 2px solid #EF6603 !important;
    background: rgba(239,102,3,0.08) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top: 1.2rem !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] input {
    background: #3D4166 !important; border-color: #525680 !important;
    color: #E8E9F0 !important; border-radius: 7px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #EF6603 !important; box-shadow: 0 0 0 2px rgba(239,102,3,0.2) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #6B6D88 !important; }

/* ── Slider ── */
[data-testid="stSlider"] label { font-size: 0.78rem !important; color: #9A9CB8 !important; }

/* ── Checkbox ── */
[data-testid="stCheckbox"] label { font-size: 0.82rem !important; color: #9A9CB8 !important; }

/* ── Separador ── */
.lbr-divider { border: none; border-top: 1px solid #525680; margin: 1rem 0; }
hr { border-color: #525680 !important; }

/* ── Header ── */
.lbr-header { border-bottom: 2px solid #525680; padding-bottom: 1.2rem; margin-bottom: 1rem; }
.lbr-title  { font-size: 1.6rem; font-weight: 700; color: #E8E9F0; margin: 0 0 2px; letter-spacing: -0.3px; }
.lbr-authors { font-size: 0.82rem; color: #9A9CB8; margin: 0 0 2px; }
.lbr-affil  { font-size: 0.75rem; color: #6B6D88; margin: 0; font-style: italic; }
.lbr-subtitle {
    font-size: 0.85rem; color: #C8CAE0; margin: 8px 0 0;
    line-height: 1.6; max-width: 900px;
    background: rgba(239,102,3,0.1); border-left: 3px solid #EF6603;
    padding: 8px 14px; border-radius: 0 6px 6px 0;
}

/* ── Status badge ── */
.lbr-status {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.75rem; font-weight: 600; padding: 4px 12px;
    border-radius: 20px; margin-bottom: 0.8rem; letter-spacing: 0.3px;
}
.lbr-status.on  { background: rgba(239,102,3,0.15); color: #FF8533; border: 1px solid rgba(239,102,3,0.3); }
.lbr-status.off { background: #3D4166; color: #9A9CB8; border: 1px solid #525680; }
.lbr-status .dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }
.lbr-status.on .dot  { background: #EF6603; }
.lbr-status.off .dot { background: #6B6D88; }

/* ── Section headers ── */
.lbr-section {
    font-size: 0.63rem; font-weight: 700; color: #6B6D88;
    text-transform: uppercase; letter-spacing: 2px;
    border-bottom: 1px solid #525680; padding-bottom: 5px;
    margin: 1.4rem 0 0.7rem;
}

/* ── Finger state cards ── */
.lbr-dedos { display: flex; gap: 7px; margin: 10px 0; }
.lbr-dedo {
    flex: 1; background: #3D4166; border: 1.5px solid #525680;
    border-radius: 10px; padding: 11px 4px; text-align: center;
    transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.lbr-dedo.aberto  { border-color: #3A7D55; background: rgba(58,158,98,0.12); }
.lbr-dedo.pouco   { border-color: #7A5200; background: rgba(239,140,3,0.1); }
.lbr-dedo.meio    { border-color: #A84400; background: rgba(239,102,3,0.12); }
.lbr-dedo.fechado { border-color: #EF6603; background: rgba(239,102,3,0.18); }
.lbr-dedo-nome { font-size: 0.58rem; color: #9A9CB8; text-transform: uppercase; letter-spacing: 0.8px; }
.lbr-dedo-icone {
    display: block; margin: 6px auto 4px;
    width: 18px; height: 38px; background: #525680;
    border-radius: 9px; position: relative;
}
.lbr-dedo.aberto  .lbr-dedo-icone { background: linear-gradient(to top, #3A9E62 100%, #525680 100%); }
.lbr-dedo.pouco   .lbr-dedo-icone { background: linear-gradient(to top, #EF8C03 33%, #525680 33%); }
.lbr-dedo.meio    .lbr-dedo-icone { background: linear-gradient(to top, #EF6603 66%, #525680 66%); }
.lbr-dedo.fechado .lbr-dedo-icone { background: linear-gradient(to top, #FF8533 100%, #525680 100%); }
.lbr-dedo-val { font-size: 0.65rem; font-weight: 700; }
.lbr-dedo.aberto  .lbr-dedo-val { color: #3A9E62; }
.lbr-dedo.pouco   .lbr-dedo-val { color: #EF8C03; }
.lbr-dedo.meio    .lbr-dedo-val { color: #EF6603; }
.lbr-dedo.fechado .lbr-dedo-val { color: #FF8533; }

/* ── Legend ── */
.lbr-legend { display: flex; gap: 14px; margin: 5px 0 0; flex-wrap: wrap; font-size: 0.68rem; color: #9A9CB8; }

/* ── Char display ── */
.lbr-char-display {
    background: #3D4166; border: 1.5px solid #525680;
    border-radius: 12px; padding: 18px; text-align: center;
    margin-bottom: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.lbr-char-big {
    font-size: 3rem; font-weight: 700; color: #EF6603;
    line-height: 1; margin-bottom: 2px; font-family: 'JetBrains Mono', monospace;
}
.lbr-char-label { font-size: 0.65rem; color: #6B6D88; text-transform: uppercase; letter-spacing: 1.5px; }

/* ── Badges ── */
.lbr-badges { display: flex; flex-wrap: wrap; gap: 5px; margin: 8px 0; }
.lbr-badge {
    width: 32px; height: 32px; display: inline-flex;
    align-items: center; justify-content: center;
    border-radius: 6px; font-size: 0.85rem; font-weight: 600;
    background: #3D4166; color: #B8BACD; border: 1px solid #525680;
    font-family: 'JetBrains Mono', monospace;
}
.lbr-badge.active {
    background: #EF6603; color: #FFFFFF; border-color: #EF6603;
    transform: scale(1.1); box-shadow: 0 2px 10px rgba(239,102,3,0.45);
}
.lbr-badge.space { width: 12px; background: none; border: 1px dashed #525680; }

/* ── Mic status ── */
.lbr-mic {
    display: flex; align-items: center; gap: 8px;
    padding: 9px 14px; border-radius: 8px; font-size: 0.8rem; margin: 6px 0;
}
.lbr-mic.idle { background: #3D4166; color: #9A9CB8; border: 1px solid #525680; }
.lbr-mic.on   { background: rgba(239,102,3,0.12); color: #FF8533; border: 1px solid rgba(239,102,3,0.3); }
.lbr-mic .pulse {
    width: 7px; height: 7px; border-radius: 50%; background: #EF6603;
    display: inline-block; animation: lbr-pulse 1.2s infinite;
}
@keyframes lbr-pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%     { opacity:0.4; transform:scale(1.5); }
}
.lbr-recognized {
    background: rgba(239,102,3,0.1); border: 1px solid rgba(239,102,3,0.25);
    border-radius: 8px; padding: 9px 14px;
    font-size: 0.82rem; color: #E8E9F0; margin: 6px 0;
}

/* ── Grid ── */
.lbr-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; margin: 8px 0; }
.lbr-grid-cell {
    aspect-ratio: 1; display: flex; align-items: center;
    justify-content: center; border-radius: 5px;
    font-size: 0.75rem; font-weight: 600;
    background: #3D4166; color: #B8BACD; border: 1px solid #525680;
    font-family: 'JetBrains Mono', monospace;
}
.lbr-grid-cell.active { background: #EF6603; color: #FFFFFF; border-color: #EF6603; }

/* ── Botões globais ── */
[data-testid="stButton"] > button {
    border-radius: 7px !important; font-size: 0.82rem !important;
    font-weight: 600 !important; letter-spacing: 0.2px !important;
    padding: 0.45rem 1rem !important;
    border: 1.5px solid #525680 !important;
    background: #3D4166 !important; color: #C8CAE0 !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}
[data-testid="stButton"] > button:hover {
    border-color: #EF6603 !important; color: #FF8533 !important;
    background: rgba(239,102,3,0.1) !important;
    box-shadow: 0 2px 8px rgba(239,102,3,0.2) !important;
}
[data-testid="stButton"] > button:active {
    background: rgba(239,102,3,0.18) !important; transform: translateY(1px) !important;
}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
    background: #EF6603 !important; color: #FFFFFF !important; border-color: #EF6603 !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #FF8533 !important; border-color: #FF8533 !important; color: #FFFFFF !important;
}
[data-testid="stButton"] > button:disabled { opacity: 0.3 !important; cursor: not-allowed !important; }

/* ── Cards ── */
.lbr-card {
    background: #3D4166; border: 1px solid #525680;
    border-radius: 10px; padding: 14px 16px; margin: 8px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.lbr-card h4 { font-size: 0.8rem; font-weight: 600; color: #E8E9F0; margin: 0 0 5px; }
.lbr-card p  { font-size: 0.76rem; color: #9A9CB8; margin: 0; line-height: 1.65; }

/* ── Steps ── */
.lbr-step { display: flex; align-items: flex-start; gap: 11px; margin: 8px 0; }
.lbr-step-num {
    width: 24px; height: 24px; border-radius: 50%;
    background: #EF6603; color: #FFFFFF; font-size: 0.7rem;
    font-weight: 700; display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
}
.lbr-step-text { font-size: 0.8rem; color: #9A9CB8; line-height: 1.55; padding-top: 3px; }
.lbr-step-text strong { color: #E8E9F0; }

/* ── Camera ── */
.lbr-cam-status {
    display: flex; align-items: center; gap: 8px;
    padding: 9px 14px; border-radius: 8px; font-size: 0.8rem; margin: 6px 0;
}
.lbr-cam-status.detecting { background: rgba(239,102,3,0.12); color: #FF8533; border: 1px solid rgba(239,102,3,0.3); }
.lbr-cam-status.waiting   { background: #3D4166; color: #9A9CB8; border: 1px solid #525680; }
.lbr-cam-status .cam-dot {
    width: 7px; height: 7px; border-radius: 50%; display: inline-block; animation: lbr-pulse 1.2s infinite;
}
.lbr-cam-status.detecting .cam-dot { background: #EF6603; }
.lbr-cam-status.waiting .cam-dot   { background: #6B6D88; }

/* ── About ── */
.about-hero {
    background: linear-gradient(135deg, #252840 0%, #1E2038 100%);
    border: 1px solid #525680;
    border-radius: 12px; padding: 14px 26px 14px 56px; margin-bottom: 18px; color: #FFFFFF;
}
.about-hero h1 { font-size: 1.55rem; font-weight: 700; margin: 0 0 4px; color: #FFFFFF; }
.about-hero .tagline { font-size: 0.92rem; color: #EF6603; margin: 0 0 10px; }
.about-hero .abstract {
    font-size: 0.78rem; color: #9A9CB8; line-height: 1.65;
    max-width: 800px; border-top: 1px solid #525680;
    padding-top: 10px; margin-top: 10px;
}
.about-section-title {
    font-size: 0.95rem; font-weight: 700; color: #E8E9F0;
    border-left: 3px solid #EF6603; padding-left: 10px; margin: 24px 0 10px;
}
.about-card {
    background: #3D4166; border: 1px solid #525680;
    border-radius: 10px; padding: 18px 20px; height: 100%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.about-card h4 { font-size: 0.85rem; font-weight: 700; color: #E8E9F0; margin: 0 0 8px; }
.about-card p, .about-card li { font-size: 0.78rem; color: #9A9CB8; line-height: 1.7; margin: 0; }
.about-card ul { padding-left: 16px; margin: 0; }
.about-metric {
    text-align: center; padding: 16px 10px;
    background: #3D4166; border: 1px solid #525680; border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.about-metric .val { font-size: 1.8rem; font-weight: 700; color: #EF6603; line-height: 1; }
.about-metric .lbl { font-size: 0.7rem; color: #6B6D88; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

/* ── Hero Header ── */
.lbr-hero {
    background: #252840;
    border: 1px solid #525680;
    border-top: 3px solid #EF6603;
    border-radius: 12px; padding: 22px 26px;
    margin-bottom: 4px;
}
.lbr-hero-eyebrow {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #EF6603; margin-bottom: 8px;
}
.lbr-hero-title {
    font-size: 1.5rem; font-weight: 700; color: #E8E9F0;
    letter-spacing: 0.5px; line-height: 1.2; margin-bottom: 10px;
}
.lbr-hero-title em { font-style: normal; color: #EF6603; }
.lbr-hero-sub {
    font-size: 0.78rem; color: #6B6D88; line-height: 1.65;
    margin-bottom: 14px;
    border-left: 2px solid #525680; padding-left: 10px;
}
.lbr-hero-sub strong { color: #9A9CB8; font-weight: 500; }

/* ── Conn box ── */
.lbr-conn-box {
    background: #252840; border: 1px solid #525680;
    border-top: 3px solid #525680;
    border-radius: 12px; padding: 16px 18px;
    margin-bottom: 4px;
}
.lbr-hdr-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.7rem; font-weight: 600; padding: 4px 12px;
    border-radius: 4px; letter-spacing: 0.5px; white-space: nowrap;
}
.lbr-hdr-badge.on  { background: rgba(34,197,94,0.1); color: #22C55E; border: 1px solid rgba(34,197,94,0.25); }
.lbr-hdr-badge.off { background: transparent; color: #6B6D88; border: 1px solid #525680; }
.lbr-hdr-badge .dot { width: 5px; height: 5px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.lbr-hdr-badge.on .dot  { background: #22C55E; animation: lbr-pulse 1.8s infinite; }
.lbr-hdr-badge.off .dot { background: #525680; }

/* ── Siga o Sinal ── */
@keyframes lbr-flash {
    0%   { opacity: 1; }
    50%  { opacity: 0; }
    100% { opacity: 1; }
}
.lbr-flash {
    animation: lbr-flash 0.4s ease-in-out 2;
}
.lbr-sinal-target {
    text-align: center;
    background: #3D4166;
    border: 1.5px solid #525680;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 8px;
}
.lbr-sinal-target .letra {
    font-size: 5rem;
    font-weight: 700;
    color: #EF6603;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}
.lbr-sinal-target .instrucao {
    font-size: 0.8rem;
    color: #6B6D88;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 8px;
}
.lbr-sinal-acerto {
    text-align: center;
    background: rgba(34,197,94,0.15);
    border: 1.5px solid rgba(34,197,94,0.4);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 8px;
}
.lbr-sinal-acerto .letra {
    font-size: 5rem;
    font-weight: 700;
    color: #22C55E;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}
.lbr-sinal-acerto .instrucao {
    font-size: 0.8rem;
    color: #22C55E;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 8px;
}
.lbr-grid-done {
    background: rgba(34,197,94,0.15) !important;
    border-color: #22C55E !important;
    color: #22C55E !important;
}

</style>
"""