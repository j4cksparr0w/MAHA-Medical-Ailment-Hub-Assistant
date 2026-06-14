import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from db import Base
import models

config = context.config
load_dotenv()

target = os.getenv("DB_TARGET", "local").lower()
url = os.getenv("DATABASE_URL_SUPABASE") if target == "supabase" else os.getenv("DATABASE_URL_LOCAL")

if not url:
    raise RuntimeError("Missing DATABASE_URL_LOCAL / DATABASE_URL_SUPABASE")

config.set_main_option("sqlalchemy.url", url)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
