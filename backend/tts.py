import subprocess


class TextToSpeech:
    def __init__(self, dispositivo_audio="hw:1,0", voz="pt-br+f3", velocidade=180):
        self.dispositivo_audio = dispositivo_audio
        self.voz = voz
        self.velocidade = velocidade

    def falar(self, texto: str):
        """Sintetiza e reproduz o texto no dispositivo de áudio especificado."""
        try:
            espeak = subprocess.Popen(
                [
                    "espeak-ng",
                    "-v",
                    self.voz,
                    "-s",
                    str(self.velocidade),
                    "--stdout",
                    texto,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["aplay", "-D", self.dispositivo_audio],
                stdin=espeak.stdout,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            espeak.stdout.close()
        except Exception as e:
            print(f"Erro ao sintetizar voz: {e}")
