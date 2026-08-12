import customtkinter as ctk
from frontend.constants import COLOR_5, FONT_FAMILY
from frontend.pages.clock import ClockPage
from frontend.pages.idle import IdlePage
from frontend.pages.light import LightPage
from frontend.pages.song import SongPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LLM Voice Assistant")
        self.geometry("650x650")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.view_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.view_container.grid(row=0, column=0, sticky="nsew")
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)

        self.views = {}
        self.active_view_key = None
        self.auto_return_timer = None

        self.register_view("idle", IdlePage(self.view_container))
        self.register_view("clock", ClockPage(self.view_container))
        self.register_view("light", LightPage(self.view_container))
        self.register_view("song", SongPage(self.view_container))

        self.footer = ctk.CTkFrame(self, height=35, fg_color="#171717", corner_radius=0)
        self.footer.grid(row=1, column=0, sticky="ew")

        self.switch_debug = ctk.CTkSwitch(
            self.footer,
            text="MODO DEBUG",
            font=(FONT_FAMILY, 10, "bold"),
            text_color="#ffffff",
            command=self.toggle_debug,
        )
        self.switch_debug.pack(side="left", padx=10, pady=5)

        self.debug_frame = ctk.CTkFrame(
            self, height=100, fg_color="#0d0d0d", corner_radius=0
        )

        self.log_textbox = ctk.CTkTextbox(
            self.debug_frame,
            font=("Consolas", 10),
            text_color="#02fcf3",
            fg_color="#0d0d0d",
            corner_radius=0,
        )
        self.log_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_textbox.insert("end", "[SYSTEM] Terminal de Debug carregado...\n")

        # Garante a exibição inicial na tela 'idle' no estado inativo (IDLE)
        self.set_assistant_state("IDLE")
        self.show_view("idle")

    def register_view(self, key: str, view_widget):
        self.views[key] = view_widget
        view_widget.grid(row=0, column=0, sticky="nsew")

    def set_assistant_state(self, state: str):
        """
        Altera o estado visual na página Idle ('IDLE' para inativo / 'OUVINDO' para modo ativo)
        """
        if "idle" in self.views and hasattr(self.views["idle"], "set_state"):
            self.views["idle"].set_state(state)

    def show_view(self, key: str, data=None, auto_return_seconds=None):
        if key not in self.views:
            return

        # Se a mesma view já estiver na tela, atualizamos apenas o estado/dados sem reexecutar a animação
        if key == self.active_view_key:
            self.views[key].on_show(data)
            return

        if self.auto_return_timer:
            self.after_cancel(self.auto_return_timer)
            self.auto_return_timer = None

        if key == "song" and not data:
            data = "good4u"

        target_view = self.views[key]

        def fade_step(alpha):
            self.attributes("-alpha", alpha)
            if alpha > 0.4:
                self.after(15, lambda: fade_step(alpha - 0.1))
            else:
                if self.active_view_key:
                    self.views[self.active_view_key].on_hide()

                target_view.tkraise()
                target_view.on_show(data)
                self.active_view_key = key
                fade_in_step(0.4)

        def fade_in_step(alpha):
            self.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.after(15, lambda: fade_in_step(alpha + 0.1))

        fade_step(1.0)

        if auto_return_seconds:
            self.auto_return_timer = self.after(
                int(auto_return_seconds * 1000), lambda: self.show_view("idle")
            )

    def toggle_debug(self):
        if self.switch_debug.get() == 1:
            self.debug_frame.grid(row=2, column=0, sticky="ew")
        else:
            self.debug_frame.grid_forget()
            self.geometry("650x650")

    def log_debug(self, message: str):
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.see("end")
