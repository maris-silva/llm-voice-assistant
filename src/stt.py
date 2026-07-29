import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)  # silencia logs internos do Kaldi

SAMPLE_RATE = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

print("⏳ Carregando o modelo de voz em português... Aguarde.")
try:
    model = Model(model_name="vosk-model-small-pt-0.3")
    rec = KaldiRecognizer(model, SAMPLE_RATE)
except Exception as e:
    print(f"❌ Erro ao carregar ou baixar o modelo: {e}")
    sys.exit(1)

print("🎙️ Ouvindo... fale algo (Ctrl+C para sair)")
print("-" * 60)

try:
    try:
        stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000,
                                    dtype='int16', channels=1, callback=callback)
    except sd.PortAudioError as e:
        print(f"❌ Não consegui abrir o microfone: {e}")
        print("Dica: rode `python3 -c \"import sounddevice as sd; print(sd.query_devices())\"` "
              "para listar os dispositivos.")
        sys.exit(1)

    with stream:
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                resultado = json.loads(rec.Result())
                texto = resultado.get("text", "").strip()
                if texto:
                    print(f"📝 {texto}")
            else:
                # Texto parcial (ainda sendo reconhecido) — opcional, mostra em tempo real
                parcial = json.loads(rec.PartialResult()).get("partial", "").strip()
                if parcial:
                    print(f"   ...{parcial}", end="\r")

except KeyboardInterrupt:
    print("\n\n👋 Encerrado pelo usuário.")