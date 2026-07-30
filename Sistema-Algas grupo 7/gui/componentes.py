# gui/componentes.py
import customtkinter as ctk


class TarjetaAlga(ctk.CTkFrame):
    """Tarjeta para mostrar una especie en la galería."""

    def __init__(self, master, nombre, clase, familia, imagen_ctk,
                 al_hacer_clic, **kwargs):
        super().__init__(
            master,
            corner_radius=10,
            fg_color=("#EAEAEA", "#2B2B2B"),
            **kwargs
        )

        self.nombre = nombre
        self.al_hacer_clic = al_hacer_clic

        # Imagen o placeholder
        if imagen_ctk is not None:
            self.lbl_img = ctk.CTkLabel(self, text="", image=imagen_ctk)
        else:
            self.lbl_img = ctk.CTkLabel(
                self,
                text="🌿 Sin imagen",
                height=120,
                fg_color=("#D0D0D0", "#3A3A3A"),
                corner_radius=8
            )
        self.lbl_img.pack(fill="x", padx=8, pady=8)

        # Nombre
        self.lbl_nombre = ctk.CTkLabel(
            self,
            text=nombre,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.lbl_nombre.pack(fill="x", padx=10, pady=(2, 0))

        # Taxonomía
        self.lbl_taxo = ctk.CTkLabel(
            self,
            text=f"{clase} • {familia}",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        self.lbl_taxo.pack(fill="x", padx=10, pady=(0, 8))

        # Hacer toda la tarjeta cliqueable
        self.bind(
            "<Button-1>",
            lambda e: self.al_hacer_clic(self.nombre)
        )
        self.lbl_img.bind(
            "<Button-1>",
            lambda e: self.al_hacer_clic(self.nombre)
        )
        self.lbl_nombre.bind(
            "<Button-1>",
            lambda e: self.al_hacer_clic(self.nombre)
        )
        self.lbl_taxo.bind(
            "<Button-1>",
            lambda e: self.al_hacer_clic(self.nombre)
        )
