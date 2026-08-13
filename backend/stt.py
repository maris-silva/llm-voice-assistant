import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

# Silencia os logs internos do Kaldi (feito uma única vez, no import do módulo)
SetLogLevel(-1)


class SpeechToText:
    def __init__(
        self,
        model_name="vosk-model-small-pt-0.3",
        sample_rate=16000,
        blocksize=4000,
        device=None,
    ):
        self._sample_rate = sample_rate
        self._blocksize = blocksize
        self._device = device
        self._queue = queue.Queue()
        self._stream = None

        print("⏳ Carregando o modelo de voz... Aguarde.")
        try:
            self._model = Model(model_name=model_name)
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar/baixar o modelo Vosk: {e}") from e

        self._rec = self._criar_recognizer(vocabulario=None)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        if self._stream is not None:
            return
        try:
            self._stream = sd.RawInputStream(
                samplerate=self._sample_rate,
                blocksize=self._blocksize,
                dtype="int16",
                channels=1,
                device=self._device,
                callback=self._callback,
            )
            self._stream.start()
        except sd.PortAudioError as e:
            raise RuntimeError(
                f"Não consegui abrir o microfone: {e}\n"
                "Dica: liste os dispositivos com "
                '`python3 -c "import sounddevice as sd; print(sd.query_devices())"` '
                "e passe o índice certo em device=."
            ) from e

    def stop(self):
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    # --- Configuração ---------------------------------------------------

    def set_vocabulario(self, palavras_ou_frases=None):
        self._rec = self._criar_recognizer(palavras_ou_frases)
        # Descarta áudio pendente (ex.: gravado durante o TTS ou antes da troca
        # de vocabulário) para a nova fase de escuta começar sem lixo acumulado.
        self._esvaziar_fila()

    def _esvaziar_fila(self):
        while True:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    def _criar_recognizer(self, vocabulario):
        if vocabulario:
            palavras = self._extrair_palavras(vocabulario)
            grammar = json.dumps(palavras + ["[unk]"])
            rec = KaldiRecognizer(self._model, self._sample_rate, grammar)
        else:
            rec = KaldiRecognizer(self._model, self._sample_rate)
        rec.SetWords(True)
        return rec

    @staticmethod
    def _extrair_palavras(frases):
        """Quebra uma lista de frases em palavras únicas (vocabulário do Vosk)."""
        palavras = set()
        for frase in frases:
            palavras.update(frase.lower().split())
        return sorted(palavras)

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self._queue.put(bytes(indata))

    def escutar(self, mostrar_parcial=False, timeout=None, on_resultado=None):
        """Gera textos reconhecidos. Se `timeout` for informado, gera `None`
        periodicamente durante silêncio (nenhum áudio finalizado), permitindo
        que quem consome o gerador faça verificações sensíveis a tempo (ex.:
        timeout de modo ativo) mesmo sem fala nova. `on_resultado`, se
        informado, é chamado com o texto bruto de cada resultado finalizado
        (inclusive vazio), útil para depuração."""
        if self._stream is None:
            self.start()

        while True:
            try:
                data = self._queue.get(timeout=timeout)
            except queue.Empty:
                yield None
                continue

            if self._rec.AcceptWaveform(data):
                resultado = json.loads(self._rec.Result())
                texto = resultado.get("text", "").strip().lower()
                if on_resultado:
                    on_resultado(texto)
                if texto:
                    yield texto
            elif mostrar_parcial:
                parcial = json.loads(self._rec.PartialResult()).get("partial", "")
                if parcial:
                    print(f"   ...{parcial}", end="\r")

    def escutar_uma_frase(self):
        for texto in self.escutar():
            return texto
