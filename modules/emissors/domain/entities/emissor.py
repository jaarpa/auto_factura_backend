from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from dataclasses import field

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.tickets.domain.entities.ticket import Ticket


@dataclass
class Emissor(Entity):
    """
    Catalog of entities that could emit a ticket that could later be invoiced
    """

    name: str
    label: str
    description: str

    tickets: list["Ticket"] = field(repr=False, default_factory=list)
