from abc import ABC, abstractmethod
from typing import Any


class RekognitionService(ABC):
    @abstractmethod
    def analyze_image(self, bucket: str, key: str) -> Any:
        """
        Process an image stored in S3 using AWS Rekognition.

        :param bucket: Name of the S3 bucket where the image is located.
        :param key: Key of the file in the bucket.
        :return: Result of analysis performed by AWS Rekognition.
        """
        pass