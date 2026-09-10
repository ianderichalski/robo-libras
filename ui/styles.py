import streamlit as st

_DARK = {
    "bg":          "#2F324D",
    "sidebar":     "#252840",
    "surface":     "#3D4166",
    "surface_hi":  "#424566",
    "border":      "#525680",
    "accent":      "#EF6603",
    "accent_soft": "#FF8533",
    "text":        "#E8E9F0",
    "text_sec":    "#9A9CB8",
    "muted":       "#6B6D88",
    "text_hover":  "#C8CAE0",
    "green":       "#22C55E",
    "green_bg":    "rgba(34,197,94,0.15)",
    "green_bd":    "rgba(34,197,94,0.4)",
    "hero_bg":     "#252840",
    "about_bg1":   "#252840",
    "about_bg2":   "#1E2038",
}

_LIGHT = {
    "bg":          "#FFF5F8",
    "sidebar":     "#FFE8EF",
    "surface":     "#FFFFFF",
    "surface_hi":  "#FFF9FB",
    "border":      "#F0D0DA",
    "accent":      "#EF6603",
    "accent_soft": "#FF8533",
    "text":        "#2A0A14",
    "text_sec":    "#6B2D40",
    "muted":       "#B07080",
    "text_hover":  "#1A0008",
    "green":       "#16A34A",
    "green_bg":    "rgba(22,163,74,0.10)",
    "green_bd":    "rgba(22,163,74,0.30)",
    "hero_bg":     "#FFFFFF",
    "about_bg1":   "#FFF9FB",
    "about_bg2":   "#FFE8EF",
}

# builder

def _build_css(p: dict) -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {{
    --lbr-bg:       {p["bg"]};
    --lbr-surface:  {p["surface"]};
    --lbr-hero:     {p["hero_bg"]};
    --lbr-border:   {p["border"]};
    --lbr-text:     {p["text"]};
    --lbr-text-sec: {p["text_sec"]};
    --lbr-muted:    {p["muted"]};
    --lbr-accent:   {p["accent"]};
}}

* {{ font-family: 'Inter', sans-serif; }}

[data-testid="stToolbar"]      {{ display: none !important; }}
[data-testid="stDecoration"]   {{ display: none !important; }}
[data-testid="stStatusWidget"] {{ display: none !important; }}
header[data-testid="stHeader"] {{ display: none !important; }}

[data-testid="stAppViewContainer"] {{ background: {p["bg"]}; }}
[data-testid="stSidebar"]          {{ background: {p["sidebar"]}; }}
.block-container {{ padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1380px; }}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    gap: 0px; border-bottom: 1px solid {p["border"]} !important;
    background: transparent; padding: 0; justify-content: center; width: 100%;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 10px 28px !important; color: {p["muted"]} !important;
    border-radius: 0 !important; border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important; transition: all 0.15s ease !important;
    letter-spacing: 0.5px !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {{
    color: {p["text_hover"]} !important; border-bottom: 2px solid {p["border"]} !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: {p["accent"]} !important; border-bottom: 2px solid {p["accent"]} !important;
    background: transparent !important; box-shadow: none !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}

/* ── Inputs ── */
[data-testid="stTextInput"] input {{
    background: {p["surface"]} !important; border-color: {p["border"]} !important;
    color: {p["text"]} !important; border-radius: 7px !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: {p["accent"]} !important; box-shadow: 0 0 0 2px rgba(239,102,3,0.2) !important;
}}
[data-testid="stTextInput"] input::placeholder {{ color: {p["muted"]} !important; }}

/* ── Selectbox ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
    background: {p["surface"]} !important; border-color: {p["border"]} !important;
    color: {p["text"]} !important; border-radius: 7px !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] label {{ font-size: 0.78rem !important; color: {p["text_sec"]} !important; }}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {{ font-size: 0.82rem !important; color: {p["text_sec"]} !important; }}

/* ── Separador ── */
.lbr-divider {{ border: none; border-top: 1px solid {p["border"]}; margin: 1rem 0; }}
hr {{ border-color: {p["border"]} !important; }}

/* ── Header ── */
.lbr-header {{ border-bottom: 2px solid {p["border"]}; padding-bottom: 1.2rem; margin-bottom: 1rem; }}
.lbr-title  {{ font-size: 1.6rem; font-weight: 700; color: {p["text"]}; margin: 0 0 2px; letter-spacing: -0.3px; }}
.lbr-authors {{ font-size: 0.82rem; color: {p["text_sec"]}; margin: 0 0 2px; }}
.lbr-affil  {{ font-size: 0.75rem; color: {p["muted"]}; margin: 0; font-style: italic; }}
.lbr-subtitle {{
    font-size: 0.85rem; color: {p["text_hover"]}; margin: 8px 0 0;
    line-height: 1.6; max-width: 900px;
    background: rgba(239,102,3,0.1); border-left: 3px solid {p["accent"]};
    padding: 8px 14px; border-radius: 0 6px 6px 0;
}}

/* ── Status badge ── */
.lbr-status {{
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.75rem; font-weight: 600; padding: 4px 12px;
    border-radius: 20px; margin-bottom: 0.8rem; letter-spacing: 0.3px;
}}
.lbr-status.on  {{ background: rgba(239,102,3,0.15); color: {p["accent_soft"]}; border: 1px solid rgba(239,102,3,0.3); }}
.lbr-status.off {{ background: {p["surface"]}; color: {p["text_sec"]}; border: 1px solid {p["border"]}; }}
.lbr-status .dot {{ width: 6px; height: 6px; border-radius: 50%; display: inline-block; }}
.lbr-status.on .dot  {{ background: {p["accent"]}; }}
.lbr-status.off .dot {{ background: {p["muted"]}; }}

/* ── Section headers ── */
.lbr-section {{
    font-size: 0.63rem; font-weight: 700; color: {p["muted"]};
    text-transform: uppercase; letter-spacing: 2px;
    border-bottom: 1px solid {p["border"]}; padding-bottom: 5px;
    margin: 1.4rem 0 0.7rem;
}}

/* ── Finger state cards ── */
.lbr-dedos {{ display: flex; gap: 7px; margin: 10px 0; }}
.lbr-dedo {{
    flex: 1; background: {p["surface"]}; border: 1.5px solid {p["border"]};
    border-radius: 10px; padding: 11px 4px; text-align: center;
    transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}
.lbr-dedo.aberto  {{ border-color: #3A7D55; background: rgba(58,158,98,0.12); }}
.lbr-dedo.pouco   {{ border-color: #7A5200; background: rgba(239,140,3,0.1); }}
.lbr-dedo.meio    {{ border-color: #A84400; background: rgba(239,102,3,0.12); }}
.lbr-dedo.fechado {{ border-color: {p["accent"]}; background: rgba(239,102,3,0.18); }}
.lbr-dedo-nome {{ font-size: 0.58rem; color: {p["text_sec"]}; text-transform: uppercase; letter-spacing: 0.8px; }}
.lbr-dedo-icone {{
    display: block; margin: 6px auto 4px;
    width: 18px; height: 38px; background: {p["border"]};
    border-radius: 9px; position: relative;
}}
.lbr-dedo.aberto  .lbr-dedo-icone {{ background: linear-gradient(to top, #3A9E62 100%, {p["border"]} 100%); }}
.lbr-dedo.pouco   .lbr-dedo-icone {{ background: linear-gradient(to top, #EF8C03 33%, {p["border"]} 33%); }}
.lbr-dedo.meio    .lbr-dedo-icone {{ background: linear-gradient(to top, #EF6603 66%, {p["border"]} 66%); }}
.lbr-dedo.fechado .lbr-dedo-icone {{ background: linear-gradient(to top, #FF8533 100%, {p["border"]} 100%); }}
.lbr-dedo-val {{ font-size: 0.65rem; font-weight: 700; }}
.lbr-dedo.aberto  .lbr-dedo-val {{ color: #3A9E62; }}
.lbr-dedo.pouco   .lbr-dedo-val {{ color: #EF8C03; }}
.lbr-dedo.meio    .lbr-dedo-val {{ color: #EF6603; }}
.lbr-dedo.fechado .lbr-dedo-val {{ color: #FF8533; }}

/* ── Legend ── */
.lbr-legend {{ display: flex; gap: 14px; margin: 5px 0 0; flex-wrap: wrap; font-size: 0.68rem; color: {p["text_sec"]}; }}

/* ── Char display ── */
.lbr-char-display {{
    background: {p["surface"]}; border: 1.5px solid {p["border"]};
    border-radius: 12px; padding: 18px; text-align: center;
    margin-bottom: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
.lbr-char-big {{
    font-size: 3rem; font-weight: 700; color: {p["accent"]};
    line-height: 1; margin-bottom: 2px; font-family: 'JetBrains Mono', monospace;
}}
.lbr-char-label {{ font-size: 0.65rem; color: {p["muted"]}; text-transform: uppercase; letter-spacing: 1.5px; }}

/* ── Badges ── */
.lbr-badges {{ display: flex; flex-wrap: wrap; gap: 5px; margin: 8px 0; }}
.lbr-badge {{
    width: 32px; height: 32px; display: inline-flex;
    align-items: center; justify-content: center;
    border-radius: 6px; font-size: 0.85rem; font-weight: 600;
    background: {p["surface"]}; color: {p["text_sec"]}; border: 1px solid {p["border"]};
    font-family: 'JetBrains Mono', monospace;
}}
.lbr-badge.active {{
    background: {p["accent"]}; color: #FFFFFF; border-color: {p["accent"]};
    transform: scale(1.1); box-shadow: 0 2px 10px rgba(239,102,3,0.45);
}}
.lbr-badge.space {{ width: 12px; background: none; border: 1px dashed {p["border"]}; }}

/* ── Mic status ── */
.lbr-mic {{
    display: flex; align-items: center; gap: 8px;
    padding: 9px 14px; border-radius: 8px; font-size: 0.8rem; margin: 6px 0;
}}
.lbr-mic.idle {{ background: {p["surface"]}; color: {p["text_sec"]}; border: 1px solid {p["border"]}; }}
.lbr-mic.on   {{ background: rgba(239,102,3,0.12); color: {p["accent_soft"]}; border: 1px solid rgba(239,102,3,0.3); }}
.lbr-mic .pulse {{
    width: 7px; height: 7px; border-radius: 50%; background: {p["accent"]};
    display: inline-block; animation: lbr-pulse 1.2s infinite;
}}
@keyframes lbr-pulse {{
    0%,100% {{ opacity:1; transform:scale(1); }}
    50%     {{ opacity:0.4; transform:scale(1.5); }}
}}
.lbr-recognized {{
    background: rgba(239,102,3,0.1); border: 1px solid rgba(239,102,3,0.25);
    border-radius: 8px; padding: 9px 14px;
    font-size: 0.82rem; color: {p["text"]}; margin: 6px 0;
}}

/* ── Grid ── */
.lbr-grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; margin: 8px 0; }}
.lbr-grid-cell {{
    aspect-ratio: 1; display: flex; align-items: center;
    justify-content: center; border-radius: 5px;
    font-size: 0.75rem; font-weight: 600;
    background: {p["surface"]}; color: {p["text_sec"]}; border: 1px solid {p["border"]};
    font-family: 'JetBrains Mono', monospace;
}}
.lbr-grid-cell.active {{ background: {p["accent"]}; color: #FFFFFF; border-color: {p["accent"]}; }}

/* ── Botões globais ── */
[data-testid="stButton"] > button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-minimal"] {{
    border-radius: 7px !important; font-size: 0.82rem !important;
    font-weight: 600 !important; letter-spacing: 0.2px !important;
    padding: 0.45rem 1rem !important;
    border: 1.5px solid {p["border"]} !important;
    background: {p["surface"]} !important; color: {p["text_hover"]} !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}}
[data-testid="stButton"] > button:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-minimal"]:hover {{
    border-color: {p["accent"]} !important; color: {p["accent_soft"]} !important;
    background: rgba(239,102,3,0.1) !important;
    box-shadow: 0 2px 8px rgba(239,102,3,0.2) !important;
}}
[data-testid="stButton"] > button:active {{
    background: rgba(239,102,3,0.18) !important; transform: translateY(1px) !important;
}}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stButton"] > button[data-testid="baseButton-primary"],
[data-testid="stBaseButton-primary"] {{
    background: {p["accent"]} !important; color: #FFFFFF !important; border-color: {p["accent"]} !important;
}}
[data-testid="stButton"] > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {{
    background: {p["accent_soft"]} !important; border-color: {p["accent_soft"]} !important; color: #FFFFFF !important;
}}
[data-testid="stButton"] > button:disabled {{ opacity: 0.3 !important; cursor: not-allowed !important; }}

/* ── Cards ── */
.lbr-card {{
    background: {p["surface"]}; border: 1px solid {p["border"]};
    border-radius: 12px; padding: 14px 16px; margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08), 0 0 0 1px {p["border"]};
}}
.lbr-card h4 {{ font-size: 0.8rem; font-weight: 700; color: {p["text"]}; margin: 0 0 5px; }}
.lbr-card p  {{ font-size: 0.76rem; color: {p["text_sec"]}; margin: 0; line-height: 1.65; }}

/* ── Steps ── */
.lbr-step {{ display: flex; align-items: flex-start; gap: 11px; margin: 8px 0; }}
.lbr-step-num {{
    width: 24px; height: 24px; border-radius: 50%;
    background: {p["accent"]}; color: #FFFFFF; font-size: 0.7rem;
    font-weight: 700; display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
}}
.lbr-step-text {{ font-size: 0.8rem; color: {p["text_sec"]}; line-height: 1.55; padding-top: 3px; }}
.lbr-step-text strong {{ color: {p["text"]}; }}

/* ── Camera ── */
.lbr-cam-status {{
    display: flex; align-items: center; gap: 8px;
    padding: 9px 14px; border-radius: 8px; font-size: 0.8rem; margin: 6px 0;
}}
.lbr-cam-status.detecting {{ background: rgba(239,102,3,0.12); color: {p["accent_soft"]}; border: 1px solid rgba(239,102,3,0.3); }}
.lbr-cam-status.waiting   {{ background: {p["surface"]}; color: {p["text_sec"]}; border: 1px solid {p["border"]}; }}
.lbr-cam-status .cam-dot {{
    width: 7px; height: 7px; border-radius: 50%; display: inline-block; animation: lbr-pulse 1.2s infinite;
}}
.lbr-cam-status.detecting .cam-dot {{ background: {p["accent"]}; }}
.lbr-cam-status.waiting .cam-dot   {{ background: {p["muted"]}; }}

/* ── About ── */
.about-hero {{
    background: linear-gradient(135deg, {p["about_bg1"]} 0%, {p["about_bg2"]} 100%);
    border: 1px solid {p["border"]};
    border-radius: 12px; padding: 14px 26px 14px 56px; margin-bottom: 18px; color: {p["text"]};
}}
.about-hero h1 {{ font-size: 1.55rem; font-weight: 700; margin: 0 0 4px; color: {p["text"]}; }}
.about-hero .tagline {{ font-size: 0.92rem; color: {p["accent"]}; margin: 0 0 10px; }}
.about-hero .abstract {{
    font-size: 0.78rem; color: {p["text_sec"]}; line-height: 1.65;
    max-width: 800px; border-top: 1px solid {p["border"]};
    padding-top: 10px; margin-top: 10px;
}}
.about-section-title {{
    font-size: 0.95rem; font-weight: 700; color: {p["text"]};
    border-left: 3px solid {p["accent"]}; padding-left: 10px; margin: 24px 0 10px;
}}
.about-card {{
    background: {p["surface"]}; border: 1px solid {p["border"]};
    border-radius: 10px; padding: 18px 20px; height: 100%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
.about-card h4 {{ font-size: 0.85rem; font-weight: 700; color: {p["text"]}; margin: 0 0 8px; }}
.about-card p, .about-card li {{ font-size: 0.78rem; color: {p["text_sec"]}; line-height: 1.7; margin: 0; }}
.about-card ul {{ padding-left: 16px; margin: 0; }}
.about-metric {{
    text-align: center; padding: 16px 10px;
    background: {p["surface"]}; border: 1px solid {p["border"]}; border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}}
.about-metric .val {{ font-size: 1.8rem; font-weight: 700; color: {p["accent"]}; line-height: 1; }}
.about-metric .lbl {{ font-size: 0.7rem; color: {p["muted"]}; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}

/* ── Hero Header ── */
.lbr-hero {{
    background: {p["hero_bg"]};
    border: 1px solid {p["border"]};
    border-top: 3px solid {p["accent"]};
    border-radius: 12px; padding: 22px 26px; margin-bottom: 4px;
}}
.lbr-hero-eyebrow {{
    font-size: 0.6rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: {p["accent"]}; margin-bottom: 8px;
}}
.lbr-hero-title {{
    font-size: 1.5rem; font-weight: 700; color: {p["text"]};
    letter-spacing: 0.5px; line-height: 1.2; margin-bottom: 10px;
}}
.lbr-hero-title em {{ font-style: normal; color: {p["accent"]}; }}
.lbr-hero-sub {{
    font-size: 0.78rem; color: {p["muted"]}; line-height: 1.65;
    margin-bottom: 14px; border-left: 2px solid {p["border"]}; padding-left: 10px;
}}
.lbr-hero-sub strong {{ color: {p["text_sec"]}; font-weight: 500; }}

/* ── Conn box ── */
.lbr-conn-box {{
    background: {p["hero_bg"]}; border: 1px solid {p["border"]};
    border-top: 3px solid {p["border"]};
    border-radius: 12px; padding: 16px 18px; margin-bottom: 4px;
}}
.lbr-hdr-badge {{
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.7rem; font-weight: 600; padding: 4px 12px;
    border-radius: 4px; letter-spacing: 0.5px; white-space: nowrap;
}}
.lbr-hdr-badge.on  {{ background: rgba(34,197,94,0.1); color: {p["green"]}; border: 1px solid rgba(34,197,94,0.25); }}
.lbr-hdr-badge.off {{ background: transparent; color: {p["muted"]}; border: 1px solid {p["border"]}; }}
.lbr-hdr-badge .dot {{ width: 5px; height: 5px; border-radius: 50%; display: inline-block; flex-shrink: 0; }}
.lbr-hdr-badge.on .dot  {{ background: {p["green"]}; animation: lbr-pulse 1.8s infinite; }}
.lbr-hdr-badge.off .dot {{ background: {p["border"]}; }}

/* ── Expander ── */
[data-testid="stExpander"],
[data-testid="stExpander"] > details,
[data-testid="stExpander"] > details > summary,
[data-testid="stExpander"] > details > div {{
    background: {p["surface"]} !important;
    border-color: {p["border"]} !important;
}}
[data-testid="stExpander"] > details > summary {{
    color: {p["text_sec"]} !important;
    border-radius: 8px !important;
}}
[data-testid="stExpander"] > details > summary:hover {{
    color: {p["accent"]} !important;
}}
[data-testid="stExpander"] > details[open] > summary {{
    border-bottom: 1px solid {p["border"]} !important;
    border-radius: 8px 8px 0 0 !important;
}}

/* ── Segmented Control ── */
div[data-baseweb="button-group"] {{
    background: {p["surface"]} !important;
    border: 1px solid {p["border"]} !important;
    border-radius: 8px !important;
    padding: 3px !important;
    gap: 2px !important;
}}
button[kind="segmented_control"] {{
    background: transparent !important;
    color: {p["text_sec"]} !important;
    border: none !important;
    border-radius: 6px !important;
}}
button[kind="segmented_control"]:hover {{
    background: rgba(239,102,3,0.1) !important;
    color: {p["accent"]} !important;
}}
button[kind="segmented_controlActive"] {{
    background: {p["accent"]} !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 6px !important;
}}
button[kind="segmented_controlActive"]:hover {{
    background: {p["accent_soft"]} !important;
    color: #FFFFFF !important;
}}
@keyframes lbr-flash {{
    0%   {{ opacity: 1; }}
    50%  {{ opacity: 0; }}
    100% {{ opacity: 1; }}
}}
.lbr-flash {{ animation: lbr-flash 0.4s ease-in-out 2; }}
.lbr-sinal-target {{
    text-align: center; background: {p["surface"]};
    border: 1.5px solid {p["border"]}; border-radius: 12px;
    padding: 24px; margin-bottom: 8px;
}}
.lbr-sinal-target .letra {{
    font-size: 5rem; font-weight: 700; color: {p["accent"]};
    line-height: 1; font-family: 'JetBrains Mono', monospace;
}}
.lbr-sinal-target .instrucao {{
    font-size: 0.8rem; color: {p["muted"]};
    text-transform: uppercase; letter-spacing: 1.5px; margin-top: 8px;
}}
.lbr-sinal-acerto {{
    text-align: center; background: {p["green_bg"]};
    border: 1.5px solid {p["green_bd"]}; border-radius: 12px;
    padding: 24px; margin-bottom: 8px;
}}
.lbr-sinal-acerto .letra {{
    font-size: 5rem; font-weight: 700; color: {p["green"]};
    line-height: 1; font-family: 'JetBrains Mono', monospace;
}}
.lbr-sinal-acerto .instrucao {{
    font-size: 0.8rem; color: {p["green"]};
    text-transform: uppercase; letter-spacing: 1.5px; margin-top: 8px;
}}
.lbr-grid-done {{
    background: {p["green_bg"]} !important;
    border-color: {p["green"]} !important;
    color: {p["green"]} !important;
}}
</style>
"""

# inject

def inject() -> None:
    theme = st.session_state.get("theme", "dark")
    palette = _DARK if theme == "dark" else _LIGHT
    st.markdown(_build_css(palette), unsafe_allow_html=True)


def toggle() -> None:
    """Alterna entre dark e light e força rerun."""
    st.session_state.theme = "light" if st.session_state.get("theme", "dark") == "dark" else "dark"

def palette() -> dict:
    """Retorna a paleta ativa para uso em HTML inline."""
    theme = st.session_state.get("theme", "dark")
    return _DARK if theme == "dark" else _LIGHT