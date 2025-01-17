import logging
from boto3.session import Session

from shared.domain.cloud.ticket_classification import SortingService
from shared.domain.cloud.classification_exceptions import ClassificationException

logger = logging.getLogger(__name__)


class AWSRekognition(SortingService):
    """
    Amazon Recognition client handling ticket classification.
    """

    def __init__(self, aws_session: Session, model_arn: str):
        self.__rekognition_client = aws_session.client("rekognition")
        self.__model_arn = model_arn

    def detect_custom_labels(self,                         
                            bucket_name:str,
                            image_key: str,
                            min_confidence: float = 10,
                            max_results:int = 10,
                            )-> list[dict]:
        try:
            response = self.__rekognition_client.detect_custom_labels(
                ProjectVersionArn= self.__model_arn,
                Image = {
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name' : image_key
                    }
                },
                MinConfidence = min_confidence,
                MaxResults =  max_results
            )
            labels = [
                {"Name": label["Name"], "Confidence": label["Confidence"]}
                for label in response.get('CustomLabels',[0])
            ]
            logger.info(f'Detected {len(labels)} labels.')
            
            for label in labels:
                logger.debug(f"Label : {label['Name']}, Confidence: {label['Confidence']:.2f}%")
            
            return labels
        except self.__rekognition_client.exceptions.ClientError as e:
            logger.error("Error detecting custom labels in image.", exc_info=True)
            raise ClassificationException("Error during custom label detect.") from e
        

