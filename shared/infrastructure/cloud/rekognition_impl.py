import boto3
from typing import Any
from shared.domain.cloud.rekognition import RekognitionService

class RekognitionServiceImpl(RekognitionService):
    def __init__(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.client = boto3.client(
            "rekognition",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def analyze_image(self, bucket: str, key: str) -> Any:
        try:
            response = self.client.detect_labels(
                Image={"S3Object": {"Bucket": bucket, "Name": key}},
                MaxLabels=10,
                MinConfidence=75,
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Error processing image with Rekognition: {e}")