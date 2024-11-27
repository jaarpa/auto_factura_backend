from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.tickets.domain.entities.ticket import Ticket


@dataclass
class Issuer(Entity):
    """
    Catalog of entities that could emit a ticket that could later be invoiced
    """

    name: str
    label: str
    description: str

    tickets: list["Ticket"] = field(repr=False, default_factory=list)
