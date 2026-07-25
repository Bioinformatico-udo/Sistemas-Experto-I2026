"""Preguntas del sistema experto siguiendo la clave taxonómica"""

def generar_preguntas():
    """Genera todas las preguntas según la clave"""
    return [
        # PASO 1
        {
            "id": "p1",
            "texto": "¿El coral tiene coralitos (hoyitos) visibles en la superficie?",
            "descripcion": "Observa si hay pequeñas cavidades circulares donde viven los pólipos.",
            "opciones": [
                {"label": "Sí, tiene coralitos visibles", "valor": "s", "principal": True},
                {"label": "No, la superficie es lisa o porosa", "valor": "no"},
            ]
        },
        # PASO 2 (si p1=no)
        {
            "id": "p2",
            "texto": "¿El coral es incrustante/ramificado o aplanado/laminar?",
            "descripcion": "¿Tiene forma de ramas o es una lámina plana?",
            "opciones": [
                {"label": "Incrustante o ramificado", "valor": "incrustante"},
                {"label": "Aplanado o en forma de láminas", "valor": "aplanado"},
            ]
        },
        # PASO 3
        {
            "id": "p3",
            "texto": "¿El coral en forma de láminas es vertical o aplanado irregular?",
            "descripcion": "Observa la orientación de las láminas.",
            "opciones": [
                {"label": "Láminas verticales", "valor": "vertical"},
                {"label": "Aplanado con superficie irregular", "valor": "irregular"},
            ]
        },
        # PASO 4
        {
            "id": "p4",
            "texto": "¿El coral es solitario (uno solo) o colonial (muchos)?",
            "descripcion": "¿Ves un solo pólipo grande o muchos juntos?",
            "opciones": [
                {"label": "Solitario (uno solo)", "valor": "solitario"},
                {"label": "Colonial (muchos juntos)", "valor": "colonial"},
            ]
        },
        # PASO 5
        {
            "id": "p5",
            "texto": "¿Cómo son los septos (radios) del coral?",
            "descripcion": "Observa los dientes en los septos.",
            "opciones": [
                {"label": "Toscamente dentados (<5 dientes/cm)", "valor": "toscamente"},
                {"label": "Finamente dentados (>5 dientes/cm)", "valor": "finamente"},
            ]
        },
        # PASO 6
        {
            "id": "p6",
            "texto": "¿La colonia es ramificada (como arbusto)?",
            "descripcion": "¿Tiene forma de ramas que se extienden?",
            "opciones": [
                {"label": "Sí, es ramificada", "valor": "ramificado"},
                {"label": "No, es masiva o laminar", "valor": "no"},
            ]
        },
        # PASO 7
        {
            "id": "p7",
            "texto": "¿Dónde están los coralitos en las ramas?",
            "descripcion": "¿Están solo en las puntas o en toda la superficie?",
            "opciones": [
                {"label": "Solo en las puntas de las ramas", "valor": "puntas"},
                {"label": "En toda la superficie de las ramas", "valor": "toda"},
            ]
        },
        # PASO 8
        {
            "id": "p8",
            "texto": "¿Qué tamaño tienen las copas (coralitos)?",
            "descripcion": "Mide el diámetro de los coralitos.",
            "opciones": [
                {"label": "Pequeñas (3-4 mm)", "valor": "pequenas"},
                {"label": "Grandes (>1 cm)", "valor": "grandes"},
            ]
        },
        # PASO 9
        {
            "id": "p9",
            "texto": "¿Qué forma tienen las copas?",
            "descripcion": "¿Son ovales/elongadas o circulares?",
            "opciones": [
                {"label": "Ovales con bordes lisos", "valor": "ovales"},
                {"label": "Circulares con septos dentados", "valor": "circulares"},
            ]
        },
        # PASO 10
        {
            "id": "p10",
            "texto": "¿Cómo son las proyecciones donde están los coralitos?",
            "descripcion": "¿Son cilíndricas o cónicas?",
            "opciones": [
                {"label": "Cilíndricas (tubos)", "valor": "cilindricas"},
                {"label": "Cónicas (como conos bajos)", "valor": "conicas"},
            ]
        },
        # PASO 11
        {
            "id": "p11",
            "texto": "¿Qué forma tienen las ramas?",
            "descripcion": "¿Son aplanadas en abanico o cilíndricas?",
            "opciones": [
                {"label": "Aplanadas a manera de abanico", "valor": "abanico"},
                {"label": "Cilíndricas divergentes", "valor": "cilindricas"},
            ]
        },
        # PASO 13
        {
            "id": "p13",
            "texto": "¿Cómo son las ramas cilíndricas?",
            "descripcion": "¿Son largas y separadas o fusionadas?",
            "opciones": [
                {"label": "Largas, rara vez fusionadas (poco tupidas)", "valor": "largas"},
                {"label": "Fusionadas, colonias tupidas", "valor": "fusionadas"},
            ]
        },
        # PASO 14
        {
            "id": "p14",
            "texto": "¿Cuántos escleroseptos (radios) tienen los coralitos?",
            "descripcion": "Cuenta los radios en el interior del coralito.",
            "opciones": [
                {"label": "10 escleroseptos", "valor": "10"},
                {"label": "Más de 10 escleroseptos", "valor": "mas_10"},
            ]
        },
        # PASO 15
        {
            "id": "p15",
            "texto": "¿Qué forma tiene la colonia?",
            "descripcion": "¿Es nodular (como nódulos) o arbustiva?",
            "opciones": [
                {"label": "Nodular o clavada", "valor": "nodular"},
                {"label": "Arbustiva", "valor": "arbustiva"},
            ]
        },
        # PASO 16
        {
            "id": "p16",
            "texto": "¿Cómo son las ramas?",
            "descripcion": "¿Son cortas y fusionadas o largas y torcidas?",
            "opciones": [
                {"label": "Cortas fusionadas (<10 mm)", "valor": "cortas"},
                {"label": "Largas y torcidas (hasta 2 cm)", "valor": "largas"},
            ]
        },
        # PASO 19
        {
            "id": "p19",
            "texto": "¿La colonia es laminar (como hojas) o masiva (como roca)?",
            "descripcion": "¿Forma placas planas o es un domo macizo?",
            "opciones": [
                {"label": "En forma de láminas u hojas", "valor": "laminar"},
                {"label": "Incrustante, masiva o submasiva", "valor": "masiva"},
            ]
        },
        # PASO 20
        {
            "id": "p20",
            "texto": "¿La superficie laminar está cubierta por copas o por colinas/valles?",
            "descripcion": "¿Ves hoyitos o surcos?",
            "opciones": [
                {"label": "Cubierta por copas", "valor": "copas"},
                {"label": "Cubierta por colinas y valles", "valor": "colinas"},
            ]
        },
        # PASO 21
        {
            "id": "p21",
            "texto": "¿Cuántos escleroseptos tienen los coralitos?",
            "descripcion": "Cuenta los radios.",
            "opciones": [
                {"label": "12 escleroseptos", "valor": "12"},
                {"label": "10 a 15 escleroseptos", "valor": "10_15"},
            ]
        },
        # PASO 22
        {
            "id": "p22",
            "texto": "¿Los coralitos tienen columela (pilar central)?",
            "descripcion": "Observa si hay un pequeño pilar en el centro del hoyito.",
            "opciones": [
                {"label": "Con columela", "valor": "con"},
                {"label": "Sin columela", "valor": "sin"},
            ]
        },
        # PASO 23
        {
            "id": "p23",
            "texto": "¿La colonia es unifacial o bifacial?",
            "descripcion": "¿Tiene pólipos en una o ambas caras?",
            "opciones": [
                {"label": "Unifacial (una cara)", "valor": "unifacial"},
                {"label": "Bifacial (dos caras)", "valor": "bifacial"},
            ]
        },
        # PASO 24
        {
            "id": "p24",
            "texto": "¿Los valles en la superficie son continuos o discontinuos?",
            "descripcion": "¿Los surcos son largos y continuos o cortos y separados?",
            "opciones": [
                {"label": "Valles continuos", "valor": "continuos"},
                {"label": "Valles discontinuos o reticulados", "valor": "discontinuos"},
            ]
        },
        # PASO 25
        {
            "id": "p25",
            "texto": "¿Cuántos coralitos hay por centímetro?",
            "descripcion": "Cuenta cuántos hoyitos hay en 1 cm de superficie.",
            "opciones": [
                {"label": "5-8 coralitos por cm", "valor": "5_8"},
                {"label": "3-5 coralitos por cm", "valor": "3_5"},
            ]
        },
        # PASO 26
        {
            "id": "p26",
            "texto": "¿Cómo son los septos alternados?",
            "descripcion": "¿Son más delgados o iguales que los interespacios?",
            "opciones": [
                {"label": "Septos alternados más delgados", "valor": "delgados"},
                {"label": "Septos iguales o casi iguales", "valor": "iguales"},
            ]
        },
        # PASO 27
        {
            "id": "p27",
            "texto": "¿Qué distancia hay entre las colinas?",
            "descripcion": "Mide la separación entre las elevaciones.",
            "opciones": [
                {"label": "6-7 mm de distancia", "valor": "6_7"},
                {"label": "2-4 mm de distancia", "valor": "2_4"},
            ]
        },
        # PASO 28
        {
            "id": "p28",
            "texto": "¿La superficie tiene proyecciones erectas bifaciales?",
            "descripcion": "¿Hay elevaciones que sobresalen?",
            "opciones": [
                {"label": "Sin proyecciones erectas", "valor": "sin"},
                {"label": "Con proyecciones erectas", "valor": "con"},
            ]
        },
        # PASO 29
        {
            "id": "p29",
            "texto": "¿Cómo son las proyecciones?",
            "descripcion": "¿Son altas e imbricadas o bajas en forma de carinas?",
            "opciones": [
                {"label": "Altas e imbricadas", "valor": "altas"},
                {"label": "Bajas y gruesas, en forma de carinas", "valor": "bajas"},
            ]
        },
        # PASO 30
        {
            "id": "p30",
            "texto": "¿La superficie masiva está cubierta por valles o por copas?",
            "descripcion": "¿Ves surcos (cerebro) o hoyitos?",
            "opciones": [
                {"label": "Cubierta por valles", "valor": "valles"},
                {"label": "Cubierta por copas", "valor": "copas"},
            ]
        },
        # PASO 31
        {
            "id": "p31",
            "texto": "¿Los valles son poco pronunciados o pronunciados?",
            "descripcion": "¿Son superficiales o profundos?",
            "opciones": [
                {"label": "Poco pronunciados (paredes bajas)", "valor": "poco"},
                {"label": "Pronunciados (paredes altas)", "valor": "pronunciados"},
            ]
        },
        # PASO 32
        {
            "id": "p32",
            "texto": "¿Qué forma tiene la colonia?",
            "descripcion": "¿Es cóncava incrustante o convexa submasiva?",
            "opciones": [
                {"label": "Incrustante cóncava", "valor": "concava"},
                {"label": "Submasiva convexa", "valor": "convexa"},
            ]
        },
        # PASO 33
        {
            "id": "p33",
            "texto": "¿Los escleroseptos son dentados o no dentados?",
            "descripcion": "Observa si los radios tienen dientes.",
            "opciones": [
                {"label": "No dentados (lisos)", "valor": "no"},
                {"label": "Dentados", "valor": "dentados"},
            ]
        },
        # PASO 34
        {
            "id": "p34",
            "texto": "¿Qué forma tiene la colonia?",
            "descripcion": "¿Tiene pilares rectos o es hemisférica?",
            "opciones": [
                {"label": "Pilares rectos y gruesos", "valor": "pilares"},
                {"label": "Masiva, hemisférica", "valor": "hemisferica"},
            ]
        },
        # PASO 35
        {
            "id": "p35",
            "texto": "¿Tiene láminas verticales dentadas en el suelo de los valles?",
            "descripcion": "Observa el fondo de los surcos.",
            "opciones": [
                {"label": "Con láminas verticales dentadas", "valor": "con"},
                {"label": "Sin láminas, con material esponjoso", "valor": "sin"},
            ]
        },
        # PASO 36
        {
            "id": "p36",
            "texto": "¿La pared que separa los valles es doble o sencilla?",
            "descripcion": "Observa la estructura de las paredes.",
            "opciones": [
                {"label": "Pared doble", "valor": "doble"},
                {"label": "Pared sencilla", "valor": "sencilla"},
            ]
        },
        # PASO 37
        {
            "id": "p37",
            "texto": "¿Las series caliculares son largas o cortas?",
            "descripcion": "Observa la longitud de las series.",
            "opciones": [
                {"label": "Series largas", "valor": "largas"},
                {"label": "Series cortas", "valor": "cortas"},
            ]
        },
        # PASO 38
        {
            "id": "p38",
            "texto": "¿Cómo es la superficie inferior de la colonia?",
            "descripcion": "¿Tiene pedúnculo ancho o es plana?",
            "opciones": [
                {"label": "Pedúnculo ancho", "valor": "pedunculo"},
                {"label": "Base plana", "valor": "plana"},
            ]
        },
        # PASO 39
        {
            "id": "p39",
            "texto": "¿Los escleroseptos son más delgados o iguales que los interespacios?",
            "descripcion": "Compara el grosor de los radios con los espacios.",
            "opciones": [
                {"label": "Más delgados", "valor": "delgados"},
                {"label": "Iguales o más gruesos", "valor": "iguales"},
            ]
        },
        # PASO 40
        {
            "id": "p40",
            "texto": "¿Las colinas son continuas o radiales?",
            "descripcion": "Observa el patrón de las elevaciones.",
            "opciones": [
                {"label": "Continuas, cubren toda la colonia", "valor": "continuas"},
                {"label": "Radiales, ausentes en el centro", "valor": "radiales"},
            ]
        },
        # PASO 41
        {
            "id": "p41",
            "texto": "¿Cómo son los valles?",
            "descripcion": "¿Son discontinuos o continuos?",
            "opciones": [
                {"label": "Discontinuos, angostos y someros", "valor": "discontinuos"},
                {"label": "Continuos, anchos y profundos", "valor": "continuos"},
            ]
        },
        # PASO 42
        {
            "id": "p42",
            "texto": "¿Qué tamaño tienen los valles?",
            "descripcion": "Mide el ancho de los surcos.",
            "opciones": [
                {"label": "Largos y sinuosos (<0.5 cm)", "valor": "menor_0_5"},
                {"label": "Cortos y lobulados (>0.5 cm)", "valor": "mayor_0_5"},
            ]
        },
        # PASO 43
        {
            "id": "p43",
            "texto": "¿Cuántos escleroseptos hay por centímetro?",
            "descripcion": "Cuenta los radios en 1 cm de longitud.",
            "opciones": [
                {"label": "Más de 20 septos por cm", "valor": "mayor_20"},
                {"label": "Menos de 20 septos por cm", "valor": "menor_20"},
            ]
        },
        # PASO 44
        {
            "id": "p44",
            "texto": "¿Las paredes entre valles tienen un surco superior?",
            "descripcion": "Observa la parte superior de las paredes.",
            "opciones": [
                {"label": "Con surco en la parte superior", "valor": "con"},
                {"label": "Sin surco", "valor": "sin"},
            ]
        },
        # PASO 45
        {
            "id": "p45",
            "texto": "¿Cómo son los dientes de los escleroseptos?",
            "descripcion": "Observa los dientes en los radios.",
            "opciones": [
                {"label": "Numerosos dientes finos", "valor": "finos"},
                {"label": "Pocos dientes toscos prominentes", "valor": "toscas"},
            ]
        },
        # PASO 46
        {
            "id": "p46",
            "texto": "¿Cómo están organizados los valles?",
            "descripcion": "¿Hay un valle central continuo o son todos discontinuos?",
            "opciones": [
                {"label": "Un valle central continuo", "valor": "central"},
                {"label": "Valles discontinuos transversales", "valor": "discontinuos"},
            ]
        },
        # PASO 47
        {
            "id": "p47",
            "texto": "¿Qué tamaño tienen los valles?",
            "descripcion": "¿Son de 2.5 cm o 1.5 cm?",
            "opciones": [
                {"label": "2.5 cm de ancho, 8 septos/cm", "valor": "2_5"},
                {"label": "1.5 cm de ancho, 12 septos/cm", "valor": "1_5"},
            ]
        },
        # PASO 48
        {
            "id": "p48",
            "texto": "¿Qué tamaño tienen las copas?",
            "descripcion": "Mide el diámetro de los coralitos.",
            "opciones": [
                {"label": "Mayor de 1 cm", "valor": "mayor_1"},
                {"label": "Menor de 1 cm", "valor": "menor_1"},
            ]
        },
        # PASO 49
        {
            "id": "p49",
            "texto": "¿El coral es muy poroso o no poroso?",
            "descripcion": "¿La superficie es esponjosa o compacta?",
            "opciones": [
                {"label": "Muy poroso (esponjoso)", "valor": "poroso"},
                {"label": "No poroso (compacto)", "valor": "compacto"},
            ]
        },
        # PASO 50
        {
            "id": "p50",
            "texto": "¿Cuántos escleroseptos tienen los coralitos?",
            "descripcion": "Cuenta los radios.",
            "opciones": [
                {"label": "12 escleroseptos", "valor": "12"},
                {"label": "24-48 escleroseptos", "valor": "24_48"},
            ]
        },
        # PASO 51
        {
            "id": "p51",
            "texto": "¿Qué profundidad y separación tienen los coralitos?",
            "descripcion": "Observa si son someros o profundos.",
            "opciones": [
                {"label": "Someros (0.7-1.2 mm, separados 0.2-0.3 mm)", "valor": "0_7_1_2"},
                {"label": "Profundos (1.2-1.5 mm, separados 0.5-0.8 mm)", "valor": "1_2_1_5"},
            ]
        },
        # PASO 52
        {
            "id": "p52",
            "texto": "¿Qué tamaño tienen los coralitos y cómo es el borde de los septos?",
            "descripcion": "Observa el borde interno de los radios.",
            "opciones": [
                {"label": "1.5-4.2 mm, septos perpendiculares", "valor": "1_5_4_2"},
                {"label": "2.6-5.0 mm, septos en pendiente", "valor": "2_6_5_0"},
            ]
        },
        # PASO 53
        {
            "id": "p53",
            "texto": "¿La columela es estiliforme (como alfiler) o no?",
            "descripcion": "Observa el centro del coralito.",
            "opciones": [
                {"label": "Estiliforme (como alfiler)", "valor": "estiliforme"},
                {"label": "No estiliforme", "valor": "no"},
            ]
        },
        # PASO 54
        {
            "id": "p54",
            "texto": "¿Qué tamaño y número de septos tienen los coralitos?",
            "descripcion": "Observa el diámetro y cuenta los radios.",
            "opciones": [
                {"label": "2.6-3.0 mm, 24 septos", "valor": "2_6_3_0"},
                {"label": "1.5-2.5 mm, 10 septos", "valor": "1_5_2_5"},
            ]
        },
        # PASO 55
        {
            "id": "p55",
            "texto": "¿Las copas están apiñadas (juntas) o separadas?",
            "descripcion": "Observa si los coralitos comparten paredes.",
            "opciones": [
                {"label": "Apiñadas (paredes fusionadas o comunes)", "valor": "apinadas"},
                {"label": "Separadas (paredes individuales)", "valor": "separadas"},
            ]
        },
        # PASO 56
        {
            "id": "p56",
            "texto": "¿Qué tamaño tienen las copas?",
            "descripcion": "Mide el diámetro de los coralitos.",
            "opciones": [
                {"label": "4.5-6.5 mm", "valor": "4_5_6_5"},
                {"label": "3-4 mm (a veces elongadas)", "valor": "3_4"},
            ]
        },
        # PASO 57
        {
            "id": "p57",
            "texto": "¿Qué tamaño tienen las copas?",
            "descripcion": "Mide el diámetro de los coralitos.",
            "opciones": [
                {"label": "Menores a 6 mm (pueden elongarse)", "valor": "menor_6"},
                {"label": "Siempre circulares, de al menos 6 mm", "valor": "mayor_6"},
            ]
        },
        # PASO 58
        {
            "id": "p58",
            "texto": "¿Qué forma tienen las copas?",
            "descripcion": "¿Son ovaladas/elongadas o circulares?",
            "opciones": [
                {"label": "Ovaladas o elongadas (3-5 mm)", "valor": "ovaladas"},
                {"label": "Circulares o poligonales (2-3.5 mm)", "valor": "circulares"},
            ]
        },
        # PASO 59
        {
            "id": "p59",
            "texto": "¿Cómo son los escleroseptos?",
            "descripcion": "¿Son espinosos o aserrados?",
            "opciones": [
                {"label": "Dentados de lados espinosos", "valor": "espinosos"},
                {"label": "Aserrados", "valor": "aserrados"},
            ]
        },
        # PASO 60
        {
            "id": "p60",
            "texto": "¿Qué tamaño tienen los coralitos?",
            "descripcion": "Mide el diámetro de los coralitos.",
            "opciones": [
                {"label": "3-3.5 mm, septos no exertos", "valor": "3_3_5"},
                {"label": "2-2.5 mm, septos exertos", "valor": "2_2_5"},
            ]
        },
        # PASO 61
        {
            "id": "p61",
            "texto": "¿La colonia es plocoide o no plocoide?",
            "descripcion": "Observa si los coralitos sobresalen o no.",
            "opciones": [
                {"label": "Plocoide", "valor": "plocoide"},
                {"label": "No plocoide", "valor": "no"},
            ]
        },
        # PASO 62
        {
            "id": "p62",
            "texto": "¿Cómo es la superficie de la colonia?",
            "descripcion": "¿Es lisa y uniforme o desigual?",
            "opciones": [
                {"label": "Lisa con coralitos uniformes", "valor": "lisa"},
                {"label": "Desigual con coralitos irregulares", "valor": "desigual"},
            ]
        },  

        {
            "id": "p63",
            "texto": "¿Dónde se encuentra el tejido vivo del coral?",
            "descripcion": "Observa la distribución del tejido en la colonia.",
            "opciones": [
                {"label": "Columnar, tejido vivo solo en la parte superior de la columna", "valor": "columnar"},
                {"label": "Crustoso, hemisférico o masivo, con proyecciones laterales en declive", "valor": "costroso_hemisferico"},
            ]
        },
    ]