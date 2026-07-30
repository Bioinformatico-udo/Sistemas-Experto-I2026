import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

# =========================== CONFIGURACIÓN DE RUTAS ==================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from frontend.pages.agregar_nva_especie import AppAdminPanel

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# ================== CREDENCIALES ==================
try:
    from credenciales import ADMIN_USER, ADMIN_PASS
except ImportError:
    ADMIN_USER = "admin"
    ADMIN_PASS = "porcellanidae2024"

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

def cargar_icono(nombre):
    """Carga un icono de la carpeta icons."""
    ruta = os.path.join(ASSETS_DIR, "icons", nombre)
    if os.path.exists(ruta):
        return ctk.CTkImage(light_image=Image.open(ruta), dark_image=Image.open(ruta), size=(40, 40))
    return None

# ================== CLASE LOGIN ==================
class AppLoginAdmin(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Acceso Administrador")
        self.configure(fg_color=BG_DARK)
        centrar_ventana(self, 420, 480)
        self.grab_set()

        # Atajo para presionar Enter e ingresar
        self.bind("<Return>", lambda event: self.verificar())

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=20)
        card.pack(fill="both", expand=True, padx=25, pady=25)

        icono = cargar_icono("login.png")
        if icono:
            ctk.CTkLabel(card, image=icono, text="").pack(pady=(20, 5))
        else:
            ctk.CTkLabel(card, text="", font=("Segoe UI Emoji", 40)).pack(pady=(20, 5))

        ctk.CTkLabel(card, text="INICIO DE SESIÓN", font=("Segoe UI", 22, "bold"), text_color=PRIMARY).pack(pady=(0, 15))

        self.user_entry = ctk.CTkEntry(card, placeholder_text="Usuario *", width=280, height=42, corner_radius=10,
                                       fg_color=ENTRY_BG, border_color=BORDER, text_color=TEXT_MAIN, font=("Segoe UI", 13))
        self.user_entry.pack(pady=6)

        self.pass_entry = ctk.CTkEntry(card, placeholder_text="Contraseña *", show="*", width=280, height=42, corner_radius=10,
                                       fg_color=ENTRY_BG, border_color=BORDER, text_color=TEXT_MAIN, font=("Segoe UI", 13))
        self.pass_entry.pack(pady=6)

        # Botón Ingresar
        ctk.CTkButton(card, text="INGRESAR", command=self.verificar, width=280, height=42, corner_radius=10,
                      fg_color=SECONDARY, hover_color=SECONDARY_HOVER, font=("Segoe UI", 13, "bold")).pack(pady=(15, 6))

        ctk.CTkLabel(card, text="Acceso exclusivo para administradores",
                     font=("Segoe UI", 10), text_color=TEXT_MUTED).pack(pady=(0, 10))

    def verificar(self):
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        
        if not user or not pwd:
            messagebox.showwarning("Advertencia", "Por favor, complete ambos campos.")
            return

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            self.destroy()
            AppAdminPanel(self.parent)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")