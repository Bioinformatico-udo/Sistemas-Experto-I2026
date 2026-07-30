import os

# --- Configuración Global de Colores y Estilo ---
COLOR_PRIMARY_DARK = "#4F46E5"    
COLOR_PRIMARY_LIGHT = "#818CF8"   
COLOR_BACKGROUND_MAIN = "#0F172A"    
COLOR_BACKGROUND_SIDEBAR = "#020617"   
COLOR_CARD_BACKGROUND = "#1E293B"     
COLOR_TEXT_PRIMARY = "#F8FAFC"   
COLOR_TEXT_SECONDARY = "#94A3B8"  
COLOR_BUTTON_HOVER = "#3730A3"             
COLOR_SIDEBAR_BUTTON_HOVER = "#1E293B"     
COLOR_SIDEBAR_BUTTON_ACTIVE = "#06B6D4"    

# --- Directorios y Rutas Dinámicas ---
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Construye las rutas uniendo carpetas a partir de FRONTEND_DIR ---
ICON_DIR = os.path.join(FRONTEND_DIR, "assets", "icons")
PAGE_DIR = os.path.join(FRONTEND_DIR, "pages")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# --- Constantes para nombres de archivos de iconos ---
ICON_INICIO = "inicio.png"
ICON_CARACTERISTICAS = "caracteristicas.png"
ICON_COMO_USAR = "como_usar.png"
ICON_GLOSARIO = "glosario.png"
ICON_SOBRE_NOSOTROS = "sobre_nosotros.png"
ICON_IDENTIFICADOR = "identificador.png"
ICON_VERIFICADOR = "verificador.png"
ICON_ADMINISTRADOR = "administrador.png"
ICON_LOGIN = "logo_sesion.png"
IMAGE_PRINCIPAL_FILENAME = "imagen_principal.jpg"

# ================== FUNCIÓN DE CENTRADO REUTILIZABLE ==================
def centrar_toplevel(ventana, ancho, alto, fijar_tamano=True):
    """Centra una ventana Toplevel en la pantalla y opcionalmente fija su tamaño."""
    # Calcula la posición para centrar la ventana
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    if fijar_tamano:
        ventana.resizable(False, False)