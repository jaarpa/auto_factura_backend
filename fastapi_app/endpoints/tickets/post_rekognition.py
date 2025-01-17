import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel

from fastapi_app.endpoints import router
from modules.tickets.domain.entities.ticket import Ticket
from shared.domain.repository import Repository
from shared.domain.cloud.storage import CloudStorage
from shared.domain.cloud.ticket_classification import SortingService

logger = logging.getLogger(__name__)


class RekognitionResponse(BaseModel):
    ticket_id: UUID
    results: dict
    model_config = {"from_attributes": True}


@router.post("/rekognition/{ticket_id}/classify/")
@inject
async def classify_ticket(
    ticket_id: UUID,
    request: Request,
    ticket_repository: Repository[Ticket] = Depends(Provide["ticket_repository"]),
    sorting_service: SortingService = Depends(Provide["ticket_sorting_service"]),
):
    """
    Processes an image stored in S3 with Amazon Rekognition.
    Authentication:
    - Requires a valid JWT access token.

    :param file_id: UUID of the file to analyze.
    :return: Results from Amazon Rekognition.
    """
    user = getattr(request.state, "user", None)
    if not user:
        logger.error("User information not found in request state.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User information not found in request state",
        )
    user_id = UUID(user["sub"])

    ticket = ticket_repository.get_by_fields(user_id=user_id, id=ticket_id)
    
    if not ticket:
        logger.warning(f'Ticket with ID {ticket_id} not fount or access denied for user {user_id}')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ticket not found or access denied. ")
    
    try:
        result = sorting_service.detect_custom_labels(
            bucket_name = 's3-dev-rekognition',
            image_key = 'test/walmart/IMG20240812214510.jpg'
        )
        return {"ticket_id": str(ticket_id), "classification":result}
    
    except Exception as e:
        logger.error(f"Error classifying ticket: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )
