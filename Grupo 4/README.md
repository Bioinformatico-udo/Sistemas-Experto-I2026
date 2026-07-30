# Clasificador de Crustáceos Porcellanidae

## Integrantes - Grupo 4

- Br. Jesús Rodríguez — C.I. V-30685591
- Br. Alejandra Mendez — C.I. V-30919860
- Br. Wilmer Moreno — C.I. V-30911319

---

## Descripción General

### Propósito del Sistema
Clasificador de Crustáceos Porcellanidae es un sistema experto interactivo diseñado para automatizar y orientar la identificación taxonómica de especímenes pertenecientes a la familia Porcellanidae (conocidos comúnmente como falsos cangrejos o cangrejos de porcelana). La herramienta guía al usuario a través de una serie de preguntas dinámicas sobre la anatomía morfológica del ejemplar recolectado y evalúa progresivamente las características observadas para emitir un diagnóstico preciso sobre el género o especie correspondiente.

### Problema Biológico y Taxonómico que Resuelve
La familia Porcellanidae pertenece al infraorden Anomura y se caracteriza por una morfología que a simple vista confunde a estudiantes e investigadores con los cangrejos verdaderos (infraorden Brachyura). La diferenciación entre especies dentro de este grupo tradicionalmente requiere el uso de claves dicotómicas impresas extensas y un alto grado de experiencia en la observación de estructuras microscópicas o sutiles, como la articulación antenal, la segmentación del caparazón o las crestas de los quelípedos.

El Clasificador de Crustáceos Porcellanidae resuelve esta barrera reduciendo la ambigüedad en la identificación de campo o laboratorio. En lugar de forzar una lectura lineal de claves taxonómicas rígidas, el sistema sintetiza el conocimiento morfológico en una base de reglas parametrizada y permite evaluar características observadas de forma flexible, entregando el resultado final acompañado del árbol taxonómico y las justificaciones morfológicas que respaldan la inferencia.

### Lógica de Inferencia y Arquitectura del Sistema
El núcleo del sistema fue desarrollado aplicando la metodología de ingeniería del conocimiento de Buchanan (Identificación, Conceptualización, Formalización, Implementación y Evaluación) y sigue los principios de la Arquitectura Hexagonal (Puertos y Adaptadores) para desacoplar completamente la lógica de inferencia del marco web y la persistencia de datos.

- **Motor de Inferencia:** Implementa un algoritmo nativo de encadenamiento hacia adelante (Forward Chaining). El motor parte de los hechos observables o respuestas suministradas por el usuario (por ejemplo, número de antenas, tipo de segmento antenal, paredes del caparazón) y evalúa de manera iterativa el conjunto de reglas de producción almacenadas en la base de conocimientos. A medida que las premisas se satisfacen, el motor deduce nuevos hechos hasta alcanzar una conclusión taxonómica definitiva (especie o género) o determinar que el espécimen no pertenece al grupo bajo estudio.
- **Base de Conocimientos:** Las reglas morfológicas y las fichas de las especies están declaradas de manera independiente en formatos estructurados (JSON), lo que permite extender el conocimiento taxonómico sin modificar el código fuente del motor.
- **Extensibilidad:** El sistema permite incorporar nuevas especies directamente desde la interfaz web mediante el modal **Agregar especie**. La aplicación persiste el registro en `src/backend/app/data/species.json`, de modo que el motor de inferencia lo incorpora automáticamente sin necesidad de modificar código.


### Valor Técnico y Académico
Desde el punto de vista académico, el proyecto sirve como un recurso pedagógico clave para estudiantes de biología y ciencias marinas, facilitando el aprendizaje práctico de la taxonomía de decápodos anomuros. A nivel técnico, demuestra la efectividad de implementar sistemas de lógica basada en reglas con una arquitectura moderna de software, mantenible, fácil de auditar mediante pruebas unitarias y lista para integrarse en plataformas web interactivas.

---

## Especies en la Base de Conocimientos

A continuación se enumeran las especies catalogadas en `species.json`. 

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
---

## Instrucciones de Instalación y Uso

### Requisitos Previos
Asegúrese de contar con los siguientes elementos instalados en su sistema operativo antes de comenzar:

- Python 3.11 o superior.
- Node.js 18.0.0 o superior junto con el gestor de paquetes npm.
- Git instalado en su consola de comandos.

### Clonación y Configuración del Repositorio
1. Clone el repositorio en su equipo local y ubíquese en la rama y carpeta correspondiente al proyecto:
   ```bash
   git clone https://github.com/Bioinformatico-udo/Sistemas-Experto-I2026.git
   git switch Grupo4
   cd Sistemas-Experto-I2026/"Grupo 4"
   ```

### Ejecución del Backend (FastAPI)
El backend contiene la lógica del motor de inferencia en Python y expone los puntos de entrada REST para procesar las reglas y hechos.

1. Ingrese al directorio del backend:
   ```bash
   cd src/backend
   ```
2. Cree y active un entorno virtual de Python:
   - En Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - En Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Instale las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie el servidor de desarrollo Uvicorn:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   El servidor estará escuchando por defecto en `http://127.0.0.1:8000`. Puede consultar la documentación interactiva Swagger en `http://127.0.0.1:8000/docs`.

### Ejecución del Frontend (Vue.js 3)
El frontend proporciona una interfaz interactiva e intuitiva para responder las preguntas sobre el espécimen y visualizar el resultado de la inferencia.

1. Abra una nueva terminal y navegue a la carpeta del frontend:
   ```bash
   cd src/frontend
   ```
2. Instale las dependencias de JavaScript:
   ```bash
   npm install
   ```
3. Ejecute el servidor local de desarrollo:
   ```bash
   npm run dev
   ```
4. Abra su navegador web en la dirección indicada en la consola (usualmente `http://localhost:5173`).

### Pruebas Automatizadas
Para verificar el correcto funcionamiento del motor de encadenamiento hacia adelante y la consistencia de la base de conocimientos, ejecute el conjunto de pruebas unitarias con pytest desde la carpeta `src/backend`:
```bash
pytest tests/
```

---

## Ejemplos de Entrada y Salida (Casos de Uso)

A continuación se presentan dos escenarios representativos de interacción con el motor de inferencia de PorcellaniDEX.

### Caso de Uso 1: Clasificación Exitosa de *Neopisosoma cf. neglectum*

En este escenario, el usuario ingresa las respuestas morfológicas de un ejemplar recolectado en zona costera rocosa.

**Entrada (Petición JSON enviada al motor de inferencia / API):**
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

**Salida (Respuesta de inferencia obtenida):**
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

---

### Caso de Uso 2: Flujo Interactivo de Diagnóstico desde la Interfaz Web (Frontend Vue.js)

Este escenario ejemplifica cómo el usuario final interactúa paso a paso con la aplicación web (`src/frontend`) a través del cuestionario dinámico, desde la selección de atributos morfológicos en la interfaz gráfica hasta la generación del reporte visual de explicabilidad.

**1. Interacción en Pantalla (Entrada del Usuario mediante Componentes Vue):**

- **Inicio:** El usuario presiona el botón "Iniciar Diagnóstico" en la vista principal (`HomeView.vue`).
- **Paso 1 (Selección Morfológica - Antenas):** La vista `DiagnosisView.vue` renderiza la primera tarjeta con la pregunta recomendada dinámicamente por el motor.
  - *Pregunta en Pantalla:* "¿Cómo es el segmento basal de la antena?"
  - *Opción seleccionada por el usuario:* `Corto (no alcanza el margen anterior del caparazón)`
- **Paso 2 (Evaluación Adaptativa - Caparazón):** Al seleccionar la opción, la aplicación envía el hecho al backend y recibe automáticamente la siguiente pregunta relevante.
  - *Pregunta en Pantalla:* "¿Las paredes posteriores del caparazón son incompletas o enteras?"
  - *Opción seleccionada por el usuario:* `Incompletas (porciones posteriores ausentes o placas pequeñas)`
- **Paso 3 (Textura de Quelípedos):**
  - *Pregunta en Pantalla:* "¿Cómo es la superficie del quelípedo?"
  - *Opción seleccionada por el usuario:* `Lisa (sin granos ni tubérculos)`

**2. Estado del Store del Frontend (Acumulación de Hechos en `diagnosisStore.js`):**

A nivel de código en el cliente frontend, las opciones marcadas por el usuario alimentan el estado reactivo que procesa la interacción:

```json
{
  "answers": [
    { "fact": "numero_antenas", "value": 2 },
    { "fact": "segmento_antenal", "value": "corto" },
    { "fact": "paredes_caparazon", "value": "incompletas" },
    { "fact": "membranas_area_branquial", "value": "unica" },
    { "fact": "superficie_quelipedo", "value": "lisa" }
  ],
  "progressPercentage": 100
}
```

**3. Renderizado del Resultado Final (Salida en `ResultView.vue`):**

Una vez concluida la inferencia, la interfaz cambia a la pantalla de resultados desplegando la especie identificada, su ficha morfológica y la cadena de explicabilidad:

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

---

## Estructura del Proyecto

El código fuente del sistema se distribuye de la siguiente manera:

```text
Grupo 4/
├── README.md                      # Documentación principal del sistema
└── src/                           # Código fuente del sistema
    ├── backend/                   # Backend desarrollado en FastAPI
    │   ├── app/
    │   │   ├── domain/            # Modelos del dominio y motor de encadenamiento nativo
    │   │   ├── ports/             # Puertos para desacoplamiento arquitectónico
    │   │   ├── adapters/          # Adaptadores (controladores HTTP y persistencia)
    │   │   ├── data/              # Base de conocimientos (reglas y catálogo de especies)
    │   │   └── main.py            # Punto de entrada de la aplicación FastAPI
    │   ├── tests/                 # Suite de pruebas unitarias con pytest
    │   └── requirements.txt       # Dependencias de Python
    └── frontend/                  # Interfaz web desarrollada en Vue.js 3 + Vite
        ├── public/                # Recursos estáticos públicos 
        ├── src/
        │   ├── assets/            # Recurso de estilos y diseño
        │   ├── components/        # Componentes UI reutilizables
        │   │   ├── common/        # Componentes base (BaseButton, ProgressBar, Modales de autenticación)
        │   │   ├── diagnosis/     # Componentes del flujo de inferencia (DiagnosisCard, ExplanabilityPanel)
        │   │   └── portfolio/     # Tarjetas y vistas del catálogo de especies
        │   ├── composables/       # Lógica reactiva reutilizable (gestión de autenticación y sesión)
        │   ├── services/          # Clientes HTTP para la integración con la API REST
        │   ├── stores/            # Gestión del estado global mediante Pinia (diagnosisStore.js)
        │   ├── views/             # Vistas principales (HomeView, DiagnosisView, ResultView)
        │   ├── App.vue            # Componente raíz de la aplicación web
        │   ├── main.js            # Punto de entrada JavaScript y montaje de Vue.js
        │   └── style.css          # Definición de estilos generales y Tailwind CSS
        ├── index.html             # Estructura HTML inicial de la aplicación SPA
        ├── package.json           # Declaración de dependencias y scripts de construcción
        └── vite.config.js         # Configuración del empaquetador de módulos Vite
```
