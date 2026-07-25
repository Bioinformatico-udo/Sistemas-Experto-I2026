# 📖 Manual de Usuario - Plataforma CoraAI (Los Roques)

Bienvenido a la guía de usuario del sistema experto **CoraAI**. Esta plataforma permite a biólogos, investigadores, estudiantes y entusiastas marinos clasificar e identificar especies de corales (*Scleractinia*) del **Parque Nacional Archipiélago de Los Roques**.

---

## 💻 1. Acceso a la Plataforma Web & Requisitos
- **Versión de Python**: **`Python 3.8 o superior`** (3.8 / 3.9 / 3.10 / 3.11).
- **Servidor**: Asegúrate de ejecutar el servidor con:
   ```bash
   python run_server.py
   ```
2. Abre tu navegador web (Chrome, Edge, Firefox, Safari) e ingresa a:
   👉 **`http://localhost:8000`**

---

## 🧭 2. Navegación Principal

La plataforma cuenta con una barra de navegación fija (*sticky header*) en la parte superior:
- **Inicio**: Presentación del sistema, tarjeta interactiva CTA de acceso rápido a los módulos y estadísticas del Parque Nacional.
- **Cuestionario**: Clave taxonómica dicotómica paso a paso.
- **Asistente IA**: Identificación inteligente por texto libre en lenguaje natural.
- **Catálogo**: Explorador completo de especies registradas con registro de nuevos corales.

---

## 📋 3. Módulo 1: Cuestionario Taxonómico Dicotómico

El Cuestionario utiliza la metodología de **IA Simbólica** basada en una serie de preguntas estructuradas de opción múltiple.

### Pasos de Uso:
1. Haz clic en **Cuestionario** en la barra superior.
2. Observarás una interfaz organizada en **2 columnas**:
   - **Columna Izquierda (Pregunta Activa & Progreso)**: Muestra la pregunta morfológica actual (ej. *¿Los coralitos son conspicuos u ocultos?*), la barra de porcentaje de avance y los botones de opción.
   - **Columna Derecha (Listado de Candidatos en Tiempo Real)**: Muestra pequeñas tarjetas horizontales con los nombres científicos y comunes de los corales que cumplen con tus respuestas hasta el momento.
3. Haz clic en la opción que mejor describa tu espécimen.
4. A medida que avanzas, la lista de candidatos de la derecha se reducirá progresivamente.
5. Al responder la última pregunta, aparecerá la **Tarjeta de Resultado Final** destacando la especie identificada junto a un recuadro con su fotografía taxonómica oficial.
6. Haz clic en **"Reiniciar Cuestionario"** para iniciar una nueva consulta.

---

## 🤖 4. Módulo 2: Diagnóstico por Lenguaje Natural con IA

El Asistente IA utiliza un enfoque **Híbrido (Red Neuronal TensorFlow + Motor de Ponderación Semántica)**.

### Pasos de Uso:
1. Haz clic en **Asistente IA** en la barra superior.
2. Se desplegará una pantalla en **2 columnas**:
   - **Columna Izquierda**:
     - **Caja de Texto Libre**: Describe la apariencia del coral en tus propias palabras (ej. *"Observé un coral ramificado de color marrón claro en zona somera con paletas aplanadas..."*).
     - **Sugerencias de 1 línea**: Haz clic en los botones de adición directa (`+ marrón`, `+ ramificada`, `+ masiva`, etc.) para autocompletar rápidamente palabras clave morfológicas.
     - **Demostraciones Rápidas**: Pruebas prefijadas (`Cuerno de Alce`, `Coral Cerebro`, `Coral de Fuego`).
     - **Botón "Ejecutar Diagnóstico IA"**.
   - **Columna Derecha**:
     - **Especie Ganadora #1**: Muestra el candidato con mayor porcentaje de similitud IA junto a su fotografía.
     - **Ranking de Especies Similares**: Lista ordenada de candidatos con sus porcentajes de coincidencia.
3. **Exploración de la Justificación Algorítmica (XAI)**:
   - Haz clic sobre la especie ganadora o sobre cualquiera de los candidatos del ranking.
   - Se abrirá el **Modal de Explicación IA**, el cual te revelará:
     - Foto y porcentaje de similitud.
     - Desglose de puntuación (Motor de Ponderación vs. Árbol de Reglas).
     - Coincidencias morfológicas verificadas (`✓`).
     - Atributos biológicos extraídos por la Red Neuronal desde tu texto.
     - Explicación narrativa de la razón de su lugar en el ranking.

---

## 🪸 5. Módulo 3: Catálogo de Especies & Registro

### Explorar Especies:
1. Haz clic en **Catálogo**.
2. Utiliza el **Buscador en Tiempo Real** para filtrar por nombre científico, común o familia.
3. Las tarjetas cuentan con carga por lotes procedimental para máxima fluidez.
4. Haz clic en **"Ver Detalle Completo"** en cualquier tarjeta para abrir el **Modal de Ficha Taxonómica** en 2 columnas con la fotografía de alta resolución, hábitat, estructura de corales e historia biológica.

### Registrar Nueva Especie:
1. En la parte superior derecha del Catálogo, haz clic en el botón verde **`+ Agregar Especie`**.
2. Rellena el formulario interactivo:
   - Identificador único (`especie_id`), Nombre Científico, Nombre Común, Familia y Orden.
   - Selecciona las características morfológicas principales (Forma de colonia, color, hábitat, coralitos).
   - Adjunta una fotografía del coral.
3. Haz clic en **"Guardar Especie"**. La nueva especie se integrará inmediatamente al archivo `especies.json` y al motor de inferencia de la aplicación.
