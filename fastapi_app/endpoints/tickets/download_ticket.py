import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from fastapi_app.endpoints import router
from modules.files.domain.entities.file import File
from modules.tickets.domain.entities.ticket import Ticket
from shared.domain.cloud.storage import CloudStorage
from shared.domain.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

@router.get("/tickets/{ticket_id}/download/")
@inject
async def download_file(
    ticket_id: UUID,
    request: Request,
    cloud_storage: CloudStorage = Depends(Provide["cloud_storage"]),
    unit_of_work: UnitOfWork = Depends(Provide["unit_of_work"]),
):
    """
    Endpoint to download the file associated with a specific ticket.
    Authentication:
    - Requires a valid JWT access token.

    :param ticket_id: ID of the ticket to retrieve the associated file.
    :return: StreamingResponse with the file content.
    """
    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    user_id = UUID(user["sub"])

    try:
        with unit_of_work as uow:
            # Retrieve the ticket entity
            ticket_repository = uow.get_repository(Ticket)
            ticket = ticket_repository.get(ticket_id) 
            if not ticket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ticket not found"
                )

            # Retrieve the associated file entity
            file_repository = uow.get_repository(File)
            file_entity = file_repository.get(ticket.file_id)
            if not file_entity:
                logger.error(f"Ticket not found for ID: {ticket_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No file associated with ticket{ticket_id}"
                )
            #Validate that the ticket belongs to the authenticated user
            if ticket.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this ticket.",
                )

            # Download the file using cloud storage
            
            file_data = cloud_storage.get_file_data(file_entity)
            if not file_data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve the file from cloud storage.",
                )
            file_data.seek(0)  # Reset file pointer in memory
            
            # Return the file as a streaming response
            return StreamingResponse(
                file_data,
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{file_entity.name}"'
                },
            )
    except Exception as e:
        logger.error(f"Error downloading file for ticket {ticket_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )