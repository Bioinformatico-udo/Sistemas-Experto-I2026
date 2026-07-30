import customtkinter as ctk
from ..styles import *

class CaracteristicasPage:
    def __init__(self, parent_frame, main_app):
        self.parent_frame = parent_frame
        self.main_app = main_app
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_BACKGROUND_MAIN, corner_radius=15)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        # Encabezado
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(
            header, 
            text="Características y Funcionalidades",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=COLOR_PRIMARY_LIGHT
        ).pack(anchor="w")

        # Descripción general
        desc = (
            "Sistema experto diseñado para la identificación taxonómica precisa "
            "de Crustáceos Anomuros de la Familia Porcellanidae mediante claves dicotómicas precisas."
        )
        ctk.CTkLabel(
            self.frame, 
            text=desc, 
            font=ctk.CTkFont(family="Segoe UI", size=14), 
            text_color=COLOR_TEXT_SECONDARY,
            wraplength=800, 
            justify="left"
        ).pack(padx=30, pady=(0, 20), anchor="w")

        # Lista  de tarjetas
        features = [
            ( 
                "Identificación Taxonómica Guiada", 
                "Diagnóstico paso a paso basado en rasgos morfológicos clave, determinando la especie con un grado de certeza."
            ),
            ( 
                "Catálogo Morfológico (23 Especies)", 
                "Acceda a fichas detalladas con imágenes de alta calidad, descripcion anatómica e informacion de la distribución geográfica."
            ),
            (
                "Resultados y Reportes Exportables", 
                "Visualice la información de forma clara, con la opción de exportar fichas técnicas completas en formato PNG."
            ),
            ( 
                "Verificador de Certeza", 
                "Valide la probabilidad de coincidencia del ejemplar en estudio mediante un motor de verificación."
            ),
            (
                "Glosario de Términos", 
                "Consulte definiciones anatómicas y taxonómicas especializadas para agilizar la interpretación de la clave."
            ),
            (
                "Gestión del Conocimiento", 
                "Módulo administrativo de acceso restringido para incorporar y enriquecer la base de datos de especies."
            )
        ]

        container = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=10)

        # Generación dinámica de tarjetas
        for tit, descr in features:
            card = ctk.CTkFrame(
                container, 
                fg_color=COLOR_CARD_BACKGROUND, 
                corner_radius=12
            )
            card.pack(fill="x", pady=8, padx=5)

            # Título de la tarjeta
            ctk.CTkLabel(
                card, 
                text=f"{tit}", 
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color=COLOR_PRIMARY_LIGHT
            ).pack(anchor="w", padx=15, pady=(12, 4))

            # Descripción dentro de la tarjeta
            ctk.CTkLabel(
                card, 
                text=descr, 
                font=ctk.CTkFont(family="Segoe UI", size=13), 
                text_color=COLOR_TEXT_SECONDARY,
                wraplength=720, 
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 12))

    def get_frame(self):
        return self.frame