from __future__ import annotations
from uuid import UUID

from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

from modules.tickets.domain.entities.ticket import Ticket
from modules.files.domain.entities.file import File
from modules.accounts.domain.entities.user import User
from modules.emissors.domain.entities.emissor import Emissor


class TicketModel(Base):
    """
    Defines the ticket table
    """

    __tablename__ = "ticket"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    emissor_id: Mapped[UUID] = mapped_column(ForeignKey("emissor.id"))
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file.id"))

    # user: Mapped["UserModel"] = relationship(back_populates="tickets")
    # emissor: Mapped["EmissorModel"] = relationship(back_populates="tickets")
    # file: Mapped["FileModel"] = relationship(
    #     back_populates="ticket", single_parent=True
    # )

    __table_args__ = (UniqueConstraint("file_id"),)


Base.registry.map_imperatively(
    Ticket,
    TicketModel.__table__,
    properties={
        "user": relationship(User, back_populates="tickets"),
        "emissor": relationship(Emissor, back_populates="tickets"),
        "file": relationship(File, back_populates="ticket", single_parent=True),
    },
)
