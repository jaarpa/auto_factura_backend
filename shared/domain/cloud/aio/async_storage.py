from typing import BinaryIO
from typing import Protocol
from typing import runtime_checkable

from modules.files.domain.entities.file import File


@runtime_checkable
class AsyncCloudStorage(Protocol):
    """
    Represents the storage of files in a cloud provider service.
    """

    async def get_file_data(self, file: File) -> BinaryIO:
        """
        Given a File entity gets the contents of said file from the cloud
        storage.

        :param file: File to download.
        :return: In-memory file-like object with the actual file data.
        """

    async def put_file_data(self, file: File, data: BinaryIO) -> File:
        """
        Given a File instance and the bytes data of the file it uploads
        the file data to the cloud storage using the file entity configuration.
        """
