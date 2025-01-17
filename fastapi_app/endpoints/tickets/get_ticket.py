import datetime
import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel

from fastapi_app.endpoints import router
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


@router.get("/ticket/{ticket_id}/")
@inject
async def get_file_info(
    ticket_id: UUID,
    request: Request,
    ticket_repository: Repository[Ticket] = Depends(Provide["ticket_repository"]),
) -> TicketResponse:
    user = getattr(request.state, "user", None)
    if not user:
        logger.error("User information not found in request state.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User information not found in request state",
        )
    
    user_id = UUID(user["sub"])
    
    #Search for the ticket with the user_id and ticket_id
    ticket = ticket_repository.get_by_fields(user_id=user_id, id= ticket_id) 
    
    if not ticket:
        logger.warning(f'Ticket with ID {ticket_id} not fount or access denied for user {user_id}')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ticket not found or access denied. ")

    logger.info(f"User {user['sub']} accessed ticket {ticket_id} successfully")
    return TicketResponse.model_validate(ticket)
