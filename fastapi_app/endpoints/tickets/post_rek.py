import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Depends, status, Request
from pydantic import BaseModel

from fastapi_app.endpoints import router
from shared.domain.cloud.storage import CloudStorage
from shared.domain.cloud.rekognition import RekognitionService
from shared.domain.unit_of_work import UnitOfWork
from modules.tickets.domain.entities.ticket import Ticket

logger = logging.getLogger(__name__)

class RekognitionResponse(BaseModel):
    ticket_id: UUID
    results: dict  
    model_config = {"from_attributes": True}
    
@router.post("/rekognition/analyze/")
@inject
async def analyze_image(
    ticket_id: UUID,
    request: Request,
    unit_of_work: UnitOfWork = Depends(Provide["unit_of_work"]),
    cloud_storage: CloudStorage = Depends(Provide["cloud_storage"]),
    rekognition_service: RekognitionService = Depends(Provide["rekognition_client"]),
    ) -> RekognitionResponse:
    """
    Processes an image stored in S3 with Amazon Rekognition.
    Authentication:
    - Requires a valid JWT access token.

    :param file_id: UUID of the file to analyze
    :return: Results from Amazon Rekognition
    """
    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    user_id = UUID(user["sub"])
    
    try: 
        with unit_of_work as uow:
            # Recover file entity
            ticket_repository = uow.get_repository(Ticket)
            ticket_entity =  ticket_repository.get(ticket_id)
            if not ticket_entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
                )
            
            #Get S3 file key
            file_key = file_entity.key
            bucket_name = file_entity.config["bucket"]
            
            # Call amazon Rekognition
            rekognition_result = rekognition_service.analyze_image(bucket_name, file_key)
            #Build the response
            labels = [
                {"Name": label["Name"], "Confidence": label["Confidence"]}
                for label in rekognition_result.get("Labels", [])
            ]
           
            return RekognitionResponse(labels=labels)
        
    except Exception as e:
        logger.error(f"Error processing image {file_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing the image",
        ) from e