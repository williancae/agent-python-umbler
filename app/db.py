import databases
import sqlalchemy

from app.config.config import settings

database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()
