from sqlalchemy import create_engine
from sqlalchemy import URL

from shared.infrastructure.pyenviron import PyEnviron
from .base import Base
from .document_type import DocumentType
from .emissor import Emissor
from .file import File
from .ticket import Ticket
from .user import User

_environ = PyEnviron()

database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=_environ.get_str("APP_USER"),
    password=_environ.get_str_from_path("APP_PASSWORD_FILE"),
    host=_environ.get_str("APP_DB_HOST"),
    port=_environ.get_int("POSTGRES_PORT"),
    database=_environ.get_str("APP_DB"),
)

engine = create_engine(database_url)


__all__ = [
    "Base",
    "DocumentType",
    "Emissor",
    "File",
    "Ticket",
    "User",
]
