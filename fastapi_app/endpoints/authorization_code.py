
from fastapi_app.endpoints import router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import httpx
import os 
import json

logger = logging.getLogger(__name__)

cognito_domain = "https://autofactura.auth.us-east-1.amazoncognito.com"
client_id = "5g70h8hdc94pfll9vq42n7pons"
client_secret = "qcdjhu4u5ab7b5icraiidtt4hpfa6ps3sidecojsi1b4da8i3av"
redirect_uri = "http://localhost:8000/callback"

@router.get("/callback")
async def callback(request: Request):
    # Authorization code 
    authorization_code = request.query_params.get("code")
    if not authorization_code:
        return {"error": "Authorization code not found"}
    
    tokens = await exchange_code_for_tokens(authorization_code)
    
    return tokens

async def exchange_code_for_tokens(code:str):
    url = f"{cognito_domain}/oauth2/token"
    data = {
        "grant_type":"authorization_code",
        "client_id": client_id,
        "client_secret":client_secret,
        "code":code,
        "redirect_uri": redirect_uri
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic NWc3MGg4aGRjOTRwZmxsOXZxNDJuN3BvbnM6cWNkamh1NHU1YWI3YjVpY3JhaWlkdHQ0aHBmYTZwczNzaWRlY29qc2kxYjRkYThpM2F2"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            return {
                "id_token": response_data.get("id_token"),
                "access_token": response_data.get("access_token"),
                "refresh_token": response_data.get("refresh_token"),
                "expires_in": response_data.get("expires_in")
            }
        else:
            return {"error": response_data.get("error","Token exchange failed")}