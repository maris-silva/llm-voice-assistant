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
* **Python 3.x**: Linguagem principal para orquestração da máquina de estados, manipulação de GPIO e chamada de bibliotecas STT.

### 5.2 Bibliotecas e Frameworks
* **STT Engine**: *Vosk API* (modelo em português brasileiro pré-treinado de vocabulário reduzido).

### 5.3 Hardware Utilizado

---

## 6. Metodologia de Desenvolvimento

---

## 7. Planos de Testes e Resultados Obtidos

### 7.1 Plano de Testes Planejados
* **Teste T01 (RF01 & RNF03)**: Validação do tempo de resposta do KWS ("Oi Assistente") e acionamento do LED de feedback visual em menos de 500ms.
* **Teste T02 (RF02 & RF04)**: Teste de precisão do acionamento de hardware (Lâmpada ON/OFF) e execução correta das faixas de áudio.
* **Teste T03 (RNF01)**: Medição de latência total entre o encerramento do comando de voz e a execução da ação (Target < 2,5s).
* **Teste T04 (RNF02)**: Teste de Confiabilidade com 100 emissões de comando em ambiente com ruído de fundo moderado (Target > 50% de acertos).

### 7.2 Tabela de Registro de Resultados
*(Esta seção será preenchida conforme a execução dos testes práticos)*

| ID Teste | Parâmetro Avaliado | Meta | Resultado Medido | Status |
| :--- | :--- | :---: | :---: | :---: |
| T01 | Tempo de feedback do LED ("Ouvindo") | < 500ms | *A preencher* | *Pendente* |
| T02 | Execução do comando "Aumentar Luz" | 100% Sucesso | *A preencher* | *Pendente* |
| T03 | Latência de processamento STT + Ação | < 2,5s | *A preencher* | *Pendente* |
| T04 | Taxa de acerto em ambiente ruidoso | >= 50% | *A preencher* | *Pendente* |

---

## 8. Conclusões e Trabalhos Futuros

### 8.1 Considerações Finais

### 8.2 Direções para Trabalhos Futuros

---

## Referências Bibliográficas

* 
*
*