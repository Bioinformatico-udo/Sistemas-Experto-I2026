import sys
from pathlib import Path

# Configurar el paquete y el sys.path si se ejecuta directamente
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

import flet as ft
from .ui.pantallas import PantallaInicio, PantallaPreguntas, PantallaResultado, PantallaGuia
from .ui.pantalla_ia import PantallaIA
from .motor_inferencia import MotorInferencia
from .preguntas import generar_preguntas
from .modelo_hibrido import PredictorCorales  # NUEVO


class SistemaCoralesApp:
    """Aplicación principal del Sistema Experto - Modo Híbrido"""
    
    def __init__(self):
        self.motor = MotorInferencia()
        self.respuestas = {}
        self.historial_preguntas = []
        self.preguntas_dict = {}
        self.indice_pregunta = 0
        self.predictor = PredictorCorales()  # NUEVO
    
    def main(self, page: ft.Page):
        """Configuración y lanzamiento de la aplicación"""
        page.title = "Coral Expert System - Los Roques"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.window_width = 1200
        page.window_height = 760
        page.window_min_width = 900
        page.window_min_height = 640
        page.window_resizable = True
        page.window_maximized = True
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        # Cargar tipografía moderna premium Outfit
        page.fonts = {
            "Outfit": "https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/Outfit%5Bwght%5D.ttf"
        }
        page.theme = ft.Theme(font_family="Outfit")
        
        self.page = page
        
        # Definir callbacks de navegación global
        self.page.on_nav_inicio = self.mostrar_inicio
        self.page.on_nav_consulta = lambda: self.iniciar_cuestionario(None)
        self.page.on_nav_ia = self.iniciar_modo_ia
        self.page.on_nav_guia = self.mostrar_guia
        
        self.mostrar_inicio()
    
    def mostrar_inicio(self):
        pantalla = PantallaInicio(
            self.page,
            self.iniciar_cuestionario,
            self.iniciar_modo_ia,
            self.mostrar_guia,
        )
        pantalla.mostrar()
    
    def iniciar_cuestionario(self, e):
        self.respuestas = {}
        self.page.respuestas_acumuladas = {}
        self.historial_preguntas = []
        preguntas_lista = generar_preguntas()
        self.preguntas_dict = {p["id"]: p for p in preguntas_lista}
        self.indice_pregunta = 0
        self.mostrar_pregunta()
    
    def mostrar_pregunta(self):
        self.page.respuestas_acumuladas = self.respuestas
        resultado = self.motor.ejecutar(self.respuestas)
        
        if resultado.get("estado") == "pregunta":
            pregunta_id = resultado["pregunta_id"]
            pregunta = self.preguntas_dict.get(pregunta_id)
            
            if not pregunta:
                self.mostrar_resultado({
                    "success": False,
                    "especie": "Error de Sistema",
                    "mensaje": f"No se encontró la pregunta con ID: {pregunta_id}"
                })
                return
            
            self.indice_pregunta += 1
            total_estimado = 8
            
            pantalla = PantallaPreguntas(
                self.page, 
                pregunta, 
                self.indice_pregunta, 
                total_estimado,
                self.procesar_respuesta,
                self.mostrar_inicio
            )
            pantalla.mostrar()
        else:
            self.mostrar_resultado(resultado)
    
    def procesar_respuesta(self, respuesta):
        resultado = self.motor.ejecutar(self.respuestas)
        if resultado.get("estado") == "pregunta":
            pregunta_id = resultado["pregunta_id"]
            pregunta_actual = self.preguntas_dict.get(pregunta_id)
            
            if pregunta_actual:
                self.respuestas[pregunta_id] = respuesta
                
                label_respuesta = respuesta
                for opcion in pregunta_actual.get("opciones", []):
                    if opcion["valor"] == respuesta:
                        label_respuesta = opcion["label"]
                
                self.historial_preguntas.append({
                    "pregunta": pregunta_actual["texto"],
                    "respuesta": label_respuesta
                })
                
        self.mostrar_pregunta()
    
    def mostrar_resultado(self, resultado):
        pantalla = PantallaResultado(
            self.page,
            resultado,
            self.historial_preguntas,
            self.reiniciar
        )
        pantalla.mostrar()
    
    # ─── MODO IA ───
    
    def iniciar_modo_ia(self, e=None):
        pantalla = PantallaIA(
            self.page,
            predictor=self.predictor,
            motor=self.motor,
            on_volver=self.mostrar_inicio
        )
        pantalla.mostrar()
    
    def reiniciar(self, e):
        self.mostrar_inicio()

    def mostrar_guia(self):
        pantalla = PantallaGuia(
            self.page,
            on_volver=self.mostrar_inicio
        )
        pantalla.mostrar()


def main():
    app = SistemaCoralesApp()
    ft.run(app.main)


if __name__ == "__main__":
    main()