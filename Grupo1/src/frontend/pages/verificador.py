import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
ASSETS_DIR = os.path.join(BASE_DIR, "frontend", "assets")
IMAGENES_DIR = os.path.join(ASSETS_DIR, "imagenes_especies")

if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)
try:
    from base_conocimiento import CARACTERISTICAS_ESPECIES
except ImportError as e:
    print(f"Error al importar desde backend: {e}")
    CARACTERISTICAS_ESPECIES = {}

COLOR_PRIMARY = "#0D9488"
COLOR_PRIMARY_HOVER = "#0F766E"
COLOR_SECONDARY = "#1E3A8A"
COLOR_SECONDARY_HOVER = "#B91C1C"
COLOR_SUCCESS = "#22C55E"
COLOR_ERROR = "#DC2626"
COLOR_WARNING = "#F59E0B"
COLOR_BACKGROUND = "#0F172A"
COLOR_CARD = "#1E293B"
COLOR_BORDER = "#334155"

class AppVerificador:
    def __init__(self, parent_window, main_app=None):
        self.parent = parent_window
        self.main_app = main_app
        self.parent.configure(fg_color=COLOR_BACKGROUND)
        self.cargar_especies_personalizadas()
        self.custom_images = self.cargar_imagenes_personalizadas()
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        self.iniciar_verificacion()

    def cargar_especies_personalizadas(self):
        json_path = os.path.join(BASE_DIR, "especies_personalizadas.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    if not contenido:
                        return
                    especies = json.loads(contenido)
                for sp in especies:
                    CARACTERISTICAS_ESPECIES[sp["nombre"]] = sp["caracteristicas"]
            except json.JSONDecodeError as e:
                print(f"Error de JSON en especies personalizadas: {e}")
            except Exception as e:
                print("Error cargando especies personalizadas:", e)

    def cargar_imagenes_personalizadas(self):
        json_path = os.path.join(BASE_DIR, "especies_personalizadas.json")
        mapping = {}
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    if not contenido:
                        return mapping
                    especies = json.loads(contenido)
                for sp in especies:
                    mapping[sp["nombre"]] = sp.get("imagen", "placeholder.jpg")
            except json.JSONDecodeError as e:
                print(f"Error de JSON en imágenes personalizadas: {e}")
            except Exception as e:
                print("Error cargando imágenes personalizadas:", e)
        return mapping

    def obtener_ruta_imagen(self, especie):
        if especie in self.custom_images:
            nombre_img = self.custom_images[especie]
        else:
            safe_name = "".join(c for c in especie if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower() + '.jpg'
            nombre_img = safe_name
        ruta = os.path.join(IMAGENES_DIR, nombre_img)
        if os.path.exists(ruta):
            return ruta
        return None

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def cerrar_ventana(self):
        self.parent.destroy()

    def iniciar_verificacion(self):
        self.limpiar_frame()
        especies = list(CARACTERISTICAS_ESPECIES.keys())

        frame_central = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_central.pack(expand=True)

        ctk.CTkLabel(
            frame_central,
            text="VERIFICAR ESPECIE",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#F3F4F6"
        ).pack(pady=(0, 30))

        ctk.CTkLabel(
            frame_central,
            text="Seleccione la especie que desea verificar:",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color="#F3F4F6"
        ).pack(pady=20)

        combo = ctk.CTkComboBox(
            frame_central,
            values=especies,
            width=400,
            height=45,
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        combo.pack(pady=10)

        info_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_CARD, corner_radius=15)
        info_frame.pack(pady=10, padx=20, fill="both", expand=True)
        info_frame.grid_columnconfigure(0, weight=2)
        info_frame.grid_columnconfigure(1, weight=3)
        info_frame.grid_rowconfigure(0, weight=1)

        img_container = ctk.CTkFrame(info_frame, fg_color=COLOR_BORDER, corner_radius=12)
        img_container.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        img_container.grid_rowconfigure(0, weight=1)
        img_container.grid_columnconfigure(0, weight=1)

        img_label = ctk.CTkLabel(img_container, text="", fg_color="transparent")
        img_label.grid(row=0, column=0, sticky="nsew")

        caract_scroll = ctk.CTkScrollableFrame(info_frame, fg_color=COLOR_BACKGROUND, corner_radius=12)
        caract_scroll.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        texto_label = ctk.CTkLabel(
            caract_scroll, text="", justify="left",
            font=("Segoe UI", 12), text_color="#F3F4F6",
            wraplength=400
        )
        texto_label.pack(anchor="w", padx=15, pady=15)

        def actualizar_info(event=None):
            especie = combo.get()
            if especie in CARACTERISTICAS_ESPECIES:
                caracts = CARACTERISTICAS_ESPECIES[especie]
                texto = "\n".join(f"• {c}" for c in caracts)
                texto_label.configure(text=texto)
            else:
                texto_label.configure(text="")
            ruta_img = self.obtener_ruta_imagen(especie)
            if ruta_img:
                try:
                    pil_img = Image.open(ruta_img)
                    pil_img.thumbnail((250, 180))
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
                    img_label.configure(image=ctk_img, text="")
                except Exception as e:
                    img_label.configure(image=None, text="[Error al cargar imagen]", font=("Segoe UI", 10))
            else:
                img_label.configure(image=None, text="[Imagen no disponible]", font=("Segoe UI", 10))

        combo.configure(command=actualizar_info)
        if especies:
            combo.set(especies[0])
            actualizar_info()

        def verificar():
            esp = combo.get()
            if esp and esp in CARACTERISTICAS_ESPECIES:
                self.mostrar_formulario_verificacion(esp)
            else:
                messagebox.showwarning("Advertencia", "Seleccione una especie válida")

        btn_frame_inicio = ctk.CTkFrame(frame_central, fg_color="transparent")
        btn_frame_inicio.pack(pady=20)

        ctk.CTkButton(
            btn_frame_inicio,
            text="Verificar Especie",
            command=verificar,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=200,
            height=45,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame_inicio,
            text="Cerrar Verificador",
            command=self.cerrar_ventana,
            fg_color=COLOR_ERROR,
            hover_color="#B91C1C",
            width=200,
            height=45,
            font=ctk.CTkFont(family="Segoe UI", size=14)
        ).pack(side="left", padx=10)

    def mostrar_formulario_verificacion(self, especie):
        self.limpiar_frame()

        ctk.CTkLabel(
            self.main_frame,
            text=f"Verificando: {especie}",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#F3F4F6"
        ).pack(pady=20)

        caracteristicas = CARACTERISTICAS_ESPECIES[especie]
        respuestas = []

        frame_chars = ctk.CTkScrollableFrame(self.main_frame, fg_color=COLOR_CARD, corner_radius=15)
        frame_chars.pack(fill="both", expand=True, padx=40, pady=10)

        for car in caracteristicas:
            char_frame = ctk.CTkFrame(frame_chars, fg_color=COLOR_BACKGROUND, corner_radius=10)
            char_frame.pack(fill="x", padx=15, pady=8)

            ctk.CTkLabel(
                char_frame,
                text=car,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                wraplength=500,
                justify="left",
                text_color="#F3F4F6"
            ).pack(side="left", padx=15, pady=12, expand=True, fill="x")

            var = ctk.StringVar(value="no")
            respuestas.append(var)

            ctk.CTkRadioButton(
                char_frame,
                text="Sí",
                variable=var,
                value="si",
                fg_color=COLOR_SUCCESS,
                hover_color="#16A34A"
            ).pack(side="right", padx=5)

            ctk.CTkRadioButton(
                char_frame,
                text="No",
                variable=var,
                value="no",
                fg_color=COLOR_ERROR,
                hover_color="#B91C1C"
            ).pack(side="right", padx=15)

        def evaluar():
            coincidencias = sum(1 for v in respuestas if v.get() == "si")
            total = len(respuestas)
            if total > 0:
                porcentaje = (coincidencias / total) * 100
                self._mostrar_resultado_verificacion(porcentaje, coincidencias, total, especie)

        ctk.CTkButton(
            self.main_frame,
            text="Evaluar coincidencias",
            command=evaluar,
            fg_color=COLOR_WARNING,
            hover_color="#D97706",
            width=250,
            height=50,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        ).pack(pady=20)

    def _mostrar_resultado_verificacion(self, porcentaje, coincidencias, total, especie):
        self.limpiar_frame()

        resultado_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_CARD, corner_radius=20)
        resultado_frame.pack(fill="both", expand=True, padx=40, pady=40)

        if porcentaje >= 75:
            icono, color, mensaje = "", COLOR_SUCCESS, f"ALTA COINCIDENCIA ({porcentaje:.0f}%)"
            desc = "El espécimen coincide con la mayoría de las características."
        elif porcentaje >= 50:
            icono, color, mensaje = "⚠️", COLOR_WARNING, f"COINCIDENCIA PARCIAL ({porcentaje:.0f}%)"
            desc = "Comparte algunas características, pero no todas."
        else:
            icono, color, mensaje = "", COLOR_ERROR, f"BAJA COINCIDENCIA ({porcentaje:.0f}%)"
            desc = "No coincide con las características típicas."

        centro = ctk.CTkFrame(resultado_frame, fg_color="transparent")
        centro.pack(expand=True)

        ctk.CTkLabel(
            centro,
            text=f"{icono} {mensaje}",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=color
        ).pack(pady=20)

        ctk.CTkLabel(
            centro,
            text=desc,
            font=ctk.CTkFont(family="Segoe UI", size=15),
            text_color="#F3F4F6"
        ).pack(pady=10)

        ctk.CTkLabel(
            centro,
            text=f"Coincidencias: {coincidencias} de {total} características",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#9CA3AF"
        ).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="Verificar otra especie",
            command=self.iniciar_verificacion,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=200,
            height=45,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Cerrar Verificador",
            command=self.cerrar_ventana,
            fg_color=COLOR_ERROR,
            hover_color=COLOR_SECONDARY_HOVER,
            width=200,
            height=45,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        ).pack(side="left", padx=10)