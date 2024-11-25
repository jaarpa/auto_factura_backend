import datetime
import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from fastapi_app.endpoints import router
from modules.tickets.domain.entities.ticket import Ticket
from shared.domain.repository import Repository

logger = logging.getLogger(__name__)

# TODO: Refactor into a more generic Catalog response
class IssuerResponse(BaseModel):
    id: UUID
    label: str
    name: str
    model_config = {"from_attributes": True}


class DocumentTypeResponse(BaseModel):
    id: UUID
    label: str
    name: str
    model_config = {"from_attributes": True}


class FileResponse(BaseModel):
    id: UUID
    name: str
    document_type: DocumentTypeResponse
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


class TicketResponse(BaseModel):
    id: UUID
    file: FileResponse
    issuer: IssuerResponse | None
    data: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


@router.get("/ticket/{ticket_id}/")
@inject
async def get_file_info(
    ticket_id: UUID,
    ticket_repository: Repository[Ticket] = Depends(Provide["ticket_repository"]),
) -> TicketResponse:
    # TODO: Validate that the user actually is the owner of this ticket
    ticket = ticket_repository.get(ticket_id)
    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No ticket with id {ticket_id}")
    return TicketResponse.model_validate(ticket)
