# Utilizamos una imagen de Python 3.11 como base
FROM python:3.11

# Instalar dependencias de sistema
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt


# Instalamos el cliente de PostgreSQL
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Exponemos el puerto 80
EXPOSE 80

# Iniciamos el servidor web
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
