"""
tests/test_frontend.py
══════════════════════════════════════════════════════════════════════════════
Suite de tests de frontend para la interfaz del Sistema Experto Coral v2.
Prueba que cada pantalla se construye correctamente, que la navegación funciona
y que los datos se integran bien con la UI.

No requiere abrir una ventana real: se utiliza un MockPage que intercepta
todos los controles de Flet sin renderizar.
══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import types
import pytest

# ─── Asegurar que el paquete src sea importable ───────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# ─── MOCK DE FLET (sin ventana gráfica) ──────────────────────────────────────

class _FakeBorder:
    def all(self, *a, **kw):   return self
    def __call__(self, *a, **kw): return self
    left = right = top = bottom = None
    class BorderSide:
        def __init__(self, *a, **kw): pass

class _FakeControl:
    """Control genérico que acepta cualquier kwarg."""
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.controls = list(args) if args else []
        self.visible = kwargs.get("visible", True)
        self.value   = kwargs.get("value", "")
        self.open    = False
    def update(self): pass
    def __iter__(self): return iter(self.controls)

def _ctrl(*a, **kw):
    return _FakeControl(*a, **kw)


def _build_flet_mock():
    """Construye un módulo 'flet' falso que devuelve FakeControls."""
    ft = types.ModuleType("flet")

    # Controles básicos
    for name in [
        "Container", "Column", "Row", "Text", "Icon", "Divider",
        "TextField", "ElevatedButton", "OutlinedButton", "TextButton",
        "ProgressBar", "ProgressRing", "Image", "Stack", "CircleAvatar",
        "AlertDialog", "SnackBar", "Chip", "ResponsiveRow", "Ref",
    ]:
        setattr(ft, name, _ctrl)

    # Enums / helpers
    ft.Page = type("Page", (), {
        "clean": lambda s: None,
        "add":   lambda s, *a: None,
        "update": lambda s: None,
        "overlay": [],
        "bgcolor": None,
        "padding": 0,
        "dialog": None,
    })

    ft.MainAxisAlignment   = type("MAA", (), {
        "CENTER": "CENTER", "START": "START",
        "END": "END", "SPACE_BETWEEN": "SPACE_BETWEEN",
        "SPACE_AROUND": "SPACE_AROUND",
    })()
    ft.CrossAxisAlignment  = type("CAA", (), {
        "CENTER": "CENTER", "START": "START",
        "END": "END", "STRETCH": "STRETCH",
    })()
    ft.FontWeight          = type("FW", (), {
        "BOLD": "BOLD", "NORMAL": "NORMAL",
        "W_300": "W_300", "W_500": "W_500",
        "W_600": "W_600",
    })()
    ft.ScrollMode          = type("SM", (), {"ADAPTIVE": "ADAPTIVE"})()
    ft.TextAlign           = type("TA", (), {"CENTER": "CENTER", "LEFT": "LEFT"})()
    ft.TextOverflow        = type("TO", (), {"ELLIPSIS": "ELLIPSIS"})()
    ft.ImageFit            = type("IF", (), {"COVER": "COVER"})()
    ft.ThemeMode           = type("TM", (), {"DARK": "DARK"})()
    ft.ClipBehavior        = type("CB", (), {"HARD_EDGE": "HARD_EDGE"})()

    ft.Icons = type("Icons", (), {
        k: k for k in [
            "HOME_ROUNDED", "ASSIGNMENT_ROUNDED", "AUTO_AWESOME_ROUNDED",
            "MENU_BOOK_ROUNDED", "LOCATION_ON_ROUNDED", "SETTINGS_ROUNDED",
            "ARROW_BACK_IOS_NEW_ROUNDED", "CHECK_CIRCLE_OUTLINE_ROUNDED",
            "HIGHLIGHT_OFF_ROUNDED", "KEYBOARD_ARROW_RIGHT_ROUNDED",
            "REFRESH_ROUNDED", "DOWNLOAD_ROUNDED", "WATER_ROUNDED",
            "CATEGORY_ROUNDED", "ACCOUNT_TREE_ROUNDED", "VERIFIED_ROUNDED",
            "SEARCH_ROUNDED", "BIOTECH_ROUNDED", "PLACE_ROUNDED",
            "SPA_ROUNDED", "LAYERS_ROUNDED", "ADJUST_ROUNDED",
            "GRID_VIEW_ROUNDED", "CIRCLE_ROUNDED", "TERRAIN_ROUNDED",
            "HELP_OUTLINE_ROUNDED", "CLOSE_ROUNDED", "ARROW_FORWARD_ROUNDED",
            "COLOR_LENS_ROUNDED", "SHAPE_LINE_ROUNDED", "STRAIGHTEN_ROUNDED",
            "TEXTURE_ROUNDED", "UPLOAD_FILE_ROUNDED", "STAR_BORDER_ROUNDED",
            "INFO_OUTLINE_ROUNDED", "CHECK_CIRCLE_ROUNDED", "STAR_ROUNDED",
            "WAVES_ROUNDED", "MENU_ROUNDED", "KEYBOARD_ARROW_DOWN_ROUNDED",
            "DASHBOARD_ROUNDED", "FILTER_VINTAGE_ROUNDED",
        ]
    })()

    # Clases de layout/estilo
    class _Padding:
        def __init__(self, *a, **kw): pass
        def symmetric(self, *a, **kw): return self
        Padding = lambda *a, **kw: None
    ft.padding = _Padding()
    ft.padding.Padding = lambda *a, **kw: None
    ft.padding.symmetric = lambda *a, **kw: None

    class _Margin:
        Margin = lambda *a, **kw: None
    ft.margin = _Margin()
    ft.margin.Margin = lambda *a, **kw: None

    class _Alignment:
        def Alignment(self, *a, **kw): return self
        center = top_center = bottom_center = center_left = center_right = None
    ft.alignment = _Alignment()

    class _Border:
        def __call__(self, *a, **kw): return None
        def all(self, *a, **kw):      return None
        class BorderSide:
            def __init__(self, *a, **kw): pass
        class Border:
            def __init__(self, *a, **kw): pass
    ft.Border = _Border()
    ft.Border.BorderSide = lambda *a, **kw: None
    ft.BorderSide  = lambda *a, **kw: None
    ft.BorderRadius = lambda *a, **kw: None

    ft.BoxShadow  = _ctrl
    ft.Offset     = lambda *a: None
    ft.TextStyle  = _ctrl
    ft.LinearGradient = _ctrl

    ft.colors     = type("C", (), {"TRANSPARENT": "transparent"})()
    ft.Colors     = ft.colors

    # RoundedRectangleBorder / ButtonStyle
    ft.RoundedRectangleBorder = lambda *a, **kw: None
    ft.ButtonStyle = _ctrl
    ft.BorderSide  = lambda *a, **kw: None

    return ft


# Sustituir flet ANTES de cualquier import del proyecto
ft_mock = _build_flet_mock()
sys.modules["flet"] = ft_mock
sys.modules["flet.controls"] = ft_mock
sys.modules["flet.controls.alignment"] = ft_mock.alignment


# ─── MOCK PAGE ────────────────────────────────────────────────────────────────

class MockPage:
    """Simula ft.Page sin abrir ninguna ventana."""
    def __init__(self):
        self.bgcolor   = None
        self.padding   = 0
        self.overlay   = []
        self.dialog    = None
        self._controls = []
        self.respuestas_acumuladas = {}

    def clean(self):    self._controls.clear()
    def add(self, *c):  self._controls.extend(c)
    def update(self):   pass


# ─── MOCK PREDICTOR ───────────────────────────────────────────────────────────

class MockPredictor:
    def esta_cargado(self): return True
    def predecir_caracteristicas(self, texto):
        return {
            "success": True,
            "respuestas": {
                "p1": "s", "p4": "colonial",
                "p6": "no", "p19": "masiva",
            },
        }


class MockPredictorFallido:
    def esta_cargado(self): return False
    def predecir_caracteristicas(self, texto):
        return {"success": False, "error": "Modelo no disponible"}


class MockMotor:
    def ejecutar(self, respuestas): return {"estado": "pregunta", "pregunta_id": "p1"}


# ══════════════════════════════════════════════════════════════════════════════
# TESTS — PANTALLAS.PY
# ══════════════════════════════════════════════════════════════════════════════

class TestColorPalette:
    """Verifica que la paleta de colores esté completa."""

    def test_colores_definidos(self):
        from src.ui.pantallas import COLORS
        required = [
            "bg", "sidebar", "card", "card_border", "surface",
            "text_primary", "text_secondary", "text_muted",
            "accent", "cobalt", "success", "warning", "error",
        ]
        for key in required:
            assert key in COLORS, f"Falta color: {key}"

    def test_colores_son_hex(self):
        from src.ui.pantallas import COLORS
        for k, v in COLORS.items():
            assert v.startswith("#"), f"Color '{k}' no empieza con #: {v}"


class TestCrearSidebar:
    """Verifica que el sidebar se construye sin errores."""

    def test_sidebar_se_construye(self):
        from src.ui.pantallas import crear_sidebar
        page = MockPage()
        sidebar = crear_sidebar(
            page,
            active_screen="inicio",
            on_inicio=lambda: None,
            on_consulta=lambda: None,
            on_ia=lambda: None,
            on_guia=lambda: None,
        )
        assert sidebar is not None

    @pytest.mark.parametrize("screen", ["inicio", "consulta", "ia", "guia"])
    def test_sidebar_todas_las_pantallas(self, screen):
        from src.ui.pantallas import crear_sidebar
        page = MockPage()
        sidebar = crear_sidebar(
            page, active_screen=screen,
            on_inicio=lambda: None, on_consulta=lambda: None,
            on_ia=lambda: None,    on_guia=lambda: None,
        )
        assert sidebar is not None


class TestCrearShell:
    """Verifica que crear_shell llama page.clean() y page.add()."""

    def test_shell_llama_clean_y_add(self):
        from src.ui.pantallas import crear_shell, crear_sidebar
        page = MockPage()
        sidebar = crear_sidebar(
            page, "inicio",
            lambda: None, lambda: None, lambda: None, lambda: None,
        )
        contenido = ft_mock.Container(content=ft_mock.Text("test"))
        crear_shell(page, sidebar, contenido)
        assert len(page._controls) > 0


class TestPantallaInicio:
    """Verifica que PantallaInicio se renderiza correctamente."""

    def test_mostrar_sin_errores(self):
        from src.ui.pantallas import PantallaInicio
        page = MockPage()
        pantalla = PantallaInicio(
            page,
            on_iniciar=lambda e: None,
            on_modo_ia=lambda e=None: None,
            on_guia=lambda: None,
        )
        pantalla.mostrar()  # no debe lanzar excepción
        assert len(page._controls) > 0

    def test_callbacks_aceptados(self):
        from src.ui.pantallas import PantallaInicio
        llamado = {"iniciar": False, "ia": False}
        page = MockPage()
        pantalla = PantallaInicio(
            page,
            on_iniciar=lambda e: llamado.update({"iniciar": True}),
            on_modo_ia=lambda e=None: llamado.update({"ia": True}),
            on_guia=lambda: None,
        )
        pantalla.mostrar()
        assert pantalla.on_iniciar is not None
        assert pantalla.on_modo_ia is not None


class TestPantallaPreguntas:
    """Verifica que PantallaPreguntas se construye con preguntas reales."""

    @pytest.fixture
    def pregunta_muestra(self):
        return {
            "id": "p1",
            "texto": "¿El coral tiene coralitos visibles?",
            "descripcion": "Observa si hay pequeñas cavidades.",
            "opciones": [
                {"label": "Sí, tiene coralitos visibles", "valor": "s"},
                {"label": "No, la superficie es lisa", "valor": "no"},
            ],
        }

    def test_mostrar_sin_errores(self, pregunta_muestra):
        from src.ui.pantallas import PantallaPreguntas
        page = MockPage()
        pantalla = PantallaPreguntas(
            page, pregunta_muestra, numero=1, total=8,
            on_responder=lambda v: None,
            on_volver=lambda: None,
        )
        pantalla.mostrar()
        assert len(page._controls) > 0

    def test_opciones_multiples(self, pregunta_muestra):
        from src.ui.pantallas import PantallaPreguntas
        page = MockPage()
        pantalla = PantallaPreguntas(
            page, pregunta_muestra, numero=1, total=8,
            on_responder=lambda v: None,
            on_volver=lambda: None,
        )
        # Debe aceptar la pregunta con 2 opciones sin error
        pantalla.mostrar()
        assert pantalla.pregunta["id"] == "p1"

    @pytest.mark.parametrize("paso,total", [(1, 8), (3, 8), (8, 8)])
    def test_progress_stepper_pasos(self, paso, total, pregunta_muestra):
        from src.ui.pantallas import PantallaPreguntas
        page = MockPage()
        pantalla = PantallaPreguntas(
            page, pregunta_muestra, numero=paso, total=total,
            on_responder=lambda v: None,
            on_volver=lambda: None,
        )
        pantalla.mostrar()  # no debe romper en ningún paso


class TestPantallaResultado:
    """Verifica la pantalla de resultado con éxito y con fallo."""

    @pytest.fixture
    def resultado_exito(self):
        return {
            "success": True,
            "especie": "Diploria labyrinthiformis",
            "nombre_comun": "Coral Cerebro",
            "familia": "Merulinidae",
            "orden": "Scleractinia",
            "mensaje": "",
            "sugerencia": "",
        }

    @pytest.fixture
    def resultado_fallo(self):
        return {
            "success": False,
            "especie": "No identificada",
            "nombre_comun": "",
            "familia": "Desconocida",
            "orden": "Desconocido",
            "mensaje": "No se pudo clasificar con los datos proporcionados.",
            "sugerencia": "Intente responder más preguntas.",
        }

    @pytest.fixture
    def historial(self):
        return [
            {"pregunta": "¿Tiene coralitos?",    "respuesta": "Sí"},
            {"pregunta": "¿Es colonial?",         "respuesta": "Colonial"},
            {"pregunta": "¿Es ramificado?",       "respuesta": "No ramificada"},
            {"pregunta": "¿Es laminar o masiva?", "respuesta": "Masivo"},
        ]

    def test_mostrar_exito(self, resultado_exito, historial):
        from src.ui.pantallas import PantallaResultado
        page = MockPage()
        pantalla = PantallaResultado(
            page, resultado_exito, historial,
            on_reiniciar=lambda e: None,
        )
        pantalla.mostrar()
        assert len(page._controls) > 0

    def test_mostrar_fallo(self, resultado_fallo, historial):
        from src.ui.pantallas import PantallaResultado
        page = MockPage()
        pantalla = PantallaResultado(
            page, resultado_fallo, historial,
            on_reiniciar=lambda e: None,
        )
        pantalla.mostrar()
        assert len(page._controls) > 0

    def test_historial_vacio(self, resultado_exito):
        from src.ui.pantallas import PantallaResultado
        page = MockPage()
        pantalla = PantallaResultado(
            page, resultado_exito, [],
            on_reiniciar=lambda e: None,
        )
        pantalla.mostrar()  # no debe romper con historial vacío

    def test_limpia_respuestas_acumuladas(self, resultado_exito, historial):
        from src.ui.pantallas import PantallaResultado
        page = MockPage()
        page.respuestas_acumuladas = {"p1": "s", "p4": "colonial"}
        pantalla = PantallaResultado(
            page, resultado_exito, historial,
            on_reiniciar=lambda e: None,
        )
        pantalla.mostrar()
        assert page.respuestas_acumuladas == {}


class TestPantallaGuia:
    """Verifica el catálogo de especies."""

    def test_carga_especies_json(self):
        from src.ui.pantallas import PantallaGuia
        page = MockPage()
        pantalla = PantallaGuia(page, on_volver=lambda: None)
        # El JSON debe haberse cargado
        assert len(pantalla._todas) > 0, "No se cargaron especies desde JSON"

    def test_cantidad_minima_especies(self):
        from src.ui.pantallas import PantallaGuia
        page = MockPage()
        pantalla = PantallaGuia(page, on_volver=lambda: None)
        assert len(pantalla._todas) >= 40, (
            f"Se esperaban ≥40 especies, se encontraron {len(pantalla._todas)}"
        )

    def test_mostrar_sin_errores(self):
        from src.ui.pantallas import PantallaGuia
        page = MockPage()
        pantalla = PantallaGuia(page, on_volver=lambda: None)
        pantalla.mostrar()
        assert len(page._controls) > 0

    def test_campos_especie_presentes(self):
        from src.ui.pantallas import PantallaGuia
        page = MockPage()
        pantalla = PantallaGuia(page, on_volver=lambda: None)
        for esp in pantalla._todas:
            for campo in ["id", "nombre_cientifico", "nombre_comun", "familia"]:
                assert campo in esp, f"Especie sin campo '{campo}': {esp.get('id')}"


# ══════════════════════════════════════════════════════════════════════════════
# TESTS — PANTALLA_IA.PY
# ══════════════════════════════════════════════════════════════════════════════

class TestPantallaIA:
    """Verifica que la pantalla IA se construye y responde correctamente."""

    def test_mostrar_modelo_activo(self):
        from src.ui.pantalla_ia import PantallaIA
        page = MockPage()
        pantalla = PantallaIA(
            page,
            predictor=MockPredictor(),
            motor=MockMotor(),
            on_volver=lambda: None,
        )
        pantalla.mostrar()
        assert len(page._controls) > 0

    def test_mostrar_modelo_inactivo(self):
        from src.ui.pantalla_ia import PantallaIA
        page = MockPage()
        pantalla = PantallaIA(
            page,
            predictor=MockPredictorFallido(),
            motor=MockMotor(),
            on_volver=lambda: None,
        )
        pantalla.mostrar()
        assert len(page._controls) > 0

    def test_analizar_texto_vacio_dispara_error(self):
        from src.ui.pantalla_ia import PantallaIA
        page = MockPage()
        pantalla = PantallaIA(
            page,
            predictor=MockPredictor(),
            motor=MockMotor(),
            on_volver=lambda: None,
        )
        pantalla.mostrar()
        # Forzar campo vacío
        pantalla.campo_texto.value = ""
        errores = []
        _orig = pantalla._mostrar_error
        pantalla._mostrar_error = lambda m: errores.append(m)
        pantalla._analizar_texto(None)
        assert len(errores) == 1
        assert "descripción" in errores[0].lower()

    def test_analizar_texto_modelo_inactivo_dispara_error(self):
        from src.ui.pantalla_ia import PantallaIA
        page = MockPage()
        pantalla = PantallaIA(
            page,
            predictor=MockPredictorFallido(),
            motor=MockMotor(),
            on_volver=lambda: None,
        )
        pantalla.mostrar()
        pantalla.campo_texto.value = "coral masivo con valles"
        errores = []
        pantalla._mostrar_error = lambda m: errores.append(m)
        pantalla._analizar_texto(None)
        assert len(errores) == 1

    def test_estado_inicial_construye_catalogo(self):
        from src.ui.pantalla_ia import PantallaIA
        page = MockPage()
        pantalla = PantallaIA(
            page,
            predictor=MockPredictor(),
            motor=MockMotor(),
            on_volver=lambda: None,
        )
        catalogo = pantalla._construir_estado_inicial()
        assert catalogo is not None

    def test_badge_similitud_muy_similar(self):
        from src.ui.pantalla_ia import _get_badge
        label, color, bg = _get_badge(90)
        assert "similar" in label.lower()
        assert color.startswith("#")

    def test_badge_similitud_moderada(self):
        from src.ui.pantalla_ia import _get_badge
        label, color, bg = _get_badge(55)
        assert label is not None
        assert color.startswith("#")

    def test_badge_baja_similitud(self):
        from src.ui.pantalla_ia import _get_badge
        label, color, bg = _get_badge(20)
        assert "baja" in label.lower()

    def test_imagen_map_contiene_ids_validos(self):
        from src.ui.pantalla_ia import IMAGENES_MAP, IMAGENES_DIR
        for esp_id, filename in IMAGENES_MAP.items():
            assert isinstance(esp_id, str) and len(esp_id) > 0
            assert filename.endswith(".jpg") or filename.endswith(".png")


# ══════════════════════════════════════════════════════════════════════════════
# TESTS — FILTRAR_CANDIDATOS
# ══════════════════════════════════════════════════════════════════════════════

class TestFiltrarCandidatos:
    """Prueba la lógica de filtrado de candidatos taxonómicos en el sidebar."""

    def test_sin_respuestas_devuelve_todos(self):
        from src.ui.pantallas import filtrar_candidatos, LISTA_ESPECIES_ROQUES
        resultado = filtrar_candidatos({})
        assert len(resultado) == len(LISTA_ESPECIES_ROQUES)

    def test_hidrocoral_filtra_correctamente(self):
        from src.ui.pantallas import filtrar_candidatos
        resultado = filtrar_candidatos({"p1": "no"})
        assert all(c["grupo"] == "hidrocoral" for c in resultado)
        assert len(resultado) == 3

    def test_solitario_filtra_correctamente(self):
        from src.ui.pantallas import filtrar_candidatos
        resultado = filtrar_candidatos({"p1": "s", "p4": "solitario"})
        assert all(c["grupo"] == "solitario" for c in resultado)

    def test_ramificado_filtra_correctamente(self):
        from src.ui.pantallas import filtrar_candidatos
        resultado = filtrar_candidatos({"p1": "s", "p4": "colonial", "p6": "ramificado"})
        assert all(c["grupo"] == "ramificado" for c in resultado)

    def test_laminar_filtra_correctamente(self):
        from src.ui.pantallas import filtrar_candidatos
        resultado = filtrar_candidatos({"p1": "s", "p4": "colonial", "p6": "no", "p19": "laminar"})
        assert all(c["grupo"] == "laminar" for c in resultado)

    def test_masivo_filtra_correctamente(self):
        from src.ui.pantallas import filtrar_candidatos
        resultado = filtrar_candidatos({"p1": "s", "p4": "colonial", "p6": "no", "p19": "masiva"})
        assert all(c["grupo"] == "masivo" for c in resultado)

    def test_candidatos_tienen_campos_requeridos(self):
        from src.ui.pantallas import filtrar_candidatos, LISTA_ESPECIES_ROQUES
        resultado = filtrar_candidatos({})
        for c in resultado:
            assert "nombre"  in c, f"Falta 'nombre' en candidato: {c}"
            assert "familia" in c, f"Falta 'familia' en candidato: {c}"
            assert "grupo"   in c, f"Falta 'grupo' en candidato: {c}"


# ══════════════════════════════════════════════════════════════════════════════
# TESTS — NAVEGACIÓN
# ══════════════════════════════════════════════════════════════════════════════

class TestNavegacion:
    """Prueba que los callbacks de navegación se conectan correctamente."""

    def test_inicio_a_consulta(self):
        from src.ui.pantallas import PantallaInicio
        page = MockPage()
        consulta_iniciada = {"ok": False}
        pantalla = PantallaInicio(
            page,
            on_iniciar=lambda e: consulta_iniciada.update({"ok": True}),
            on_modo_ia=lambda e=None: None,
            on_guia=lambda: None,
        )
        pantalla.mostrar()
        # Simular clic en "Iniciar encuesta"
        pantalla.on_iniciar(None)
        assert consulta_iniciada["ok"] is True

    def test_inicio_a_ia(self):
        from src.ui.pantallas import PantallaInicio
        page = MockPage()
        ia_iniciada = {"ok": False}
        pantalla = PantallaInicio(
            page,
            on_iniciar=lambda e: None,
            on_modo_ia=lambda e=None: ia_iniciada.update({"ok": True}),
            on_guia=lambda: None,
        )
        pantalla.mostrar()
        pantalla.on_modo_ia()
        assert ia_iniciada["ok"] is True

    def test_preguntas_respuesta_callback(self):
        from src.ui.pantallas import PantallaPreguntas
        page = MockPage()
        respuesta_recibida = {"valor": None}

        pregunta = {
            "id": "p1",
            "texto": "¿El coral tiene coralitos?",
            "descripcion": "",
            "opciones": [{"label": "Sí", "valor": "s"}, {"label": "No", "valor": "no"}],
        }

        pantalla = PantallaPreguntas(
            page, pregunta, numero=1, total=8,
            on_responder=lambda v: respuesta_recibida.update({"valor": v}),
            on_volver=lambda: None,
        )
        pantalla.mostrar()
        # Simular selección de respuesta
        pantalla.on_responder("s")
        assert respuesta_recibida["valor"] == "s"

    def test_resultado_callback_reiniciar(self):
        from src.ui.pantallas import PantallaResultado
        page = MockPage()
        reiniciado = {"ok": False}
        pantalla = PantallaResultado(
            page,
            {"success": True, "especie": "Test", "nombre_comun": "",
             "familia": "F", "orden": "O", "mensaje": "", "sugerencia": ""},
            [],
            on_reiniciar=lambda e: reiniciado.update({"ok": True}),
        )
        pantalla.mostrar()
        pantalla.on_reiniciar(None)
        assert reiniciado["ok"] is True

    def test_ia_volver_callback(self):
        from src.ui.pantalla_ia import PantallaIA
        page = MockPage()
        volvio = {"ok": False}
        pantalla = PantallaIA(
            page,
            predictor=MockPredictor(),
            motor=MockMotor(),
            on_volver=lambda: volvio.update({"ok": True}),
        )
        pantalla.mostrar()
        pantalla.on_volver()
        assert volvio["ok"] is True


# ══════════════════════════════════════════════════════════════════════════════
# TESTS — DATOS (JSON)
# ══════════════════════════════════════════════════════════════════════════════

class TestDatosJSON:
    """Verifica la integridad del JSON de especies."""

    @pytest.fixture
    def especies(self):
        import json
        path = os.path.join(ROOT, "data", "especies.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_json_cargable(self, especies):
        assert isinstance(especies, list)
        assert len(especies) > 0

    def test_cantidad_especies(self, especies):
        assert len(especies) >= 40, (
            f"Se esperaban ≥40 especies, hay {len(especies)}"
        )

    def test_todos_tienen_id(self, especies):
        for esp in especies:
            assert "id" in esp and esp["id"], f"Especie sin id: {esp}"

    def test_ids_unicos(self, especies):
        ids = [e["id"] for e in especies]
        assert len(ids) == len(set(ids)), "Existen IDs duplicados en especies.json"

    def test_campos_obligatorios(self, especies):
        required = ["id", "nombre_cientifico", "nombre_comun",
                    "familia", "orden", "descripcion", "habitat"]
        for esp in especies:
            for campo in required:
                assert campo in esp, (
                    f"Especie '{esp.get('id')}' no tiene campo '{campo}'"
                )

    def test_familias_validas(self, especies):
        familias_conocidas = {
            "Milleporidae", "Stylasteridae", "Acroporidae", "Agariciidae",
            "Merulinidae", "Montastraeidae", "Siderastreidae", "Poritidae",
            "Faviidae", "Mussidae", "Meandrinidae", "Pocilloporidae",
            "Dendrophylliidae", "Rhizangiidae", "Astrocoeniidae",
        }
        for esp in especies:
            assert esp.get("familia") in familias_conocidas, (
                f"Familia desconocida '{esp.get('familia')}' en especie '{esp.get('id')}'"
            )

    def test_imagenes_disponibles_tienen_especie_correspondiente(self, especies):
        img_dir = os.path.join(ROOT, "data", "Imagenes")
        if not os.path.isdir(img_dir):
            pytest.skip("Directorio Imagenes no encontrado")
        ids_especies = {e["id"] for e in especies}
        for fname in os.listdir(img_dir):
            base = os.path.splitext(fname)[0]
            assert base in ids_especies, (
                f"Imagen '{fname}' no corresponde a ninguna especie registrada"
            )


# ══════════════════════════════════════════════════════════════════════════════
# TESTS — COMPONENTES UI AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════

class TestComponentesUI:
    """Prueba los helpers de UI de pantallas.py."""

    def test_neopill_activo(self):
        from src.ui.pantallas import NeoPill
        pill = NeoPill("Test", is_active=True)
        assert pill is not None

    def test_neopill_inactivo(self):
        from src.ui.pantallas import NeoPill
        pill = NeoPill("Test", is_active=False, on_click=lambda _: None)
        assert pill is not None

    def test_progress_stepper_completo(self):
        from src.ui.pantallas import ProgressStepper
        stepper = ProgressStepper(current=5, total=5)
        assert stepper is not None

    def test_progress_stepper_inicio(self):
        from src.ui.pantallas import ProgressStepper
        stepper = ProgressStepper(current=1, total=5)
        assert stepper is not None

    def test_lista_especies_roques_completa(self):
        from src.ui.pantallas import LISTA_ESPECIES_ROQUES
        assert len(LISTA_ESPECIES_ROQUES) == 40, (
            f"Se esperaban 40 especies, hay {len(LISTA_ESPECIES_ROQUES)}"
        )

    def test_grupos_de_especies(self):
        from src.ui.pantallas import LISTA_ESPECIES_ROQUES
        grupos = {c["grupo"] for c in LISTA_ESPECIES_ROQUES}
        expected = {"hidrocoral", "ramificado", "solitario", "laminar", "masivo"}
        assert grupos == expected, f"Grupos inesperados: {grupos}"
