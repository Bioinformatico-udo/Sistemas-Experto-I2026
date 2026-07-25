# Manual Técnico - Sistema Experto Taxonómico Los Roques

Este manual contiene las especificaciones arquitectónicas, de diseño y detalles de la estructura interna del Sistema Experto.

## 🏗️ Arquitectura del Sistema

El sistema sigue una arquitectura modular en Python, separando claramente la base de conocimiento, la interfaz del usuario y el motor de inferencia.

```
├── src/
│   ├── main.py                 # Orquestador del sistema e interfaz por consola
│   ├── motor_inferencia.py     # Motor de razonamiento (recorrido del árbol de decisiones)
│   ├── base_conocimiento.py    # Clase que gestiona el acceso a JSONs de reglas y especies
│   ├── preguntas.py            # Formateo y captura de preguntas/respuestas del usuario
│   └── explicacion.py          # Módulo explicativo de inferencias y fallos
├── data/
│   ├── especies.json           # Base de datos de especies (atributos, hábitats, descripciones)
│   └── reglas.json             # Estructura del árbol dicotómico de decisiones
```

## ⚙️ Funcionamiento del Motor de Inferencia
El motor de inferencia (`MotorInferencia`) es **dirigido por el árbol de decisiones**. Recibe un estado acumulado (hechos/respuestas) y ejecuta las siguientes acciones:
1. Si el nodo actual contiene un `"resultado"`, se detiene con `estado = "exito"` y recupera la especie correspondiente.
2. Si el nodo actual requiere un `"atributo"`, revisa si ya se encuentra en las respuestas acumuladas:
   - Si **sí**, avanza al nodo hijo correspondiente y repite.
   - Si **no**, detiene la iteración con `estado = "pregunta"` y solicita al orquestador que formule la pregunta al usuario.
3. Si el usuario selecciona un camino sin salida o inconsistente, responde con `estado = "fallo"`.

## 🗂️ Representación del Conocimiento (Formatos JSON)

### Estructura de Especie (`data/especies.json`)
```json
{
  "id": "identificador_unico",
  "nombre_cientifico": "Nombre científico en latín",
  "nombre_comun": "Nombre vernáculo o común",
  "grupo": "Grupo taxonómico",
  "descripcion": "Descripción detallada",
  "habitat": "Zona geográfica/ecológica en Los Roques",
  "caracteristicas": {
    "atributo1": "valor1"
  }
}
```

### Estructura de Reglas (`data/reglas.json`)
Es un árbol n-ario (en la práctica, binario/dicotómico para claves taxonómicas) donde cada nodo intermedio tiene:
- `pregunta`: El texto a mostrar.
- `atributo`: La propiedad evaluada.
- `opciones`: Un diccionario cuyas claves son las posibles respuestas del usuario, mapeando hacia subárboles (otros nodos).
- O bien, un nodo hoja con `resultado`: El identificador de la especie clasificada.
