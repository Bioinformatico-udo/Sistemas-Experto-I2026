# Sistema Experto para la Identificación de Corales de Mochima (CoralBot)

## Integrantes del Grupo

- [Jhon Fernandez  Cedula de Identidad : 32.086.485 ]
https://github.com/Jhon-Fernandez1/Portafolio-Personal
- [Alfonso Cedeño  Cedula de Identidad : 31.241.821 ]
https://github.com/fonchocc/Portafolio-Personal-UDO
- [Roberth Alvarez Cedula de Identidad : 31.232.207 ]
https://github.com/RoberthAlverez/RoberthAlverez

## Descripción General

Este proyecto desarrolla un sistema experto interactivo para identificar especies de corales del Parque Nacional Mochima a partir de características observables como familia, género, profundidad, forma y complejidad de cuidado. La aplicación está diseñada como una herramienta didáctica, visual e intuitiva para apoyar la identificación de corales sin requerir un conocimiento taxonómico previo.

El sistema resuelve el problema de reconocer especies de corales de manera guiada y accesible, utilizando una base de conocimiento estructurada y reglas de inferencia para ofrecer resultados útiles a estudiantes, investigadores y visitantes.

## Objetivo de la Aplicación

El objetivo principal de la aplicación es facilitar la identificación de corales del Parque Nacional Mochima mediante un sistema experto interactivo, accesible y fácil de usar. Su propósito es apoyar a estudiantes, investigadores y visitantes en la clasificación de especies a partir de características observables, sin requerir conocimientos taxonómicos avanzados.

Además, la aplicación busca:

- promover el aprendizaje sobre la biodiversidad coralina del ecosistema de Mochima,
- enseñar de forma práctica cómo funciona la lógica de un sistema experto,
- y ofrecer una herramienta visual y didáctica para explorar información ecológica, morfológica y taxonómica de los corales.

## ¿Qué ofrece la aplicación?

La aplicación integra tres módulos principales de interacción:

1. Catálogo de corales
   - Permite visualizar todas las especies registradas en la base de conocimiento.
   - Incluye búsqueda por nombre, familia, género o palabras clave.
   - Muestra información descriptiva y atributos relevantes de cada coral.

2. Chatbot de identificación
   - Permite al usuario interactuar de forma natural con CoralBot.
   - El sistema puede interpretar respuestas simples o frases descriptivas.
   - Resume las características recibidas y propone una especie o un grupo de especies compatibles.

3. Cuestionario experto
   - Ofrece un recorrido más estructurado y técnico.
   - Hace preguntas morfológicas y taxonómicas para reducir opciones de forma progresiva.
   - Es útil cuando el usuario desea una identificación más rigurosa.

4. Inicio de sesión de administrador
   - Permite acceder a un panel de gestión.
   - El administrador puede agregar, editar o eliminar especies del catálogo.
   - Cada operación genera un respaldo automático del archivo de datos.

5. Responsables
   - Se puede Visualizar los Nombres de los Responsables y su Direccion del Portafolio en Github.
## Arquitectura del Sistema

### Base de Conocimientos

La base de conocimiento está conformada por el archivo [env/Include/diccionario.json](env/Include/diccionario.json), que almacena la información de las especies de corales en formato JSON. Cada registro contiene atributos como:

- descripción general,
- familia,
- género,
- profundidad ideal,
- forma de la colonia,
- complejidad de cuidado,
- palabras clave,
- estado actual,
- morfología detallada.

Este formato permite estructurar el conocimiento de manera organizada, editable y fácil de consultar por el sistema experto.

### Motor de Inferencia

El motor de inferencia se encuentra implementado en [env/Include/main_corales.py](env/Include/main_corales.py). A partir de las respuestas del usuario, el sistema:

- interpreta las características ingresadas,
- compara dichas características con la base de conocimiento,
- filtra las especies candidatas,
- y propone una o varias opciones compatibles.

Para este proyecto se emplea lógica difusa, ya que el sistema no depende únicamente de coincidencias exactas. En muchos casos, las respuestas del usuario pueden ser imprecisas o expresadas de forma natural, por lo que el motor combina coincidencias textuales, similitud semántica y reglas de clasificación para obtener resultados útiles y aproximados.

### Diagrama de Arquitectura

El sistema está compuesto por los siguientes módulos:

- Interfaz de usuario: desarrollada con Streamlit.
- Base de conocimiento: archivo JSON con la información de los corales.
- Motor de inferencia: lógica de Difusa y filtrado de candidatos.
- Módulo de administración: manejo de agregar, editar y eliminar especies.

## Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip
- Git
- Streamlit
- Docker opcional, si se desea ejecutar en contenedor

### Pasos de instalación

1. Clona el repositorio:

```powershell
git clone <URL-del-repositorio>
cd "Grupo 2 Corales 1"
```

2. Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

4. Ejecuta la aplicación:

```powershell
streamlit run env\Include\main_corales.py
```
### Ejecutar la aplicación con Docker

Si se desea usar Docker, se recomienda seguir estos pasos:

1. Asegúrese de tener Docker Desktop instalado y en ejecución.
2. Abra la terminal en la raíz del proyecto.
3. Construya la imagen del contenedor:

```powershell
docker build -t coralbot_app .
```

4. Ejecute el contenedor:

```powershell
docker run --rm -p 8501:8501 coralbot_app
```

5. Abra el navegador en la dirección:

```text
http://localhost:8501
```

6. Si el puerto 8501 ya está ocupado, puede cambiar el mapeo de puertos, por ejemplo:

```powershell
docker run --rm -p 8502:8501 coralbot_app
```


## Guía de Uso

La aplicación ofrece varios modos de interacción y puede ejecutarse tanto de forma local como mediante Docker. A continuación se presenta una guía más detallada para utilizarla correctamente.

### 1. Catálogo de corales

Permite explorar las especies registradas, buscar información y revisar los atributos de cada coral.

Pasos recomendados:

- abra la vista de catálogo desde la barra lateral,
- use la barra de búsqueda para filtrar por nombre, familia, género o palabras clave,
- revise la descripción del coral y sus atributos principales,
- y utilice esta vista para conocer mejor la base de conocimiento del sistema.

### 2. Chatbot de identificación

El usuario puede escribir respuestas breves o frases descriptivas, por ejemplo:

- "coral ramificado en aguas someras"
- "Acropora"
- "coral masivo en profundidad media"

El sistema interpreta la entrada y muestra las especies más compatibles. Esta opción es ideal para usuarios que desean una respuesta rápida y sencilla.

### 3. Cuestionario experto

El usuario responde preguntas morfológicas y taxonómicas para refinar la identificación. Por ejemplo:

1. ¿La colonia es ramificada?
2. ¿Las ramas terminan en un cáliz central prominente?
3. ¿La forma de las ramas es cilíndrica o aplanada?

Con estas respuestas, el sistema reduce las opciones y puede devolver una especie probable. Esta opción es más adecuada cuando se desea una identificación más técnica y precisa.

### 4. Inicio de sesión de administrador

El administrador puede ingresar con las credenciales:

- Usuario: admin
- Contraseña: admin123

Una vez autenticado, puede agregar, editar o eliminar especies del catálogo. Esta sección permite mantener la base de conocimiento actualizada.

### 5. Recomendaciones de uso

- para obtener resultados más precisos, describa las características del coral con detalle,
- si no está seguro de la respuesta, puede usar el cuestionario experto,
- y si desea actualizar la información del sistema, debe iniciar sesión como administrador.

## Ejemplos de Ejecución

A continuación se presentan tres ejemplos detallados de cómo podría utilizarse la aplicación en la práctica.

### Ejemplo 1: Uso del Chatbot

Escenario:

Un usuario desea identificar un coral que observa en el mar y escribe una descripción breve.

Acción del usuario:

- Ingresa a la aplicación.
- Selecciona la opción de chatbot.
- Escribe: "coral ramificado en aguas someras".

Qué hace el sistema:

- Reconoce palabras clave como "ramificado" y "aguas someras".
- Interpreta que la forma del coral es ramificada y que su profundidad ideal es somera.
- Compara estas características con la base de conocimiento.

Resultado esperado:

- El sistema muestra una o varias especies candidatas compatibles con esa descripción.
- En la interfaz aparece la propuesta más probable junto con información adicional sobre la especie.

### Ejemplo 2: Uso del Cuestionario Experto

Escenario:

Un usuario desea una identificación más técnica y precisa.

Acción del usuario:

- Entra al modo cuestionario.
- Responde la primera pregunta con: "Ramificado".
- Responde la segunda pregunta con: "Sí".
- Responde la tercera pregunta con: "Cilíndricas".

Qué hace el sistema:

- Usa cada respuesta para reducir el conjunto de especies candidatas.
- Aplica reglas de clasificación y lógica difusa para encontrar las opciones más compatibles.
- Continúa con nuevas preguntas si la identificación aún no es definitiva.

Resultado esperado:

- El sistema puede devolver una especie probable, por ejemplo un coral del tipo Acropora, junto con su descripción, familia y características morfológicas.
- Si la coincidencia no es total, muestra las especies que siguen siendo posibles.

### Ejemplo 3: Uso del Catálogo

Escenario:

Un usuario desea consultar información de una especie específica sin usar el chatbot ni el cuestionario.

Acción del usuario:

- Ingresa a la aplicación.
- Selecciona la opción de catálogo.
- Escribe en la barra de búsqueda: "Acropora".

Qué hace el sistema:

- Filtra las especies que coinciden con la búsqueda.
- Muestra tarjetas o información resumida de cada coral encontrado.
- Permite revisar sus atributos principales como familia, género, profundidad y forma.

Resultado esperado:

- El usuario visualiza los corales relacionados con la búsqueda y puede explorar su información detallada.

### Ejemplo 4: Uso del Panel de Administración

Escenario:

Un administrador desea actualizar la base de conocimiento con una nueva especie.

Acción del administrador:

- Inicia sesión con las credenciales de administrador.
- Entra al panel de gestión.
- Completa los campos: nombre científico, familia, género, profundidad, forma, complejidad y descripción.
- Guarda la información.

Qué hace el sistema:

- Registra la nueva especie en el catálogo.
- Crea automáticamente un respaldo del archivo JSON antes de guardar los cambios.

Resultado esperado:

- La nueva especie queda disponible en el catálogo y podrá ser usada en futuras identifications.

## Conclusiones y Trabajo Futuro

Este proyecto permitió integrar conceptos de inteligencia artificial, sistemas expertos y desarrollo de interfaces interactivas en una herramienta útil para la identificación de corales. Durante el desarrollo se enfrentaron desafíos relacionados con la organización del conocimiento, la interpretación de respuestas imprecisas y la mejora de la experiencia del usuario.

Como trabajo futuro, se propone:

- ampliar la base de conocimiento con más especies,
- mejorar la precisión del motor de inferencia,
- incorporar imágenes y visualización más detallada,
- y desarrollar una versión con mayor capacidad de análisis semántico.

## Referencias

Weil, E. (2003). Coral and coral reefs of Venezuela, pp. 303-330. En: Cortés, J. (ed.). Latin American Coral Reefs. Amsterdam: Elsevier.

Sant, S., et al. (2002 / 2003). Composición de especies de corales pétreos en las bahías de Santa Fe, Mochima y Manzanillo, Parque Nacional Mochima.

Pauls, S. (1982 / 1988). Estudio de las comunidades coralinas del Parque Nacional Mochima. (Trabajos pioneros y monografías de referencia sobre la caracterización y zonificación de los arrecifes franjeantes en esta área protegida de los estados Sucre y Anzoátegui).

Abbott, R. (1974). American Seashells. Van Nostrand Reinhold Co., New York. 663 pp.

Abbott, T. & P. Morris. (1995). A field guide to shells of the Atlantic and Gulf Coasts.

Cervigón, F. (1991 / 1993). Trabajos y guías de identificación de peces de las costas de Venezuela.

Humann, P. & N. DeLoach. (2002). Reef coral identification, Florida, Caribbean, Bahamas. 2ª ed. New World Publications Inc., Florida.

Lutz, M. (2013). Learning Python (5th ed.). O'Reilly Media. (Referencia fundamental para comprender las bases de la sintaxis, estructuras de datos y programación orientada a objetos en Python).

McKinney, W. (2022). Python for Data Analysis: Data Wrangling with Pandas, NumPy, and Jupyter (3rd ed.). O'Reilly Media. (Indispensable si tu aplicación procesa bases de datos, fichas en formato JSON o tablas de registros de especies de corales).

Streamlit Inc. (2026). Streamlit Documentation: The fastest way to build and share data apps. Sitio web oficial: docs.streamlit.io. (La fuente principal para consultar widgets, manejo de estados de sesión st.session_state, formularios y despliegue).

Sykalo, A. (2023). Getting Started with Streamlit: Build interactive web applications for data science and machine learning in Python. Packt Publishing. (Un libro práctico enfocado en llevar modelos y sistemas basados en Python directamente a interfaces web interactivas).
