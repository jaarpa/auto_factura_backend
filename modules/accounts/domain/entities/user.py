from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.tickets.domain.entities.ticket import Ticket


@dataclass
class User(Entity):
    """
    User entity
    """

    email: str

    tickets: list["Ticket"] = field(repr=False, default_factory=list)
