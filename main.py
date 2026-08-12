import sys
import signal
from frontend.app import App
from backend.assistant_engine import AssistantEngine

if __name__ == "__main__":
    app = App()
    engine = AssistantEngine(app)

    def on_closing():
        """Sintetiza e executa a limpeza final dos recursos"""
        print("\n[SYSTEM] Encerrando o aplicativo e limpando processos...")
        engine.stop()
        app.destroy()
        sys.exit(0)

    # Captura interrupção do terminal (Ctrl + C)
    signal.signal(signal.SIGINT, lambda sig, frame: on_closing())
    signal.signal(signal.SIGTERM, lambda sig, frame: on_closing())

    # Captura o fecho do Tkinter pelo botão 'X' da janela
    app.protocol("WM_DELETE_WINDOW", on_closing)

    engine.start()
    app.mainloop()
