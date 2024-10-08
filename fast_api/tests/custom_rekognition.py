import boto3
import json 

rekognition_client = boto3.client('rekognition')
model_arn = 'arn:aws:rekognition:us-east-1:767398010748:project/ticket_classification/version/ticket_classification.2024-08-19T20.15.30/1724120129902'

response = rekognition_client.detect_custom_labels(
    ProjectVersionArn=model_arn,
    Image={
        'S3Object': {
            'Bucket': 'custom-labels-console-us-east-1-f23390f701',
            'Name': 'test/coppel/Alfonso Ikayka Martínez Aragón pgg1_Coppel - Alfonso Ikayka Martinez Aragón.jpeg'
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