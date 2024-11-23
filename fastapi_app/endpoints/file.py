import logging
from collections import defaultdict
from typing import Annotated
from uuid import UUID, uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, UploadFile
from fastapi import File as FastAPIFile

from fastapi_app.endpoints import router
from modules.files.domain.entities.file import File
from shared.domain.cloud.storage import CloudStorage
from shared.domain.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


# TODO: Fix this endpoint
@router.post("/file/")
@inject
async def create_upload_file(
    files: Annotated[
        list[UploadFile], FastAPIFile(description="Multiple files as UploadFile")
    ],
    cloud_storage: CloudStorage = Depends(Provide["cloud_storage"]),
    unit_of_work: UnitOfWork = Depends(Provide["unit_of_work"]),
) -> dict[str, list[File]]:
    """
    Receives files to create their corresponding entities and store
    them in the cloud.

    :return: created file entities that were actually stored and created
    """

    file_entities = defaultdict(list)
    ticket_type_id = UUID("a9e39cc9-1749-4da6-b271-cd71cd0481df")
    try:
        with unit_of_work as uow:
            for file in files:
                file_id = uuid4()
                filename = file.filename or str(file_id)
                file_key = f"{ticket_type_id}/{file_id}_{filename}"
                file_config = {
                    "provider": "s3",
                    "bucket": "autofactura",
                    "key": file_key,
                }
                file_entity = File(
                    id=file_id,
                    name=filename,
                    key=file_key,
                    config=file_config,
                    document_type_id=ticket_type_id,
                )
                try:
                    logger.info(f"The file {filename} will have the id {file_id}")
                    cloud_storage.put_file_data(file_entity, file.file)
                    uow.add(file_entity)
                    file_entities["uploaded"].append(file_entity)
                except Exception:
                    file_entities["failed"].append(file_entity)
                    logger.exception("Uploading file error")
            uow.commit()
    except Exception as e:
        logger.error(f"{e}")
    return file_entities
