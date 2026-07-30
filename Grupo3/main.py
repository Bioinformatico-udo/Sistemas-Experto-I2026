import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QStackedWidget, QStatusBar, QMessageBox
)
from PyQt6.QtGui import QFont, QShortcut, QKeySequence
from PyQt6.QtCore import Qt

from modelo.especies import cargarEspeciesUsuario, obtenerTodasLasEspecies
from modelo.preguntas import PREGUNTAS
from motor.inferencia import MotorInferencia
from ui.estilos import ESTILO_MARINO
from ui.widget_header import HeaderWidget
from ui.pantalla_inicio import PantallaInicio
from ui.pantalla_diagnostico import PreguntaWidget, ResultadoWidget
from ui.pantalla_catalogo import CatalogoWidget
from ui.dialogo_agregar_especie import DialogoAgregarEspecie


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        cargarEspeciesUsuario()
        self.setWindowTitle("Sistema Experto — Diogenidae | Macanao, Venezuela")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 780)
        self.setStyleSheet(ESTILO_MARINO)

        self.motor = MotorInferencia()
        self._construirUi()
        self._instalarAtajosGlobales()

    def _construirUi(self):
        central = QWidget()
        self.setCentralWidget(central)
        mainLayout = QVBoxLayout(central)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.header = HeaderWidget()
        self.header.btnDiagnostico.setChecked(True)
        mainLayout.addWidget(self.header)

        self.stack = QStackedWidget()
        mainLayout.addWidget(self.stack)

        self.pagInicio = PantallaInicio(self._iniciarDiagnostico)
        self.pagDiagnosticoContenido = QStackedWidget()
        self.pagCatalogo = CatalogoWidget(onVolver=lambda: self._navegar(0, self.header.btnDiagnostico))

        self.stack.addWidget(self.pagInicio)
        self.stack.addWidget(self.pagDiagnosticoContenido)
        self.stack.addWidget(self.pagCatalogo)

        navMap = [
            (self.header.btnDiagnostico, 0),
            (self.header.btnCatalogo, 2),
            (self.header.btnAgregar, None),
        ]
        for btn, idx in navMap:
            if idx is not None:
                btn.clicked.connect(lambda checked, i=idx, b=btn: self._navegar(i, b))
            else:
                btn.clicked.connect(self._abrirDialogoAgregar)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(
            "🦀  Sistema Experto — Diogenidae, Península de Macanao"
        )

    def _instalarAtajosGlobales(self):
        QShortcut(QKeySequence("Ctrl+D"), self, self._irADiagnostico)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, self._irACatalogo)
        QShortcut(QKeySequence("Ctrl+Shift+A"), self, self._abrirDialogoAgregar)

    def _irADiagnostico(self):
        if len(self.motor.observaciones) == 0 and self.pagDiagnosticoContenido.count() == 0:
            self.stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(1)
        self.header.btnDiagnostico.setChecked(True)
        self.header.btnCatalogo.setChecked(False)

    def _irACatalogo(self):
        self.stack.setCurrentIndex(2)
        self.header.btnDiagnostico.setChecked(False)
        self.header.btnCatalogo.setChecked(True)
        self.status.showMessage("Catálogo de especies")

    def _navegar(self, idx, btnActivo):
        for btn in [self.header.btnDiagnostico, self.header.btnCatalogo]:
            btn.setChecked(False)
        btnActivo.setChecked(True)

        if idx == 0:
            if (
                len(self.motor.observaciones) == 0
                and self.pagDiagnosticoContenido.count() == 0
            ):
                self.stack.setCurrentIndex(0)
            else:
                self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(idx)

    def _abrirDialogoAgregar(self):
        dialogo = DialogoAgregarEspecie(self)
        if dialogo.exec() == DialogoAgregarEspecie.DialogCode.Accepted:
            self.pagCatalogo.refrescar()
            self.status.showMessage(
                "Nueva especie agregada a la base de conocimiento."
            )

    def _iniciarDiagnostico(self):
        self.motor.reset()
        self.stack.setCurrentIndex(1)
        self.header.btnDiagnostico.setChecked(True)
        self.header.btnCatalogo.setChecked(False)
        self._mostrarSiguientePregunta()

    def _mostrarSiguientePregunta(self):
        siguiente = self.motor.siguientePregunta()
        totalPosibles = len(PREGUNTAS)
        respondidas = len(self.motor.observaciones)
        pct = int((respondidas / totalPosibles) * 100)

        if siguiente is None or self.motor.diagnosticoCompleto():
            resultados = self.motor.inferir()
            if not resultados:
                especies = obtenerTodasLasEspecies()
                resultados = list(especies.items())
            self._mostrarResultado(resultados)
            return

        num = respondidas + 1
        tieneAtras = len(self.motor.ordenRespuestas) > 0
        widgetP = PreguntaWidget(
            pregunta=siguiente,
            numActual=num,
            total=totalPosibles,
            progresoPct=pct,
            onRespuesta=self._onRespuesta,
            onReiniciar=self._reiniciar,
            onAtras=self._irAtras if tieneAtras else None,
            observaciones=dict(self.motor.observaciones),
            preguntas=PREGUNTAS,
        )
        while self.pagDiagnosticoContenido.count() > 0:
            w = self.pagDiagnosticoContenido.widget(0)
            self.pagDiagnosticoContenido.removeWidget(w)
            w.deleteLater()
        self.pagDiagnosticoContenido.addWidget(widgetP)
        self.pagDiagnosticoContenido.setCurrentWidget(widgetP)
        self.status.showMessage(
            f"Pregunta {num} — {siguiente['texto'][:60]}..."
        )

    def _irAtras(self):
        if not self.motor.ordenRespuestas:
            return
        self.motor.deshacerUltimaRespuesta()
        siguiente = self.motor.siguientePregunta()
        if siguiente is None:
            self._mostrarResultado(self.motor.inferir())
        else:
            self._mostrarSiguientePregunta()

    def _onRespuesta(self, preguntaId, valor):
        self.motor.registrarRespuesta(preguntaId, valor)
        resultados = self.motor.inferir()
        siguiente = self.motor.siguientePregunta()

        if siguiente is None or len(resultados) == 1:
            self._mostrarResultado(resultados)
        else:
            self._mostrarSiguientePregunta()

    def _irACatalogoConEspecie(self, nombre):
        self.stack.setCurrentIndex(2)
        self.header.btnDiagnostico.setChecked(False)
        self.header.btnCatalogo.setChecked(True)
        self.pagCatalogo.seleccionarEspecie(nombre)
        self.status.showMessage(f"Catálogo — {nombre}")

    def _mostrarResultado(self, resultados):
        while self.pagDiagnosticoContenido.count() > 0:
            w = self.pagDiagnosticoContenido.widget(0)
            self.pagDiagnosticoContenido.removeWidget(w)
            w.deleteLater()

        widgetR = ResultadoWidget(
            resultados=resultados,
            observaciones=self.motor.observaciones,
            preguntas=PREGUNTAS,
            onReiniciar=self._reiniciar,
            onVerCatalogo=self._irACatalogoConEspecie,
        )
        self.pagDiagnosticoContenido.addWidget(widgetR)
        self.pagDiagnosticoContenido.setCurrentWidget(widgetR)

        if resultados:
            nombre, fc, _ = resultados[0]
            self.status.showMessage(f"Diagnóstico completo: {nombre}")

    def _reiniciar(self):
        if self.motor.ordenRespuestas:
            respuesta = QMessageBox.question(
                self,
                "Reiniciar diagnóstico",
                "¿Está seguro de reiniciar el diagnóstico?\n"
                "Todas las respuestas se perderán.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if respuesta != QMessageBox.StandardButton.Yes:
                return

        self.motor.reset()
        while self.pagDiagnosticoContenido.count() > 0:
            w = self.pagDiagnosticoContenido.widget(0)
            self.pagDiagnosticoContenido.removeWidget(w)
            w.deleteLater()
        self.stack.setCurrentIndex(0)
        self.status.showMessage(
            "🦀  Sistema Experto — Diogenidae, Península de Macanao"
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema Experto Diogenidae")
    app.setOrganizationName("UDO - Biología Marina")
    app.setFont(QFont("Segoe UI", 11))

    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
