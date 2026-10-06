import streamlit as st

_LIGHT = {
    "bg":            "#F6F5FB",
    "bg_grad":       "#FFF4EA",
    "surface":       "#FFFFFF",
    "surface_2":     "#F3F2F9",
    "border":        "#E5E3F0",
    "border_strong": "#D4D1E4",
    "text":          "#22233D",
    "text_sec":      "#5C5E7E",
    "muted":         "#73759A",
    "accent":        "#EF6603",
    "accent_dark":   "#C25000",
    "accent_soft":   "#FFF0E3",
    "accent_line":   "#FFD3B0",
    "green":         "#16874A",
    "green_dark":    "#168246",
    "green_soft":    "#E4F7EC",
    "red":           "#D93A40",
    "red_dark":      "#B9363A",
    "red_soft":      "#FDECEC",
    "yellow":        "#B07D00",
    "yellow_soft":   "#FFF6DB",
    "blue":          "#2F80ED",
    "blue_dark":     "#1F62C0",
    "blue_soft":     "#E7F0FE",
    "purple":        "#8B5CF6",
    "purple_dark":   "#6D3FDB",
    "purple_soft":   "#F1EBFF",
    "pink":          "#E8457C",
    "pink_dark":     "#BF2E60",
    "pink_soft":     "#FDE9F0",
    "shadow":        "0 1px 2px rgba(34,35,61,.04), 0 4px 12px rgba(34,35,61,.05)",
    "on_accent":     "#FFFFFF",
    "green_btn":     "#1FA45A",
    "shadow_sm":     "0 1px 2px rgba(34,35,61,.08)",
}

_DARK = {
    "bg":            "#23263D",
    "bg_grad":       "#2B2540",
    "surface":       "#2F3352",
    "surface_2":     "#292C48",
    "border":        "#40456E",
    "border_strong": "#1A1C31",
    "text":          "#EEEFF7",
    "text_sec":      "#A9ACCB",
    "muted":         "#7A7DA3",
    "accent":        "#EF6603",
    "accent_dark":   "#A34400",
    "accent_soft":   "rgba(239,102,3,.16)",
    "accent_line":   "rgba(239,102,3,.45)",
    "green":         "#35C574",
    "green_dark":    "#1E8A4D",
    "green_soft":    "rgba(53,197,116,.15)",
    "red":           "#F2575C",
    "red_dark":      "#A8333A",
    "red_soft":      "rgba(242,87,92,.15)",
    "yellow":        "#F5B82E",
    "yellow_soft":   "rgba(245,184,46,.15)",
    "blue":          "#5B9BFF",
    "blue_dark":     "#2F6AD0",
    "blue_soft":     "rgba(91,155,255,.15)",
    "purple":        "#A17BFF",
    "purple_dark":   "#6E47D6",
    "purple_soft":   "rgba(161,123,255,.16)",
    "pink":          "#FF6B9A",
    "pink_dark":     "#C23E6C",
    "pink_soft":     "rgba(255,107,154,.15)",
    "shadow":        "0 1px 2px rgba(0,0,0,.18), 0 4px 14px rgba(0,0,0,.14)",
    "on_accent":     "#FFFFFF",
    "green_btn":     "#1C8F4F",
    "shadow_sm":     "0 1px 3px rgba(0,0,0,.28)",
}


def _vars(p: dict) -> str:
    return "\n".join(f"    --lbr-{k.replace('_', '-')}: {v};" for k, v in p.items())


_FONT = "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');"

_CSS = """
/* ── Base ─────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"],
button, input, textarea, select, label, p, li, h1, h2, h3, h4 {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
}
[data-testid="stIconMaterial"], .material-symbols-rounded {
    font-family: 'Material Symbols Rounded' !important;
}

[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], header[data-testid="stHeader"] { display: none !important; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(1200px 380px at 50% -120px, var(--lbr-bg-grad), transparent 70%),
        var(--lbr-bg);
    color: var(--lbr-text);
}
[data-testid="stSidebar"] { background: var(--lbr-surface-2); }
.block-container { padding-top: 1.1rem !important; padding-bottom: 3rem !important; max-width: 1320px; }

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: var(--lbr-text-sec); }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--lbr-muted) !important; }
[data-testid="stWidgetLabel"] p { color: var(--lbr-text-sec) !important; font-weight: 700 !important; font-size: .9rem !important; }
a { color: var(--lbr-accent); }

/* ── Cabeçalho ─────────────────────────────────────────── */
.lbr-brand { display: flex; align-items: center; gap: 12px; }
.lbr-brand img { width: 46px; height: 46px; border-radius: 10px; background: var(--lbr-surface);
    border: 1px solid var(--lbr-border); padding: 4px; }
.lbr-brand-name { font-size: 1.45rem; font-weight: 800; color: var(--lbr-text); letter-spacing: -.3px; line-height: 1; }
.lbr-brand-name span { color: var(--lbr-accent); }
.lbr-brand-sub { font-size: .74rem; font-weight: 700; color: var(--lbr-muted); margin-top: 3px; }

.lbr-hdr-right { display: flex; justify-content: flex-end; }
.lbr-hdr-badge {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: .8rem; font-weight: 800; padding: 8px 14px;
    border-radius: 999px; white-space: nowrap; border: 1px solid;
}
.lbr-hdr-badge.on  { background: var(--lbr-green-soft); color: var(--lbr-green); border-color: var(--lbr-green); }
.lbr-hdr-badge.off { background: var(--lbr-surface); color: var(--lbr-muted); border-color: var(--lbr-border); }
.lbr-hdr-badge .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.lbr-hdr-badge.on .dot  { background: var(--lbr-green); animation: lbr-pulse 1.8s infinite; }
.lbr-hdr-badge.off .dot { background: var(--lbr-border-strong); }

.st-key-lbr_header { margin-bottom: .4rem; }

/* ── Navegação principal (segmented control "nav") ─────── */
.st-key-nav [data-testid="stButtonGroup"] { display: flex; justify-content: center; }
.st-key-nav [role="radiogroup"] { flex-wrap: nowrap !important; }
.st-key-nav [role="radiogroup"] {
    background: var(--lbr-surface) !important; border: 1px solid var(--lbr-border) !important;
    border-radius: 14px !important; padding: 5px !important; gap: 4px !important;
    box-shadow: var(--lbr-shadow);
}
.st-key-nav button[data-variant="segmented_control"],
.st-key-nav [data-testid^="stBaseButton-segmented_control"] {
    font-size: 1rem !important; padding: .55rem 1.25rem !important; min-height: 44px;
    border-radius: 10px !important;
}
.st-key-nav button[data-variant="segmented_control"] p,
.st-key-nav [data-testid^="stBaseButton-segmented_control"] p { font-size: 1rem !important; font-weight: 800 !important; }

/* selo na seção de configuração da tela Início */
.lbr-conn-badge { margin-bottom: 10px; }

/* ── Segmented control (todos) ─────────────────────────── */
/* cada regra cobre o HTML do Streamlit novo (data-variant) e do antigo (kind / data-testid) */
[data-testid^="stBaseButton-segmented_control"] { gap: 6px !important; }
[data-testid^="stBaseButton-segmented_control"] [data-testid="stIconMaterial"] { margin-right: 2px; }
[data-testid="stButtonGroup"] [role="radiogroup"] {
    background: var(--lbr-surface-2); border: 1px solid var(--lbr-border);
    border-radius: 10px; padding: 4px; gap: 4px; width: fit-content;
}
button[data-variant="segmented_control"],
[data-testid^="stBaseButton-segmented_control"] {
    background: transparent !important; color: var(--lbr-text-sec) !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 800 !important; padding: .4rem 1rem !important;
    transition: background .15s ease, color .15s ease !important;
}
button[data-variant="segmented_control"] p,
[data-testid^="stBaseButton-segmented_control"] p { font-weight: 700 !important; color: inherit !important; font-size: .92rem !important; }
button[data-variant="segmented_control"]:hover:not([aria-checked="true"]),
[data-testid="stBaseButton-segmented_control"]:hover {
    background: var(--lbr-accent-soft) !important; color: var(--lbr-accent) !important;
}
button[data-variant="segmented_control"][aria-checked="true"],
[data-testid="stBaseButton-segmented_controlActive"] {
    background: var(--lbr-accent) !important; color: var(--lbr-on-accent) !important;
    box-shadow: var(--lbr-shadow-sm) !important;
}
button[data-variant="segmented_control"]:disabled,
[data-testid^="stBaseButton-segmented_control"]:disabled { opacity: .45 !important; }

/* ── Sub-navegação (modos dentro das abas) ─────────────── */
.st-key-lbr_subnav { margin: .2rem 0 .2rem; }
.st-key-lbr_subnav [role="radiogroup"] {
    background: transparent !important; border: none !important; padding: 0 !important; gap: 10px !important;
}
.st-key-lbr_subnav button[data-variant="segmented_control"],
.st-key-lbr_subnav [data-testid^="stBaseButton-segmented_control"] {
    background: var(--lbr-surface) !important; color: var(--lbr-text-sec) !important;
    border: 1px solid var(--lbr-border) !important;
    border-radius: 10px !important; padding: .5rem 1.1rem !important; min-height: 44px;
}
.st-key-lbr_subnav button[data-variant="segmented_control"] p,
.st-key-lbr_subnav [data-testid^="stBaseButton-segmented_control"] p { font-size: .98rem !important; }
.st-key-lbr_subnav button[data-variant="segmented_control"]:hover:not([aria-checked="true"]),
.st-key-lbr_subnav [data-testid="stBaseButton-segmented_control"]:hover {
    border-color: var(--lbr-accent-line) !important; color: var(--lbr-accent) !important; background: var(--lbr-surface) !important;
}
.st-key-lbr_subnav button[data-variant="segmented_control"][aria-checked="true"],
.st-key-lbr_subnav [data-testid="stBaseButton-segmented_controlActive"] {
    background: var(--lbr-accent-soft) !important; color: var(--lbr-accent) !important;
    border-color: var(--lbr-accent) !important; box-shadow: none !important;
}
.st-key-lbr_subnav [data-testid="stIconMaterial"] { font-size: 1.25rem !important; }

/* submodo (A→Z / Aleatório): chips pequenos */
.st-key-lbr_subnav2 [role="radiogroup"] { padding: 3px !important; border-radius: 999px !important; }
.st-key-lbr_subnav2 button[data-variant="segmented_control"],
.st-key-lbr_subnav2 [data-testid^="stBaseButton-segmented_control"] { border-radius: 999px !important; padding: .25rem .9rem !important; min-height: 32px; }
.st-key-lbr_subnav2 button[data-variant="segmented_control"] p,
.st-key-lbr_subnav2 [data-testid^="stBaseButton-segmented_control"] p { font-size: .86rem !important; }
.st-key-lbr_subnav2 button[data-variant="segmented_control"][aria-checked="true"],
.st-key-lbr_subnav2 [data-testid="stBaseButton-segmented_controlActive"] { box-shadow: none !important; }
.lbr-sublabel { font-size: .74rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; color: var(--lbr-muted); }

/* ── Botões (estilo 3D) ────────────────────────────────── */
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    border-radius: 10px !important; min-height: 46px;
    font-weight: 700 !important; letter-spacing: 0 !important;
    padding: .5rem 1.1rem !important;
    transition: transform .08s ease, filter .15s ease, background .15s ease, border-color .15s ease !important;
}
[data-testid="stBaseButton-secondary"] p,
[data-testid="stBaseButton-primary"] p { font-weight: 700 !important; font-size: .95rem !important; color: inherit !important; }

[data-testid="stBaseButton-secondary"] {
    background: var(--lbr-surface) !important; color: var(--lbr-text) !important;
    border: 1px solid var(--lbr-border) !important; box-shadow: var(--lbr-shadow-sm) !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--lbr-accent-line) !important;
    color: var(--lbr-accent) !important; background: var(--lbr-accent-soft) !important;
}
[data-testid="stBaseButton-primary"] {
    background: var(--lbr-accent) !important; color: var(--lbr-on-accent) !important;
    border: 1px solid var(--lbr-accent) !important;
    
}
[data-testid="stBaseButton-primary"] { box-shadow: 0 2px 8px rgba(239,102,3,.25) !important; }
[data-testid="stBaseButton-primary"]:disabled { box-shadow: none !important; }
[data-testid="stBaseButton-primary"]:hover { filter: brightness(1.07); color: var(--lbr-on-accent) !important; }
[data-testid="stBaseButton-secondary"]:active:not(:disabled),
[data-testid="stBaseButton-primary"]:active:not(:disabled) {
    transform: translateY(1px);
}
[data-testid="stBaseButton-secondary"]:disabled,
[data-testid="stBaseButton-primary"]:disabled {
    opacity: .45 !important; cursor: not-allowed !important; transform: none !important;
    background: var(--lbr-surface-2) !important; color: var(--lbr-muted) !important;
    border-color: var(--lbr-border) !important;
}
[data-testid="stBaseButton-secondary"]:focus:not(:active),
[data-testid="stBaseButton-primary"]:focus:not(:active) { box-shadow: none !important; }
[data-testid="stBaseButton-secondary"]:focus-visible,
[data-testid="stBaseButton-primary"]:focus-visible { outline: 3px solid var(--lbr-accent-line) !important; outline-offset: 2px; }

/* Botão do tema (ícone redondo) */
.st-key-btn_theme button, [class*="st-key-btn_arduino"] button {
    min-height: 44px !important; height: 44px; width: 44px !important; min-width: 44px !important;
    padding: 0 !important; border-radius: 50% !important;
}
.st-key-btn_theme [data-testid="stIconMaterial"],
[class*="st-key-btn_arduino"] [data-testid="stIconMaterial"] { font-size: 1.35rem !important; margin: 0 !important; }
/* Arduino ligado = verde, desligado = cinza */
.st-key-btn_arduino_on button {
    background: var(--lbr-green-soft) !important; color: var(--lbr-green) !important;
    border-color: var(--lbr-green) !important;
}
.st-key-btn_arduino_off button { color: var(--lbr-muted) !important; }
.st-key-btn_arduino_off button:hover { color: var(--lbr-accent) !important; }

.st-key-btn_theme button p { font-size: 1.15rem !important; }

/* Botão verde (sucesso) — envolva num st.container(key="lbr_go_...") */
[class*="st-key-lbr_go"] [data-testid="stBaseButton-primary"] {
    background: var(--lbr-green-btn) !important; border-color: var(--lbr-green-btn) !important;
}

/* ── Inputs ────────────────────────────────────────────── */
[data-testid="stTextInputRootElement"],
[data-testid="stTextInput"] div[data-baseweb="input"] {
    background: var(--lbr-surface) !important; border: 1px solid var(--lbr-border) !important;
    border-radius: 10px !important; transition: border-color .15s ease, box-shadow .15s ease;
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: var(--lbr-accent) !important; box-shadow: 0 0 0 4px var(--lbr-accent-soft) !important;
}
[data-testid="stTextInput"] div[data-baseweb="base-input"] { background: transparent !important; border: none !important; }
[data-testid="stTextInput"] input {
    background: transparent !important; color: var(--lbr-text) !important; border: none !important;
    font-size: 1.02rem !important; font-weight: 700 !important; padding: .6rem .85rem !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--lbr-muted) !important; font-weight: 600; }

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: var(--lbr-surface) !important; border: 1px solid var(--lbr-border) !important;
    color: var(--lbr-text) !important; border-radius: 10px !important; font-weight: 700;
}
[data-baseweb="popover"] ul, [data-baseweb="popover"] li { background: var(--lbr-surface) !important; color: var(--lbr-text) !important; }
[data-baseweb="popover"] li:hover { background: var(--lbr-accent-soft) !important; }

[data-testid="stSlider"] label p { color: var(--lbr-text-sec) !important; }
[data-testid="stSlider"] [role="slider"] { background: var(--lbr-accent) !important; box-shadow: 0 0 0 4px var(--lbr-accent-soft) !important; }
[data-testid="stSliderThumbValue"] { color: var(--lbr-accent) !important; font-weight: 800; }
[data-testid="stCheckbox"] label > span:first-child { border-color: var(--lbr-border-strong) !important; }
[data-testid="stCheckbox"] label p { font-size: .95rem !important; color: var(--lbr-text-sec) !important; font-weight: 700 !important; }

/* ── Balões de ajuda (tooltip), spinner, slider ───────── */
[data-baseweb="tooltip"] > div,
[data-testid="stTooltipContent"] {
    background: var(--lbr-surface) !important; color: var(--lbr-text) !important;
    border-radius: 10px !important;
}
[data-baseweb="tooltip"] > div, [role="tooltip"] > [data-testid="stTooltipContent"] {
    border: 1px solid var(--lbr-border) !important; box-shadow: var(--lbr-shadow) !important;
}
[data-baseweb="tooltip"] p, [data-testid="stTooltipContent"] p { color: var(--lbr-text) !important; font-weight: 600; }
[data-baseweb="tooltip"] [data-baseweb="tooltip-arrow"], [data-baseweb="tooltip"] > div > div:empty { background: var(--lbr-surface) !important; }
[data-testid="stSpinner"], [data-testid="stSpinner"] p { color: var(--lbr-text-sec) !important; }
[data-testid="stSliderTickBar"], [data-testid="stSliderTickBar"] span,
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"] { color: var(--lbr-muted) !important; }
[data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p, [data-testid="stCheckbox"] p { color: var(--lbr-text-sec) !important; }

/* ── Expander ──────────────────────────────────────────── */
[data-testid="stExpander"] details {
    background: var(--lbr-surface) !important; border: 1px solid var(--lbr-border) !important;
    border-radius: 12px !important; overflow: hidden;
}
[data-testid="stExpander"] summary { color: var(--lbr-text) !important; font-weight: 800 !important; }
[data-testid="stExpander"] summary p { color: var(--lbr-text) !important; font-weight: 800 !important; }
[data-testid="stExpander"] summary:hover, [data-testid="stExpander"] summary:hover p { color: var(--lbr-accent) !important; }

/* ── Alerts ────────────────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── Títulos de seção ─────────────────────────────────── */
.lbr-section {
    display: flex; align-items: center; gap: 8px;
    font-size: .8rem; font-weight: 800; color: var(--lbr-muted);
    text-transform: uppercase; letter-spacing: 1.6px;
    margin: 0 0 .7rem; padding-top: 1.3rem;
}
/* título que abre uma coluna não precisa do espaço de cima (mantém as colunas alinhadas) */
[data-testid="stColumn"] [data-testid="stVerticalBlock"] > div:first-child .lbr-section { padding-top: 0; }

/* ── Cards ─────────────────────────────────────────────── */
.lbr-card {
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 16px; padding: 18px 20px; margin: 8px 0;
    box-shadow: var(--lbr-shadow);
}
.lbr-card h4 { font-size: 1rem; font-weight: 800; color: var(--lbr-text); margin: 0 0 6px; padding: 0; }
.lbr-card p  { font-size: .92rem; color: var(--lbr-text-sec); margin: 0; line-height: 1.6; }
.lbr-card.center { text-align: center; }
.lbr-empty { text-align: center; padding: 46px 20px; border-style: dashed; box-shadow: none; }
.lbr-empty .ico {
    width: 56px; height: 56px; margin: 0 auto 12px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    background: var(--lbr-accent-soft); color: var(--lbr-accent);
}
.lbr-empty .ico svg { width: 28px; height: 28px; }
.lbr-empty .ico .spin { animation: lbr-spin 1s linear infinite; }
@keyframes lbr-spin { to { transform: rotate(360deg); } }
.lbr-empty p { font-size: .98rem; }

/* ── Barra de progresso ────────────────────────────────── */
.lbr-progress-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; }
.lbr-progress-head .t { font-size: 1rem; font-weight: 800; color: var(--lbr-text); }
.lbr-progress-head .n { font-size: .95rem; font-weight: 800; color: var(--lbr-accent); }
.lbr-bar { background: var(--lbr-surface-2); border: 1px solid var(--lbr-border); border-radius: 999px; height: 20px; overflow: hidden; }
.lbr-bar > div {
    height: 100%; border-radius: 999px;
    background: var(--lbr-accent); position: relative; transition: width .4s ease;
}
.lbr-bar.green > div { background: var(--lbr-green); }

/* ── Estatísticas (quiz) ──────────────────────────────── */
.lbr-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; }
.lbr-stat { border-radius: 12px; padding: 12px 8px; text-align: center; border: 1px solid; }
.lbr-stat .v { font-size: 1.7rem; font-weight: 800; line-height: 1.1; }
.lbr-stat .l { font-size: .74rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
.lbr-stat.green  { background: var(--lbr-green-soft);  border-color: var(--lbr-green);  color: var(--lbr-green); }
.lbr-stat.red    { background: var(--lbr-red-soft);    border-color: var(--lbr-red);    color: var(--lbr-red); }
.lbr-stat.orange { background: var(--lbr-accent-soft); border-color: var(--lbr-accent); color: var(--lbr-accent); }

/* ── Cartão do sinal (imagem + letra) ─────────────────── */
.lbr-sign {
    position: relative; background: var(--lbr-surface); border: 1px solid var(--lbr-border); border-radius: 16px; padding: 18px; text-align: center;
    box-shadow: var(--lbr-shadow);
}
.lbr-sign img { width: 100%; max-width: 250px; aspect-ratio: 1; object-fit: contain;
    border-radius: 12px; background: #FFFFFF; display: block; margin: 0 auto; }
.lbr-sign .tag {
    position: absolute; top: 14px; left: 14px;
    min-width: 62px; height: 62px; padding: 0 10px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    background: var(--lbr-accent); color: var(--lbr-on-accent);
    font-size: 2.3rem; font-weight: 800; box-shadow: var(--lbr-shadow-sm);
}
.lbr-sign .tag.q { background: var(--lbr-accent); box-shadow: var(--lbr-shadow-sm); }
.lbr-sign .link { display: inline-block; margin-top: 10px; font-size: .82rem; font-weight: 700; color: var(--lbr-muted); text-decoration: none; }
.lbr-sign .link:hover { color: var(--lbr-accent); }

.lbr-counter { text-align: center; font-size: 1.05rem; font-weight: 800; color: var(--lbr-text-sec); }
.lbr-counter span { color: var(--lbr-muted); font-weight: 700; }

/* ── Letra grande ─────────────────────────────────────── */
.lbr-char-display {
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 16px; padding: 16px; text-align: center; margin-bottom: 8px;
}
.lbr-char-big { font-size: 4rem; font-weight: 800; color: var(--lbr-accent); line-height: 1; }
.lbr-char-display.idle .lbr-char-big { color: var(--lbr-muted); }
.lbr-char-label { font-size: .78rem; font-weight: 800; color: var(--lbr-muted); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }

/* ── Dedos ────────────────────────────────────────────── */
.lbr-dedos { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 10px 0; }
.lbr-dedo {
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 12px; padding: 12px 4px 10px; text-align: center; transition: all .2s ease;
    --c: var(--lbr-muted); --s: var(--lbr-surface-2);
}
.lbr-dedo.aberto  { --c: var(--lbr-green);  --s: var(--lbr-green-soft); }
.lbr-dedo.pouco   { --c: var(--lbr-yellow); --s: var(--lbr-yellow-soft); }
.lbr-dedo.meio    { --c: var(--lbr-accent); --s: var(--lbr-accent-soft); }
.lbr-dedo.fechado { --c: var(--lbr-red);    --s: var(--lbr-red-soft); }
.lbr-dedo { border-color: var(--c); background: var(--s); }
.lbr-dedo-nome { font-size: .72rem; font-weight: 800; color: var(--lbr-text-sec); text-transform: uppercase; letter-spacing: .6px; }
.lbr-dedo-bar { display: block; margin: 8px auto 6px; width: 20px; height: 44px; border-radius: 10px;
    background: linear-gradient(to top, var(--c) var(--fill, 0%), var(--lbr-border) var(--fill, 0%)); }
.lbr-dedo.aberto  .lbr-dedo-bar { --fill: 100%; }
.lbr-dedo.pouco   .lbr-dedo-bar { --fill: 66%; }
.lbr-dedo.meio    .lbr-dedo-bar { --fill: 40%; }
.lbr-dedo.fechado .lbr-dedo-bar { --fill: 14%; }
.lbr-dedo-val { font-size: .8rem; font-weight: 800; color: var(--c); }

.lbr-legend { display: flex; gap: 8px; flex-wrap: wrap; margin: 6px 0 4px; }
.lbr-legend span { font-size: .78rem; font-weight: 800; padding: 3px 10px; border-radius: 999px; }
.lbr-legend .aberto  { color: var(--lbr-green);  background: var(--lbr-green-soft); }
.lbr-legend .pouco   { color: var(--lbr-yellow); background: var(--lbr-yellow-soft); }
.lbr-legend .meio    { color: var(--lbr-accent); background: var(--lbr-accent-soft); }
.lbr-legend .fechado { color: var(--lbr-red);    background: var(--lbr-red-soft); }

/* ── Badges da soletração ─────────────────────────────── */
.lbr-badges { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }
.lbr-badge {
    width: 40px; height: 44px; display: inline-flex; align-items: center; justify-content: center;
    border-radius: 12px; font-size: 1.15rem; font-weight: 800;
    background: var(--lbr-surface); color: var(--lbr-text-sec);
    border: 1px solid var(--lbr-border);
    transition: all .15s ease;
}
.lbr-badge.active {
    background: var(--lbr-accent); color: var(--lbr-on-accent); border-color: var(--lbr-accent-dark);
    transform: translateY(-4px) scale(1.08);
}
.lbr-badge.space { width: 14px; background: none; border: none; }
.lbr-mini-label { margin-top: 12px; font-size: .78rem; font-weight: 800; color: var(--lbr-accent); text-transform: uppercase; letter-spacing: 1.4px; }

/* ── Status (mic / câmera) ────────────────────────────── */
.lbr-mic, .lbr-cam-status {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 16px; border-radius: 10px; font-size: .95rem; font-weight: 700; margin: 8px 0;
    border: 1px solid;
}
.lbr-mic.idle, .lbr-cam-status.waiting { background: var(--lbr-surface); color: var(--lbr-text-sec); border-color: var(--lbr-border); }
.lbr-mic.on, .lbr-cam-status.detecting { background: var(--lbr-accent-soft); color: var(--lbr-accent); border-color: var(--lbr-accent-line); }
.lbr-cam-status.ok { background: var(--lbr-green-soft); color: var(--lbr-green); border-color: var(--lbr-green); }
.lbr-mic .pulse, .lbr-cam-status .cam-dot {
    width: 10px; height: 10px; border-radius: 50%; display: inline-block; animation: lbr-pulse 1.2s infinite;
    background: currentColor; flex-shrink: 0;
}
.lbr-recognized {
    background: var(--lbr-accent-soft); border: 1px solid var(--lbr-accent-line);
    border-radius: 10px; padding: 10px 14px; font-size: .95rem; font-weight: 700; color: var(--lbr-text); margin: 6px 0;
}

/* ── Passos "Como funciona" ───────────────────────────── */
.lbr-steps { display: grid; gap: 12px; margin: 2px 0 4px; }
.lbr-step { display: flex; align-items: baseline; gap: 12px; }
.lbr-step-num {
    flex-shrink: 0; min-width: 18px;
    font-size: .95rem; font-weight: 800; color: var(--lbr-accent);
    font-variant-numeric: tabular-nums;
}
.lbr-step-text { font-size: .95rem; color: var(--lbr-text-sec); line-height: 1.55; }
.lbr-step-text strong { color: var(--lbr-text); font-weight: 600; }

/* ── Grade do alfabeto (botões) ───────────────────────── */
[class*="st-key-lbr_grid"] [data-testid="stHorizontalBlock"] { gap: 8px !important; }
[class*="st-key-lbr_grid"] [data-testid="stColumn"] { min-width: 0 !important; }
[class*="st-key-lbr_grid"] [data-testid="stBaseButton-secondary"],
[class*="st-key-lbr_grid"] [data-testid="stBaseButton-primary"] {
    width: 100%; min-height: 50px; padding: 0 !important; border-radius: 10px !important;
}
[class*="st-key-lbr_grid"] button p { font-size: 1.15rem !important; font-weight: 800 !important; }
[class*="st-key-cell_done_"] [data-testid="stBaseButton-secondary"] {
    background: var(--lbr-green-soft) !important; color: var(--lbr-green) !important;
    border-color: var(--lbr-green) !important;
}

/* Grade do alfabeto (só visual) */
.lbr-grid { display: grid; grid-template-columns: repeat(9, 1fr); gap: 8px; margin: 8px 0; }
.lbr-grid-cell {
    aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
    border-radius: 12px; font-size: 1.05rem; font-weight: 800;
    background: var(--lbr-surface); color: var(--lbr-text-sec);
    border: 1px solid var(--lbr-border);
}
.lbr-grid-cell.active { background: var(--lbr-accent); color: var(--lbr-on-accent); border-color: var(--lbr-accent-dark); }
.lbr-grid-cell.lbr-grid-done { background: var(--lbr-green-soft); color: var(--lbr-green); border-color: var(--lbr-green); }
.lbr-grid-cell.off { opacity: .35; border-style: dashed; }

/* ── Quiz ─────────────────────────────────────────────── */
.lbr-question { font-size: 1.5rem; font-weight: 800; color: var(--lbr-text); margin: .4rem 0 .9rem; }
.lbr-question span { color: var(--lbr-accent); }
[class*="st-key-lbr_quiz_opts"] [data-testid="stBaseButton-secondary"] { min-height: 56px !important; border-radius: 12px !important; }
[class*="st-key-lbr_quiz_opts"] [data-testid="stBaseButton-secondary"] p { font-size: 1.5rem !important; font-weight: 800 !important; }
[class*="st-key-lbr_quiz_opts"] [data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--lbr-accent) !important; color: var(--lbr-accent) !important; background: var(--lbr-accent-soft) !important;
}
.lbr-opts { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.lbr-opt {
    min-height: 92px; border-radius: 16px; display: flex; align-items: center; justify-content: center; gap: 10px;
    font-size: 2.2rem; font-weight: 800; border: 1px solid var(--lbr-border);
    background: var(--lbr-surface); color: var(--lbr-muted); opacity: .55;
}
.lbr-opt .ic { font-size: 1.2rem; }
.lbr-opt.right { opacity: 1; background: var(--lbr-green-soft); color: var(--lbr-green); border-color: var(--lbr-green); animation: lbr-pop .35s ease; }
.lbr-opt.wrong { opacity: 1; background: var(--lbr-red-soft); color: var(--lbr-red); border-color: var(--lbr-red); animation: lbr-shake .4s ease; }

.lbr-feedback {
    display: flex; align-items: center; gap: 14px; border-radius: 16px; padding: 14px 18px; margin-bottom: 14px;
    border: 1px solid; animation: lbr-slide .3s ease;
}
.lbr-feedback .ic { width: 46px; height: 46px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 800; color: #FFF; flex-shrink: 0; }
.lbr-feedback .t { font-size: 1.2rem; font-weight: 800; }
.lbr-feedback .s { font-size: .95rem; font-weight: 700; color: var(--lbr-text-sec); }
.lbr-feedback.ok  { background: var(--lbr-green-soft); border-color: var(--lbr-green); }
.lbr-feedback.ok .ic { background: var(--lbr-green); }
.lbr-feedback.ok .t { color: var(--lbr-green); }
.lbr-feedback.bad { background: var(--lbr-red-soft); border-color: var(--lbr-red); }
.lbr-feedback.bad .ic { background: var(--lbr-red); }
.lbr-feedback.bad .t { color: var(--lbr-red); }

/* ── Siga o Sinal ─────────────────────────────────────── */
.lbr-sinal-target, .lbr-sinal-acerto {
    text-align: center; border-radius: 16px; padding: 22px; margin-bottom: 12px;
    border: 1px solid;
}
.lbr-sinal-target { background: var(--lbr-surface); border-color: var(--lbr-border); }
.lbr-sinal-acerto { background: var(--lbr-green-soft); border-color: var(--lbr-green); animation: lbr-pop .35s ease; }
.lbr-sinal-target .letra, .lbr-sinal-acerto .letra { font-size: 6rem; font-weight: 800; line-height: 1; }
.lbr-sinal-target .letra { color: var(--lbr-accent); }
.lbr-sinal-acerto .letra { color: var(--lbr-green); }
.lbr-sinal-target .instrucao, .lbr-sinal-acerto .instrucao {
    font-size: .95rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 8px;
}
.lbr-sinal-target .instrucao { color: var(--lbr-text-sec); }
.lbr-sinal-acerto .instrucao { color: var(--lbr-green); }

.lbr-streak {
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    border-radius: 16px; padding: 12px 18px; margin-bottom: 12px; border: 1px solid;
    --c: var(--lbr-text-sec);
    background: var(--lbr-surface); border-color: var(--lbr-border); transition: all .25s ease;
}
.lbr-streak.warm { --c: var(--lbr-yellow); background: var(--lbr-yellow-soft); border-color: var(--lbr-yellow); }
.lbr-streak.hot  { --c: var(--lbr-accent); background: var(--lbr-accent-soft); border-color: var(--lbr-accent); animation: lbr-glow 1.5s infinite ease-in-out; }
.lbr-streak .k { font-size: .76rem; font-weight: 800; color: var(--lbr-text-sec); text-transform: uppercase; letter-spacing: 1.4px; }
.lbr-streak .l { font-size: 1.05rem; font-weight: 800; color: var(--c); }
.lbr-streak .n { font-size: 2.6rem; font-weight: 800; color: var(--c); line-height: 1; }

.lbr-celebrate { text-align: center; padding: 34px 20px; border-color: var(--lbr-green); }
.lbr-celebrate .ico {
    width: 56px; height: 56px; margin: 0 auto; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    background: var(--lbr-green-soft); color: var(--lbr-green);
}
.lbr-celebrate .ico svg { width: 30px; height: 30px; }
.lbr-celebrate h4 { font-size: 1.4rem !important; margin-top: 10px !important; }

/* ── Imagens da câmera ────────────────────────────────── */
[data-testid="stImage"] img { border-radius: 16px; }

/* ── Início ───────────────────────────────────────────── */
.lbr-hero {
    display: flex; align-items: center; gap: 32px;
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 18px; padding: 30px 36px; margin: .4rem 0 1rem; box-shadow: var(--lbr-shadow);
}
.lbr-hero img { width: 150px; height: 150px; flex-shrink: 0; border-radius: 18px;
    background: var(--lbr-accent-soft); padding: 14px; }
.lbr-hero-eyebrow { font-size: .8rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; color: var(--lbr-accent); }
.lbr-hero-title { font-size: 2.4rem; font-weight: 800; color: var(--lbr-text); line-height: 1.1; margin: 6px 0 10px; letter-spacing: -.5px; }
.lbr-hero-title em { font-style: normal; color: var(--lbr-accent); }
.lbr-hero-sub { font-size: 1.08rem; color: var(--lbr-text-sec); line-height: 1.6; max-width: 640px; }
.lbr-hero-sub strong { color: var(--lbr-text); }
.lbr-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
.lbr-chip { font-size: .82rem; font-weight: 800; padding: 6px 12px; border-radius: 999px;
    background: var(--lbr-surface-2); color: var(--lbr-text-sec); border: 1px solid var(--lbr-border); }

.lbr-mode-head { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.lbr-mode-icon {
    width: 52px; height: 52px; border-radius: 12px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    background: var(--c-soft); color: var(--c); border: 1px solid var(--c);
}
.lbr-mode-icon svg { width: 28px; height: 28px; }
.lbr-mode-title { font-size: 1.05rem; font-weight: 800; color: var(--lbr-text); line-height: 1.15; }
.lbr-mode-where { font-size: .72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: var(--c); }
.lbr-mode-desc { font-size: .92rem; color: var(--lbr-text-sec); line-height: 1.5; margin-bottom: 10px; }
.lbr-mode-tag { display: inline-block; font-size: .74rem; font-weight: 800; padding: 3px 9px; border-radius: 999px; margin-bottom: 12px; }
.lbr-mode-tag.free { background: var(--lbr-green-soft); color: var(--lbr-green); }
.lbr-mode-tag.hw   { background: var(--lbr-surface-2); color: var(--lbr-text-sec); }

[data-testid="stColumn"]:has(> div > [class*="st-key-lbr_mode_"]) > div,
[data-testid="stColumn"]:has([class*="st-key-lbr_mode_"]) { height: 100%; }
[class*="st-key-lbr_mode_"] {
    display: flex; flex-direction: column; justify-content: space-between;
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 16px; padding: 18px 16px 16px; height: 100%;
    box-shadow: var(--lbr-shadow); transition: transform .15s ease, border-color .15s ease;
}
[class*="st-key-lbr_mode_"]:hover { transform: translateY(-3px); border-color: var(--lbr-accent-line); }
[class*="st-key-lbr_mode_"] [data-testid="stBaseButton-secondary"] { min-height: 42px; }

.lbr-path { display: flex; align-items: stretch; gap: 10px; flex-wrap: wrap; }
.lbr-path-step {
    flex: 1; min-width: 180px; display: flex; align-items: center; gap: 12px;
    background: var(--lbr-surface); border: 1px solid var(--lbr-border); border-radius: 14px; padding: 12px 14px;
}
.lbr-path-step .n { width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center;
    background: var(--lbr-accent); color: #FFF; font-weight: 800; font-size: 1.05rem; box-shadow: var(--lbr-shadow-sm); }
.lbr-path-step .t { font-weight: 800; color: var(--lbr-text); font-size: 1rem; }
.lbr-path-step .s { font-weight: 700; color: var(--lbr-text-sec); font-size: .86rem; }
.lbr-path-arrow { display: flex; align-items: center; color: var(--lbr-muted); font-weight: 800; font-size: 1.3rem; }

/* ── Início (layout original) ─────────────────────────── */
.lbr-home-hero { text-align: center; padding: 2.2rem 1rem 1.6rem; }
.lbr-home-hero img { width: 120px; height: 120px; object-fit: contain; }
.lbr-home-hero .t { font-size: 2.8rem; font-weight: 800; color: var(--lbr-text); margin: 18px 0 8px; letter-spacing: -.5px; line-height: 1; }
.lbr-home-hero .t span { color: var(--lbr-accent); }
.lbr-home-hero .s { font-size: 1.1rem; color: var(--lbr-text-sec); max-width: 580px; margin: 0 auto; line-height: 1.7; }
.lbr-home-hero .s strong { color: var(--lbr-text); }
.lbr-home-label {
    font-size: .8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.6px;
    color: var(--lbr-muted); margin-bottom: .9rem;
}
.lbr-mode-center { text-align: center; display: flex; flex-direction: column; align-items: center; }
.lbr-mode-center .lbr-mode-icon { width: 60px; height: 60px; border-radius: 14px; margin-bottom: 12px; }
.lbr-mode-center .lbr-mode-icon svg { width: 34px; height: 34px; }
.lbr-mode-center .lbr-mode-title { font-size: 1.12rem; margin-bottom: 6px; }
.lbr-mode-center .lbr-mode-where { margin-bottom: 12px; }
.lbr-start { margin-top: 1.4rem; padding: 20px 24px; border-left: 4px solid var(--lbr-accent); }
.lbr-card .hl, .lbr-text .hl { color: var(--lbr-accent); }
.lbr-card strong, .lbr-text strong { color: var(--lbr-text); }
.lbr-card .hl { color: var(--lbr-accent) !important; }
.lbr-text { font-size: .95rem; color: var(--lbr-text-sec); line-height: 1.7; margin: 0 0 10px; }

/* ── Imagem do sinal (layout original: 200px centralizada) ── */
.lbr-sign-img { text-align: center; margin-bottom: 10px; }
.lbr-sign-img img {
    width: 200px; height: 200px; object-fit: contain; background: #FFFFFF;
    border-radius: 16px; border: 1px solid var(--lbr-border); padding: 6px;
}
.lbr-sign-img a { display: block; margin-top: 6px; font-size: .8rem; font-weight: 700; color: var(--lbr-muted); text-decoration: none; }
.lbr-sign-img a:hover { color: var(--lbr-accent); }

/* ── Resultado do quiz (card da letra) ─────────────────── */
.lbr-char-display.ok  { background: var(--lbr-green-soft); border-color: var(--lbr-green); animation: lbr-pop .35s ease; }
.lbr-char-display.ok .lbr-char-big, .lbr-char-display.ok .lbr-char-label { color: var(--lbr-green); }
.lbr-char-display.bad { background: var(--lbr-red-soft); border-color: var(--lbr-red); animation: lbr-shake .4s ease; }
.lbr-char-display.bad .lbr-char-big, .lbr-char-display.bad .lbr-char-label { color: var(--lbr-red); }
.lbr-char-display.q .lbr-char-big { color: var(--lbr-accent); }
.lbr-opts.compact { gap: 12px; }
.lbr-opts.compact .lbr-opt { min-height: 56px; font-size: 1.5rem; border-radius: 12px; }

/* ── Aviso de erro (conexão Arduino) ────────────────────── */
.lbr-alert {
    display: flex; gap: 12px; align-items: center; margin: 12px 0 6px;
    background: var(--lbr-yellow-soft); border: 1px solid var(--lbr-yellow);
    border-radius: 12px; padding: 12px 16px; animation: lbr-slide .3s ease;
}
.lbr-alert .ic { font-size: 1.4rem; line-height: 1; flex-shrink: 0; }
.lbr-alert .t { font-size: 1rem; font-weight: 800; color: var(--lbr-text); }
.lbr-alert p { font-size: .9rem; color: var(--lbr-text-sec); margin: 2px 0 0; line-height: 1.5; }
.lbr-alert code { font-size: .8rem; background: var(--lbr-surface); padding: 1px 6px; border-radius: 6px; color: var(--lbr-text); }

/* ── Botão de dica (Siga o Sinal) ──────────────────────── */
.st-key-sinal_dica_btn [data-testid="stBaseButton-secondary"] {
    background: var(--lbr-yellow-soft) !important; color: var(--lbr-text) !important;
    border-color: var(--lbr-yellow) !important;
}
.st-key-sinal_dica_btn [data-testid="stBaseButton-secondary"]:hover { filter: brightness(1.05); color: var(--lbr-text) !important; }
.st-key-sinal_dica_btn [data-testid="stIconMaterial"] { color: var(--lbr-yellow); }
.lbr-dica {
    display: flex; align-items: center; gap: 16px; margin: 4px 0 10px;
    background: var(--lbr-surface); border: 1px solid var(--lbr-yellow); border-radius: 14px;
    padding: 12px; animation: lbr-pop .3s ease;
}
.lbr-dica img { width: 120px; height: 120px; object-fit: contain; background: #FFFFFF; border-radius: 12px; flex-shrink: 0; }
.lbr-dica .t { font-size: .74rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; color: var(--lbr-yellow); }
.lbr-dica .l { font-size: 2.4rem; font-weight: 800; color: var(--lbr-text); line-height: 1.1; }
.lbr-dica p { font-size: .9rem; color: var(--lbr-text-sec); margin: 2px 0 0; }

/* ── Dicas (lista com ícones) ─────────────────────────── */
.lbr-tips { display: grid; gap: 14px; margin: 2px 0 4px; }
.lbr-tip { display: flex; gap: 12px; align-items: flex-start; }
.lbr-tip .ic { flex-shrink: 0; color: var(--lbr-accent); padding-top: 1px; }
.lbr-tip .ic svg { width: 20px; height: 20px; display: block; }
.lbr-tip .t { font-size: .95rem; font-weight: 700; color: var(--lbr-text); }
.lbr-tip .d { font-size: .9rem; color: var(--lbr-text-sec); line-height: 1.5; }

/* ── Aviso discreto (ex.: Arduino desconectado) ───────── */
.lbr-notice {
    display: flex; align-items: center; gap: 10px; font-size: .92rem; color: var(--lbr-text-sec);
    background: var(--lbr-accent-soft); border: 1px solid var(--lbr-accent-line);
    border-radius: 12px; padding: 12px 16px; margin: 4px 0 14px;
}
.lbr-notice svg { width: 20px; height: 20px; color: var(--lbr-accent); flex-shrink: 0; }
.lbr-notice strong { color: var(--lbr-text); font-weight: 700; }
.lbr-recognized-line { margin-top: 6px !important; font-weight: 600; color: var(--lbr-text) !important; }

/* ── Sobre ────────────────────────────────────────────── */
.about-hero {
    display: flex; align-items: center; gap: 28px;
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 18px; padding: 28px 32px; margin: .4rem 0 18px; color: var(--lbr-text); box-shadow: var(--lbr-shadow);
}
.about-hero h1 { font-size: 2rem !important; font-weight: 800 !important; margin: 0 0 4px !important; padding: 0 !important; color: var(--lbr-text) !important; }
.about-hero .tagline { font-size: 1.1rem; font-weight: 800; color: var(--lbr-accent); margin: 0 0 12px; }
.about-hero .abstract { font-size: .98rem; color: var(--lbr-text-sec); line-height: 1.7; max-width: 820px; }
.about-hero .abstract strong { color: var(--lbr-text); }
.about-hero .img { flex: 0 0 240px; }
.about-hero .img img { width: 100%; border-radius: 16px; object-fit: cover; }
.about-section-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.25rem; font-weight: 800; color: var(--lbr-text); margin: 28px 0 12px;
}
.about-section-title::before { content: ""; width: 8px; height: 26px; border-radius: 4px; background: var(--lbr-accent); }
.about-card {
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
    border-radius: 16px; padding: 20px 24px; height: 100%; box-shadow: var(--lbr-shadow);
}
.about-card p, .about-card li { font-size: .98rem; color: var(--lbr-text-sec); line-height: 1.75; margin: 0 0 12px; }
.about-card p:last-child { margin-bottom: 0; }
.about-card strong { color: var(--lbr-text); }
.about-card .hl { color: var(--lbr-accent); }
.about-quote { border-left: 4px solid var(--lbr-accent); padding-left: 16px; }
.about-quote p { color: var(--lbr-text) !important; font-weight: 700; }
.about-metric {
    text-align: center; padding: 20px 10px; border-radius: 16px;
    background: var(--lbr-surface); border: 1px solid var(--lbr-border);
}
.about-metric .val { font-size: 2.3rem; font-weight: 800; color: var(--lbr-accent); line-height: 1; }
.about-metric .lbl { font-size: .8rem; font-weight: 800; color: var(--lbr-text-sec); margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; }
.about-use {
    background: var(--lbr-surface); border: 1px solid var(--lbr-border); border-top: 3px solid var(--c);
    border-radius: 16px; padding: 18px 20px; height: 100%;
}
.about-use .k { font-size: .8rem; font-weight: 800; color: var(--c); letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 8px; }
.about-use p { font-size: .95rem; color: var(--lbr-text-sec); line-height: 1.65; margin: 0; }
.about-use strong { color: var(--lbr-text); }
.lbr-footer { text-align: center; font-size: .85rem; font-weight: 700; color: var(--lbr-muted); margin-top: 28px; }

/* ── Animações ────────────────────────────────────────── */
@keyframes lbr-pulse { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: .4; transform: scale(1.5); } }
@keyframes lbr-pop   { 0% { transform: scale(.85); } 60% { transform: scale(1.05); } 100% { transform: scale(1); } }
@keyframes lbr-shake { 0%,100% { transform: translateX(0); } 25% { transform: translateX(-6px); } 75% { transform: translateX(6px); } }
@keyframes lbr-slide { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes lbr-glow  { 0%,100% { box-shadow: 0 0 0 0 var(--lbr-accent-soft); } 50% { box-shadow: 0 0 0 8px var(--lbr-accent-soft); } }
.lbr-flash { animation: lbr-pop .35s ease; }

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}

/* ── Telas menores ────────────────────────────────────── */
@media (max-width: 1200px) {
    .lbr-brand-sub { display: none; }
    .lbr-hdr-badge .txt { display: none; }
    .lbr-hdr-badge { padding: 10px; }
    .st-key-nav button[data-variant="segmented_control"],
    .st-key-nav [data-testid^="stBaseButton-segmented_control"] { padding: .5rem .75rem !important; }
    .st-key-nav button[data-variant="segmented_control"] p,
    .st-key-nav [data-testid^="stBaseButton-segmented_control"] p { font-size: .92rem !important; }
    .lbr-mode-head { flex-direction: column; align-items: flex-start; gap: 8px; }
    .lbr-mode-title { font-size: .98rem; overflow-wrap: anywhere; }
    [class*="st-key-lbr_mode_"] { padding: 14px 12px 12px; }
    .lbr-mode-desc { font-size: .86rem; }
}
@media (max-width: 900px) {
    .lbr-hero, .about-hero { flex-direction: column; text-align: center; padding: 24px 20px; }
    .lbr-hero-title { font-size: 1.8rem; }
    .lbr-chips { justify-content: center; }
    .about-hero .img { flex-basis: auto; max-width: 220px; }
    .lbr-grid { grid-template-columns: repeat(7, 1fr); }
}
"""


def inject() -> None:
    theme = st.session_state.get("theme", "dark")
    pal = _DARK if theme == "dark" else _LIGHT
    st.markdown(
        f"<style>\n{_FONT}\n:root {{\n{_vars(pal)}\n}}\n{_CSS}\n</style>",
        unsafe_allow_html=True,
    )


def toggle() -> None:
    """Alterna entre claro e escuro."""
    st.session_state.theme = "light" if st.session_state.get("theme", "dark") == "dark" else "dark"


def palette() -> dict:
    """Retorna a paleta ativa (para casos raros em que precisa do valor e não da var CSS)."""
    return _DARK if st.session_state.get("theme", "dark") == "dark" else _LIGHT