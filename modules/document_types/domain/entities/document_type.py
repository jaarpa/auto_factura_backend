from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from dataclasses import field

from shared.domain.entity import Entity

if TYPE_CHECKING:
    from modules.files.domain.entities.file import File


@dataclass
class DocumentType(Entity):
    """
    Catalog of different document type existing in the app (ticket, invoice, ...)
    """

    name: str
    label: str
    description: str

    files: list[File] = field(repr=False, default_factory=list)
