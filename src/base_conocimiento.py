import os
import json

class BaseConocimiento:
    """
    Clase encargada de cargar, validar y administrar la base de datos de especies
    y las reglas de decisión (el árbol de decisión taxonómico).
    """
    def __init__(self, ruta_especies=None, ruta_reglas=None):
        # Determinar rutas por defecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_especies = ruta_especies or os.path.join(base_dir, 'data', 'especies.json')
        self.ruta_reglas = ruta_reglas or os.path.join(base_dir, 'data', 'reglas.json')
        
        self.especies = {}
        self.arbol_decisiones = {}
        
        self.cargar_datos()

    def cargar_datos(self):
        """Carga las especies y reglas desde archivos JSON."""
        # Cargar especies
        try:
            with open(self.ruta_especies, 'r', encoding='utf-8') as f:
                lista_especies = json.load(f)
                self.especies = {esp['id']: esp for esp in lista_especies}
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo de especies en: {self.ruta_especies}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar JSON en especies: {str(e)}")

        # Cargar árbol de decisiones/reglas
        try:
            with open(self.ruta_reglas, 'r', encoding='utf-8') as f:
                self.arbol_decisiones = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo de reglas/árbol en: {self.ruta_reglas}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar JSON en reglas: {str(e)}")

    def obtener_especie(self, especie_id):
        """Retorna los datos de una especie dado su ID o None si no existe."""
        return self.especies.get(especie_id)

    def obtener_arbol(self):
        """Retorna el árbol de decisiones completo."""
        return self.arbol_decisiones

    def listar_especies(self):
        """Retorna la lista de todas las especies registradas."""
        return list(self.especies.values())

    def agregar_especie(self, especie_dict):
        """Agrega una nueva especie y guarda el archivo especies.json actualizado."""
        esp_id = especie_dict.get("id")
        if not esp_id:
            esp_id = especie_dict.get("nombre_cientifico", "").strip().lower().replace(" ", "_")
            especie_dict["id"] = esp_id

        self.especies[esp_id] = especie_dict

        # Guardar en archivo especies.json
        lista_actualizada = list(self.especies.values())
        with open(self.ruta_especies, 'w', encoding='utf-8') as f:
            json.dump(lista_actualizada, f, ensure_ascii=False, indent=2)

        return especie_dict
