from stt import SpeechToText

def main():
    with SpeechToText() as stt:
        print("🎙️ Ouvindo... fale algo (Ctrl+C para sair)")
        print("-" * 60)
        for texto in stt.escutar(mostrar_parcial=True):
            print(f"📝 {texto}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Encerrado pelo usuário.")
    except RuntimeError as e:
        print(f"❌ {e}")