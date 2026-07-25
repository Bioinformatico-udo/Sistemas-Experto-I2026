"""
Motor de inferencia - Sistema Experto para Corales de Los Roques
Sigue la clave taxonómica del Atlántico y filtra por familias locales.
"""

class NecesitaPregunta(Exception):
    def __init__(self, pregunta_id):
        self.pregunta_id = pregunta_id


class MotorInferencia:
    # Familias permitidas registradas para Los Roques
    FAMILIAS_PERMITIDAS = {
        "Milleporidae",
        "Stylasteridae",
        "Acroporidae",
        "Agariciidae",
        "Merulinidae",
        "Montastraeidae",
        "Siderastreidae",
        "Poritidae",
        "Faviidae",
        "Mussidae",
        "Meandrinidae",
        "Pocilloporidae",
        "Dendrophylliidae",
        "Rhizangiidae",
        "Astrocoeniidae"
    }

    def __init__(self):
        self.respuestas = {}
        self.paso_actual = 1
        self.historial = []

    def _get_respuesta(self, pregunta_id):
        val = self.respuestas.get(pregunta_id)
        if val is None:
            raise NecesitaPregunta(pregunta_id)
        return val

    def ejecutar(self, respuestas):
        """Ejecuta el motor con las respuestas del usuario"""
        self.respuestas = respuestas
        self.historial = []
        self.paso_actual = 1
        try:
            return self._navegar(self.paso_actual)
        except NecesitaPregunta as e:
            return {
                "estado": "pregunta",
                "pregunta_id": e.pregunta_id
            }

    def _retornar_no_albergado(self, familia="Desconocida"):
        return {
            "success": False,
            "especie": "No albergada en Los Roques",
            "nombre_comun": "Desconocido",
            "familia": familia,
            "mensaje": "Su coral no es de los albergados en los Roques",
            "sugerencia": f"La familia '{familia}' no pertenece a las familias de corales autóctonos registrados para el Parque Nacional Archipiélago de Los Roques."
        }

    def _resultado(self, especie, nombre_comun, familia):
        """Formatea el resultado final, filtrando por familias permitidas"""
        if familia not in self.FAMILIAS_PERMITIDAS:
            return self._retornar_no_albergado(familia)
            
        return {
            "success": True,
            "especie": especie,
            "nombre_comun": nombre_comun,
            "familia": familia,
            "orden": "Scleractinia" if familia not in ["Milleporidae"] else "Anthoathecata"
        }

    def _navegar(self, paso):
        """Navega por el árbol de decisión según el paso actual"""
        
        # --- PASO 1: ¿Tiene coralitos? ---
        if paso == 1:
            if self._get_respuesta("p1") == "no":
                return self._navegar(2)   # Sin coralitos → Hidrocorales
            else:
                return self._navegar(4)   # Con coralitos → Escleractinios

        # --- PASO 2: Hidrocorales ---
        elif paso == 2:
            val = self._get_respuesta("p2")
            if val == "incrustante":
                return self._resultado("Millepora alcicornis", "Coral de Fuego Cuerno de Alce", "Milleporidae")
            elif val == "aplanado":
                return self._navegar(3)

        # --- PASO 3: Millepora laminar ---
        elif paso == 3:
            if self._get_respuesta("p3") == "vertical":
                return self._resultado("Millepora complanata", "Coral de Fuego Laminar", "Milleporidae")
            else:
                return self._resultado("Millepora squarrosa", "Coral de Fuego Irregular", "Milleporidae")

        # --- PASO 4: Escleractinios ---
        elif paso == 4:
            if self._get_respuesta("p4") == "solitario":
                return self._navegar(5)
            else:
                return self._navegar(6)

        # --- PASO 5: Corales solitarios ---
        elif paso == 5:
            if self._get_respuesta("p5") == "toscamente":
                return self._resultado("Scolymia lacera", "Coral Solitario", "Mussidae")
            else:
                return self._resultado("Scolymia cubensis", "Coral Solitario", "Mussidae")

        # --- PASO 6: Corales coloniales ---
        elif paso == 6:
            if self._get_respuesta("p6") == "ramificado":
                return self._navegar(7)
            else:
                return self._navegar(19)

        # --- PASO 7: Coralitos en puntas o toda la rama ---
        elif paso == 7:
            if self._get_respuesta("p7") == "puntas":
                return self._navegar(8)
            else:
                return self._navegar(10)

        # --- PASO 8: Copas pequeñas o grandes ---
        elif paso == 8:
            if self._get_respuesta("p8") == "pequenas":
                return self._retornar_no_albergado("Oculinidae")
            else:
                return self._navegar(9)

        # --- PASO 9: Copas ovales o circulares ---
        elif paso == 9:
            if self._get_respuesta("p9") == "ovales":
                return self._resultado("Eusmilia fastigiata", "Coral Flor de Copa", "Meandrinidae")
            else:
                return self._resultado("Mussa angulosa", "Coral de Musgo", "Mussidae")

        # --- PASO 10: Proyecciones cilíndricas o cónicas ---
        elif paso == 10:
            if self._get_respuesta("p10") == "cilindricas":
                return self._navegar(11)
            else:
                return self._navegar(14)

        # --- PASO 11: Acropora ---
        elif paso == 11:
            if self._get_respuesta("p11") == "abanico":
                return self._resultado("Acropora palmata", "Coral Orejón", "Acroporidae")
            else:
                return self._navegar(13)

        # --- PASO 13: Acropora cervicornis vs prolifera ---
        elif paso == 13:
            if self._get_respuesta("p13") == "largas":
                return self._resultado("Acropora cervicornis", "Tarrito de Venado", "Acroporidae")
            else:
                return self._resultado("Acropora prolifera", "Coral Fusionado", "Acroporidae")

        # --- PASO 14: Número de escleroseptos ---
        elif paso == 14:
            if self._get_respuesta("p14") == "10":
                return self._navegar(15)
            else:
                return self._navegar(17)  # CORREGIDO: Ahora va a Porites ramificados

        # --- PASO 15: Madracis ---
        elif paso == 15:
            if self._get_respuesta("p15") == "nodular":
                return self._resultado("Madracis decactis", "Coral de Estrellas", "Pocilloporidae")
            else:
                return self._resultado("Madracis mirabilis", "Coral de Estrellas", "Pocilloporidae")

        # --- PASO 16: Oculina (Desactivada, mantenida por compatibilidad) ---
        elif paso == 16:
            return self._retornar_no_albergado("Oculinidae")

        # --- PASO 17: Porites ramificados - Diámetro de ramas ---
        elif paso == 17:
            if self._get_respuesta("p17") == "finas":
                return self._resultado("Porites divaricata", "Coral de Dedo Delgado", "Poritidae")
            else:
                return self._navegar(18)

        # --- PASO 18: Porites ramificados - Forma de puntas ---
        elif paso == 18:
            if self._get_respuesta("p18") == "bifurcadas":
                return self._resultado("Porites furcata", "Coral de Dedo Bifurcado", "Poritidae")
            else:
                return self._resultado("Porites porites", "Coral de Dedo", "Poritidae")

        # --- PASO 19: NO ramificado: laminar o masivo ---
        elif paso == 19:
            if self._get_respuesta("p19") == "laminar":
                return self._navegar(20)
            else:
                return self._navegar(30)

        # --- PASO 20: Agariciidae (laminar) ---
        elif paso == 20:
            if self._get_respuesta("p20") == "copas":
                return self._navegar(21)
            else:
                return self._navegar(22)

        # --- PASO 21: Porites colonensis o Mycetophyllia ressi ---
        elif paso == 21:
            if self._get_respuesta("p21") == "12":
                return self._resultado("Porites colonensis", "Coral de Dedo", "Poritidae")
            else:
                return self._resultado("Mycetophyllia ressi", "Coral de Placas", "Mussidae")

        # --- PASO 22: Con columela o sin ---
        elif paso == 22:
            if self._get_respuesta("p22") == "con":
                return self._navegar(23)
            else:
                return self._resultado("Leptoseris cucullata", "Coral Hoja", "Agariciidae")

        # --- PASO 23: Unifacial o bifacial ---
        elif paso == 23:
            if self._get_respuesta("p23") == "unifacial":
                return self._navegar(24)
            else:
                return self._resultado("Agaricia tenuifolia", "Coral Hoja", "Agariciidae")

        # --- PASO 24: Valles continuos o discontinuos ---
        elif paso == 24:
            if self._get_respuesta("p24") == "continuos":
                return self._navegar(25)
            else:
                return self._navegar(28)

        # --- PASO 25: 5-8 o 3-5 coralitos/cm ---
        elif paso == 25:
            if self._get_respuesta("p25") == "5_8":
                return self._navegar(27)
            else:
                return self._navegar(26)

        # --- PASO 26: Septos alternados más delgados o iguales ---
        elif paso == 26:
            if self._get_respuesta("p26") == "delgados":
                return self._resultado("Agaricia lamarcki", "Coral Hoja", "Agariciidae")
            else:
                return self._resultado("Agaricia grahamae", "Coral Hoja", "Agariciidae")

        # --- PASO 27: Colinas 6-7 mm o 2-4 mm ---
        elif paso == 27:
            if self._get_respuesta("p27") == "6_7":
                return self._resultado("Agaricia undata", "Coral Hoja", "Agariciidae")
            else:
                return self._resultado("Agaricia fragilis", "Coral Hoja", "Agariciidae")

        # --- PASO 28: Sin proyecciones o con proyecciones ---
        elif paso == 28:
            if self._get_respuesta("p28") == "sin":
                return self._resultado("Undaria agaricites purpurea", "Coral Hoja", "Agariciidae")
            else:
                return self._navegar(29)

        # --- PASO 29: Proyecciones altas o bajas ---
        elif paso == 29:
            if self._get_respuesta("p29") == "altas":
                return self._resultado("Undaria agaricites danai", "Coral Hoja", "Agariciidae")
            else:
                return self._resultado("Undaria agaricites carinata", "Coral Hoja", "Agariciidae")

        # --- PASO 30: Masivos: valles o copas ---
        elif paso == 30:
            if self._get_respuesta("p30") == "valles":
                return self._navegar(31)
            else:
                return self._navegar(48)

        # --- PASO 31: Valles poco pronunciados o pronunciados ---
        elif paso == 31:
            if self._get_respuesta("p31") == "poco":
                return self._navegar(32)
            else:
                return self._navegar(33)

        # --- PASO 32: Agaricia agaricites formas ---
        elif paso == 32:
            if self._get_respuesta("p32") == "concava":
                return self._resultado("Undaria agaricites agaricites", "Coral Hoja", "Agariciidae")
            else:
                return self._resultado("Undaria agaricites humilis", "Coral Hoja", "Agariciidae")

        # --- PASO 33: Septos no dentados o dentados ---
        elif paso == 33:
            if self._get_respuesta("p33") == "no":
                return self._navegar(34)
            else:
                return self._navegar(35)

        # --- PASO 34: Dendrogyra o Meandrina ---
        elif paso == 34:
            if self._get_respuesta("p34") == "pilares":
                return self._resultado("Dendrogyra cylindrus", "Coral Pilar", "Meandrinidae")
            else:
                return self._resultado("Meandrina meandrites", "Coral Cerebro", "Meandrinidae")

        # --- PASO 35: Con láminas verticales o sin ---
        elif paso == 35:
            if self._get_respuesta("p35") == "con":
                return self._navegar(36)
            else:
                return self._navegar(42)

        # --- PASO 36: Pared doble o sencilla ---
        elif paso == 36:
            if self._get_respuesta("p36") == "doble":
                return self._navegar(37)
            else:
                return self._navegar(39)

        # --- PASO 37: Series largas o cortas ---
        elif paso == 37:
            if self._get_respuesta("p37") == "largas":
                return self._navegar(38)
            else:
                return self._resultado("Colpophyllia breviserialis", "Coral Cerebro", "Faviidae")

        # --- PASO 38: Colpophyllia natans formas ---
        elif paso == 38:
            if self._get_respuesta("p38") == "pedunculo":
                return self._resultado("Colpophyllia natans amaranthus", "Coral Cerebro", "Faviidae")
            else:
                return self._resultado("Colpophyllia natans natans", "Coral Cerebro", "Faviidae")

        # --- PASO 39: Septos más delgados o iguales ---
        elif paso == 39:
            if self._get_respuesta("p39") == "delgados":
                return self._navegar(40)
            else:
                return self._resultado("Mycetophyllia aliciae", "Coral de Placas", "Mussidae")

        # --- PASO 40: Colinas continuas o radiales ---
        elif paso == 40:
            if self._get_respuesta("p40") == "continuas":
                return self._navegar(41)
            else:
                return self._resultado("Mycetophyllia lamarckiana", "Coral de Placas", "Mussidae")

        # --- PASO 41: Valles discontinuos o continuos ---
        elif paso == 41:
            if self._get_respuesta("p41") == "discontinuos":
                return self._resultado("Mycetophyllia ferox", "Coral de Placas", "Mussidae")
            else:
                return self._resultado("Mycetophyllia danaana", "Coral de Placas", "Mussidae")

        # --- PASO 42: Valles <0.5 cm o >0.5 cm ---
        elif paso == 42:
            if self._get_respuesta("p42") == "menor_0_5":
                return self._navegar(43)
            else:
                return self._navegar(45)

        # --- PASO 43: >20 septos/cm o <20 septos/cm ---
        elif paso == 43:
            if self._get_respuesta("p43") == "mayor_20":
                return self._resultado("Diploria clivosa", "Coral Cerebro", "Faviidae")
            else:
                return self._navegar(44)

        # --- PASO 44: Paredes con surco o sin ---
        elif paso == 44:
            if self._get_respuesta("p44") == "con":
                return self._resultado("Diploria labyrinthiformis", "Coral Cerebro Laberinto", "Faviidae")
            else:
                return self._resultado("Pseudodiploria strigosa", "Coral Cerebro", "Faviidae")

        # --- PASO 45: Dientes finos o toscos ---
        elif paso == 45:
            if self._get_respuesta("p45") == "finos":
                return self._navegar(46)
            else:
                return self._navegar(47)

        # --- PASO 46: Manicina areolata formas ---
        elif paso == 46:
            if self._get_respuesta("p46") == "central":
                return self._resultado("Manicina areolata areolata", "Coral Corazón de Roca", "Faviidae")
            else:
                return self._resultado("Manicina areolata mayori", "Coral Corazón de Roca", "Faviidae")

        # --- PASO 47: Isophyllia sinuosa o multiflora ---
        elif paso == 47:
            if self._get_respuesta("p47") == "2_5":
                return self._resultado("Isophyllia sinuosa", "Coral Cerebro", "Mussidae")
            else:
                return self._resultado("Isophyllia multiflora", "Coral Cerebro", "Mussidae")

        # --- PASO 48: Copas >1 cm o <1 cm ---
        elif paso == 48:
            if self._get_respuesta("p48") == "mayor_1":
                return self._resultado("Isophyllastrea rigida", "Coral Estrella", "Mussidae")
            else:
                return self._navegar(49)

        # --- PASO 49: Muy poroso o no poroso ---
        elif paso == 49:
            if self._get_respuesta("p49") == "poroso":
                return self._navegar(50)
            else:
                return self._navegar(53)

        # --- PASO 50: 12 septos o 24-48 septos ---
        elif paso == 50:
            if self._get_respuesta("p50") == "12":
                return self._navegar(51)
            else:
                return self._navegar(52)

        # --- PASO 51: Porites branneri o astreoides ---
        elif paso == 51:
            if self._get_respuesta("p51") == "0_7_1_2":
                return self._resultado("Porites branneri", "Coral de Dedo", "Poritidae")
            else:
                return self._resultado("Porites astreoides", "Coral de Dedo", "Poritidae")

        # --- PASO 52: Siderastrea radians o siderea ---
        elif paso == 52:
            if self._get_respuesta("p52") == "1_5_4_2":
                return self._resultado("Siderastrea radians", "Coral Mucura", "Siderastreidae")
            else:
                return self._resultado("Siderastrea siderea", "Coral Mucura", "Siderastreidae")

        # --- PASO 53: Columela estiliforme o no ---
        elif paso == 53:
            if self._get_respuesta("p53") == "estiliforme":
                return self._navegar(54)
            else:
                return self._navegar(55)

        # --- PASO 54: Stephanocoenia o Madracis (CORREGIDO) ---
        elif paso == 54:
            if self._get_respuesta("p54") == "2_6_3_0":
                return self._resultado("Stephanocoenia intersepta", "Coral Estrella", "Astrocoeniidae")
            else:
                return self._resultado("Madracis decactis", "Coral de Estrellas", "Pocilloporidae")

        # --- PASO 55: Copas apiñadas o separadas ---
        elif paso == 55:
            if self._get_respuesta("p55") == "apinadas":
                return self._navegar(56)
            else:
                return self._navegar(57)

        # --- PASO 56: Favia fragum o conferta ---
        elif paso == 56:
            if self._get_respuesta("p56") == "4_5_6_5":
                return self._resultado("Favia fragum", "Coral Estrella", "Faviidae")
            else:
                return self._resultado("Favia conferta", "Coral Estrella", "Faviidae")

        # --- PASO 57: Copas <6 mm o >6 mm ---
        elif paso == 57:
            if self._get_respuesta("p57") == "menor_6":
                return self._navegar(58)
            else:
                return self._resultado("Montastraea cavernosa", "Coral de Montaña", "Faviidae")

        # --- PASO 58: Copas ovaladas o circulares ---
        elif paso == 58:
            if self._get_respuesta("p58") == "ovaladas":
                return self._navegar(59)
            else:
                return self._navegar(60)

        # --- PASO 59: Favia gravida o Dichocoenia ---
        elif paso == 59:
            if self._get_respuesta("p59") == "espinosos":
                return self._resultado("Favia gravida", "Coral Estrella", "Faviidae")
            else:
                return self._resultado("Dichocoenia stokesi", "Coral de Orugas", "Meandrinidae")

        # --- PASO 60: Solenastrea hyades o paso 61 ---
        elif paso == 60:
            if self._get_respuesta("p60") == "3_3_5":
                return self._resultado("Solenastrea hyades", "Coral Estrella", "Faviidae")
            else:
                return self._navegar(61)

        # --- PASO 61: Plocoide o no plocoide ---
        elif paso == 61:
            if self._get_respuesta("p61") == "plocoide":
                return self._navegar(62)
            else:
                return self._resultado("Solenastrea bournoni", "Coral Estrella", "Faviidae")

        # --- PASO 62: Orbicella annularis, faveolata o franksi (CORREGIDO) ---
        elif paso == 62:
            if self._get_respuesta("p62") == "lisa":
                return self._navegar(63)  # Redirige al nuevo paso
            else:
                return self._resultado("Orbicella franksi", "Coral Montaña", "Merulinidae")

        # --- PASO 63: Orbicella annularis vs faveolata ---
        elif paso == 63:
            if self._get_respuesta("p63") == "columnar":
                return self._resultado("Orbicella annularis", "Coral Montaña", "Merulinidae")
            else:
                return self._resultado("Orbicella faveolata", "Coral Montaña", "Merulinidae")
                
        # Si llega aquí, algo salió mal
        return {
            "success": False,
            "especie": "No identificada",
            "nombre_comun": "Desconocido",
            "familia": "Desconocida",
            "mensaje": "No se pudo identificar la especie. Revisa las respuestas."
        }