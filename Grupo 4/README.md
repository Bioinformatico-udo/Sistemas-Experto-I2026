# Clasificador de Crustáceos Porcellanidae

## Integrantes del Grupo

- Br. Jesús Rodríguez — C.I. V-30685591
- Br. Alejandra Méndez — C.I. V-30919860
- Br. Wilmer Moreno — C.I. V-30911319

---

## Descripción General

El Clasificador de Crustáceos Porcellanidae es un sistema experto interactivo concebido para resolver la ambigüedad en la identificación taxonómica de los crustáceos pertenecientes a la familia Porcellanidae (falsos cangrejos o cangrejos de porcelana, pertenecientes al infraorden Anomura).

### Problema y Dominio del Conocimiento
A nivel de campo o laboratorio, los especímenes de Porcellanidae se confunden fácilmente con los cangrejos verdaderos (infraorden Brachyura) debido a su abdomen reducido plegado bajo el cefalotórax. Además, la diferenciación interna a nivel de género y especie requiere la evaluación de rasgos morfológicos sutiles (estructura de los segmentos antenales, suturas del caparazón, número de membranas branquiales, número de placas del telson y textura de los quelípedos). Tradicionalmente, este proceso se realiza mediante claves dicotómicas impresas extensas que resultan complejas para estudiantes e investigadores sin experiencia especializada.

### Utilidad del Sistema Experto
La herramienta automatiza la evaluación taxonómica guiando al usuario a través de un cuestionario dinámico adaptativo. Evalúa únicamente las características morfológicas necesarias para deducir la especie o determinar si el ejemplar no pertenece a la familia o subfilo, ofreciendo un diagnóstico respaldado por un reporte transparente de explicabilidad lógica.

---

## Arquitectura del Sistema

### Descripción de la Base de Conocimientos
La base de conocimientos está desacoplada del motor de inferencia mediante archivos en formato JSON declarativo (`src/backend/app/data/`):
- **Hechos y Preguntas (`rules.json`):** Define el catálogo de atributos morfológicos observables (`numero_antenas`, `segmento_antenal`, `paredes_caparazon`, `membranas_area_branquial`, `superficie_quelipedo`, entre otros) y las preguntas con opciones estructuradas presentadas al usuario.
- **Catálogo de Especies (`species.json`):** Contiene las fichas taxonómicas, descripciones y conjuntos de atributos requeridos para identificar cada especie.

#### Especies Registradas en la Base de Conocimientos:
- *Neopisosoma cf. neglectum*
- *Neopisosoma angustifrons*
- *Neopisosoma orientale*
- *Clastotoechus nodosus*
- *Pachycheles serratus*
- *Pachycheles monilifer*
- *Pachycheles riseii*
- *Pachycheles ackleianus*
- *Petrolisthes tridentatus*
- *Petrolisthes tonsorius*
- *Petrolisthes jugosus*
- *Petrolisthes politus*
- *Petrolisthes lewisi*
- *Petrolisthes armatus*
- *Petrolisthes galathinus*
- *Petrolisthes marginatus*
- *Minyocerus angustus*
- *Megalobrachium soriatum*
- *Megalobrachium mortenseni*
- *Megalobrachium poeyi*
- *Megalobrachium roseum*
- *Pisidia brasiliensis*
- *Porcellana sayana*

### Explicación del Motor de Inferencia
El motor de inferencia está desarrollado en Python 3.11+ aplicando la metodología de ingeniería del conocimiento de Buchanan y los principios de la Arquitectura Hexagonal:
- **Estrategia de Razonamiento:** Utiliza **Encadenamiento hacia Adelante (Forward Chaining)**. Partiendo de las premisas morfológicas recolectadas (hechos), el motor evalúa iterativamente las reglas de producción para inferir nuevos hechos de nivel superior (subfilo, familia, género) hasta concluir en la especie o declarar un descarte.
- **Mecanismo de Explicabilidad:** Registra cada regla disparada en orden cronológico, generando una traza justificativa que explica al usuario el porqué de la conclusión taxonómica.
- **Extensibilidad:** El sistema permite incorporar nuevas especies directamente desde la interfaz web mediante el modal **Agregar especie** (previa autenticación con usuario `admin` y contraseña `Admin`). La aplicación persiste el registro en `src/backend/app/data/species.json`, de modo que el motor de inferencia lo incorpora automáticamente sin necesidad de modificar código.

### Diagrama de Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph Frontend["Interfaz Web (Vue.js 3 + Vite)"]
        UI["HomeView / DiagnosisView"] -->|1. Selección de Hechos Morfológicos| STORE["Pinia Store (diagnosisStore)"]
        STORE -->|2. Petición HTTP REST| API_CLIENT["Servicio API (api.js)"]
        RESULT_VIEW["ResultView (Ficha + Explicabilidad)"] <--|5. Respuesta con Especie y Justificación| STORE
    end

    subgraph Backend["Backend FastAPI (Arquitectura Hexagonal)"]
        API_CLIENT -->|3. Controlador REST (Adapters)| CTRL["Inference Router"]
        CTRL -->|4. Ejecución de Inferencia| ENGINE["Motor Forward Chaining (Domain)"]
        ENGINE <-->|Consulta de Reglas y Especies| KB["Base de Conocimientos (JSON)"]
    end
```

### Recursos Educativos
El sistema integra fichas informativas con descripciones anatómicas, hábitats naturales y un catálogo interactivo que sirve como recurso didáctico para la docencia universitaria en taxonomía de decápodos anomuros.

---

## Instalación y Configuración

### Prerrequisitos
- **Python:** 3.11 o superior.
- **Node.js:** 18.0.0 o superior con el gestor de paquetes `npm`.
- **Git:** Instalado en la consola de comandos.

### Instrucciones Paso a Paso

1. **Clonación del Repositorio:**
   ```bash
   git clone https://github.com/Bioinformatico-udo/Sistemas-Experto-I2026.git
   git switch Grupo4
   cd Sistemas-Experto-I2026/"Grupo 4"
   ```

2. **Configuración y Ejecución del Backend (FastAPI):**
   Navegue al directorio del backend y cree el entorno virtual:
   ```bash
   cd src/backend
   python -m venv venv
   ```
   - En Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
   - En Linux / macOS: `source venv/bin/activate`

   Instale las dependencias y ejecute el servidor API:
   ```bash
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload
   ```
   El backend estará disponible en `http://127.0.0.1:8000` (documentación de la API en `/docs`).

3. **Configuración y Ejecución del Frontend (Vue.js 3):**
   En una nueva terminal, navegue al frontend e inicie el servidor de desarrollo:
   ```bash
   cd src/frontend
   npm install
   npm run dev
   ```
   La interfaz web estará disponible en `http://localhost:5173`.

4. **Ejecución de Pruebas Automatizadas:**
   Desde la carpeta `src/backend`:
   ```bash
   pytest tests/
   ```
   O de forma alternativa mediante el módulo de Python con salida detallada:
   ```bash
   python -m pytest -v
   ```

---

## Guía de Uso

### Modo de Interacción con el Sistema
El sistema ofrece dos vías de interacción según las necesidades del usuario:

1. **Interfaz Web Interactiva (Recomendado):**
   Accediendo a `http://localhost:5173`, el usuario inicia el diagnóstico asistido. El sistema despliega tarjetas con preguntas morfológicas de selección múltiple (como tipo de segmento antenal o suturas del caparazón). A medida que se responde cada pregunta, el motor reevalúa las reglas y solicita únicamente las variables adicionales pertinentes.

2. **API REST / Consola de Comandos (cURL / Postman):**
   Se pueden enviar conjuntos de hechos en formato JSON mediante peticiones HTTP POST a la ruta `/api/v1/inference/evaluate` para recibir el diagnóstico estructurado directamente sin usar la interfaz gráfica.

### Explicación de la Interfaz Web
- **Vista Principal (`HomeView.vue`):** Pantalla de bienvenida, acceso al catálogo completo de especies y botón de inicio de diagnóstico.
- **Vista de Diagnóstico (`DiagnosisView.vue`):** Indicador de progreso adaptativo, tarjeta de la pregunta actual (`DiagnosisCard.vue`) y estado de consulta en tiempo real.
- **Vista de Resultados (`ResultView.vue`):** Despliega la especie identificada, su fotografía, hábitat, clasificación taxonómica estructurada y el panel de explicabilidad con las reglas disparadas.
- **Modal de Inicio de Sesión (`LoginModal.vue`):** Permite al usuario autenticarse como experto para desbloquear la gestión de la base de conocimientos.
- **Modal Agregar Especie (`AddSpeciesModal.vue`):** Formulario exclusivo para usuarios autenticados que permite incorporar nuevas especies a la base de datos morfológica.

### Autenticación para la Gestión de Especies
Para registrar nuevas especies en el sistema desde la interfaz web, se requiere iniciar sesión como usuario experto desde el botón de acceso en la barra superior. Las credenciales predeterminadas de administración son:

- **Usuario:** `admin`
- **Contraseña:** `Admin`

Al iniciar sesión con estas credenciales, el sistema activa los privilegios de experto y habilita el modal de **Agregar especie**, guardando automáticamente los nuevos datos morfológicos en `species.json` de manera persistente.

---

## Ejemplos de Ejecución

### Ejemplo 1: Clasificación Exitosa de *Neopisosoma cf. neglectum* (Vía API REST)

**Entrada (Petición JSON):**
```json
{
  "facts": {
    "numero_antenas": 2,
    "segmento_antenal": "corto",
    "paredes_caparazon": "incompletas",
    "membranas_area_branquial": "unica",
    "superficie_quelipedo": "lisa"
  }
}
```

**Salida / Diagnóstico Obtenido:**
```json
{
  "status": "COMPLETED",
  "identified_species": {
    "id": "Neopisosoma_cf_neglectum",
    "name": "Neopisosoma cf. neglectum",
    "description": "Especie de Porcellanidae caracterizada por quelípedos lisos sin granos ni tubérculos y carpo con tres crestas dorsales longitudinales.",
    "habitat": "Zona costera rocosa.",
    "taxonomy": {
      "kingdom": "Animalia",
      "phylum": "Arthropoda",
      "subphylum": "Crustacea",
      "class": "Malacostraca",
      "order": "Decapoda",
      "infraorder": "Anomura",
      "family": "Porcellanidae",
      "genus": "Neopisosoma",
      "species": "Neopisosoma cf. neglectum"
    }
  },
  "justification": [
    "Regla R-CRUST-01: Se confirmó el subfilo Crustacea al poseer 2 pares de antenas.",
    "Regla R-PORC-02: Se confirmó la familia Porcellanidae al presentar el segmento antenal basal corto.",
    "Regla R-NEO-05: Se determinó el género Neopisosoma por paredes del caparazón incompletas y membrana branquial única.",
    "Regla R-NEO-NEG-01: Se concluyó la especie Neopisosoma cf. neglectum debido a la superficie lisa del quelípedo."
  ],
  "confidence": 1.0
}
```

### Ejemplo 2: Flujo Interactivo y Salida en Interfaz Web (Frontend)

**1. Interacción en Pantalla:**
- El usuario selecciona `2 pares de antenas` y `segmento antenal corto`.
- El sistema consulta el motor y recomienda la pregunta de paredes del caparazón (`Incompletas`).
- El usuario indica `Superficie del quelípedo lisa`.

**2. Renderizado del Resultado Final (`ResultView.vue`):**

```text
+-------------------------------------------------------------------------------+
|                        RESULTADO DEL DIAGNÓSTICO                             |
+-------------------------------------------------------------------------------+
| ESPECIE IDENTIFICADA: Neopisosoma cf. neglectum                              |
| NIVEL DE CERTEZA:     100% (Inferencia Lógica Completa)                       |
| HÁBITAT:              Zona costera rocosa                                     |
+-------------------------------------------------------------------------------+
| TAXONOMÍA DETALLADA:                                                          |
| Reino: Animalia | Filo: Arthropoda | Clase: Malacostraca | Orden: Decapoda   |
| Infraorden: Anomura | Familia: Porcellanidae | Género: Neopisosoma            |
+-------------------------------------------------------------------------------+
| PANEL DE EXPLICABILIDAD (CADENA DE REGLAS DISPARADAS):                        |
| [v] R-CRUST-01 : 2 pares de antenas -> Subfilo Crustacea                      |
| [v] R-PORC-02  : Segmento antenal corto -> Familia Porcellanidae              |
| [v] R-NEO-05   : Paredes incompletas y 1 membrana -> Género Neopisosoma      |
| [v] R-NEO-NEG  : Quelípedo liso -> Especie Neopisosoma cf. neglectum          |
+-------------------------------------------------------------------------------+
```

### Ejemplo 3: Flujo Interactivo sin Coincidencia al 100% (Presentación de Especies Candidatas)

Este escenario ejemplifica el comportamiento del sistema cuando la información morfológica suministrada por el usuario es parcial o insuficiente para alcanzar una deducción única del 100%. La interfaz web notifica que no se ha detectado una especie de forma inequívoca y presenta las tres especies con mayor porcentaje de probabilidad y concordancia morfológica.

**1. Interacción en Pantalla:**
- **Paso 1:** El usuario indica `2 pares de antenas` y `segmento antenal corto`.
- **Paso 2:** El usuario selecciona `Paredes del caparazón enteras`.
- **Paso 3:** El usuario no logra determinar la estructura del telson o la textura del carpo por daño morfológico en el espécimen de laboratorio y finaliza la consulta.

**2. Diagnóstico Emitido por el Motor (Respuesta con Candidatas):**

```json
{
  "status": "INCOMPLETE_CERTAINTY",
  "identified_species": null,
  "top_candidate_species": [
    {
      "id": "Petrolisthes_tridentatus",
      "name": "Petrolisthes tridentatus",
      "match_percentage": 75,
      "description": "Petrolisthes con diente lobuliforme en los ángulos orbitales internos.",
      "habitat": "Arrecifes tropicales y zonas rocosas."
    },
    {
      "id": "Petrolisthes_tonsorius",
      "name": "Petrolisthes tonsorius",
      "match_percentage": 60,
      "description": "Petrolisthes con frente triangular y mero de la tercera pata caminadora inflado.",
      "habitat": "Zonas rocosas expuestas."
    },
    {
      "id": "Petrolisthes_jugosus",
      "name": "Petrolisthes jugosus",
      "match_percentage": 50,
      "description": "Especie de Petrolisthes con telson de cinco piezas y margen del carpo dentado.",
      "habitat": "Arrecifes coralinos y rocas."
    }
  ]
}
```

**3. Renderizado en la Interfaz Web (`ResultView.vue`):**

```text
+-------------------------------------------------------------------------------+
|                      NO SE ENCONTRÓ UNA ESPECIE EXACTA                        |
+-------------------------------------------------------------------------------+
| MENSAJE: No se detectó una especie con 100% de certidumbre según los datos    |
| ingresados. A continuación se presentan las 3 especies más probables con       |
| mayor porcentaje de concordancia:                                             |
+-------------------------------------------------------------------------------+
| CANDIDATA 1 (CONCORDANCIA: 75%):                                              |
| Especie:   Petrolisthes tridentatus                                           |
| Hábitat:   Arrecifes tropicales y zonas rocosas                               |
| Atributos Coincidentes: 2 antenas, segmento corto, paredes enteras            |
+-------------------------------------------------------------------------------+
| CANDIDATA 2 (CONCORDANCIA: 60%):                                              |
| Especie:   Petrolisthes tonsorius                                             |
| Hábitat:   Zonas rocosas expuestas                                            |
| Atributos Coincidentes: 2 antenas, segmento corto, paredes enteras            |
+-------------------------------------------------------------------------------+
| CANDIDATA 3 (CONCORDANCIA: 50%):                                              |
| Especie:   Petrolisthes jugosus                                               |
| Hábitat:   Arrecifes coralinos y rocas                                        |
| Atributos Coincidentes: 2 antenas, segmento corto, paredes enteras            |
+-------------------------------------------------------------------------------+
```

---

## Conclusiones y Trabajo Futuro

### Reflexión sobre el Proceso de Desarrollo
El desarrollo del Clasificador de Crustáceos Porcellanidae permitió aplicar de manera práctica la metodología de ingeniería del conocimiento de Buchanan. La estructuración del conocimiento morfológico en reglas de producción aisladas facilitó el desacoplamiento entre el razonamiento lógico y la representación de datos. Asimismo, la adopción de una Arquitectura Hexagonal garantizó una integración limpia y mantenible entre el motor de inferencia en Python (FastAPI) y la interfaz de usuario en Vue.js 3.

Uno de los principales retos consistió en modelar la ambigüedad taxonómica inicial entre Anomura y Brachyura, minimizando la cantidad de preguntas requeridas para cada diagnóstico. Se resolvió priorizando dinámicamente las preguntas con mayor poder discriminatorio en la base de conocimientos.

### Posibles Mejoras y Extensiones Futuras
- **Visión por Computador Integrada:** Incorporar modelos de clasificación de imágenes para sugerir rasgos morfológicos de forma automática a partir de fotografías tomadas en campo.
- **Lógica Difusa y Manejo de Incertidumbre:** Extender el motor para admitir factores de certeza cuando las estructuras anatómicas del ejemplar se encuentren parcialmente dañadas.
- **Exportación de Reportes PDF:** Permitir la descarga de informes técnicos de diagnóstico con ficha taxonómica y mapa de distribución geográfica.
- **Modo PWA Offline:** Habilitar capacidades PWA para la ejecución sin conexión a internet en estaciones biológicas aisladas.

---

## Referencias Bibliográficas para la construcción de la base de conocimientos

- Lira, C. F. (1997). *Crustáceos anomuros costeros de la Península de Macanao, Isla de Margarita, Venezuela* [Tesis de maestría, Universidad de Oriente].
