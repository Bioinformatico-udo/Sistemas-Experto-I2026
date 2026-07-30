ESTILO_MARINO = """
QMainWindow, QWidget {
    background-color: #0A192F;
    color: #E0F7FA;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
}
QLabel { color: #E0F7FA; }
QLabel#titulo { color: #00E5FF; font-size: 20px; font-weight: bold; }
QLabel#subtitulo { color: #80DEEA; font-size: 12px; }
QLabel#pregunta { color: #FFFFFF; font-size: 15px; font-weight: bold; }
QLabel#historial_label { color: #546E7A; font-size: 11px; font-weight: bold; }
QLabel#historial_item { color: #78909C; font-size: 11px; }
QLabel#contador_caracteres { color: #546E7A; font-size: 11px; }
QLabel#req_asterisco { color: #FF5252; font-size: 14px; font-weight: bold; }
QPushButton#btn_principal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006064, stop:1 #00838F);
    color: white; border: none; border-radius: 8px; padding: 12px 24px; font-size: 14px; font-weight: bold;
}
QPushButton#btn_principal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00838F, stop:1 #0097A7);
}
QPushButton#btn_principal:pressed { background: #004D40; }
QPushButton#btn_principal:disabled { background: #1A3A5C; color: #546E7A; }
QPushButton#btn_opcion {
    background: #112240; color: #B2EBF2; border: 2px solid #1A3A5C; border-radius: 10px; padding: 14px 20px; font-size: 13px; text-align: left;
}
QPushButton#btn_opcion:hover { background: #1A3A5C; border-color: #00BCD4; color: white; }
QPushButton#btn_opcion:pressed { background: #00338D; }
QPushButton#btn_opcion:focus { border-color: #00E5FF; }
QPushButton#btn_reset {
    background: #1A1A2E; color: #FF5252; border: 2px solid #FF5252; border-radius: 8px; padding: 8px 18px; font-size: 12px;
}
QPushButton#btn_reset:hover { background: #FF5252; color: white; }
QPushButton#btn_nav {
    background: transparent; color: #00E5FF; border: 1px solid #00838F; border-radius: 6px; padding: 6px 14px; font-size: 12px;
}
QPushButton#btn_nav:hover { background: #00838F; color: white; }
QPushButton#btn_nav:checked { background: #00838F; color: white; }
QPushButton#btn_nav_accion {
    background: transparent; color: #FFD600; border: 1px solid #FFD600; border-radius: 6px; padding: 6px 14px; font-size: 12px;
}
QPushButton#btn_nav_accion:hover { background: #FFD600; color: #000; }
QPushButton#btn_examinar {
    background: #112240; color: #80DEEA; border: 1px solid #1A3A5C; border-radius: 6px; padding: 4px 12px; font-size: 11px;
}
QPushButton#btn_examinar:hover { background: #1A3A5C; color: #00E5FF; border-color: #00BCD4; }
QPushButton#btn_back {
    background: transparent; color: #80DEEA; border: 1px solid #1A3A5C; border-radius: 6px; padding: 6px 14px; font-size: 11px;
}
QPushButton#btn_back:hover { background: #1A3A5C; color: #00E5FF; border-color: #00BCD4; }
QPushButton#btn_back:disabled { color: #1A3A5C; border-color: #0D2137; }
QPushButton#btn_secundario {
    background: transparent; color: #00E5FF; border: 1px solid #00BCD4; border-radius: 6px; padding: 8px 16px; font-size: 12px;
}
QPushButton#btn_secundario:hover { background: #00838F; color: white; }
QFrame#panel { background: #112240; border: 1px solid #1A3A5C; border-radius: 12px; }
QFrame#panel_historial { background: #061021; border: 1px solid #1A3A5C; border-radius: 8px; }
QFrame#header { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0D3B6E, stop:1 #0A1628); border-bottom: 2px solid #00838F; }
QFrame#resultado_card { background: #0D2137; border: 2px solid #00838F; border-radius: 12px; }
QTextBrowser { background: #0D2137; color: #B2EBF2; border: 1px solid #1A3A5C; border-radius: 8px; padding: 10px; font-size: 13px; line-height: 1.6; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { background: #0A1628; width: 8px; }
QScrollBar::handle:vertical { background: #1A3A5C; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QTreeWidget { background: #0D2137; color: #B2EBF2; border: 1px solid #1A3A5C; border-radius: 8px; alternate-background-color: #112240; font-size: 12px; }
QTreeWidget::item:hover { background: #1A3A5C; }
QTreeWidget::item:selected { background: #006064; color: white; }
QHeaderView::section { background: #0A1628; color: #00E5FF; padding: 6px; border: 1px solid #1A3A5C; font-weight: bold; }
QProgressBar { background: #0D2137; border: 1px solid #1A3A5C; border-radius: 4px; text-align: center; color: white; font-size: 11px; }
QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006064, stop:1 #00BCD4); border-radius: 4px; }
QStatusBar { background: #061021; color: #546E7A; border-top: 1px solid #1A3A5C; font-size: 11px; }
QDialog { background: #0A1628; }
QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox {
    background: #112240; color: #E0F7FA; border: 1px solid #1A3A5C; border-radius: 6px; padding: 6px;
}
QLineEdit:focus, QTextEdit:focus { border-color: #00BCD4; }
QLabel#form_label { color: #80DEEA; font-size: 12px; font-weight: bold; }
QCheckBox { color: #B2EBF2; spacing: 8px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #1A3A5C; background: #0D2137; }
QCheckBox::indicator:checked { background: #006064; border-color: #00BCD4; }
QGroupBox { color: #00E5FF; font-size: 13px; font-weight: bold; border: 1px solid #1A3A5C; border-radius: 8px; margin-top: 12px; padding-top: 16px; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }
QLabel#preview_label { border: 1px solid #1A3A5C; background-color: #061021; border-radius: 8px; }
QLineEdit#busqueda { background: #0D2137; color: #B2EBF2; border: 1px solid #1A3A5C; border-radius: 6px; padding: 6px; font-size: 12px; }
QLineEdit#busqueda:focus { border-color: #00BCD4; }
"""
