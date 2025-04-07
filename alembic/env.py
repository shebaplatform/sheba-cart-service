import os
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.base import Base
from app.models import cart, cart_item  # import all models

# Load environment variables
load_dotenv()

# Alembic Config object
config = context.config

# Read DB connection from env
DB_URL = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", DB_URL)

# Set up logging
fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DB_URL, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
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
