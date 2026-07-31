# 🦀 PorcellanSpark – Sistema Experto para la Identificación de Crustáceos Porcellanidae

> **Grupo 1** — Universidad de Oriente, Núcleo Nueva Esparta  
> _Sistemas Expertos_

---

## 👥 Integrantes

| Nombre                | Rol                       | Portafolio                                              |
| :-------------------- | :------------------------ | :------------------------------------------------------ |
| **Alexander Urbina**  | Desarrollador Full‑Stack  | [Portafolio](https://portafolio-alexander.netlify.app/) |
| **Allenairam Rojas**  | Investigadora Principal   | [Portafolio](https://allenairam-rojas.vercel.app/)      |
| **Luisana Rodríguez** | Desarrolladora Full‑Stack | [Portafolio](https://portafolio-luisana.netlify.app/)   |

---

## 📋 Resumen Ejecutivo

**PorcellanSpark** es un sistema experto de escritorio que automatiza la identificación taxonómica de crustáceos anomuros de la familia **Porcellanidae**, utilizando como fuente principal el trabajo de grado de Lira (1997) sobre las especies costeras de la Península de Macanao, Isla de Margarita, Venezuela.

El desarrollo se ha guiado por la **metodología de Buchanan**, cubriendo las fases de identificación, conceptualización, formalización, implementación y prueba. El resultado es un prototipo funcional que combina un motor de inferencia híbrido (reglas proposicionales exactas + lógica difusa para atributos subjetivos) con una interfaz gráfica moderna construida en CustomTkinter.

---

## 🔍 Descripción General

El sistema resuelve el problema de la identificación morfológica de estos crustáceos, que requiere analizar características tanto categóricas (número de placas del telson, presencia/ausencia de espinas) como subjetivas (tamaño, grado de setosidad). A través de un cuestionario guiado basado en la clave dicotómica original, el sistema determina la especie y calcula un **porcentaje de certeza** que combina la evidencia exacta con la evaluación difusa del tamaño.

---

## 📐 Metodología de Desarrollo (Buchanan)

El proyecto siguió las cinco fases de la metodología de Buchanan:

1. **Identificación** – Definición del alcance (familia Porcellanidae), actores (expertos en biología, desarrolladores) y recursos (Lira, 1997).
2. **Conceptualización** – Mapeo de atributos morfológicos clave, divididos en discretos (ej. placas del telson) y difusos (tamaño, setosidad).
3. **Formalización** – Codificación de 134 reglas proposicionales (SI-ENTONCES) y 23 reglas difusas con funciones de membresía.
4. **Implementación** – Desarrollo del prototipo en Python con interfaz interactiva, módulo de hechos, motor de reglas y consulta integrada.
5. **Prueba y refinamiento** – Validación de resultados contra la taxonomía documentada, ajuste de reglas y mejoras de usabilidad.

---

## ✨ Características Principales

- 🧬 **Identificación guiada** por clave dicotómica con 23 especies registradas.
- ⚙️ **Motor de inferencia híbrido**: _forward chaining_ + lógica difusa (funciones triangulares y trapezoidales).
- 🔬 **Verificador de especies**: compara características observadas con la ficha técnica y devuelve un porcentaje de similitud/coincidencia.
- 📖 **Glosario interactivo** con búsqueda en tiempo real insensible a acentos.
- 🛡️ **Panel de administración** protegido por login para agregar nuevas especies con validación de duplicados y previsualización de imagen.
- 📸 **Exportación de resultados** a formato PNG.
- 💾 **Persistencia de datos** en archivo JSON.
- 🎨 **Interfaz moderna** con modo oscuro, barra lateral de navegación y ventanas centradas.

---

## 🏛️ Arquitectura del Sistema

### 1. Base de Conocimiento (`backend/base_conocimiento.py`)

- **Reglas proposicionales**: 134 reglas que implementan la clave dicotómica completa (adaptada de Gore & Abele, 1976).
- **Características de especies**: Fichas técnicas detalladas con datos morfológicos, ecológicos y de distribución.
- **Reglas difusas**: 23 reglas que evalúan el tamaño del espécimen para ajustar el grado de certeza.

### 2. Motor de Inferencia (`backend/motor_inferencia.py`)

1. **Fase proposicional**: Encadenamiento hacia adelante (_forward chaining_) para identificar la especie candidata.
2. **Fase difusa**: Si la especie tiene una regla difusa asociada, se solicita el tamaño en cm y se calcula el grado de pertenencia para ajustar la certeza final (60% base proposicional + 40% ajuste difuso).

### 3. Funciones de Membresía (`backend/utils.py`)

- Implementación de funciones triangular y trapezoidal para modelar conceptos lingüísticos como "pequeño", "mediano" y "grande", así como evaluación de incertidumbre cualitativa.

---

## 📂 Estructura del Proyecto

```text
Grupo1/
├── src/
│   ├── main.py                     # Punto de entrada de la aplicación
│   ├── credenciales.py             # Credenciales del administrador
│   ├── especies_personalizadas.json # Base de datos de especies agregadas
│   ├── backend/
│   │   ├── base_conocimiento.py    # Reglas, especies y preguntas
│   │   ├── motor_inferencia.py     # Motor de inferencia híbrido
│   │   └── utils.py                # Funciones de lógica difusa
│   └── frontend/
│       ├── styles.py               # Colores, rutas y centrado de ventanas
│       ├── pages/
│       │   ├── inicio.py           # Página de bienvenida
│       │   ├── caracteristicas.py  # Funcionalidades del sistema
│       │   ├── como_usar.py        # Guía de uso paso a paso
│       │   ├── glosario.py         # Glosario de términos
│       │   ├── sobre_nosotros.py   # Información del equipo
│       │   ├── identificador.py    # Ventana del identificador guiado
│       │   ├── verificador.py      # Ventana del verificador
│       │   ├── login_admin.py      # Login del administrador
│       │   ├── agregar_nva_especie.py # Panel para agregar especies
│       │   └── resultado_especie.py # Ventana de resultado con ficha
│       └── assets/
│           ├── imagen_principal.jpg
│           ├── icons/              # Iconos de la barra lateral
│           └── imagenes_especies/  # Imágenes de cada especie
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── requirements.txt
```

---

## 🚀 Requisitos e Instalación

### Requisitos previos

- **Python 3.8 o superior**
- **pip** (incluido con Python)
- _En Linux:_ `python3-tk` (`sudo apt install python3-tk`)
- _Opcional:_ **Docker Desktop** (para ejecución en contenedor)

### Instalación estándar (Local)

1. Clonar o descomprimir el repositorio.
2. Abrir una terminal en la carpeta `src/` (donde se encuentra `main.py`).
3. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```bash
   python main.py
   ```

### Ejecución con Docker

1. Asegúrate de tener **Docker Desktop** instalado y en ejecución.
2. _Nota para Windows:_ Instalar y ejecutar **VcXsrv** (servidor X11) marcando la opción _"Disable access control"_.
3. Construir la imagen de Docker:
   ```bash
   docker build -t porcellanspark .
   ```
4. Ejecutar el contenedor según tu sistema operativo:
   - **Windows (PowerShell):**
     ```powershell
     docker run --rm -e DISPLAY=host.docker.internal:0 -v ${PWD}/especies_personalizadas.json:/app/especies_personalizadas.json porcellanspark
     ```
   - **Linux / macOS:**
     ```bash
     xhost +local:docker
     docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd)/especies_personalizadas.json:/app/especies_personalizadas.json --network host porcellanspark
     ```

---

## 📖 Guía de Uso

### 🏠 Pantalla de Inicio

Desde la pantalla principal se accede a las dos funciones principales del sistema:

- **Comenzar Identificación de Especie:** Abre el cuestionario guiado interactivo.
- **Iniciar Verificación de Especie:** Permite comparar características con una especie ya existente en el sistema.

### 🧬 Identificación Guiada

1. Haga clic en **"COMENZAR IDENTIFICACIÓN DE ESPECIE"**.
2. Responda paso a paso las preguntas sobre la morfología del crustáceo.
3. Presione **"Analizar Especie"**.
4. El sistema mostrará la especie identificada con su ficha técnica, imagen correspondiente y porcentaje de certeza.
5. Opcionalmente, puede exportar el resultado a una imagen PNG.

### 🔬 Verificador de Especie

1. Haga clic en **"INICIAR VERIFICACIÓN DE ESPECIE"**.
2. Seleccione una especie del listado disponible.
3. Observe la imagen de referencia y sus características taxonómicas.
4. Marque **"Sí"** o **"No"** en cada característica según lo observado en su espécimen.
5. Presione **"Evaluar coincidencias"** para obtener el porcentaje de similitud.

### 📚 Glosario

En la sección **"GLOSARIO DE TÉRMINOS"** encontrará definiciones claras de todos los términos anatómicos utilizados en la clave. Cuenta con un buscador en tiempo real insensible a acentos.

### 🛡️ Panel de Administración

1. Haga clic en **"ADMINISTRADOR"** en la barra lateral.
2. Inicie sesión con las credenciales predeterminadas:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`
3. Complete el formulario para agregar una nueva especie (nombre científico, características e imagen).
4. Si la especie ya se encuentra registrada, el sistema le ofrecerá añadir características diferenciadoras.
5. Las nuevas especies se almacenarán en `especies_personalizadas.json` y aparecerán automáticamente en el verificador.

---

## 🧪 Ejemplos de Ejecución

### Ejemplo 1: Identificación de _Petrolisthes armatus_

- **Entrada del usuario:**
  - Artejo basal de la antena: `corto`
  - Paredes posteriores: `enteras`
  - Carpo de los quelípedos: `dientes_lobulos`
  - Telson: `7 piezas`
  - Espina epibranquial: `presente`
  - Margen flexor del carpo: `tres_separados`
- **Salida del sistema:**
  - **Especie identificada:** _Petrolisthes armatus_
  - **Certeza:** ~95% (ajustado por tamaño mediano‑grande mediante lógica difusa)
  - Ficha técnica completa e imagen oficial de la especie.

### Ejemplo 2: Agregar una nueva especie

- **Entrada del administrador:**
  - Nombre científico: `Pachycheles chacei`
  - Características: Las requeridas por la ficha técnica.
  - Imagen: Seleccionada mediante el explorador de archivos integrado.
- **Salida del sistema:**
  - Especie agregada correctamente y disponible de inmediato en el módulo de verificación.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Interfaz Gráfica:** CustomTkinter / Tkinter
- **Procesamiento de Imágenes:** Pillow (PIL)
- **Persistencia de Datos:** JSON
- **Motor de Inferencia:** Forward chaining + Lógica difusa (implementación propia)
- **Contenedorización:** Docker, Docker Compose

---
## Conclusiones y Trabajo Futuro

### 📝 Conclusiones

El desarrollo de **PorcellanSpark** ha sido una experiencia enriquecedora que nos permitió aplicar conocimientos en sistemas expertos, lógica difusa y programación en Python. A lo largo del proceso, logramos construir un prototipo funcional que integra un motor de inferencia híbrido, una interfaz gráfica amigable y una base de conocimientos detallada, facilitando la identificación taxonómica de crustáceos Porcellanidae.

El sistema ha demostrado ser efectivo en la clasificación de especies a partir de características morfológicas tanto discretas como subjetivas, logrando un porcentaje de certeza ajustable mediante lógica difusa. La incorporación de un panel de administración y la capacidad de agregar nuevas especies fortalecen la escalabilidad del proyecto.

### ⚠️ Desafíos y Soluciones

Uno de los principales desafíos fue la formalización adecuada de las reglas difusas y la integración con el motor de inferencia proposicional. Para ello, se implementaron funciones de membresía triangulares y trapezoidales, y se diseñaron algoritmos que combinan ambos enfoques para obtener resultados precisos y confiables.

Otra dificultad fue la estructuración de una interfaz intuitiva y moderna, lograda mediante el uso de CustomTkinter, que permite una experiencia de usuario mejorada.

### 🚀 Trabajo Futuro

En futuras versiones, se planea:

- **Ampliar la base de conocimientos** incluyendo más especies y atributos, así como datos ecológicos y de distribución.
- **Mejorar la lógica difusa** incorporando técnicas avanzadas de aprendizaje automático para ajustar automáticamente los parámetros de las funciones de membresía.
- **Implementar un módulo de aprendizaje** que permita al sistema aprender de nuevas observaciones y mejorar sus reglas automáticamente.
- **Desarrollar una versión web** para facilitar el acceso y uso desde diferentes plataformas.
- **Integrar reconocimiento de imágenes** mediante técnicas de visión artificial para identificar especies a partir de fotografías en lugar de cuestionarios guiados.

Este proyecto continúa en desarrollo, con la intención de convertirse en una herramienta confiable y accesible para biólogos, estudiantes y entusiastas de la taxonomía de crustáceos.
## 📚 Referencias

1. **Lira, C. F. (1997).** _Crustáceos anomuros costeros de la Península de Macanao, Isla de Margarita, Venezuela._ Trabajo de grado, Universidad de Oriente, Núcleo Nueva Esparta.
2. **Gore, R. H. & Abele, L. G. (1976).** _Shallow water porcelain crabs from the Pacific coast of Panama and adjacent Caribbean waters._ Smithsonian Contributions to Zoology, 237.
3. **Haig, J. (1960).** _The Porcellanidae (Crustacea Anomura) of the eastern Pacific._ Allan Hancock Pacific Expeditions, 24.

---

## 💡 Notas Adicionales
- Las imágenes de las especies deben colocarse en `src/frontend/assets/imagenes_especies/` con el formato `nombre_cientifico.jpg` (ejemplo: `neopisosoma_cf_neglectum.jpg`).
- El archivo `especies_personalizadas.json` se genera y actualiza automáticamente al agregar la primera especie desde el panel de administración.
- Si no desea utilizar Docker, basta con tener Python 3.8+ instalado en su sistema, ejecutar `pip install -r requirements.txt` y posteriormente `python main.py` desde la carpeta `src/`.
