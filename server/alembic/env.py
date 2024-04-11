import os
from logging.config import fileConfig

from alembic import context
from app.models import *  # Ensure all your models are imported here
from app.models.base import Base
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool, create_engine

# This workaround is for forcing the PostgreSQL dialect to treat the database as a specific version.
# It can be useful for compatibility issues, but be cautious using it.
from sqlalchemy.dialects.postgresql.base import PGDialect
PGDialect._get_server_version_info = lambda *args: (9, 2)

load_dotenv()  # Load environment variables from .env file, if it exists

# Use the environment variable for the database URL
database_url = os.getenv("POSTGRES_URL")

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = database_url  # Use the database URL from environment variable
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Override the sqlalchemy.url configuration from the Alembic config with database_url
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
