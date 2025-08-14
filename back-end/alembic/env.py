
import os
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'models')))

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", url)

from db import metadata
target_metadata = metadata

def run_migrations_offline():
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
