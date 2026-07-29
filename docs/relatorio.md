# LLM Voice Assistant - Assistente de Voz Offline Baseado em Raspberry Pi

## 1. Introdução

### 1.1 Motivação e Justificativa
Com a popularização de assistentes virtuais comerciais (como Amazon Alexa, Google Assistant e Apple Siri), a automação residencial e o controle de dispositivos por voz tornaram-se interfaces comuns de interação humano-computador. Contudo, esses sistemas comerciais possuem uma grande dependência de conectividade com a nuvem, o que impõe desafios significativos referentes à **privacidade dos dados**, **latência de rede** e **indisponibilidade na ausência de conexão à internet**.

A arquitetura proposta neste projeto aborda essas restrições por meio do desenvolvimento de um **Assistente de Voz 100% Offline**, embarcado em uma placa **Raspberry Pi 3**. Toda a inferência de áudio, processamento de palavras de ativação e reconhecimento de fala (*Speech-to-Text - STT*) ocorre diretamente no hardware local, garantindo a privacidade do usuário, eliminando o tráfego de dados para servidores externos e oferecendo uma resposta previsível e determinística.

Um projeto similar usado como  referência da comunidade open-source, foi o **Vosk**: [https://github.com/alphacep/vosk-api](https://github.com/alphacep/vosk-api).

---

## 2. Objetivos

### 2.1 Objetivo Geral

### 2.2 Objetivos Específicos

---

## 3. Especificação de Requisitos

A Tabela 1 detalha os Requisitos Funcionais (RF) e Não Funcionais (RNF) definidos para o sistema:

### Tabela 1: Especificação de Requisitos do Sistema
| ID | Descrição do Requisito | Tipo |
| :--- | :--- | :---: |
| **RF01** | Reconhecer a palavra de ativação (ex: `"Oi, Assistente"`) executando a inferência de áudio 100% localmente no hardware, sem dependência de conexão com a internet. | **RF** |
| **RF02** | O sistema deve mapear uma intenção de voz para acionar um componente de hardware periférico conectado (ex: controle de iluminação). | **RF** |
| **RF03** | Reconhecer a palavra de desativação (ex: `"Desligar Assistente"`) executando a inferência de áudio 100% localmente no hardware, e acionar modo "escuta inativa". | **RF** |
| **RF04** | Tocar arquivos de áudio locais (ex: `"Tocar Música 4"`, `"Tocar Parabéns Para Você"`) acionando o player nativo via saída P2 ou HDMI ao reconhecer o comando específico. | **RF** |
| **RNF01** | **Eficiência:** O intervalo de tempo entre o fim da fala do usuário e o início da ação do sistema não deve ultrapassar **2,5 segundos**. | **RNF** |
| **RNF02** | **Confiabilidade:** Deve apresentar uma taxa de acerto no reconhecimento do comando de pelo menos **85%** em um ambiente com ruído moderado. | **RNF** |
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
* **Teste T04 (RNF02)**: Teste de Confiabilidade com 100 emissões de comando em ambiente com ruído de fundo moderado (Target > 85% de acertos).

### 7.2 Tabela de Registro de Resultados
*(Esta seção será preenchida conforme a execução dos testes práticos)*

| ID Teste | Parâmetro Avaliado | Meta | Resultado Medido | Status |
| :--- | :--- | :---: | :---: | :---: |
| T01 | Tempo de feedback do LED ("Ouvindo") | < 500ms | *A preencher* | *Pendente* |
| T02 | Execução do comando "Aumentar Luz" | 100% Sucesso | *A preencher* | *Pendente* |
| T03 | Latência de processamento STT + Ação | < 2,5s | *A preencher* | *Pendente* |
| T04 | Taxa de acerto em ambiente ruidoso | >= 85% | *A preencher* | *Pendente* |

---

## 8. Conclusões e Trabalhos Futuros

### 8.1 Considerações Finais

### 8.2 Direções para Trabalhos Futuros

---

## Referências Bibliográficas

* 
*
*