from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

if TYPE_CHECKING:
    from models.file import File


class DocumentType(Base):
    """
    Catalog of different document type existing in the app (ticket, invoice, ...)
    """

    __tablename__ = "document_type"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    label: Mapped[str]
    description: Mapped[str]

    files: Mapped[list["File"]] = relationship(back_populates="document_type")
