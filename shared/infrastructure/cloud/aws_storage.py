import logging
from io import BytesIO
from typing import BinaryIO
from uuid import UUID

from boto3.session import Session

from modules.files.domain.entities.file import File
from shared.domain.cloud.storage import CloudStorage
from shared.domain.cloud.storage_exceptions import FileUploadException

logger = logging.getLogger(__name__)

class AWSS3(CloudStorage):
    """
    Amazon S3 client for handling files.
    """

    def __init__(self, aws_session: Session, default_bucket: str):
        self.__s3_client = aws_session.client("s3")
        self.__default_bucket = default_bucket

    def get_file_data(self, file: File) -> BinaryIO:
        """
        Given a File entity gets the contents of said file from the cloud
        storage.

        :param file: File to download.
        :return: In-memory file-like object with the actual file data.
        """
        file_data = BytesIO()
        bucket_name = file.config.get("aws", {}).get("bucket_name")
        key = file.key
        self.__s3_client.download_fileobj(bucket_name, key, file_data)
        return file_data

    def put_file_data(
        self, file: File, data: BinaryIO, bucket: str | None = None, **kwargs
    ):
        """
        Given a File instance and the bytes data of the file it uploads
        the file data to the cloud storage using the file entity configuration.
        """
        bucket_name = bucket or self.__default_bucket
        try:
            logger.info(
                f"Uploading object with key={file.key} to {bucket_name=} and kwargs={kwargs}"
            )
            self.__s3_client.upload_fileobj(data, bucket_name, file.key, kwargs)
        except self.__s3_client.exceptions.ClientError as e:
            raise FileUploadException from e

    def get_file_key(self, file_id: UUID, filename: str, document_type: str) -> str:
        return f"{document_type}/{file_id}_{filename}"

    def get_file_config(
        self,
        file_id: UUID,
        filename: str,
        document_type: str,
        bucket_name: str | None = None,
    ) -> dict[str, str]:
        bucket = bucket_name or self.__default_bucket
        file_config = {
            "provider": "s3",
            "bucket": bucket,
            "key": self.get_file_key(file_id, filename, document_type),
        }
        return file_config
