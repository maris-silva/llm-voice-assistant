import threading
import time
import subprocess
from pathlib import Path

from backend.stt import SpeechToText
from backend.musica import Player
from backend.hardware import HardwareController
from backend.tts import TextToSpeech

WAKE_WORD = "ativar"
SLEEP_WORDS = ["desativar", "cancelar", "pode ir", "tchau", "fechar"]
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_MUSICAS = RAIZ_PROJETO / "musicas"

TIMEOUT_MODO_ATIVO = 15.0


class AssistantEngine:
    def __init__(self, app_interface):
        self.app = app_interface
        self.player = Player(dispositivo_audio="hw:2,0")
        self.tts = TextToSpeech(
            dispositivo_audio="hw:2,0"
        )  # Inicialização do TTS no mesmo fone
        self.stt = None
        self.thread = None
        self.is_running = False

        self.comandos = {
            "acender_luz": (
                ["ligar a luz", "acender", "acender a luz", "luz"],
                self.cmd_acender_luz,
            ),
            "apagar_luz": (
                ["apagar", "apagar a luz", "desligar a luz", "escuro"],
                self.cmd_apagar_luz,
            ),
            "olivia_rodrigo": (
                [
                    "olivia",
                    "olivia rodrigo",
                    "toca olivia rodrigo",
                    "good 4 u",
                    "musica",
                    "rodrigo",
                ],
                self.cmd_tocar_musica,
            ),
            "parar_musica": (
                ["parar a musica", "parar musica", "para a musica", "parar"],
                self.cmd_parar_musica,
            ),
            "horas": (["horas", "que horas"], self.cmd_mostrar_horas),
            "desativar": (
                SLEEP_WORDS,
                self.cmd_desativar_modo_ativo,
            ),
        }

        self.vocab_comandos = [
            frase for gatilhos, _ in self.comandos.values() for frase in gatilhos
        ]

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._loop_escuta, daemon=True)
        self.thread.start()

    def stop(self):
        """Para o loop de escuta e limpa os subprocessos atrelados de mídia e síntese de voz"""
        self.is_running = False

        # Interrompe a execução do Player de áudio
        try:
            if hasattr(self, "player") and self.player:
                self.player.parar()
        except Exception:
            pass

        # Garante o término forçado dos processos aplay e espeak-ng órfãos no sistema
        try:
            subprocess.run(["pkill", "-f", "aplay"], stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-f", "espeak-ng"], stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def _loop_escuta(self):
        try:
            with SpeechToText() as stt:
                self.stt = stt
                self.stt.set_vocabulario([WAKE_WORD])
                modo_comando = False
                ultimo_comando_timestamp = 0

                self.log(f"Inicializado em modo inativo. Diga '{WAKE_WORD}'...")

                for texto in self.stt.escutar():
                    if not self.is_running:
                        break

                    tempo_atual = time.time()

                    if modo_comando and (
                        tempo_atual - ultimo_comando_timestamp > TIMEOUT_MODO_ATIVO
                    ):
                        modo_comando = False
                        self.stt.set_vocabulario([WAKE_WORD])
                        self.log(
                            "⏰ Timeout atingido. Voltando ao modo inativo (IDLE)."
                        )
                        self.app.after(0, lambda: self.app.set_assistant_state("IDLE"))

                    if not modo_comando:
                        if WAKE_WORD in texto:
                            modo_comando = True
                            ultimo_comando_timestamp = time.time()
                            self.stt.set_vocabulario(self.vocab_comandos)
                            self.log("🔔 Palavra de ativação detectada!")
                            self.app.after(
                                0, lambda: self.app.set_assistant_state("OUVINDO")
                            )
                            # Feedback sonoro opcional de confirmação ao ser ativado
                            self.tts.falar("Poodee faalaar.")
                    else:
                        ultimo_comando_timestamp = time.time()
                        self.log(f"🧠 Comando recebido: '{texto}'")
                        nome, acao = self._identificar_comando(texto)

                        if acao:
                            acao()
                            if nome == "desativar":
                                modo_comando = False
                                self.stt.set_vocabulario([WAKE_WORD])
                                continue
                        else:
                            self.log("❓ Comando não reconhecido.")
                            self.tts.falar(
                                "Deescuulpee, nããoo eenteendii oo coomaandoo."
                            )

        except Exception as e:
            self.log(f"❌ Erro no Engine de Voz: {e}")

    def _identificar_comando(self, texto):
        for nome, (gatilhos, acao) in self.comandos.items():
            for gatilho in gatilhos:
                if gatilho in texto:
                    return nome, acao
        return None, None

    def log(self, mensagem):
        self.app.after(0, lambda: self.app.log_debug(mensagem))

    def cmd_acender_luz(self):
        HardwareController.acender_luz()
        self.app.after(
            0, lambda: self.app.show_view("light", data=True, auto_return_seconds=4)
        )
        self.tts.falar("Luuz aaceesaa.")

    def cmd_apagar_luz(self):
        HardwareController.apagar_luz()
        self.app.after(
            0, lambda: self.app.show_view("light", data=False, auto_return_seconds=4)
        )
        self.tts.falar("Luuz aapaagaadaa.")

    def cmd_mostrar_horas(self):
        from datetime import datetime

        agora = datetime.now()
        texto_hora = (
            f"Aagooraa sããoo {agora.hour} hooraas ee {agora.minute} miinuutoos."
        )

        self.app.after(0, lambda: self.app.show_view("clock", auto_return_seconds=5))
        self.tts.falar(texto_hora)

    def cmd_tocar_musica(self):
        self.tts.falar("Toocaandoo Ooliiviiaa Roodriigoo.")
        faixa = self.player.tocar(PASTA_MUSICAS / "good4u.wav")
        self.app.after(0, lambda: self.app.show_view("song", data="good4u"))

    def cmd_parar_musica(self):
        self.player.parar()
        self.app.after(0, lambda: self.app.show_view("idle"))
        self.tts.falar("Múúsiicaa paaraadaa.")

    def cmd_desativar_modo_ativo(self):
        self.log("😴 Modo de escuta contínua encerrado pelo usuário.")
        self.tts.falar("Deesaatiivaandoo.")
        self.app.after(0, lambda: self.app.set_assistant_state("IDLE"))
        self.app.after(0, lambda: self.app.show_view("idle"))
