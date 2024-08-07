import psycopg2 
from psycopg2 import sql
import boto3 
import os 

subfolder = 'pruebas'
file_path = 'ruta/local/al/archivo/tuarchivo.jpg'
file_name = 'archivo.jpg'
s3_key = f'{subfolder}/{file_name}'
print(s3_key)
try:
    # conexión a la base de datos de postgreSQL
    conn = psycopg2.connect(
        dbname = "db_receip",
        user = "gubene",
        password = "260316@",
        host = "localhost",
        port = "5432"
    )
    # cursor para ejecutar consultas
    cur = conn.cursor()
    # Consulta SQL para insertar el valor generado en la tabla
    insert_query = sql.SQL("INSERT INTO t_receipt (key_S3) VALUES (%s)")
    
    cur.execute(insert_query,[s3_key])
    conn.commit()
    print("SUCCESSFULY PROCESS")
finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()

