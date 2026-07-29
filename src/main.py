from stt import SpeechToText
from gpiozero import LED
WAKE_WORD = "ativar"

COMANDOS = {
    "acender_luz": (["ligar a luz", "acender", "acender a luz", "luz"],
                     "💡 Executando: Ligando as luzes do quarto..."),
    "horas":       (["horas", "que horas"],
                     "⏰ Executando: Buscando o horário atual do sistema..."),
    "cancelar":    (["desligar", "cancelar"],
                     "😴 Executando: Cancelado."),
}

VOCAB_COMANDOS = [frase for gatilhos, _ in COMANDOS.values() for frase in gatilhos]

led = LED(17)
def identificar_comando(texto):
    for nome, (gatilhos, msg) in COMANDOS.items():
        for gatilho in gatilhos:
            if gatilho in texto:
                return nome, msg
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
                _, msg = identificar_comando(texto)
                if _ == "acender_luz":
                    LED.on()
                    
                print(msg if msg else "❓ Comando não reconhecido.")

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