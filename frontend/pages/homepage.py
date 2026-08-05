import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    """Interface para criar facilmente novas telas de ação"""

    def __init__(self, master, bg_color, **kwargs):
        super().__init__(master, fg_color=bg_color, corner_radius=0, **kwargs)

    def on_show(self, data=None):
        """Método executado automaticamente quando a tela é exibida"""
        pass

    def on_hide(self):
        """Método executado automaticamente quando a tela sai de cena"""
        pass
