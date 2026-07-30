from modelo.especies import obtenerTodasLasEspecies
from modelo.preguntas import PREGUNTAS


class MotorInferencia:
    """Motor de inferencia por encadenamiento hacia adelante.

    Mantiene una memoria de trabajo (self.observaciones) con los hechos
    aportados por el usuario y, en cada ciclo, dispara la primera regla
    (pregunta) cuya precondicion se satisface. Al agotarse las reglas
    aplicables, calcula un factor de certeza (FC) por especie.
    """

    def __init__(self):
        self.observaciones = {}
        self.ordenRespuestas = []
        self.preguntas = PREGUNTAS

    def reset(self):
        self.observaciones = {}
        self.ordenRespuestas = []

    def siguientePregunta(self):
        for p in self.preguntas:
            if p["id"] not in self.observaciones:
                if p["aplicaCuando"](self.observaciones):
                    return p
        return None

    def registrarRespuesta(self, preguntaId, valor):
        if preguntaId not in self.observaciones:
            self.ordenRespuestas.append(preguntaId)
        self.observaciones[preguntaId] = valor

    def deshacerUltimaRespuesta(self):
        if not self.ordenRespuestas:
            return None
        ultimoId = self.ordenRespuestas.pop()
        if ultimoId in self.observaciones:
            del self.observaciones[ultimoId]
        return ultimoId

    def inferir(self):
        """Devuelve [(nombre, fc, datos), ...] ordenado de mayor a menor FC."""
        especies = obtenerTodasLasEspecies()
        resultados = []
        for nombre, datos in especies.items():
            fc = self._calcularFc(datos.get("caracteres", {}))
            if fc > 0:
                resultados.append((nombre, fc, datos))
        resultados.sort(key=lambda x: (-x[1], x[0]))
        return resultados

    def _calcularFc(self, caracteresEspecie):
        """FC = % de caracteres OBSERVADOS que coinciden con la especie.

        El denominador son unicamente los caracteres que el usuario ya
        respondio y que la especie declara (caracteres comparables). Asi,
        una especie totalmente consistente con las observaciones obtiene
        100 y el resultado no depende de cuantos caracteres declare la
        ficha de cada especie.
        """
        comparables = 0
        coincidencias = 0
        for clave, valorObservado in self.observaciones.items():
            if clave in caracteresEspecie:
                comparables += 1
                if caracteresEspecie[clave] == valorObservado:
                    coincidencias += 1
        if comparables == 0:
            return 0
        return round((coincidencias / comparables) * 100)

    def conflictos(self, caracteresEspecie):
        """Caracteres observados que CONTRADICEN a la especie (para explicar)."""
        return [
            clave
            for clave, valorObservado in self.observaciones.items()
            if clave in caracteresEspecie and caracteresEspecie[clave] != valorObservado
        ]

    def diagnosticoCompleto(self):
        return self.siguientePregunta() is None
