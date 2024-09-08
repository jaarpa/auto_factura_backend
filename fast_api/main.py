import os
from uuid import UUID
from fastapi import FastAPI, File, UploadFile, HTTPException

# from fastapi import Body
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# import boto3
from dotenv import load_dotenv
# from botocore.exceptions import NoCredentialsError,ClientError
# import psycopg2
# from psycopg2 import sql
# from importlib import reload, import_module
from shared.infrastructure.alchemy_unit_of_work import AlchemyUnitOfWork
from shared.infrastructure.alchemy_repository import AlchemyRepository
from modules.files.domain.entities.file import File as FileEntity


app = FastAPI()
load_dotenv()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.post("/files/")
# async def create_file(file: bytes= File()):
#     return {"file_size": len(file)}

MAX_FILE_SIZE = 5 * 1048576

ALLOWED_FILE_TYPE = {"image/jpeg", "image/png", "image/jpg"}  # cuándo usar el set ...?

# @app.middleware("http")
# async def limit_file_size(request,call_next):

#     if request.headers.get("content-length"):
#         content_length = int(request.headers.get("content-length"))
#         if content_length > MAX_FILE_SIZE:
#             return JSONResponse(content={"error":"Archivo demasiado grande."},status_code=413)

#     return await call_next(request)

# # Isolated function to upload file to S3,
# def upload_file_s3(file_path: str,bucket_name: str,subfolder:str) -> str:
#     """
#     Upload file to a subfolder of an s3 bucket and save the key to a PostgreSQL

#     :param file_path: Local path of the file to upload.
#     :param bucket_name: S3 bucket name.
#     :param subfolder: subfolder to save the file.
#     :return: key of the file uploaded to S3.llklkll

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
#         if e.response['ERROR']['Code'] == '404':

#             try:
#                 # Uploadfile
#                 s3_client.upload_file(file_path, bucket_name,key)#

#                 # conexión a la base de datos de postgreSQL
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

# file_path = 'src/fast_api/prueba.jpg' #Used for testing
# bucket_name = 'rubenstocker26'
# subfolder = 'pruebas'


@app.post("/file/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_FILE_TYPE:
        raise HTTPException(
            status_code=404,
            detail=f"Tipo de archivo no permitido. Solo se admite {ALLOWED_FILE_TYPE}",
        )
    if not file.filename:
        raise HTTPException(
            status_code=404,
            detail="File is missing filename",
        )
    try:
        # contents = await file.read()
        # print(f"Archivo recivido: {file.filename}, tamaño: {len(contents)} bytes")
        file_location = f"/tmp/{file.filename}"
        # with open(file_location,'wb') as f:
        #     f.write(file.file.read())

        # Upload file to S3
        # upload_file_s3(file_location,bucket_name,subfolder)
        uploaded_ticket = FileEntity(
            name=file.filename,
            key=file_location,
            config={},
            document_type_id=UUID("a9e39cc9-1749-4da6-b271-cd71cd0481df"),
        )
        with AlchemyUnitOfWork() as uow:
            file_repository = AlchemyRepository[FileEntity](FileEntity, uow.session)
            file_repository.add(uploaded_ticket)
            uow.commit()

        return {"filename": file.filename}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something wrong") from e

    finally:
        # Delete temporaly file
        if os.path.exists(file_location):
            os.remove(file_location)
