import os
import sys
import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import shutil
from PIL import Image
import re

# =========================== CONFIGURACIÓN DE RUTAS DINÁMICAS ==================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")
IMAGENES_ESPECIES_DIR = os.path.join(ASSETS_DIR, "imagenes_especies")
JSON_ESPECIES_PATH = os.path.join(BASE_DIR, "especies_personalizadas.json")

if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)
try:
    from backend.base_conocimiento import CARACTERISTICAS_ESPECIES
except ImportError:
    CARACTERISTICAS_ESPECIES = {}

# ================== CONFIGURACIÓN Y ESTILOS ==================
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
ERROR_HOVER = "#B91C1C"

# ================== FUNCIONES AUXILIARES ==================
def centrar_ventana(ventana, ancho, alto):
    ventana.geometry(f"{ancho}x{alto}")
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"+{x}+{y}")
    ventana.resizable(False, False)

def eliminar_duplicados_y_normalizar(lista_caracteristicas):
    unicas = []
    for c in lista_caracteristicas:
        normalizada = c.strip().lower()
        if normalizada and not any(normalizada == u.strip().lower() for u in unicas):
            unicas.append(c.strip()) # Se guarda la versión original con formato
    return unicas

def cargar_especies_json():
    """Carga las especies desde el archivo JSON."""
    if not os.path.exists(JSON_ESPECIES_PATH):
        return []
    try:
        with open(JSON_ESPECIES_PATH, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else []
    except json.JSONDecodeError:
        messagebox.showwarning("Advertencia", "El archivo 'especies_personalizadas.json' está corrupto o vacío. Se creará uno nuevo.")
        return []
    except Exception as e:
        messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo JSON: {e}")
        return []

def guardar_especies_json(especies):
    """Guarda la lista de especies en el archivo JSON."""
    try:
        with open(JSON_ESPECIES_PATH, "w", encoding="utf-8") as f:
            json.dump(especies, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error de Guardado", f"No se pudo guardar en la base de datos:\n{e}")
        return False

CARACTERISTICAS_ESPECIES = {}
try:
    from backend.base_conocimiento import CARACTERISTICAS_ESPECIES as backend_caract
    CARACTERISTICAS_ESPECIES.update(backend_caract)
except ImportError:
    print("Advertencia: No se pudo importar CARACTERISTICAS_ESPECIES desde backend.base_conocimiento. Se usará el JSON.")

# Se carga también del JSON para tener una vista completa y actualizada
especies_desde_json = cargar_especies_json()
for especie_data in especies_desde_json:
    nombre = especie_data.get("nombre")
    caracteristicas = especie_data.get("caracteristicas", [])
    if nombre and nombre not in CARACTERISTICAS_ESPECIES:
        CARACTERISTICAS_ESPECIES[nombre] = caracteristicas
    elif nombre and nombre in CARACTERISTICAS_ESPECIES:
        # Si ya existe en el backend, fusionar características (para evitar duplicados)
        caract_existentes = CARACTERISTICAS_ESPECIES[nombre]
        caract_json_norm = {c.strip().lower() for c in caracteristicas}
        caract_existentes_norm = {c.strip().lower() for c in caract_existentes}
        for c in caracteristicas:
            if c.strip().lower() not in caract_existentes_norm:
                CARACTERISTICAS_ESPECIES[nombre].append(c.strip())
                caract_existentes_norm.add(c.strip().lower())


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
        self.imagen_guardada_nombre = None
        self.preview_label = None
        self.crear_interfaz()

    def crear_interfaz(self):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        header_text_frame = ctk.CTkFrame(header, fg_color="transparent")
        header_text_frame.pack(side="left")
        
        ctk.CTkLabel(header_text_frame, text="Nueva Especie", font=("Segoe UI", 24, "bold"), text_color=PRIMARY).pack(anchor="w")
        ctk.CTkLabel(header_text_frame, text="Complete los campos requeridos para el registro (*)", font=("Segoe UI", 12), text_color=TEXT_MUTED).pack(anchor="w")

        content = ctk.CTkFrame(outer, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        left_col = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=15)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        left_col.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(left_col, text="Nombre científico *",
                     font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 5))
        self.nombre_entry = ctk.CTkEntry(left_col, height=40, placeholder_text="Ej: Pachycheles chacei ", fg_color=ENTRY_BG, 
                                         border_color=BORDER, text_color=TEXT_MAIN, font=("Segoe UI", 13))
        self.nombre_entry.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(left_col, text="Características (una por línea) *",
                     font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN).pack(anchor="w", padx=15, pady=(0, 5))
        self.carac_text = ctk.CTkTextbox(left_col, fg_color=ENTRY_BG, border_color=BORDER, border_width=1, 
                                         text_color=TEXT_MAIN,
                                         font=("Segoe UI", 13), activate_scrollbars=True)
        self.carac_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        right_col = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=15)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)

        ctk.CTkLabel(right_col, text="Imagen de la especie *",
                     font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 10))

        preview_frame = ctk.CTkFrame(right_col, fg_color=ENTRY_BG, corner_radius=10, border_color=BORDER, border_width=1)
        preview_frame.pack(padx=15, pady=0, fill="both", expand=True)
        
        self.preview_label = ctk.CTkLabel(preview_frame, text="Sin vista previa",
                                          font=("Segoe UI", 12), text_color=TEXT_MUTED, justify="center")
        self.preview_label.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkButton(right_col, text="Seleccionar imagen...", command=self.seleccionar_imagen,
                      height=36, corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                      font=("Segoe UI", 12, "bold")).pack(fill="x", padx=15, pady=10)

        self.img_name_label = ctk.CTkLabel(right_col, text="Ningún archivo seleccionado",
                                           font=("Segoe UI", 11), text_color=TEXT_MUTED, wraplength=200)
        self.img_name_label.pack(pady=(0, 15))

        btn_frame = ctk.CTkFrame(outer, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))

        inner_btn_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        inner_btn_frame.pack(anchor="center")

        btn_guardar = ctk.CTkButton(inner_btn_frame, text="Guardar Especie", command=self.guardar_especie, width=180,
                                    height=42, corner_radius=10, fg_color=PRIMARY, hover_color=PRIMARY_HOVER, 
                                    font=("Segoe UI", 13, "bold"))
        btn_guardar.pack(side="left", padx=8)

        btn_cerrar = ctk.CTkButton(inner_btn_frame, text="Cerrar", command=self.confirmar_cierre, width=130, height=42, 
                                   corner_radius=10, fg_color= "#B91C1C", border_color=BORDER, border_width=1,
                                   hover_color=ERROR_HOVER, text_color=TEXT_MAIN, font=("Segoe UI", 13, "bold"))
        btn_cerrar.pack(side="left", padx=8)

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(title="Seleccionar imagen de la especie", 
                                           filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif"), ("Todos", "*.*")])
        if ruta:
            self.imagen_path = ruta
            self.img_name_label.configure(text=os.path.basename(ruta))
            self.mostrar_preview(ruta)
        else:
            if not self.imagen_path:
                self.img_name_label.configure(text="Ningún archivo seleccionado")
                self.preview_label.configure(image=None, text="Sin vista previa")

    def mostrar_preview(self, ruta):
        """Muestra una vista previa de la imagen seleccionada."""
        try:
            img = Image.open(ruta)
            img.thumbnail((220, 180)) # Ajusta el tamaño para la vista previa
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=ctk_img, text="")
        except Exception as e:
            self.preview_label.configure(image=None, text="Error al cargar\nla imagen")
            messagebox.showerror("Error de Imagen", f"No se pudo previsualizar la imagen.\n{e}")

    def validar_campos(self):
        """Realiza todas las validaciones necesarias antes de guardar."""
        # 1. Validación de Nombre Científico
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error de Validación", "El nombre científico es obligatorio.")
            return False, None, None, None

        if len(nombre) < 3 or len(nombre) > 100:
            messagebox.showerror("Error de Validación", "El nombre científico debe tener entre 3 y 100 caracteres.")
            return False, None, None, None
            
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-]+$", nombre):
            messagebox.showerror("Error de Validación", "El nombre científico solo debe contener letras, espacios y guiones.")
            return False, None, None, None

        # 2. Validación de Características
        caract_bruto = self.carac_text.get("1.0", "end-1c").strip().splitlines()
        caract = eliminar_duplicados_y_normalizar(caract_bruto)
        
        if not caract:
            messagebox.showerror("Error de Validación", "Debe ingresar al menos una característica.")
            return False, None, None, None
            
        for c in caract:
            if len(c) < 4:
                messagebox.showerror("Error de Validación", f"La característica '{c}' es demasiado corta (mínimo 4 caracteres).")
                return False, None, None, None
            if len(c) > 200:
                messagebox.showerror("Error de Validación", f"La característica '{c}' excede el límite de 200 caracteres.")
                return False, None, None, None

        # 3. Validación de Imagen
        if not self.imagen_path and self.imagen_guardada_nombre is None:
            messagebox.showerror("Error de Validación", "Debe subir una imagen para la especie.")
            return False, None, None, None

        if self.imagen_path:
            ext = os.path.splitext(self.imagen_path)[1].lower()
            extensiones_validas = {'.jpg', '.jpeg', '.png', '.gif'}
            
            if ext not in extensiones_validas:
                messagebox.showerror("Error de Validación", "El formato del archivo de imagen no es válido. Utilice JPG, PNG o GIF.")
                return False, None, None, None

        # Si todas las validaciones pasan, se retorna True y los datos son procesados
        return True, nombre, caract, self.imagen_path

    def obtener_nombre_archivo_seguro(self, nombre_especie):
        """ Para generar un nombre de archivo seguro para la imagen."""
        ext = os.path.splitext(self.imagen_path)[1].lower()
        safe_name = re.sub(r'[^\w\s-]', '', nombre_especie).strip()
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        
        nombre_base = f"{safe_name}{ext}"
        nombre_final = nombre_base
        contador = 1
        
        # Para asegurar que el nombre del archivo sea único en el directorio de destino
        while os.path.exists(os.path.join(IMAGENES_ESPECIES_DIR, nombre_final)):
            nombre_final = f"{safe_name}_{contador}{ext}"
            contador += 1
        return nombre_final

    def guardar_especie(self):
        """Para Validar los datos y guardar la nueva especie o actualizar una existente."""
        
        # --- Validación General de Campos ---
        valido, nombre, caract, ruta_imagen_temporal = self.validar_campos()
        if not valido:
            return

        # --- Procesamiento de Especie Existente ---
        nombre_lower = nombre.lower()
        nombre_existente_original = None
        for clave in CARACTERISTICAS_ESPECIES.keys():
            if clave.lower() == nombre_lower:
                nombre_existente_original = clave
                break

        if nombre_existente_original:
            caract_actuales_norm = [c.strip().lower() for c in CARACTERISTICAS_ESPECIES[nombre_existente_original]]
            nuevas_caract_a_agregar = []
            
            for c_nueva in caract:
                if c_nueva.strip().lower() not in caract_actuales_norm:
                    nuevas_caract_a_agregar.append(c_nueva.strip())
                    caract_actuales_norm.append(c_nueva.strip().lower()) # Para añadir a la lista para evitar duplicados en esta iteración

            if not nuevas_caract_a_agregar:
                messagebox.showinfo("Sin cambios", "Todas las características ingresadas ya existen en la ficha de esta especie. No se realizaron cambios.")
                self.destroy()
                return

            resp = messagebox.askyesno(
                "Especie Existente",
                f"La especie '{nombre_existente_original}' ya existe.\n¿Desea añadir las características nuevas que no estén repetidas?\n\n"
                "Seleccione 'Sí' para agregar solo las nuevas características a la ficha existente."
            )
            if not resp:
                self.destroy()
                return

            # Si el usuario acepta, se actualiza CARACTERISTICAS_ESPECIES y luego el JSON
            CARACTERISTICAS_ESPECIES[nombre_existente_original].extend(nuevas_caract_a_agregar)
           
            especies_json_actual = cargar_especies_json()
            for especie_data in especies_json_actual:
                if especie_data.get("nombre") == nombre_existente_original:
                    especie_data["caracteristicas"] = CARACTERISTICAS_ESPECIES[nombre_existente_original]
                    break
            
            if guardar_especies_json(especies_json_actual):
                messagebox.showinfo("Éxito", f"Se añadieron {len(nuevas_caract_a_agregar)} característica(s) nueva(s) a '{nombre_existente_original}'.")
                self.destroy()
            return
        
        # Manejo de la imagen
        img_destino_nombre = "placeholder.jpg" # Valor por defecto
        if self.imagen_path:
            try:
                img_destino_nombre = self.obtener_nombre_archivo_seguro(nombre)
                shutil.copy(self.imagen_path, os.path.join(IMAGENES_ESPECIES_DIR, img_destino_nombre))
                self.imagen_guardada_nombre = img_destino_nombre # Se guarda el nombre para futuras referencias
            except Exception as e:
                messagebox.showerror("Error de Imagen", f"No se pudo copiar la imagen: {e}")
                return # Se detiene si hay un error al copiar la imagen

        # Preparar datos para el JSON
        nueva_especie_data = {
            "nombre": nombre,
            "caracteristicas": caract,
            "imagen": img_destino_nombre
        }
        
        # Cargar datos existentes, añadir la nueva y guardar
        especies_json_actual = cargar_especies_json()
        especies_json_actual.append(nueva_especie_data)
        
        if guardar_especies_json(especies_json_actual):
            # Actualizar la caché en memoria si el guardado fue exitoso
            CARACTERISTICAS_ESPECIES[nombre] = caract
            if hasattr(self.parent, 'cargar_especies_personalizadas'):
                self.parent.cargar_especies_personalizadas()
            messagebox.showinfo("Éxito", "Especie agregada correctamente.")
            self.destroy()

    def confirmar_cierre(self):
        """Para preguntar al usuario si desea cerrar si hay cambios no guardados."""

        # Para comprobar si hay algún contenido en los campos principales
        nombre_actual = self.nombre_entry.get().strip()
        caract_actual = self.carac_text.get("1.0", "end-1c").strip()
        imagen_seleccionada = self.imagen_path is not None

        if nombre_actual or caract_actual or imagen_seleccionada:
            respuesta = messagebox.askyesno(
                "Confirmar Cierre",
                "¿Está seguro de que desea cerrar la ventana? Los cambios no guardados se perderán."
            )
            if respuesta:
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("200x200")

    root.mainloop()