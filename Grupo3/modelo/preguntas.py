PREGUNTAS = [
    {
        "id": "pleopodosPrimerSomito",
        "texto": "¿Existen apéndices PAREADOS en el PRIMER somito abdominal?",
        "explicacion": (
            "En las hembras: ¿hay pleópodos en el 1er segmento abdominal?\n"
            "En los machos: ¿hay pleópodos en el 1er Y 2do segmento abdominal?\n\n"
            "→ SI: género Paguristes\n"
            "→ NO: resto de géneros"
        ),
        "imagenDesc": "Abdomen vista ventral — buscar apéndices en 1er somito",
        "opciones": [("Sí, hay apéndices pareados", True), ("No hay apéndices en 1er somito", False)],
        "aplicaCuando": lambda obs: True,
    },
    {
        "id": "flageloSetasLargas",
        "texto": "¿Las setas del flagelo antenal miden MÁS de 6 veces la longitud de un artejo del flagelo?",
        "explicacion": (
            "Observe el flagelo antenal bajo lupa.\n"
            "→ Setas largas (> 6× artejo): Paguristes angustitheca\n"
            "→ Setas cortas (≤ 1× artejo): Paguristes perplexus"
        ),
        "imagenDesc": "Flagelo antenal — comparar longitud de setas vs artejo",
        "opciones": [("Sí, setas muy largas (> 6× artejo)", True), ("No, setas cortas (≈ 1 artejo o menos)", False)],
        "aplicaCuando": lambda obs: obs.get("pleopodosPrimerSomito") is True,
    },
    {
        "id": "quelipedosIguales",
        "texto": "¿Los quelípedos son IGUALES o SUBIGUALES (aproximadamente del mismo tamaño)?",
        "explicacion": (
            "Compare el tamaño de ambos quelípedos:\n"
            "→ Iguales/subiguales: Isocheles, Clibanarius spp.\n"
            "→ Desiguales: Petrochirus (der. mayor), Calcinus, Dardanus (izq. mayor)"
        ),
        "imagenDesc": "Vista frontal de quelípedos — comparar longitud total",
        "opciones": [("Sí, son aproximadamente iguales", True), ("No, son claramente desiguales", False)],
        "aplicaCuando": lambda obs: obs.get("pleopodosPrimerSomito") is False,
    },
    {
        "id": "dedosCuchara",
        "texto": "¿El ápice de los dedos de los quelípedos tiene forma de CUCHARA (extremo en espátula)?",
        "explicacion": (
            "Vista del extremo distal de los dedos del quelípedo:\n"
            "→ Ápice en cuchara/espátula: géneros Clibanarius (y Paguristes)\n"
            "→ Ápice aguzado o con forma diferente: Isocheles (aguzado)"
        ),
        "imagenDesc": "Extremo distal de los dedos del quelípedo",
        "opciones": [("Sí, ápice en forma de cuchara", True), ("No, ápice aguzado o diferente", False)],
        "aplicaCuando": lambda obs: obs.get("quelipedosIguales") is True,
    },
    {
        "id": "caparazonReticulado",
        "texto": "¿El caparazón posterior presenta celdas calcificadas con apariencia RETICULADA?",
        "explicacion": (
            "Observe el abdomen (caparazón posterior):\n"
            "→ Reticulado / mosaico calcificado: Isocheles wurdemanni (DIAGNÓSTICO)\n"
            "→ Sin celdas calcificadas: otros géneros"
        ),
        "imagenDesc": "Caparazón posterior (abdomen) — buscar patrón reticulado",
        "opciones": [("Sí, reticulado con celdas calcificadas", True), ("No, sin apariencia reticulada", False)],
        "aplicaCuando": lambda obs: obs.get("quelipedosIguales") is True and obs.get("dedosCuchara") is False,
    },
    {
        "id": "dactiloMayorPropodo",
        "texto": "¿El DACTILO del 1er y 2do par de patas caminadoras es MÁS LARGO que el propodo?",
        "explicacion": (
            "Mida el dactilo vs. propodo en el 1er o 2do par de patas caminadoras:\n"
            "→ Dactilo > propodo: Clibanarius cubensis\n"
            "→ Dactilo < propodo: C. antillensis o C. tricolor"
        ),
        "imagenDesc": "Patas caminadoras 1° y 2° par — comparar dactilo vs propodo",
        "opciones": [("Sí, dactilo más largo que el propodo", True), ("No, dactilo más corto que el propodo", False)],
        "aplicaCuando": lambda obs: obs.get("quelipedosIguales") is True and obs.get("dedosCuchara") is True,
    },
    {
        "id": "bandasTransversasRojas",
        "texto": "¿Las patas caminadoras presentan BANDAS TRANSVERSAS y lunares de color ROJO?",
        "explicacion": (
            "Observe el patrón de coloración en las patas caminadoras:\n"
            "→ Bandas TRANSVERSAS rojas + lunares: Clibanarius tricolor\n"
            "→ Bandas LONGITUDINALES claras (no rojas transversas): C. antillensis"
        ),
        "imagenDesc": "Patrón cromático de patas caminadoras — bandas transversas vs. longitudinales",
        "opciones": [("Sí, bandas transversas rojas + lunares", True), ("No, bandas longitudinales claras", False)],
        "aplicaCuando": lambda obs: obs.get("dactiloMayorPropodo") is False and obs.get("dedosCuchara") is True,
    },
    {
        "id": "quelipedoDerechoLigeramenteMayor",
        "texto": "¿El quelípedo DERECHO es ligeramente más grande que el izquierdo?",
        "explicacion": (
            "Compare tamaño de quelípedos cuando son desiguales:\n"
            "→ DERECHO ligeramente mayor: Petrochirus diogenes\n"
            "→ IZQUIERDO mucho mayor: Calcinus tibicen o Dardanus fucosus"
        ),
        "imagenDesc": "Quelípedos — determinar cuál es el mayor",
        "opciones": [("Sí, el quelípedo DERECHO es ligeramente mayor", True), ("No, el IZQUIERDO es mucho mayor", False)],
        "aplicaCuando": lambda obs: obs.get("quelipedosIguales") is False,
    },
    {
        "id": "quelipedoLiso",
        "texto": "¿El quelípedo izquierdo (mayor) es LISO, sin setas en su superficie exterior?",
        "explicacion": (
            "Observe la superficie del quelípedo izquierdo (el mayor):\n"
            "→ LISO (sin setas, salvo interior de dedos) + ápice calcáreo: Calcinus tibicen\n"
            "→ Con HACES DE SETAS en la palma + ápice córneo: Dardanus fucosus"
        ),
        "imagenDesc": "Superficie del quelípedo izquierdo — setas y ápice de los dedos",
        "opciones": [("Sí, liso, sin setas en superficie exterior", True), ("No, con haces de setas en la palma", False)],
        "aplicaCuando": lambda obs: obs.get("quelipedoDerechoLigeramenteMayor") is False and obs.get("quelipedosIguales") is False,
    },
]

PREGUNTAS_POR_ID = {p["id"]: p for p in PREGUNTAS}
