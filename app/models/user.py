from ormar import Integer, Model, OrmarConfig, String

from app.db import database, metadata

ormar_config = OrmarConfig(
    database=database,
    metadata=metadata,
)


class User(Model):
    ormar_config = ormar_config
    ormar_config.tablename = "users"

    id: int = Integer(primary_key=True)
    name: str = String(max_length=100)
    email: str = String(max_length=100, unique=True, nullable=False)
