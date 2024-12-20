from typing import Any

from boto3.session import Session

from shared.domain.cloud.rekognition import RekognitionService


class RekognitionServiceImpl(RekognitionService):
    """_summary_
    Amazon Recognition client
    """
    def __init__(self, aws_session:Session, model_arn:str):
        self.__rekognition_client = aws_session.client("rekognition")
        self.__model_arn = model_arn

    def analyze_image(self, bucket, image_key, model_arn):
        return super().analyze_image(bucket, image_key, model_arn)