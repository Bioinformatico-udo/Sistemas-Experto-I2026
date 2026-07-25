"""
Sistema de Ponderación Inteligente para Inferencia de Corales - FASE 2 (FINAL).
Compara tokens contra CARACTERÍSTICAS TAXONÓMICAS REALES del JSON.
Puntuación diferenciada: coincidencia EXACTA vs PARCIAL.
Ponderación de colores y formas insensible a acentos/diacríticos y plurales.
Unificado como único motor de ranking del sistema, con calibración de escala de tamaño.
"""

import json
import re
from pathlib import Path


def _norm_esp(w: str) -> str:
    """Normaliza texto eliminando acentos y singularizando plurales simples."""
    w = w.lower().strip()
    for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ü", "u")]:
        w = w.replace(a, b)
    if len(w) > 3 and w.endswith("s"):
        w = w[:-1]
    return w


class PonderadorCaracteristicas:

    PESOS = {
        "MICROESTRUCTURA": 2.0,
        "NOMBRE_CIENTIFICO": 2.0,
        "FORMA": 1.7,
        "TEXTURA": 1.5,
        "NOMBRE_COMUN": 1.2,
        "HABITAT": 0.7,
        "TAMANO": 0.5,
        "COLOR": 0.4,
        "GENERICO": 0.1,
    }

    LIMITES_CATEGORIA = {
        "NOMBRE_COMUN": 2.0, "COLOR": 2.5, "FORMA": 3.0,
        "TEXTURA": 3.0, "HABITAT": 2.0, "TAMANO": 1.0,
        "GENERICO": 0.5, "MICROESTRUCTURA": 4.0, "NOMBRE_CIENTIFICO": 4.0,
    }

    PESOS_COLOR = {
        "marron": 0.2, "cafe": 0.2, "gris": 0.2, "beige": 0.2,
        "crema": 0.2, "arena": 0.2,
        "verdoso": 0.3, "amarillento": 0.3, "blanquecino": 0.3,
        "blanco": 0.4, "amarillo": 0.4, "verde": 0.4,
        "anaranjado": 1.0, "naranja": 1.0,
        "rosado": 1.2, "rosa": 1.2,
        "azulado": 1.2, "negro": 0.8,
        "purpura": 1.5, "violeta": 1.5,
    }

    FORMAS_GENERALES = {"ramificada", "masiva", "laminar", "solitario", "incrustante", "columnar"}

    SINONIMOS_FORMA = {
        "ramificado": "ramificada", "ramas": "ramificada", "ramificacion": "ramificada",
        "arbusto": "ramificada", "arbustivo": "ramificada", "dedos": "ramificada",
        "candelabro": "ramificada", "tridente": "ramificada", "arbol": "ramificada",
        "cuerno": "ramificada", "ramita": "ramificada", "ramitas": "ramificada",
        "manojo": "ramificada", "ramillete": "ramificada", "flores": "ramificada",
        "ramo": "ramificada", "copita": "ramificada", "florecita": "ramificada",
        "masivo": "masiva", "masiva": "masiva", "domo": "masiva",
        "roca": "masiva", "piedra": "masiva", "redondo": "masiva",
        "bola": "masiva", "balon": "masiva", "monticulo": "masiva",
        "hemisferico": "masiva", "esfera": "masiva", "pelota": "masiva",
        "laminar": "laminar", "lamina": "laminar", "hoja": "laminar",
        "placa": "laminar", "plato": "laminar", "disco": "laminar",
        "laja": "laminar", "papel": "laminar", "tortilla": "laminar", "folioso": "laminar",
        "solitario": "solitario", "solo": "solitario", "unico": "solitario",
        "individual": "solitario", "aislado": "solitario",
        "incrustante": "incrustante", "incrustado": "incrustante",
        "costra": "incrustante", "pegado": "incrustante",
        "columnar": "columnar", "columna": "columnar", "pilar": "columnar", "pilares": "columnar",
        "abanico": "abanico", "paleta": "abanico", "paletas": "abanico",
        "cilindricas": "cilindrica", "cilindrica": "cilindrica", "cilindrico": "cilindrica",
        "fusionadas": "fusionada", "fusionada": "fusionada", "fusionado": "fusionada",
        "finas": "fina", "fina": "fina", "delicadas": "fina", "delicada": "fina", "fino": "fina",
        "aplanado": "aplanado", "aplanada": "aplanado",
        "irregular": "irregular",
        "vertical": "vertical",
        "nodular": "nodular",
        "bifacial": "bifacial", "transparente": "bifacial",
        # Nuevos sinónimos (femeninos, coloquiales, biólogo)
        "coliflor": "nodular",
        "bifurcan": "ramificada",
        "bifurcada": "ramificada",
        "bifurcado": "ramificada",
        "pegada": "incrustante",
        "enorme": "masiva",
        "espagueti": "ramificada",
        "tieso": "ramificada",
        "hilo": "ramificada",
        "lechuga": "bifacial",
        "delgada": "fina",
        "delgado": "fina",
        "fragil": "irregular",
        "hemisferica": "masiva",
    }

    SINONIMOS_TEXTURA = {
        "valles": "valles", "surcos": "valles", "cerebro": "valles", "cerebros": "valles",
        "cerebroide": "valles", "laberinto": "valles", "canales": "valles",
        "grietas": "valles", "meandros": "valles", "sinuoso": "valles", "surco": "valles",
        "copas": "copas", "hoyitos": "copas", "huecos": "copas", "hueco": "copas",
        "poros": "copas", "poro": "copas", "agujeros": "copas", "agujero": "copas",
        "panal": "copas", "colmena": "copas", "celdas": "copas", "celda": "copas",
        "hoyuelos": "copas", "hoyuelo": "copas", "puntitos": "copas", "huequitos": "copas",
        "enrejado": "copas", "esponjoso": "copas",
        "liso": "lisa", "lisa": "lisa", "uniforme": "lisa", "suave": "lisa",
        # Nuevos sinónimos textura
        "estrellita": "copas",
        "meandroide": "valles",
    }

    SINONIMOS_MICROESTRUCTURA = {
        "en cada punta": "coralitos_en_puntas",
        "en las puntas": "coralitos_en_puntas",
        "solo en puntas": "coralitos_en_puntas",
        "copita blanca": "coralitos_en_puntas",
    }

    SINONIMOS_COLOR = {
        "rosado": "rosado_anaranjado", "rosa": "rosado_anaranjado",
        "anaranjado": "rosado_anaranjado", "naranja": "rosado_anaranjado",
        "purpura": "purpura", "violeta": "purpura",
        "marron": "marron", "cafe": "marron",
        "gris": "grisaceo", "grisaceo": "grisaceo",
        "amarillento": "amarillo", "amarillo": "amarillo",
        "verdoso": "verde", "verde": "verde",
        "blanco": "blanco",
        # Variantes femeninas
        "rosada": "rosado_anaranjado",
        "anaranjada": "rosado_anaranjado",
        "grisacea": "grisaceo",
    }

    REEMPLAZOS_COLOQUIALES = {
        "dedos largos": "cilindrica",
        "dedo largo": "cilindrica",
        "arbusto sin hojas": "ramificada",
        "arbusto sin hoja": "ramificada",
        "huequitos por debajo": "bifacial",
        "huequito por debajo": "bifacial",
        "de los dos lados": "bifacial",
        "dos lados": "bifacial",
        "ambos lados": "bifacial",
        "de ambas caras": "bifacial",
        "ambas caras": "bifacial",
    }

    PALABRAS_HABITAT = [
        "cuevas", "oquedades", "profundo", "profunda", "someras", "someros",
        "oleaje", "arrecife", "barrera", "franjeante", "arena", "arenoso",
        "rocoso", "pared", "techo", "bajo", "alto",
    ]

    STOP_WORDS = {
        "en", "de", "del", "por", "para", "como", "un", "una", "unos", "unas",
        "el", "la", "los", "las", "su", "sus", "muy", "bastante", "algo",
        "poco", "mucho", "que", "con", "y", "pero", "es", "fue", "era",
        "son", "eran", "estaba", "estaban", "tiene", "tenia", "habia",
        "a", "e", "o", "se", "le", "les", "lo", "me", "nos", "te",
        "hermoso", "bonito", "interesante", "lindo", "bello", "precioso",
        "vi", "encontre", "observe", "parece", "parecia", "dijo", "dice",
        "asi", "entonces", "luego", "despues", "tambien", "ademas",
        "esto", "esta", "este", "aquel", "aquella", "alli", "aqui",
        "lleno", "cada", "solo", "forma", "color", "coloracion", "tono",
        "tonalidad", "parece", "parecia", "lado", "claro",
    }

    PALABRAS_GENERICAS = {"coral", "corales"}

    def __init__(self):
        self.especies = []
        self._cargar_especies()
        self.PESOS_COLOR = {_norm_esp(k): v for k, v in self.PESOS_COLOR.items()}
        self.SINONIMOS_FORMA = {_norm_esp(k): v for k, v in self.SINONIMOS_FORMA.items()}
        self.SINONIMOS_TEXTURA = {_norm_esp(k): v for k, v in self.SINONIMOS_TEXTURA.items()}
        self.SINONIMOS_COLOR = {_norm_esp(k): v for k, v in self.SINONIMOS_COLOR.items()}
        self.PALABRAS_HABITAT = [_norm_esp(h) for h in self.PALABRAS_HABITAT]

    def _cargar_especies(self):
        rutas = [
            Path(__file__).parent.parent / "data" / "especies.json",
            Path("data/especies.json"),
            Path("../data/especies.json")
        ]
        for ruta in rutas:
            if ruta.exists():
                try:
                    with open(ruta, "r", encoding="utf-8") as f:
                        self.especies = json.load(f)
                    return
                except Exception as e:
                    print(f"Error al cargar especies desde {ruta}: {e}")
        self.especies = []

    def _get_peso_color(self, color: str) -> float:
        color_base = self.SINONIMOS_COLOR.get(color, color)
        return self.PESOS_COLOR.get(color, self.PESOS_COLOR.get(color_base, self.PESOS["COLOR"]))

    def determinar_escala_tamano(self, tokens: list) -> str:
        escala_pequena = {"mini", "diminuto", "pequeno", "chico", "chiquito", "delgado", "delgada", "fino", "fina", "finito", "finita"}
        escala_grande = {"grande", "enorme", "gigante", "grueso", "gruesa", "ancho", "ancha", "masivo", "masiva", "enormes", "gigantes"}
        for t in tokens:
            if t in escala_pequena:
                return "PEQUENO"
            if t in escala_grande:
                return "GRANDE"
        return None

    def evaluar_medida_escala(self, escala: str, caract: dict) -> float:
        if not escala:
            return 0.0
            
        score = 0.0
        
        # 1. Analizar copas_diametro
        copas_dia = caract.get("copas_diametro", "")
        if copas_dia:
            if escala == "PEQUENO" and "menor" in copas_dia:
                score += 0.3
            elif escala == "GRANDE" and "mayor" in copas_dia:
                score += 0.3
                
        # 2. Analizar ramas_diametro
        ramas_dia = caract.get("ramas_diametro", "")
        if ramas_dia:
            if escala == "PEQUENO" and "menor" in ramas_dia:
                score += 0.3
            elif escala == "GRANDE" and "mayor" in ramas_dia:
                score += 0.3
                
        # 3. Analizar colinas_distanciadas
        colinas_dist = caract.get("colinas_distanciadas", "")
        if colinas_dist:
            if escala == "PEQUENO" and "2-4" in colinas_dist:
                score += 0.2
            elif escala == "GRANDE" and "mayor" in colinas_dist:
                score += 0.2
                
        # 4. Analizar coralitos_medida
        coralitos_med = caract.get("coralitos_medida", "")
        if coralitos_med:
            match = re.findall(r"([0-9.]+)", coralitos_med)
            if match:
                try:
                    vals = [float(v) for v in match]
                    promedio = sum(vals) / len(vals)
                    if escala == "PEQUENO" and promedio < 3.0:
                        score += 0.3
                    elif escala == "GRANDE" and promedio >= 3.0:
                        score += 0.3
                except ValueError:
                    pass
                    
        # 5. Relacionar con la forma de la colonia
        forma = caract.get("forma", "")
        if forma:
            if escala == "PEQUENO" and any(x in forma for x in ["solitario", "fina"]):
                score += 0.2
            elif escala == "GRANDE" and any(x in forma for x in ["masiva", "columnar"]):
                score += 0.2
                
        return score

    def _tokenizar(self, texto: str) -> list:
        texto = texto.lower().strip()
        for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ü", "u")]:
            texto = texto.replace(a, b)
        for frase, rep in self.REEMPLAZOS_COLOQUIALES.items():
            texto = texto.replace(frase, rep)
        texto = re.sub(r'[.,;:!?¿¡()"»«\'\"]+', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        palabras = texto.split()
        return [_norm_esp(p) for p in palabras if _norm_esp(p) not in self.STOP_WORDS and len(p) > 1]

    def _evaluar_token(self, token: str) -> dict:
        categorias = {}
        token_lower = token.lower().strip()

        for especie in self.especies:
            nombre_cientifico = _norm_esp(especie.get("nombre_cientifico", ""))
            if token_lower in [p for p in nombre_cientifico.split() if len(p) > 3]:
                categorias["NOMBRE_CIENTIFICO"] = self.PESOS["NOMBRE_CIENTIFICO"]
                break

        if token_lower not in self.PALABRAS_GENERICAS:
            for especie in self.especies:
                nombre_comun = _norm_esp(especie.get("nombre_comun", ""))
                if token_lower in [p for p in nombre_comun.split() if len(p) > 3]:
                    categorias["NOMBRE_COMUN"] = self.PESOS["NOMBRE_COMUN"]
                    break

        if token_lower in self.SINONIMOS_FORMA:
            categorias["FORMA"] = self.PESOS["FORMA"]

        if token_lower in self.SINONIMOS_TEXTURA:
            categorias["TEXTURA"] = self.PESOS["TEXTURA"]

        # Microestructura (frases compuestas)
        for frase, valor in self.SINONIMOS_MICROESTRUCTURA.items():
            if frase in token_lower or token_lower in frase:
                categorias["MICROESTRUCTURA"] = self.PESOS["MICROESTRUCTURA"]
                break

        # Evaluación de Color (corregido bug comprobando también SINONIMOS_COLOR)
        if token_lower in self.PESOS_COLOR or token_lower in self.SINONIMOS_COLOR:
            categorias["COLOR"] = self._get_peso_color(token_lower)

        if token_lower in self.PALABRAS_HABITAT:
            categorias["HABITAT"] = self.PESOS["HABITAT"]

        # Clasificación de Escala / Tamaño
        escala = self.determinar_escala_tamano([token_lower])
        if escala:
            categorias["TAMANO"] = self.PESOS["TAMANO"]

        if not categorias:
            categorias["GENERICO"] = self.PESOS["GENERICO"]

        return categorias

    def evaluar_texto(self, texto: str) -> dict:
        tokens = self._tokenizar(texto)
        if not tokens:
            return {"evidencias_por_categoria": {}, "peso_total": 0.0, "tokens_evaluados": 0, "tokens": []}

        categorias_acumuladas = {}
        for token in tokens:
            resultados = self._evaluar_token(token)
            for categoria, peso in resultados.items():
                categorias_acumuladas[categoria] = categorias_acumuladas.get(categoria, 0.0) + peso

        for categoria in categorias_acumuladas:
            limite = self.LIMITES_CATEGORIA.get(categoria, 10.0)
            categorias_acumuladas[categoria] = min(categorias_acumuladas[categoria], limite)

        factor_normalizacion = max(1, len(tokens) * 0.5)
        peso_total = sum(categorias_acumuladas.values()) / factor_normalizacion

        return {
            "evidencias_por_categoria": categorias_acumuladas,
            "peso_total": round(peso_total, 2),
            "tokens_evaluados": len(tokens),
            "tokens": tokens,
        }

    def puntuar_especies(self, evidencias: dict, max_resultados: int = 41) -> list:
        categorias = evidencias.get("evidencias_por_categoria", {})
        tokens = evidencias.get("tokens", [])
        scores = []

        for especie in self.especies:
            score = 0.0
            nombre_cientifico = _norm_esp(especie.get("nombre_cientifico", ""))
            nombre_comun = _norm_esp(especie.get("nombre_comun", ""))
            habitat_especie = _norm_esp(especie.get("habitat", ""))
            tipo_especie = _norm_esp(especie.get("tipo", ""))
            caract = especie.get("caracteristicas", {})

            # Cruce de Tipo de Coral (Hidrocoral vs Escleractinio)
            for token in tokens:
                if token in tipo_especie:
                    score += 0.20

            for categoria, peso_acumulado in categorias.items():
                if peso_acumulado <= 0:
                    continue

                if categoria == "NOMBRE_CIENTIFICO":
                    for token in tokens:
                        if len(token) > 3 and token in nombre_cientifico:
                            score += peso_acumulado * 0.20

                elif categoria == "NOMBRE_COMUN":
                    for token in tokens:
                        if len(token) > 3 and token in nombre_comun:
                            score += peso_acumulado * 0.10

                elif categoria == "FORMA":
                    forma_especie = _norm_esp(caract.get("forma", ""))
                    for token in tokens:
                        forma_token = self.SINONIMOS_FORMA.get(token, "")
                        if forma_token:
                            if forma_token in self.FORMAS_GENERALES:
                                if forma_token in forma_especie:
                                    score += peso_acumulado * 0.08
                            else:
                                partes = forma_especie.split("_")
                                if forma_token in partes:
                                    score += peso_acumulado * 0.20

                elif categoria == "TEXTURA":
                    # Recopilar todos los campos relacionados con textura de características
                    superficie_especie = ""
                    for k, v in caract.items():
                        if any(x in k for x in ["superficie", "copa", "valle", "surco"]):
                            superficie_especie += " " + str(k) + " " + str(v)
                    superficie_especie = _norm_esp(superficie_especie)
                    for token in tokens:
                        textura_token = self.SINONIMOS_TEXTURA.get(token, "")
                        if textura_token and textura_token in superficie_especie:
                            score += peso_acumulado * 0.15

                elif categoria == "COLOR":
                    color_especie = _norm_esp(str(caract.get("color", "")))
                    for token in tokens:
                        color_token = self.SINONIMOS_COLOR.get(token, "")
                        if color_token and color_token in color_especie:
                            score += peso_acumulado * 0.15

                elif categoria == "MICROESTRUCTURA":
                    coralitos_en = _norm_esp(caract.get("coralitos_en", ""))
                    for token in tokens:
                        if token in coralitos_en:
                            score += peso_acumulado * 0.20

                elif categoria == "HABITAT":
                    for token in tokens:
                        if token in habitat_especie:
                            score += peso_acumulado * 0.05

                elif categoria == "TAMANO":
                    escala = self.determinar_escala_tamano(tokens)
                    if escala:
                        score += peso_acumulado * self.evaluar_medida_escala(escala, caract)

                elif categoria == "GENERICO":
                    score += peso_acumulado * 0.005

            scores.append({
                "id": especie.get("id"),
                "nombre_cientifico": especie.get("nombre_cientifico"),
                "nombre_comun": especie.get("nombre_comun"),
                "familia": especie.get("familia"),
                "score": round(score, 4),
            })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:max_resultados]

    def diagnosticar(self, texto: str) -> dict:
        evidencias = self.evaluar_texto(texto)
        especies = self.puntuar_especies(evidencias, max_resultados=5)
        score_top = especies[0]["score"] if especies else 0.0

        if especies and score_top > 0.4:
            confianza = "ALTA"
        elif especies and score_top > 0.15:
            confianza = "MEDIA"
        else:
            confianza = "BAJA"

        return {"texto": texto, "evidencias": evidencias, "top_especies": especies[:5], "confianza": confianza}


if __name__ == "__main__":
    ponderador = PonderadorCaracteristicas()
    textos = [
        "coral rosa",
        "coral marron",
        "manojo de dedos largos y flacos, arbusto sin hojas, cafe",
        "roca redonda con huecos como panal de abejas, verdoso",
        "plato hondo aplastado, finito, huequitos por debajo, transparente",
        "ramillete de flores, copita blanca en cada punta, profundo",
    ]
    for texto in textos:
        print(f"\n{'='*60}")
        print(f"TEXTO: {texto}")
        print(f"{'='*60}")
        r = ponderador.evaluar_texto(texto)
        print(f"\nTokens: {r['tokens']}")
        print(f"Categorías:")
        for cat, peso in sorted(r['evidencias_por_categoria'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:25s}: {peso:.2f}")
        especies = ponderador.puntuar_especies(r, max_resultados=3)
        print(f"\nTop 3:")
        for i, esp in enumerate(especies):
            print(f"  {i+1}. {esp['nombre_cientifico']} ({esp['nombre_comun']}) - {esp['score']:.4f}")