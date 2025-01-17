from typing import Protocol, runtime_checkable


@runtime_checkable
class SortingService(Protocol):
    """
    Represents the classification of tickets with some independent service.
    """

    def detect_custom_labels(
        self,
        bucket_name: str,
        image_key: str,
        min_confidence: float = 10,
        max_result: int = 10,
    ) -> list[dict]:
        """
        Process an image stored in S3 using a custom model.
        Identifies the issuer of the ticket, for example; Walmart, Liverpool, Gas station, among others.

        :param bucket_name: Name of the S3 bucket where the image is located.
        :param image_key: Key of the file in the bucket.
        :param min_confidence: Minimum confidence level for the labels(default:10).
        :param max_results: Maximum number of labels to return (default:10)
        :return: A list of detected labels with their confidence levels. The ticket issuer. 
        """
        pass
