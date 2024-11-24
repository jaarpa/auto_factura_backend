from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from modules.accounts.domain.entities.user import User
from modules.tickets.domain.entities.ticket import Ticket


class UserModel(Base):
    """
    Defines the user table
    """

    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()


Base.registry.map_imperatively(
    User,
    UserModel.__table__,
    properties={
        "tickets": relationship(Ticket, back_populates="user", repr=False),
    },
)
