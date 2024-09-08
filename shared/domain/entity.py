from uuid import UUID
from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass
from dataclasses import field
from shared.domain import utc_now


@dataclass
class Entity:
    """
    General Entity with basic fields. Every domain entity must inherit from this.
    """

    id: UUID = field(default_factory=uuid4, kw_only=True)
    created_at: datetime = field(default_factory=utc_now, kw_only=True)
    updated_at: datetime = field(default_factory=utc_now, kw_only=True)
