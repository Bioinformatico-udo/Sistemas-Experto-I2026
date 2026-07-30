# gui/interfaz.py
import os
import customtkinter as ctk
from gui.utilidades import CacheImagenes
from gui.componentes import TarjetaAlga
from gui.identificador import IdentificadorAsistido
from gui.ventanas import VentanaDetalle, VentanaNuevaEspecie, VentanaDetalle, VentanaNuevaEspecie, VentanaGestionUsuarios


class AplicacionExpertaAlgas(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self, base_conocimiento):
        super().__init__()

        self.gestor = base_conocimiento
        self.base_algas = self.gestor.obtener_todas()

        self.clase_seleccionada = "Todas"

        # Configuración de la ventana
        self.title("Sistema Experto - Identificación de Algas")
        self.geometry("1100x700")
        self.minsize(1000, 650)

        # Ruta raíz y assets
        self.ruta_raiz = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.ruta_assets = os.path.join(self.ruta_raiz, "assets")
        self.cache_imagenes = CacheImagenes(self.ruta_assets)

        # Crear interfaz
        self.crear_interfaz_principal()

        # Inicializar identificador
        self.identificador = IdentificadorAsistido(base_algas=self.base_algas)
        self.construir_identificador_cascada()

    def crear_interfaz_principal(self):
        """Crea la estructura de la ventana (navbar, columnas, galería)."""
        # Navbar
        self.navbar = ctk.CTkFrame(
            self,
            height=50,
            corner_radius=0,
            fg_color=("#222222", "#111111")
        )
        self.navbar.pack(fill="x", side="top")

        lbl_logo = ctk.CTkLabel(
            self.navbar,
            text="🔬 Sistema Experto de Algas",
            text_color="white",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lbl_logo.pack(side="left", padx=20, pady=10)

        btn_usuarios = ctk.CTkButton(
            self.navbar,
            text="⚙️ Usuarios",
            fg_color="#2980B9",
            hover_color="#2471A3",
            width=100,
            font=ctk.CTkFont(weight="bold"),
            command=lambda: VentanaGestionUsuarios.abrir(self, self.gestor_usr)
        )
        btn_usuarios.pack(side="right", padx=(0, 10), pady=10)

        btn_add = ctk.CTkButton(
            self.navbar,
            text="+ Añadir Nueva Especie",
            fg_color="#27AE60",
            hover_color="#219653",
            font=ctk.CTkFont(weight="bold"),
            command=self.click_anadir_especie
        )
        btn_add.pack(side="right", padx=20, pady=10)

        # Cuerpo (dos columnas)
        self.cuerpo = ctk.CTkFrame(self, fg_color="transparent")
        self.cuerpo.pack(fill="both", expand=True, padx=20, pady=20)

        # Columna izquierda: identificador
        self.col_izquierda = ctk.CTkFrame(
            self.cuerpo,
            width=350,
            corner_radius=12
        )
        self.col_izquierda.pack(side="left", fill="both", padx=(0, 10))
        self.col_izquierda.pack_propagate(False)

        ctk.CTkLabel(
            self.col_izquierda,
            text="Identificador Asistido",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15, padx=15, anchor="w")

        self.box_pregunta = ctk.CTkFrame(
            self.col_izquierda,
            fg_color=("#F5F5F5", "#202020"),
            corner_radius=10
        )
        self.box_pregunta.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Columna derecha: galería
        self.col_derecha = ctk.CTkFrame(self.cuerpo, corner_radius=12)
        self.col_derecha.pack(
            side="right", fill="both", expand=True, padx=(10, 0)
        )

        self.header_galeria = ctk.CTkFrame(self.col_derecha, fg_color="transparent")
        self.header_galeria.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            self.header_galeria,
            text="Galería Interactiva",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15, padx=20, anchor="w")

        self.var_busqueda = ctk.StringVar()
        self.var_busqueda.trace_add("write", self.filtrar_galeria) # Detecta cuando se escribe

        self.entry_busqueda = ctk.CTkEntry(
            self.header_galeria,
            placeholder_text="Buscar Alga por Nombre",
            width=220
        )
        self.entry_busqueda.pack(side="right")

        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.filtrar_galeria())

        # --- BARRA DE BOTONES DE FILTRO POR CLASE ---
        self.frame_filtros_clase = ctk.CTkFrame(self.col_derecha, fg_color="transparent")
        self.frame_filtros_clase.pack(fill="x", padx=20, pady=(5, 10))

        # Lista de configuración para los botones: (Texto/Clase, Color normal, Color hover)
        opciones_filtros = [
            ("Todas", "#555555", "#333333"),
            ("Chlorophyta", "#27AE60", "#1E8449"),
            ("Phaeophyceae", "#D35400", "#A04000"),
            ("Rhodophyta", "#C0392B", "#922B21")
        ]

        for nombre_clase, color, color_hover in opciones_filtros:
            btn = ctk.CTkButton(
                self.frame_filtros_clase,
                text=nombre_clase,
                height=28,
                fg_color=color,
                hover_color=color_hover,
                # Usamos nombre=nombre_clase en el lambda para capturar el valor correcto
                command=lambda c=nombre_clase: self.seleccionar_filtro_clase(c)
            )
            btn.pack(side="left", padx=(0, 5))

        self.grid_galeria = ctk.CTkScrollableFrame(
            self.col_derecha,
            fg_color="transparent"
        )
        self.grid_galeria.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Render inicial de la galería
        self.actualizar_galeria_tarjetas()

    # IDENTIFICADOR ASISTIDO EN CASCADA

    def construir_identificador_cascada(self):
        """Construye la UI del cuestionario en cascada (Clase -> Familia -> Especie)."""
        # Limpiar contenedor
        for w in self.box_pregunta.winfo_children():
            w.destroy()

        # Variables de estado para los menús
        self.var_clase = ctk.StringVar(value="Seleccione Clase")
        self.var_familia = ctk.StringVar(value="Seleccione Familia")
        self.var_especie = ctk.StringVar(value="Seleccione Clave")
        self.diccionario_claves = {} # Para mapear la selección visual con el nombre real de la especie

        # --- 1. MENÚ CLASE ---
        ctk.CTkLabel(
            self.box_pregunta, 
            text="1. Grupo o Clase:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(25, 5), padx=20, anchor="w")

        opciones_clase = self.identificador.obtener_clases()
        self.cb_clase = ctk.CTkOptionMenu(
            self.box_pregunta,
            variable=self.var_clase,
            values=opciones_clase,
            command=self.al_seleccionar_clase
        )
        self.cb_clase.pack(fill="x", padx=20, pady=(0, 15))

        # --- 2. MENÚ FAMILIA ---
        ctk.CTkLabel(
            self.box_pregunta, 
            text="2. Familia Morfológica:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5), padx=20, anchor="w")

        self.cb_familia = ctk.CTkOptionMenu(
            self.box_pregunta,
            variable=self.var_familia,
            values=["Esperando selección previa..."],
            state="disabled", # Bloqueado inicialmente
            command=self.al_seleccionar_familia
        )
        self.cb_familia.pack(fill="x", padx=20, pady=(0, 15))

        # --- 3. MENÚ CLAVE DICOTÓMICA ---
        ctk.CTkLabel(
            self.box_pregunta, 
            text="3. Clave Dicotómica:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(10, 5), padx=20, anchor="w")

        self.cb_especie = ctk.CTkOptionMenu(
            self.box_pregunta,
            variable=self.var_especie,
            values=["Esperando selección previa..."],
            state="disabled" # Bloqueado inicialmente
        )
        self.cb_especie.pack(fill="x", padx=20, pady=(0, 25))

        # --- BOTÓN IDENTIFICAR ---
        self.btn_identificar = ctk.CTkButton(
            self.box_pregunta,
            text="Ver Detalles del Alga",
            height=40,
            fg_color="#27AE60",
            hover_color="#219653",
            font=ctk.CTkFont(weight="bold", size=14),
            state="disabled", # Bloqueado inicialmente
            command=self.mostrar_resultado_identificacion
        )
        self.btn_identificar.pack(fill="x", padx=20, pady=(10, 20))


    def al_seleccionar_clase(self, valor):
        """Evento que se dispara al elegir una clase. Desbloquea las familias."""
        familias = self.identificador.obtener_familias(valor)
        
        # Actualizar y desbloquear menú de familia
        self.var_familia.set("Seleccione Familia")
        self.cb_familia.configure(values=familias, state="normal")
        
        # Resetear y bloquear el menú inferior (por si el usuario retrocede)
        self.var_especie.set("Esperando selección previa...")
        self.cb_especie.configure(values=["Esperando selección previa..."], state="disabled")
        self.btn_identificar.configure(state="disabled")


    def al_seleccionar_familia(self, valor):
        """Evento que se dispara al elegir una familia. Desbloquea las claves."""
        especies_claves = self.identificador.obtener_especies_por_claves(self.var_clase.get(), valor)
        
        opciones_claves = []
        self.diccionario_claves.clear()
        
        for especie, clave in especies_claves:
            # Creamos un texto descriptivo para que el usuario lea la clave
            texto_opcion = f"Clave: {clave}"
            # Acortamos el texto si es muy largo para que no deforme el menú
            texto_mostrar = texto_opcion[:65] + "..." if len(texto_opcion) > 65 else texto_opcion
            
            opciones_claves.append(texto_mostrar)
            # Guardamos la relación entre el texto visual y el nombre real de la especie
            self.diccionario_claves[texto_mostrar] = especie

        # Actualizar y desbloquear clave y botón final
        self.var_especie.set("Seleccione Clave")
        self.cb_especie.configure(values=opciones_claves, state="normal")
        self.btn_identificar.configure(state="normal")


    def mostrar_resultado_identificacion(self):
        """Obtiene la especie seleccionada y abre su ventana modal."""
        seleccion = self.var_especie.get()
        if seleccion in self.diccionario_claves:
            nombre_especie = self.diccionario_claves[seleccion]
            self.abrir_modal_detalle(nombre_especie)

    # GALERÍA y Filtros

    

    def filtrar_galeria(self, *arg):
        """Callback ejecutado cada vez que cambia el texto del buscador."""
        texto_filtro = self.entry_busqueda.get()
        self.actualizar_galeria_tarjetas(filtro=texto_filtro)

    def seleccionar_filtro_clase(self, clase):
        """Actualiza la clase seleccionada y refresca las tarjetas."""
        self.clase_seleccionada = clase
        self.filtrar_galeria()  

    def actualizar_galeria_tarjetas(self, filtro=""):
        """Construye la galería de tarjetas a partir de los datos actuales."""
        for w in self.grid_galeria.winfo_children():
            w.destroy()

        self.grid_galeria.grid_columnconfigure(
            (0, 1, 2), weight=1, pad=10
        )

        fila = 0
        columna = 0

        filtro_norm = filtro.strip().lower()

        for nombre, datos in self.base_algas.items():
            if filtro_norm and filtro_norm not in nombre.lower():
                continue
            clase_alga = datos.get("clase", "")
            if self.clase_seleccionada != "Todas" and self.clase_seleccionada.lower() != clase_alga.lower():
                continue

            img = self.cache_imagenes.obtener(
                datos.get("imagen", "default.png"),
                (180, 120)
            )
            tarjeta = TarjetaAlga(
                self.grid_galeria,
                nombre=nombre,
                clase=datos["clase"],
                familia=datos["familia"],
                imagen_ctk=img,
                al_hacer_clic=self.abrir_modal_detalle
            )
            tarjeta.grid(
                row=fila, column=columna, padx=10, pady=10,
                sticky="nsew"
            )

            columna += 1
            if columna > 2:
                columna = 0
                fila += 1

    # ============================
    # MODALES
    # ============================

    def abrir_modal_detalle(self, nombre_especie):
        """Abre el modal de detalle de una especie."""
        datos = self.base_algas.get(nombre_especie)
        if datos:
            VentanaDetalle.abrir(
                self,
                nombre_especie,
                datos,
                self.ruta_assets
            )

    def click_anadir_especie(self):
        """Abre el modal para añadir una nueva especie."""
        VentanaNuevaEspecie.abrir(
            self,
            self.gestor,
            self.recargar_galeria_en_caliente
        )

    def recargar_galeria_en_caliente(self):
        """Recarga los datos del gestor y actualiza la galería y el identificador."""
        self.base_algas = self.gestor.obtener_todas()
        self.actualizar_galeria_tarjetas()
        self.identificador.base_algas = self.base_algas
        self.construir_identificador_cascada()
