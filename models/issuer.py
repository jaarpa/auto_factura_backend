from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from modules.issuer.domain.entities.issuer import Issuer
from modules.tickets.domain.entities.ticket import Ticket


class IssuerModel(Base):
    """
    Defines the Issuer table
    """

    __tablename__ = "issuer"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    label: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


Base.registry.map_imperatively(
    Issuer,
    IssuerModel.__table__,
    properties={"tickets": relationship(Ticket, back_populates="issuer", repr=False)},
)
