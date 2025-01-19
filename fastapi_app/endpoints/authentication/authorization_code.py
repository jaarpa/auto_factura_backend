import base64
import logging
from uuid import UUID

import httpx
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from fastapi_app.endpoints import router
from modules.accounts.domain.services.jwt_validator import JWTValidator

logger = logging.getLogger(__name__)


@router.get("/authorization_code")
@inject
async def cognito_login_callback(
    code: UUID = Query(description="Cognito authorization code"),
    jwt_validator: JWTValidator = Depends(Provide["jwt_validator"]),
    token_url: str = Depends(Provide["app_config.cognito.cognito_token_url"]),
    client_id: str = Depends(Provide["app_config.cognito.client_id"]),
    client_secret: str = Depends(Provide["app_config.cognito.client_secret"]),
    redirect_uri: str = Depends(Provide["app_config.cognito.redirect_uri"]),
):
    """
    Exchanges an authorization code provided by cognito login for id_token,
    access_token, and refresh_token. This endpoint is called on successful
    cognito login.

    More info on this flow here
    - https://www.oauth.com/oauth2-servers/server-side-apps/authorization-code/
    - https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
    """
    try:
        authorization = base64.b64encode(
            bytes(f"{client_id}:{client_secret}", "utf-8")
        ).decode("utf-8")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {authorization}",
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": str(code),
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data, headers=headers)
            response_data = response.json()

        if response.status_code != status.HTTP_200_OK:
            logger.warning(f"Failed to exchange token: {response_data}")
            raise HTTPException(
                status_code=response.status_code,
                detail=response_data.get("error", "Failed to get token"),
            )

        # Get the ID Token
        id_token = response_data.get("id_token")
        access_token = response_data.get("access_token")
        refresh_token = response_data.get("refresh_token")

        if not id_token or not access_token or not refresh_token:
            logger.error(f"Token not found in response {response_data}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ID token not found",
            )

        # Validate tokens
        await jwt_validator.decode_jwt(id_token, verify_aud=True)
        await jwt_validator.decode_jwt(access_token)

    except httpx.RequestError as e:
        logger.error(f"An error occurred while requesting tokens: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed token request",
        ) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(
        content={
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )
