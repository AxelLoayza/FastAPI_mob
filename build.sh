#!/bin/bash
# Script de construcción para Render

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar migraciones de Alembic
alembic upgrade head

echo "✓ Build completado - Migraciones aplicadas"
