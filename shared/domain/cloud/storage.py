from typing import BinaryIO, Protocol, runtime_checkable
from uuid import UUID

from modules.files.domain.entities.file import File


@runtime_checkable
class CloudStorage(Protocol):
    """
    Represents the storage of files in a cloud provider service.
    """

    def get_file_data(self, file: File) -> BinaryIO:
        """
        Given a File entity gets the contents of said file from the cloud
        storage.

        :param file: File to download.
        :return: In-memory file-like object with the actual file data.
        """

    def put_file_data(self, file: File, data: BinaryIO) -> File:
        """
        Given a File instance and the bytes data of the file it uploads
        the file data to the cloud storage using the file entity configuration.

        :raises UploadingFileException: If the file couldn't be uploaded.
        """

    def get_file_key(self, file_id: UUID, filename: str, document_type: str) -> str:
        """
        Creates the unique key identifier for a file with the cloud provider

        :param file_id: File identifier in our db
        :param filename: Human readable file name
        :param document_type: Document type (e.g. ticket, invoice, etc)
        :return: Unique cloud identifier
        """

    def get_file_config(
        self, file_id: UUID, filename: str, document_type: str
    ) -> dict[str, str]:
        """
        Creates the file configuration used to manage the file with
        the cloud provider

        :param file_id: File identifier in our db
        :param filename: Human readable file name
        :param document_type: Document type (e.g. ticket, invoice, etc)
        :return: Dictionary with the file configuration
        """
