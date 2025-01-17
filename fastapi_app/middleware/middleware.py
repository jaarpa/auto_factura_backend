import logging

from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Request, status
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWKClient, decode

# Public routes.
PUBLIC_ROUTES = [
    "/",
    "/callback",
    "/docs",
    "/openapi.json",
]

# @app.middleware("http")
@inject
async def validate_jwt(
    request: Request,
    call_next,
    region: str = Provide["app_config.cognito.region"],
    client_id: str = Provide["app_config.cognito.client_id"],
    user_pool_id: str = Provide["app_config.cognito.user_pool_id"],
):
    """
    Middleware to validate JWT on each request.
    """
    jwks_url: str = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
    issuer: str = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
    jwks_client = PyJWKClient(jwks_url)
    try:
        if request.url.path in PUBLIC_ROUTES:
            logging.debug(
                f"Request path '{request.url.path}' is in PUBLIC_ROUTES. Skipping validation."
            )
            return await call_next(request)
        # Get the token from the Authorization header

        auth_header = request.headers.get("Authorization")
        # logging.debug(f"Authorization header found: {auth_header}")
        if not auth_header or not auth_header.startswith("Bearer "):
            logging.error(f"Authorization header missing or malformed: {auth_header}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or malformed",
            )
        parts = auth_header.strip().split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            logging.error(f"Authorization header malformed: {auth_header}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header malformed",
            )
        token = parts[1]

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            logging.info(f"Signing key retrieved: {signing_key.key}")
        except Exception as e:
            logging.error(f"Error retrieving signing key: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Signing key error: {str(e)}",
            )

        logging.info("Validation process started")
        try:
            decoded_token = decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=issuer,
            )
            # Stores the decoded token in the request.state
            # logging.info(f"Decoded token successfully: {decoded_token}")
            request.state.user = decoded_token
            logging.info("Middleware validation successful")

        except ExpiredSignatureError:
            logging.error("Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )

        except InvalidTokenError:
            logging.error("invalid token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        except Exception as e:
            logging.error(f"Unexpected error during token decoding: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error during token validation",
            )

    except HTTPException as e:
        # Re-raise any HTTPException encountered
        raise e

    except Exception as e:
        logging.error(f"Unexpected error during JWT validation: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return await call_next(request)
