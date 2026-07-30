import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from frontend.styles import centrar_toplevel

# Función para cargar módulos del backend
def cargar_modulos_backend():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(current_dir, "backend")
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        from backend.motor_inferencia import MotorInferencia
        from backend.base_conocimiento import PREGUNTAS_OPCIONES, PREGUNTAS
        return MotorInferencia, PREGUNTAS_OPCIONES, PREGUNTAS, True
    except Exception as e:
        print(f"Error al importar módulos del backend: {e}")
        messagebox.showerror("Error de Importación", str(e))
    return None, None, None, False

MotorInferencia, PREGUNTAS_OPCIONES, PREGUNTAS, backend_loaded = cargar_modulos_backend()

class CustomFuzzyInputDialog(ctk.CTkToplevel):
    def __init__(self, master, text, title, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title(title)
        self.overrideredirect(True)
        self.configure(fg_color="#0F172A")
        
        centrar_toplevel(self,320,200)
        
        self.text_value = None

        inner_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#0F172A")
        inner_frame.pack(padx=20, pady=20, fill="both", expand=True)

        label = ctk.CTkLabel(inner_frame, text=text, text_color="#F9FAFB", wraplength=350, font=ctk.CTkFont(size=14))
        label.pack(pady=(10, 15))

        self.entry = ctk.CTkEntry(inner_frame, fg_color="#1F2937", text_color="#F9FAFB", border_color="#374151", height=35)
        self.entry.pack(pady=(0, 20), padx=20, fill="x")
        self.entry.bind("<Return>", self.get_value) 

        ok_btn = ctk.CTkButton(inner_frame, text="Aceptar", command=self.get_value,  fg_color="#0D9488", hover_color="#0F766E", 
                              text_color="#F9FAFB", font=ctk.CTkFont(weight="bold"), height=35, width=120)
        ok_btn.pack(pady=(0, 10))

        self.focus_set()
        self.grab_set() 
        self.wait_window() 

    def get_value(self, event=None):
        self.text_value = self.entry.get()
        self.destroy()

    def get_input(self):
        return self.text_value

class AppIdentificador:
    def __init__(self, root, main_app=None):
        self.root = root
        self.main_app = main_app
        self.root.title("Identificador de Crustáceos Anomuros de la Familia Porcellanidae")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color="#0F172A")

        if not backend_loaded:
            messagebox.showerror("Error Crítico", "No se pudieron cargar los módulos de inferencia.")
            self.root.destroy()
            return

        self.motor = MotorInferencia(self)
        self.campos = {}
    
        for clave, opciones in PREGUNTAS_OPCIONES.items():
            label_texto = PREGUNTAS.get(clave, clave.replace("_", " ").title())
            self.campos[clave] = {"label": label_texto, "tipo": "combo", "valores": opciones}

        self.widgets = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#1F2937")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="Identificación de Crustáceos Anomuros de la Familia Porcellanidae",
                     font=ctk.CTkFont(size=19, weight="bold"), text_color="#F9FAFB").pack(pady=10)

        form_frame = ctk.CTkScrollableFrame(main_frame, corner_radius=10, fg_color="#374151")
        form_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        for i, (clave, config) in enumerate(self.campos.items()):
            ctk.CTkLabel(form_frame, text=config["label"], text_color="#9CA3AF",
                        font=ctk.CTkFont(weight="bold"), anchor="w", wraplength=400).grid( 
                        row=i, column=0, pady=25, padx=(20, 30), sticky="w")
            
            max_longitud = max([len(str(val)) for val in config["valores"]]) if config["valores"] else 20
            ancho_calculado = max(250, max_longitud * 9)
            
            widget = ctk.CTkComboBox(form_frame, values=config["valores"], state="readonly",
                                    width=ancho_calculado, fg_color="#1F2937", button_color="#2563EB",
                                    dropdown_fg_color="#374151", dropdown_hover_color="#4B5563",
                                    text_color="#F9FAFB", font=ctk.CTkFont(weight="bold"))
            if config["valores"]:
                widget.set(config["valores"][0])

            widget.grid(row=i, column=1, pady=25, padx=(0, 20), sticky="ew")
            self.widgets[clave] = widget

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="#1F2937")
        buttons_frame.pack(pady=10)
        
        ctk.CTkButton(buttons_frame, text="Analizar Especie", command=self.procesar, 
                    fg_color="#0D9488", hover_color="#0F766E", text_color="#F9FAFB",
                    font=ctk.CTkFont(weight="bold"), width=200, height=45).grid(row=0, column=0, padx=20)
        
        ctk.CTkButton(buttons_frame, text="Cerrar Identificador", command=self.root.destroy,
                    fg_color="#DC2626", hover_color="#B91C1C", width=200, height=45).grid(row=0, column=1, padx=20)

    def procesar(self):
        try:
            self.motor.hechos.clear()
            self.motor.hechos_difusos.clear()
            self.motor.reglas_aplicadas.clear()
            self.motor.conclusiones.clear()

            for clave, widget in self.widgets.items():
                valor = widget.get().strip().lower()
                if valor:
                    self.motor.hechos[clave] = valor

            self.motor.ejecutar()
            
            especie, certeza = self.motor.obtener_especie_con_certeza()

            if not especie:
                messagebox.showinfo("Sin resultados", "No se encontraron coincidencias con las características seleccionadas.")
                return
            try:
                from frontend.pages.resultado_especie import VentanaResultadoEspecie
                VentanaResultadoEspecie(self.root, especie, certeza)
            except ImportError as e:
                messagebox.showerror("Error de Módulo", f"No se pudo cargar la vista de resultados.\n{e}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar la inferencia.\n{e}")

    # Fallback para el motor si falta un dato
    def preguntar(self, atributo, texto):
        return "no"

    def preguntar_con_opciones(self, atributo, texto, opciones):
        return opciones[0] if opciones else None

    def preguntar_difuso(self, atributo, categoria):
        texto = f"Para afinar la certeza ({categoria}):\nIngrese el {atributo.replace('_', ' ')} en centímetros (ej. 2.5):"
        
        dialog = CustomFuzzyInputDialog(self.root, text=texto, title="Datos adicionales (Lógica Difusa)")
        respuesta = dialog.get_input()
        
        if respuesta:
            try:
                return float(respuesta)
            except ValueError:
                return 0.5
        return None