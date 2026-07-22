# ScleraSys 🪸

## Descripción general
**ScleraSys** es un sistema experto interactivo diseñado para el diagnóstico, clasificación e identificación taxonómica de corales pétreos ubicados en la isla de Cubagua. 

El sistema emplea un motor de inferencia determinista combinado con lógica difusa (`scikit-fuzzy`) para evaluar la certeza ecológica de las especies marinas en función de sus atributos. Desarrollado íntegramente en Python utilizando **Streamlit** para la interfaz de usuario, ScleraSys cuenta con un sistema de roles (Administrador/Visitante), un módulo de gestión (CRUD) para agregar atributos dinámicos o nuevas especies a la base de datos JSON, y un catálogo interactivo con filtros de búsqueda en tiempo real. 

---

## Instrucciones de instalación y uso

El proyecto está contenerizado utilizando Docker para garantizar un despliegue idéntico en cualquier entorno o sistema operativo, evitando conflictos de dependencias.

### Requisitos previos
* Tener instalado y en ejecución [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Pasos para la ejecución vía Docker
1. **Clonar el proyecto** 
2. **Abrir la terminal:** Ubícarse en la raíz de la carpeta extraída (donde se encuentra el archivo `Dockerfile`).
3. **Construir la imagen:** Ejecuta el siguiente comando para compilar el entorno del sistema experto:
   ```bash
   docker build -t sclerasys_app .
4. **Correr el proyecto:** desde la terminal ejecutar docker run -p 8501:8501 sclerasys_app
5. **Acceder al Sistema:** http://localhost:8501
6. **Usuario:** "admin" contraseña: "udo123"

# Ejemplos de entrada/salida
El sistema experto evalúa la información proporcionada por el usuario en tiempo real para generar un diagnóstico preciso.

# Ejemplo 1: Diagnóstico de especie
Entrada (Inputs del usuario en el formulario dinámico):

Forma de la colonia: Ramificada.

Estructura del coralito: Sobresaliente.

Profundidad observada: 5 metros.

Nivel de iluminación: Alta.

# Salida del sistema experto:

Identificación taxonómica de la especie coincidente (Ej. Acropora cervicornis).

Porcentaje de certeza ecológica calculado mediante lógica difusa.

Ficha técnica detallada del coral y galería de imágenes asociadas.

# Ejemplo 2: Gestión de base de datos (Módulo Administrador)
Entrada:

Ingreso de credenciales de administrador.

Adición de una nueva especie con descripción técnica y la creación de un nuevo atributo morfológico personalizado (Ej. "Textura del tejido coralino").

# Salida:

Actualización automática del archivo corales_cubagua.json.

Generación de un respaldo automático en la carpeta respaldos/ previo a la modificación para evitar pérdida de datos.

La nueva especie y su atributo se vuelven inmediatamente consultables y evaluables en el motor de inferencia y el catálogo general.