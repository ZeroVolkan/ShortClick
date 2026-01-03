from sqlmodel import SQLModel, create_engine

from .models import *  # noqa: F403  # нужен для регистрации модели в metadata

path_database = "database.db"
engine = create_engine(f"sqlite:///{path_database}", echo=True)

# SQLModel.metadata.create_all(engine) # Миграции будут через Alembic
