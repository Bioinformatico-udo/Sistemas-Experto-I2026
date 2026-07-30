import customtkinter as ctk
import unicodedata
from ..styles import *

HOVER_CARD = "#2A3B55"

def eliminar_acentos(texto):
    """Elimina los acentos de una cadena usando normalización Unicode."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

class GlosarioPage:
    def __init__(self, parent_frame, main_app):
        self.parent_frame = parent_frame
        self.main_app = main_app
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_BACKGROUND_MAIN, corner_radius=15)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        # Cabecera con buscador
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Glosario de Terminos",
                     font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
                     text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w")

        self.busqueda = ctk.CTkEntry(header, placeholder_text="Buscar término...", width=250,
                                     fg_color=COLOR_CARD_BACKGROUND, text_color=COLOR_TEXT_PRIMARY,
                                     border_color=COLOR_PRIMARY_LIGHT)
        self.busqueda.pack(side="right", padx=10)
        self.busqueda.bind("<KeyRelease>", self.filtrar)

        # Contenedor de términos
        self.scroll = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)
        self.scroll.bind("<Button-1>", lambda e: self.frame.focus_set())

        # Datos del glosario
        self.glosario_data = [
            ("Caparazón", "Parte dorsal del exoesqueleto que cubre el cefalotórax. En los Porcellanidae, suele ser aplanado y más ancho que largo."),
            ("Quelípedos", "Primer par de pereiópodos modificados en pinzas; usados para alimentación y defensa."),
            ("Anténulas", "Primer par de antenas, cortas, con función sensorial."),
            ("Antenas", "Segundo par de apéndices cefálicos, con función sensorial y a veces defensiva."),
            ("Pleópodos", "Apéndices abdominales; en hembras sirven para portar huevos."),
            ("Telson", "Placa terminal del abdomen; puede tener 5 o 7 piezas en esta familia."),
            ("Anomuro", "Infraorden de decápodos que incluye cangrejos ermitaños y porcelánidos."),
            ("Cefalotórax", "Fusión de cabeza y tórax."),
            ("Abdomen", "Parte posterior del cuerpo, plegada bajo el cefalotórax en Porcellanidae."),
            ("Isquion", "Tercer artejo de un apéndice; segmento basal."),
            ("Mero", "Cuarto artejo de un apéndice; situado entre isquion y carpo."),
            ("Carpo", "Quinto artejo; su margen flexor puede presentar dientes o ser liso."),
            ("Propodo", "Sexto artejo; forma la palma de los quelípedos."),
            ("Dactilo", "Séptimo artejo; dedo móvil de la pinza."),
            ("Flagelo", "Parte distal multiarticulada de las antenas."),
            ("Espina epibranquial", "Pequeña espina en la región branquial del caparazón."),
            ("Paredes laterales", "Estructuras laterales del caparazón; pueden ser completas o incompletas."),
            ("Frente", "Parte anterior del caparazón; puede ser trilobulada, recta, etc."),
            ("Tubérculo", "Protuberancia elevada en la superficie del exoesqueleto."),
            ("Gránulo", "Pequeña elevación redondeada, menor que un tubérculo.")
        ]
        self.mostrar_terminos("")

    def mostrar_terminos(self, filtro):
        # Limpiar contenedor
        for w in self.scroll.winfo_children():
            w.destroy()

        filtro_normalizado = eliminar_acentos(filtro).lower()

        for term, defin in self.glosario_data:
            term_normalizado = eliminar_acentos(term).lower()
            # Si no hay filtro, mostrar todo; si hay, que contenga el texto (sin acentos)
            if not filtro_normalizado or filtro_normalizado in term_normalizado:
                card = ctk.CTkFrame(self.scroll, fg_color=COLOR_CARD_BACKGROUND, corner_radius=10)
                card.pack(fill="x", pady=4, padx=5)
                ctk.CTkLabel(card, text=term, font=ctk.CTkFont(size=15, weight="bold"),
                             text_color=COLOR_PRIMARY_LIGHT).pack(anchor="w", padx=15, pady=(8, 0))
                ctk.CTkLabel(card, text=defin, font=ctk.CTkFont(size=13),
                             text_color=COLOR_TEXT_SECONDARY, wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(3, 8))

                # Hover
                def on_enter(e, c=card):
                    c.configure(fg_color=HOVER_CARD)
                def on_leave(e, c=card):
                    c.configure(fg_color=COLOR_CARD_BACKGROUND)

                card.bind("<Enter>", on_enter)
                card.bind("<Leave>", on_leave)

    def filtrar(self, event=None):
        texto = self.busqueda.get()
        self.mostrar_terminos(texto)

    def get_frame(self):
        return self.frame