# Sistema experto para identificación de corales de Mochima

Este proyecto implementa un sistema experto interactivo para identificar especies de corales del Parque Nacional Mochima a partir de características observables como familia, género, profundidad, forma y complejidad de cuidado.

La aplicación fue desarrollada con Python y Streamlit, y utiliza un catálogo estructurado en formato JSON como base de conocimiento.

## ¿Qué hace el sistema?

El sistema presenta un chatbot llamado CoralBot que guía al usuario mediante preguntas sencillas. A partir de las respuestas, el programa:

- compara las características ingresadas con un catálogo de especies,
- filtra las opciones más compatibles,
- muestra la especie más probable,
- y ofrece una descripción detallada con información ecológica y morfológica.

## Objetivo del proyecto

Ayudar a identificar corales del ecosistema de Mochima mediante un enfoque de razonamiento basado en reglas y coincidencias taxonómicas, sin necesidad de que el usuario conozca la clasificación científica completa.

## Estructura del proyecto

- [env/Include/main_corales.py](env/Include/main_corales.py): archivo principal de la app. Contiene la lógica del sistema experto, el flujo conversacional, la interpretación de respuestas y la inferencia de especies.
- [env/Include/diccionario.json](env/Include/diccionario.json): base de conocimiento del sistema. Aquí se almacenan las especies, sus atributos y sus descripciones.
- [env/Include/styles.css](env/Include/styles.css): estilos visuales de la interfaz.
- [env/](env/): entorno virtual de Python con las dependencias necesarias para ejecutar la aplicación.

## Componentes principales del código

### 1. Carga del catálogo
El archivo principal carga el contenido de [env/Include/diccionario.json](env/Include/diccionario.json) al iniciar la aplicación. Cada entrada del JSON representa una especie de coral y contiene campos como:

- descripción,
- familia,
- género,
- profundidad ideal,
- forma,
- complejidad,
- palabras clave,
- estado actual,
- morfología.

### 2. Flujo conversacional
La app usa Streamlit para mostrar una interfaz tipo chat. El sistema:

1. inicia una sesión de identificación,
2. hace preguntas una por una,
3. recibe respuestas del usuario,
4. interpreta las respuestas mediante funciones de normalización y coincidencia,
5. filtra candidatos y muestra resultados.

### 3. Lógica de inferencia
El programa compara las respuestas del usuario contra los atributos de cada entrada del catálogo. Si encuentra una coincidencia clara, muestra la especie identificada; si hay varias opciones, presenta una lista de candidatos.

### 4. Interfaz de usuario
La interfaz está diseñada para que la experiencia sea sencilla y natural. Incluye:

- un chat con mensajes del usuario y del sistema,
- navegación entre vistas de catálogo y chatbot,
- mensajes de bienvenida,
- botones para reiniciar la identificación.

## Cómo funciona la identificación

El sistema experto trabaja con estas características:

- Familia: por ejemplo Acroporidae, Mussidae o Poritidae.
- Género: por ejemplo Acropora, Diploria o Porites.
- Profundidad ideal: somera, media o profunda.
- Forma: ramificado, masivo o incrustante.
- Complejidad: baja, media o alta.

A partir de estas características, el sistema intenta encontrar la especie más compatible dentro del catálogo.

## Requisitos

Para ejecutar este proyecto necesitas:

- Python 3.x
- Streamlit
- El entorno virtual incluido en [env/](env/)

## Instrucciones de ejecución

Desde la raíz del proyecto, ejecuta los siguientes comandos en PowerShell:

```powershell
.
.
env\Scripts\activate
streamlit run env\Include\main_corales.py
```

Luego abre la URL que muestre Streamlit en tu navegador.

## Ejemplo de uso

El usuario puede escribir algo como:

- Acroporidae
- Acropora
- Somera
- Ramificado
- Baja

O también puede escribir respuestas más libres, como:

- coral ramificado en aguas someras
- especie de coral cerebro
- forma masiva y complejidad media

El sistema intentará interpretar esas frases y encontrar posibles coincidencias.

## Notas importantes

- El sistema se apoya en un catálogo manual, por lo que la calidad de las identificaciones depende de la información registrada en [env/Include/diccionario.json](env/Include/diccionario.json).
- La lógica incorpora coincidencias por texto y fuzzy matching para manejar respuestas imprecisas.
- El proyecto está pensado como una herramienta educativa y de apoyo para el estudio de corales de Mochima.

## Autoría y propósito

Este proyecto combina:

- inteligencia artificial aplicada a sistemas expertos,
- procesamiento de lenguaje natural básico,
- y una base de datos temática sobre corales del Caribe venezolano.

Es una propuesta útil para mostrar cómo un sistema experto puede organizar conocimiento ecológico y convertirlo en una experiencia interactiva.

## Cómo iniciar el proyecto

A continuación se presentan instrucciones claras y reproducibles para ejecutar la aplicación. Elija la opción que prefiera: usar Docker (recomendado) o ejecutar localmente con Python.

### Requisitos previos

- Windows 10/11 o macOS/Linux
- Git (para clonar el repositorio)
- Docker Desktop (si va a usar Docker)
- Python 3.8+ (si va a ejecutar sin Docker)

### Opción A — Ejecutar con Docker (recomendado)

1. Clona el repositorio y entra en la carpeta del proyecto:

```powershell
git clone <URL-del-repositorio>
cd "Grupo 2 Corales 1"
```

2. Construye la imagen Docker desde la raíz del proyecto:

```powershell
docker build -t coralbot_app .
```

3. Ejecuta el contenedor y publica el puerto 8501 (puerto por defecto de Streamlit):

```powershell
docker run --rm -p 8501:8501 coralbot_app
```

4. Abre tu navegador en http://localhost:8501 y verifica que la app cargue.

Notas:
- Use `--rm` para que el contenedor se elimine al detenerlo.
- Si el puerto 8501 ya está en uso, cambie el mapeo de puertos, por ejemplo `-p 8502:8501`.

### Opción B — Ejecutar localmente con Python (sin Docker)

1. Crea y activa un entorno virtual (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En CMD usa:

```cmd
.\.venv\Scripts\activate
```

2. Instala dependencias (si existe `requirements.txt`) o instala Streamlit:

```powershell
pip install -r requirements.txt
# o, si no existe requirements.txt
pip install streamlit
```

3. Ejecuta la aplicación Streamlit:

```powershell
streamlit run env\Include\main_corales.py
```

4. Abre http://localhost:8501 en tu navegador.

### Solución de problemas comunes

- PowerShell bloquea la ejecución de scripts: ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` como administrador si es necesario.
- Si falta algún paquete, instala con `pip install <paquete>` o revisa `requirements.txt`.
- Verifica que la ruta `env\Include\main_corales.py` exista y que el archivo sea el punto de entrada correcto.

Si prefieres, puedo añadir un `requirements.txt` o un `docker-compose.yml` para facilitar la ejecución. Dime cuál opción prefieres.
