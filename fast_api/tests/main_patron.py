import strategy
from context import InvoiceContext
from store_identifier import StoresIdentifier


def main():
    identifying = StoresIdentifier()
    bucket_name = 'custom-labels-console-us-east-1-f23390f701'
    ticket_image = 'test/walmart/2024-01-15_04-19-32-090.png'
    
    store_name = identifying.indetify_ticket(ticket_image,bucket_name)
    strategy = identifying.get_strategy(store_name)
    
    context = InvoiceContext(strategy)
    context.process_ticket(ticket_image,bucket_name)
    
    #Hasta aquí, el resultado obtenido es el siguiente.
    #{
    # "tr": "04344",
    # "tc": "355361503256050489142"
    # }
    #que corresponde a las consultas personalizadas para el caso de Walmart.


if __name__ == "__main__":
    main()



