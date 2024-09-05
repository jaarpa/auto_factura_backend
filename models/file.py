from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

if TYPE_CHECKING:
    from models.document_type import DocumentType
    from models.ticket import Ticket


class File(Base):
    """
    This represents any file uploaded to the app
    (tickets | profile pictures | etc)
    """

    __tablename__ = "file"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    key: Mapped[str]
    config: Mapped[dict] = mapped_column(JSON)
    document_type_id: Mapped[UUID] = mapped_column(ForeignKey("document_type.id"))

    document_type: Mapped["DocumentType"] = relationship(
        "DocumentType", back_populates="files"
    )
    ticket: Mapped["Ticket"] = relationship(back_populates="file", default=None)
