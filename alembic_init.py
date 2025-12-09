"""
Script para inicializar Alembic y crear la primera migración
Ejecutar con: python alembic_init.py
"""

import os
import subprocess
from pathlib import Path

def init_alembic():
    """Inicializar Alembic si no existe"""
    alembic_path = Path("alembic")
    
    if not alembic_path.exists():
        print("Inicializando Alembic...")
        subprocess.run(["alembic", "init", "alembic"], check=True)
        print("✓ Alembic inicializado")
    else:
        print("✓ Alembic ya está inicializado")

if __name__ == "__main__":
    init_alembic()
    print("\nProximos pasos:")
    print("1. Editar alembic/env.py para usar tu SQLAlchemy metadata")
    print("2. Ejecutar: alembic revision --autogenerate -m 'Initial migration'")
    print("3. Ejecutar: alembic upgrade head")
