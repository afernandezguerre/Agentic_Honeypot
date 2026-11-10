# Usamos una imagen oficial de Python como base
FROM python:3.11-slim

# Copiamos el binario de uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Activamos el bytecode de python y evitamos el buffering de los logs
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Primero copiamos los archivos de configuración de dependencias para aprovechar la caché de Docker
COPY pyproject.toml uv.lock ./

# Instalamos las dependencias del proyecto sin crear un entorno virtual dentro (los paquetes van al sistema global del contenedor)
RUN uv sync --frozen --no-dev --no-install-project

# Copiamos el resto del código del proyecto
COPY . /app

# Si necesitas instalar el propio proyecto (si está empaquetado)
RUN uv sync --frozen --no-dev

# Comando por defecto para ejecutar tu aplicación (ej: main.py)
CMD ["uv", "run", "python", "main.py"]