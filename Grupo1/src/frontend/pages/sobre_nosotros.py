import webbrowser
import customtkinter as ctk
from ..styles import *

HOVER_CARD = "#2A3B55"

class SobreNosotrosPage:
    def __init__(self, parent_frame, main_app):
        self.parent_frame = parent_frame
        self.main_app = main_app
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_BACKGROUND_MAIN, corner_radius=15)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        # Cabecera
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 5))
        ctk.CTkLabel(header, text="Sobre Nosotros",
                     font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w")
        ctk.CTkLabel(header, text="Conozca al equipo detrás del sistema y la base científica",
                     font=ctk.CTkFont(size=14), text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(5, 0))

        scroll = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=10)

        # --- Equipo de Desarrollo ---
        ctk.CTkLabel(scroll, text="Desarrolladores", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w", pady=(20, 20))

        devs = [
            ("Alexander Urbina", "Desarrollador Full-Stack", "https://portafolio-alexander.netlify.app"),
            ("Allenairam Rojas", "Diseñadora IU/UX e Investigadora Principal del Proyecto", "https://allenairam-rojas.vercel.app/"),
            ("Luisana Rodríguez", "Desarrolladora Full-Stack", "https://portafolio-luisana.netlify.app")
        ]
        self._crear_tarjetas_equipo(scroll, devs)

        # --- Expertos en el area ---
        ctk.CTkLabel(scroll, text="Expertos en Biología Marina y Carcinología", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w", pady=(20, 20))

        expertos = [
            ("Lic. Jose Morillo", "Especialista en Informática y Biología Marina", None),
            ("MSc. Carlos Lira", "Experto en Carcinología. Autor del estudio “Crustáceos anomuros costeros de la Península de Macanao, Isla de Margarita, Venezuela” (1997)", None)
        ]
        self._crear_tarjetas_equipo(scroll, expertos)

        # --- Misión ---
        ctk.CTkLabel(scroll, text="Nuestra Misión", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(scroll, text="Facilitar la identificación taxonómica de los Crustaceos Anomuros de la Familia Porcellanidae para impulsar el aprendizaje, la ciencia ciudadana y la conservación marina ",
                     font=ctk.CTkFont(size=13), text_color=COLOR_TEXT_SECONDARY, wraplength=700, justify="left").pack(anchor="w", padx=10)

    def _crear_tarjetas_equipo(self, parent, miembros):
        fila = ctk.CTkFrame(parent, fg_color="transparent")
        fila.pack(fill="x", pady=10)
        fila.grid_columnconfigure((0, 1, 2), weight=1)

        for idx, item in enumerate(miembros):
            nombre = item[0]
            rol = item[1]
            url = item[2] if len(item) > 2 else None

            card = ctk.CTkFrame(fila, fg_color=COLOR_CARD_BACKGROUND, corner_radius=12)
            card.grid(row=0, column=idx, padx=8, sticky="nsew")
            card.grid_rowconfigure(0, weight=1)

            iniciales = "".join([n[0] for n in nombre.split()]).upper()
            avatar = ctk.CTkFrame(card, width=55, height=55, fg_color=COLOR_PRIMARY_LIGHT, corner_radius=27)
            avatar.pack(pady=(15, 5))
            avatar.pack_propagate(False)
            ctk.CTkLabel(avatar, text=iniciales, font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=COLOR_TEXT_PRIMARY).pack(expand=True)

            ctk.CTkLabel(card, text=nombre, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLOR_TEXT_PRIMARY).pack()
   
            ctk.CTkLabel(card, text=rol, font=ctk.CTkFont(size=12),
                         text_color=COLOR_TEXT_SECONDARY, wraplength=180).pack(pady=(0, 10))

            if url:
                card.configure(cursor="hand2")

                def on_enter(e, c=card):
                    c.configure(fg_color=HOVER_CARD)

                def on_leave(e, c=card):
                    c.configure(fg_color=COLOR_CARD_BACKGROUND)

                def open_link(e, target_url=url):
                    webbrowser.open_new_tab(target_url)

                def bind_events_recursive(widget):
                    widget.configure(cursor="hand2")
                    widget.bind("<Enter>", on_enter)
                    widget.bind("<Leave>", on_leave)
                    widget.bind("<Button-1>", open_link)
                    for child in widget.winfo_children():
                        bind_events_recursive(child)

                bind_events_recursive(card)

    def get_frame(self):
        return self.frame