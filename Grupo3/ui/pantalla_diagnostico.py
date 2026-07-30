import os

from modelo.especies import rutaRecurso
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QProgressBar, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QShortcut, QKeySequence
from PyQt6.QtCore import Qt


class PreguntaWidget(QWidget):
    def __init__(self, pregunta, numActual, total, progresoPct,
                 onRespuesta, onReiniciar, onAtras=None,
                 observaciones=None, preguntas=None, historialAbierto=False, parent=None):
        super().__init__(parent)
        self.onRespuesta = onRespuesta
        self.onAtras = onAtras
        self.preguntaId = pregunta["id"]
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 15, 40, 20)
        layout.setSpacing(8)

        progLayout = QHBoxLayout()
        progLbl = QLabel(f"Pregunta {numActual} de {total}")
        progLbl.setStyleSheet("color: #546E7A; font-size: 12px;")
        progLayout.addWidget(progLbl)
        progLayout.addStretch()

        btnAtras = QPushButton("← Atrás")
        btnAtras.setObjectName("btn_back")
        btnAtras.setToolTip("Volver a la pregunta anterior (Backspace)")
        btnAtras.setEnabled(onAtras is not None)
        if onAtras:
            btnAtras.clicked.connect(onAtras)
        progLayout.addWidget(btnAtras)

        btnReiniciar = QPushButton("⟳ Reiniciar")
        btnReiniciar.setObjectName("btn_reset")
        btnReiniciar.setToolTip("Reiniciar el diagnóstico desde cero")
        btnReiniciar.clicked.connect(onReiniciar)
        progLayout.addWidget(btnReiniciar)
        layout.addLayout(progLayout)

        barra = QProgressBar()
        barra.setValue(progresoPct)
        barra.setTextVisible(False)
        barra.setFixedHeight(6)
        layout.addWidget(barra)

        if observaciones and preguntas:
            respPrev = [(p, observaciones[p["id"]])
                        for p in preguntas
                        if p["id"] in observaciones and p["id"] != self.preguntaId]
            if respPrev:
                histFrame = QFrame()
                histFrame.setObjectName("panel_historial")
                histLayout = QVBoxLayout(histFrame)
                histLayout.setContentsMargins(12, 8, 12, 8)
                histLayout.setSpacing(3)

                self._historialAbierto = historialAbierto
                flecha = "▴" if self._historialAbierto else "▾"
                toggleBtn = QPushButton(f"{flecha} Respuestas anteriores ({len(respPrev)})")
                toggleBtn.setStyleSheet(
                    "background: transparent; color: #546E7A; font-size: 11px; "
                    "font-weight: bold; text-align: left; border: none; padding: 2px 0;"
                )
                toggleBtn.setCursor(Qt.CursorShape.PointingHandCursor)
                histLayout.addWidget(toggleBtn)

                histContenido = QVBoxLayout()
                histContenido.setSpacing(2)
                for p, val in respPrev:
                    icono = "SI" if val else "NO"
                    lbl = QLabel(f"  [{icono}]  {p['texto']}")
                    lbl.setObjectName("historial_item")
                    lbl.setWordWrap(True)
                    histContenido.addWidget(lbl)

                histWidget = QWidget()
                histWidget.setLayout(histContenido)
                histWidget.setVisible(self._historialAbierto)

                def makeToggle(w, b):
                    return lambda: self._toggleHistorial(w, b)
                toggleBtn.clicked.connect(makeToggle(histWidget, toggleBtn))
                histLayout.addWidget(histWidget)

                layout.addWidget(histFrame)

        panel = QFrame()
        panel.setObjectName("panel")
        panelLayout = QVBoxLayout(panel)
        panelLayout.setContentsMargins(30, 25, 30, 25)
        panelLayout.setSpacing(16)

        preguntaLbl = QLabel(pregunta["texto"])
        preguntaLbl.setObjectName("pregunta")
        preguntaLbl.setWordWrap(True)
        preguntaLbl.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        preguntaLbl.setStyleSheet("color: #FFFFFF;")
        panelLayout.addWidget(preguntaLbl)

        expFrame = QFrame()
        expFrame.setStyleSheet("background: #061021; border-radius: 8px; padding: 2px;")
        expLayout = QVBoxLayout(expFrame)
        expLayout.setContentsMargins(12, 10, 12, 10)
        expIcon = QLabel(pregunta["explicacion"])
        expIcon.setStyleSheet("color: #80DEEA; font-size: 12px;")
        expIcon.setWordWrap(True)
        expLayout.addWidget(expIcon)
        panelLayout.addWidget(expFrame)

        panelLayout.addSpacing(8)
        for textoOpcion, valor in pregunta["opciones"]:
            indicador = "[1]" if valor else "[2]"
            btn = QPushButton(f"  {indicador}  {textoOpcion}")
            btn.setObjectName("btn_opcion")
            btn.setFixedHeight(52)
            btn.setFont(QFont("Segoe UI", 12))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            tecla = "1" if valor else "2"
            btn.setToolTip(f"Presione [{tecla}] para seleccionar esta opción")
            btn.clicked.connect(lambda checked, v=valor, pid=pregunta["id"]: onRespuesta(pid, v))
            panelLayout.addWidget(btn)

        layout.addWidget(panel)
        layout.addStretch()

        self._instalarAtajos(pregunta)

    def _instalarAtajos(self, pregunta):
        for textoOpcion, valor in pregunta["opciones"]:
            tecla = "1" if valor else "2"
            sc = QShortcut(QKeySequence(tecla), self)
            sc.activated.connect(lambda v=valor, pid=pregunta["id"]: self.onRespuesta(pid, v))
        if self.onAtras:
            scBack = QShortcut(QKeySequence(Qt.Key.Key_Backspace), self)
            scBack.activated.connect(self.onAtras)
            scEsc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
            scEsc.activated.connect(self.onAtras)

    def _toggleHistorial(self, widget, btn):
        visible = not widget.isVisible()
        widget.setVisible(visible)
        self._historialAbierto = visible
        flecha = "▴" if visible else "▾"
        count = btn.text().split("(")[-1].rstrip(")")
        btn.setText(f"{flecha} Respuestas anteriores ({count})")

    def obtenerHistorialAbierto(self):
        return getattr(self, '_historialAbierto', False)


class ResultadoWidget(QWidget):
    def __init__(self, resultados, observaciones, preguntas,
                 onReiniciar, onVerCatalogo=None, parent=None):
        super().__init__(parent)
        self.preguntas = preguntas
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(12)

        if resultados:
            topNombre, topFc, topDatos = resultados[0]
            color = topDatos.get("color", "#00838F")
        else:
            topNombre, topFc, topDatos, color = "Sin resultado", 0, {}, "#546E7A"

        tituloLbl = QLabel("Resultado del diagnóstico")
        tituloLbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        tituloLbl.setStyleSheet("color: #00E5FF;")
        layout.addWidget(tituloLbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        contenido = QWidget()
        contLayout = QVBoxLayout(contenido)
        contLayout.setSpacing(14)

        if topFc == 100:
            confTexto = "IDENTIFICACIÓN DEFINITIVA"
            confColor = "#00C853"
        elif topFc >= 70:
            confTexto = "IDENTIFICACIÓN PROBABLE — hay caracteres en conflicto"
            confColor = "#FFD600"
        else:
            confTexto = "IDENTIFICACIÓN TENTATIVA — hay caracteres en conflicto"
            confColor = "#FF6D00"

        mainCard = QFrame()
        mainCard.setObjectName("resultado_card")
        mainCard.setStyleSheet(
            f"QFrame#resultado_card {{ background: #0D2137; border: 2px solid {color}; border-radius: 12px; }}"
        )
        mainCardLayout = QVBoxLayout(mainCard)
        mainCardLayout.setContentsMargins(24, 20, 24, 20)
        mainCardLayout.setSpacing(10)

        confianzaBadge = QLabel(f"{confTexto}")
        confianzaBadge.setStyleSheet(
            f"background: {confColor}; color: #000; font-weight: bold; font-size: 12px; border-radius: 10px; padding: 4px 8px;"
        )
        confianzaBadge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        mainCardLayout.addWidget(confianzaBadge)

        if topDatos:
            bloquePrincipal = QHBoxLayout()
            bloquePrincipal.setSpacing(20)

            datosLayout = QVBoxLayout()
            datosLayout.setSpacing(10)

            nombreLbl = QLabel(f"<i>{topNombre}</i>")
            nombreLbl.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
            nombreLbl.setStyleSheet(f"color: {color};")
            datosLayout.addWidget(nombreLbl)

            autorLbl = QLabel(topDatos.get("autor", ""))
            autorLbl.setStyleSheet("color: #78909C; font-size: 13px;")
            datosLayout.addWidget(autorLbl)

            sep = QFrame()
            sep.setFrameShape(QFrame.Shape.HLine)
            sep.setStyleSheet("border: 1px solid #1A3A5C;")
            datosLayout.addWidget(sep)

            descLbl = QLabel(topDatos.get("descripcion", ""))
            descLbl.setWordWrap(True)
            descLbl.setStyleSheet("color: #B2EBF2; font-size: 13px; line-height: 1.6;")
            datosLayout.addWidget(descLbl)

            ecoLayout = QGridLayout()
            ecoLayout.setSpacing(8)
            ecoDatos = [
                ("Sustratos", ", ".join(topDatos.get("sustratos", []))),
                ("Estaciones", ", ".join(topDatos.get("estaciones", []))),
                ("Profundidad (m)",
                 f"{topDatos.get('profundidadM', (0, 0))[0]} - {topDatos.get('profundidadM', (0, 0))[1]}"),
                ("Distribucion", topDatos.get("distribucion", "")),
                ("Talla LE (mm)",
                 f"{topDatos['tallaMm']['LE_min']} - {topDatos['tallaMm']['LE_max']}"),
            ]
            for i, (k, v) in enumerate(ecoDatos):
                kLbl = QLabel(k)
                kLbl.setStyleSheet("color: #546E7A; font-size: 12px; font-weight: bold;")
                vLbl = QLabel(v)
                vLbl.setStyleSheet("color: #E0F7FA; font-size: 12px;")
                vLbl.setWordWrap(True)
                ecoLayout.addWidget(kLbl, i, 0)
                ecoLayout.addWidget(vLbl, i, 1)
            datosLayout.addLayout(ecoLayout)
            bloquePrincipal.addLayout(datosLayout, stretch=2)

            imgRuta = rutaRecurso(topDatos.get("imagen", ""))
            imgLbl = QLabel()
            imgLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            imgLbl.setStyleSheet(
                f"border: 1px solid {color}; background-color: #061021; border-radius: 8px;"
            )
            imgLbl.setFixedSize(320, 240)
            imgLbl.setToolTip("Imagen de referencia del especimen")

            if imgRuta and os.path.exists(imgRuta):
                pixmap = QPixmap(imgRuta).scaled(
                    310, 230, Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                imgLbl.setPixmap(pixmap)
            else:
                imgLbl.setText("Imagen no disponible")
                imgLbl.setStyleSheet(
                    "color: #546E7A; font-size: 13px; border: 1px dashed #1A3A5C; "
                    "background-color: #061021; border-radius: 8px;"
                )

            bloquePrincipal.addWidget(imgLbl, alignment=Qt.AlignmentFlag.AlignTop)
            mainCardLayout.addLayout(bloquePrincipal)

            notaFrame = QFrame()
            notaFrame.setStyleSheet("background: #061021; border-radius: 8px;")
            notaLayout = QVBoxLayout(notaFrame)
            notaLayout.setContentsMargins(12, 8, 12, 8)
            notaLbl = QLabel(
                f"Clave diagnostica: {topDatos.get('notaIdentificacion', '')}"
            )
            notaLbl.setWordWrap(True)
            notaLbl.setStyleSheet("color: #FFD600; font-size: 12px;")
            notaLayout.addWidget(notaLbl)
            mainCardLayout.addWidget(notaFrame)

        contLayout.addWidget(mainCard)

        if len(resultados) > 1:
            otrasLbl = QLabel("Otras especies consideradas (coincidencia parcial):")
            otrasLbl.setStyleSheet("color: #546E7A; font-size: 13px; font-weight: bold;")
            contLayout.addWidget(otrasLbl)
            for nombre, fc, datos in resultados[1:4]:
                if fc > 0:
                    c = datos.get("color", "#546E7A")
                    mini = QFrame()
                    mini.setToolTip(
                        f"{fc}% de caracteres observados coinciden con {nombre}"
                    )
                    mini.setStyleSheet(
                        f"background: #112240; border: 1px solid {c}; border-radius: 8px;"
                    )
                    miniLayout = QHBoxLayout(mini)
                    miniLayout.setContentsMargins(14, 10, 14, 10)
                    nLbl = QLabel(f"<i>{nombre}</i>  ({datos.get('autor', '')})")
                    nLbl.setStyleSheet(f"color: {c}; font-size: 13px;")
                    barraMini = QProgressBar()
                    barraMini.setValue(fc)
                    barraMini.setTextVisible(False)
                    barraMini.setFixedHeight(4)
                    barraMini.setFixedWidth(80)
                    pctLbl = QLabel(f"{fc}%")
                    pctLbl.setStyleSheet("color: #546E7A; font-size: 11px;")
                    miniLayout.addWidget(nLbl)
                    miniLayout.addStretch()
                    miniLayout.addWidget(barraMini)
                    miniLayout.addWidget(pctLbl)
                    contLayout.addWidget(mini)

        obsTitulo = QLabel("Observaciones registradas:")
        obsTitulo.setStyleSheet("color: #546E7A; font-size: 13px; font-weight: bold;")
        contLayout.addWidget(obsTitulo)

        obsFrame = QFrame()
        obsFrame.setStyleSheet("background: #061021; border-radius: 8px;")
        obsLayout = QVBoxLayout(obsFrame)
        obsLayout.setContentsMargins(14, 10, 14, 10)
        obsLayout.setSpacing(4)
        for pid in observaciones:
            val = observaciones[pid]
            p = next((q for q in preguntas if q["id"] == pid), None)
            if p:
                indicador = "SI" if val else "NO"
                lbl = QLabel(f"  [{indicador}]  {p['texto']}")
                lbl.setStyleSheet("color: #78909C; font-size: 11px;")
                lbl.setWordWrap(True)
                obsLayout.addWidget(lbl)
        contLayout.addWidget(obsFrame)

        contLayout.addStretch()
        scroll.setWidget(contenido)
        layout.addWidget(scroll)

        btnRow = QHBoxLayout()
        btnRow.setSpacing(10)

        if onVerCatalogo and topDatos:
            btnVerCatalogo = QPushButton("Ver en catalogo")
            btnVerCatalogo.setObjectName("btn_secundario")
            btnVerCatalogo.setFixedHeight(40)
            btnVerCatalogo.setToolTip("Ir al catalogo y ver la ficha completa de esta especie")
            btnVerCatalogo.clicked.connect(lambda: onVerCatalogo(topNombre))
            btnRow.addWidget(btnVerCatalogo)

        btnNuevo = QPushButton("Nuevo diagnostico")
        btnNuevo.setObjectName("btn_principal")
        btnNuevo.setFixedHeight(44)
        btnNuevo.setToolTip("Reiniciar y comenzar un nuevo diagnostico")
        btnNuevo.clicked.connect(onReiniciar)
        btnRow.addWidget(btnNuevo)

        layout.addLayout(btnRow)
