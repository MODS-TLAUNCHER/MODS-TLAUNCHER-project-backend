#!/bin/bash

# ==========================================
# Levantar contenedores Docker
# ==========================================

echo "Iniciando base de datos PostgreSQL..."

docker compose up -d

# ==========================================
# Mostrar contenedores creados
# ==========================================

echo ""
echo "Contenedores activos:"
docker ps -a