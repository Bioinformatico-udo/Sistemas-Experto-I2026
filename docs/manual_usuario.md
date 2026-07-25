# Manual de Usuario - Sistema Experto Taxonómico Los Roques

Este manual describe el funcionamiento y el uso del sistema experto para la clasificación e identificación de especies marinas del Parque Nacional Archipiélago de Los Roques.

## 📌 Introducción
El sistema utiliza un **árbol de decisión dicotómico** para guiar al usuario mediante preguntas sencillas de opción múltiple basadas en la morfología del espécimen que se desea clasificar.

## 🚀 Requisitos e Instalación

### Requisitos Previos
* Python 3.8 o superior.
* `pip` (administrador de paquetes de Python).

### Instalación
1. Clone el repositorio y navegue hasta el directorio del proyecto:
   ```bash
   cd Sistemas-Experto-I2026
   ```
2. Instale las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Instrucciones de Uso

1. Ejecute la aplicación principal:
   ```bash
   python src/main.py
   ```
2. Se presentará el menú principal:
   - **1) Identificar un organismo (Diagnóstico):** Inicia la encuesta interactiva basada en el árbol de decisión taxonómico.
   - **2) Listar especies registradas:** Muestra una lista de todas las especies conocidas por la base de datos con su información ecológica.
   - **3) Salir:** Cierra la aplicación.

### Flujo de Diagnóstico (Opción 1)
* El sistema le hará preguntas como: *¿El organismo pertenece al reino animal o vegetal/alga?*
* Escriba el número de la opción que corresponda a su espécimen.
* Si desea cancelar el proceso en cualquier momento, presione `0`.
* Al finalizar el recorrido, el sistema le ofrecerá una explicación con la especie clasificada y el camino de inferencia que se siguió.
