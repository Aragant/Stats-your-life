from logging.config import fileConfig
import os

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.core.config import settings
from app.core.db import Base

from app.task.model import Task
from app.user.model import User

load_dotenv()

# --- Alembic config ---
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# C’est ça que Alembic utilise pour autogenerate
target_metadata = Base.metadata




# --- Connexion async ---
def get_url():
    return settings.DATABASE_URL


def run_migrations_offline():
    """Mode offline (génère SQL sans se connecter à la DB)."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Mode online (connexion réelle à la DB)."""
    connectable = create_async_engine(get_url(), poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # détecte les changements de type
        render_as_batch=True,  # utile si SQLite tests
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
