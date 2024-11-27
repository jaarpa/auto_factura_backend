from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from modules.accounts.domain.entities.user import User
from modules.files.domain.entities.file import File
from modules.issuer.domain.entities.issuer import Issuer
from modules.tickets.domain.entities.ticket import Ticket


class TicketModel(Base):
    """
    Defines the ticket table
    """

    __tablename__ = "ticket"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    issuer_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("issuer.id"), nullable=True
    )
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file.id"))

    __table_args__ = (UniqueConstraint("file_id"),)


Base.registry.map_imperatively(
    Ticket,
    TicketModel.__table__,
    properties={
        "user": relationship(User, back_populates="tickets"),
        "issuer": relationship(Issuer, back_populates="tickets"),
        "file": relationship(File, back_populates="ticket", single_parent=True),
    },
)
