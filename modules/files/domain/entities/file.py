from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Optional
from dataclasses import dataclass
from dataclasses import field
from uuid import UUID

from shared.domain.entity import Entity


if TYPE_CHECKING:
    from modules.document_types.domain.entities.document_type import DocumentType
    from modules.tickets.domain.entities.ticket import Ticket


@dataclass
class File(Entity):
    """
    This represents any file uploaded to the app
    (tickets | profile pictures | etc)
    """

    name: str
    key: str
    config: dict
    document_type_id: UUID

    document_type: DocumentType = field(init=False)
    ticket: Optional[Ticket] = field(init=False)
