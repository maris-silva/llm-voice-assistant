from pathlib import Path
from gpiozero import Buzzer
from stt import SpeechToText
from musica import Player

WAKE_WORD = "ativar"
player = Player()

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_OLIVIA_RODRIGO = RAIZ_PROJETO / "musicas" 
buzzer = Buzzer(12)  # ajuste o pino GPIO conforme sua ligação


def acender_luz():
    buzzer.on()
    print("💡 Executando: Ligando as luzes do quarto...")


def apagar_luz():
    buzzer.off()
    print("🌑 Executando: Desligando as luzes do quarto...")


def mostrar_horas():
    from datetime import datetime
    print(f"⏰ Agora são: {datetime.now().strftime('%H:%M')}")


def cancelar():
    print("😴 Executando: Cancelado.")


def tocar_olivia_rodrigo():
    player.tocar(PASTA_OLIVIA_RODRIGO)
 
 
def parar_musica():
    player.parar()
    print("⏹️ Música parada.")

# comando -> (frases-gatilho, função a executar)
COMANDOS = {
    "acender_luz": (["ligar a luz", "acender", "acender a luz", "luz"], acender_luz),
    "apagar_luz":  (["apagar","apagar a luz", "desligar a luz", "escuro"], apagar_luz),
    "olivia_rodrigo": (["olivia", "olivia rodrigo", "toca olivia rodrigo", "musica da olivia"], tocar_olivia_rodrigo),
    "parar_musica":   (["parar a musica", "parar musica", "para a musica"], parar_musica),
    "horas":       (["horas", "que horas"], mostrar_horas),
    "cancelar":    (["desligar", "cancelar"], cancelar),
}

VOCAB_COMANDOS = [frase for gatilhos, _ in COMANDOS.values() for frase in gatilhos]


def identificar_comando(texto):
    for nome, (gatilhos, acao) in COMANDOS.items():
        for gatilho in gatilhos:
            if gatilho in texto:
                return nome, acao
    return None, None


def main():
    with SpeechToText() as stt:
        print("\n🤖 [Alexa Local]: Inicializada com sucesso!")
        print("🎙️ Modo de Espera. Diga 'ativar' para falar um comando.")
        print("-" * 60)

        stt.set_vocabulario([WAKE_WORD])
        modo_comando = False

        for texto in stt.escutar():
            if not modo_comando:
                if WAKE_WORD in texto:
                    print("\n🔔 [Alexa]: Diga o comando...")
                    modo_comando = True
                    stt.set_vocabulario(VOCAB_COMANDOS)
                else:
                    print(f"💤 Ouvido (Ignorado): '{texto}'")
            else:
                print(f"🧠 [Comando Recebido]: '{texto}'")
                nome, acao = identificar_comando(texto)
                if acao:
                    acao()
                else:
                    print("❓ Comando não reconhecido.")

                print("-" * 60)
                print("🎙️ Modo de Espera. Diga 'ativar'.")
                stt.set_vocabulario([WAKE_WORD])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Assistente encerrado pelo usuário.")
    except RuntimeError as e:
        print(f"❌ {e}")