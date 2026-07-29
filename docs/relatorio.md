# LLM Voice Assistant - Assistente de Voz Offline Baseado em Raspberry Pi

## 1. Introdução

### 1.1 Motivação e Justificativa
Com a popularização de assistentes virtuais comerciais (como a Alexa da Amazon, o Google Assistant e a Siri da Apple), a automação residencial e o controle de dispositivos por voz tornaram-se interfaces comuns de interação humano-computador. Contudo, esses sistemas comerciais possuem uma grande dependência de conectividade com a nuvem, o que impõe desafios significativos referentes à **privacidade dos dados**, **latência de rede** e **indisponibilidade na ausência de conexão à internet**.

A arquitetura proposta neste projeto aborda essas restrições por meio do desenvolvimento de um **Assistente de Voz 100% Offline**, embarcado em uma placa **Raspberry Pi 3**. Toda a inferência de áudio, processamento de palavras de ativação e reconhecimento de fala (*Speech-to-Text - STT*) ocorre diretamente no hardware local, garantindo a privacidade do usuário, eliminando o tráfego de dados para servidores externos e oferecendo uma resposta previsível e determinística.

Um projeto similar usado como  referência da comunidade open-source, foi o **Vosk API**: [https://github.com/alphacep/vosk-api](https://github.com/alphacep/vosk-api).

---

## 2. Objetivos

### 2.1 Objetivo Geral
Desenvolver, integrar e avaliar um Assistente de Voz 100% Offline e embarcado em uma plataforma Raspberry Pi 3, capaz de processar comandos de fala localmente para o controle acionável de iluminação periférica via GPIO e reprodução de faixas de áudio nativas, garantindo privacidade, baixa latência e operação independente de conectividade com a internet.

### 2.2 Objetivos Específicos
* **Reconhecimento de Fala (STT) e Mapeamento de Comandos:**
  * Integrar um motor de *Speech-to-Text* (STT) de vocabulário restrito otimizado para a arquitetura ARM do Raspberry Pi 3.
  * Implementar um algoritmo determinístico de correspondência de texto (*string matching*) para mapear comandos específicos (ex: `"Ligar LED"`, `"Tocar Olivia Rodrigo"`, `"Horas"`).

* **Integração de Hardware e Atuadores:**
  * Mapear e controlar os pinos da interface GPIO da placa por meio de um módulo isolado de iluminação ( módulo de controle do LED).
  * Gerenciar a reprodução de mídias sonoras locais através de um player de áudio por meio, também, de um outro módulo isolado.

* **Validação de Desempenho e Qualidade (Requisitos Não Funcionais):**
  * Assegurar a eficiência temporal do sistema, garantindo um intervalo máximo de **2,5 segundos** entre o término da fala do usuário e a ação correspondente (RNF01).
  * Obter uma confiabilidade de reconhecimento com taxa de acerto igual ou superior a **50%** em cenários com nível de ruído ambiental moderado (RNF02).
  * Garantir um tempo de resposta de usabilidade com indicativos visuais/sonoros imediatos em até **500 ms** ao transitar entre estados (RNF03).
  
* **(Opcional) Interface para depuração:**
  * Desenvolver uma interface gráfica que facilite a depuração do sistema desenvolvido, centralizando informações como o seu estado atual em tempo real durante execução, as palavras reconhecidas e se, possível, um botão que permita o início da fala do comando pelo usuário.
  *  A interface visa facilitar o entendimento do sistema e seu funcionamento, tanto pelos desenvolvedores quanto para os avaliadores do projeto.
---

## 3. Especificação de Requisitos

A Tabela 1 detalha os Requisitos Funcionais (RF) e Não Funcionais (RNF) definidos para o sistema ao longo da matéria:

### Tabela 1: Especificação de Requisitos do Sistema
| ID | Descrição do Requisito | Tipo |
| :--- | :--- | :---: |
| **RF01** | Reconhecer a palavra de ativação (ex: `"Ativar"`) executando a inferência de áudio 100% localmente no hardware, sem dependência de conexão com a internet. | **RF** |
| **RF02** | O sistema deve mapear uma intenção de voz (ex: `"Luz"`) para acionar um componente de hardware periférico conectado (ex: controle de iluminação). | **RF** |
| **RF03** | Reconhecer a palavra de desativação (ex: `"Desligar"`) executando a inferência de áudio 100% localmente no hardware, e acionar modo "escuta inativa". | **RF** |
| **RF04** | Tocar arquivos de áudio locais (ex: `"Tocar Olivia Rodrigo"`) acionando o player nativo via saída P2 ou HDMI ao reconhecer o comando específico. | **RF** |
| **RF05** | Indicar as horas no momento atual ao reconhecer o comando específico. (ex: `"Horas"`) | **RF** |
| **RNF01** | **Eficiência:** O intervalo de tempo entre o fim da fala do usuário e o início da ação do sistema não deve ultrapassar **2,5 segundos**. | **RNF** |
| **RNF02** | **Confiabilidade:** Deve apresentar uma taxa de acerto no reconhecimento do comando de pelo menos **50%** em um ambiente com ruído moderado. | **RNF** |
| **RNF03** | **Usabilidade:** Deve fornecer indicativos perceptíveis e imediatos (visuais ou sonoros) em até **500ms** para três estados: `"Ouvindo"`, `"Processando"` e `"Erro de Compreensão"`. | **RNF** |

---

## 4. Arquitetura do Sistema

### 4.1 Arquitetura Física
A arquitetura de hardware é centralizada na placa **Raspberry Pi 3 Model XXXXX **. 

### 4.2 Arquitetura de Software e Modelagem Comportamental

#### 4.2.1 Máquina de Estados (Diagrama de Transição de Estados)
O comportamento do sistema é regido por uma Máquina de Estados:

---

## 5. Ferramentas, Linguagens e Componentes

### 5.1 Linguagens de Programação
* **Python 3.x**: Linguagem adotada para o desenvolvimento de toda a lógica do assistente. Foi escolhida devido ao suporte maduro a sistemas embarcados, facilidade de integração com drivers de áudio/hardware e ecossistema de bibliotecas para processamento de voz local.

### 5.2 Bibliotecas e Frameworks
* **Speech-to-Text (STT) Engine:**
  * `vosk` (Vosk API): Pacote de reconhecimento de fala offline. Utiliza um modelo em Português do Brasil de vocabulário restrito otimizado para a arquitetura ARM, permitindo a conversão áudio-texto local.
* **Manipulação de Hardware (GPIO):**
  * `gpiozero`: Biblioteca para controle dos pinos de entrada e saída (GPIO) da Raspberry Pi 3, responsável pelo acionamento do hardware de iluminação (LED) 
* **Processamento e Captura de Áudio:**
  * `pyaudio` (Interface Python para PortAudio, já instalada na placa): Utilizada para realizar a captura contínua do fluxo de áudio em tempo real enviado pelo microfone.

### 5.3 Hardware Utilizado
* **Placa de Processamento Central (SBC):** Raspberry Pi 3 Model B.
* **Dispositivo de Captura e Saída de Som:** Headset USB.

---
## 6. Metodologia de Desenvolvimento

A metodologia adotada para a construção do assistente de voz offline fundamentou-se nos princípios já trabalhados anteriormente em laboratório de **desenvolvimento iterativo e incremental**, alinhados a boas práticas de **engenharia de software** (como os princípios SOLID). O foco principal da estrutura de código em `src/` foi garantir a **modularização**, o **desacoplamento de bibliotecas externas** e a **reutilização de componentes**, viabilizando a adição progressiva de novas funcionalidades ao longo das semanas de desenvolvimento sem a necessidade de refatorações destrutivas, de forma que seja possível adicionar o máximo de funcionalidades possível até a entrega final.

---

### 6.1 Estrutura Modular e Desacoplamento do Código

A arquitetura de software implementada no diretório `src/` isolou as responsabilidades do sistema em módulos independentes. Essa abordagem viabilizou a abstração dependências de bibliotecas de terceiros, garantindo as seguintes vantagens arquiteturais:

* **Abstração das Engines de Áudio:** Os motores de inferência local (*Vosk*, etc.) não estão acoplados diretamente ao fluxo principal do sistema. Em vez disso, são encapsulados por interfaces/wrappers específicos. Caso seja necessário substituir a biblioteca de *Speech-to-Text* por outra alternativa mais leve ou robusta, a mudança fica restrita ao módulo correspondente, mantendo o restante da aplicação intocado.
* **Isolamento da Camada de Hardware (GPIO Driver):** O controle dos atuadores (iluminação/módulo relé e LEDs de status) e sensores (botão físico) é intermediado por uma camada de controle que abstrai as chamadas diretas de bibliotecas de hardware (como `gpiozero`). Essa segregação foi definida também de modo a facilitar a realização de testes unitários durante o isolamento de falhas.
* **Desencadeamento por Eventos e Máquina de Estados:** O orquestrador central do sistema (`main.py` / controlador) gerencia as transições entre estados (*Escuta Passiva*, *Escuta Ativa*, *Processando* e *Repouso*) sem se preocupar com os detalhes de baixo nível da captura do sinal do áudio USB ou do controle de periféricos ligados à placa.

---
### 6.2 Fluxo Iterativo de Implementação

O ciclo de desenvolvimento do repositório foi organizado em fases incrementais e orientadas a testes. A estratégia permitiu validar o comportamento do sistema camada por camada, combinando a construção de **módulos isolados** com a execução de **testes unitários automatizados** e **testes de não-regressão** para garantir que a inclusão de novas funcionalidades não quebrasse os recursos já validados.

1. **Módulo STT de Captura e Testes Unitários de Áudio:**
   * Desenvolvimento isolado do módulo de captura do microfone USB.

2. **Módulo de Controle de Periféricos via GPIO (Luz/LED) e Testes de Atuação:**
   * Desenvolvimento do módulo desacoplado de hardware para manipulação de pinos GPIO (para o caso do LED).

3. **Módulo Orquestrador Central do Sistema:**
   * Integração do motor de *Speech-to-Text* (STT) com vocabulário restrito e parser de *string matching* para o entrar em estado de Escuta e ligar o LED.

4. **Retorno de Horário Atual:** 
   * Extensão incremental do orquestrador para suportar a função utilitária de horário atual via comando `"Horas"`.

5. **Tocar músicas pré-definidas:** 
    * Desenvolvimento de módulo de controle de hardware também asbtraído para tocar a música escolhida pelo usuário por meio do comando (`"Tocar {música}"`).

6. **Desenvolvimento de interface de depuração:**
    * Execução de **testes de não-regressão** automatizados para assegurar que a adição da leitura do relógio e faixas musicais não alterou a assertividade dos comandos de iluminação criados anteriormente.

A cada passo avançado, o grupo planeja adicionar testes unitários automatizados ao repositório, de forma a permitir validações rápidas de funcionamento, e também adicionar **testes de não-regressão**, os quais serão atualizados gradativa e iterativamente a partir do Passo 4 para cada nova funcionalidade que conseguirmos desenvolver.

7. **Documentação Final e Realização de Testes Planejados:**
    * Com o sistema completo desenvolvido, realizaremos um último grupo de testes, seguindo a a Tabela de Testes Planejados explicitada abaixo, para documentar os resultados e o desempenho do sistema no relatório 

---
## 7. Testes Planejados

### 7.1 Testes Planejados
* **Teste T01 (RF01 & RNF03)**: Validação do tempo de resposta de (`"Ativar"`) e (`"Desligar"`) com feedback visual em menos de 500ms.
* **Teste T02 (RF02)**: Teste de precisão do acionamento de hardware (LED ligado e desligado).
* **Teste T03 (RF04)**: Teste de execução correta das faixas de áudio pré-definidas.
* **Teste T04 (RF05)**: Teste de display correto do horário atual com o comando (`"Horas"`).
* **Teste T05 (RNF01)**: Cronometragem de latência total entre o encerramento do comando de voz e a execução da ação para diversas amostragens (desejado menor que 2,5s). 
* **Teste T06 (RNF02)**: Teste de Confiabilidade também com diversas emissões de comando (~50) em ambiente com ruído de fundo moderado (desejado pelo menos 50% de acertos).

### 7.2 Resultados Observados
*(Esta seção será preenchida incrementalmente)*

| ID Teste | Parâmetro Avaliado | Requisitos Associados | Meta | Resultado Medido | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **T01** | Tempo de resposta para palavras de ativação/desativação (`"Ativar"` e `"Desligar"`) e indicação de feedback visual | RF01, RNF03 | < 500 ms | *A preencher* | *Pendente* |
| **T02** | Precisão do acionamento de hardware do periférico (LED Ligar/Desligar) | RF02 | 100% de sucesso nas acionaçoes | *A preencher* | *Pendente* |
| **T03** | Execução e reprodução correta das faixas de áudio pré-definidas | RF04 | 100% de execução correta | *A preencher* | *Pendente* |
| **T04** | Exibição/retorno correto do horário atual após comando de voz (`"Horas"`) | RF05 | 100% de precisão | *A preencher* | *Pendente* |
| **T05** | Latência total entre o fim do comando de voz e a execução da ação (amostragem contínua) | RNF01 | < 2,5 s | *A preencher* | *Pendente* |
| **T06** | Taxa de acerto/confiabilidade no reconhecimento de comandos em ambiente ruidoso (~50 emissões) | RNF02 | >= 50% de acertos | *A preencher* | *Pendente* |
---

## 8. Conclusões e Trabalhos Futuros
*(Esta seção será preenchida futuramente)*

### 8.1 Considerações Finais

### 8.2 Direções para Trabalhos Futuros

---

## Referências Bibliográficas
* 
*
*