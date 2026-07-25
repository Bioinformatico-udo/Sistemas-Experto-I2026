class GeneradorExplicacion:
    """
    Generador de explicaciones para el sistema experto.
    Traduce el camino recorrido en el árbol de decisión a explicaciones legibles
    por humanos sobre 'cómo' y 'por qué' el sistema llegó a un diagnóstico.
    """
    def __init__(self):
        pass

    def explicar_exito(self, especie, camino):
        """
        Genera una explicación detallada del porqué se clasificó una especie.
        """
        explicacion = []
        explicacion.append("=" * 60)
        explicacion.append("📜 EXPLICACIÓN DEL DIAGNÓSTICO TAXONÓMICO")
        explicacion.append("=" * 60)
        explicacion.append(f"Organismo clasificado como: {especie['nombre_comun']} ({especie['nombre_cientifico']})")
        explicacion.append(f"Grupo: {especie['grupo']}")
        explicacion.append("-" * 60)
        explicacion.append("Pasos de inferencia seguidos (Árbol de Decisión):")
        
        for idx, (pregunta, respuesta) in enumerate(camino, 1):
            explicacion.append(f"  {idx}. {pregunta} -> Elegiste: '{respuesta}'")
            
        explicacion.append("-" * 60)
        explicacion.append("Información de la Especie:")
        explicacion.append(f"  • Descripción: {especie['descripcion']}")
        explicacion.append(f"  • Hábitat en Los Roques: {especie['habitat']}")
        
        caract_str = ", ".join([f"{k}: {v}" for k, v in especie['caracteristicas'].items()])
        explicacion.append(f"  • Características confirmadas: {caract_str}")
        explicacion.append("=" * 60)
        
        return "\n".join(explicacion)

    def explicar_fallo(self, mensaje, camino):
        """
        Genera una explicación de por qué falló el proceso de clasificación.
        """
        explicacion = []
        explicacion.append("=" * 60)
        explicacion.append("⚠️ DIAGNÓSTICO INCOMPLETO O NO LOGRADO")
        explicacion.append("=" * 60)
        explicacion.append(f"Motivo del fallo: {mensaje}")
        explicacion.append("-" * 60)
        explicacion.append("Camino recorrido antes del fallo:")
        
        if not camino:
            explicacion.append("  No se realizaron preguntas.")
        for idx, (pregunta, respuesta) in enumerate(camino, 1):
            explicacion.append(f"  {idx}. {pregunta} -> Elegiste: '{respuesta}'")
            
        explicacion.append("-" * 60)
        explicacion.append("Recomendación: Revise las características del organismo o amplíe la base de conocimiento.")
        explicacion.append("=" * 60)
        
        return "\n".join(explicacion)
