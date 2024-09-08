from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlalchemy import URL

from shared.infrastructure.pyenviron import PyEnviron

from .base import Base
from .document_type import DocumentTypeModel
from .emissor import EmissorModel
from .file import FileModel
from .ticket import TicketModel
from .user import UserModel

_environ = PyEnviron()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=_environ.get_str("APP_USER"),
    password=_environ.get_str_from_path("APP_PASSWORD_FILE"),
    host=_environ.get_str("APP_DB_HOST"),
    port=_environ.get_int("POSTGRES_PORT"),
    database=_environ.get_str("APP_DB"),
)

engine = create_engine(
    database_url, echo=_environ.get_bool("DEBUG"), echo_pool=_environ.get_bool("DEBUG")
)
async_engine = create_async_engine(
    database_url, echo=_environ.get_bool("DEBUG"), echo_pool=_environ.get_bool("DEBUG")
)

__all__ = [
    "Base",
    "DocumentTypeModel",
    "EmissorModel",
    "FileModel",
    "TicketModel",
    "UserModel",
]
