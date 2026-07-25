# **Título del Proyecto:** ScleraSys 

## **Integrantes del Grupo**
* Samuel Antonio Salazar Millan
* Cruz David Marcano Díaz
* Jesús Ali Brito Salazar

## **Descripción general**

**ScleraSys** es un sistema experto interactivo diseñado para el diagnóstico, clasificación e identificación taxonómica de corales pétreos ubicados en la isla de Cubagua. 

El problema principal que resuelve es la dificultad y el tiempo requerido para identificar correctamente especies marinas en el sitio por parte de investigadores o estudiantes que no poseen un nivel de experticia avanzado en biología marina. El dominio de conocimiento del sistema se centra en la morfología y ecología de los corales locales. La utilidad principal de este SE es actuar como un asistente virtual confiable que evalúa atributos dinámicos ingresados por el usuario para arrojar un porcentaje de certeza taxonómica, agilizando la toma de decisiones ecológicas y el levantamiento de inventarios marinos.

El sistema emplea un motor de inferencia determinista combinado con lógica difusa (`scikit-fuzzy`) para evaluar la certeza ecológica de las especies marinas en función de sus atributos. Desarrollado íntegramente en Python utilizando **Streamlit** para la interfaz de usuario, ScleraSys cuenta con un sistema de roles (Administrador/Visitante), un módulo de gestión (CRUD) para agregar atributos dinámicos o nuevas especies a la base de datos JSON, y un catálogo interactivo con filtros de búsqueda en tiempo real. 

---

## **Arquitectura del Sistema**

### 1. Base de Conocimientos

La base de conocimientos está estructurada en un formato no relacional utilizando un archivo `corales_cubagua.json`. 
* **Hechos:** Los datos fijos y catalogados de las especies de corales (nombres científicos, descripciones, y galerías de imágenes).
* **Reglas:** Los parámetros morfológicos y ecológicos (ej. forma de la colonia, estructura del coralito, profundidad, nivel de iluminación) que el sistema evalúa para determinar si las características ingresadas coinciden con una especie existente.

### 2. Motor de Inferencia
El sistema emplea un mecanismo de **encadenamiento hacia adelante**. El usuario ingresa los datos iniciales a través del formulario (los hechos observados) y el motor evalúa las reglas hasta llegar a una conclusión taxonómica.
* **Manejo de Incertidumbre:** ScleraSys maneja la ambigüedad inherente a las observaciones naturales mediante **lógica difusa** (utilizando la librería `scikit-fuzzy`). Esto permite que el sistema no dependa de coincidencias exactas, sino que calcule y devuelva un porcentaje de "certeza ecológica" (ej. 85% de probabilidad de que sea *Acropora cervicornis*).

---

## **Instalación y Configuración**

El proyecto está contenerizado utilizando Docker para garantizar un despliegue idéntico en cualquier entorno o sistema operativo, evitando conflictos de dependencias.

### Requisitos Previos

* Tener instalado y en ejecución [Docker Desktop](https://www.docker.com/products/docker-desktop/).
* Si se desea ejecutar sin Docker, se requiere **Python 3.10 o superior** y las librerías especificadas en el archivo `requirements.txt` (`streamlit`, `numpy`, `scipy`, `networkx`, `scikit-fuzzy`).

### Pasos para la ejecución vía Docker

1. **Clonar el proyecto** 
2. **Abrir la terminal:** Ubícarse en la raíz de la carpeta extraída (donde se encuentra el archivo `Dockerfile`).
3. **Construir la imagen:** Ejecuta el siguiente comando para compilar el entorno del sistema experto:
   ```bash
   docker build -t sclerasys_app .
   ```
4. **Correr el proyecto:** desde la terminal ejecutar:
   ```bash
   docker run -p 8501:8501 sclerasys_app
   ```
5. **Acceder al Sistema:** http://localhost:8501
6. **Usuario:** "admin" contraseña: "udo123"

---

## **Guía de Uso**

ScleraSys opera a través de una interfaz gráfica interactiva construida con Streamlit, accesible desde cualquier navegador web.

1. **Acceso al Sistema:** Abre tu navegador e ingresa a http://localhost:8501

2. **Módulo de Diagnóstico (Visitante):** En la pantalla principal, el usuario encontrará un cuestionario dinámico. Selecciona los atributos del coral observado en los menús desplegables y presiona "Evaluar Especie" para que el motor procese los datos.

3. **Módulo de Gestión (Administrador):** En el panel lateral, accede a la sección de Login utilizando las credenciales predeterminadas (Usuario: admin / Contraseña: udo123). Esto habilitará opciones CRUD para agregar, editar o eliminar corales del archivo corales_cubagua.json.

---

## **Ejemplos de Ejecución**
El sistema experto evalúa la información proporcionada por el usuario en tiempo real para generar un diagnóstico preciso.

### Caso 1: Diagnóstico de especie

* Entrada (Inputs del usuario en el formulario dinámico):

* Forma de la colonia: faldones.

* Organización de los Coralites: plocoide.

* Profundidad observada: 15 metros.

* Tipo de gemación: extratencular.


### Salida del sistema experto:

* Identificación taxonómica de la especie coincidente (Ej. Orbicella faveolata).

* Porcentaje de certeza ecológica calculado mediante lógica difusa.

* Ficha técnica detallada del coral y galería de imágenes asociadas.


### Caso 2: Gestión de Base de Datos y Prevención de Errores

* Entrada (Panel de Administración):

* Ingreso de credenciales de administrador.
Login exitoso.

* Adición de una nueva especie con descripción técnica y la creación de un nuevo atributo morfológico personalizado (Ej. "Textura del tejido coralino").

### Salida:

* Actualización automática del archivo corales_cubagua.json y del catálogo en tiempo real.

* Previo a la sobreescritura, el sistema genera automáticamente un archivo de copia de seguridad en la carpeta /respaldos para garantizar la integridad de los datos.

* La nueva especie y su atributo se vuelven inmediatamente consultables y evaluables en el motor de inferencia y el catálogo general.


## **Conclusiones y Trabajo Futuro**

### Conclusiones del desarrollo: 
El desarrollo de ScleraSys demostró la viabilidad de integrar motores de inferencia matemáticos en interfaces web modernas. El principal desafío técnico radicó en la calibración de las funciones de membresía de la lógica difusa para que los porcentajes de certeza reflejaran escenarios biológicos realistas. La implementación de un formato JSON dinámico facilitó enormemente la flexibilidad del sistema, permitiendo que la base de conocimientos escale sin necesidad de modificar el código fuente.

### Trabajo Futuro:

* Expansión de la Base de Conocimientos: Incorporar datos de corales blandos y otras zonas geográficas del Mar Caribe.

* Integración de Visión Artificial: Añadir un modelo de redes neuronales convolucionales (CNN) que permita complementar el sistema de preguntas taxonómicas con el análisis directo de fotografías subacuáticas subidas por el usuario.

* Migración a Cloud: Desplegar el contenedor de Docker en servicios en la nube (como AWS o Google Cloud) para su uso masivo.

## **Referencias**

* Documentación oficial de Scikit-Fuzzy: https://pythonhosted.org/scikit-fuzzy/

* Documentación oficial de Streamlit: https://docs.streamlit.io/

* Gómez, A., & Cervigón, F. (2024). Bionomía bentónica costera de la isla de Cubagua (Venezuela). I. Costa este y oeste. Boletín del Instituto Oceanográfico de Venezuela.

* Yranzo, A., Villamizar, E., Romero, M., & Boadas, H. (2014). Estructura de las comunidades de corales y octocorales de Isla de Aves, Venezuela, Caribe Nororiental. Revista de Biología Tropical, 62 (Suppl. 3), 115-136.

* Del Mónaco, C., Narciso, S., Alfonso, F., Gimenez, E., & Bustillos, F. (2010). Evaluación de las comunidades de corales y peces de algunos arrecifes de la isla La Tortuga y cayos adyacentes, Venezuela. Boletín del Centro de Investigaciones Biológicas, 44(3), 353-376.

* Weil, E. (2003). The corals and coral reefs of Venezuela. En J. Cortés (Ed.), Latin American Coral Reefs (pp. 303-330). Amsterdam, Países Bajos: Elsevier Science B.V.

* Reyes, J., Santodomingo, N., & Flórez, P. (2010). Corales Escleractinios de Colombia. Invemar Serie de Publicaciones Especiales, No. 14. Santa Marta, Colombia: Instituto de Investigaciones Marinas y Costeras “José Benito Vives de Andréis” (Invemar).