# gui/ventanas.py
import os
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox


class VentanaDetalle:
    """Ventana modal para mostrar detalles de una especie."""

    @staticmethod
    def abrir(master, especie, datos, ruta_assets):
        """Abre el modal de detalle."""
        carac = datos["caracteristicas"]

        modal = ctk.CTkToplevel(master)
        modal.title(f"Detalles: {especie}")
        modal.geometry("550x750")
        modal.transient(master)
        modal.grab_set()

        # Título
        lbl_t = ctk.CTkLabel(
            modal,
            text=especie,
            font=ctk.CTkFont(size=22, weight="bold", slant="italic")
        )
        lbl_t.pack(pady=15)

        # Taxonomía
        lbl_taxo = ctk.CTkLabel(
            modal,
            text=f"Clase: {datos['clase']}   |   Familia: {datos['familia']}",
            text_color="#27AE60",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lbl_taxo.pack(pady=(0, 10))

        # Imagen
        nombre_img = datos.get("imagen", "default.png")
        ruta_img = os.path.join(ruta_assets, nombre_img)
        if os.path.exists(ruta_img):
            img = ctk.CTkImage(
                light_image=Image.open(ruta_img),
                dark_image=Image.open(ruta_img),
                size=(300, 200)
            )
            lbl_img = ctk.CTkLabel(modal, text="", image=img)
            lbl_img.pack(pady=10)

        # Texto con características
        txt_box = ctk.CTkTextbox(modal, font=ctk.CTkFont(size=13), wrap="word")
        txt_box.pack(fill="both", expand=True, padx=25, pady=10)

        detalles = (
            f"🔹 CLAVE DE IDENTIFICACIÓN:\n{carac.get('clave_id', 'N/A')}\n\n"
            f"🔹 TALO:\n{carac.get('talo', 'N/A')}\n\n"
            f"🔹 TAMAÑO:\n{carac.get('tamaño_cm', 'N/A')}\n\n"
            f"🔹 ESTRUCTURA CELULAR:\n{carac.get('estructura', 'N/A')}\n\n"
            f"🔹 FIJACIÓN:\n{carac.get('fijacion', 'N/A')}\n\n"
            f"🔹 HÁBITAT:\n{carac.get('habitat', 'N/A')}"
        )
        txt_box.insert("0.0", detalles)
        txt_box.configure(state="disabled")

        btn_cerrar = ctk.CTkButton(
            modal, text="Cerrar", fg_color="gray", command=modal.destroy
        )
        btn_cerrar.pack(pady=15)


class VentanaNuevaEspecie:
    """Ventana modal para registrar una nueva especie."""

    @staticmethod
    def abrir(master, gestor, recargar_callback):
        """
        gestor: instancia de GestorDatos.
        recargar_callback: función a llamar tras guardar con éxito.
        """
        modal_form = ctk.CTkToplevel(master)
        modal_form.title("Registrar Nueva Especie - Sistema Experto")
        modal_form.geometry("600x750")
        modal_form.transient(master)
        modal_form.grab_set()

        # Título
        lbl_titulo = ctk.CTkLabel(
            modal_form,
            text="Formulario 'Añadir Nueva Especie'",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        lbl_titulo.pack(pady=15)

        # Contenedor con scroll
        scroll = ctk.CTkScrollableFrame(modal_form, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=5)

        # --- SECCIÓN TAXONOMÍA ---
        ctk.CTkLabel(
            scroll,
            text="Taxonomía y Clasificación",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#27AE60"
        ).pack(anchor="w", pady=(5, 5))

        frame_tax = ctk.CTkFrame(scroll, fg_color=("#F5F5F5", "#202020"))
        frame_tax.pack(fill="x", pady=5)
        frame_tax.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frame_tax, text="Clase:").grid(
            row=0, column=0, padx=15, pady=(10, 0), sticky="w"
        )
        ctk.CTkLabel(frame_tax, text="Familia:").grid(
            row=0, column=1, padx=15, pady=(10, 0), sticky="w"
        )

        cb_clase = ctk.CTkOptionMenu(
            frame_tax,
            values=["Chlorophyta", "Rhodophyta", "Phaeophyceae"]
        )
        cb_clase.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")

        ent_familia = ctk.CTkEntry(frame_tax, placeholder_text="Ej: Ulvaceae")
        ent_familia.grid(row=1, column=1, padx=15, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(
            frame_tax, text="Nombre Científico (Especie):"
        ).grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 0), sticky="w")

        ent_nombre = ctk.CTkEntry(frame_tax, placeholder_text="Ej: Ulva rigida")
        ent_nombre.grid(
            row=3, column=0, columnspan=2, padx=15, pady=(0, 15),
            sticky="ew"
        )

        # --- SECCIÓN CARACTERÍSTICAS ---
        ctk.CTkLabel(
            scroll,
            text="Características Diagnósticas",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#27AE60"
        ).pack(anchor="w", pady=(15, 5))

        ctk.CTkLabel(
            scroll,
            text="Clave de Identificación Asistida (Pregunta Descriptiva):",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(5, 2))
        txt_clave = ctk.CTkTextbox(scroll, height=60)
        txt_clave.pack(fill="x", pady=2)
        txt_clave.insert(
            "0.0",
            "Lámina gruesa de color verde oscuro con bordes dentados rizado..."
        )

        ctk.CTkLabel(scroll, text="Morfología del Talo:").pack(
            anchor="w", pady=(5, 2)
        )
        txt_talo = ctk.CTkEntry(
            scroll,
            placeholder_text="Ej: Laminar, membranoso, lobulado..."
        )
        txt_talo.pack(fill="x", pady=2)

        ctk.CTkLabel(scroll, text="Tamaño promedio (cm):").pack(
            anchor="w", pady=(5, 2)
        )
        txt_tamano = ctk.CTkEntry(
            scroll,
            placeholder_text="Ej: 5 a 20 cm de longitud"
        )
        txt_tamano.pack(fill="x", pady=2)

        ctk.CTkLabel(scroll, text="Hábitat y Distribución Ecológica:").pack(
            anchor="w", pady=(5, 2)
        )
        txt_habitat = ctk.CTkEntry(
            scroll,
            placeholder_text=(
                "Ej: Zonas intermareales expuestas, sustrato rocoso..."
            )
        )
        txt_habitat.pack(fill="x", pady=2)

        # --- SECCIÓN IMAGEN ---
        ctk.CTkLabel(
            scroll,
            text="Imagen del Espécimen",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#27AE60"
        ).pack(anchor="w", pady=(15, 5))

        frame_img = ctk.CTkFrame(
            scroll,
            height=80,
            border_width=2,
            border_color="gray",
            fg_color="transparent"
        )
        frame_img.pack(fill="x", pady=5)

        ctk.CTkLabel(
            frame_img,
            text="📁 Imagen: [ default.png ]\n(Módulo de carga listo)",
            justify="center",
            font=ctk.CTkFont(size=12)
        ).place(relx=0.5, rely=0.5, anchor="center")

        # --- BOTÓN GUARDAR ---
        def guardar():
            nombre = ent_nombre.get().strip()
            clase = cb_clase.get()
            familia = ent_familia.get().strip()
            clave = txt_clave.get("0.0", "end").strip()
            talo = txt_talo.get().strip()
            tamano = txt_tamano.get().strip()
            habitat = txt_habitat.get().strip()

            if not nombre or not familia or not clave:
                messagebox.showerror(
                    "Campos Incompletos",
                    "Los campos Nombre Científico, Familia y Clave de "
                    "Identificación son obligatorios."
                )
                return

            caracteristicas = {
                "talo": talo if talo else "No especificado",
                "tamaño_cm": tamano if tamano else "No especificado",
                "estructura": "Definido por el recolector",
                "fijacion": "No especificado",
                "habitat": habitat if habitat else "No especificado",
                "clave_id": clave
            }

            exito, mensaje = gestor.registrar_especie(
                nombre=nombre,
                clase=clase,
                familia=familia,
                caracteristicas=caracteristicas,
                ruta_imagen="default.png"
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                modal_form.destroy()
                recargar_callback()
            else:
                messagebox.showerror("Error", mensaje)

        ctk.CTkButton(
            modal_form,
            text="Cargar Especie 💾",
            height=45,
            fg_color="#27AE60",
            hover_color="#219653",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=guardar
        ).pack(fill="x", padx=25, pady=(10, 20))

class VentanaGestionUsuarios:
    """Ventana modal para administrar y eliminar usuarios registrados."""

    @staticmethod
    def abrir(master, gestor_usuarios):
        modal = ctk.CTkToplevel(master)
        modal.title("Gestión de Usuarios")
        modal.geometry("400x450")
        modal.transient(master)
        modal.grab_set()

        ctk.CTkLabel(
            modal, 
            text="Usuarios Registrados", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)

        lbl_info = ctk.CTkLabel(
            modal, 
            text=f"Total: {gestor_usuarios.total_usuarios()}/{gestor_usuarios.MAX_USUARIOS}",
            text_color="#27AE60",
            font=ctk.CTkFont(weight="bold")
        )
        lbl_info.pack(pady=(0, 10))

        frame_lista = ctk.CTkScrollableFrame(modal, width=320, height=250)
        frame_lista.pack(pady=10, padx=20)

        def recargar_lista():
            for w in frame_lista.winfo_children():
                w.destroy()

            lbl_info.configure(
                text=f"Total: {gestor_usuarios.total_usuarios()}/{gestor_usuarios.MAX_USUARIOS}"
            )

            for usuario in gestor_usuarios.obtener_lista_usuarios():
                item = ctk.CTkFrame(frame_lista, fg_color=("#EAEAEA", "#2B2B2B"))
                item.pack(fill="x", pady=5, padx=5)

                ctk.CTkLabel(
                    item, text=f"👤 {usuario}", 
                    font=ctk.CTkFont(weight="bold")
                ).pack(side="left", padx=10)

                def eliminar_click(u=usuario):
                    if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{u}'?"):
                        exito, msj = gestor_usuarios.eliminar_usuario(u)
                        if exito:
                            messagebox.showinfo("Éxito", msj)
                            recargar_lista()
                        else:
                            messagebox.showwarning("Atención", msj)

                ctk.CTkButton(
                    item, text="🗑️", width=35, height=30,
                    fg_color="#C0392B", hover_color="#922B21",
                    command=eliminar_click
                ).pack(side="right", padx=5, pady=5)

        recargar_lista()

        ctk.CTkButton(
            modal, text="Cerrar", fg_color="gray", command=modal.destroy
        ).pack(pady=15)