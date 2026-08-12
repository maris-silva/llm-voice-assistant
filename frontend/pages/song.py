import os
import customtkinter as ctk
from PIL import Image
from mutagen.mp3 import MP3
from frontend.constants import COLOR_2, FONT_FAMILY
from frontend.pages.homepage import HomePage


class SongPage(HomePage):
    def __init__(self, master):
        super().__init__(master, bg_color=COLOR_2)

        self.song_name = None
        self.song_duration = 0
        self.elapsed_seconds = 0
        self.is_playing = False
        self.is_liked = False
        self.timer_id = None

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lbl_cover = ctk.CTkLabel(self, text="")
        self.lbl_cover.grid(row=0, column=0, pady=(15, 5))

        self.info_frame = ctk.CTkFrame(self, fg_color="transparent", width=380)
        self.info_frame.grid(row=1, column=0)
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.info_frame,
            text="Nome da Música",
            font=(FONT_FAMILY, 16, "bold"),
            text_color="#1da374",
            anchor="w",
        )
        self.lbl_title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        self.btn_like = ctk.CTkButton(
            self.info_frame,
            text="♡",
            font=(FONT_FAMILY, 22),
            text_color="#1da374",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color="#8ecfb8",
            corner_radius=16,
            command=self.toggle_like,
        )
        self.btn_like.grid(row=0, column=1, sticky="e")

        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent", width=380)
        self.progress_frame.grid(row=2, column=0)
        self.progress_frame.grid_columnconfigure((0, 1), weight=1)

        self.slider_progress = ctk.CTkProgressBar(
            self.progress_frame,
            progress_color="#1da374",
            fg_color="#8ecfb8",
            height=6,
            width=380,
        )
        self.slider_progress.set(0)
        self.slider_progress.grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5)
        )

        self.lbl_time_current = ctk.CTkLabel(
            self.progress_frame,
            text="0:00",
            font=(FONT_FAMILY, 10),
            text_color="#1da374",
        )
        self.lbl_time_current.grid(row=1, column=0, sticky="w")

        self.lbl_time_total = ctk.CTkLabel(
            self.progress_frame,
            text="0:00",
            font=(FONT_FAMILY, 10),
            text_color="#1da374",
        )
        self.lbl_time_total.grid(row=1, column=1, sticky="e")

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Estado: executando",
            font=(FONT_FAMILY, 11, "italic"),
            text_color="#1da374",
        )
        self.lbl_status.grid(row=3, column=0, pady=(0, 10), sticky="s")

    def on_show(self, song_name="good4u"):
        self.song_name = song_name
        self.lbl_title.configure(text=song_name.capitalize())

        self.is_liked = False
        self.btn_like.configure(text="♡", text_color="#1da374")

        self.elapsed_seconds = 0
        self.slider_progress.set(0)
        self.lbl_time_current.configure(text="0:00")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        cover_path = os.path.join(base_dir, "..", "assets", f"{song_name}.png")
        audio_path = os.path.join(base_dir, "..", "songs", f"{song_name}.mp3")

        if os.path.exists(cover_path):
            pil_img = Image.open(cover_path)
            ctk_img = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(160, 160)
            )
            self.lbl_cover.configure(image=ctk_img, text="")
        else:
            self.lbl_cover.configure(
                text="🎵 [Sem Capa]",
                font=(FONT_FAMILY, 24),
                text_color="#1da374",
            )

        if os.path.exists(audio_path):
            try:
                audio = MP3(audio_path)
                self.song_duration = int(audio.info.length)
            except Exception:
                self.song_duration = 180
        else:
            self.song_duration = 180

        self.lbl_time_total.configure(text=self.format_time(self.song_duration))

        self.is_playing = True
        self.update_progress_tick()

    def on_hide(self):
        self.is_playing = False
        if self.timer_id:
            self.after_cancel(self.timer_id)

    def update_progress_tick(self):
        if not self.is_playing:
            return

        if self.elapsed_seconds <= self.song_duration:
            progress_ratio = self.elapsed_seconds / max(1, self.song_duration)
            self.slider_progress.set(progress_ratio)
            self.lbl_time_current.configure(text=self.format_time(self.elapsed_seconds))

            self.elapsed_seconds += 1
            self.timer_id = self.after(1000, self.update_progress_tick)
        else:
            self.slider_progress.set(1.0)
            self.lbl_time_current.configure(text=self.format_time(self.song_duration))
            self.is_playing = False

    def toggle_like(self):
        self.is_liked = not self.is_liked

        if self.is_liked:
            self.btn_like.configure(text="♥", text_color="#1da374")
        else:
            self.btn_like.configure(text="♡", text_color="#1da374")

    @staticmethod
    def format_time(seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"
