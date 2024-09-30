# import boto3
# from dotenv import load_dotenv
# import os
# from botocore.exceptions import NoCredentialsError, ClientError
# import psycopg2
# from psycopg2 import sql
# from fastapi import FastAPI, File, UploadFile, HTTPException

# load_dotenv()

# file_path = 'src/fastapi_app/img3.jpg'
# bucket_name = 'rubenstocker26'
# subfolder = 'pruebas'

# def upload_file_s3(file_path: str,bucket_name: str,subfolder:str) -> str:
#     """
#     Upload file to a subfolder of an s3 bucket and save the key to a PostgreSQL

#     :param file_path: Local path of the file to upload.
#     :param bucket_name: S3 bucket name.
#     :param subfolder: subfolder to save the file.
#     :return: key of the file uploaded to S3.

#     """
#     s3_client = boto3.client(
#             's3',
#             aws_access_key_id = os.environ.get('aws_access_key_id'),
#             aws_secret_access_key = os.environ.get('aws_secret_access_key'),
#             region_name = os.environ.get('aws_region_name'),
#             )

#     file_name = file_path.split('/')[-1]
#     key = f"{subfolder}/{file_name}" # for the "head_object" method key is equal to object_name

#     try:
#         s3_client.head_object(Bucket=bucket_name, Key=key)
#         print(f'The {file_name} file is already exists in the {bucket_name} bucket')
#         return False
#     except ClientError as e:
#         error_code = e.response['Error']['Code']
#         if error_code == '404':

#             try:
#                 # Uploadfile
#                 s3_client.upload_file(file_path, bucket_name,key)#

#                 # conexión a la base de datos de postgreSQL
#                 ##CONVERTIR A VARIABLES DE ENTORNO EN CASO DE SER NECESARIO.
#                 conn = psycopg2.connect(
#                 dbname = "db_receip",
#                 user = "gubene",
#                 password = "260316@",
#                 host = "localhost",
#                 port = "5432"
#                 )
#                 # cursor para ejecutar consultas
#                 cur = conn.cursor()
#                 # Consulta SQL para insertar el valor generado en la tabla
#                 insert_query = sql.SQL("INSERT INTO t_receipt (key_S3) VALUES (%s)")
#                 cur.execute(insert_query,[key])
#                 conn.commit()
#                 print(f"FILE RECEIVED AND KEY SAVED IN THE DATABASE")

#             except FileNotFoundError:
#                 print(f"FILE NOT FOUND")
#             except  NoCredentialsError:
#                 print(f"CREDENTIALS WERE NOT FOUND")
#             finally:
#                 # Cerrar el cursor y la conexión
#                 cur.close()
#                 conn.close()

#         else:
#             print(f'ERROR VERIFYING THE EXISTENCE OF THE FILE')
#             return False


# file = upload_file_s3(file_path,bucket_name,subfolder)
