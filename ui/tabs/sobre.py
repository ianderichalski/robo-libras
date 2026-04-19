import base64
import streamlit as st

def render(tab) -> None:
    with tab:
        _render_hero()
        _render_metrics()
        _render_motivation()
        _render_technology()
        _render_how_to_use()
        _render_professor()
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
            <h1>O que é o RoboLibras?</h1>
            <div class="tagline">Aprender LIBRAS de forma concreta, interativa e inclusiva.</div>
            <div class="abstract">
                O <strong style="color:#E8E9F0">RoboLibras</strong> é um objeto de aprendizagem 
                para o ensino do alfabeto manual da LIBRAS que integra três modalidades de interação — 
                <strong>texto digitado</strong>, <strong>voz</strong> e 
                <strong>gestos via câmera</strong> — com a reprodução física dos sinais por uma 
                mão robótica. O estudante visualiza cada sinal em tempo real, compreendendo 
                a posição exata dos dedos de forma concreta e dinâmica. Desenvolvido com 
                hardware acessível e software de código aberto, o sistema pode ser utilizado 
                por professores e estudantes diretamente em sala de aula, promovendo 
                <em>aprendizagem ativa</em> e <em>educação inclusiva</em>.
            </div>
        </div>
        <div style="flex:1;min-width:160px">{img_tag}</div>
    </div>
    """, unsafe_allow_html=True)

def _render_metrics() -> None:
    m1, m2, m3, m4 = st.columns(4)
    for col, val, lbl in [
        (m1, "32", "Sinais ensináveis"),
        (m2, "3",  "Modos de aprendizagem"),
        (m3, "3",  "Modalidades de entrada"),
        (m4, "A–Z", "Alfabeto manual completo"),
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
            A <strong style="color:#E8E9F0">LIBRAS</strong> é reconhecida como meio legal de comunicação 
            no Brasil (Lei nº 10.436/2002) e sua presença nas escolas é obrigatória desde o 
            Decreto nº 5.626/2005. No entanto, o ensino do alfabeto manual ainda enfrenta um 
            desafio concreto: a <strong style="color:#EF6603">escassez de recursos didáticos interativos</strong> 
            que permitam ao estudante visualizar, explorar e praticar os sinais de forma dinâmica 
            em sala de aula. Materiais impressos e vídeos estáticos limitam o engajamento e 
            dificultam a compreensão da posição exata dos dedos em cada sinal.
        </p>
        <p style="color:#9A9CB8;font-size:0.83rem;line-height:1.8;margin-bottom:16px">
            Esse cenário é ainda mais relevante considerando que cerca de 
            <strong style="color:#EF6603">2,3 milhões de brasileiros possuem deficiência auditiva severa</strong> 
            (IBGE, 2022), reforçando a necessidade de práticas pedagógicas inclusivas que aproximem 
            estudantes ouvintes e surdos. A formação de professores e o acesso a ferramentas 
            acessíveis são pilares fundamentais para que a inclusão aconteça de fato nas escolas.
        </p>
        <div style="border-left:3px solid #EF6603;padding-left:16px">
            <p style="color:#C8CAE0;font-size:0.83rem;line-height:1.8;margin:0">
                O RoboLibras nasce como resposta pedagógica a esse desafio — um objeto de 
                aprendizagem que combina texto, voz e visão computacional para tornar o ensino 
                do alfabeto manual da LIBRAS concreto, interativo e acessível em qualquer sala de aula.
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
            <div style="font-size:0.7rem;font-weight:700;color:#EF6603;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">① Soletração Livre</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Conecte o Arduino, digite a palavra desejada e clique em <strong>Soletrear</strong>. A mão reproduzirá cada letra sequencialmente. Também é possível ativar o microfone e falar a palavra.</p>
        </div>
        """, unsafe_allow_html=True)
    with cu2:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #EF6603;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#EF6603;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">② Modo Aula e Quiz</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Na aba <strong>Texto / Voz</strong>, explore o alfabeto letra por letra no <strong>Modo Aula</strong> ou teste seus conhecimentos no <strong>Quiz</strong>. Funcionam sem Arduino conectado.</p>
        </div>
        """, unsafe_allow_html=True)
    with cu3:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #EF6603;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#EF6603;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">③ Siga o Sinal</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Na aba <strong>Câmera</strong>, pratique os sinais em sequência <strong>A→Z</strong> ou em modo <strong>Aleatório</strong>. A câmera detecta seu sinal e confirma quando correto. Funciona sem Arduino conectado.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def _render_professor() -> None:
    st.markdown('<div class="about-section-title">Para o Professor</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-card">
        <p style="color:#9A9CB8;font-size:0.83rem;line-height:1.8;margin-bottom:16px">
            O RoboLibras foi pensado para ser utilizado em sala de aula como recurso pedagógico
            de apoio ao ensino de LIBRAS. Abaixo estão algumas sugestões de uso:
        </p>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3, gap="small")
    with p1:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #3B8BD4;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#3B8BD4;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">Introdução ao Alfabeto</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Use o <strong>Modo Aula</strong> para apresentar cada letra do alfabeto manual à turma. A mão robótica executa o sinal enquanto os alunos observam a posição dos dedos no painel.</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #3B8BD4;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#3B8BD4;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">Avaliação Formativa</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Utilize o <strong>Quiz</strong> ao final da aula para verificar o aprendizado. Os alunos identificam a letra correspondente ao sinal exibido — sem precisar de Arduino conectado.</p>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div style="background:#2F324D;border:1px solid #525680;border-top:2px solid #3B8BD4;border-radius:8px;padding:14px;height:100%">
            <div style="font-size:0.7rem;font-weight:700;color:#3B8BD4;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px">Prática Individualizada</div>
            <p style="font-size:0.76rem;color:#9A9CB8;line-height:1.65;margin:0">Oriente os alunos a utilizarem o <strong>Siga o Sinal</strong> com a webcam para praticar individualmente. O modo A→Z garante progressão e o Aleatório desafia os mais avançados.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def _render_footer() -> None:
    st.markdown(
        '<p style="text-align:center;font-size:0.75rem;color:#6B6D88">'
        '© 2026, Iandê de Freitas Richalski · Projeto InteliGente - UTFPR</p>',
        unsafe_allow_html=True,
    )