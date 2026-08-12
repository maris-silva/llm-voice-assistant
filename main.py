from frontend.app import App
from backend.assistant_engine import AssistantEngine

if __name__ == "__main__":
    app = App()

    engine = AssistantEngine(app)
    engine.start()

    app.mainloop()
