# ------------------------------------------------------------
# Diccionario de opciones para preguntas con múltiples respuestas
# ------------------------------------------------------------

PREGUNTAS_OPCIONES = {
    # Pregunta inicial para confirmar que es Porcellanidae
    'confirmacion_porcellanidae': ['si', 'no'],
    
    # Atributos de la clave dicotómica
    'artejo_basal_antena': ['corto', 'avanzado'],
    'paredes_posteriores': ['ausentes', 'enteras', 'placas'],
    'paredes_laterales': ['incompletas', 'completas'],
    'quelipedos_superficie': ['granulos_tuberculos', 'lisa'],
    'quelipedos_tuberculos_conicos': ['si', 'no'],
    'quelipedos_forma': ['aplanados_subiguales', 'gruesos_desiguales'],
    'frente_vista_dorsal': ['trilobulada', 'sinuosa', 'recta', 'convexa'],
    'telson_piezas': ['5', '7'],
    'carpo_quelipedos': ['entero', 'dientes_lobulos'],
    'espina_epibranquial': ['presente', 'ausente'],
    'margen_flexor_carpo': ['tres_subiguales', 'tres_cuatro_unidos', 'tres_separados', 'cuatro_separados'],
    'caparazon_textura': ['aspero', 'liso'],
    'flagelo_rudimentario': ['si', 'no'],
    'relacion_largo_ancho': ['1.3', 'menos_1.3'],
    'frente_estructura': ['tridentada', 'trilobulada', 'inclinada', 'recta'],
    'margenes_laterales_espinulas': ['si', 'no'],
    'dedos_torcidos': ['si', 'no'],
    'lobulo_proximal_carpo': ['si', 'no'],
    'caparazon_erosionado': ['si', 'no'],
    'setas_abundantes': ['si', 'no'],
    'frente_diente_lobuliforme': ['si', 'no'],
    'mero_tercer_pata_inflado': ['si', 'no'],
    'espina_supraorbital': ['si', 'no'],
    'carpo_liso': ['si', 'no'],
    'pubescencia_fina': ['si', 'no'],
}

# ------------------------------------------------------------
# Diccionario de preguntas (texto amigable para el usuario)
# ------------------------------------------------------------
PREGUNTAS = {
    'confirmacion_porcellanidae': '¿El espécimen pertenece a la familia PORCELLANIDAE? (cangrejos porcelánidos, abdomen simétrico, cuarto par de patas con pinza)',
    'artejo_basal_antena': '¿El artejo basal de la antena es CORTO o AVANZADO? (corto/avanzado)',
    'paredes_posteriores': 'Las porciones posteriores de la pared del caparazón son: ¿AUSENTES, ENTERAS o PLACAS? (ausentes/enteras/placas)',
    'paredes_laterales': '¿Las paredes laterales del caparazón son INCOMPLETAS o COMPLETAS? (incompletas/completas)',
    'quelipedos_superficie': 'La superficie dorsal de los quelípedos es: ¿LISA o tiene GRÁNULOS/TUBÉRCULOS? (lisa/granulos_tuberculos)',
    'quelipedos_tuberculos_conicos': '¿Los quelípedos tienen TUBÉRCULOS CÓNICOS? (si/no)',
    'quelipedos_forma': 'Los quelípedos son: ¿APLANADOS SUBIGUALES o GRUESOS DESIGUALES? (aplanados_subiguales/gruesos_desiguales)',
    'frente_vista_dorsal': 'La frente en vista dorsal es: ¿TRILOBULADA, SINUOSA, RECTA o CONVEXA? (trilobulada/sinuosa/recta/convexa)',
    'telson_piezas': '¿Cuántas piezas tiene el telson? (5/7)',
    'carpo_quelipedos': 'El carpo de los quelípedos es: ¿ENTERO o tiene DIENTES/LÓBULOS? (entero/dientes_lobulos)',
    'espina_epibranquial': '¿Presenta ESPINA en la región epibranquial? (presente/ausente)',
    'margen_flexor_carpo': 'El margen flexor del carpo tiene: ¿3 SUBIGUALES, 3-4 UNIDOS, 3 SEPARADOS o 4 SEPARADOS? (tres_subiguales/tres_cuatro_unidos/tres_separados/cuatro_separados)',
    'caparazon_textura': 'La superficie del caparazón es: ¿ÁSPERA o LISA? (aspero/liso)',
    'flagelo_rudimentario': '¿Los artejos móviles de la antena son muy pequeños y el flagelo rudimentario? (si/no)',
    'relacion_largo_ancho': 'El caparazón es: ¿1.3 VECES más largo que ancho, o MENOS? (1.3/menos_1.3)',
    'frente_estructura': 'La frente es: ¿TRIDENTADA, TRILOBULADA, INCLINADA o RECTA? (tridentada/trilobulada/inclinada/recta)',
    'margenes_laterales_espinulas': '¿Los márgenes laterales tienen ESPÍNULAS posteriores al ángulo epibranquial? (si/no)',
    'dedos_torcidos': '¿Los dedos de los quelípedos están TORCIDOS? (si/no)',
    'lobulo_proximal_carpo': '¿El margen flexor del carpo tiene LÓBULO PROXIMAL? (si/no)',
    'caparazon_erosionado': '¿El caparazón y quelípedos están EROSIONADOS? (si/no)',
    'setas_abundantes': '¿El caparazón y quelípedos tienen SETAS ABUNDANTES? (si/no)',
    'frente_diente_lobuliforme': '¿La frente tiene DIENTE LOBULIFORME en los ángulos orbitales? (si/no)',
    'mero_tercer_pata_inflado': '¿El mero del tercer par de patas está INFLADO? (si/no)',
    'espina_supraorbital': '¿Presenta ESPINA SUPRAORBITAL? (si/no)',
    'carpo_liso': '¿El carpo de los quelípedos es LISO? (si/no)',
    'pubescencia_fina': '¿El caparazón tiene FINA PUBESCENCIA? (si/no)',
}

# ------------------------------------------------------------
# REGLAS PROPOSICIONALES - CLAVE DICOTÓMICA
# ------------------------------------------------------------
REGLAS_PROPOSICIONALES = [

    # ===================== REGLA INICIAL =====================
    {
        'id': 'R000',
        'condiciones': [('confirmacion_porcellanidae', 'si')],
        'conclusion': {
            'reino': 'Animalia',
            'phylum': 'Arthropoda',
            'orden': 'Decapoda',
            'familia': 'Porcellanidae'
        },
        'explicacion': 'Confirmación: el espécimen pertenece a la familia Porcellanidae.'
    },

    # ===================== PASO 1: ARTEJO BASAL =====================
    {
        'id': 'R101',
        'condiciones': [('familia', 'Porcellanidae'), ('artejo_basal_antena', 'corto')],
        'conclusion': {'clave_grupo': 'grupo_2'},
        'explicacion': 'Artejo basal corto → segmentos móviles con acceso a la órbita → grupo 2'
    },
    {
        'id': 'R102',
        'condiciones': [('familia', 'Porcellanidae'), ('artejo_basal_antena', 'avanzado')],
        'conclusion': {'clave_grupo': 'grupo_17'},
        'explicacion': 'Artejo basal avanzado → segmentos móviles sin acceso a la órbita → grupo 17'
    },

    # ===================== PASO 2: PAREDES POSTERIORES =====================
    {
        'id': 'R103',
        'condiciones': [('clave_grupo', 'grupo_2'), ('paredes_posteriores', 'ausentes')],
        'conclusion': {'clave_subgrupo': 'subgrupo_3'},
        'explicacion': 'Paredes posteriores ausentes o con placas → paso 3'
    },
    {
        'id': 'R104',
        'condiciones': [('clave_grupo', 'grupo_2'), ('paredes_posteriores', 'enteras')],
        'conclusion': {'genero': 'Petrolisthes', 'clave_subgrupo': 'subgrupo_10'},
        'explicacion': 'Paredes posteriores enteras → género Petrolisthes'
    },

    # ===================== PASO 3: PAREDES LATERALES =====================
    {
        'id': 'R105',
        'condiciones': [('clave_subgrupo', 'subgrupo_3'), ('paredes_laterales', 'incompletas')],
        'conclusion': {'genero': 'Neopisosoma', 'clave_subgrupo': 'subgrupo_4'},
        'explicacion': 'Paredes laterales incompletas → género Neopisosoma'
    },
    {
        'id': 'R106',
        'condiciones': [('clave_subgrupo', 'subgrupo_3'), ('paredes_laterales', 'completas')],
        'conclusion': {'clave_subgrupo': 'subgrupo_6'},
        'explicacion': 'Paredes laterales con placas → paso 6'
    },

    # ===================== PASO 4/5: NEOPISOSOMA =====================
    {
        'id': 'R107',
        'condiciones': [('genero', 'Neopisosoma'), ('quelipedos_superficie', 'lisa')],
        'conclusion': {'especie': 'Neopisosoma cf. neglectum'},
        'explicacion': 'Quelípedos lisos sin gránulos → Neopisosoma cf. neglectum'
    },
    {
        'id': 'R108',
        'condiciones': [('genero', 'Neopisosoma'), ('quelipedos_superficie', 'granulos_tuberculos')],
        'conclusion': {'clave_subgrupo': 'subgrupo_5'},
        'explicacion': 'Quelípedos con gránulos/tubérculos → paso 5'
    },
    {
        'id': 'R109',
        'condiciones': [('clave_subgrupo', 'subgrupo_5'), ('quelipedos_tuberculos_conicos', 'si')],
        'conclusion': {'especie': 'Neopisosoma angustifrons', 'genero': 'Neopisosoma'},
        'explicacion': 'Gránulos + tubérculos cónicos, setas escasas → Neopisosoma angustifrons'
    },
    {
        'id': 'R110',
        'condiciones': [('clave_subgrupo', 'subgrupo_5'), ('quelipedos_tuberculos_conicos', 'no')],
        'conclusion': {'especie': 'Neopisosoma orientale', 'genero': 'Neopisosoma'},
        'explicacion': 'Gránulos uniformes, setas dispersas en palma → Neopisosoma orientale'
    },

    # ===================== PASO 6: CLASTOTOECHUS vs PACHYCHELES =====================
    {
        'id': 'R111',
        'condiciones': [
            ('clave_subgrupo', 'subgrupo_6'),
            ('quelipedos_forma', 'aplanados_subiguales'),
            ('frente_vista_dorsal', 'trilobulada'),
            ('telson_piezas', '5')
        ],
        'conclusion': {'especie': 'Clastotoechus nodosus', 'genero': 'Clastotoechus'},
        'explicacion': 'Quelípedos aplanados, frente trilobulada, telson 5 → Clastotoechus nodosus'
    },
    {
        'id': 'R112',
        'condiciones': [('clave_subgrupo', 'subgrupo_6'), ('quelipedos_forma', 'gruesos_desiguales')],
        'conclusion': {'genero': 'Pachycheles', 'clave_subgrupo': 'subgrupo_7'},
        'explicacion': 'Quelípedos gruesos y desiguales → género Pachycheles'
    },

    # ===================== PASO 7/8/9: PACHYCHELES =====================
    {
        'id': 'R113',
        'condiciones': [('genero', 'Pachycheles'), ('telson_piezas', '7')],
        'conclusion': {'especie': 'Pachycheles serratus', 'genero': 'Pachycheles'},
        'explicacion': 'Telson 7 piezas → Pachycheles serratus'
    },
    {
        'id': 'R114',
        'condiciones': [('genero', 'Pachycheles'), ('telson_piezas', '5'), ('frente_vista_dorsal', 'convexa')],
        'conclusion': {'especie': 'Pachycheles monilifer', 'genero': 'Pachycheles'},
        'explicacion': 'Telson 5, frente convexa con porción media avanzada → Pachycheles monilifer'
    },
    {
        'id': 'R115',
        'condiciones': [('genero', 'Pachycheles'), ('telson_piezas', '5'), ('frente_vista_dorsal', 'sinuosa'), ('carpo_liso', 'si')],
        'conclusion': {'especie': 'Pachycheles riseii', 'genero': 'Pachycheles'},
        'explicacion': 'Telson 5, frente sinuosa, carpo liso → Pachycheles riseii'
    },
    {
        'id': 'R116',
        'condiciones': [('genero', 'Pachycheles'), ('telson_piezas', '5'), ('frente_vista_dorsal', 'recta'), ('carpo_liso', 'no')],
        'conclusion': {'especie': 'Pachycheles ackleianus', 'genero': 'Pachycheles'},
        'explicacion': 'Telson 5, frente recta, carpo con tubérculos → Pachycheles ackleianus'
    },

    # ===================== PASO 10/11: PETROLISTHES (CARPO ENTERO) =====================
    {
        'id': 'R117',
        'condiciones': [('genero', 'Petrolisthes'), ('carpo_quelipedos', 'entero'), ('frente_diente_lobuliforme', 'si')],
        'conclusion': {'especie': 'Petrolisthes tridentatus', 'genero': 'Petrolisthes'},
        'explicacion': 'Carpo entero, frente con diente lobuliforme → Petrolisthes tridentatus'
    },
    {
        'id': 'R118',
        'condiciones': [('genero', 'Petrolisthes'), ('carpo_quelipedos', 'entero'), ('frente_diente_lobuliforme', 'no'), ('mero_tercer_pata_inflado', 'si')],
        'conclusion': {'especie': 'Petrolisthes tonsorius', 'genero': 'Petrolisthes'},
        'explicacion': 'Carpo entero, frente triangular sin diente, mero inflado → Petrolisthes tonsorius'
    },

    # ===================== PASO 12/13: PETROLISTHES (CARPO CON DIENTES) =====================
    {
        'id': 'R119',
        'condiciones': [('genero', 'Petrolisthes'), ('carpo_quelipedos', 'dientes_lobulos'), ('telson_piezas', '5')],
        'conclusion': {'especie': 'Petrolisthes jugosus', 'genero': 'Petrolisthes'},
        'explicacion': 'Carpo con dientes, telson 5 → Petrolisthes jugosus'
    },
    {
        'id': 'R120',
        'condiciones': [
            ('genero', 'Petrolisthes'), ('carpo_quelipedos', 'dientes_lobulos'),
            ('telson_piezas', '7'), ('espina_epibranquial', 'ausente'),
            ('margen_flexor_carpo', 'tres_subiguales')
        ],
        'conclusion': {'especie': 'Petrolisthes politus', 'genero': 'Petrolisthes'},
        'explicacion': 'Telson 7, espina ausente, 3 dientes subiguales → Petrolisthes politus'
    },
    {
        'id': 'R121',
        'condiciones': [
            ('genero', 'Petrolisthes'), ('carpo_quelipedos', 'dientes_lobulos'),
            ('telson_piezas', '7'), ('espina_epibranquial', 'ausente'),
            ('margen_flexor_carpo', 'tres_cuatro_unidos')
        ],
        'conclusion': {'especie': 'Petrolisthes lewisi', 'genero': 'Petrolisthes'},
        'explicacion': 'Telson 7, espina ausente, 3-4 dientes unidos distalmente → Petrolisthes lewisi'
    },
    {
        'id': 'R122',
        'condiciones': [
            ('genero', 'Petrolisthes'), ('carpo_quelipedos', 'dientes_lobulos'),
            ('telson_piezas', '7'), ('espina_epibranquial', 'presente'),
            ('margen_flexor_carpo', 'tres_separados')
        ],
        'conclusion': {'especie': 'Petrolisthes armatus', 'genero': 'Petrolisthes'},
        'explicacion': 'Telson 7, espina presente, 3 dientes separados → Petrolisthes armatus'
    },
    {
        'id': 'R123',
        'condiciones': [
            ('genero', 'Petrolisthes'), ('carpo_quelipedos', 'dientes_lobulos'),
            ('telson_piezas', '7'), ('espina_epibranquial', 'presente'),
            ('margen_flexor_carpo', 'cuatro_separados'), ('caparazon_textura', 'aspero')
        ],
        'conclusion': {'especie': 'Petrolisthes galathinus', 'genero': 'Petrolisthes'},
        'explicacion': 'Telson 7, espina presente, 4 dientes, caparazón áspero → Petrolisthes galathinus'
    },
    {
        'id': 'R124',
        'condiciones': [
            ('genero', 'Petrolisthes'), ('carpo_quelipedos', 'dientes_lobulos'),
            ('telson_piezas', '7'), ('espina_epibranquial', 'presente'),
            ('margen_flexor_carpo', 'cuatro_separados'), ('caparazon_textura', 'liso'),
            ('pubescencia_fina', 'si')
        ],
        'conclusion': {'especie': 'Petrolisthes marginatus', 'genero': 'Petrolisthes'},
        'explicacion': 'Telson 7, espina presente, 4 dientes, caparazón liso con pubescencia → Petrolisthes marginatus'
    },

    # ===================== PASO 17: MINYOCERUS =====================
    {
        'id': 'R125',
        'condiciones': [('clave_grupo', 'grupo_17'), ('flagelo_rudimentario', 'si'), ('relacion_largo_ancho', '1.3')],
        'conclusion': {'especie': 'Minyocerus angustus', 'genero': 'Minyocerus'},
        'explicacion': 'Flagelo rudimentario, caparazón 1.3x más largo → Minyocerus angustus'
    },
    {
        'id': 'R126',
        'condiciones': [('clave_grupo', 'grupo_17'), ('flagelo_rudimentario', 'no'), ('relacion_largo_ancho', 'menos_1.3')],
        'conclusion': {'clave_subgrupo': 'subgrupo_18'},
        'explicacion': 'Flagelo normal, caparazón <1.3x → paso 18'
    },

    # ===================== PASO 18: MEGALOBRACHIUM =====================
    {
        'id': 'R127',
        'condiciones': [('clave_subgrupo', 'subgrupo_18'), ('frente_estructura', 'inclinada')],
        'conclusion': {'genero': 'Megalobrachium', 'clave_subgrupo': 'subgrupo_19'},
        'explicacion': 'Frente inclinada/redondeada → género Megalobrachium'
    },
    {
        'id': 'R128',
        'condiciones': [('clave_subgrupo', 'subgrupo_18'), ('frente_estructura', 'recta')],
        'conclusion': {'clave_subgrupo': 'subgrupo_22'},
        'explicacion': 'Frente recta, prominente → paso 22'
    },

    # ===================== PASO 19/20/21: MEGALOBRACHIUM ESPECIES =====================
    {
        'id': 'R129',
        'condiciones': [('genero', 'Megalobrachium'), ('telson_piezas', '5')],
        'conclusion': {'especie': 'Megalobrachium soriatum', 'genero': 'Megalobrachium'},
        'explicacion': 'Telson 5 → Megalobrachium soriatum'
    },
    {
        'id': 'R130',
        'condiciones': [('genero', 'Megalobrachium'), ('telson_piezas', '7'), ('caparazon_erosionado', 'si')],
        'conclusion': {'especie': 'Megalobrachium mortenseni', 'genero': 'Megalobrachium'},
        'explicacion': 'Telson 7, caparazón erosionado → Megalobrachium mortenseni'
    },
    {
        'id': 'R131',
        'condiciones': [('genero', 'Megalobrachium'), ('telson_piezas', '7'), ('caparazon_erosionado', 'no'), ('setas_abundantes', 'si')],
        'conclusion': {'especie': 'Megalobrachium poeyi', 'genero': 'Megalobrachium'},
        'explicacion': 'Telson 7, setas abundantes → Megalobrachium poeyi'
    },
    {
        'id': 'R132',
        'condiciones': [('genero', 'Megalobrachium'), ('telson_piezas', '7'), ('caparazon_erosionado', 'no'), ('setas_abundantes', 'no')],
        'conclusion': {'especie': 'Megalobrachium roseum', 'genero': 'Megalobrachium'},
        'explicacion': 'Telson 7, setas escasas → Megalobrachium roseum'
    },

    # ===================== PASO 22: PISIDIA vs PORCELLANA =====================
    {
        'id': 'R133',
        'condiciones': [
            ('clave_subgrupo', 'subgrupo_22'),
            ('margenes_laterales_espinulas', 'si'),
            ('dedos_torcidos', 'si'),
            ('lobulo_proximal_carpo', 'no')
        ],
        'conclusion': {'especie': 'Pisidia brasiliensis', 'genero': 'Pisidia'},
        'explicacion': 'Márgenes con espínulas, dedos torcidos, sin lóbulo → Pisidia brasiliensis'
    },
    {
        'id': 'R134',
        'condiciones': [
            ('clave_subgrupo', 'subgrupo_22'),
            ('margenes_laterales_espinulas', 'no'),
            ('dedos_torcidos', 'no'),
            ('lobulo_proximal_carpo', 'si')
        ],
        'conclusion': {'especie': 'Porcellana sayana', 'genero': 'Porcellana'},
        'explicacion': 'Sin espínulas, dedos no torcidos, con lóbulo proximal → Porcellana sayana'
    },
]

REGLAS_DIFUSAS = [
    # --- Género Neopisosoma (Suelen ser pequeños) ---
    {
        'id': 'RD001', 'especie': 'Neopisosoma cf. neglectum',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Especie pequeña, comúnmente menor a 2 cm.'
    },  
    {
        'id': 'RD002', 'especie': 'Neopisosoma angustifrons',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Especie pequeña, comúnmente menor a 2 cm.'
    },
    {
        'id': 'RD003', 'especie': 'Neopisosoma orientale',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Especie pequeña, comúnmente menor a 2 cm.'
    },
    
    # --- Género Clastotoechus -------------------------------------------
    {
        'id': 'RD004', 'especie': 'Clastotoechus nodosus',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Habitante de bancos de mejillones, de tamaño reducido.'
    },

    # --- Género Pachycheles (Robustos, tamaño mediano) --------------------
    {
        'id': 'RD005', 'especie': 'Pachycheles serratus',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Suelen tener caparazones robustos y gruesos de tamaño mediano.'
    },
    {
        'id': 'RD006', 'especie': 'Pachycheles monilifer',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Suelen tener caparazones robustos y gruesos de tamaño mediano.'
    },
    {
        'id': 'RD007', 'especie': 'Pachycheles riseii',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Suelen tener caparazones robustos y gruesos de tamaño mediano.'
    },
    {
        'id': 'RD008', 'especie': 'Pachycheles ackleianus',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Suelen tener caparazones robustos y gruesos de tamaño mediano.'
    },

    # --- Género Petrolisthes (Muy variables, varían entre grandes y medianos) ---
    {
        'id': 'RD009', 'especie': 'Petrolisthes tridentatus',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Tamaño intermedio, habita bajo rocas intermareales.'
    },
    {
        'id': 'RD010', 'especie': 'Petrolisthes tonsorius',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Tamaño intermedio, habita bajo rocas.'
    },
    {
        'id': 'RD011', 'especie': 'Petrolisthes jugosus',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Suele ser más pequeño que otros Petrolisthes.'
    },
    {
        'id': 'RD012', 'especie': 'Petrolisthes politus',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Cangrejo mediano común en zonas costeras.'
    },
    {
        'id': 'RD013', 'especie': 'Petrolisthes lewisi',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Cangrejo mediano común en zonas costeras.'
    },
    {
        'id': 'RD014', 'especie': 'Petrolisthes armatus',
        'condiciones_difusas': [('tamano_cm', 'grande', 0.5)],
        'explicacion': 'Una de las especies que puede alcanzar mayor tamaño relativo.'
    },
    {
        'id': 'RD015', 'especie': 'Petrolisthes galathinus',
        'condiciones_difusas': [('tamano_cm', 'grande', 0.5)],
        'explicacion': 'Caparazón áspero y vistoso, puede alcanzar gran tamaño.'
    },
    {
        'id': 'RD016', 'especie': 'Petrolisthes marginatus',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Tamaño estándar para el género en su etapa adulta.'
    },

    # --- Género Minyocerus (Simbiontes diminutos) ---
    {
        'id': 'RD017', 'especie': 'Minyocerus angustus',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.7)],
        'explicacion': 'Es una especie diminuta simbionte de estrellas de mar.'
    },

    # --- Género Megalobrachium (Pequeños a medianos) ---
    {
        'id': 'RD018', 'especie': 'Megalobrachium soriatum',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Suele presentar tamaños reducidos en su adultez.'
    },
    {
        'id': 'RD019', 'especie': 'Megalobrachium mortenseni',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Habita en corales, cuerpo pequeño y compacto.'
    },
    {
        'id': 'RD020', 'especie': 'Megalobrachium poeyi',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Puede alcanzar tamaños ligeramente mayores que sus congéneres.'
    },
    {
        'id': 'RD021', 'especie': 'Megalobrachium roseum',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Suele presentar tamaños reducidos en su adultez.'
    },

    # --- Géneros Pisidia y Porcellana ---
    {
        'id': 'RD022', 'especie': 'Pisidia brasiliensis',
        'condiciones_difusas': [('tamano_cm', 'pequeño', 0.5)],
        'explicacion': 'Cangrejos pequeños con adaptaciones en los dedos.'
    },
    {
        'id': 'RD023', 'especie': 'Porcellana sayana',
        'condiciones_difusas': [('tamano_cm', 'mediano', 0.5)],
        'explicacion': 'Comensal en conchas de cangrejos ermitaños, tamaño intermedio.'
    }
]

# ------------------------------------------------------------
# CARACTERÍSTICAS DE ESPECIES PARA VERIFICACIÓN
# ------------------------------------------------------------
CARACTERISTICAS_ESPECIES = {
    "Neopisosoma cf. neglectum": [
        "Caparazón subcuadrado, tan largo como ancho, superficie lisa",
        "Quelípedos sin gránulos ni tubérculos",
        "Carpo de quelípedos con tres crestas dorsales longitudinales",
        "Paredes laterales incompletas",
        "Distribución: Colombia, Granada, Antillas Holandesas"
    ],
    "Neopisosoma angustifrons": [
        "Caparazón subcuadrado, superficie lisa, paredes laterales incompletas",
        "Quelípedos desiguales, con gránulos y tubérculos cónicos en la palma",
        "Margen flexor del carpo con 4 o más dientes irregulares",
        "Telson con 5 placas, pleópodos ausentes en machos",
        "Distribución: Golfo de México a Venezuela"
    ],
    "Neopisosoma orientale": [
        "Caparazón subcuadrado, casi liso, convexo longitudinalmente",
        "Quelípedos con gránulos uniformes, setas dispersas en la palma",
        "Margen anterior de la anténula aserrado y setoso",
        "Telson con 7 placas",
        "Distribución: Trinidad y Venezuela (primer registro)"
    ],
    "Clastotoechus nodosus": [
        "Caparazón más largo que ancho, cubierto de gránulos",
        "Frente trilobulada en vista dorsal con penacho de setas",
        "Quelípedos aplanados, subiguales",
        "Telson con 5 placas",
        "Habita bancos de mejillones"
    ],
    "Pachycheles serratus": [
        "Caparazón ligeramente más ancho que largo, convexo",
        "Frente convexa en vista dorsal, trilobulada en vista frontal",
        "Quelípedos desiguales, carpo con 3 dientes lobulados",
        "Telson con 7 placas",
        "Muy común en rocas, corales y esponjas"
    ],
    "Pachycheles monilifer": [
        "Caparazón tan largo como ancho en machos, más ancho en hembras",
        "Frente con porción media más avanzada y cubierta de setas",
        "Carpo y propodo con tubérculos discoidales en hileras",
        "Telson con 5 placas",
        "Distribución: Florida a Brasil"
    ],
    "Pachycheles riseii": [
        "Caparazón más ancho que largo, frente sinuosa en vista dorsal",
        "Quelípedos desiguales, carpo liso sin gránulos ni tubérculos",
        "Telson con 5 placas",
        "Pleópodos ausentes en machos",
        "Distribución: Florida a Brasil"
    ],
    "Pachycheles ackleianus": [
        "Caparazón más ancho que largo, convexo, frente recta",
        "Quelípedos con tubérculos dispuestos irregularmente",
        "Telson con 5 placas, machos con pleópodos",
        "Frente amplia, casi recta, sin setas",
        "Distribución: Florida a Brasil"
    ],
    "Petrolisthes tridentatus": [
        "Caparazón subcuadrado, con gránulos bajos",
        "Frente con diente lobuliforme en los ángulos orbitales internos",
        "Ángulo orbital interno formado por un lóbulo cónico (apariencia tridentada)",
        "Telson con 7 placas",
        "Habita bajo rocas en zona intermareal"
    ],
    "Petrolisthes tonsorius": [
        "Caparazón subcuadrado, casi liso, con pliegues cortos",
        "Frente triangular sin dientes lobuliformes",
        "Carpo de quelípedos con gránulos diagonales",
        "Mero del tercer par de patas inflado",
        "Distribución: Colombia, Venezuela y Pacífico"
    ],
    "Petrolisthes jugosus": [
        "Caparazón subcircular, más ancho que largo en hembras",
        "Frente trilobulada, surco medio profundo",
        "Telson con 5 piezas (única en el género)",
        "Carpo de quelípedos con margen extensor aserrado",
        "Distribución: Florida a Venezuela"
    ],
    "Petrolisthes politus": [
        "Caparazón subcircular, con gránulos pequeños",
        "Margen flexor del carpo con 3 dientes subiguales",
        "Espina epibranquial ausente",
        "Telson con 7 placas",
        "Distribución: Cayos de Florida a Venezuela"
    ],
    "Petrolisthes lewisi": [
        "Caparazón subcuadrado, superficie irregular",
        "Margen flexor del carpo con 3-4 dientes, los distales unidos",
        "Espina epibranquial ausente",
        "Telson con 7 placas",
        "Distribución: Pacífico (California a Ecuador), primer registro en Atlántico"
    ],
    "Petrolisthes armatus": [
        "Caparazón ligeramente más largo que ancho",
        "Espina epibranquial presente",
        "Margen flexor del carpo con 3 dientes separados",
        "Telson con 7 placas",
        "Muy común en sustratos rocosos y corales"
    ],
    "Petrolisthes galathinus": [
        "Caparazón más largo que ancho, áspero, con estrías transversales",
        "Espina supraorbital presente, espina epibranquial presente",
        "Margen flexor del carpo con 4 dientes separados",
        "Telson con 7 placas",
        "Distribución: Atlántico (Cabo Hatteras a Brasil) y Pacífico"
    ],
    "Petrolisthes marginatus": [
        "Caparazón casi liso, con pliegues en la región posterolateral",
        "Espina epibranquial presente, ángulo orbital externo terminado en espina",
        "Margen flexor del carpo con 4 dientes separados",
        "Telson con 7 placas, caparazón cubierto de fina pubescencia",
        "Distribución: Panamá a Brasil, Pacífico y Atlántico"
    ],
    "Minyocerus angustus": [
        "Caparazón 1.3 veces más largo que ancho",
        "Artejos móviles de la antena muy pequeños, flagelo rudimentario",
        "Especie simbionte de estrellas de mar",
        "Distribución: Cubagua, Los Testigos, Margarita"
    ],
    "Megalobrachium soriatum": [
        "Caparazón tan largo como ancho, frente inclinada",
        "Telson con 5 placas",
        "Quelípedos cubiertos de tubérculos fuertes y setas abundantes",
        "Urópodos con ramas diminutas en machos",
        "Distribución: Carolina del Norte a Brasil"
    ],
    "Megalobrachium mortenseni": [
        "Caparazón casi tan ancho como largo, fuertemente erosionado",
        "Margen flexor del carpo con protuberancia truncada",
        "Telson con 7 placas",
        "Habita coral cerebro (registro inusual)",
        "Distribución: Islas Vírgenes a Brasil"
    ],
    "Megalobrachium poeyi": [
        "Caparazón tan largo como ancho, cubierto de gránulos",
        "Setas abundantes en caparazón y quelípedos",
        "Telson con 7 placas",
        "Paredes laterales densamente setosas",
        "Distribución: Pacífico (Costa Rica a Panamá) y Atlántico (Florida a Brasil)"
    ],
    "Megalobrachium roseum": [
        "Caparazón casi tan ancho como largo, con protuberancias",
        "Frente trilobulada, lóbulos laterales truncados",
        "Quelípedos con 3 surcos longitudinales profundos",
        "Telson con 7 placas",
        "Distribución: Panamá a Brasil"
    ],
    "Pisidia brasiliensis": [
        "Caparazón ovalado, casi tan ancho como largo",
        "Márgenes laterales con espínulas posteriores al ángulo epibranquial",
        "Quelípedos con uno o ambos dedos torcidos",
        "Telson con 7 placas",
        "Distribución: Colombia, Venezuela, Brasil"
    ],
    "Porcellana sayana": [
        "Caparazón más largo que ancho, con gránulos pequeños",
        "Frente tridentada, diente medio triangular y más avanzado",
        "Quelípedos subiguales, carpo con lóbulo proximal en margen flexor",
        "Telson con 7 placas",
        "Distribución: Cabo Hatteras a Brasil"
    ],
}

# ------------------------------------------------------------
# Diccionarios para almacenar hechos durante la consulta
# ------------------------------------------------------------
HECHOS = {}
HECHOS_DIFUSOS = {}