# 1. Usar una imagen oficial y ligera de Python
FROM python:3.12-slim

# 2. Establecer la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar primero el archivo de requerimientos
COPY requirements.txt .

# 4. Instalar las dependencias sin guardar caché para ahorrar espacio
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el resto de tu proyecto (código, json, carpeta de imágenes)
COPY . .

# 6. Exponer el puerto por defecto que utiliza Streamlit
EXPOSE 8501

# 7. Comando para arrancar el Sistema Experto
# IMPORTANTE: Cambia "app.py" por el nombre exacto de tu archivo principal si es diferente
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]