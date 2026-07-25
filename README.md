# Sistema Experto Taxonómico: Corales de Los Roques 🌊🪸

Este proyecto implementa un **Sistema Experto Híbrido** diseñado para identificar y clasificar las especies de corales del **Parque Nacional Archipiélago de Los Roques, Venezuela**. 

Combina la precisión científica de la **IA Simbólica** (Árbol de Decisión Dicotómico y Motor de Inferencia Reglado) con la flexibilidad de la **IA Subsimbólica** (Red Neuronal en TensorFlow/Keras y Motor de Ponderación Inteligente), expuesto a través de un backend **FastAPI** y una interfaz web moderna en **React + Vite**.

---

## 📂 Arquitectura del Proyecto

```
Sistemas-Experto-I2026/
├── run_server.py               # Lanzador principal del servidor FastAPI + React
├── src/
│   ├── api/                    # Servidor REST en FastAPI
│   │   ├── app.py              # Endpoints API y middleware CORS
│   │   └── schemas.py          # Modelos Pydantic para validación
│   ├── motor_inferencia.py     # Motor de inferencia en árbol dicotómico
│   ├── modelo_hibrido.py       # Red Neuronal TensorFlow y Predictor Híbrido
│   ├── motor_ponderacion.py    # Algoritmo de ponderación semántica
│   ├── base_conocimiento.py    # Gestor de especies y reglas taxonómicas
│   ├── preguntas.py            # Generador de clave de preguntas
│   └── explicacion.py          # Generador de explicaciones de diagnóstico
├── frontend/                   # Aplicación Web SPA (React + Vite)
│   ├── src/
│   │   ├── components/         # Cuestionario, Modo IA, Catálogo y Guía
│   │   ├── App.jsx             # Contenedor principal React
│   │   └── index.css           # Sistema de diseño oceanográfico
│   └── package.json
├── data/                       # Dataset, reglas.json y especies.json
├── tests/                      # Suite de pruebas unitarias pytest y API
├── requirements.txt            # Dependencias Python
└── README.md
```

---

## 🛠️ Instalación y Lanzamiento

### 1. Requerimientos e Instalación
Asegúrese de tener Python 3.8+ y Node.js 18+ instalados.
```bash
pip install -r requirements.txt
```

### 2. Iniciar el Servidor Unificado (FastAPI + React)
Ejecute en la raíz del proyecto:
```bash
python run_server.py
```
- 🌐 **Interfaz Web (React)**: [http://localhost:8000](http://localhost:8000)
- 📚 **Documentación API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Desarrollo de Frontend (Opcional - Hot Reload)
Si desea hacer cambios en vivo al código React:
```bash
cd frontend
npm install
npm run dev
```
Acceda a `http://localhost:5173`.

### 4. Ejecutar Pruebas Unitarias y de API
```bash
pytest
```
