import customtkinter as ctk
from tkinter import messagebox

class VentanaLogin(ctk.CTk):
    """Ventana de inicio de sesión y registro de usuarios."""

    def __init__(self, gestor_usuarios, callback_login_exitoso):
        super().__init__()

        self.gestor = gestor_usuarios
        self.callback_login_exitoso = callback_login_exitoso

        self.title("Acceso al Sistema - Identificador de Algas")
        self.geometry("400x520")
        self.resizable(False, False)

        # Tabview para Login y Registro
        self.tabview = ctk.CTkTabview(self, width=350, height=450)
        self.tabview.pack(padx=25, pady=25)

        self.tab_login = self.tabview.add("Iniciar Sesión")
        self.tab_registro = self.tabview.add("Registrarse")

        self._construir_tab_login()
        self._construir_tab_registro()

    def _construir_tab_login(self):
        ctk.CTkLabel(
            self.tab_login, text="Bienvenido", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        self.ent_user_login = ctk.CTkEntry(
            self.tab_login, placeholder_text="Usuario", width=250
        )
        self.ent_user_login.pack(pady=10)

        self.ent_pass_login = ctk.CTkEntry(
            self.tab_login, placeholder_text="Contraseña", show="*", width=250
        )
        self.ent_pass_login.pack(pady=10)

        ctk.CTkButton(
            self.tab_login, text="Ingresar", width=250, height=40,
            fg_color="#27AE60", hover_color="#219653",
            font=ctk.CTkFont(weight="bold"),
            command=self._ejecutar_login
        ).pack(pady=20)

    def _construir_tab_registro(self):
        ctk.CTkLabel(
            self.tab_registro, text="Crear Nueva Cuenta", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 5))

        self.lbl_cupos = ctk.CTkLabel(
            self.tab_registro, 
            text=f"Usuarios: {self.gestor.total_usuarios()}/{self.gestor.MAX_USUARIOS}",
            text_color="gray"
        )
        self.lbl_cupos.pack(pady=(0, 10))

        self.ent_user_reg = ctk.CTkEntry(
            self.tab_registro, placeholder_text="Nuevo Usuario", width=250
        )
        self.ent_user_reg.pack(pady=8)

        self.ent_pass_reg = ctk.CTkEntry(
            self.tab_registro, placeholder_text="Nueva Contraseña", show="*", width=250
        )
        self.ent_pass_reg.pack(pady=8)

        ctk.CTkButton(
            self.tab_registro, text="Registrar Usuario", width=250, height=40,
            fg_color="#2980B9", hover_color="#2471A3",
            font=ctk.CTkFont(weight="bold"),
            command=self._ejecutar_registro
        ).pack(pady=20)

    def _ejecutar_login(self):
        user = self.ent_user_login.get()
        password = self.ent_pass_login.get()

        exito, msj = self.gestor.validar_login(user, password)
        if exito:
            self.destroy() # Cierra la ventana de login
            self.callback_login_exitoso(user) # Inicia la app principal
        else:
            messagebox.showerror("Error de Acceso", msj)

    def _ejecutar_registro(self):
        user = self.ent_user_reg.get()
        password = self.ent_pass_reg.get()

        exito, msj = self.gestor.registrar_usuario(user, password)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.ent_user_reg.delete(0, 'end')
            self.ent_pass_reg.delete(0, 'end')
            self.lbl_cupos.configure(
                text=f"Usuarios: {self.gestor.total_usuarios()}/{self.gestor.MAX_USUARIOS}"
            )
            self.tabview.set("Iniciar Sesión")
        else:
            messagebox.showwarning("Atención", msj)