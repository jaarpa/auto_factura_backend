from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

if TYPE_CHECKING:
    from models.ticket import Ticket


class Emissor(Base):
    """
    Catalog of entities that could emit a ticket that could later be invoiced
    """

    __tablename__ = "emissor"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    label: Mapped[str]
    description: Mapped[str]

    tickets: Mapped["Ticket"] = relationship(back_populates="emissor")
