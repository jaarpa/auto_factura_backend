from fastapi_app.endpoints import router
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import httpx
import json
import jwt
from fastapi import Depends
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from modules.accounts.domain.service.interface_jwt_validator import JWTValidator
from containers.containers import Container

logger = logging.getLogger(__name__)


@router.get("/callback")
@inject
async def callback(
    request: Request,
    jwt_validator: JWTValidator = Depends(Provide["jwt_validator"]),
    cognito_domain: str = Depends(Provide["app_config.cognito.cognito_domain"]),
    client_id: str = Depends(Provide["app_config.cognito.client_id"]),
    client_secret: str = Depends(Provide["app_config.cognito.client_secret"]),
    redirect_uri: str = Depends(Provide["app_config.cognito.redirect_uri"]),
    authorization: str = Depends(Provide["app_config.cognito.authorization"]),
):
    # param authorization is different from the Authorization Code, thi is for the header
    # of the token exchange request.

    # Authorization code
    authorization_code = request.query_params.get("code")
    if not authorization_code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    # Exchange the authorization code for the JSON Web Keys.
    url = f"{cognito_domain}/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {authorization}",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response_data = response.json()

        if response.status_code != 200:
            logger.error(f"Failed to exchange token: {response_data}")
            raise HTTPException(
                status_code=response.status_code,
                detail=response_data.get("error", "Token exchange failed"),
            )

        # Get the ID Token
        id_token = response_data.get("id_token")

        if not id_token:
            logger.error("ID token not found in response")
            raise HTTPException(status_code=400, detail="ID token not found")

        # Validate tokens
        decoded_token = await jwt_validator.validate_jwt(id_token)

    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting tokens: {exc}")
        raise HTTPException(
            status_code=500, detail="Failed to exchange token due to network error"
        )

    return JSONResponse(
        content={
            "message": "Token validated successfully",
            "decoded_token": decoded_token,
        }
    )