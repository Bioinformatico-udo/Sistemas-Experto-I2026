import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageGrab
from frontend.styles import centrar_toplevel

# --- Configuración de Rutas Dinámicas ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(FRONTEND_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from frontend.styles import ASSETS_DIR
    IMAGENES_ESPECIES_DIR = os.path.join(ASSETS_DIR, "imagenes_especies")
except ImportError:
    ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")
    IMAGENES_ESPECIES_DIR = os.path.join(ASSETS_DIR, "imagenes_especies")

try:
    from backend.base_conocimiento import CARACTERISTICAS_ESPECIES
except ImportError:
    CARACTERISTICAS_ESPECIES = {}

#--------------- Resultados ----------------------
class VentanaResultadoEspecie(ctk.CTkToplevel):
    def __init__(self, parent, especie, certeza):
        super().__init__(parent)
        centrar_toplevel(self, 900, 500)
        self.especie = especie
        self.certeza = certeza 
        self.title("Resultado de la Identificación de la Especie")
        self.geometry("900x500")
        self.configure(fg_color="#0F172A")
        self.transient(parent)
        self.grab_set()

        self.construir_interfaz()

    def construir_interfaz(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1F2937")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- Encabezado ---
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 15))

        ctk.CTkLabel(header_frame, text=f"Especie identificada: {self.especie.title()}",
                     font=ctk.CTkFont(size=22, weight="bold"), text_color="#3B82F6").pack(pady=(0, 5))
        
        #Mostrar grado de certeza
        color_certeza = "#10B981" if self.certeza >= 80 else "#F59E0B" if self.certeza >= 50 else "#EF4444"
        ctk.CTkLabel(header_frame, text=f"Grado de Certeza: {self.certeza}% (Inferencia Híbrida)",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=color_certeza).pack()

        # --- Contenido (Imagen y Ficha Tecnica) ---
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # --- Carga de Imagen ---
        nombre_imagen = "".join(c for c in self.especie if c.isalnum() or c in (' ', '-', '_')).rstrip()
        nombre_imagen = nombre_imagen.replace(' ', '_').lower() + '.jpg'
        img_path = os.path.join(IMAGENES_ESPECIES_DIR, nombre_imagen)

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                pil_img.thumbnail((300, 250)) 
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
                ctk.CTkLabel(left_frame, image=ctk_img, text="").pack(anchor="center", pady=10)
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                ctk.CTkLabel(left_frame, text="[Error al renderizar la imagen]", text_color="#9CA3AF").pack()
        else:
            ctk.CTkLabel(left_frame, text="[Imagen no disponible]", text_color="#9CA3AF").pack()

        # --- Ficha Técnica ---
        caracts = CARACTERISTICAS_ESPECIES.get(self.especie, [])
        texto = "\n\n".join(f"• {c}" for c in caracts)
        
        ctk.CTkLabel(right_frame, text="Ficha Técnica:", font=ctk.CTkFont(size=16, weight="bold"), 
                    text_color="#F9FAFB").pack(anchor="w", pady=(10, 10))

        ficha_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="transparent", height=150)
        ficha_scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(ficha_scroll, text=texto if texto else "No hay datos disponibles para esta especie.", justify="left",
                     font=ctk.CTkFont(size=13), text_color="#F9FAFB",wraplength=320).pack(anchor="w")
        
        # --- Botones de Acción ---
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=15)

        ctk.CTkButton(self.buttons_frame, text="Exportar a PNG", command=self.exportar_png,
                      fg_color="#0D9488", hover_color="#0F766E", text_color="#F9FAFB",
                      font=ctk.CTkFont(weight="bold"), width=200, height=45).pack(side="left", padx=10)

        ctk.CTkButton(self.buttons_frame, text="Cerrar", command=self.destroy,
                      fg_color="#DC2626", hover_color="#B91C1C", text_color="#F9FAFB",
                      font=ctk.CTkFont(weight="bold"), width=200, height=45).pack(side="left", padx=10)

    #-------- Exportar resultado a png -------------------------
    def exportar_png(self):
        """Captura el main_frame y guarda la imagen."""
        self.buttons_frame.pack_forget()
        self.update_idletasks()
        
        x = self.main_frame.winfo_rootx()
        y = self.main_frame.winfo_rooty()
        ancho = self.main_frame.winfo_width()
        alto = self.main_frame.winfo_height()
        bbox = (x, y, x + ancho, y + alto)
        
        try:
            captura = ImageGrab.grab(bbox)
        except Exception as e:
            self.buttons_frame.pack(pady=15)
            messagebox.showerror("Error", f"No se pudo capturar la pantalla:\n{e}")
            return

        self.buttons_frame.pack(pady=15)
        self.update_idletasks()

        nombre_default = f"resultado_{self.especie.replace(' ', '_').lower()}.png"
        directorio_seguro = os.path.expanduser("~")
        
        ruta_guardado = filedialog.asksaveasfilename(
            initialdir=directorio_seguro,
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png")],
            initialfile=nombre_default,
            title="Guardar resultado como..."
        )
        
        if ruta_guardado:
            try:
                captura.save(ruta_guardado)
                messagebox.showinfo("Exportación Exitosa", f"El resultado se exportó de forma limpia en:\n{ruta_guardado}")
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"Hubo un problema al guardar la imagen:\n{str(e)}")