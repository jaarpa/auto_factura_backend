from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import Mapped
from sqlalchemy import func
from sqlalchemy.orm import mapped_column

from shared.domain import utc_now


class Base(MappedAsDataclass, DeclarativeBase):
    """
    General base class from wich any model must inherit to be added to
    the mapping registry.
    Subclasses will be converted to dataclasses.
    """

    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),  # pylint: disable=not-callable
        default_factory=utc_now,
        kw_only=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
        default_factory=utc_now,
        kw_only=True,
    )
