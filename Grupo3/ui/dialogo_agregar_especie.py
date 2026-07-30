import os
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QScrollArea, QFrame, QFileDialog,
    QWidget, QMessageBox, QColorDialog, QCheckBox, QComboBox
)
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt

from modelo.especies import (
    CLAVES_CARACTERES, agregarEspecieUsuario,
    importarEspeciesDeJson, ESPECIES, obtenerTodasLasEspecies
)


class DialogoAgregarEspecie(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar nueva especie")
        self.setMinimumSize(700, 600)
        self.setStyleSheet("background: #0A192F; color: #E0F7FA;")
        self._rutaImagen = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        titulo = QLabel("Agregar nueva especie")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #00E5FF;")
        layout.addWidget(titulo)

        sub = QLabel('Los campos marcados con <span style="color:#FF5252;">*</span> son obligatorios.')
        sub.setStyleSheet("color: #546E7A; font-size: 12px;")
        layout.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        formContenido = QWidget()
        formLayout = QVBoxLayout(formContenido)
        formLayout.setSpacing(10)

        self.campos = {}

        def addCampo(label, key, obligatorio=False, multilinea=False, tooltip="", comboItems=None):
            lbl = QLabel(f"{label}{' *' if obligatorio else ''}")
            lbl.setStyleSheet("color: #B2EBF2; font-size: 12px; font-weight: bold;")
            if tooltip:
                lbl.setToolTip(tooltip)

            campoFrame = QFrame()
            campoFrame.setStyleSheet(
                "background: #0D2137; border: 1px solid #1A3A5C; border-radius: 6px; padding: 2px;"
            )
            capa = QVBoxLayout(campoFrame)
            capa.setContentsMargins(4, 2, 4, 2)

            if comboItems:
                widget = QComboBox()
                widget.setEditable(True)
                widget.addItems(comboItems)
                widget.setCurrentText("")
                widget.lineEdit().setPlaceholderText(f"Seleccione o escriba {label.lower()}...")
                widget.setStyleSheet("background: transparent; color: #E0F7FA; border: none; font-size: 12px;")
            elif multilinea:
                widget = QTextEdit()
                widget.setFixedHeight(80)
                widget.setStyleSheet("background: transparent; color: #E0F7FA; border: none; font-size: 12px;")
                widget.setPlaceholderText(f"Ingrese {label.lower()}...")
                widget.setAcceptRichText(False)
            else:
                widget = QLineEdit()
                widget.setStyleSheet("background: transparent; color: #E0F7FA; border: none; font-size: 12px;")
                widget.setPlaceholderText(f"Ingrese {label.lower()}...")

            capa.addWidget(widget)
            self.campos[key] = widget

            if obligatorio:
                def obtenerTexto(w):
                    if isinstance(w, QTextEdit):
                        return w.toPlainText().strip()
                    if isinstance(w, QComboBox):
                        return w.currentText().strip()
                    return w.text().strip()
                fn = lambda: lbl.setStyleSheet(
                    "color: #FF5252; font-size: 12px; font-weight: bold;"
                    if obtenerTexto(widget) == ""
                    else "color: #B2EBF2; font-size: 12px; font-weight: bold;"
                )
                if isinstance(widget, QTextEdit):
                    widget.textChanged.connect(fn)
                elif isinstance(widget, QComboBox):
                    widget.currentTextChanged.connect(fn)
                else:
                    widget.textChanged.connect(fn)

            row = QVBoxLayout()
            row.addWidget(lbl)
            row.addWidget(campoFrame)
            formLayout.addLayout(row)

        addCampo("Nombre cientifico", "nombre", True, tooltip="Genero y especie (ej: Clibanarius erythropus)")
        generosExistentes = sorted(set(
            info["genero"] for info in obtenerTodasLasEspecies().values()
        ))
        addCampo("Genero", "genero", True, tooltip="Genero del especie", comboItems=generosExistentes)
        addCampo("Autor y ano", "autor", True, tooltip="Nombre del autor y ano de descripcion (ej: Latreille, 1817)")
        addCampo("Descripcion", "descripcion", True, True, tooltip="Descripcion morfologica breve de la especie")
        addCampo("Distribucion", "distribucion", tooltip="Localidades donde se ha reportado la especie")
        addCampo("Sustratos", "sustratos", tooltip="Tipos de sustrato separados por coma")
        addCampo("Estaciones", "estaciones", tooltip="Estaciones del ano separadas por coma")
        addCampo("Profundidad min (m)", "profMin")
        addCampo("Profundidad max (m)", "profMax")
        addCampo("Longitud del escudo min (LE mm)", "tallaMin")
        addCampo("Longitud del escudo max (LE mm)", "tallaMax")
        addCampo("Ancho del escudo min (AE mm)", "aeMin")
        addCampo("Ancho del escudo max (AE mm)", "aeMax")
        addCampo("Clave diagnostica", "notaIdentificacion", True, True, tooltip="Descripcion de los caracteres diagnosticos clave")
        addCampo("Fuente", "fuente", tooltip="Referencia bibliografica")

        # Imagen
        imgRow = QVBoxLayout()
        imgLbl = QLabel("Imagen (opcional)")
        imgLbl.setStyleSheet("color: #B2EBF2; font-size: 12px; font-weight: bold;")
        imgRow.addWidget(imgLbl)
        imgEnc = QHBoxLayout()
        self.rutaImagenLbl = QLabel("Ningun archivo seleccionado")
        self.rutaImagenLbl.setStyleSheet("color: #546E7A; font-size: 11px;")
        imgEnc.addWidget(self.rutaImagenLbl, stretch=1)
        btnImg = QPushButton("Examinar...")
        btnImg.setObjectName("btn_examinar")
        btnImg.setToolTip("Seleccionar una imagen JPG del especimen")
        btnImg.clicked.connect(self._seleccionarImagen)
        imgEnc.addWidget(btnImg)
        imgRow.addLayout(imgEnc)
        formLayout.addLayout(imgRow)

        # Color de acento
        colorRow = QVBoxLayout()
        colorLbl = QLabel("Color de acento *")
        colorLbl.setStyleSheet("color: #B2EBF2; font-size: 12px; font-weight: bold;")
        colorLbl.setToolTip("Color hexadecimal para resaltar la especie en la interfaz")
        colorRow.addWidget(colorLbl)

        colorEnc = QFrame()
        colorEnc.setStyleSheet("background: #0D2137; border: 1px solid #1A3A5C; border-radius: 6px;")
        colorEncLayout = QHBoxLayout(colorEnc)
        colorEncLayout.setContentsMargins(4, 2, 4, 2)

        self.colorPreview = QFrame()
        self.colorPreview.setFixedSize(28, 28)
        self.colorPreview.setStyleSheet("background: #00838F; border-radius: 4px;")
        colorEncLayout.addWidget(self.colorPreview)

        self.campos["color"] = QLineEdit()
        self.campos["color"].setText("#00838F")
        self.campos["color"].setStyleSheet("background: transparent; color: #E0F7FA; border: none; font-size: 12px;")
        self.campos["color"].textChanged.connect(self._actualizarColorPreview)
        colorEncLayout.addWidget(self.campos["color"], stretch=1)

        btnColor = QPushButton("Seleccionar color...")
        btnColor.setObjectName("btn_examinar")
        btnColor.setToolTip("Abrir selector de color")
        btnColor.clicked.connect(self._seleccionarColor)
        colorEncLayout.addWidget(btnColor)
        colorRow.addWidget(colorEnc)
        formLayout.addLayout(colorRow)

        # Caracteres diagnosticos
        caracTit = QLabel("Caracteres diagnosticos")
        caracTit.setStyleSheet("color: #00E5FF; font-size: 14px; font-weight: bold; margin-top: 8px;")
        formLayout.addWidget(caracTit)

        caracNota = QLabel("Marque los caracteres que PRESENTE esta especie (los no marcados se guardan como ausentes).")
        caracNota.setStyleSheet("color: #546E7A; font-size: 11px;")
        caracNota.setWordWrap(True)
        formLayout.addWidget(caracNota)

        self.checkboxes = {}
        for clave in sorted(CLAVES_CARACTERES):
            etiqueta = clave[0].upper() + "".join(
                " " + c if c.isupper() else c for c in clave[1:]
            )
            cb = QCheckBox(etiqueta)
            cb.setToolTip(clave)
            cb.setStyleSheet(
                "color: #B2EBF2; font-size: 11px; "
                "background: #0D2137; border: 1px solid #1A3A5C; border-radius: 4px; padding: 4px 8px;"
            )
            self.checkboxes[clave] = cb
            formLayout.addWidget(cb)

        scroll.setWidget(formContenido)
        layout.addWidget(scroll, stretch=1)

        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(10)

        btnImportar = QPushButton("Importar desde JSON")
        btnImportar.setObjectName("btn_examinar")
        btnImportar.setFixedHeight(36)
        btnImportar.setToolTip("Importar una o mas especies desde un archivo JSON")
        btnImportar.clicked.connect(self._importarJson)
        btnLayout.addWidget(btnImportar)

        btnExportar = QPushButton("Exportar a JSON")
        btnExportar.setObjectName("btn_examinar")
        btnExportar.setFixedHeight(36)
        btnExportar.setToolTip("Exportar los datos ingresados a un archivo JSON")
        btnExportar.clicked.connect(self._exportarJson)
        btnLayout.addWidget(btnExportar)

        btnLayout.addStretch()

        btnCancelar = QPushButton("Cancelar")
        btnCancelar.setObjectName("btn_back")
        btnCancelar.setFixedHeight(40)
        btnCancelar.setToolTip("Descartar cambios y cerrar")
        btnCancelar.clicked.connect(self.reject)
        btnLayout.addWidget(btnCancelar)

        self.btnGuardar = QPushButton("Guardar especie")
        self.btnGuardar.setObjectName("btn_principal")
        self.btnGuardar.setFixedHeight(44)
        self.btnGuardar.setToolTip("Guardar la nueva especie en la base de datos")
        self.btnGuardar.clicked.connect(self._guardar)
        btnLayout.addWidget(self.btnGuardar)

        layout.addLayout(btnLayout)
        self._ultimoColorValido = "#00838F"

    def _actualizarColorPreview(self):
        texto = self.campos["color"].text().strip()
        if texto.startswith("#") and len(texto) == 7:
            try:
                QColor(texto)
                self.colorPreview.setStyleSheet(f"background: {texto}; border-radius: 4px;")
                self._ultimoColorValido = texto
            except Exception:
                pass

    def _seleccionarColor(self):
        color = QColorDialog.getColor(QColor(self._ultimoColorValido), self, "Seleccionar color de acento")
        if color.isValid():
            hexColor = color.name()
            self.campos["color"].setText(hexColor)
            self.colorPreview.setStyleSheet(f"background: {hexColor}; border-radius: 4px;")
            self._ultimoColorValido = hexColor

    def _seleccionarImagen(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "", "Imagenes (*.jpg *.jpeg *.png *.bmp)"
        )
        if ruta:
            self._rutaImagen = ruta
            self.rutaImagenLbl.setText(os.path.basename(ruta))
            self.rutaImagenLbl.setStyleSheet("color: #80DEEA; font-size: 11px;")

    def _importarJson(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Importar especies desde JSON", "", "JSON (*.json)"
        )
        if not ruta:
            return
        try:
            count = importarEspeciesDeJson(ruta)
            total = len(obtenerTodasLasEspecies())
            QMessageBox.information(
                self, "Importacion exitosa",
                f"Se importaron {count} especie(s) correctamente.\n"
                f"Total de especies en la base: {total}\n\n"
                "Puede cerrar este dialogo y revisar el catalogo."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error de importacion",
                                 f"No se pudo importar el archivo:\n{e}")
            return
        self.accept()

    def _exportarJson(self):
        datos = self._recogerDatos()
        if not datos or not datos.get("nombre"):
            QMessageBox.warning(self, "Datos insuficientes",
                                "Complete al menos el nombre de la especie antes de exportar.")
            return
        nombreArchivo = datos["nombre"].replace(" ", "_").lower() + ".json"
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Exportar especie a JSON",
            nombreArchivo, "JSON (*.json)"
        )
        if not ruta:
            return
        try:
            exportData = {
                datos["nombre"]: {
                    "genero": datos["genero"],
                    "autor": datos["autor"],
                    "descripcion": datos["descripcion"],
                    "distribucion": datos.get("distribucion", ""),
                    "sustratos": [s.strip() for s in datos.get("sustratos", "").split(",") if s.strip()],
                    "estaciones": [e.strip() for e in datos.get("estaciones", "").split(",") if e.strip()],
                    "profundidadM": (
                        int(datos.get("profMin", 0) or 0),
                        int(datos.get("profMax", 0) or 0)
                    ),
                    "tallaMm": {
                        "LE_min": float(datos.get("tallaMin", 0) or 0),
                        "LE_max": float(datos.get("tallaMax", 0) or 0),
                        "AE_min": float(datos.get("aeMin", 0) or 0),
                        "AE_max": float(datos.get("aeMax", 0) or 0)
                    },
                    "color": datos.get("color", "#00838F"),
                    "notaIdentificacion": datos.get("notaIdentificacion", ""),
                    "fuente": datos.get("fuente", ""),
                    "caracteres": datos.get("caracteres", {}),
                    "imagen": datos.get("imagen", "")
                }
            }
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(exportData, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Exportacion exitosa",
                                    f"Especie exportada a:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error de exportacion",
                                 f"No se pudo exportar:\n{e}")

    def _textoCampo(self, key):
        w = self.campos[key]
        if isinstance(w, QTextEdit):
            return w.toPlainText().strip()
        if isinstance(w, QComboBox):
            return w.currentText().strip()
        return w.text().strip()

    def _recogerDatos(self):
        nombre = self._textoCampo("nombre")
        genero = self._textoCampo("genero")
        autor = self._textoCampo("autor")
        descripcion = self._textoCampo("descripcion")
        distribucion = self._textoCampo("distribucion")
        sustratos = self._textoCampo("sustratos")
        estaciones = self._textoCampo("estaciones")
        profMin = self._textoCampo("profMin")
        profMax = self._textoCampo("profMax")
        tallaMin = self._textoCampo("tallaMin")
        tallaMax = self._textoCampo("tallaMax")
        aeMin = self._textoCampo("aeMin")
        aeMax = self._textoCampo("aeMax")
        color = self._textoCampo("color")
        notaId = self._textoCampo("notaIdentificacion")
        fuente = self._textoCampo("fuente")

        if not color.startswith("#") or len(color) != 7:
            color = "#00838F"

        caracteres = {}
        for clave, cb in self.checkboxes.items():
            caracteres[clave] = cb.isChecked()

        return {
            "nombre": nombre,
            "genero": genero,
            "autor": autor,
            "descripcion": descripcion,
            "distribucion": distribucion,
            "sustratos": sustratos,
            "estaciones": estaciones,
            "profMin": profMin,
            "profMax": profMax,
            "tallaMin": tallaMin,
            "tallaMax": tallaMax,
            "aeMin": aeMin,
            "aeMax": aeMax,
            "color": color,
            "notaIdentificacion": notaId,
            "fuente": fuente,
            "imagen": self._rutaImagen,
            "caracteres": caracteres
        }

    def _guardar(self):
        datos = self._recogerDatos()

        if not datos["nombre"]:
            QMessageBox.warning(self, "Campo obligatorio", "El nombre cientifico es obligatorio.")
            return
        if not datos["genero"]:
            QMessageBox.warning(self, "Campo obligatorio", "El genero es obligatorio.")
            return
        if not datos["autor"]:
            QMessageBox.warning(self, "Campo obligatorio", "El autor es obligatorio.")
            return
        if not datos["descripcion"]:
            QMessageBox.warning(self, "Campo obligatorio", "La descripcion es obligatoria.")
            return
        if not datos["notaIdentificacion"]:
            QMessageBox.warning(self, "Campo obligatorio", "La clave diagnostica es obligatoria.")
            return

        nombre = datos["nombre"]
        if nombre in obtenerTodasLasEspecies():
            QMessageBox.warning(self, "Especie existente",
                                f"'{nombre}' ya existe en la base de datos.")
            return

        especiesDict = {
            "genero": datos["genero"],
            "autor": datos["autor"],
            "descripcion": datos["descripcion"],
            "distribucion": datos.get("distribucion", ""),
            "sustratos": [s.strip() for s in datos["sustratos"].split(",") if s.strip()],
            "estaciones": [e.strip() for e in datos["estaciones"].split(",") if e.strip()],
            "profundidadM": (
                int(datos["profMin"]) if datos["profMin"] else 0,
                int(datos["profMax"]) if datos["profMax"] else 0
            ),
            "tallaMm": {
                "LE_min": float(datos["tallaMin"]) if datos["tallaMin"] else 0.0,
                "LE_max": float(datos["tallaMax"]) if datos["tallaMax"] else 0.0,
                "AE_min": float(datos["aeMin"]) if datos["aeMin"] else 0.0,
                "AE_max": float(datos["aeMax"]) if datos["aeMax"] else 0.0
            },
            "color": datos["color"],
            "notaIdentificacion": datos["notaIdentificacion"],
            "fuente": datos.get("fuente", ""),
            "imagen": datos["imagen"],
            "caracteres": datos["caracteres"]
        }

        try:
            agregarEspecieUsuario(nombre, especiesDict)
            QMessageBox.information(
                self, "Especie agregada",
                f"'{nombre}' se ha agregado correctamente a la base de datos."
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"No se pudo guardar la especie:\n{e}")
