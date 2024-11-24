from __future__ import annotations

from uuid import UUID

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from modules.document_types.domain.entities.document_type import DocumentType
from modules.files.domain.entities.file import File
from modules.tickets.domain.entities.ticket import Ticket


class FileModel(Base):
    """
    Defines the File table
    """

    __tablename__ = "file"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    key: Mapped[str]
    config: Mapped[dict] = mapped_column(JSON)
    document_type_id: Mapped[UUID] = mapped_column(ForeignKey("document_type.id"))


Base.registry.map_imperatively(
    File,
    FileModel.__table__,
    properties={
        "document_type": relationship(DocumentType, back_populates="files"),
        "ticket": relationship(Ticket, back_populates="file"),
    },
)
