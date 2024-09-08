from abc import ABC, abstractmethod
# from store_identifier import StoresIdentifier
class InvoiceStrategy(ABC):
    @abstractmethod
    def process_ticket(self,ticket_image,bucket_name):
        pass
   
#Strategy for Walamart
class WalmartStrategy(InvoiceStrategy):
    #Lógica para solicitar factura de walmart    
    def process_ticket(self,ticket_image: str, bucket_name:str):
        from store_identifier import StoresIdentifier
        store_identifier = StoresIdentifier()    
        queries_config = {
            'Queries':[
                {
                    'Text': 'what is the tr number?',
                    'Alias': 'tr'
                },
                {
                    'Text': 'what is the tc number?',
                    'Alias': 'tc'
                }
            ]
        }
        
        store_identifier.process_expense(
            ticket_image=ticket_image,
            bucket_name=bucket_name,
            qf=queries_config,
            store_name='walmart',
            version='1'    
        )
        
    
#Strategy for OXXO
class OxxoStrategy(InvoiceStrategy):
    def process_ticket(self,ticket_image,bucket_name):
       print("solicitando factura de oxxo")

class LiverpoolStrategy(InvoiceStrategy):
    
    
    def process_ticket(self,ticket_image,bucket_name):
        print("Solicitando factura de Liverpool")