import math
import os
from PIL import Image
import customtkinter as ctk
from frontend.constants import COLOR_5, FONT_FAMILY
from frontend.pages.homepage import HomePage


class IdlePage(HomePage):
    def __init__(self, master):
        super().__init__(master, bg_color=COLOR_5)
        self.state = "IDLE"
        self.anim_step = 0
        self.is_animating = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=0, sticky="nsew")
        self.center_frame.grid_rowconfigure(0, weight=1)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "..", "assets")
        image_path = os.path.join(assets_dir, "z.png")

        try:
            pil_image = Image.open(image_path)
            self.z_image = ctk.CTkImage(
                light_image=pil_image, dark_image=pil_image, size=(100, 100)
            )
            self.lbl_sleep = ctk.CTkLabel(
                self.center_frame, text="", image=self.z_image
            )
        except Exception:
            self.lbl_sleep = ctk.CTkLabel(
                self.center_frame,
                text="Z z z",
                font=(FONT_FAMILY, 38, "bold"),
                text_color="#737373",
            )

        self.bars_container = ctk.CTkFrame(self.center_frame, fg_color="transparent")

        self.bars = []
        for i in range(5):
            bar = ctk.CTkFrame(
                self.bars_container,
                fg_color="#737373",
                width=18,
                height=20,
                corner_radius=14,
            )
            self.bars.append(bar)

        self.lbl_status = ctk.CTkLabel(
            self, text="Estado: idle", font=(FONT_FAMILY, 14), text_color="#525252"
        )
        self.lbl_status.grid(row=1, column=0, pady=(0, 20), sticky="s")

        self.set_state("IDLE")

    def set_state(self, new_state: str):
        self.state = new_state
        self.lbl_status.configure(text=f"Estado: {new_state.lower()}")

        if self.state == "OUVINDO":
            self.lbl_sleep.pack_forget()
            self.bars_container.pack(expand=True)
            for i, bar in enumerate(self.bars):
                bar.pack(side="left", padx=2, expand=True)

            if not self.is_animating:
                self.is_animating = True
                self.animate_bars()
        else:
            self.is_animating = False
            self.bars_container.pack_forget()
            for bar in self.bars:
                bar.pack_forget()
            self.lbl_sleep.pack(expand=True)

    def animate_bars(self):
        """Simula a equalização do microfone com onda senoidal"""
        if not self.is_animating:
            return

        self.anim_step += 0.2
        for i, bar in enumerate(self.bars):
            h = int(20 + 30 * math.sin(self.anim_step + i * 0.8))
            bar.configure(height=max(12, abs(h)))

        self.after(50, self.animate_bars)
