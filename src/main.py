import os
import re
import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

# Silencia os logs internos do Kaldi/Vosk (deixam o terminal mais limpo
# e evitam overhead de I/O desnecessário na RPi3)
SetLogLevel(-1)

SAMPLE_RATE = 16000

# --- Palavras-chave -------------------------------------------------------
WAKE_WORD = "ativar"

# Mapeia comando -> (lista de gatilhos, mensagem de execução)
# Usar uma gramática restrita ao invés de reconhecimento livre aumenta MUITO
# a precisão e reduz o uso de CPU, o que é essencial na RPi3.
COMANDOS = {
    "acender_luz": (["ligar a luz", "acender", "acender a luz", "luz"],
                     "💡 Executando: Ligando as luzes do quarto..."),
    "horas":       (["horas", "que horas"],
                     "⏰ Executando: Buscando o horário atual do sistema..."),
    "cancelar":    (["desligar", "cancelar"],
                     "😴 Executando: Cancelado."),
}

def montar_vocabulario(frases):
    """Extrai palavras únicas de uma lista de frases para montar a gramática."""
    palavras = set()
    for frase in frases:
        palavras.update(frase.split())
    return sorted(palavras)

# Vocabulário da gramática de "espera" (só precisa reconhecer a wake word,
# mas incluímos [unk] para não travar em outras falas)
VOCAB_ESPERA = json.dumps([WAKE_WORD, "[unk]"])

# Vocabulário da gramática de "comando" (todas as frases de gatilho + [unk])
todas_frases = [f for triggers, _ in COMANDOS.values() for f in triggers]
VOCAB_COMANDO = json.dumps(montar_vocabulario(todas_frases) + ["[unk]"])

# --- Áudio -----------------------------------------------------------------
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

print("⏳ Carregando o modelo de voz em português... Aguarde.")
try:
    model = Model(model_name="vosk-model-small-pt-0.3")
except Exception as e:
    print(f"❌ Erro ao carregar ou baixar o modelo: {e}")
    sys.exit(1)

def novo_reconhecedor(vocabulario):
    """Cria um KaldiRecognizer com gramática restrita (mais preciso e leve)."""
    r = KaldiRecognizer(model, SAMPLE_RATE, vocabulario)
    r.SetWords(True)
    return r

rec = novo_reconhecedor(VOCAB_ESPERA)

print("\n🤖 [Alexa Local]: Inicializada com sucesso!")
print("🎙️ Modo de Espera. Diga 'ativar' para falar um comando.")
print("-" * 60)

modo_comando = False
padrao_wake = re.compile(rf"\b{re.escape(WAKE_WORD)}\b")

def identificar_comando(texto):
    for nome, (gatilhos, msg) in COMANDOS.items():
        for gatilho in gatilhos:
            if re.search(rf"\b{re.escape(gatilho)}\b", texto):
                return nome, msg
    return None, None

try:
    try:
        stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000,
                                    dtype='int16', channels=1, callback=callback)
    except sd.PortAudioError as e:
        print(f"❌ Não consegui abrir o microfone: {e}")
        print("Dica: rode `python3 -c \"import sounddevice as sd; print(sd.query_devices())\"` "
              "para listar os dispositivos e ajuste sd.default.device se necessário.")
        sys.exit(1)

    with stream:
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                resultado = json.loads(rec.Result())
                texto = resultado.get("text", "").lower().strip()

                if not texto:
                    continue

                if not modo_comando:
                    if padrao_wake.search(texto):
                        print("\n🔔 [Alexa]: Diga o comando...")
                        modo_comando = True
                        rec = novo_reconhecedor(VOCAB_COMANDO)
                    else:
                        print(f"💤 Ouvido (Ignorado): '{texto}'")
                else:
                    print(f"🧠 [Comando Recebido]: '{texto}'")

                    nome, msg = identificar_comando(texto)
                    if msg:
                        print(msg)
                    else:
                        print("❓ Comando não reconhecido.")

                    print("-" * 60)
                    print("🎙️ Modo de Espera. Diga 'ativar'.")
                    modo_comando = False
                    rec = novo_reconhecedor(VOCAB_ESPERA)

except KeyboardInterrupt:
    print("\n\n👋 Assistente encerrado pelo usuário.")