import base64
import logging
from typing import Annotated

import httpx
from dependency_injector.wiring import Provide, inject
from fastapi import Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from fastapi_app.endpoints import router
from modules.authorization.domain.services.jwt_validator import JWTValidator

logger = logging.getLogger(__name__)


class RefreshToken(BaseModel):
    refresh_token: str


@router.post("/refresh")
@inject
async def refresh_access_tokens(
    refresh_token: Annotated[
        str,
        Body(description="Refresh token from previous authentication", embed=True),
    ],
    jwt_validator: JWTValidator = Depends(Provide["jwt_validator"]),
    token_url: str = Depends(Provide["app_config.cognito.token_url"]),
    client_id: str = Depends(Provide["app_config.cognito.client_id"]),
    client_secret: str = Depends(Provide["app_config.cognito.client_secret"]),
    redirect_uri: str = Depends(Provide["app_config.cognito.redirect_uri"]),
):
    """
    Exchanges a refresh token for a new set of id_token, access_token,
    and refresh_token.
    This endpoint should be called when the current access_token expires.

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
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
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

        if not id_token or not access_token:
            logger.error(f"Token not found in response {response_data}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ID token not found",
            )

        # Validate tokens
        # Only the id_token has an audience
        await jwt_validator.decode_jwt(id_token, verify_aud=True)
        # When not having an audience verifies client_id by default
        await jwt_validator.decode_jwt(access_token)

    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting tokens: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed token request",
        )

    return JSONResponse(
        content={
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )
