# gui/utilidades.py
import os
from PIL import Image
import customtkinter as ctk


class CacheImagenes:
    """Gestor de caché de imágenes para evitar recargas desde disco."""

    def __init__(self, ruta_assets):
        self.ruta_assets = ruta_assets
        self.cache = {}

    def obtener(self, nombre_archivo, tamaño):
        """
        Devuelve un objeto CTkImage desde caché o lo carga del disco.
        tamaño: tupla (ancho, alto) en píxeles.
        """
        clave = f"{nombre_archivo}_{tamaño[0]}_{tamaño[1]}"
        if clave in self.cache:
            return self.cache[clave]

        ruta = os.path.join(self.ruta_assets, nombre_archivo)
        if os.path.exists(ruta):
            img_pil = Image.open(ruta)
            # Redimensionar con thumbnail para ahorrar memoria
            img_pil.thumbnail((tamaño[0] * 2, tamaño[1] * 2))
            img_ctk = ctk.CTkImage(
                light_image=img_pil,
                dark_image=img_pil,
                size=tamaño
            )
            self.cache[clave] = img_ctk
            return img_ctk

        self.cache[clave] = None
        return None
