import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from fastapi_app.endpoints import router
from modules.tickets.domain.entities.ticket import Ticket
from shared.domain.cloud.storage import CloudStorage
from shared.domain.repository import Repository

logger = logging.getLogger(__name__)

@router.get("/tickets/{ticket_id}/download/")
@inject
async def download_file(
    ticket_id: UUID,
    request: Request,
    cloud_storage: CloudStorage = Depends(Provide["cloud_storage"]),
    ticket_repository: Repository[Ticket] = Depends(Provide["ticket_repository"]),
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
        ticket = ticket_repository.get_by_fields(user_id=user_id, id=ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        
        # Download the file using cloud storage
        
        file_data = cloud_storage.get_file_data(ticket.file)
        
        file_data.seek(0)  # Reset file pointer in memory
        
        # Return the file as a streaming response
        return StreamingResponse(
            file_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{ticket.file.name}"'
            },
        )
    except Exception as e:
        logger.error(f"Error downloading file for ticket {ticket_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )