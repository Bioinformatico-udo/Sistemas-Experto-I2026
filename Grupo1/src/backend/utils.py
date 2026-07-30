# =============================================================================
# FUNCIONES AUXILIARES - LÓGICA DIFUSA
# ==========================================================================================================
# Este archivo contiene funciones matemáticas para el cálculo de grados de pertenencia en la lógica difusa.
# ==========================================================================================================

def triangular(x, a, b, c):
    """
    Función de pertenencia triangular.

    Args:
        x: Valor a evaluar.
        a: Límite inferior.
        b: Pico máximo (grado = 1).
        c: Límite superior.

    Returns:
        float: Grado de pertenencia entre 0 y 1.
    """
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0

def trapezoidal(x, a, b, c, d):
    """
    Función de pertenencia trapezoidal.

    Args:
        x: Valor a evaluar.
        a: Límite inferior.
        b: Inicio de la meseta (grado = 1).
        c: Fin de la meseta (grado = 1).
        d: Límite superior.

    Returns:
        float: Grado de pertenencia entre 0 y 1.
    """
    if x <= a or x >= d:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    return 0.0

def evaluar_incertidumbre(respuesta_usuario):
    """
    Convierte respuestas cualitativas en valores difusos (0 a 1).

    Args:
        respuesta_usuario: Respuesta textual del usuario.

    Returns:
        float: Grado de certeza entre 0 y 1.
    """
    if respuesta_usuario is None:
        return 0.5

    respuestas = {
        'si': 1.0,
        'sí': 1.0,
        's': 1.0,
        'no': 0.0,
        'n': 0.0,
        'tal vez': 0.5,
        'talvez': 0.5,
        'probablemente': 0.75,
        'probable': 0.75,
        'poco probable': 0.25,
        'dudoso': 0.4,
        'casi seguro': 0.9,
        'casi nada': 0.1
    }
    return respuestas.get(respuesta_usuario.lower(), 0.5)

def grado_tamano(valor_cm, categoria):
    """
    Función de pertenencia para el tamaño (pequeño, mediano, grande).

    Args:
        valor_cm: Tamaño en centímetros.
        categoria: 'pequeño', 'mediano' o 'grande'.

    Returns:
        float: Grado de pertenencia entre 0 y 1.
    """
    if valor_cm is None:
        return 0.5

    try:
        valor_cm = float(valor_cm)
    except (ValueError, TypeError):
        return 0.5

    if categoria == "pequeño":
        if valor_cm <= 1:
            return 1.0
        elif 1 < valor_cm <= 2:
            return 1.0 - (valor_cm - 1)
        elif 2 < valor_cm <= 3:
            return 3 - valor_cm
        else:
            return 0.0

    elif categoria == "mediano":
        if valor_cm < 2:
            return 0.0
        elif 2 <= valor_cm <= 3:
            return valor_cm - 2
        elif 3 < valor_cm <= 4:
            return 1.0
        elif 4 < valor_cm <= 5:
            return 5 - valor_cm
        else:
            return 0.0

    elif categoria == "grande":
        if valor_cm <= 4:
            return 0.0
        elif 4 < valor_cm <= 5:
            return valor_cm - 4
        else:
            return 1.0

    return 0.0

def grado_color(respuesta_usuario, color_esperado):
    """
    Evalúa el grado de certeza sobre el color.

    Args:
        respuesta_usuario: Respuesta textual del usuario.
        color_esperado: Color esperado (no utilizado, se mantiene por compatibilidad).

    Returns:
        float: Grado de certeza entre 0 y 1.
    """
    return evaluar_incertidumbre(respuesta_usuario)