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


# TODO: Refactor into a more generic Catalog response
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
    ticket = ticket_repository.get(ticket_id)

    if not ticket:
        logger.warning(f"Ticket with ID {ticket_id} not found.")
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No ticket with id {ticket_id}")

    logger.info(f"Authenticated user ID: {type(user['sub'])}")
    logger.info(f" Ticket owner ID: {type(ticket.user_id)}")

    if str(ticket.user_id) != user["sub"]:  # "sub" Contains the user ID in Cognito.
        logger.warning(f"User {user['sub']} tried to access ticket {ticket_id}.")
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="You do not have access to this ticket."
        )

    logger.info(f"User {user['sub']} accessed ticket {ticket_id} successfully")
    return TicketResponse.model_validate(ticket)
