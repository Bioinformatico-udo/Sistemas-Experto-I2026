from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from modelo.especies import ESPECIES


class PantallaInicio(QWidget):
    def __init__(self, onIniciar, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(20)
        layout.addStretch()

        card = QFrame()
        card.setObjectName("panel")
        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(40, 35, 40, 35)
        cardLayout.setSpacing(18)

        emojiLbl = QLabel("🦀")
        emojiLbl.setFont(QFont("Segoe UI Emoji", 64))
        emojiLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(emojiLbl)

        t1 = QLabel("Sistema Experto de Identificación")
        t1.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        t1.setStyleSheet("color: #00E5FF;")
        t1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(t1)

        t2 = QLabel("Cangrejos Ermitaños · Familia Diogenidae")
        t2.setFont(QFont("Segoe UI", 14))
        t2.setStyleSheet("color: #B2EBF2;")
        t2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(t2)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("border: 1px solid #1A3A5C;")
        cardLayout.addWidget(sep)

        desc = QLabel(
            "Responda una serie de preguntas sobre las características morfológicas "
            "del espécimen para identificar la especie dentro de la familia "
            "<b>Diogenidae</b>.<br><br>"
            "Basado en la clave dicotómica de Provenzano (1959), adaptada por Lira (1997) "
            "para la Península de Macanao, Venezuela.<br><br>"
            "Puede <b>agregar nuevas especies</b> desde cualquier región de Venezuela "
            "usando el botón del menú superior."
        )
        desc.setStyleSheet("color: #90A4AE; font-size: 13px; line-height: 1.7;")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(desc)

        badgesLayout = QHBoxLayout()
        badgesLayout.setSpacing(8)
        generos = {}
        for nombre, datos in ESPECIES.items():
            gen = datos["genero"]
            generos[gen] = generos.get(gen, 0) + 1
        for gen, count in sorted(generos.items()):
            badge = QLabel(f"{gen} ({count})")
            badge.setStyleSheet(
                "background: #0D3B6E; color: #80DEEA; border: 1px solid #00838F; border-radius: 10px; padding: 3px 10px; font-size: 11px;"
            )
            badgesLayout.addWidget(badge)
        badgesLayout.addStretch()
        cardLayout.addLayout(badgesLayout)

        self.lblContador = QLabel()
        self.lblContador.setStyleSheet("color: #546E7A; font-size: 11px;")
        self.lblContador.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(self.lblContador)
        self._actualizarContador()

        btn = QPushButton("Iniciar Diagnóstico")
        btn.setObjectName("btn_principal")
        btn.setFixedHeight(48)
        btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        btn.setToolTip("Comenzar el diagnóstico interactivo")
        btn.clicked.connect(onIniciar)
        cardLayout.addWidget(btn)

        layout.addWidget(card)
        layout.addStretch()

    def _actualizarContador(self):
        from modelo.especies import obtenerTodasLasEspecies
        total = len(obtenerTodasLasEspecies())
        originales = len(ESPECIES)
        if total > originales:
            self.lblContador.setText(
                f"{originales} especies originales + {total - originales} agregadas por usuario"
            )
        else:
            self.lblContador.setText(f"{originales} especies registradas")
