# gui/identificador.py

class IdentificadorAsistido:
    """Maneja el filtrado de opciones para el cuestionario de identificación."""

    def __init__(self, base_algas):
        self.base_algas = base_algas

    def obtener_clases(self):
        """Devuelve una lista única de todas las clases disponibles."""
        clases = set(datos["clase"] for datos in self.base_algas.values())
        return sorted(list(clases))

    def obtener_familias(self, clase_seleccionada):
        """Devuelve las familias que pertenecen a una clase específica."""
        if not clase_seleccionada or clase_seleccionada == "Seleccione Clase":
            return []
        
        familias = set(
            datos["familia"]
            for datos in self.base_algas.values()
            if datos["clase"] == clase_seleccionada
        )
        return sorted(list(familias))

    def obtener_especies_por_claves(self, clase_seleccionada, familia_seleccionada):
        """Devuelve una lista de tuplas (Especie, Clave_Dicotómica) para la selección final."""
        if not familia_seleccionada or familia_seleccionada == "Seleccione Familia":
            return []

        coincidencias = []
        for especie, datos in self.base_algas.items():
            if datos["clase"] == clase_seleccionada and datos["familia"] == familia_seleccionada:
                clave = datos["caracteristicas"].get("clave_id", "Sin clave")
                coincidencias.append((especie, clave))
                
        return coincidencias