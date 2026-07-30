from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont


class HeaderWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("header")
        self.setFixedHeight(80)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        iconLbl = QLabel("🦀")
        iconLbl.setFont(QFont("Segoe UI Emoji", 28))
        iconLbl.setFixedWidth(50)
        layout.addWidget(iconLbl)

        textoFrame = QVBoxLayout()
        titulo = QLabel("Sistema Experto — Familia Diogenidae")
        titulo.setObjectName("titulo")
        sub = QLabel("Basado en Lira (1997)")
        sub.setObjectName("subtitulo")
        textoFrame.addWidget(titulo)
        textoFrame.addWidget(sub)
        layout.addLayout(textoFrame)
        layout.addStretch()

        navLayout = QHBoxLayout()
        self.btnDiagnostico = QPushButton("Diagnóstico")
        self.btnDiagnostico.setToolTip("Iniciar o reanudar un diagnóstico (Ctrl+D)")
        self.btnCatalogo = QPushButton("Catálogo")
        self.btnCatalogo.setToolTip("Explorar todas las especies en la base de conocimiento (Ctrl+May+C)")
        self.btnAgregar = QPushButton("Agregar")
        self.btnAgregar.setToolTip("Agregar una nueva especie manualmente o desde JSON (Ctrl+May+A)")

        self.btnDiagnostico.setObjectName("btn_nav")
        self.btnDiagnostico.setCheckable(True)
        self.btnCatalogo.setObjectName("btn_nav")
        self.btnCatalogo.setCheckable(True)
        self.btnAgregar.setObjectName("btn_nav_accion")

        for btn in [self.btnDiagnostico, self.btnCatalogo, self.btnAgregar]:
            btn.setFixedHeight(32)
            navLayout.addWidget(btn)
        navLayout.setSpacing(6)
        layout.addLayout(navLayout)
