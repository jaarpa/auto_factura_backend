from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.accounts.domain.entities.user import User
    from modules.files.domain.entities.file import File
    from modules.issuer.domain.entities.issuer import Issuer


@dataclass
class Ticket(Entity):
    """
    Represents a ticket with all its related data like ticket file, issuer
    author
    """

    user_id: UUID
    issuer_id: UUID
    file_id: UUID
    data: dict = field(default_factory=dict)

    user: User = field(init=False)
    file: File = field(init=False)
    issuer: Issuer = field(init=False)
