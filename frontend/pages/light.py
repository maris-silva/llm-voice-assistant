import os
from PIL import Image
import customtkinter as ctk
from frontend.constants import FONT_FAMILY
from frontend.pages.homepage import HomePage


class LightPage(HomePage):
    def __init__(self, master):
        super().__init__(master, bg_color="#02fcf3")

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "..", "assets")
        image_path = os.path.join(assets_dir, "lampada.png")

        try:
            pil_image = Image.open(image_path)
            self.lamp_image = ctk.CTkImage(
                light_image=pil_image, dark_image=pil_image, size=(80, 80)
            )
            self.lbl_icon = ctk.CTkLabel(self, text="", image=self.lamp_image)
        except Exception:
            self.lbl_icon = ctk.CTkLabel(
                self, text="💡", font=(FONT_FAMILY, 50), text_color="#00918c"
            )

        self.lbl_icon.grid(row=0, column=0, sticky="s")

        self.lbl_title = ctk.CTkLabel(
            self,
            text="Luz ligada!",
            font=(FONT_FAMILY, 24, "bold"),
            text_color="#00918c",
        )
        self.lbl_title.grid(row=1, column=0)

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Estado: executando",
            font=(FONT_FAMILY, 12, "italic"),
            text_color="#00918c",
        )
        self.lbl_status.grid(row=2, column=0, sticky="n")
