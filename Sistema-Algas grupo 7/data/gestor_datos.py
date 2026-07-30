# data/gestor_datos.py
import json
import os

class GestorDatos:
    """Clase para manejar la persistencia de datos de las especies en formato JSON."""

    def __init__(self):
        # Genera la ruta dinámica hacia 'algas_db.json' dentro de la carpeta 'data'
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_db = os.path.join(directorio_actual, "algas_db.json")
        self.base_algas = self._cargar_datos()

    def _cargar_datos(self):
        """Lee y carga los datos desde el archivo JSON."""
        if not os.path.exists(self.ruta_db):
            return {}
        
        try:
            with open(self.ruta_db, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            print("Error: No se pudo leer el archivo JSON correctamente.")
            return {}

    def _guardar_datos(self):
        """Sobrescribe el archivo JSON con los datos actuales en memoria."""
        try:
            with open(self.ruta_db, 'w', encoding='utf-8') as archivo:
                # ensure_ascii=False permite que se guarden bien las tildes y ñ
                json.dump(self.base_algas, archivo, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False

    def obtener_todas(self):
        """Devuelve el diccionario completo de especies registradas."""
        return self.base_algas

    def registrar_especie(self, nombre, clase, familia, caracteristicas, ruta_imagen="default.png"):
        """Añade una nueva especie al diccionario y actualiza el archivo JSON."""
        if nombre in self.base_algas:
            return False, "La especie ya existe en la base de conocimiento."

        self.base_algas[nombre] = {
            "clase": clase,
            "familia": familia,
            "imagen": ruta_imagen,
            "caracteristicas": caracteristicas
        }
        
        exito = self._guardar_datos()
        
        if exito:
            return True, f"La especie '{nombre}' ha sido registrada con éxito."
        else:
            return False, "Ocurrió un error al intentar guardar en el archivo de base de datos."