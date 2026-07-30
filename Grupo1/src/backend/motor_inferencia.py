# =============================================================================
# MOTOR DE INFERENCIA HÍBRIDO (PROPOSICIONAL + DIFUSO)
# =============================================================================

from backend.base_conocimiento import REGLAS_PROPOSICIONALES, REGLAS_DIFUSAS, PREGUNTAS_OPCIONES
from backend.utils import grado_tamano, evaluar_incertidumbre 

class MotorInferencia:
    """
    Motor de inferencia híbrido.
    1. Fase Proposicional: Identifica la especie exacta mediante reglas duras.
    2. Fase Difusa: Calcula el grado de certeza evaluando atributos difusos (ej. tamaño).
    """

    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.reglas_prop = REGLAS_PROPOSICIONALES
        self.reglas_difusas = REGLAS_DIFUSAS
        self.hechos = {}
        self.hechos_difusos = {}
        self.reglas_aplicadas = []
        self.conclusiones = []
        self.certeza_final = 100.0

    def evaluar_condicion_proposicional(self, atributo, valor_esperado):
        """Evalúa una condición exacta"""
        if atributo in self.hechos:
            return self.hechos[atributo] == valor_esperado

        atributos_inferidos = ['superfamilia', 'familia', 'genero', 'clave_grupo', 'clave_subgrupo']
        if atributo in atributos_inferidos:
            return False

        if atributo in PREGUNTAS_OPCIONES:
            opciones = PREGUNTAS_OPCIONES[atributo]
            from backend.base_conocimiento import PREGUNTAS
            texto = PREGUNTAS.get(atributo, f"Seleccione {atributo.replace('_', ' ')}:")
            respuesta = self.interfaz.preguntar_con_opciones(atributo, texto, opciones)
        else:
            texto = f"¿{atributo.replace('_', ' ')}? (si/no)"
            respuesta = self.interfaz.preguntar(atributo, texto)

        if respuesta is None:
            respuesta = "no"
        self.hechos[atributo] = respuesta.lower()
        print(f"      [DEBUG] {atributo} = '{self.hechos[atributo]}'")
        return self.hechos[atributo] == valor_esperado

    def evaluar_condicion_difusa(self, atributo, categoria, umbral):
        # Se solicita el valor al usuario si se tiene (ej. solicitar el tamaño en cm)
        if atributo not in self.hechos_difusos:
            valor = self.interfaz.preguntar_difuso(atributo, categoria)
            if valor is None:
                valor = 0.5 # Valor neutro
            self.hechos_difusos[atributo] = valor
            
        valor_ingresado = self.hechos_difusos[atributo]
        
        grado = 0.0
        if atributo == 'tamano_cm':
            grado = grado_tamano(valor_ingresado, categoria)
        else:
            # Para respuestas subjetivas usamos evaluar_incertidumbre
            grado = evaluar_incertidumbre(str(valor_ingresado))

        return grado, grado >= umbral

    def ejecutar_proposicional(self):
        """Ejecuta la identificación exacta usando encadenamiento hacia adelante."""
        print("\n Aplicando reglas proposicionales (Filtro)...")
        print("=" * 50)

        cambios = True
        while cambios:
            cambios = False
            for regla in self.reglas_prop:
                if regla in self.reglas_aplicadas:
                    continue

                ok = True
                for attr, val in regla['condiciones']:
                    if not self.evaluar_condicion_proposicional(attr, val):
                        ok = False
                        break

                if ok:
                    self.reglas_aplicadas.append(regla)
                    for clave, valor in regla['conclusion'].items():
                        self.hechos[clave] = valor
                        if clave in ['especie', 'superfamilia', 'familia']:
                            self.conclusiones.append({clave: valor})
                    print(f"\n REGLA {regla['id']} APLICADA: {regla['explicacion']}")
                    cambios = True
                    break
        return self.conclusiones

    def ejecutar_difuso(self, especie_candidata):
        """
        Se calcula la certeza de la especie encontrada cruzándola con sus atributos difusos en la base de conocimiento.
        """
        if not self.reglas_difusas or not especie_candidata:
            return

        print(f"\n Aplicando reglas difusas para validar certeza de: {especie_candidata}")
        
        # Buscar la regla difusa asociada a la especie
        regla_especie = next((r for r in self.reglas_difusas if r['especie'] == especie_candidata), None)
        
        if regla_especie:
            grados = []
            for attr, cat, umb in regla_especie['condiciones_difusas']:
                grado, _ = self.evaluar_condicion_difusa(attr, cat, umb)
                grados.append(grado)
                print(f"      → {attr} ({cat}): Grado de pertenencia = {grado}")
            
            if grados:
                # La certeza será el promedio de las membresías obtenidas (Lógica Difusa)
                promedio_membresia = sum(grados) / len(grados)
                # Se pondera el 60% peso de la clave proposicional exacta, 40% del ajuste difuso
                self.certeza_final = round(60 + (40 * promedio_membresia), 1)
                
            print(f"   ✓ Certeza final calculada: {self.certeza_final}%")

    def ejecutar(self):
        print("\n" + "=" * 60)
        print(" INICIANDO MOTOR DE INFERENCIA HÍBRIDO")
        print("=" * 60)
        
        # 1. Se obtiene la especie candidata de forma lógica
        self.ejecutar_proposicional()
        especie_candidata = self._buscar_especie_en_conclusiones()
        
        # 2. Si se encuentra, se aplica la lógica difusa para calcular el grado de certeza
        if especie_candidata:
            self.ejecutar_difuso(especie_candidata)

    def _buscar_especie_en_conclusiones(self):
        for conc in self.conclusiones:
            if 'especie' in conc:
                esp = conc['especie']
                if 'posible' not in esp.lower():
                    return esp
        return None

    def obtener_especie_con_certeza(self):
        especie = self._buscar_especie_en_conclusiones()
        return especie, self.certeza_final

    def obtener_todas_especies(self):
        especies = []
        for conc in self.conclusiones:
            if 'especie' in conc:
                especies.append(conc['especie'])
        return especies