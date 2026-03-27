import base64
import streamlit as st

def render(tab) -> None:
    with tab:
        _render_hero()
        _render_metrics()
        _render_motivation()
        _render_technology()
        _render_how_to_use()
        _render_footer()

def _render_hero() -> None:
    img_path = "docs/mao-robotica.png"
    try:
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:100%;border-radius:8px;object-fit:cover;">'
    except FileNotFoundError:
        img_tag = ""

    st.markdown(f"""
    <div class="about-hero" style="display:flex;align-items:center;gap:24px;">
        <div style="flex:3">
            <h1>O que é este projeto?</h1>
            <div class="tagline">Tecnologia assistiva de baixo custo para inclusão de pessoas surdas.</div>
            <div class="abstract">
                <strong style="color:#E8E9F0">RoboLibras</strong> é uma iniciativa de pesquisa aplicada
                dedicada à concepção de tecnologias assistivas de baixo custo com impacto social mensurável —
                uma mão robótica impressa em 3D que recebe comandos por <strong>texto digitado</strong>,
                <strong>voz</strong> ou <strong>espelhamento em tempo real pela câmera</strong> e reproduz
                fisicamente cada letra do alfabeto manual da LIBRAS por meio de 5 servomotores controlados
                via Arduino. O projeto situa-se na interseção entre <em>robótica educacional</em>,
                <em>visão computacional</em> e <em>acessibilidade linguística</em>, com foco em soluções
                reproduzíveis usando hardware acessível (Arduino + impressão 3D) e software 100% open-source.
            </div>
        </div>
        <div style="flex:1;min-width:160px">{img_tag}</div>
    </div>
    """, unsafe_allow_html=True)

def _render_metrics() -> None:
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, val, lbl in [
        (m1, "5",  "Servomotores"),
        (m2, "4",  "Níveis de Flexão"),
        (m3, "32", "Sinais Mapeados"),
        (m4, "21", "Landmarks"),
        (m5, "3",  "Modos de Entrada"),
    ]:
        with col:
            st.markdown(f"""
            <div class="about-metric">
                <div class="val">{val}</div>
                <div class="lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

def _render_motivation() -> None:
    st.markdown('<div class="about-section-title">Motivação &amp; Problema que Resolve</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-card">
        <p style="color:#9A9CB8;font-size:0.83rem;line-height:1.8;margin-bottom:16px">
            A <strong style="color:#E8E9F0">LIBRAS</strong> é reconhecida como meio legal de comunicação no Brasil 
            (Lei nº 10.436/2002 e Decreto nº 5.626/2005) e representa o principal meio de comunicação para uma parcela significativa da população surda. 
            Dados recentes indicam que cerca de <strong style="color:#EF6603">2,3 milhões de brasileiros possuem deficiência auditiva</strong>, 
            podendo ultrapassar 10 milhões quando considerados todos os graus de perda auditiva. Ainda assim, a LIBRAS permanece pouco difundida entre a população ouvinte, 
            gerando barreiras de comunicação em contextos como educação, serviços públicos e interações cotidianas.
        </p>
        <p style="color:#9A9CB8;font-size:0.83rem;line-height:1.8;margin-bottom:16px">
            Embora existam soluções tecnológicas voltadas à tradução e mediação da língua de sinais, muitas apresentam 
            <strong style="color:#EF6603">alto custo</strong>, dependência de infraestrutura complexa ou baixa acessibilidade. 
            Esse cenário limita sua adoção em larga escala, especialmente em ambientes educacionais e regiões com menos recursos, 
            reforçando a necessidade de alternativas mais acessíveis e eficientes.
        </p>
        <div style="border-left:3px solid #EF6603;padding-left:16px">
            <p style="color:#C8CAE0;font-size:0.83rem;line-height:1.8;margin:0">
                Este projeto é uma alternativa acessível: uma mão robótica que reproduz fisicamente
                o alfabeto manual da LIBRAS a partir de texto, voz ou gestos — pensada para facilitar
                o aprendizado e aproximar pessoas.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def _render_technology() -> None:
    st.markdown('<div class="about-section-title">Tecnologia</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-card">
        <p style="color:#9A9CB8;font-size:0.83rem;line-height:1.8">
            O sistema usa um <strong style="color:#E8E9F0">Arduino Uno</strong> para controlar 5 servomotores
            que movem cada dedo da mão robótica. A detecção de gestos pela câmera é feita com
            <strong style="color:#E8E9F0">MediaPipe</strong>, tecnologia do Google capaz de identificar
            a posição da mão em tempo real. O reconhecimento de voz usa o
            <strong style="color:#E8E9F0">Google Speech</strong> em português.
            Tudo é executado localmente no computador — sem servidores externos, sem custos de nuvem.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def _render_how_to_use() -> None:
    st.markdown('<div class="about-section-title">Como Usar o Sistema</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-card">
        <p><strong style="color:#E8E9F0">Pré-requisitos:</strong>
        Arduino Uno com firmware StandardFirmata, Python 3.10, dependências do <code style="color:#EF6603;background:rgba(239,102,3,0.1);padding:1px 6px;border-radius:4px">requirements.txt</code>
        e microfone (opcional para modo de voz).</p>
    </div>
    """, unsafe_allow_html=True)

    cu1, cu2, cu3 = st.columns(3, gap="small")
    with cu1:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #EF6603;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#EF6603;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">① Modo Texto</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Conecte o Arduino na aba lateral, digite a palavra desejada no campo de texto e clique em <strong>Soletrar</strong>. A mão reproduzirá cada letra sequencialmente.</p>
        </div>
        """, unsafe_allow_html=True)
    with cu2:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #EF6603;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#EF6603;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">② Modo Voz</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Clique em <strong>Ativar microfone</strong>. Fale a palavra em português e o sistema reconhecerá automaticamente e acionará os servos. Ajuste o atraso entre letras pelo slider.</p>
        </div>
        """, unsafe_allow_html=True)
    with cu3:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #EF6603;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#EF6603;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">③ Modo Câmera</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Acesse a aba <strong>Câmera</strong>, clique em <strong>Iniciar câmera</strong> e posicione a mão frente à webcam. A mão robótica espelha seus gestos em tempo real.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

def _render_footer() -> None:
    st.markdown(
        '<p style="text-align:center;font-size:0.75rem;color:#6B6D88">'
        '© 2026, Iandê de Freitas Richalski · Projeto InteliGente - UTFPR</p>',
        unsafe_allow_html=True,
    )