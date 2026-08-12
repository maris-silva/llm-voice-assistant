import subprocess

def falar(texto, voz="pt-br", velocidade=120):
    espeak = subprocess.Popen(
        ["espeak-ng", "-v", voz,"-s", str(velocidade), "--stdout", texto],
        stdout=subprocess.PIPE
    )
    subprocess.run(
        ["aplay", "-D", "default"],
        stdin=espeak.stdout
    )
    espeak.stdout.close()

if __name__ == "__main__":
    falar("Olá, isso é um teste de texto para voz rodando em Python no Raspberry Pi")