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
