import streamlit as st

from src.poses import normalize_text, FINGER_ORDER

_STATE_NAME = {0: "aberto", 0.33: "pouco", 0.66: "meio", 1: "fechado"}
_STATE_LABEL = {0: "○ Aberto", 0.33: "◔ Pouco", 0.66: "◑ Meio", 1: "● Fechado"}
_FINGER_PT = {
    "polegar": "Polegar",
    "indicador": "Indicador",
    "medio": "Médio",
    "anelar": "Anelar",
    "minimo": "Mínimo",
}

def _nearest_state(val: float) -> float:
    keys = [0, 0.33, 0.66, 1]
    return min(keys, key=lambda k: abs(k - val))

def render_dedos(pose: dict | None) -> None:
    cards = ""
    for nome in FINGER_ORDER:
        val = pose.get(nome, 0) if pose else 0
        val = _nearest_state(val)
        estado = _STATE_NAME.get(val, "aberto")
        label = _STATE_LABEL.get(val, "○ Aberto")
        cards += f"""
        <div class="lbr-dedo {estado}">
            <div class="lbr-dedo-nome">{_FINGER_PT[nome]}</div>
            <span class="lbr-dedo-icone lbr-dedo-bar"></span>
            <div class="lbr-dedo-val">{label}</div>
        </div>"""
    st.markdown(f'<div class="lbr-dedos">{cards}</div>', unsafe_allow_html=True)

def render_char(char: str) -> None:
    display = char.upper() if char and char.strip() else "—"
    label = "sinal atual" if char and char.strip() else "repouso"
    st.markdown(f"""
    <div class="lbr-char-display">
        <div class="lbr-char-big">{display}</div>
        <div class="lbr-char-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def render_badges(text: str, active: str = "") -> None:
    norm = normalize_text(text)
    html = ""
    for c in norm:
        if c == " ":
            html += '<span class="lbr-badge space"></span>'
        else:
            cls = "active" if c.upper() == active.upper() and active.strip() else ""
            html += f'<span class="lbr-badge {cls}">{c.upper()}</span>'
    st.markdown(f'<div class="lbr-badges">{html}</div>', unsafe_allow_html=True)

def render_legend() -> None:
    st.markdown("""
    <div class="lbr-legend">
        <span style="color:#16A34A;font-weight:600">○ Aberto</span>
        <span style="color:#CA8A04;font-weight:600">◔ Pouco</span>
        <span style="color:#EA580C;font-weight:600">◑ Meio</span>
        <span style="color:#DC2626;font-weight:600">● Fechado</span>
    </div>""", unsafe_allow_html=True)