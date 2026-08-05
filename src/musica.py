"""
musica.py — Tocador simples de arquivos WAV locais via aplay (ALSA).

Uso:
    player = Player(dispositivo_audio="hw:2,0")  # ex: headset USB (ver `aplay -l`)
    player.tocar("musicas/olivia_rodrigo")        # toca uma faixa aleatória da pasta
    player.parar()                                 # interrompe a reprodução
"""

import random
import subprocess
from pathlib import Path


class Player:
    def __init__(self, dispositivo_audio=None):
        """
        dispositivo_audio: dispositivo ALSA a forçar na saída, ex: "hw:2,0".
        Descubra o número certo com `aplay -l` (card X, device Y -> "hw:X,Y").
        Deixe None para usar a saída padrão do sistema.
        """
        self._dispositivo_audio = dispositivo_audio
        self._processo = None

    def tocar(self, caminho_pasta, aleatorio=True):
        """Toca uma faixa .wav da pasta informada (em background, não bloqueia)."""
        self.parar()  # garante que não fica música tocando por cima de outra

        pasta = Path(caminho_pasta)
        musicas = sorted(pasta.glob("*.wav"))
        if not musicas:
            print(f"⚠️ Nenhum .wav encontrado em '{pasta}'")
            return

        escolhida = random.choice(musicas) if aleatorio else musicas[0]
        print(f"🎵 Tocando: {escolhida.name}")

        comando = ["aplay", "-q"]
        if self._dispositivo_audio:
            comando += ["-D", self._dispositivo_audio]
        comando.append(str(escolhida))

        try:
            self._processo = subprocess.Popen(
                comando,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            print("❌ aplay não encontrado. Instale com: sudo apt install alsa-utils")

    def parar(self):
        """Interrompe a música atual, se houver alguma tocando."""
        if self._processo and self._processo.poll() is None:
            self._processo.terminate()
            self._processo.wait()
        self._processo = None

    def tocando(self):
        """True se alguma música estiver tocando no momento."""
        return self._processo is not None and self._processo.poll() is None