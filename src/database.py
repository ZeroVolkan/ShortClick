from sqlmodel import create_engine

from .logger import logger
from .models import *  # noqa: F403  # нужен для регистрации модели в metadata

path_database = "database.db"
engine = create_engine(f"sqlite:///{path_database}", echo=True)
logger.info(f"Database engine created: {engine}")
logger.info(f"Database path: {path_database}")

# SQLModel.metadata.create_all(engine) # Миграции через Alembic


__all__ = ["engine"]
