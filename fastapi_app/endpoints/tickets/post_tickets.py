import logging
from typing import Annotated
from uuid import UUID, uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, UploadFile, status, Request
from fastapi import File as FastAPIFile
from pydantic import BaseModel

from fastapi_app.endpoints import router
from modules.accounts.domain.entities.user import User
from modules.document_types.domain.constants import (
    TICKET_DOCUMENT_TYPE_ID,
    TICKET_DOCUMENT_TYPE_NAME,
)
from modules.files.domain.entities.file import File
from modules.tickets.domain.entities.ticket import Ticket
from shared.domain.cloud.storage import CloudStorage
from shared.domain.cloud.storage_exceptions import FileUploadException
from shared.domain.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

# TODO: Refactor to return also the file data.
class NewTicketResponse(BaseModel):
    id: UUID
    file_id: UUID
    data: dict
    model_config = {"from_attributes": True}


# TODO: This issuer should be later set by the results from rekognition
@router.post("/tickets/")
@inject
async def create_upload_file(
    request: Request,
    files: Annotated[
        list[UploadFile], FastAPIFile(description="Tickets to start processing")
    ],
    cloud_storage: CloudStorage = Depends(Provide["cloud_storage"]),
    unit_of_work: UnitOfWork = Depends(Provide["unit_of_work"]),
) -> list[NewTicketResponse]:
    """
    Receives files to create their corresponding entities and store
    them in the cloud.
    Authentication:
    - Requires a valid JWT access token.

    :return: created file entities that were actually stored and created
    """

    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Unauthorized")
    user_id = UUID(user["sub"])
    #user_id = UUID("a4183418-90a1-704e-2f13-402c62ce811f")
    try:
        tickets_response = list()
        with unit_of_work as uow:
            user_repository = uow.get_repository(User)
            user = user_repository.get(user_id)
            if not user:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED)

            ticket_type_id = TICKET_DOCUMENT_TYPE_ID
            document_type_name = TICKET_DOCUMENT_TYPE_NAME

            for file in files:
                file_id = uuid4()
                filename = file.filename or str(file_id)
                file_config = cloud_storage.get_file_config(
                    file_id, filename, document_type_name
                )
                file_key = file_config["key"]
                file_entity = File(
                    id=file_id,
                    name=filename,
                    key=file_key,
                    config=file_config,
                    document_type_id=ticket_type_id,
                )
                ticket_entity = Ticket(
                    id=file_id,
                    user_id=user_id,
                    file_id=file_entity.id,
                )
                ticket_entity.file = file_entity
                cloud_storage.put_file_data(file_entity, file.file)
                uow.add(ticket_entity)
                tickets_response.append(NewTicketResponse.model_validate(ticket_entity))
            uow.commit()
        return tickets_response
    except FileUploadException as e:
        logger.error(f"Error uploading the file with config {file_config}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Error uploading your file"
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
        ) from e
