import threading
from pathlib import Path
from datetime import datetime

from backend.stt import SpeechToText
from backend.musica import Player
from backend.hardware import HardwareController

WAKE_WORD = "ativar"
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_MUSICAS = RAIZ_PROJETO / "songs"


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

                self.log(f"Inicializado. Diga '{WAKE_WORD}'...")

                for texto in self.stt.escutar():
                    if not self.is_running:
                        break

                    if not modo_comando:
                        if WAKE_WORD in texto:
                            modo_comando = True
                            self.stt.set_vocabulario(self.vocab_comandos)
                            self.log("🔔 Palavra de ativação detectada!")

                            # Atualiza UI para estado OUVINDO
                            self.app.after(
                                0, lambda: self.app.views["idle"].set_state("OUVINDO")
                            )
                    else:
                        self.log(f"🧠 Comando recebido: '{texto}'")
                        nome, acao = self._identificar_comando(texto)

                        if acao:
                            acao()
                        else:
                            self.log("❓ Comando não reconhecido.")
                            self.app.after(
                                0, lambda: self.app.views["idle"].set_state("IDLE")
                            )

                        # Retorna ao modo de espera
                        modo_comando = False
                        self.stt.set_vocabulario([WAKE_WORD])

        except Exception as e:
            self.log(f"❌ Erro no Engine de Voz: {e}")

    def _identificar_comando(self, texto):
        for nome, (gatilhos, acao) in self.comandos.items():
            for gatilho in gatilhos:
                if gatilho in texto:
                    return nome, acao
        return None, None

    def log(self, mensagem):
        """Envia mensagens de log com segurança para a UI"""
        self.app.after(0, lambda: self.app.log_debug(mensagem))

    # --- AÇÕES E INTEGRAÇÃO COM AS PÁGINAS ---

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
        faixa = self.player.tocar(PASTA_MUSICAS / "good4u.mp3")
        self.app.after(
            0, lambda: self.app.show_view("song", data="good4u", auto_return_seconds=10)
        )

    def cmd_parar_musica(self):
        self.player.parar()
        self.app.after(0, lambda: self.app.show_view("idle"))
