# Walkthrough: Clasificación Híbrida Inteligente con Top 3 en la UI

Hemos rediseñado la interfaz del asistente de identificación por IA para presentar los resultados de una manera mucho más robusta y natural para modelos de Machine Learning, eliminando los mensajes binarios de fallo del motor.

## Cambios Implementados

1. **Ranking Híbrido Multicriterio**:
   - En lugar de realizar una validación dicotómica estricta de todo o nada (que falla fácilmente si hay ligeras discrepancias en la descripción del usuario), la pantalla de la IA ahora calcula un score continuo para las 41 especies registradas en el Parque Nacional Los Roques.
   - **Fórmula del Score**: `(Coincidencia Taxonómica de la Red * 0.5) + (Similitud Física de Texto * 0.5)`. Esto da un balance óptimo entre las características predichas por la red neuronal de TensorFlow y las palabras físicas explícitas en el texto del usuario.

2. **Nuevo Diseño de Resultados (Top 3)**:
   - **Recomendación Principal (Winner)**: Se destaca en la cabecera del resultado con un icono de verificación verde, detallando el nombre científico, nombre común, familia y
3. **Fusión e Integración Híbrida y Centralización del Ranking (`PredictorCorales`)**
- **Penalización Taxonómica**: Modificamos la obtención de confianza: las predicciones `desconocido` se marcan con confianza `0.0` para indicar falta de información taxonómica.
- **Detección de Baja Confianza**: Definimos que un análisis es de **baja confianza** si el promedio de las confianzas es `< 0.5` o si se logran predecir **menos de 3 características** taxonómicas activas.
- **Integración Semántica**: Si hay baja confianza, el predictor ejecuta la búsqueda semántica en la base de datos de especies. Si hay coincidencias semánticas, extrae las características taxonómicas reales de la especie ganadora y las combina/sobrescribe en las respuestas neuronales antes de enviarlas al motor.
- **Cálculo de Similitud Centralizado en el Backend**: Trasladamos el cálculo de similitud y ordenamiento de especies (`calcular_ranking_especies`) directamente al backend. Esto elimina duplicidades y permite al frontend cargar los resultados procesados listos para mostrar.
- **Filtro de Prefijos Robusto**: Ajustamos el motor de coincidencia de texto para requerir que las palabras coincidan por prefijo (`startswith`), evitando falsos positivos semánticos (por ejemplo, que la palabra `"rosa"` diera puntos a `"porosa"` en las especies del género *Millepora*).

4. **Mejoras del Dataset para Formas Masivas y Valles (Root Cause Fix)**:
   - Identificamos que el modelo confundía descripciones de corales cerebro (masivos con valles) asignándoles la clase de forma `"laminar"`.
   - **Enriquecimiento del Dataset**: Agregamos nuevos sinónimos en [`src/generador_dataset.py`](file:///c:/Users/Pc01/Desktop/Lazaro/Sistemas%20expertos/Sistemas-Experto-I2026/src/generador_dataset.py) para que la red neuronal los asocie correctamente:
     - Formas masivas: `"redondo"`, `"redonda"`, `"esférico"`, `"esférica"`, `"forma redonda"`.
     - Superficie de valles: `"surcos profundos"`, `"surcos"`, `"surcos sinuosos"`, `"canales"`.
   - **Algoritmo de Superposición Semántica (Overlap Coefficient)**: Modificamos [`src/ui/pantalla_ia.py`](file:///c:/Users/Pc01/Desktop/Lazaro/Sistemas%20expertos/Sistemas-Experto-I2026/src/ui/pantalla_ia.py) para calcular la similitud buscando en el nombre común, científico y descripción, empleando normalización de acentos y lematización básica de plurales en español.

---

## Verificación

* Ejecuta la aplicación utilizando la consola en su entorno virtual local:
  ```powershell
  .\venv\Scripts\python.exe -X utf8 -u -m src.main
  ```
* **Comportamiento**: Escribe cualquier descripción descriptiva, por ejemplo, `"Coral grande redondo con surcos profundos como cerebro, color gris, zona profunda"`. La interfaz te mostrará ahora correctamente a **Diploria labyrinthiformis** y **Pseudodiploria strigosa** (Coral Cerebro) con **67% de confianza** liderando el ranking, y la red neuronal clasificará de forma óptima las variables `p19 = masiva` y `p30 = valles`.
* **Animación de Carga por Pasos**: Al pulsar el botón de análisis, se muestra un stepper animado que simula las 4 etapas lógicas de clasificación (Lectura/Normalización, Red Neuronal Keras, Inferencia Semántica y Cómputo del Ranking) durante exactamente 2 segundos antes de desvelar el Top 5 de similitud.

