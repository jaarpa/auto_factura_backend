from typing import Union
from fastapi import FastAPI, Body, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel 

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/files/")
async def create_file(file: bytes= File()):
    return {"file_size": len(file)}

MAX_FILE_SIZE = 5 * 1048576

ALLOWED_FILE_TYPE = {"image/jpeg", "image/png", "image/jpg"} # cuándo usar el set ...?

@app.middleware("http")
async def limit_file_size(request,call_next):
    
    if request.headers.get("content-length"):
        content_length = int(request.headers.get("content-length"))
        if content_length > MAX_FILE_SIZE:
            return JSONResponse(content={"error":"Archivo demasiado grande."},status_code=413)
    
    return await call_next(request)

@app.post("/uploadfile/")
async def create_upload_file(file:UploadFile = File(...)):
    if file.content_type not in ALLOWED_FILE_TYPE:
        raise HTTPException(status_code=400, detail= "Tipo de archivo no permitido. Solo se admite JPEG")
    
    contents = await file.read()
    print(f"Archivo recivido: {file.filename}, tamaño: {len(contents)} bytes")
    
    return {"filename": file.filename}
