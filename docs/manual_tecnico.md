# 🛠️ Manual Técnico - Arquitectura CoraAI

Este documento ofrece las especificaciones técnicas del backend, frontend, API REST y motores de inteligencia artificial del sistema experto **CoraAI**.

---

## 📋 1. Requisitos del Sistema y Entorno
- **Python**: **`Python 3.8 o superior`** (Recomendado Python 3.10 / 3.11 para TensorFlow 2.15 y FastAPI 0.110).
- **Node.js**: **`Node.js 18.0 o superior`** & **`npm 9.0+`**.
- **Sistema Operativo**: Multiplataforma (Windows 10/11, Linux Ubuntu 20.04+, macOS).

---

## 🏗️ 2. Arquitectura de Software

La aplicación sigue una arquitectura cliente-servidor desacoplada con compilación unificada para distribución en producción.

```text
[ Cliente Navegador Web (React SPA) ]
                │
         Peticiones HTTP REST
                │
                ▼
[ Servidor FastAPI (Python Uvicorn) ]
   ├── StaticFiles Middleware (Distribuir React Build /dist)
   ├── Endpoints API (/api/cuestionario, /api/ia, /api/especies)
   └── Motor Híbrido AI
        ├── Motor Inferencia Dicotómico (Simbólico)
        ├── Red Neuronal TensorFlow/Keras (Subsimbólico)
        └── Motor de Ponderación Semántica (NLP)
```

---

## 📡 2. Endpoints de la API REST (`src/api/app.py`)

### 2.1. Cuestionario Dicotómico
- **`GET /api/cuestionario/pregunta-inicial`**
  - Retorna la primera pregunta del árbol de decisión con sus opciones.
- **`POST /api/cuestionario/siguiente-pregunta`**
  - Recibe la pregunta actual y la opción seleccionada. Retorna la siguiente pregunta o el resultado final de la especie.
- **`POST /api/cuestionario/candidatos`**
  - Recibe el historial de respuestas hasta el momento y evalúa `base_conocimiento.py` para devolver el listado filtrado de candidatos compatibles en tiempo real.

### 2.2. Diagnóstico IA (Lenguaje Natural)
- **`POST /api/ia/diagnostico`**
  - **Entrada**: `{ "texto": "descripcion libre..." }`
  - **Procesamiento**: Tokenización NLP -> Predicción Red Neuronal TensorFlow -> Motor de Ponderación Semántica -> Matriz Híbrida.
  - **Salida**: Objeto con `especie_ganadora`, `top_candidatos`, `respuestas_deducidas` y `desglose_explicativo`.

### 2.3. Catálogo de Especies & CRUD
- **`GET /api/especies`**
  - Devuelve el listado completo de las 41+ especies registradas en `data/especies.json`.
- **`GET /api/especies/{especie_id}`**
  - Devuelve los detalles biológicos, ecológicos y taxonómicos completos de una especie.
- **`POST /api/especies`**
  - Registra una nueva especie en `data/especies.json` y decodifica la imagen subida en Base64 para guardarla como `data/Imagenes/{especie_id}.jpg`.
- **`GET /api/imagenes/{especie_id}.jpg`**
  - Sirve el archivo estático de imagen de la especie solicitada.

---

## 🎨 3. Frontend React (`frontend/src/`)

### 3.1. Sistema de Diseño (Liquid Glassmorphic)
- **`index.css`**: Define variables CSS nativas para colores bioluminiscentes (`--accent-primary: #3ecfb4`, `--accent-purple: #a78bfa`, `--accent-coral: #ff6b9d`), glassmorphism (`backdrop-filter: blur(20px)`), elevaciones y bordes con luz interior (`inset 0 1px 0 rgba(255,255,255,0.25)`).

### 3.2. Componentes Principales
- **`App.jsx`**: Shell de la aplicación SPA con la barra de navegación transparente, Hero de bienvenida con tarjetas CTA traslúcidas de colores personalizados (`#359693` y `#5d3596`), y la franja de estadísticas.
- **`Cuestionario.jsx`**: Layout en 2 columnas que calcula candidatos en tiempo real y renderiza la tarjeta final con fotografía `110x110px`.
- **`DiagnosticoIA.jsx`**: Layout en 2 columnas con sugerencias en 1 sola línea, demostraciones rápidas y disparador del modal de explicabilidad.
- **`ModalDetalleCoral.jsx`**: Modal en 2 columnas montado en `document.body` vía `ReactDOM.createPortal` para evitar desajustes por CSS transforms.
- **`ModalExplicacionIA.jsx`**: Modal de explicabilidad algorítmica (XAI) montado vía `createPortal` para detallar la justificación del ranking híbrido.
- **`ModalAgregarEspecie.jsx`**: Formulario modal para registrar nuevas especies y cargar imágenes.

---

## ⚙️ 4. Reconstrucción y Despliegue

Cada modificación realizada en los componentes de `frontend/src/` requiere recompilar el paquete estático antes de que tome efecto en la API FastAPI:

```bash
cd frontend
npm run build
```
Esto genera la carpeta `frontend/dist/` optimizada que sirve `run_server.py`.
