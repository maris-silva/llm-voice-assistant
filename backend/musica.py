import random
import subprocess
from pathlib import Path


class Player:
    def __init__(self, dispositivo_audio=None):
        self._dispositivo_audio = dispositivo_audio
        self._processo = None

    def tocar(self, caminho_pasta_ou_arquivo):
        self.parar()
        caminho = Path(caminho_pasta_ou_arquivo)

        if caminho.is_dir():
            faixas = sorted(list(caminho.glob("*.wav")) + list(caminho.glob("*.mp3")))
            if not faixas:
                print(f"⚠️ Nenhuma faixa áudio em '{caminho}'")
                return None
            escolhida = random.choice(faixas)
        else:
            escolhida = caminho

        if not escolhida.exists():
            print(f"⚠️ Arquivo não encontrado: {escolhida}")
            return None

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
            return escolhida.stem
        except FileNotFoundError:
            print("❌ aplay não encontrado.")
            return None

    def parar(self):
        if self._processo and self._processo.poll() is None:
            self._processo.terminate()
            self._processo.wait()
        self._processo = None