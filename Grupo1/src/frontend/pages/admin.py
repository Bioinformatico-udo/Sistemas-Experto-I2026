# frontend/pages/admin.py
import os
import sys
import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import shutil
from PIL import Image

# ================== CONFIGURACIÓN DE RUTAS ==================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")
IMAGENES_ESPECIES_DIR = os.path.join(ASSETS_DIR, "imagenes_especies")

if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from base_conocimiento import CARACTERISTICAS_ESPECIES

# ================== CREDENCIALES ==================
try:
    from credenciales import ADMIN_USER, ADMIN_PASS
except ImportError:
    ADMIN_USER = "admin"
    ADMIN_PASS = "porcellanidae2024"

# ================== PALETA DE COLORES ==================
BG_DARK = "#0B0F19"
CARD_BG = "#1A2332"
PRIMARY = "#0D9488"
PRIMARY_HOVER = "#0F766E"
SECONDARY = "#2563EB"
SECONDARY_HOVER = "#1D4ED8"
TEXT_MAIN = "#F1F5F9"
TEXT_MUTED = "#94A3B8"
ENTRY_BG = "#1E293B"
BORDER = "#334155"
ERROR = "#DC2626"
SUCCESS = "#22C55E"

# ================== FUNCIONES AUXILIARES ==================
def centrar_ventana(ventana, ancho, alto):
    """Centra la ventana de manera robusta."""
    ventana.geometry(f"{ancho}x{alto}")
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"+{x}+{y}")
    ventana.resizable(False, False)

def cargar_icono(nombre):
    """Carga un icono de la carpeta icons."""
    ruta = os.path.join(ASSETS_DIR, "icons", nombre)
    if os.path.exists(ruta):
        return ctk.CTkImage(light_image=Image.open(ruta), dark_image=Image.open(ruta), size=(40, 40))
    return None

def eliminar_duplicados_y_normalizar(lista_caracteristicas):
    """Elimina duplicados (ignorando mayúsculas/minúsculas y espacios) y devuelve la lista limpia."""
    unicas = []
    for c in lista_caracteristicas:
        normalizada = c.strip().lower()
        if normalizada and not any(normalizada == u.strip().lower() for u in unicas):
            unicas.append(c.strip())
    return unicas

# ================== CLASE LOGIN ==================
class AppLoginAdmin(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Acceso Administrador")
        self.configure(fg_color=BG_DARK)
        centrar_ventana(self, 420, 440)
        self.grab_set()

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=20)
        card.pack(fill="both", expand=True, padx=25, pady=25)

        icono = cargar_icono("login.png")
        if icono:
            ctk.CTkLabel(card, image=icono, text="").pack(pady=(20, 5))
        else:
            ctk.CTkLabel(card, text="🔐", font=("Segoe UI Emoji", 45)).pack(pady=(20, 5))

        ctk.CTkLabel(card, text="INICIO DE SESIÓN",
                     font=("Segoe UI", 24, "bold"),
                     text_color=PRIMARY).pack(pady=(0, 15))

        self.user_entry = ctk.CTkEntry(card, placeholder_text="Usuario", width=280,
                                       height=45, corner_radius=12,
                                       fg_color=ENTRY_BG, border_color=BORDER,
                                       text_color=TEXT_MAIN, font=("Segoe UI", 13))
        self.user_entry.pack(pady=8)

        self.pass_entry = ctk.CTkEntry(card, placeholder_text="Contraseña", show="*",
                                       width=280, height=45, corner_radius=12,
                                       fg_color=ENTRY_BG, border_color=BORDER,
                                       text_color=TEXT_MAIN, font=("Segoe UI", 13))
        self.pass_entry.pack(pady=8)

        ctk.CTkButton(card, text="INGRESAR", command=self.verificar,
                      width=220, height=45, corner_radius=12,
                      fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                      font=("Segoe UI", 14, "bold")).pack(pady=20)

        ctk.CTkLabel(card, text="Acceso exclusivo para administradores",
                     font=("Segoe UI", 10), text_color=TEXT_MUTED).pack(pady=(0, 15))

    def verificar(self):
        user = self.user_entry.get()
        pwd = self.pass_entry.get()
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            self.destroy()
            AppAdminPanel(self.parent)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# ================== CLASE PANEL AGREGAR ESPECIE ==================
class AppAdminPanel(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Agregar Nueva Especie")
        self.configure(fg_color=BG_DARK)
        centrar_ventana(self, 800, 650)
        self.grab_set()

        self.imagen_path = None
        self.preview_label = None
        self.crear_interfaz()

    def crear_interfaz(self):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", pady=(10, 20))
        ctk.CTkLabel(header, text="➕ Nueva Especie",
                     font=("Segoe UI", 28, "bold"),
                     text_color=PRIMARY).pack(side="left")
        ctk.CTkLabel(header, text="Complete los campos requeridos",
                     font=("Segoe UI", 12), text_color=TEXT_MUTED).pack(side="right", padx=10)

        content = ctk.CTkFrame(outer, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)

        # Columna izquierda
        left_col = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=15)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        left_col.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(left_col, text="Nombre científico *",
                     font=("Segoe UI", 14, "bold"), text_color=TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 5))
        self.nombre_entry = ctk.CTkEntry(left_col, width=380, height=42,
                                         placeholder_text="Ej: Testus marinus",
                                         fg_color=ENTRY_BG, border_color=BORDER,
                                         text_color=TEXT_MAIN, font=("Segoe UI", 13))
        self.nombre_entry.pack(padx=15, pady=(0, 15))

        ctk.CTkLabel(left_col, text="Características * (una por línea)",
                     font=("Segoe UI", 14, "bold"), text_color=TEXT_MAIN).pack(anchor="w", padx=15, pady=(0, 5))
        self.carac_text = ctk.CTkTextbox(left_col, width=380, height=250,
                                         fg_color=ENTRY_BG, border_color=BORDER,
                                         text_color=TEXT_MAIN, font=("Segoe UI", 13),
                                         activate_scrollbars=True)
        self.carac_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)

        # Columna derecha
        right_col = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=15)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        ctk.CTkLabel(right_col, text="Imagen de la especie",
                     font=("Segoe UI", 14, "bold"), text_color=TEXT_MAIN).pack(pady=(15, 10))

        preview_frame = ctk.CTkFrame(right_col, fg_color=ENTRY_BG, corner_radius=10)
        preview_frame.pack(padx=15, pady=5, fill="both", expand=True)
        self.preview_label = ctk.CTkLabel(preview_frame, text="Previsualización",
                                          font=("Segoe UI", 13), text_color=TEXT_MUTED,
                                          justify="center")
        self.preview_label.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkButton(right_col, text="Seleccionar imagen...", command=self.seleccionar_imagen,
                      width=160, height=35, corner_radius=8,
                      fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                      font=("Segoe UI", 12, "bold")).pack(pady=10)

        self.img_name_label = ctk.CTkLabel(right_col, text="Ningún archivo",
                                           font=("Segoe UI", 11), text_color=TEXT_MUTED,
                                           wraplength=180)
        self.img_name_label.pack(pady=(0, 15))

        # Botón guardar
        btn_frame = ctk.CTkFrame(outer, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        ctk.CTkButton(btn_frame, text="💾 Guardar Especie", command=self.guardar_especie,
                      width=250, height=45, corner_radius=10,
                      fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                      font=("Segoe UI", 15, "bold")).pack()

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen de la especie",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif"), ("Todos", "*.*")]
        )
        if ruta:
            self.imagen_path = ruta
            self.img_name_label.configure(text=os.path.basename(ruta))
            self.mostrar_preview(ruta)
        else:
            self.imagen_path = None
            self.img_name_label.configure(text="Ningún archivo")
            self.preview_label.configure(image=None, text="Previsualización")

    def mostrar_preview(self, ruta):
        try:
            img = Image.open(ruta)
            img.thumbnail((220, 180))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=ctk_img, text="")
        except Exception as e:
            self.preview_label.configure(image=None, text="Error al cargar\nla imagen")
            messagebox.showerror("Error", f"No se pudo previsualizar la imagen.\n{e}")

    def guardar_especie(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre científico es obligatorio.")
            return

        # Verificar duplicado de nombre (insensible a mayúsculas)
        nombre_lower = nombre.lower()
        existe = False
        nombre_existente = None
        for clave in CARACTERISTICAS_ESPECIES.keys():
            if clave.lower() == nombre_lower:
                existe = True
                nombre_existente = clave
                break

        if existe:
            # Obtener características actuales (normalizadas)
            caract_actuales = CARACTERISTICAS_ESPECIES[nombre_existente]
            caract_norm_actuales = [c.strip().lower() for c in caract_actuales]

            # Obtener características nuevas del textbox (normalizadas y sin duplicados)
            nuevas_caract_bruto = self.carac_text.get("1.0", "end-1c").strip().splitlines()
            nuevas_caract = eliminar_duplicados_y_normalizar(nuevas_caract_bruto)
            nuevas_norm = [c.strip().lower() for c in nuevas_caract]

            # Si todas las características nuevas ya existen en la ficha actual
            if all(nc in caract_norm_actuales for nc in nuevas_norm):
                messagebox.showinfo(
                    "Sin cambios",
                    "Todas las características ingresadas ya existen en la ficha de esta especie. No se realizaron cambios."
                )
                return

            # Si hay alguna característica nueva que no esté en la ficha
            resp = messagebox.askyesno(
                "Especie existente",
                f"La especie '{nombre_existente}' ya existe.\n¿Desea añadir las características que no estén repetidas?\n\n"
                "Seleccione 'Sí' para agregar solo las nuevas líneas a la ficha existente."
            )
            if resp:
                # Agregar solo las características que no están presentes
                agregadas = 0
                for nc in nuevas_caract:
                    if nc.strip().lower() not in caract_norm_actuales:
                        CARACTERISTICAS_ESPECIES[nombre_existente].append(nc.strip())
                        self.actualizar_json(nombre_existente, nc.strip())
                        agregadas += 1
                if agregadas > 0:
                    messagebox.showinfo("Éxito", f"Se añadieron {agregadas} característica(s) nueva(s).")
                    self.destroy()
                else:
                    messagebox.showinfo("Información", "No se añadió ninguna característica nueva (ya existían todas).")
            return

        # Especie nueva: procesar características
        caract_bruto = self.carac_text.get("1.0", "end-1c").strip().splitlines()
        caract = eliminar_duplicados_y_normalizar(caract_bruto)
        if not caract:
            messagebox.showerror("Error", "Debe ingresar al menos una característica.")
            return

        # Avisar si había duplicados eliminados
        if len(caract) < len([c for c in caract_bruto if c.strip()]):
            messagebox.showinfo("Duplicados eliminados",
                                "Se detectaron características duplicadas y fueron eliminadas automáticamente.")

        # Procesar imagen (igual que antes)
        img_destino = "placeholder.jpg"
        if self.imagen_path:
            try:
                ext = os.path.splitext(self.imagen_path)[1]
                safe_name = "".join(c for c in nombre if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_') + ext
                destino = os.path.join(IMAGENES_ESPECIES_DIR, safe_name)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                shutil.copy(self.imagen_path, destino)
                img_destino = safe_name
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")
                return

        nueva_especie = {
            "nombre": nombre,
            "caracteristicas": caract,
            "imagen": img_destino
        }
        json_path = os.path.join(BASE_DIR, "especies_personalizadas.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    especies = json.loads(contenido) if contenido else []
            except:
                especies = []
        else:
            especies = []
        especies.append(nueva_especie)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(especies, f, indent=2, ensure_ascii=False)

        CARACTERISTICAS_ESPECIES[nombre] = caract
        if hasattr(self.parent, 'cargar_especies_personalizadas'):
            self.parent.cargar_especies_personalizadas()

        messagebox.showinfo("Éxito", "Especie agregada correctamente.")
        self.destroy()

    def actualizar_json(self, nombre, nueva_caracteristica):
        json_path = os.path.join(BASE_DIR, "especies_personalizadas.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    especies = json.loads(contenido) if contenido else []
            except:
                especies = []
        else:
            especies = []
        for sp in especies:
            if sp["nombre"] == nombre:
                sp["caracteristicas"].append(nueva_caracteristica)
                break
        else:
            especies.append({
                "nombre": nombre,
                "caracteristicas": CARACTERISTICAS_ESPECIES[nombre],
                "imagen": "placeholder.jpg"
            })
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(especies, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("200x200")
    app = AppLoginAdmin(root)
    root.mainloop()