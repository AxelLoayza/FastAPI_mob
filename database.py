import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from dotenv import load_dotenv
from sqlalchemy import create_engine, event, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# URLs de conexión
DATABASE_URL = os.getenv("DATABASE_URL", "")  # Pool de conexión para aplicación
DIRECT_URL = os.getenv("DIRECT_URL", "")      # Conexión directa para migraciones

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en .env")

# Limpiar la URL de parámetros no soportados por psycopg2
def clean_database_url(url):
    """Remove pgbouncer=true parameter from URL as it's not supported by psycopg2"""
    parsed = urlparse(url)
    
    # Parse query string
    if parsed.query:
        params = parse_qs(parsed.query)
        # Remove pgbouncer parameter
        params.pop('pgbouncer', None)
        # Reconstruct query string
        new_query = urlencode(params, doseq=True)
    else:
        new_query = ''
    
    # Reconstruct URL
    clean_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return clean_url

# Limpiar URLs
DATABASE_URL_CLEAN = clean_database_url(DATABASE_URL)
DIRECT_URL_CLEAN = clean_database_url(DIRECT_URL) if DIRECT_URL else DATABASE_URL_CLEAN

# Configuración del motor para producción con Supabase
engine = create_engine(
    DATABASE_URL_CLEAN,
    poolclass=pool.QueuePool,
    pool_size=15,
    max_overflow=25,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "application_name": "barbershop_api"
    },
    echo=False,
)

# Motor directo para migraciones (sin pool)
direct_engine = create_engine(
    DIRECT_URL_CLEAN,
    poolclass=pool.NullPool,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
