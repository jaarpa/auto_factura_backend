from typing import Protocol, runtime_checkable


@runtime_checkable
class RekognitionService(Protocol):
    """_summary_
    Represents the image analysis service in AWS Rekognition.
    """

    def analyze_image(
        self,
        bucket: str,
        image_key: str,
        model_arn: str,
    ) -> dict:
        """
        Process an image stored in S3 using a custom model.
        Identifies the issuer of the ticket, for example; Walmart, Liverpool, Gas station, among others.
        
        :param bucket: Name of the S3 bucket where the image is located.
        :param image_key: Key of the file in the bucket.
        :param model_arn: ARN of the custom model to use.
        :return: the issuer of the ticket and more information.
        """
        pass
