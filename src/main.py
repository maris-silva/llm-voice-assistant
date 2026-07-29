from gpiozero import LED
from stt import SpeechToText

WAKE_WORD = "ativar"

led = LED(17)  # ajuste o pino GPIO conforme sua ligação


def acender_luz():
    led.on()
    print("💡 Executando: Ligando as luzes do quarto...")


def apagar_luz():
    led.off()
    print("🌑 Executando: Desligando as luzes do quarto...")


def mostrar_horas():
    from datetime import datetime
    print(f"⏰ Agora são: {datetime.now().strftime('%H:%M')}")


def cancelar():
    print("😴 Executando: Cancelado.")


# comando -> (frases-gatilho, função a executar)
COMANDOS = {
    "acender_luz": (["ligar a luz", "acender", "acender a luz", "luz"], acender_luz),
    "apagar_luz":  (["apagar a luz", "desligar a luz"], apagar_luz),
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
                modo_comando = False
                stt.set_vocabulario([WAKE_WORD])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Assistente encerrado pelo usuário.")
    except RuntimeError as e:
        print(f"❌ {e}")