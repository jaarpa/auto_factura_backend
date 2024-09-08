from strategy import InvoiceStrategy

class InvoiceContext:
    
    def __init__(self, strategy: InvoiceStrategy):
        self._strategy =  strategy
        
    def set_strategy(self, strategy: InvoiceStrategy):
        self._strategy = strategy
        
    def process_ticket(self,ticket_image,bucket_name):
        self._strategy.process_ticket(ticket_image,bucket_name)
        
