from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from dataclasses import field

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.tickets.domain.entities.ticket import Ticket


@dataclass
class User(Entity):
    """
    User entity protocol
    """

    email: str

    tickets: list["Ticket"] = field(repr=False, default_factory=list)
