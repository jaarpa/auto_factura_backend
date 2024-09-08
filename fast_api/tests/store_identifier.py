import strategy
import boto3
from dotenv import load_dotenv
import os
load_dotenv()
import json
from store_information import store_strategy_map

class StoresIdentifier:  
    def __init__(self):
        self.store_strategy_map = store_strategy_map
        
    def indetify_ticket(self, ticket_name:str, bucket_name:str)-> str: 
        """
        Returns the ticket label (store name)
        
        :param ticket_image: image name.
        :param bucket_name: bucket name. 
        """
        #Toma las credenciales configuradas en el aquipo local... 
        rekognition_client = boto3.client('rekognition')
        model_arn = os.environ.get("model_arn")
        
        response = rekognition_client.detect_custom_labels(
            ProjectVersionArn = model_arn,
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name' : ticket_name
                }
            },
            MinConfidence=10,
            MaxResults=10
        )
        return response['CustomLabels'][0]['Name']
    
    def get_strategy(self,store_name):
        """
        Method for obtaining the strategy corresponding to the identified store.
        """
        strategy = store_strategy_map.get(store_name,None)['strategy']
        if strategy is None:
            raise ValueError(f"Strategy not found for {store_name} store")
        return strategy
    
    def get_id_adapter(self,store_name:str):
        """
        Method for obtaining the id adapter corresponding to the identified store.
        """
        id_adapter = store_strategy_map.get(store_name,None)['id_adapter']
        if id_adapter is None:
            raise ValueError(f"Strategy not found for {store_name} store")
        return id_adapter

    def get_store_config(self,store_name): 
        #Está función podría usarse en vez de tener 'get_strategy' y 'get_id_adapter' por separado.
        """
        Obtener la configuración específica de la tienda.
        """
    
        store_config = store_strategy_map.get(store_name)
        
        return store_config
    
    def process_expense(self,ticket_image:str ,bucket_name:str, qf: dict, store_name:str, version:str):
        """
        Method for custom queries with aws textract.
        
        :param ticket_image: image name.
        :param bucket_name: bucket name. 
        :param qf: QueriesConfig.
        :param store_name: store name.
        :param version: id adapter version.
        """
        client = boto3.client('textract')
        response = client.analyze_document(
            Document = {
                'S3Object' : {
                    'Bucket' : bucket_name,
                    'Name': ticket_image
                    
                }
            },
            FeatureTypes=['QUERIES'],
            QueriesConfig= qf,
            AdaptersConfig= {
                'Adapters':[
                    {
                        'AdapterId': self.get_id_adapter(store_name),
                        'Version': version
                    }       
                ]
            }
        )
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
        return result
    
#EL CÓDIGO SIGUIENTE LO USÉ PARA PROBAR DE MANERA AISLADA CADA PARTE, NO ES IMPORTANTE  
    
# test = StoresIdentifier()
# walmart_strategy = test.get_id_adapter("walmart")
# print(walmart_strategy)      
               
# walmart_config = test.store_strategy_map.get('walmart')
# print(walmart_config)

# test_adapter =  test.get_id_adapter('walmart')
# print(test_adapter)
# def main():
#     identifying = StoresIdentifier()
#     bucket_name = 'custom-labels-console-us-east-1-f23390f701'
#     ticket_name = 'test/walmart/2024-01-15_04-19-32-090.png'
#     prueba = identifying.indetify_ticket(ticket_name,bucket_name)
#     print(prueba)

# if __name__ == "__main__":
#     main()

