import json
import os
import hashlib

class GestorUsuarios:
    """Maneja el registro, autenticación y eliminación de usuarios (Máx 6)."""

    MAX_USUARIOS = 6

    def __init__(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_db = os.path.join(directorio_actual, "usuarios.json")
        self.usuarios = self._cargar_usuarios()

    def _encriptar_password(self, password):
        """Encripta la contraseña usando SHA-256 por seguridad."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def _cargar_usuarios(self):
        """Carga los usuarios desde el archivo JSON."""
        if not os.path.exists(self.ruta_db):
            # Si no existe, crea un usuario admin por defecto
            admin_defecto = {
                "admin": {
                    "password": self._encriptar_password("admin123")
                }
            }
            self._guardar_en_disco(admin_defecto)
            return admin_defecto
        
        try:
            with open(self.ruta_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _guardar_en_disco(self, datos=None):
        """Guarda el diccionario de usuarios en el archivo JSON."""
        if datos is None:
            datos = self.usuarios
        try:
            with open(self.ruta_db, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False

    def validar_login(self, usuario, password):
        """Verifica si las credenciales son correctas."""
        usuario = usuario.strip().lower()
        if usuario in self.usuarios:
            pass_hash = self._encriptar_password(password)
            if self.usuarios[usuario]["password"] == pass_hash:
                return True, "Inicio de sesión exitoso."
        return False, "Usuario o contraseña incorrectos."

    def registrar_usuario(self, usuario, password):
        """Registra un nuevo usuario validando el límite de 6."""
        usuario = usuario.strip().lower()

        if len(self.usuarios) >= self.MAX_USUARIOS:
            return False, f"Límite alcanzado. Máximo {self.MAX_USUARIOS} usuarios permitidos."

        if not usuario or not password:
            return False, "Por favor complete todos los campos."

        if usuario in self.usuarios:
            return False, "El nombre de usuario ya está registrado."

        self.usuarios[usuario] = {
            "password": self._encriptar_password(password)
        }
        
        if self._guardar_en_disco():
            return True, f"Usuario '{usuario}' registrado con éxito."
        return False, "Error al guardar el nuevo usuario."

    def eliminar_usuario(self, usuario):
        """Elimina un usuario del sistema."""
        usuario = usuario.strip().lower()
        
        if usuario not in self.usuarios:
            return False, "El usuario no existe."

        if len(self.usuarios) <= 1:
            return False, "No se puede eliminar el único usuario del sistema."

        del self.usuarios[usuario]
        if self._guardar_en_disco():
            return True, f"Usuario '{usuario}' eliminado correctamente."
        return False, "Error al intentar eliminar el usuario."

    def obtener_lista_usuarios(self):
        """Devuelve la lista con los nombres de usuario."""
        return list(self.usuarios.keys())

    def total_usuarios(self):
        """Devuelve el conteo de usuarios registrados."""
        return len(self.usuarios)