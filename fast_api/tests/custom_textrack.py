#Request custom queries to texttrack
import boto3
import json
#f781b57d74d0
# Crear cliente de Textract

# queries_config = {
#     'Queries':[
#         {
#             'Text': 'what is the tr number?',
#             'Alias': 'tr'
#         },
#         {
#             'Text': 'what is the tc number?',
#             'Alias': 'tc'
#         }
#     ]
# }

def process_expense(bucket,document):
    print("la vaxa ñpca")
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': document
                # 'Version': '1'
            }
        },
        FeatureTypes=[
            'QUERIES'
        ],
        # QueriesConfig = queries_config,
        QueriesConfig={
            'Queries':  [
        {
            'Text': 'what is the tr number?',
            'Alias': 'tr'
        },
        {
            'Text': 'what is the tc number?',
            'Alias': 'tc'
        }
        ]
        },
        AdaptersConfig={
            'Adapters': [
                {
                    'AdapterId': 'f781b57d74d0',
                    'Version': '1'
                },
            ]
        }
    )

    # Procesar la respuesta
    # Crear un diccionario para almacenar los resultados
    result = {}
    # FALTA VERIFICAR QUE FUNCIONE PARA TODOS LOS ADAPTADORES.
    # Iterar sobre los bloques
    for block in response['Blocks']:
        block_type = block.get('BlockType')
        
        # Si el bloque es del tipo QUERY_RESULT, buscamos su ID para emparejarlo con su QUERY
        if block_type == "QUERY_RESULT":
            text = block.get('Text')
            query_id = block.get('Id')
            
            # Buscar el bloque QUERY correspondiente
            for query_block in response['Blocks']:
                if query_block.get('BlockType') == "QUERY":
                    relationships = query_block.get('Relationships', [])
                
                    for relation in relationships:
                        if query_id in relation.get('Ids', []):
                            alias = query_block.get('Query', {}).get('Alias')
                            result[alias] = text

    # # Imprimir el resultado final
    print(json.dumps(result, indent=4))
    #SOLO FALTA AGREAR EL APARTADO PARA LA GENERACIÓN DEL ARCHIVO JSON
    # with open('resultado_textract_FINAL.json', 'w') as json_file:
    #     json.dump(result, json_file, indent=4)
    # print(data['Blocks'][1]['Relationships'][0]['Ids'])
        
    # # Guardar el resultado en un archivo JSON
    # RESULTADO OBTENIDO DE TEXTRACK
    # with open('resultado_textract.json', 'w') as json_file:
    #     json.dump(response, json_file, indent=4)

def main():
    # session = boto3.Session(profile_name='default')
    # s3_connection = session.resource('s3')
    # client = session.client('textract', region_name='us-east-1')
    bucket = 'custom-labels-console-us-east-1-f23390f701'
    document = 'train/walmart/2024-01-15_04-19-32-090.png'
    process_expense(bucket,document)
    
if __name__ == "__main__":
    main()