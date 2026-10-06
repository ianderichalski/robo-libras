import streamlit as st
from ui.components import img_b64, html

def render(tab) -> None:
    with tab:
        _render_hero()
        _render_metrics()
        _render_motivation()
        _render_technology()
        _render_professor()
        _render_footer()

def _render_hero() -> None:
    src = img_b64("docs/mao-robotica.png")
    img_html = f'<div class="img"><img src="{src}" alt="Mão robótica"></div>' if src else ""
    html(f"""
    <div class="about-hero">
        <div style="flex:1">
            <h1>O que é o RoboLibras?</h1>
            <div class="tagline">Aprender LIBRAS de forma concreta, interativa e inclusiva.</div>
            <div class="abstract">
                O <strong>RoboLibras</strong> é um objeto de aprendizagem para o ensino do alfabeto
                manual da LIBRAS que integra três modalidades de interação (<strong>texto digitado</strong>,
                <strong>voz</strong> e <strong>gestos via câmera</strong>) com a reprodução física
                dos sinais por uma mão robótica. O estudante visualiza cada sinal em tempo real e entende
                a posição exata dos dedos de forma concreta. Desenvolvido com hardware acessível e
                software de código aberto, o sistema pode ser usado por professores e estudantes
                diretamente em sala de aula, promovendo <em>aprendizagem ativa</em> e
                <em>educação inclusiva</em>.
            </div>
        </div>
        {img_html}
    </div>
    """)

def _render_metrics() -> None:
    cols = st.columns(4)
    for col, val, lbl in [
        (cols[0], "26",  "Sinais ensináveis"),
        (cols[1], "5",   "Modos de aprendizagem"),
        (cols[2], "3",   "Modalidades de entrada"),
        (cols[3], "A–Z", "Alfabeto manual completo"),
    ]:
        with col:
            html(f'<div class="about-metric"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>')

def _render_motivation() -> None:
    html('<div class="about-section-title">Motivação &amp; Problema que Resolve</div>')
    html("""
    <div class="about-card">
        <p>
            A <strong>LIBRAS</strong> é reconhecida como meio legal de comunicação no Brasil
            (Lei nº 10.436/2002), e sua presença nas escolas é obrigatória desde o Decreto nº 5.626/2005.
            No entanto, o ensino do alfabeto manual ainda enfrenta um desafio concreto: a
            <strong class="hl">escassez de recursos didáticos interativos</strong> que permitam ao estudante
            visualizar, explorar e praticar os sinais de forma dinâmica em sala de aula. Materiais impressos
            e vídeos estáticos limitam o engajamento e dificultam a compreensão da posição exata dos dedos
            em cada sinal.
        </p>
        <p>
            Esse cenário é ainda mais relevante considerando que cerca de
            <strong class="hl">10,3 milhões de brasileiros possuem algum grau de deficiência auditiva</strong>
            (IBGE, 2022), o que reforça a necessidade de práticas pedagógicas inclusivas que aproximem
            estudantes ouvintes e surdos. A formação de professores e o acesso a ferramentas acessíveis
            são pilares para que a inclusão aconteça de fato nas escolas.
        </p>
        <div class="about-quote">
            <p>
                O RoboLibras nasce como resposta pedagógica a esse desafio: um objeto de aprendizagem
                que combina texto, voz e visão computacional para tornar o ensino do alfabeto manual
                da LIBRAS concreto, interativo e acessível em qualquer sala de aula.
            </p>
        </div>
    </div>
    """)

def _render_technology() -> None:
    html('<div class="about-section-title">Tecnologia</div>')
    html("""
    <div class="about-card">
        <p>
            O sistema usa um <strong>Arduino Uno</strong> para controlar 5 servomotores que movem cada
            dedo da mão robótica. A detecção de gestos pela câmera é feita com o <strong>MediaPipe</strong>,
            tecnologia do Google capaz de identificar a posição da mão em tempo real. O reconhecimento de
            voz usa o <strong>Google Speech</strong> em português. Tudo pode ser executado localmente no
            computador ou acessado pelo navegador via servidor web.
        </p>
    </div>
    """)

def _render_professor() -> None:
    html('<div class="about-section-title">Para o Professor</div>')
    html("""
    <div class="about-card" style="margin-bottom:14px">
        <p>O RoboLibras foi pensado para ser usado em sala de aula como recurso pedagógico de apoio
        ao ensino de LIBRAS. Algumas sugestões de uso:</p>
    </div>
    """)

    usos = [
        ("var(--lbr-accent)", "Introdução ao alfabeto",
         "Use o <strong>Modo Aula</strong> para apresentar cada letra do alfabeto manual à turma. "
         "A mão robótica executa o sinal enquanto os alunos observam a posição dos dedos."),
        ("var(--lbr-accent)", "Avaliação formativa",
         "Use o <strong>Quiz</strong> ao final da aula para verificar o aprendizado. Os alunos "
         "identificam a letra correspondente ao sinal exibido, sem precisar do Arduino."),
        ("var(--lbr-accent)", "Prática individual",
         "Oriente os alunos a usarem o <strong>Siga o Sinal</strong> com a webcam para praticar. "
         "O modo A→Z garante progressão e o Aleatório desafia os mais avançados."),
    ]
    cols = st.columns(3, gap="small")
    for col, (cor, titulo, texto) in zip(cols, usos):
        with col:
            html(f'<div class="about-use" style="--c:{cor}"><div class="k">{titulo}</div><p>{texto}</p></div>')

def _render_footer() -> None:
    html('<div class="lbr-footer">© 2026, InteliGente</div>')