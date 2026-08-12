# O QUE É O LLM VOICE ASSISTANT

[![Testes](https://github.com/maris-silva/llm-voice-assistant/actions/workflows/tests.yml/badge.svg)](https://github.com/maris-silva/llm-voice-assistant/actions/workflows/tests.yml)

## Assistente de Voz 100% Offline e Modular para Raspberry Pi

O **LLM Voice Assistant** é uma solução de assistente virtual embarcada desenvolvida para rodar totalmente **offline** em uma **Raspberry Pi 3**. O projeto prioriza a privacidade do usuário, eliminando o tráfego de dados para a nuvem e proporcionando baixa latência nas interações.

O sistema utiliza um mecanismo de **Speech-to-Text (STT)** em português que roda localmente. Ele atua em modo de espera aguardando um comando de palavra-chave (ex: `"ativar"`). Ao reconhecer a ativação, o assistente entra em um ciclo operacional modular que processa comandos de voz e executa ações diretas no hardware e software local.

### Destaques do Projeto
* **100% Offline:** Nenhuma requisição externa ou dependência de internet.
* **Hardware Embarcado:** Desenvolvido e otimizado para Raspberry Pi 3.
* **Periféricos Simples:** Utiliza um headset USB (fone de ouvido + microfone) para entrada de áudio e saída sonora.
* **Arquitetura Modular:** Estrutura expansível onde novos arquivos de comandos podem ser adicionados facilmente para estender as capacidades do assistente.
* **Funcionalidades Iniciais:**
  * **Controle de Hardware:** Acionamento e desligamento do LED da Raspberry Pi via GPIO.
  * **Feedback via Terminal:** Transcrição em tempo real e status da execução exibidos via linha de comando.


# ORGANIZAÇÃO DE PASTAS

A estrutura do diretório do projeto está organizada da seguinte forma:

```text
llm-voice-assistant/
├── docs/
│   └── relatorio.md        # Documentação completa e relatório final do projeto
├── src/
│   ├── LED.py             # Módulo de controle do LED da placa via GPIO
│   ├── main.py            # Script principal (orquestrador e loop de escuta)
│   └── stt.py             # Módulo de processamento Speech-to-Text (Vosk)
├── tests/
│   ├── conftest.py        # Configuração compartilhada (mocka hardware GPIO)
│   ├── test_comandos.py   # Testes do reconhecimento/roteamento de comandos
│   ├── test_stt.py        # Testes do SpeechToText (Vosk/microfone mockados)
│   ├── test_musica.py     # Testes do tocador de música (aplay mockado)
│   └── test_tts.py        # Testes do texto-para-voz (espeak-ng mockado)
├── .github/
│   └── workflows/
│       └── tests.yml      # CI: roda a suíte de testes a cada push/PR
├── .gitignore             # Arquivos ignorados pelo repositório Git
├── LICENSE                # Licença do projeto
└── README.md              # Visão geral e guia rápido de uso do projeto
```

# Guia Passo a Passo: Como Rodar o LLM Voice Assistant

## 1. Pré-requisitos de Hardware e Sistema

### Hardware Necessário
* **Placa:** Raspberry Pi 3 rodando **Raspberry Pi OS**.
* **Áudio:** Headset USB (ou microfone USB + saída de áudio).
* **Módulo LED:** 1x LED conectado ao **pino GPIO 17** e GND, utilizando um resistor (220Ω a 330Ω).

> **Nota:** A conexão com a internet é necessária **apenas na primeira execução** para que a biblioteca faça o download automático do modelo de voz. Depois disso, rodará 100% offline.

---

## 2. Preparação do Sistema Operacional

Abra o terminal do Raspberry Pi OS e instale as dependências de áudio nativas:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv portaudio19-dev libasound2-dev
```

---

## 3. Configuração do Ambiente Virtual (venv) e Bibliotecas

1. Navegue até a pasta do projeto:
   ```bash
   cd llm-voice-assistant
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as bibliotecas Python exatas que o seu código exige:
   ```bash
   pip install --upgrade pip
   pip install vosk sounddevice gpiozero
   ```

---

## 4. Teste e Configuração de Áudio

Antes de rodar o código, garanta que o microfone USB é o dispositivo padrão do sistema. Se o código falhar ao abrir o microfone, você pode descobrir o ID do seu microfone rodando:

```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```
*Anote o número do seu microfone e, se necessário, configure o `sd.default.device` no seu script.*

---

## 5. Rodando o Assistente de Voz

Com o ambiente virtual ativado (`venv`), inicie o script principal:

```bash
python3 src/main.py
```

### O que vai acontecer na primeira vez?
Como o código usa `Model(model_name="vosk-model-small-pt-0.3")`, **a primeira execução vai demorar um pouco mais**, pois o Vosk fará o download de aproximadamente 40MB do modelo para a pasta `.cache` da sua Raspberry.

### Fluxo de Interação
Assim que o terminal exibir `[Alexa Local]: Inicializada com sucesso!`, siga os passos:

1. **Ativação:** Diga **`"ativar"`**.
   * *O sistema responderá:* `🔔 [Alexa]: Diga o comando...`
2. **Envio de Comandos:** Fale um dos comandos programados.
   * Diga **`"ligar a luz"`** ou **`"acender"`** -> O LED no GPIO 17 acenderá.
   * Diga **`"horas"`** -> Ele reconhecerá a intenção de buscar a hora.
   * Diga **`"cancelar"`** -> O assistente volta a dormir.

---

## 6. Solução de Problemas (Troubleshooting)

| Problema | Solução |
| :--- | :--- |
| **`PermissionError: GPIO` ou `gpiomem`** | Seu usuário não tem permissão de hardware. Rode: `sudo usermod -aG gpio $USER`, reinicie a placa e tente de novo. |
| **`PortAudioError` no terminal** | O script não achou o microfone. Rode o comando do Passo 4 para listar os dispositivos de áudio e verificar a conexão. |
| **Fica travado no "Carregando modelo..."** | Verifique a conexão com a internet. O Vosk está tentando baixar o modelo na primeira execução. |

---

# Testes Automatizados

O projeto tem uma suíte de testes (`tests/`) que cobre o reconhecimento/roteamento de comandos, o `SpeechToText`, o tocador de música e o texto-para-voz. Hardware (microfone, GPIO) e processos externos (`aplay`, `espeak-ng`) são todos simulados — a suíte roda em qualquer máquina, não precisa de Raspberry Pi nem de microfone conectado.

## Comando rápido

Com o ambiente virtual ativado (Passo 3):

```bash
pytest --cov=src --cov-report=term-missing
```

## Vendo os resultados no GitHub

A cada push na `main` ou Pull Request aberto, o workflow [`Testes`](.github/workflows/tests.yml) roda automaticamente. Pra acompanhar:
* **Badge no topo deste README** — status da última execução na `main`.
* **Aba "Actions"** do repositório — lista cada execução, com o log completo.
* **Bolinha ao lado de cada commit** na lista de commits — indica se aquele commit passou nos testes.
* Dentro de uma execução específica, a aba **"Summary"** mostra a tabela de cobertura de testes.