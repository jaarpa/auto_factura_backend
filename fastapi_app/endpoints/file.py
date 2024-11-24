import logging
from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Form, HTTPException, UploadFile, status
from fastapi import File as FastAPIFile
from pydantic import BaseModel

from fastapi_app.endpoints import router
from modules.document_types.domain.entities.document_type import DocumentType
from modules.files.domain.entities.file import File
from shared.domain.cloud.storage import CloudStorage
from shared.domain.cloud.storage_exceptions import UploadingFileException
from shared.domain.repository import Repository
from shared.domain.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

class FileResponse(BaseModel):
    id: UUID
    name: str
    document_type_id: UUID
    model_config = {"from_attributes": True}

@router.put("/file/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def create_upload_file(
    file: Annotated[
        UploadFile, FastAPIFile(description="Multiple files as UploadFile")
    ],
    file_id: Annotated[UUID, Form()],
    document_type_name: Annotated[str, Form()],
    document_type_repository: Repository[DocumentType] = Depends(
        Provide["document_type_repository"]
    ),
    cloud_storage: CloudStorage = Depends(Provide["cloud_storage"]),
    unit_of_work: UnitOfWork = Depends(Provide["unit_of_work"]),
) -> FileResponse:
    """
    Receives files to create their corresponding entities and store
    them in the cloud.

    :return: created file entities that were actually stored and created
    """

    try:
        document_type = document_type_repository.get_by_fields(name=document_type_name)
        if not document_type:
            raise Exception
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
            document_type_id=document_type.id,
        )
        cloud_storage.put_file_data(file_entity, file.file)
        with unit_of_work as uow:
            uow.add(file_entity)
            uow.commit()
            file_response = FileResponse.model_validate(file_entity)
        return file_response
    except UploadingFileException as e:
        logger.error(f"Error uploading the file with config {file_config}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Error uploading your file"
        ) from e
