FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

# Instalar herramientas de compilación mínimas (si alguna dependencia necesita compilar ruedas)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copiar el código de la aplicación
COPY . /app

# Puerto por defecto de Streamlit
EXPOSE 8501

# Ejecutar la app
CMD ["streamlit", "run", "main_corales.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
