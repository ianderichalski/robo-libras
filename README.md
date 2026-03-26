<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-Firmata-00979D?style=flat-square&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-FF6F00?style=flat-square)](https://mediapipe.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)

<img src="docs/demo.gif" alt="Demonstração  mão robótica" width="600">

---

<h4>RoboLibras: Um Sistema Robótico Assistivo Multimodal de Baixo Custo para Reconhecimento e Reprodução Acessível do Alfabeto Manual da LIBRAS</h4>

  <a href="#arquitetura-do-sistema">Arquitetura do Sistema</a> •
  <a href="#hardware">Hardware</a> •
  <a href="#instalação-e-configuração">Instalação e Configuração</a> •
  <a href="#uso">Uso</a> •
  <a href="#calibração-dos-servos">Calibração dos Servos</a> •
  <a href="#estrutura-do-repositório">Estrutura do Repositório</a> •
  <a href="#dependências">Dependências</a> •
  <a href="#limitações-conhecidas">Limitações Conhecidas</a> •
  <a href="#trabalhos-futuros">Trabalhos Futuros</a> •
  <a href="#referências">Referências</a> 

</div>

--- 

## Resumo

Um dos principais desafios em tecnologia assistiva para a Língua Brasileira de Sinais (LIBRAS) é prover representação física acessível e em tempo real dos sinais manuais, considerando que soluções existentes são frequentemente proprietárias ou dependem de infraestrutura computacional robusta. Este trabalho apresenta o RoboLibras, um sistema de baixo custo e reproduzível que integra hardware acessível e software de código aberto para a reprodução do alfabeto manual da LIBRAS. O sistema combina três modalidades de entrada — texto, voz e gestos via câmera — com cinco servomotores controlados por Arduino. A detecção de pose da mão em tempo real e um classificador baseado em aprendizado de máquina permitem o reconhecimento automático de 32 sinais (26 letras e 6 dígitos). Uma interface web interativa permite operação e visualização do sistema. Considerando que cerca de 2,3 milhões de brasileiros possuem deficiência auditiva severa (IBGE, 2019), o RoboLibras contribui para facilitar aprendizado e comunicação inclusiva. Resultados experimentais demonstram a viabilidade de sistemas robóticos assistivos multimodais utilizando hardware acessível, evidenciando aplicações potenciais em contextos educacionais e de inclusão social.

## Arquitetura do Sistema

### Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE ENTRADA                       │
│                                                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│   │  Texto (UI)  │  │  Voz (mic)   │  │  Câmera (webcam) │  │
│   └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│          │                 │                   │            │
│          │         Google Speech API     MediaPipe          │
│          │         SpeechRecognition     Hand Landmarker    │
└──────────┼─────────────────┼───────────────────┼────────────┘
           │                 │                   │
           └─────────────────┴───────────────────┘
                             │
                    pose: dict[str, float]
                    (5 dedos × 4 níveis)
                             │
┌────────────────────────────┼────────────────────────────────┐
│                   CAMADA DE CONTROLE                        │
│                            │                                │
│            src/servo.py · src/speller.py                    │
│            Mapeamento pose → ângulos (SERVO_ANGLES)         │
└────────────────────────────┼────────────────────────────────┘
                             │
                    pyFirmata · USB Serial
                    57600 baud · StandardFirmata
                             │
┌────────────────────────────┼────────────────────────────────┐
│                  CAMADA DE HARDWARE                         │
│                            │                                │
│              Arduino Uno · 5× Servo SG90                    │
│              Mão robótica impressa em 3D                    │
│              Acionamento por tendões                        │
└─────────────────────────────────────────────────────────────┘
```

### Modalidades de entrada

| Modalidade | Descrição | Implementação |
|---|---|---|
| **Texto** | Soletração sequencial a partir de string digitada pelo usuário | `src/speller.py` |
| **Voz** | Reconhecimento de fala contínuo em pt-BR em thread assíncrona | `src/voice.py` + Google Speech API |
| **Câmera** | Espelhamento em tempo real via estimativa de pose da mão | `src/camera.py` + MediaPipe |

### Codificação das poses

Cada caractere é representado como um vetor de 5 valores discretos (um por dedo), mapeados a ângulos de servo na tabela `SERVO_ANGLES` em `src/config.py`:

| Valor | Estado | Descrição |
|---|---|---|
| `0` | ○ Aberto | Dedo totalmente estendido |
| `0.33` | ◔ Pouco | Leve curvatura (~33% do range) |
| `0.66` | ◑ Meio | Semiflexão (~66% do range) |
| `1` | ● Fechado | Flexão máxima |

**Exemplo — letra L:**

```python
{"polegar": 0, "indicador": 0, "medio": 1, "anelar": 1, "minimo": 1}
#  ○ aberto      ○ aberto      ● fechado   ● fechado   ● fechado
```

O dicionário completo de poses (`src/poses.py`) cobre **32 sinais**: letras A–Z e dígitos 0–5. Os dígitos 6–9 requerem duas mãos e não são suportados nesta versão. O módulo de voz converte números por extenso em português para seus dígitos correspondentes (`"zero"` → `0`, `"um"` → `1`, ..., `"cinco"` → `5`).

## Hardware

### Lista de materiais

| Componente | Qtd | Especificação |
|---|---|---|
| Arduino Uno / Nano | 1 | Qualquer placa compatível com StandardFirmata |
| Micro servo SG90 | 5 | Torque: 1,8 kgf·cm; range: 0–180°; alimentação: 4,8–6 V |
| Kit de mão robótica | 1 | [Kit Mão Robótica 3D + Servos — Compatível com Arduino](https://produto.mercadolivre.com.br/MLB-3637665659-kit-mo-robotica-3d-servos-compativel-com-arduino-_JM) — impressão 3D, acionamento por tendões |
| Fios jumper M-M | ~16 | Conexão servos → pinos digitais do Arduino |

> ⚠️ **Alimentação:** recomenda-se fonte externa regulada de 5 V para os servos. Alimentar 5 servos SG90 simultaneamente pelo pino 5 V do Arduino pode exceder a corrente máxima suportada (~500 mA via USB), causando instabilidade ou danos à placa.

### Pinagem padrão

| Dedo | Pino digital (Arduino) |
|---|---|
| Polegar | 10 |
| Indicador | 9 |
| Médio | 8 |
| Anelar | 7 |
| Mínimo | 6 |

> Para alterar a pinagem, edite `src/config.py` → `FINGER_PINS`.

## Instalação e Configuração

### Firmware do Arduino

Carregue o **StandardFirmata** na placa antes de qualquer execução:

```
Arduino IDE → Arquivo → Exemplos → Firmata → StandardFirmata → Upload
```

### Ambiente Python

> 💡 **Recomendado: Python 3.10.** A biblioteca `pyFirmata 1.1.0` utiliza `inspect.getargspec`, removido no Python 3.11+. Versões superiores podem funcionar com ajustes no código, mas podem causar erros na inicialização do Arduino.

```bash
git clone https://github.com/ianderichalski/robo-libras.git
cd robo-libras

python --version   # confirme que é 3.10.x

python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### PyAudio (modo voz)

O `pyaudio` depende de bibliotecas nativas e requer instalação separada:

| Sistema | Comando |
|---|---|
| **Windows** | `pip install pipwin && pipwin install pyaudio` |
| **Linux (Ubuntu/Debian)** | `sudo apt install portaudio19-dev python3-dev && pip install pyaudio` |
| **macOS** | `brew install portaudio && pip install pyaudio` |

> O modo de voz requer conexão com a internet para acessar a Google Speech API.

### Modelo MediaPipe

O arquivo `hand_landmarker.task` é baixado automaticamente na primeira execução do modo câmera e salvo em `models/`. Para download manual:

```
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

### Porta serial

Edite `src/config.py` conforme o sistema operacional:

```python
SERIAL_PORT = "COM4"               # Windows
# SERIAL_PORT = "/dev/ttyUSB0"     # Linux
# SERIAL_PORT = "/dev/cu.usbmodem..."  # macOS
```

## Uso

### Interface Web (recomendado)

```bash
streamlit run app.py
```

Abre automaticamente no navegador. Disponibiliza os três modos de entrada, visualização em tempo real do estado de cada dedo e painel de conexão com o Arduino.

### Interface de Linha de Comando

```bash
python main.py
```

Menu interativo com os modos Voz, Texto, Câmera e Teste dos servos.

## Calibração dos Servos

> ⚠️ Os ângulos definidos em `src/config.py` foram calibrados especificamente para o modelo de mão utilizado. Modelos com dimensões de articulação ou comprimento de tendão distintos **exigem recalibração individual**.

```bash
python -m tools.calibrate
python -m tools.calibrate --port COM3   # porta alternativa
```

### Controles interativos

| Tecla | Ação |
|---|---|
| `d` / `a` | Incrementa / decrementa ±1° |
| `D` / `A` | Incrementa / decrementa ±10° |
| `1` | Salva ângulo atual como **aberto** |
| `2` | Salva ângulo atual como **pouco** |
| `3` | Salva ângulo atual como **meio** |
| `4` | Salva ângulo atual como **fechado** |
| `t` | Executa sequência de teste completa do dedo |
| `q` | Confirma dedo atual e avança ao próximo |

Ao concluir todos os dedos, o script imprime o bloco `SERVO_ANGLES` completo para substituição em `src/config.py`.

### Boas práticas

- Incremente o ângulo gradualmente (passos de 5°) e interrompa assim que o dedo atingir a posição desejada visualmente
- Não utilize 180° como padrão para a posição fechada — o limite seguro é o ângulo imediatamente anterior à resistência mecânica da articulação
- Um chiado leve em repouso é inerente ao SG90 (vibração da bobina pelo sinal PWM contínuo do Firmata) e não indica defeito; chiado intenso em uma pose específica indica que o ângulo ultrapassa o limite físico do mecanismo

## Estrutura do Repositório

```
├── app.py                    # Ponto de entrada da interface web (Streamlit)
├── main.py                   # Interface de linha de comando
├── requirements.txt          # Dependências Python
├── README.md
├── LICENSE
├── .gitignore
│
├── .streamlit/
│   └── config.toml           # Configuração visual da interface web
│
├── docs/
│   └── .gitkeep              # Diretório para demo.gif e demais mídias
│
├── models/
│   └── hand_landmarker.task  # Modelo MediaPipe (download automático, não versionado)
│
├── src/                      # Módulos do sistema (lógica de negócio)
│   ├── config.py             # Parâmetros centralizados (pinos, ângulos, timing)
│   ├── poses.py              # Dicionário de poses LIBRAS (A–Z, 0–5)
│   ├── servo.py              # Controlador de hardware via pyFirmata
│   ├── speller.py            # Motor de soletração com suporte a callbacks
│   ├── voice.py              # Listener de voz assíncrono (threading)
│   └── camera.py             # Pipeline de câmera (MediaPipe + OpenCV)
│
├── ui/                       # Interface Streamlit (apresentação)
│   ├── styles.py             # CSS customizado
│   ├── state.py              # Inicialização do session_state
│   ├── components.py         # Componentes visuais reutilizáveis
│   ├── actions.py            # Lógica de ações (conexão, soletração, câmera)
│   └── tabs/                 # Abas da interface
│       ├── texto_voz.py      # Aba Texto / Voz
│       ├── camera.py         # Aba Câmera
│       └── sobre.py          # Aba Sobre
│
└── tools/
    └── calibrate.py          # Ferramenta interativa de calibração dos servos
```

## Dependências

| Biblioteca | Versão | Finalidade |
|---|---|---|
| pyFirmata | 1.1.0 | Comunicação serial com Arduino via protocolo Firmata |
| Streamlit | ≥ 1.30 | Interface web interativa |
| MediaPipe | ≥ 0.10.18 | Estimativa de pose da mão (21 landmarks) |
| OpenCV | ≥ 4.8 | Captura e anotação de frames da câmera |
| SpeechRecognition | 3.10.4 | Interface com Google Speech API (pt-BR) |
| NumPy | ≥ 1.26, < 2 | Processamento matricial de imagem |
| Pillow | ≥ 10.0 | Suporte a formatos de imagem no Streamlit |
| protobuf | ≥ 4.25, < 5 | Serialização interna do MediaPipe |

## Limitações Conhecidas

- **Modo câmera:** a detecção de landmarks pelo MediaPipe opera com apenas uma mão por frame e requer iluminação adequada e contraste com o fundo
- **Modo voz:** depende de conexão com a internet e da disponibilidade da Google Speech API; ruído ambiente pode degradar o reconhecimento
- **Calibração:** os ângulos são específicos ao modelo físico utilizado e não são transferíveis diretamente a outros kits de mão robótica
- **Dígitos 6–9:** os sinais de 6 a 9 em LIBRAS requerem duas mãos simultâneas e não são suportados nesta versão de mão única

## Trabalhos Futuros

A versão 1.0 do projeto cobre o alfabeto manual da LIBRAS com uma mão robótica e três modalidades de entrada. As evoluções planejadas para versões futuras são:
 
**v1.x — Melhorias incrementais**
- Reconhecimento de letras da LIBRAS pela câmera em tempo real, identificando automaticamente qual sinal o usuário está formando com a mão
- Aprimoramento da detecção de gestos no modo câmera, com melhor robustez a variações de iluminação e posicionamento da mão
- Refinamento do processo de calibração dos servos, tornando-o mais guiado e reproduzível
- Melhorias na interface web, com foco em usabilidade e feedback visual em tempo real
 
**v2.0 — Suporte a duas mãos**
- Integração de uma segunda mão robótica para suporte aos dígitos 6–9 e sinais compostos do alfabeto manual da LIBRAS, que requerem uso simultâneo das duas mãos
- Sincronização em tempo real entre as duas mãos via dois Arduinos operando em paralelo
 
**v3.0 — Interface conversacional com LLM**
- Integração com um modelo de linguagem para tradução de texto ou voz diretamente para sinais completos de palavras em LIBRAS — não soletração letra por letra, mas o gesto real de cada palavra como a língua funciona de fato
- O fluxo previsto: `input → LLM → texto → tradutor LIBRAS → sinal da palavra → 2 mãos robóticas`
- Objetivo: tornar o sistema um canal de comunicação real e natural entre ouvintes e pessoas surdas

## Referências

[1] Zhang, F.; Bazarevsky, V.; Vakunov, A.; Tkachenka, A.; Sung, G.; Chang, C.; Grundmann, M. (2020).  
*MediaPipe Hands: On-device Real-time Hand Tracking.*  
arXiv:2006.10214.  
https://arxiv.org/abs/2006.10214  

[2] Google LLC. (2023).  
*MediaPipe Hand Landmarker — Hand landmarks detection guide.*  
Google for Developers.  
https://developers.google.com/mediapipe/solutions/vision/hand_landmarker  

[3] Firmata Developers.  
*StandardFirmata — Firmata firmware for Arduino.*  
GitHub.  
https://github.com/firmata/arduino  

[4] Gonzalez Amador, K. D. (2025).  
*Low-Cost Open-Source Ambidextrous Robotic Hand with 23 Direct-Drive Servos for American Sign Language Alphabet.*  
arXiv:2509.03690.  
https://arxiv.org/abs/2509.03690  

[5] Adeyanju, I. A. et al. (2023).  
*Design and prototyping of a robotic hand for sign language using locally-sourced materials.*  
Scientific African, 19, e01533.  
https://doi.org/10.1016/j.sciaf.2022.e01533  

[6] IBGE — Instituto Brasileiro de Geografia e Estatística. (2023).  
*Censo Demográfico 2022: Pessoas com Deficiência.*  
https://www.ibge.gov.br  


[7] FENEIS — Federação Nacional de Educação e Integração dos Surdos. (2020–2024).  
*Materiais institucionais sobre LIBRAS e acessibilidade.*  
https://www.feneis.org.br  