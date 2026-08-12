import threading
import time
from pathlib import Path

from backend.stt import SpeechToText
from backend.musica import Player
from backend.hardware import HardwareController

WAKE_WORD = "ativar"
SLEEP_WORDS = ["desativar", "cancelar", "pode ir", "tchau", "fechar"]
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_MUSICAS = RAIZ_PROJETO / "musicas"

# Tempo limite em segundos sem detectar fala/comando antes de fechar a escuta ativa
TIMEOUT_MODO_ATIVO = 15.0


class AssistantEngine:
    def __init__(self, app_interface):
        self.app = app_interface
        self.player = Player(dispositivo_audio="hw:2,0")
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

                    # Verifica estouro do timeout baseado no tempo desde a última fala/escuta ativa
                    if modo_comando and (
                        tempo_atual - ultimo_comando_timestamp > TIMEOUT_MODO_ATIVO
                    ):
                        modo_comando = False
                        self.stt.set_vocabulario([WAKE_WORD])
                        self.log(
                            "⏰ Timeout de escuta atingido. Voltando ao modo inativo (IDLE)."
                        )
                        self.app.after(0, lambda: self.app.set_assistant_state("IDLE"))

                    if not modo_comando:
                        if WAKE_WORD in texto:
                            modo_comando = True
                            # Inicia o cronômetro do modo ativo exatamente ao escutar "ativar"
                            ultimo_comando_timestamp = time.time()
                            self.stt.set_vocabulario(self.vocab_comandos)
                            self.log(
                                "🔔 Palavra de ativação detectada! Escuta ativa iniciada."
                            )

                            self.app.after(
                                0, lambda: self.app.set_assistant_state("OUVINDO")
                            )
                    else:
                        # Sempre atualiza o timestamp após receber qualquer áudio do usuário no modo ativo
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

    # --- AÇÕES DA INTERFACE ---

    def cmd_acender_luz(self):
        HardwareController.acender_luz()
        self.app.after(
            0, lambda: self.app.show_view("light", data=True, auto_return_seconds=4)
        )

    def cmd_apagar_luz(self):
        HardwareController.apagar_luz()
        self.app.after(
            0, lambda: self.app.show_view("light", data=False, auto_return_seconds=4)
        )

    def cmd_mostrar_horas(self):
        self.app.after(0, lambda: self.app.show_view("clock", auto_return_seconds=5))

    def cmd_tocar_musica(self):
        faixa = self.player.tocar(PASTA_MUSICAS / "good4u.wav")
        # Sem auto_return_seconds: a SongPage fecha só ao terminar a música ou por comando de voz
        self.app.after(0, lambda: self.app.show_view("song", data="good4u"))

    def cmd_parar_musica(self):
        self.player.parar()
        self.app.after(0, lambda: self.app.show_view("idle"))

    def cmd_desativar_modo_ativo(self):
        self.log("😴 Modo de escuta contínua encerrado pelo usuário.")
        self.app.after(0, lambda: self.app.set_assistant_state("IDLE"))
        self.app.after(0, lambda: self.app.show_view("idle"))
