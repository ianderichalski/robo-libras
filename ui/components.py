import base64
import os
from functools import lru_cache

import streamlit as st

from src.poses import normalize_text, FINGER_ORDER

_STATE_NAME = {0: "aberto", 0.33: "pouco", 0.66: "meio", 1: "fechado"}
_STATE_LABEL = {0: "Aberto", 0.33: "Pouco", 0.66: "Meio", 1: "Fechado"}
_FINGER_PT = {
    "polegar": "Polegar",
    "indicador": "Indicador",
    "medio": "Médio",
    "anelar": "Anelar",
    "minimo": "Mínimo",
}

INES_URL = "https://dicionario.ines.gov.br"

def _nearest_state(val: float) -> float:
    keys = [0, 0.33, 0.66, 1]
    return min(keys, key=lambda k: abs(k - val))

@lru_cache(maxsize=64)
def img_b64(path: str) -> str:
    """Lê uma imagem e devolve data-URI (com cache)."""
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"

def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)

def section(title: str) -> None:
    html(f'<div class="lbr-section">{title}</div>')

def render_sign(char: str, tag: str | None = None, tag_cls: str = "", link: bool = True) -> None:
    """Cartão com a foto do sinal + etiqueta da letra no canto."""
    src = img_b64(os.path.join("docs", "alphabet", f"{char}.jpg"))
    tag_html = f'<div class="tag {tag_cls}">{tag}</div>' if tag else ""
    img_html = f'<img src="{src}" alt="Sinal da letra">' if src else '<div style="height:200px"></div>'
    link_html = (
        f'<a class="link" href="{INES_URL}" target="_blank">Ver movimento no Dicionário INES/MEC ↗</a>'
        if link else ""
    )
    html(f'<div class="lbr-sign">{tag_html}{img_html}{link_html}</div>')

def render_sign_img(char: str, link: bool = True) -> None:
    src = img_b64(os.path.join("docs", "alphabet", f"{char}.jpg"))
    if not src:
        return
    link_html = f'<a href="{INES_URL}" target="_blank">Ver movimento no Dicionário INES/MEC ↗</a>' if link else ""
    html(f'<div class="lbr-sign-img"><img src="{src}" alt="Sinal da letra">{link_html}</div>')

def render_progress(title: str, done: int, total: int, color: str = "") -> None:
    pct = int(done / total * 100) if total else 0
    html(f"""
    <div class="lbr-card">
        <div class="lbr-progress-head">
            <span class="t">{title}</span>
            <span class="n">{done}/{total}</span>
        </div>
        <div class="lbr-bar {color}"><div style="width:{pct}%"></div></div>
    </div>""")

def steps_html(steps: list[str]) -> str:
    items = "".join(
        f'<div class="lbr-step"><div class="lbr-step-num">{i}</div>'
        f'<div class="lbr-step-text">{s}</div></div>'
        for i, s in enumerate(steps, 1)
    )
    return f'<div class="lbr-steps">{items}</div>'

def render_steps(steps: list[str]) -> None:
    html(steps_html(steps))

_EMPTY_ICONS = {
    "camera": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"><path d="M15.5 9.5 21 6.5v11l-5.5-3"/>
        <rect x="3" y="6" width="12.5" height="12" rx="2.5"/></svg>""",
    "loading": """<svg class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round"><path d="M21 12a9 9 0 1 1-6.2-8.56"/></svg>""",
}

_TIP_ICONS = {
    "sun":  '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "hand": '<path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-6-2.4l-3.6-3.6a2 2 0 0 1 2.8-2.8L7 15"/>',
    "slow": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "usb":  '<path d="M12 2v14M12 2l-3 3M12 2l3 3"/><circle cx="12" cy="19" r="2.5"/><path d="M12 12 7 9V7M12 14l5-3V9"/>',
}

def render_tips(tips: list[tuple[str, str, str]]) -> None:
    items = "".join(
        f'''<div class="lbr-tip"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{_TIP_ICONS.get(ic, "")}</svg></div>
            <div><div class="t">{t}</div><div class="d">{d}</div></div></div>'''
        for ic, t, d in tips
    )
    html(f'<div class="lbr-tips">{items}</div>')

def render_notice(texto: str) -> None:
    html(f"""
    <div class="lbr-notice">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
            stroke-linejoin="round"><path d="M12 2v14M12 2l-3 3M12 2l3 3"/><circle cx="12" cy="19" r="2.5"/>
            <path d="M12 12 7 9V7M12 14l5-3V9"/></svg>
        <span>{texto}</span>
    </div>""")

def render_empty(icon: str, text: str) -> None:
    """Card vazio com ícone de linha (icon = "camera" ou "loading")."""
    svg = _EMPTY_ICONS.get(icon, _EMPTY_ICONS["camera"])
    html(f'<div class="lbr-card lbr-empty"><div class="ico">{svg}</div><p>{text}</p></div>')

def render_dedos(pose: dict | None) -> None:
    cards = ""
    for nome in FINGER_ORDER:
        val = pose.get(nome, 0) if pose else 0
        val = _nearest_state(val)
        estado = _STATE_NAME.get(val, "aberto")
        label = _STATE_LABEL.get(val, "Aberto")
        cards += f"""
        <div class="lbr-dedo {estado}">
            <div class="lbr-dedo-nome">{_FINGER_PT[nome]}</div>
            <span class="lbr-dedo-bar"></span>
            <div class="lbr-dedo-val">{label}</div>
        </div>"""
    html(f'<div class="lbr-dedos">{cards}</div>')

def render_char(char: str, label: str | None = None) -> None:
    has = bool(char and char.strip())
    display = char.upper() if has else "—"
    label = label or ("sinal atual" if has else "repouso")
    idle = "" if has else "idle"
    html(f"""
    <div class="lbr-char-display {idle}">
        <div class="lbr-char-big">{display}</div>
        <div class="lbr-char-label">{label}</div>
    </div>""")

def render_badges(text: str, active: str = "") -> None:
    norm = normalize_text(text)
    out = ""
    for c in norm:
        if c == " ":
            out += '<span class="lbr-badge space"></span>'
        else:
            cls = "active" if c.upper() == active.upper() and active.strip() else ""
            out += f'<span class="lbr-badge {cls}">{c.upper()}</span>'
    html(f'<div class="lbr-badges">{out}</div>')

def render_legend() -> None:
    html("""
    <div class="lbr-legend">
        <span class="aberto">Aberto</span>
        <span class="pouco">Pouco</span>
        <span class="meio">Meio</span>
        <span class="fechado">Fechado</span>
    </div>""")