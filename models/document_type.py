from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from modules.document_types.domain.entities.document_type import DocumentType
from modules.files.domain.entities.file import File


class DocumentTypeModel(Base):
    """
    Defines the DocumentType table
    """

    __tablename__ = "document_type"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    label: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


Base.registry.map_imperatively(
    DocumentType,
    DocumentTypeModel.__table__,
    properties={
        "files": relationship(File, back_populates="document_type", repr=False)
    },
)
