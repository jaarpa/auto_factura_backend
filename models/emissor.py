from __future__ import annotations
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base
from modules.emissors.domain.entities.emissor import Emissor
from modules.tickets.domain.entities.ticket import Ticket


class EmissorModel(Base):
    """
    Defines the Emissor table
    """

    __tablename__ = "emissor"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    label: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


Base.registry.map_imperatively(
    Emissor,
    EmissorModel.__table__,
    properties={"tickets": relationship(Ticket, back_populates="emissor", repr=False)},
)
