from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID
from dataclasses import dataclass
from dataclasses import field

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.accounts.domain.entities.user import User
    from modules.files.domain.entities.file import File
    from modules.emissors.domain.entities.emissor import Emissor


@dataclass
class Ticket(Entity):
    """
    Represents a ticket with all its related data like ticket file, emissor
    author
    """

    user_id: UUID
    emissor_id: UUID
    file_id: UUID
    data: dict = field(default_factory=dict)

    user: User = field(init=False)
    emissor: File = field(init=False)
    file: Emissor = field(init=False)
