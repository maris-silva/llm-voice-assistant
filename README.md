# O QUE É O LLM VOICE ASSISTANT

[![Testes](https://github.com/maris-silva/llm-voice-assistant/actions/workflows/tests.yml/badge.svg)](https://github.com/maris-silva/llm-voice-assistant/actions/workflows/tests.yml)

## Assistente de Voz 100% Offline e Modular para Raspberry Pi

O **LLM Voice Assistant** é uma solução de assistente virtual embarcada desenvolvida para rodar totalmente **offline** em uma **Raspberry Pi 3**, combinando reconhecimento de fala (STT) e síntese de voz (TTS) executados localmente para conversar com o usuário. O projeto prioriza a privacidade do usuário, eliminando o tráfego de dados para a nuvem e proporcionando baixa latência nas interações.

O sistema utiliza um mecanismo de **Speech-to-Text (STT)** em português que roda localmente. Ele atua em modo de espera aguardando um comando de palavra-chave (ex: `"ativar"`). Ao reconhecer a ativação, o assistente entra em um ciclo operacional modular que processa comandos de voz e executa ações diretas no hardware e software local.

### Destaques do Projeto
* **100% Offline:** Nenhuma requisição externa ou dependência de internet.
* **Hardware Embarcado:** Desenvolvido e otimizado para Raspberry Pi 3.
* **Periféricos Simples:** Utiliza um headset USB (fone de ouvido + microfone) para entrada de áudio e saída sonora.
* **Arquitetura Modular:** Estrutura expansível onde novos arquivos de comandos podem ser adicionados facilmente para estender as capacidades do assistente.
* **Interface Gráfica:** Telas em `customtkinter` (repouso, ouvindo, luz, música) que refletem o estado do assistente em tempo real, com um painel de debug embutido.
* **Controle de Hardware:** Acionamento e desligamento do LED da Raspberry Pi via GPIO.
* **Reprodução de Música:** Toca faixas locais sob comando de voz, exibindo capa e progresso na tela.
* **Persistência de Sessão:** Detecta e sinaliza na tela se a execução anterior foi encerrada de forma abrupta (ex.: queda de energia), sem depender de hardware extra — ver [Seção 5.1](#51-persistência-de-sessão).


# ORGANIZAÇÃO DE PASTAS

A estrutura do diretório do projeto está organizada da seguinte forma:

```text
llm-voice-assistant/
├── main.py                 # Ponto de entrada único: sobe a interface gráfica e o backend
├── requirements.txt        # Dependências Python do projeto
├── musicas/                # Faixas de áudio (.wav) tocadas pelo assistente
├── docs/
│   └── relatorio.md        # Documentação completa e relatório final do projeto
├── backend/
│   ├── assistant_engine.py # Orquestrador: máquina de estados, thread de escuta, roteamento de comandos
│   ├── stt.py              # Speech-to-Text (Vosk)
│   ├── musica.py           # Tocador de áudio local (aplay)
│   ├── tts.py              # Texto-para-voz (espeak-ng)
│   ├── hardware.py         # Controle do LED via GPIO
│   └── state_log.py        # Persistência de sessão (detecta encerramento abrupto)
├── frontend/
│   ├── app.py       # Janela principal e troca de telas (customtkinter)
│   ├── constants.py
│   ├── pages/       # Telas: idle, clock, light, song
│   └── assets/      # Imagens usadas pelas telas (capas de música, ícones)
├── src/                     # Protótipo inicial (referência do desenvolvimento incremental;
│                            # não é mais o caminho de execução principal do sistema)
│   ├── LED.py
│   ├── main.py
│   └── stt.py
├── tests/
│   ├── conftest.py        # Configuração compartilhada (mocka hardware GPIO)
│   ├── test_comandos.py   # Testes do reconhecimento/roteamento de comandos
│   ├── test_stt.py        # Testes do SpeechToText (Vosk/microfone mockados)
│   ├── test_musica.py     # Testes do tocador de música (aplay mockado)
│   ├── test_tts.py        # Testes do texto-para-voz (espeak-ng mockado)
│   └── test_state_log.py  # Testes da persistência de sessão
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
* **Display:** monitor conectado via HDMI — o assistente roda com uma interface gráfica (`customtkinter`), não só via terminal.

> **Nota:** A conexão com a internet é necessária **apenas na primeira execução** para que a biblioteca faça o download automático do modelo de voz. Depois disso, rodará 100% offline.

---

## 2. Preparação do Sistema Operacional

Abra o terminal do Raspberry Pi OS e instale as dependências de áudio nativas:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv portaudio19-dev libasound2-dev alsa-utils espeak-ng
```

* `portaudio19-dev` / `libasound2-dev`: necessários pra `sounddevice` capturar o microfone.
* `alsa-utils`: fornece o `aplay`, usado pra tocar música e a fala sintetizada.
* `espeak-ng`: motor de síntese de voz (TTS) usado pelo assistente pra responder falando.

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

3. Instale as bibliotecas Python do projeto a partir do `requirements.txt`:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 4. Teste e Configuração de Áudio

Antes de rodar o código, garanta que o microfone USB é o dispositivo padrão do sistema. Se o código falhar ao abrir o microfone, você pode descobrir o ID do seu microfone rodando:

```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```
*Anote o número do seu microfone e, se necessário, configure o `sd.default.device` no seu script.*

### 4.1 Configurando o dispositivo de saída de áudio (música e TTS)

Música e a fala do assistente (TTS) saem via `aplay`, apontando pra um dispositivo ALSA (ex.: `hw:1,0`). **O índice do card do headset USB varia de máquina pra máquina** — e pode até mudar na mesma máquina se o headset for desconectado/reconectado ou a placa reiniciar. Por isso esse valor não é fixo no código: ele vem da variável de ambiente `AUDIO_DEVICE`, com `hw:1,0` como padrão se ela não estiver definida.

1. Descubra o card certo **na máquina que você está usando agora**:
   ```bash
   aplay -l
   ```
   Procure a linha do headset USB, ex.: `card 1: Device [USB Audio Device]...` → o dispositivo é `hw:1,0`.

2. Se o card não for `1` (o padrão), exporte a variável antes de rodar o app:
   ```bash
   export AUDIO_DEVICE=hw:2,0
   ```

3. Pra não precisar repetir isso a cada sessão, adicione essa linha no final do `~/.bashrc` (ou `~/.profile`) **daquela máquina específica** e abra um terminal novo.

> **Importante:** `AUDIO_DEVICE` é uma configuração local de cada máquina/Raspberry Pi (fica no `~/.bashrc` dela), não do projeto — cada uma guarda o próprio valor. Se o assistente ficar mudo depois de trocar de máquina, o primeiro passo é sempre rodar `aplay -l` de novo e conferir/reexportar essa variável lá.

---

## 5. Rodando o Assistente de Voz

Com o ambiente virtual ativado (`venv`), inicie o script principal (na raiz do projeto):

```bash
python3 main.py
```

Isso abre a janela do assistente (interface `customtkinter`) e inicia a escuta em segundo plano. O `src/main.py` que aparece na árvore de pastas é o protótipo inicial do projeto, mantido só como referência — não é mais o caminho de execução usado.

### O que vai acontecer na primeira vez?
Como o código usa `Model(model_name="vosk-model-small-pt-0.3")`, **a primeira execução vai demorar um pouco mais**, pois o Vosk fará o download de aproximadamente 40MB do modelo para a pasta `.cache` da sua Raspberry (o terminal mostra `⏳ Carregando o modelo de voz... Aguarde.` nesse meio tempo).

### Fluxo de Interação
Assim que a janela abrir na tela de **Repouso**, siga os passos:

1. **Ativação:** Diga **`"ativar"`**.
   * *O sistema responde:* a tela muda para "Ouvindo" e o assistente confirma por voz (TTS).
2. **Envio de Comandos:** Fale um dos comandos programados.
   * Diga **`"ligar a luz"`** ou **`"acender"`** -> o LED no GPIO 17 acende e a tela reflete o estado.
   * Diga **`"horas"`** -> o assistente fala e mostra o horário atual.
   * Diga **`"tocar olivia rodrigo"`**, **`"tocar armandinho"`** ou **`"crystal castles"`** -> toca a faixa e abre a tela de música (capa, progresso, curtir).
   * Diga **`"cancelar"`**, **`"desativar"`** ou **`"tchau"`** -> o assistente volta a dormir.
3. **Painel de Debug (opcional):** ative o switch **"MODO DEBUG"** no rodapé da janela para acompanhar em tempo real o log de eventos reconhecidos pelo sistema.

### 5.1 Persistência de Sessão

A cada execução, o sistema registra início e fim em `sessao.log` (raiz do projeto, não versionado — ver `.gitignore`). Se a Raspberry Pi perder energia ou o processo for encerrado de forma abrupta (sem passar pelo `Ctrl+C`/fechamento da janela), esse arquivo fica com um registro de início sem o registro de fim correspondente.

Na execução seguinte, o sistema detecta essa inconsistência automaticamente:
* O painel **"MODO DEBUG"** abre sozinho, mesmo que o switch esteja desligado.
* Aparece a mensagem: `⚠️ Sessão anterior não encerrou corretamente (última atividade: ...)`.

Isso funciona sem nenhum hardware extra — o arquivo é só texto em disco, que sobrevive normalmente a uma queda de energia. Pra simular esse cenário sem precisar desligar a placa fisicamente, mate o processo à força em vez de fechar normalmente e rode de novo:
```bash
pkill -9 -f "python3 main.py"
python3 main.py
```

---
## 6. Implementação da memória SWAP e priorização do processo 
### 6.1. Configuração de SWAP (WSL 2)
A alteração do SWAP ocorre via arquivo `.wslconfig` no Windows (`%USERPROFILE%`):
1. **Editar/Criar `%USERPROFILE%\.wslconfig`**:
   ```ini
   [wsl2]
   memory=8GB
   swap=16GB
2. Aplicar: Execute `wsl --shutdown` no PowerShell e reinicie o terminal.

3. Validar: Use `free -h` ou `swapon --show` no Linux.

### 6.2. Priorização de Processos
Prioridade de CPU :

`sudo nice -n -20 python3 main.py`

---

## 7. Solução de Problemas (Troubleshooting)

| Problema | Solução |
| :--- | :--- |
| **`PermissionError: GPIO` ou `gpiomem`** | Seu usuário não tem permissão de hardware. Rode: `sudo usermod -aG gpio $USER`, reinicie a placa e tente de novo. |
| **`PortAudioError` no terminal** | O script não achou o microfone. Rode o comando do Passo 4 para listar os dispositivos de áudio e verificar a conexão. |
| **Fica travado no "Carregando modelo..."** | Verifique a conexão com a internet. O Vosk está tentando baixar o modelo na primeira execução. |
| **Comando de música/hora executa mas não sai som nenhum** | `AUDIO_DEVICE` está apontando pro card ALSA errado nessa máquina. Rode `aplay -l`, confira o card do headset e exporte `AUDIO_DEVICE=hw:X,0` com o número certo (veja Seção 4.1). |

---

# Testes Automatizados

O projeto tem uma suíte de testes (`tests/`) que cobre o reconhecimento/roteamento de comandos, o `SpeechToText`, o tocador de música, o texto-para-voz e a persistência de sessão. Hardware (microfone, GPIO) e processos externos (`aplay`, `espeak-ng`) são todos simulados — a suíte roda em qualquer máquina, não precisa de Raspberry Pi nem de microfone conectado.

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