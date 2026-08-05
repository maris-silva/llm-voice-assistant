"""
musica.py — Tocador simples de MP3 locais via mpg123 (leve, ideal p/ RPi3).

Uso:
    player = Player()
    player.tocar("musicas/olivia_rodrigo")   # toca uma faixa aleatória da pasta
    player.parar()                            # interrompe a reprodução
"""

import random
import subprocess
from pathlib import Path


class Player:
    def __init__(self):
        self._processo = None

    def tocar(self, caminho_pasta, aleatorio=True):
        """Toca uma faixa da pasta informada (em background, não bloqueia)."""
        self.parar()  # garante que não fica música tocando por cima de outra

        pasta = Path(caminho_pasta)
        musicas = sorted(pasta.glob("*.mp3"))
        if not musicas:
            print(f"⚠️ Nenhuma música encontrada em '{pasta}'")
            return

        escolhida = random.choice(musicas) if aleatorio else musicas[0]
        print(f"🎵 Tocando: {escolhida.name}")

        try:
            self._processo = subprocess.Popen(
                ["mpg123", "-q", str(escolhida)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            print("❌ mpg123 não encontrado. Instale com: sudo apt install mpg123")

    def parar(self):
        """Interrompe a música atual, se houver alguma tocando."""
        if self._processo and self._processo.poll() is None:
            self._processo.terminate()
            self._processo.wait()
        self._processo = None

    def tocando(self):
        """True se alguma música estiver tocando no momento."""
        return self._processo is not None and self._processo.poll() is None