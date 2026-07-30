*Sistema Identificador de Macroalgas*
# Grupo 7
**Integrantes:**
            Asencion Gonzáles CI:31502822
            Diego Tovar CI:30414491
            Jorge La Rosa CI:30708170
```markdown
# 🔬 Sistema Experto - Identificación y Clasificación de Algas

Aplicación de escritorio desarrollada en **Python** y **CustomTkinter** diseñada como un sistema experto interactivo para la identificación, estudio y clasificación de macroalgas marinas (*Chlorophyta*, *Phaeophyceae*, *Rhodophyta*).

El sistema combina un cuestionario de identificación asistida en cascada mediante claves dicotómicas con una galería interactiva y un módulo seguro de gestión de usuarios.

---
## 🌟 Características Principales

* 🔒 **Autenticación y Seguridad**:
  * Sistema de inicio de sesión y registro de usuarios con almacenamiento de contraseñas encriptadas mediante el algoritmo **SHA-256**.
  * Control de cupos con un límite configurable de usuarios del sistema (máximo 6 usuarios).
  * Panel de administración para visualizar y eliminar cuentas registradas.

* 🧠 **Identificador Asistido (Cuestionario en Cascada)**:
  * Motor de búsqueda y filtrado dinámico en tres niveles: **Clase $\rightarrow$ Familia $\rightarrow$ Clave Dicotómica**.
  * Desbloqueo progresivo de opciones basado en la taxonomía seleccionada.
  * Acceso directo a la ficha técnica completa del espécimen identificado.

* 🖼️ **Galería Interactiva y Búsqueda**:
  * Visualización mediante tarjetas interactivas (*cards*) con taxonomía e imagen representativa.
  * Búsqueda en tiempo real por nombre de especie.
  * Filtro rápido por grandes grupos taxonómicos (*Todas*, *Chlorophyta*, *Phaeophyceae*, *Rhodophyta*).

* 📝 **Gestión de la Base de Conocimiento**:
  * Formulario *in-app* para el registro de nuevas especies.
  * Inserción de datos taxonómicos, morfología del talo, estructura celular, hábitat, patrón de fijación y claves de identificación.
  * Recarga en caliente (*hot reload*) de la galería e identificador al registrar una nueva especie.

* 🚀 **Optimización de Rendimiento**:
  * Módulo de caché de imágenes para prevenir consumo excesivo de memoria RAM y lecturas redundantes en disco.

---
## 📁 Estructura del Proyecto

```text
.
├── main.py                  # Punto de entrada principal de la aplicación
├── assets/                  # Directorio de imágenes de los especímenes (PNG/JPG)
├── data/
│   ├── algas_db.json        # Base de conocimiento (Especies y sus características)
│   ├── gestor_datos.py      # Gestor de persistencia e inserción de algas en JSON
│   ├── gestor_usuarios.py   # Gestor de autenticación, hash SHA-256 y usuarios
│   └── usuarios.json        # Base de datos local de credenciales (auto-generado)
└── gui/
    ├── componentes.py       # Componentes visuales reutilizables (Tarjetas de Galería)
    ├── identificador.py     # Lógica de filtrado en cascada para el identificador asistido
    ├── interfaz.py          # Ventana principal (Navbar, Identificador y Galería)
    ├── login.py              # Ventana de autenticación y creación de cuenta
    ├── utilidades.py        # Gestor de caché y utilidades de interfaz
    └── ventanas.py          # Ventanas modales (Detalle, Añadir Especie, Gestión de Usuarios)

```

---
## 🛠️ Requisitos e Instalación

### Requisitos Previos

* **Python 3.8** o superior instalado en el sistema.

### Dependencias

El proyecto utiliza las siguientes librerías de Python:

* `customtkinter`: Interfaz gráfica moderna con soporte para modo oscuro/claro automático.
* `Pillow` (`PIL`): Procesamiento y redimensionamiento de imágenes.

Para instalarlas, ejecuta el siguiente comando en la consola:

```bash
pip install customtkinter pillow

```

---
## 🚀 Modo de Uso

1. **Asegurar la estructura de archivos**:
Asegúrate de que la carpeta `assets/` exista y contenga las imágenes correspondientes o la imagen por defecto (`default.png`).

2. **Ejecutar la aplicación**:
```bash
python main.py

```

3. **Credenciales por defecto**:
Si ejecutas la aplicación por primera vez sin un archivo `usuarios.json` previo, el sistema creará automáticamente la siguiente cuenta de usuario:
* **Usuario:** `admin`
* **Contraseña:** `admin123`

# Nota: **también puedes crear un nuevo ususario**

---
## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **GUI Framework:** CustomTkinter / Tkinter
* **Persistencia de Datos:** JSON (NoSQL estructurado)
* **Seguridad:** Encriptación SHA-256 (`hashlib`)
* **Procesamiento de Imágenes:** Pillow (PIL)

```
```
