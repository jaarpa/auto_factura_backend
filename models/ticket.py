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
    from models.user import User
    from models.file import File
    from models.emissor import Emissor


class Ticket(Base):
    """
    Represents a ticket with all its related data like ticket file, emissor
    author
    """

    __tablename__ = "ticket"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    emissor_id: Mapped[UUID] = mapped_column(ForeignKey("emissor.id"))
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file.id"))

    user: Mapped["User"] = relationship(back_populates="tickets")
    emissor: Mapped["Emissor"] = relationship(back_populates="tickets")
    file: Mapped["File"] = relationship(back_populates="ticket")
