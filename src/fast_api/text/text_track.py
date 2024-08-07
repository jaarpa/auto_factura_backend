import boto3
from dotenv import load_dotenv
import os 
load_dotenv()

textrack = boto3.client('textract',
                        aws_access_key_id= os.getenv('aws_access_key_id'),
                        aws_secret_access_key=os.getenv('aws_secret_access_key'),
                        region_name=os.getenv('aws_region_name'))

bucket_name = 's3customlabels'
document_name = 'rgg1_the_home_depot.jpeg'

def analyze_document(bucket_name,document_name):
    response = textrack.analyze_document(
        Document = {'S3Object':{'Bucket': bucket_name, 'Name': document_name}},
        FeatureTypes = ['TABLES','FORMS']
    )
    return response

response = analyze_document(bucket_name,document_name)

print(response)