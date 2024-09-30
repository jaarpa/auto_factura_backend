from typing import BinaryIO
from io import BytesIO

from boto3.session import Session

from shared.domain.cloud.storage import CloudStorage
from modules.files.domain.entities.file import File


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
        self.__s3_client.upload_fileobj(data, bucket_name, file.key, kwargs)
