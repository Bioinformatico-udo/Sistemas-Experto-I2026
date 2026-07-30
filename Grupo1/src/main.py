import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import importlib
import json
from PIL import Image
from frontend.styles import (
    COLOR_PRIMARY_DARK, COLOR_PRIMARY_LIGHT, COLOR_BACKGROUND_MAIN, COLOR_BACKGROUND_SIDEBAR, COLOR_CARD_BACKGROUND,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_BUTTON_HOVER, COLOR_SIDEBAR_BUTTON_HOVER, COLOR_SIDEBAR_BUTTON_ACTIVE,
    ICON_DIR, PAGE_DIR, ASSETS_DIR, ICON_INICIO, ICON_CARACTERISTICAS, ICON_COMO_USAR, ICON_GLOSARIO, ICON_SOBRE_NOSOTROS,
    ICON_IDENTIFICADOR, IMAGE_PRINCIPAL_FILENAME, ICON_VERIFICADOR, ICON_ADMINISTRADOR,
    centrar_toplevel
)
import backend.base_conocimiento as base_conocimiento
import io

# --- CONFIGURACIÓN PARA MANEJAR CARACTERES UNICODE (UTF-8) ---
try:
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except Exception:
    pass
# -------------------------------------------------------------

class CrustaceosPorcellanidae(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.WIDTH, self.HEIGHT = 1100, 650
        self._init_window()
        self._init_vars()
        self.check_directories_and_modules()
        self.create_widgets()

        # Cargar especies personalizadas desde JSON al iniciar
        self.cargar_especies_personalizadas()

        # Mostrar por defecto la página de inicio y activar su botón
        self.show_frame(self.page_instances["inicio"].get_frame(),
                        self.nav_buttons_data[0]["container"],
                        self.nav_buttons_data[0]["text_label"],
                        self.nav_buttons_data[0]["icon_label"])

        self.deiconify()  
        self.after(10, lambda: (self.deiconify(), self.state('zoomed')))

    def _init_window(self):
        """Configura la ventana principal, tamaño, modo y centrado."""
        self.title("PorcellanSpark - v1.0")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.configure(fg_color=COLOR_BACKGROUND_MAIN)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

    def _init_vars(self):
        """Inicializa variables para estado de navegación y ventanas."""
        self.active_nav_button_container = None
        self.active_nav_text_label = None
        self.active_nav_icon_label = None
        self.identificador_window = None
        self.verificador_window = None
        self.administrador_window = None

    def check_directories_and_modules(self):
        print("--- Verificando directorios y módulos ---")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        paths = [
            (ICON_DIR, "directorio de iconos"),
            (PAGE_DIR, "directorio de páginas"),
            (ASSETS_DIR, "directorio de assets"),
            (os.path.join(base_dir, "backend", "motor_inferencia.py"), "motor_inferencia.py"),
            (os.path.join(base_dir, "backend", "base_conocimiento.py"), "base_conocimiento.py")
        ]
        for path, desc in paths:
            if not os.path.exists(path):
                print(f"Advertencia: {desc} no existe en {path}")
        print("--- Verificación completada ---")

    def create_widgets(self):
        """Crea los componentes principales: sidebar, contenido, páginas y botones de navegación."""
        self._create_sidebar()
        self._create_main_frame()
        self._load_pages()
        self._create_nav_buttons()

    def _create_sidebar(self):
        """Construye la barra lateral con logo y título."""
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_BACKGROUND_SIDEBAR)
        self.sidebar_frame.pack(side="left", fill="y")
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PorcellanSpark - v1.0",
                                         font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
                                         text_color=COLOR_PRIMARY_LIGHT)
        self.logo_label.grid(row=0, column=0, padx=40, pady=40, sticky="nw")

    def _create_main_frame(self):
        """Configura el área principal donde se mostrarán las páginas."""
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BACKGROUND_MAIN, corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def _load_pages(self):
        """Carga las páginas dinámicamente usando importlib y las prepara para mostrar."""
        self.pages = {
            "inicio": {"module": "inicio", "class": "InicioPage"},
            "caracteristicas": {"module": "caracteristicas", "class": "CaracteristicasPage"},
            "como_usar": {"module": "como_usar", "class": "ComoUsarPage"},
            "glosario": {"module": "glosario", "class": "GlosarioPage"},
            "sobre_nosotros": {"module": "sobre_nosotros", "class": "SobreNosotrosPage"}
        }
        self.page_instances = {}
        for key, info in self.pages.items():
            module_path = f"frontend.pages.{info['module']}"
            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, info['class'])
                instance = cls(self.main_frame, self)
                self.page_instances[key] = instance
                # Coloca el frame en la interfaz y lo oculta inicialmente
                instance.get_frame().grid(row=0, column=0, sticky="nsew")
                print(f"Página '{key}' cargada correctamente.")
            except Exception as e:
                print(f"Error cargando página '{key}': {e}")
                messagebox.showerror("Error", f"Error al cargar página '{key}': {e}")

    def _create_nav_buttons(self):
        """Crea los botones de navegación en la barra lateral con iconos y textos."""
        nav_items = [
            (ICON_INICIO, "INICIO / INFORMACIÓN GENERAL", "inicio"),
            (ICON_CARACTERISTICAS, "CARACTERÍSTICAS Y FUNCIONALIDADES", "caracteristicas"),
            (ICON_COMO_USAR, "CÓMO USAR", "como_usar"),
            (ICON_GLOSARIO, "GLOSARIO DE TÉRMINOS", "glosario"),
            (ICON_SOBRE_NOSOTROS, "SOBRE NOSOTROS", "sobre_nosotros"),
            (ICON_ADMINISTRADOR, "ADMINISTRADOR", "administrador")
        ]
        self.nav_buttons_data = []

        for i, (icon_filename, text, page_key) in enumerate(nav_items):
            icon_image = self.load_image(icon_filename, size=(35,35))
            container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", corner_radius=10, cursor="hand2")
            container.grid(row=i+2, column=0, padx=10, pady=5, sticky="ew")
            container.grid_columnconfigure(0, weight=0)
            container.grid_columnconfigure(1, weight=0)

            # Crear etiqueta para icono
            icon_label = ctk.CTkLabel(container, image=icon_image, text="", width=60)
            icon_label.grid(row=1, column=0, padx=(10,5), pady=15)

            # Crear etiqueta para texto
            text_label = ctk.CTkLabel(container, text=text,
                                      font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                      text_color=COLOR_TEXT_SECONDARY,
                                      anchor="w", justify="left", padx=5)
            text_label.grid(row=1, column=1, padx=(0,10), pady=15, sticky="w")

            # Asociar eventos para interacción visual y navegación
            for widget in [container, text_label, icon_label]:
                widget.bind("<Enter>", lambda e, bc=container, tl=text_label, il=icon_label: self.on_enter_nav(bc, tl, il))
                widget.bind("<Leave>", lambda e, bc=container, tl=text_label, il=icon_label: self.on_leave_nav(bc, tl, il))

                # Lógica para los botones de acción especiales
                if page_key == "identificador":
                    widget.bind("<Button-1>", lambda e: self.abrir_identificador())
                elif page_key == "verificador":
                    widget.bind("<Button-1>", lambda e: self.abrir_verificador())
                elif page_key == "administrador":
                    widget.bind("<Button-1>", lambda e: self.abrir_administrador())
                else:
                    widget.bind("<Button-1>", lambda e, p=page_key, bc=container, tl=text_label, il=icon_label: self.show_frame(self.page_instances[p].get_frame(), bc, tl, il))

            # Guardar en lista para gestionar estilos y estado
            self.nav_buttons_data.append({"container": container, "text_label": text_label, "icon_label": icon_label, "page_key": page_key})

    def load_image(self, filename, directory=None, size=(20,20)):
        """Carga una imagen y la convierte en CTkImage, devuelve placeholder si falla."""
        if directory is None:
            directory = ICON_DIR
        filepath = os.path.join(directory, filename)
        try:
            pil_image = Image.open(filepath)
            return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)
        except Exception:
            # En caso de error, retornar una imagen simple de color
            placeholder = Image.new('RGB', size, color=COLOR_TEXT_SECONDARY)
            return ctk.CTkImage(light_image=placeholder, dark_image=placeholder, size=size)

    def on_enter_nav(self, container, text_label, icon_label):
        """Cambio de estilo al pasar el ratón sobre un botón de navegación."""
        if container != self.active_nav_button_container:
            container.configure(fg_color=COLOR_SIDEBAR_BUTTON_HOVER)
            text_label.configure(text_color=COLOR_TEXT_PRIMARY)

    def on_leave_nav(self, container, text_label, icon_label):
        """Restaurar estilos al quitar el ratón del botón de navegación."""
        if container != self.active_nav_button_container:
            container.configure(fg_color="transparent")
            text_label.configure(text_color=COLOR_TEXT_SECONDARY)

    def show_frame(self, frame, container=None, text_label=None, icon_label=None):
        """Muestra la página seleccionada y actualiza estilos de los botones."""
        # Restablece estilos a todos los botones
        for btn in self.nav_buttons_data:
            btn["container"].configure(fg_color="transparent")
            btn["text_label"].configure(text_color=COLOR_TEXT_SECONDARY)

        # Oculta todas las páginas
        for p in self.page_instances.values():
            p.get_frame().grid_forget()

        # Muestra la página seleccionada
        frame.grid(row=0, column=0, sticky="nsew")

        # Marca el botón activo
        if container:
            container.configure(fg_color=COLOR_SIDEBAR_BUTTON_ACTIVE)
            text_label.configure(text_color=COLOR_TEXT_PRIMARY)
            self.active_nav_button_container = container
            self.active_nav_text_label = text_label
            self.active_nav_icon_label = icon_label
        else:
            # Si no se especifica, activa el primero
            if self.nav_buttons_data:
                first = self.nav_buttons_data[0]
                first["container"].configure(fg_color=COLOR_SIDEBAR_BUTTON_ACTIVE)
                first["text_label"].configure(text_color=COLOR_TEXT_PRIMARY)
                self.active_nav_button_container = first["container"]
                self.active_nav_text_label = first["text_label"]
                self.active_nav_icon_label = first["icon_label"]

    # ==================== IDENTIFICADOR DE ESPECIE ====================
    def abrir_identificador(self):
        """Abre la ventana de identificación, evita duplicados y la trae al frente si ya existe."""
        if self.identificador_window and self.identificador_window.winfo_exists():
            self.identificador_window.lift()
            print("Ventana de identificador ya abierta, trayéndola al frente.")
            return
        self._crear_ventana_identificador()

    def _crear_ventana_identificador(self):
        try:
            import frontend.pages.identificador as ident_mod
            self.identificador_window = ctk.CTkToplevel(self)
            self.identificador_window.title("Identificador de Crustáceos Anomuros de la Familia Porcellanidae")
            centrar_toplevel(self.identificador_window, 800, 600)
            self.identificador_window.transient(self)

            # Construir la interfaz interna ANTES de hacer grab_set
            app_identificador = ident_mod.AppIdentificador(self.identificador_window, self)

            # Ahora sí, hacer modal
            self.identificador_window.grab_set()

            def on_closing():
                if self.identificador_window:
                    try:
                        if self.identificador_window.grab_current() == self.identificador_window:
                            self.identificador_window.grab_release()
                        self.identificador_window.destroy()
                    except:
                        pass
                    finally:
                        self.identificador_window = None

            self.identificador_window.protocol("WM_DELETE_WINDOW", on_closing)
            print("Nueva ventana de identificador creada.")
        except Exception as e:
            print(f"Error creando ventana identificador: {e}")
            messagebox.showerror("Error", f"Error al abrir identificador: {e}")
            if self.identificador_window:
                self.identificador_window.destroy()
                self.identificador_window = None

    # ==================== VERIFICADOR DE ESPECIE ====================
    def abrir_verificador(self):
        """Abre la ventana de verificación, evita duplicados y la trae al frente si ya existe."""
        if self.verificador_window and self.verificador_window.winfo_exists():
            self.verificador_window.lift()
            print("Ventana de verificador ya abierta, trayéndola al frente.")
            return
        self._crear_ventana_verificador()

    def _crear_ventana_verificador(self):
        try:
            import frontend.pages.verificador as verif_mod
            self.verificador_window = ctk.CTkToplevel(self)
            self.verificador_window.title("Verificador de Especies de Crustáceos Anomuros de la Familia Porcellanidae")
            centrar_toplevel(self.verificador_window, 900, 600)
            self.verificador_window.transient(self)

            app_verificador = verif_mod.AppVerificador(self.verificador_window, self)

            self.verificador_window.grab_set()

            def on_closing():
                if self.verificador_window:
                    try:
                        if self.verificador_window.grab_current() == self.verificador_window:
                            self.verificador_window.grab_release()
                        self.verificador_window.destroy()
                    except:
                        pass
                    finally:
                        self.verificador_window = None

            self.verificador_window.protocol("WM_DELETE_WINDOW", on_closing)
            print("Nueva ventana de verificador creada.")
        except Exception as e:
            print(f"Error creando ventana verificador: {e}")
            messagebox.showerror("Error", f"Error al abrir verificador: {e}")
            if self.verificador_window:
                self.verificador_window.destroy()
                self.verificador_window = None

    # ==================== ADMINISTRADOR ====================
    def abrir_administrador(self):
        if self.administrador_window and self.administrador_window.winfo_exists():
            self.administrador_window.lift()
            return
        try:
            from frontend.pages.login_admin import AppLoginAdmin
            self.administrador_window = AppLoginAdmin(self)
            self.administrador_window.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_ventana("administrador"))
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir administrador: {e}")
            self.administrador_window = None

    def _cerrar_ventana(self, ventana):
        if ventana == "identificador":
            if self.identificador_window:
                self.identificador_window.destroy()
                self.identificador_window = None
        elif ventana == "verificador":
            if self.verificador_window:
                self.verificador_window.destroy()
                self.verificador_window = None
        elif ventana == "administrador":
            if self.administrador_window:
                self.administrador_window.destroy()
                self.administrador_window = None

    # ==================== CARGA DE ESPECIES PERSONALIZADAS ====================
    def cargar_especies_personalizadas(self):
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "especies_personalizadas.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    if not contenido:   # archivo vacío
                        return
                    custom_list = json.loads(contenido)
                for sp in custom_list:
                    base_conocimiento.CARACTERISTICAS_ESPECIES[sp["nombre"]] = sp["caracteristicas"]
                print("Especies personalizadas cargadas correctamente.")
            except json.JSONDecodeError as e:
                print(f"Error de JSON (archivo ignorado): {e}")
            except Exception as e:
                print("Error cargando especies personalizadas:", e)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    backend_dir = os.path.join(BASE_DIR, "backend")
    if os.path.isdir(backend_dir) and backend_dir not in sys.path:
        sys.path.append(backend_dir)
        print(f"Directorio 'backend' añadido a sys.path: {backend_dir}")

    app = CrustaceosPorcellanidae()
    app.mainloop()