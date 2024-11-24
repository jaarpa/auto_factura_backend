import boto3
from dotenv import load_dotenv
import os 
load_dotenv()

sqs = boto3.client('sqs',
                   aws_access_key_id= os.getenv('aws_access_key_id'),
                   aws_secret_access_key=os.getenv('aws_secret_access_key'),
                   region_name=os.getenv('aws_region_name'))

sqs_queue_url=os.getenv('sqs_queue_url')

message = 'Hola sqs'

def send_message_sqs(message_body:str):
    try:
        response = sqs.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody= message
        )
        print('mensaje enviado a la cola')
    except Exception as e:
        raise e


##### REKOGNITION ######


image_path = "src/fastapi_app/img3.jpg"

def image_rekognition(image_path):
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
        print('pruebas')
        #print(type(image_bytes))
    rekognition_client = boto3.client('rekognition',
                   aws_access_key_id= os.getenv('aws_access_key_id'),
                   aws_secret_access_key=os.getenv('aws_secret_access_key'),
                   region_name=os.getenv('aws_region_name'))
    
    response = rekognition_client.detect_text(Image={'Bytes':image_bytes})
    print('Submitted image')
    print('--------------------')
    for text_detection in response['TextDetections']:
        print(f'Detected text: {text_detection["DetectedText"]}')
        print(f'Confidence: {text_detection["Confidence"]}%')
        print(f'Type: {text_detection["Type"]}')
# prueba = send_message_sqs(message)

prueba_rk = image_rekognition(image_path)

###CREEA ARCHIVO JSON CON LAS ETIQUETAS CORRESPONDIENTES
# list_response = s3_client.list_objects_v2(Bucket=bucket_name)
# results = []
# for obj in response.get('Contents',[]):
#     image_name = obj['Key']
#     # results.append(image_name)

#     rek_response = detect_labels(image_name)

#     image_result = {
#         'Image' : image_name,
#         'Labels' : []
#     }

#     for label in rek_response['Labels']:
#         image_result['Labels'].append({
#             'Name': label['Name'],
#             'Confidence' :label['Confidence']
#         })

#     results.append(image_result)

# json_data = {
#     'results': results
# }

# s3_client.put_object(
#     Bucket = 'rubenstocker26',
#     Key = 'resultado_final.json',
#     Body = json.dumps(json_data, indent=4),
#     ContentType = 'application/json'
#     )
# # print('proceso exitoso')
