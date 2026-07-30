from data.gestor_datos import GestorDatos
from data.gestor_usuarios import GestorUsuarios
from gui.login import VentanaLogin
from gui.interfaz import AplicacionExpertaAlgas

def iniciar_sistema():
    gestor_db = GestorDatos()
    gestor_usr = GestorUsuarios()

    def abrir_app_principal(usuario_logueado):
        # Inicializa la ventana principal solo cuando el login es correcto
        app = AplicacionExpertaAlgas(base_conocimiento=gestor_db)
        # Inyectamos el gestor de usuarios a la app para el menú de gestión
        app.gestor_usr = gestor_usr
        app.mainloop()

    # Arrancar con la ventana de Login
    login = VentanaLogin(
        gestor_usuarios=gestor_usr,
        callback_login_exitoso=abrir_app_principal
    )
    login.mainloop()

if __name__ == "__main__":
    iniciar_sistema()