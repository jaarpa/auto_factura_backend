import datetime
import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from fastapi_app.endpoints import router
from fastapi_app.middlewares.authorization import get_current_user_id
from modules.tickets.domain.entities.ticket import Ticket
from shared.domain.repository import Repository

logger = logging.getLogger(__name__)


class CatalogResponse(BaseModel):
    id: UUID
    label: str
    name: str
    model_config = {"from_attributes": True}


class FileResponse(BaseModel):
    id: UUID
    name: str
    document_type: CatalogResponse
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


class TicketResponse(BaseModel):
    id: UUID
    file: FileResponse
    issuer: CatalogResponse | None
    data: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


@router.get("/ticket/{ticket_id}/", response_model=TicketResponse)
@inject
async def get_file_info(
    ticket_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    ticket_repository: Repository[Ticket] = Depends(Provide["ticket_repository"]),
) -> Ticket:
    """
    Retrieves information on the ticket with the specified `ticket_id`
    only returns the information if the logged in user is the owner of
    the ticket.
    """
    #Search for the ticket with the user_id and ticket_id
    ticket = ticket_repository.get_by_fields(user_id=user_id, id=ticket_id)

    if not ticket:
        logger.warning(f'Ticket with ID {ticket_id} not fount or access denied for user {user_id}')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ticket not found.")

    logger.debug(f"User {user_id} accessed ticket {ticket_id} successfully")
    return ticket
