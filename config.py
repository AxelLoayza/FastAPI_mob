"""
Configuración de la aplicación FastAPI para diferentes entornos
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DIRECT_URL = os.getenv("DIRECT_URL")

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    ENVIRONMENT = "development"

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    ENVIRONMENT = "production"

# Seleccionar configuración según el entorno
if os.getenv("ENVIRONMENT") == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()
