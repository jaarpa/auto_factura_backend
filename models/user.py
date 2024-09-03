from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    """
    User. Credentials should be managed by cognito
    """

    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str]

    tickets = relationship("Ticket", back_populates="user")
