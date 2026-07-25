# CoraAI — Sistema Experto Taxonómico de Corales (Los Roques) 🌊🪸

![CoraAI Logo](frontend/src/assets/logo.png)

**CoraAI** es un **Sistema Experto Híbrido** de última generación diseñado para la identificación, clasificación y análisis pedagógico-científico de especies de corales duros y fotosintéticos del orden *Scleractinia*, halladas en el **Parque Nacional Archipiélago de Los Roques, Venezuela**.

Combina la precisión y certeza de la **IA Simbólica** (Árbol de Decisión Dicotómico y Motor de Inferencia de Reglas Biológicas) con la adaptabilidad y flexibilidad de la **IA Subsimbólica** (Red Neuronal en TensorFlow/Keras + Motor de Ponderación Semántica NLP).

---

## 🚀 Estado Actual del Proyecto (Rama `Grupo8`)

- 🌐 **Interfaz Web SPA Modernizada**: Desarrollada en **React + Vite** con diseño **Liquid Glassmorphism**, estética marina bioluminiscente y tipografía *Montserrat*.
- ⚡ **Backend REST de Alta Velocidad**: Servidor unificado en **FastAPI / Uvicorn** con documentación Swagger integrada.
- 📋 **Cuestionario Dicotómico Guiado (2 Columnas)**: Preguntas paso a paso con filtrado en tiempo real del listado de candidatos en pequeñas tarjetas horizontales y tarjeta de resultado final con recuadro fotográfico `110x110px`.
- 🤖 **Diagnóstico por Lenguaje Natural con IA**: Procesamiento de descripciones con sugerencias de 1 sola línea (`+ marrón`, `+ ramificada`, etc.) y modal de **Explicabilidad Algorítmica (XAI)**.
- 🪸 **Catálogo de Especies & Gestión CRUD**: Carga procedimental por lotes con esqueletos de carga (*shimmers*), modal detallado en 2 columnas montado via `createPortal` y formulario modal de **Alta de Nueva Especie** (`POST /api/especies`) con almacenamiento de imágenes.

---

## 📂 Arquitectura General de la Aplicación

```
Sistemas-Experto-I2026/
├── run_server.py               # Lanzador unificado del servidor FastAPI + Producción React
├── requirements.txt            # Dependencias de Python (FastAPI, TensorFlow, Pydantic, etc.)
├── .gitignore                  # Exclusiones de control de versiones Git
├── src/                        # Núcleo del Backend en Python
│   ├── api/
│   │   ├── app.py              # Endpoints API REST (/api/cuestionario, /api/ia, /api/especies)
│   │   └── schemas.py          # Validación de entradas/salidas Pydantic v2
│   ├── motor_inferencia.py     # Motor de Inferencia Simbólico (Árbol Dicotómico)
│   ├── modelo_hibrido.py       # Red Neuronal TensorFlow/Keras & Clasificador Híbrido
│   ├── motor_ponderacion.py    # Motor de Ponderación Semántica por Atributos Morfológicos
│   ├── base_conocimiento.py    # Gestión de especies.json y reglas.json
│   ├── preguntas.py            # Generador de clave de preguntas taxonómicas
│   └── explicacion.py          # Generador de explicaciones algorítmicas (XAI)
├── frontend/                   # Aplicación Web SPA (React + Vite)
│   ├── src/
│   │   ├── assets/             # Logo oficial transparente y recursos gráficos
│   │   ├── components/         # Componentes React (Cuestionario, DiagnosticoIA, Catalogo, Modales)
│   │   │   ├── Cuestionario.jsx
│   │   │   ├── DiagnosticoIA.jsx
│   │   │   ├── CatalogoEspecies.jsx
│   │   │   ├── GuiaTaxonomica.jsx
│   │   │   ├── ModalDetalleCoral.jsx
│   │   │   ├── ModalAgregarEspecie.jsx
│   │   │   └── ModalExplicacionIA.jsx
│   │   ├── App.jsx             # Shell principal de navegación y Hero
│   │   └── index.css           # Sistema de Diseño Liquid Glassmorphism
│   ├── dist/                   # Build compilado de producción servido por FastAPI
│   └── package.json
├── data/                       # Base de datos JSON y fotografías taxonómicas
│   ├── especies.json           # Registro de las 41+ especies de Los Roques
│   ├── reglas.json             # Reglas del árbol dicotómico
│   └── Imagenes/               # Galería de imágenes de alta resolución (.jpg)
├── docs/                       # Documentación Técnica, de Usuario y Sistema Híbrido
│   ├── manual_usuario.md       # Guía detallada para el usuario final
│   ├── manual_tecnico.md       # Especificaciones técnicas de la API y componentes
│   └── funcionamiento_hibrido.md# Detalle del Motor Simbólico + Subsimbólico
└── tests/                      # Pruebas unitarias automatizadas con pytest
```

---

## 🛠️ Guía de Instalación y Ejecución

### 1. Requisitos Previos
- **Python 3.8+**
- **Node.js 18+** y **npm** (para modificaciones en el frontend)

### 2. Instalación de Dependencias
En la raíz del proyecto, ejecute:
```bash
pip install -r requirements.txt
```

### 3. Lanzar la Aplicación (Servidor Unificado)
Ejecute el script de arranque principal:
```bash
python run_server.py
```
- 🌐 **Plataforma Web (React)**: Abre [http://localhost:8000](http://localhost:8000) en tu navegador.
- 📚 **Documentación API (Swagger UI)**: Consulta [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🧪 Pruebas Unitarias Automatizadas

Para validar los motores de inferencia, reglas y endpoints de la API, ejecute:
```bash
pytest
```

---

## 🤝 Integrantes del Proyecto (Grupo 8)

Desarrollado para el curso de **Sistemas Expertos (I2026)**.
