from fastapi_app.endpoints import router
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import httpx
import os 
import json
import jwt
from jwt import PyJWKClient

logger = logging.getLogger(__name__)

cognito_domain = "https://autofactura.auth.us-east-1.amazoncognito.com"
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = "http://localhost:8000/callback"
jwks_url = "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_RSQXxoYER/.well-known/jwks.json"
region = "us-east-1"
user_pool_id = "us-east-1_RSQXxoYER"

@router.get("/callback")
async def callback(request: Request):
    # Authorization code
    authorization_code = request.query_params.get("code")
    if not authorization_code:
        return {"error": "Authorization code not found"}

    tokens = await exchange_code_for_tokens(authorization_code)

    # Obtener el ID token
    id_token = tokens.get("id_token")
    if not id_token:  # or not await validate_jwt(id_token):
        raise HTTPException(status_code=400, detail="ID token not found")

    # Validar el ID token
    decoded_token = await validate_jwt(id_token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid or expired ID token")

    return JSONResponse(
        content={
            "message": "Token validated successfully",
            "decoded_token": decoded_token,
        }
    )


async def exchange_code_for_tokens(code: str):
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


# Crear un cliente PyJWK para obtener la clave pública
jwks_client = PyJWKClient(jwks_url)


async def validate_jwt(token: str) -> dict:

    try:
        # Get the token header and find the corresponding key.
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Decode and validate token.
        decoded_token = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=client_id,
            issuer=f"https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}",
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Unexpected error during JWT validation:{e}")
        raise HTTPException(status_code=500, detail=str(e))
