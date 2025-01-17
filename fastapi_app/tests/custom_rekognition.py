import boto3
import json 

session = boto3.Session(profile_name='autoinvoice-dev')
rekognition_client = session.client('rekognition', region_name='us-east-2')
model_arn = 'arn:aws:rekognition:us-east-2:600627332804:project/rek_autoinvoice_dev/version/rek_autoinvoice_dev.2025-01-15T12.43.05/1736966583873'

response = rekognition_client.detect_custom_labels(
    ProjectVersionArn=model_arn,
    Image={
        'S3Object': {
            'Bucket': 's3-dev-rekognition',
            'Name': 'test/walmart/IMG20240812214510.jpg'
        }
    },
    MinConfidence=10,  # Puedes ajustar el umbral de confianza mínimo
    MaxResults=10
)

for label in response['CustomLabels']:
    print(f"Etiqueta: {label['Name']}, Confianza: {label['Confidence']:.2f}%")

output_file = 'resultado_custom_rek.json'

# Guardar el resultado en un archivo JSON
with open(output_file, 'w') as file:
    json.dump(response, file, indent=4)