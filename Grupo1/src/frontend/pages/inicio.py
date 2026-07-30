import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import importlib
from PIL import Image

# Importar constantes y rutas desde styles.py
from ..styles import (
    COLOR_BACKGROUND_MAIN, COLOR_CARD_BACKGROUND, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_PRIMARY_DARK, COLOR_PRIMARY_LIGHT, COLOR_BUTTON_HOVER,
    ASSETS_DIR, ICON_IDENTIFICADOR, IMAGE_PRINCIPAL_FILENAME,
    ICON_VERIFICADOR
)

class InicioPage:
    def __init__(self, parent_frame, main_app):
        self.parent_frame = parent_frame
        self.main_app = main_app
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_BACKGROUND_MAIN, corner_radius=15)
        self.frame.grid_columnconfigure(0, weight=1) 
        self.frame.grid_rowconfigure(0, weight=1) 
        self.frame.grid_rowconfigure(1, weight=4) 
        self.frame.grid_rowconfigure(2, weight=0) 
        self.frame.grid_rowconfigure(3, weight=0) 
        self.frame.grid_rowconfigure(4, weight=0) 
        self.frame.grid_rowconfigure(5, weight=0) 
        self.frame.grid_rowconfigure(6, weight=1) 
        self._create_widgets()

    def _create_widgets(self):
        """Crea los widgets de la página de inicio."""
        # Título
        title_label = ctk.CTkLabel(self.frame, text="Bienvenido al Sistema Experto de Identificación de Crustáceos Anomuros de la Familia Porcellanidae",
                                  font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color=COLOR_TEXT_PRIMARY,
                                  justify="right", pady=10)
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        # Contenedor para la imagen principal
        image_container_frame = ctk.CTkFrame(self.frame, fg_color=COLOR_CARD_BACKGROUND, corner_radius=15)
        image_container_frame.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")
        image_container_frame.grid_columnconfigure(0, weight=1)
        image_container_frame.grid_rowconfigure(0, weight=1)

        # Cargar y mostrar la imagen principal
        main_image_path = os.path.join(ASSETS_DIR, IMAGE_PRINCIPAL_FILENAME)
        if os.path.exists(main_image_path):
            try:
                with Image.open(main_image_path) as img:
                    img_width, img_height = img.size

                # Calcular dimensiones para que la imagen se ajuste al contenedor
                container_width = 800
                container_height = 400

                aspect_ratio = img_height / img_width
                new_width = container_width
                new_height = int(new_width * aspect_ratio)

                if new_height > container_height:
                    new_height = container_height
                    new_width = int(new_height / aspect_ratio)

                main_image = self.main_app.load_image(IMAGE_PRINCIPAL_FILENAME, directory=ASSETS_DIR, size=(new_width, new_height))
                image_label = ctk.CTkLabel(image_container_frame, image=main_image, text="")
                image_label.grid(row=0, column=0,
                                 pady=(container_height - new_height) // 2,
                                 padx=(container_width - new_width) // 2,
                                 sticky="nsew")
            except Exception as e:
                print(f"Error al procesar la imagen principal '{IMAGE_PRINCIPAL_FILENAME}': {e}")
                image_placeholder_label = ctk.CTkLabel(image_container_frame, text="[ ERROR AL CARGAR IMAGEN ]",
                                                      font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                                                      text_color=COLOR_TEXT_SECONDARY)
                image_placeholder_label.grid(row=0, column=0, sticky="nsew")
        else:
            # Placeholder si la imagen no existe
            image_placeholder_label = ctk.CTkLabel(image_container_frame, text="[ REEMPLAZAR CON TU IMAGEN ]",
                                                  font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                                                  text_color=COLOR_TEXT_SECONDARY)
            image_placeholder_label.grid(row=0, column=0, sticky="nsew")

        # Descripción general
        description_text = (
            "Utilice este sistema para identificar y verificar especies de la familia Porcellanidae. Explore las secciones para obtener más información,"
            " aprenda a usar la herramienta y consulte el glosario técnico. Estamos dedicados a la investigación marina."
        )
        description_label = ctk.CTkLabel(self.frame, text=description_text, font=ctk.CTkFont(family="Segoe UI", size=14),
                                        text_color=COLOR_TEXT_SECONDARY, wraplength=800, justify="center")
        description_label.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="s")

        action_buttons_frame = ctk.CTkFrame(self.frame, fg_color=COLOR_BACKGROUND_MAIN)
        action_buttons_frame.grid(row=5, column=0, padx=20, pady=(0, 30), sticky="s")
        action_buttons_frame.grid_columnconfigure(0, weight=1) 
        action_buttons_frame.grid_columnconfigure(1, weight=1) 

        # Botón para verificar especie
        verificador_button_icon = self.main_app.load_image(ICON_VERIFICADOR, size=(40, 40))
        verificador_button = ctk.CTkButton(
            action_buttons_frame,
            text="INICIAR VERIFICACIÓN DE ESPECIE",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            fg_color=COLOR_PRIMARY_DARK,
            hover_color=COLOR_BUTTON_HOVER,
            corner_radius=40,
            image=verificador_button_icon,
            compound="left",
            command=self.main_app.abrir_verificador,
            border_width=0
        )

        verificador_button.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="nsew") 

        # Botón para abrir el identificador  
        start_button_icon = self.main_app.load_image(ICON_IDENTIFICADOR, size=(40, 40))
        start_button = ctk.CTkButton(
            action_buttons_frame,
            text="COMENZAR IDENTIFICACIÓN DE ESPECIE",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            fg_color=COLOR_PRIMARY_DARK,
            hover_color=COLOR_BUTTON_HOVER,
            corner_radius=40,
            image=start_button_icon,
            compound="left",
            command=self.main_app.abrir_identificador, 
            border_width=0
        )
        start_button.grid(row=0, column=1, padx=(15, 0), pady=10, sticky="nsew") 

    def get_frame(self):
        """Retorna el frame principal de esta página."""
        return self.frame
