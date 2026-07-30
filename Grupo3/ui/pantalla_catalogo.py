import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTreeWidget, QTreeWidgetItem, QLineEdit,
    QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from modelo.especies import rutaRecurso, ESPECIES, obtenerTodasLasEspecies, eliminarEspecieUsuario


class CatalogoWidget(QWidget):
    def __init__(self, onVolver=None, parent=None):
        super().__init__(parent)
        self.especies = {}
        self._recargar()
        self.currentImage = None
        self._onVolver = onVolver
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(6)

        btnVolver = QPushButton("← Volver al inicio")
        btnVolver.setObjectName("btn_back")
        btnVolver.setToolTip("Regresar a la pantalla principal")
        if onVolver:
            btnVolver.clicked.connect(onVolver)
        layout.addWidget(btnVolver)

        titulo = QLabel("Catalogo de especies — Diogenidae")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #00E5FF;")
        layout.addWidget(titulo)

        sub = QLabel(
            "Seleccione una especie en el arbol de la izquierda para ver sus detalles"
        )
        sub.setStyleSheet("color: #546E7A; font-size: 12px;")
        layout.addWidget(sub)

        splitLayout = QHBoxLayout()
        splitLayout.setSpacing(16)

        leftPanel = QVBoxLayout()
        leftPanel.setSpacing(8)

        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar especie por nombre, autor o descripcion...")
        self.busqueda.setStyleSheet(
            "background: #0D2137; color: #E0F7FA; border: 1px solid #1A3A5C; "
            "border-radius: 6px; padding: 8px 12px; font-size: 12px;"
        )
        self.busqueda.textChanged.connect(self._filtrar)
        leftPanel.addWidget(self.busqueda)

        self.arbol = QTreeWidget()
        self.arbol.setHeaderHidden(True)
        self.arbol.setStyleSheet(
            "QTreeWidget { background: #0D2137; color: #B2EBF2; border: 1px solid #1A3A5C; "
            "border-radius: 6px; font-size: 12px; }"
            "QTreeWidget::item { padding: 4px 0; }"
            "QTreeWidget::item:selected { background: #00838F; color: white; }"
        )
        self.arbol.setMinimumWidth(260)
        self.arbol.setAnimated(True)
        self.arbol.currentItemChanged.connect(self._onItemSeleccionado)
        leftPanel.addWidget(self.arbol, stretch=1)

        splitLayout.addLayout(leftPanel, stretch=2)
        self._populateArbol()

        self.detalleScroll = QScrollArea()
        self.detalleScroll.setWidgetResizable(True)
        self.detalleScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.detalleWidget = QWidget()
        self.detalleLayout = QVBoxLayout(self.detalleWidget)
        self.detalleLayout.setSpacing(10)
        self._mostrarBienvenida()
        self.detalleScroll.setWidget(self.detalleWidget)
        splitLayout.addWidget(self.detalleScroll, stretch=3)

        layout.addLayout(splitLayout, stretch=1)

    def _recargar(self):
        self.especies = obtenerTodasLasEspecies()

    def _mostrarBienvenida(self):
        self._limpiarDetalle()
        bienvenida = QLabel(
            "Seleccione una especie del arbol para ver sus datos"
        )
        bienvenida.setStyleSheet("color: #546E7A; font-size: 14px; padding: 40px;")
        bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detalleLayout.addWidget(bienvenida)

    def _limpiarDetalle(self):
        while self.detalleLayout.count():
            item = self.detalleLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.currentImage = None

    def _populateArbol(self, filtro=""):
        self.arbol.clear()
        filtro = filtro.lower()
        generos = {}
        for nombre, datos in self.especies.items():
            gen = datos["genero"]
            if filtro:
                if (filtro not in nombre.lower() and
                        filtro not in datos.get("autor", "").lower() and
                        filtro not in datos.get("descripcion", "").lower()):
                    continue
            generos.setdefault(gen, []).append((nombre, datos))

        for gen in sorted(generos):
            genItem = QTreeWidgetItem(self.arbol, [gen])
            genItem.setFlags(genItem.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            genFont = QFont("Segoe UI", 12, QFont.Weight.Bold)
            genItem.setFont(0, genFont)
            genItem.setForeground(0, Qt.GlobalColor.cyan)

            for nombre, datos in sorted(generos[gen], key=lambda x: x[0]):
                esUsuario = nombre not in ESPECIES
                texto = nombre + (" (usuario)" if esUsuario else "")
                spItem = QTreeWidgetItem(genItem, [texto])
                spItem.setData(0, Qt.ItemDataRole.UserRole, nombre)

                if esUsuario:
                    spItem.setForeground(0, Qt.GlobalColor.yellow)

            genItem.setExpanded(True)

    def _filtrar(self, texto):
        self._populateArbol(texto)

    def seleccionarEspecie(self, nombreEspecie):
        if nombreEspecie in self.especies:
            self._mostrarDetalle(nombreEspecie, self.especies[nombreEspecie])
            self.busqueda.setText("")
            return
        for nombre in self.especies:
            if nombreEspecie.lower() in nombre.lower():
                self._mostrarDetalle(nombre, self.especies[nombre])
                self.busqueda.setText("")
                return
        QMessageBox.information(
            self, "No encontrada",
            f"La especie '{nombreEspecie}' no se encuentra en el catalogo."
        )

    def _onItemSeleccionado(self, current, previous):
        if current and current.data(0, Qt.ItemDataRole.UserRole):
            nombre = current.data(0, Qt.ItemDataRole.UserRole)
            if nombre in self.especies:
                self._mostrarDetalle(nombre, self.especies[nombre])

    def _mostrarDetalle(self, nombre, datos):
        self._limpiarDetalle()
        esUsuario = nombre not in ESPECIES

        card = QFrame()
        card.setObjectName("panel")
        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(24, 20, 24, 20)
        cardLayout.setSpacing(12)

        encabezado = QHBoxLayout()
        nomLbl = QLabel(f"<i>{nombre}</i>")
        nomLbl.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        nomLbl.setStyleSheet(f"color: {datos.get('color', '#00838F')};")
        encabezado.addWidget(nomLbl)
        encabezado.addStretch()
        if esUsuario:
            badge = QLabel("usuario")
            badge.setStyleSheet(
                "background: #FFD600; color: #000; font-size: 11px; font-weight: bold; "
                "padding: 3px 8px; border-radius: 8px;"
            )
            encabezado.addWidget(badge)
        cardLayout.addLayout(encabezado)

        autorLbl = QLabel(datos.get("autor", ""))
        autorLbl.setStyleSheet("color: #78909C; font-size: 13px;")
        cardLayout.addWidget(autorLbl)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("border: 1px solid #1A3A5C;")
        cardLayout.addWidget(sep)

        contDetalle = QHBoxLayout()
        contDetalle.setSpacing(20)

        textoLayout = QVBoxLayout()
        textoLayout.setSpacing(8)

        descLbl = QLabel(datos.get("descripcion", ""))
        descLbl.setWordWrap(True)
        descLbl.setStyleSheet("color: #E0F7FA; font-size: 13px;")
        textoLayout.addWidget(descLbl)

        textoLayout.addSpacing(4)
        gridDatos = QGridLayout()
        gridDatos.setSpacing(6)
        campos = [
            ("Distribucion", datos.get("distribucion", "")),
            ("Sustratos", ", ".join(datos.get("sustratos", [])) if isinstance(datos.get("sustratos"), list) else datos.get("sustratos", "")),
            ("Estaciones", ", ".join(datos.get("estaciones", []))),
            ("Profundidad (m)", f"{datos.get('profundidadM', (0, 0))[0]} - {datos.get('profundidadM', (0, 0))[1]}"),
            ("Longitud del escudo (LE mm)", f"{datos['tallaMm']['LE_min']} - {datos['tallaMm']['LE_max']}"),
            ("Ancho del escudo (AE mm)", f"{datos['tallaMm'].get('AE_min', '-')} - {datos['tallaMm'].get('AE_max', '-')}"),
        ]
        fila = 0
        for k, v in campos:
            if not v or v == " - ":
                continue
            kLbl = QLabel(k)
            kLbl.setStyleSheet("color: #546E7A; font-size: 12px; font-weight: bold;")
            vLbl = QLabel(v)
            vLbl.setStyleSheet("color: #E0F7FA; font-size: 12px;")
            vLbl.setWordWrap(True)
            gridDatos.addWidget(kLbl, fila, 0)
            gridDatos.addWidget(vLbl, fila, 1)
            fila += 1
        textoLayout.addLayout(gridDatos)
        contDetalle.addLayout(textoLayout, stretch=2)

        imgRuta = rutaRecurso(datos.get("imagen", ""))
        imgLbl = QLabel()
        imgLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imgLbl.setStyleSheet(
            f"border: 1px solid {datos.get('color', '#00838F')}; "
            f"background-color: #061021; border-radius: 8px;"
        )
        imgLbl.setFixedSize(300, 220)
        imgLbl.setToolTip("Imagen de referencia del especimen")

        if imgRuta and os.path.exists(imgRuta):
            pixmap = QPixmap(imgRuta).scaled(
                290, 210, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            imgLbl.setPixmap(pixmap)
            self.currentImage = imgRuta
        else:
            imgLbl.setText("Imagen no disponible")
            imgLbl.setStyleSheet(
                "color: #546E7A; font-size: 13px; border: 1px dashed #1A3A5C; "
                "background-color: #061021; border-radius: 8px;"
            )
        contDetalle.addWidget(imgLbl, alignment=Qt.AlignmentFlag.AlignTop)

        cardLayout.addLayout(contDetalle)

        if datos.get("notaIdentificacion"):
            notaFrame = QFrame()
            notaFrame.setStyleSheet("background: #061021; border-radius: 8px;")
            notaLayout = QVBoxLayout(notaFrame)
            notaLayout.setContentsMargins(12, 8, 12, 8)
            notaLbl = QLabel(
                f"Clave diagnostica: {datos['notaIdentificacion']}"
            )
            notaLbl.setWordWrap(True)
            notaLbl.setStyleSheet("color: #FFD600; font-size: 12px;")
            notaLayout.addWidget(notaLbl)
            cardLayout.addWidget(notaFrame)

        if datos.get("caracteres"):
            caracFrame = QFrame()
            caracFrame.setStyleSheet("background: #061021; border-radius: 8px;")
            caracLayout = QVBoxLayout(caracFrame)
            caracLayout.setContentsMargins(12, 8, 12, 8)
            caracTit = QLabel("Caracteres diagnosticos (clave dicotomica):")
            caracTit.setStyleSheet("color: #546E7A; font-size: 12px; font-weight: bold;")
            caracLayout.addWidget(caracTit)
            caracGrid = QGridLayout()
            caracGrid.setSpacing(3)
            fila = 0
            col = 0
            for k, v in datos["caracteres"].items():
                etiqueta = k[0].upper() + "".join(
                    " " + c if c.isupper() else c for c in k[1:]
                )
                estado = "SI" if v else "NO"
                colorEstado = "#00E676" if v else "#FF5252"
                cl = QLabel(etiqueta)
                cl.setStyleSheet("color: #80DEEA; font-size: 11px;")
                vl = QLabel(estado)
                vl.setStyleSheet(
                    f"color: {colorEstado}; font-size: 11px; font-weight: bold; "
                    f"background: #0D2137; border-radius: 4px; padding: 1px 6px;"
                )
                caracGrid.addWidget(cl, fila, 0)
                caracGrid.addWidget(vl, fila, 1)
                fila += 1
            caracLayout.addLayout(caracGrid)
            cardLayout.addWidget(caracFrame)

        if datos.get("fuente"):
            fuenFrame = QFrame()
            fuenFrame.setStyleSheet("background: #061021; border-radius: 8px;")
            fuenLayout = QVBoxLayout(fuenFrame)
            fuenLayout.setContentsMargins(12, 8, 12, 8)
            fuenLbl = QLabel(f"Fuente: {datos['fuente']}")
            fuenLbl.setWordWrap(True)
            fuenLbl.setStyleSheet("color: #78909C; font-size: 11px;")
            fuenLayout.addWidget(fuenLbl)
            cardLayout.addWidget(fuenFrame)

        self.detalleLayout.addWidget(card)

        if esUsuario:
            self.detalleLayout.addSpacing(6)
            btnEliminar = QPushButton("Eliminar esta especie de usuario")
            btnEliminar.setObjectName("btn_reset")
            btnEliminar.setFixedHeight(36)
            btnEliminar.setToolTip("Eliminar permanentemente esta especie agregada por el usuario")
            btnEliminar.clicked.connect(lambda: self._eliminarEspecie(nombre))
            self.detalleLayout.addWidget(btnEliminar)

        self.detalleLayout.addStretch()

    def refrescar(self):
        self._recargar()
        self._populateArbol()
        self._mostrarBienvenida()

    def _eliminarEspecie(self, nombre):
        resp = QMessageBox.question(
            self, "Confirmar eliminacion",
            f"Esta seguro de eliminar la especie '{nombre}'?\n"
            "Esta accion no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resp == QMessageBox.StandardButton.Yes:
            eliminarEspecieUsuario(nombre)
            self._recargar()
            self._populateArbol()
            self._mostrarBienvenida()
