# Guía de Instalación: Sistema Experto de Macroalgas

Este documento detalla los pasos necesarios para instalar, configurar y ejecutar el Sistema Experto Ficológico. El proyecto está dividido en dos componentes principales: el **Backend** (desarrollado en Python con FastAPI) y el **Frontend** (desarrollado en Node.js con Next.js y React).

---

## 1. Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas en tu sistema (en este caso, Windows):
- **Python**: Versión 3.8 o superior.
- **Node.js**: Versión 18.0 o superior (se recomienda la versión LTS).

---

## 2. Instalación del Backend (Python / FastAPI)

El backend expone la lógica del motor de inferencia mediante una API HTTP. Se recomienda instalarlo en un entorno virtual para aislar sus dependencias.

### Pasos:

1. **Abrir la terminal** en la raíz del proyecto (la carpeta `Sistema Experto Macroalgas`).
2. **Crear un entorno virtual**:
   ```powershell
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - En **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - En **Windows (CMD)**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```

4. **Instalar las dependencias**:
   Con el entorno virtual activado, ejecuta:
   ```powershell
   pip install -r requirements.txt
   ```
   *Esto instalará `fastapi`, `uvicorn`, `pydantic`, `python-dotenv` y otras librerías necesarias.*

---

## 3. Instalación del Frontend (Next.js / React)

El frontend proporciona la interfaz gráfica web interactiva.

### Pasos:

1. Desde la terminal en la raíz del proyecto, **navega a la carpeta del frontend**:
   ```powershell
   cd Frontend
   ```

2. **Instalar las dependencias de Node**:
   ```powershell
   npm install
   ```

---

## 4. Ejecución del Sistema

Puedes levantar el sistema ejecutando cada servicio por separado.

### Ejecución Manual en Terminales Separadas (Recomendado en Windows)

**Terminal 1: Backend**
1. Abre una terminal en la raíz del proyecto.
2. Activa el entorno virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Inicia el servidor de la API:
   ```powershell
   python main.py
   # O alternativamente: python api_server.py
   ```
*El backend se iniciará, exponiendo los endpoints en `http://127.0.0.1:8000`.*

**Terminal 2: Frontend**
1. Abre otra terminal y navega al directorio del Frontend:
   ```powershell
   cd Frontend
   ```
2. Inicia el servidor de desarrollo de Next.js:
   ```powershell
   npm run dev
   ```
*La interfaz gráfica estará disponible en tu navegador en `http://localhost:3000`.*

### Ejecución con Script de Bash (WSL/Git Bash)
Si utilizas WSL, Git Bash o un emulador de bash en Windows, puedes usar el script de inicio rápido incluido:
```bash
./start_project.sh
```

---

## 5. Uso de las Herramientas por Línea de Comandos (CLI)

El proyecto incluye varias herramientas que pueden ejecutarse directamente en la terminal (asegúrate de tener el entorno virtual de Python activado):

- **Modo interactivo en consola:**
  ```powershell
  python expert_algas.py
  ```
- **Prueba de Calibración:** Ejecuta las pruebas automatizadas sobre muestras de herbario:
  ```powershell
  python expert_algas.py --calibration
  ```
- **Editor de la Base de Conocimiento:** Abre el editor interactivo para la ontología:
  ```powershell
  python knowledge_editor.py
  ```
- **Restaurar Base de Datos:** Regenera `algae_knowledge.json` al estado por defecto:
  ```powershell
  python generar_json_prueba.py
  ```
