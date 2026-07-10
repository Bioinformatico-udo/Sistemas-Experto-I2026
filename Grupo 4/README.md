# Sistema Experto de Clasificación Taxonómica de Crustáceos - Grupo 4

Este proyecto consiste en un sistema experto de clasificación taxonómica de crustáceos basado en un motor de **Encadenamiento hacia Adelante (Forward Chaining)** desarrollado de forma nativa en Python 3.11+ utilizando FastAPI y una interfaz de usuario interactiva construida en Vue.js 3 y Tailwind CSS.

El diseño del proyecto sigue estrictamente la metodología de **Buchanan** para la ingeniería del conocimiento y la **Arquitectura Hexagonal (Ports and Adapters)** para garantizar que la lógica de negocio esté completamente desacoplada de los frameworks y el almacenamiento.

## 📂 Estructura del Proyecto

El código fuente del proyecto se organiza dentro de la carpeta `src/`:

```text
Grupo 4/
├── README.md                      # Este archivo
├── src/                           # Código fuente
│   ├── backend/                   # Backend en FastAPI
│   │   ├── app/
│   │   │   ├── domain/            # Capa de Dominio (Modelos y Motor puro)
│   │   │   ├── ports/             # Interfaces/Puertos
│   │   │   ├── adapters/          # Adaptadores (Controladores API y Persistencia JSON)
│   │   │   └── data/              # Base de conocimientos (Reglas y Especies separadas)
│   │   └── main.py                # Entrada de la aplicación backend
│   └── frontend/                  # Frontend en Vue.js 3
```

## 🛠️ Requisitos e Instalación

Para ejecutar el backend:
1. Navega a `src/backend` e instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor uvicorn:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

Para ejecutar el frontend:
1. Navega a `src/frontend` e instala las dependencias:
   ```bash
   npm install
   ```
2. Ejecuta el servidor de desarrollo:
   ```bash
   npm run dev
   ```
