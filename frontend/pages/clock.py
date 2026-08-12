from datetime import datetime
import customtkinter as ctk
from frontend.constants import COLOR_3, FONT_FAMILY
from frontend.pages.homepage import HomePage


class ClockPage(HomePage):
    def __init__(self, master):
        super().__init__(master, bg_color=COLOR_3)

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self, text="Agora são...", font=(FONT_FAMILY, 18), text_color="#262626"
        )
        self.lbl_title.grid(row=0, column=0, sticky="s", pady=10)

        self.lbl_time = ctk.CTkLabel(
            self, text="00:00", font=(FONT_FAMILY, 48, "bold"), text_color="#000000"
        )
        self.lbl_time.grid(row=1, column=0)

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Estado: executando",
            font=(FONT_FAMILY, 12, "italic"),
            text_color="#525252",
        )
        self.lbl_status.grid(row=2, column=0, sticky="n")

    def on_show(self, data=None):
        horario_atual = datetime.now().strftime("%H:%M")
        self.lbl_time.configure(text=horario_atual)
