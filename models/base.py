from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from shared.domain import utc_now


class Base(MappedAsDataclass, DeclarativeBase):
    """
    General base class from wich any model must inherit to be added to
    the mapping registry.
    Subclasses will be converted to dataclasses.
    """

    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        default_factory=utc_now,
        kw_only=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default_factory=utc_now,
        kw_only=True,
    )
