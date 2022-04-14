from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from src.database import DatabaseSettings, create_database_url
from src.database.tables import metadata

config = context.config
fileConfig(config.config_file_name)

target_metadata = metadata
db_settings = DatabaseSettings()
config.set_main_option('sqlalchemy.url', create_database_url(db_settings))


def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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


run_migrations_online()
