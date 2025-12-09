#!/usr/bin/env python3
"""
Script de utilidades para migraciones con Alembic y Supabase
Uso:
    python migrate.py --help
    python migrate.py create "nombre de la migración"
    python migrate.py upgrade
    python migrate.py downgrade
"""

import argparse
import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

ALEMBIC_DIR = Path("alembic")

def check_alembic_initialized():
    """Verificar si Alembic está inicializado"""
    return ALEMBIC_DIR.exists()

def init():
    """Inicializar Alembic"""
    if check_alembic_initialized():
        print("✓ Alembic ya está inicializado")
        return
    
    print("Inicializando Alembic...")
    subprocess.run(["alembic", "init", "alembic"], check=True)
    print("✓ Alembic inicializado")
    print("\nEdita alembic/env.py y configura los parámetros de conexión")

def create(name):
    """Crear una nueva migración"""
    if not check_alembic_initialized():
        print("✗ Alembic no está inicializado. Ejecuta: python migrate.py init")
        return
    
    print(f"Creando migración: {name}")
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", name], check=True)
    print(f"✓ Migración creada: {name}")

def upgrade(revision="head"):
    """Ejecutar migraciones pendientes"""
    print(f"Ejecutando migraciones hasta: {revision}")
    subprocess.run(["alembic", "upgrade", revision], check=True)
    print(f"✓ Migraciones aplicadas")

def downgrade(revision):
    """Revertir migraciones"""
    if not revision:
        print("✗ Debes especificar la revisión a la que revertir")
        return
    
    print(f"Revirtiendo migraciones a: {revision}")
    subprocess.run(["alembic", "downgrade", revision], check=True)
    print(f"✓ Migraciones revertidas")

def status():
    """Ver estado de las migraciones"""
    print("Estado de las migraciones:")
    subprocess.run(["alembic", "current"], check=True)
    print("\nHistorial de migraciones:")
    subprocess.run(["alembic", "history"], check=True)

def main():
    parser = argparse.ArgumentParser(
        description="Utilidad de migraciones para Supabase con Alembic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python migrate.py init                    # Inicializar Alembic
  python migrate.py create "Add users"      # Crear nueva migración
  python migrate.py upgrade                 # Aplicar todas las migraciones
  python migrate.py downgrade -1            # Revertir última migración
  python migrate.py status                  # Ver estado actual
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Inicializar Alembic")
    
    create_parser = subparsers.add_parser("create", help="Crear nueva migración")
    create_parser.add_argument("name", help="Nombre de la migración")
    
    upgrade_parser = subparsers.add_parser("upgrade", help="Aplicar migraciones")
    upgrade_parser.add_argument("revision", nargs="?", default="head", 
                               help="Revisión objetivo (default: head)")
    
    downgrade_parser = subparsers.add_parser("downgrade", help="Revertir migraciones")
    downgrade_parser.add_argument("revision", help="Revisión a la que revertir")
    
    subparsers.add_parser("status", help="Ver estado de migraciones")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init()
    elif args.command == "create":
        create(args.name)
    elif args.command == "upgrade":
        upgrade(args.revision)
    elif args.command == "downgrade":
        downgrade(args.revision)
    elif args.command == "status":
        status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
