from logging.config import fileConfig
import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Cargar variables de entorno
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from database import Base
from models import Usuario, Cita, Barbero, Cliente

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Función para limpiar URL de parámetros no soportados
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

# Obtener URL de conexión directa para migraciones
sqlalchemy_url = os.getenv("DIRECT_URL") or os.getenv("DATABASE_URL")
sqlalchemy_url = clean_database_url(sqlalchemy_url)
config.set_main_option("sqlalchemy.url", sqlalchemy_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Usar DIRECT_URL para migraciones
    url = os.getenv("DIRECT_URL") or os.getenv("DATABASE_URL")
    
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
