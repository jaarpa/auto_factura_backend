from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import Mapped
from sqlalchemy import func
from sqlalchemy.orm import mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    """
    General base class from wich any model must inherit to be added to
    the mapping registry.
    Subclasses will be converted to dataclasses.
    """

    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()  # pylint: disable=not-callable
    )
    updeated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(), onupdate=func.now()  # pylint: disable=not-callable
    )
