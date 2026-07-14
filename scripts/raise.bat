@echo off

REM ==========================================
REM Levantar contenedores Docker
REM ==========================================

echo Iniciando base de datos PostgreSQL...

docker compose up -d

REM ==========================================
REM Mostrar contenedores creados
REM ==========================================

echo.
echo Contenedores activos:
docker ps -a

pause