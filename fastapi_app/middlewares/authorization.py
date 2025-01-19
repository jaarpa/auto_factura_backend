import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    SimpleUser,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection

from modules.authorization.domain.services.jwt_validator import JWTValidator

# Public routes.
PUBLIC_ROUTES = [
    "/authorization_code",
    "/refresh",
    "/status",
    "/docs",
    "/openapi.json",
]

logger = logging.getLogger(__name__)


@inject
class JWTAuthBackend(AuthenticationBackend):

    PUBLIC_ROUTES = [
        "/authorization_code",
        "/refresh",
        "/status",
        "/docs",
        "/openapi.json",
    ]

    def __init__(
        self,
        jwt_validator: JWTValidator = Provide["jwt_validator"],
        authorization_url: str = Provide["app_config.cognito.authorization_url"],
        app_domain: str = Provide["app_config.app.domain"],
        debug: bool = Provide["app_config.app.debug"],
        jwt_signature_validation: bool = Provide[
            "app_config.app.jwt_signature_validation"
        ],
        environment: str = Provide["app_config.app.environment"],
    ):
        """
        Class dedicated exclusively to validate that there is a JWT token
        in the request and that this token is valid.

        The list `PUBLIC_ROUTES` is a list of routes that won't be checked
        for a valid jwt token. If there is provided token anyway it will be
        decoded and add the user id data and scopes to the request.

        The JWT signature check can be skipped only on local development
        (environment == local) if you are debugging (debug = True) and
        you explicitly set jwt_signature_validation = False

        More info on how this works:
        - https://www.starlette.io/authentication/

        :param jwt_validator: Class used to validate the jwt if found, defaults to Provide["jwt_validator"]
        :param authorization_url: Url where the login of a user could start. This is used for documentation,
        defaults to Provide["app_config.cognito.authorization_url"]
        :param app_domain: App domain, used for crafting the refresh and token urls. Those urls are used
        for the generated documentation to show the endpoints used to get new tokens from an authorization code
        or a refresh token, defaults to Provide["app_config.app.domain"]
        :param debug: Flag to modify wether to check the token signature or not, defaults to Provide["app_config.app.debug"]
        :param jwt_signature_validation: Flag to modify wether to check the token signature or not, defaults to Provide[ "app_config.app.jwt_signature_validation" ]
        :param environment: Flag to modify wether to check the token signature or not, defaults to Provide["app_config.app.environment"]
        """
        super().__init__()
        self.__jwt_validator = jwt_validator
        self.__authorization_url = authorization_url
        self.__app_domain = app_domain
        self.__debug = debug
        self.__jwt_signature_validation = jwt_signature_validation
        self.__environment = environment

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser]:
        """
        Authenticates the user from the JWT token in the connection.

        If the user visits a public route the jwt token is not required,
        but if it is provided anyway it will be decoded.
        If the user visits a non-public route with no jwt token the request will
        be stopped. If the user provides a jwt token but the signature verification
        is off, the token will be decoded but not validated.

        :param conn: starlette connection where the token is searched for
        and where the user data will be set at.
        :raises AuthenticationError: If the token is not present or
        is invalid when visiting a non-public route
        :return: AuthCredentials which sets request.auth.scopes and some
        instance of BaseUser which sets request.user
        """
        public_route = conn.url.path in PUBLIC_ROUTES
        if public_route:
            logger.debug(
                f"Request path '{conn.url.path}' is in PUBLIC_ROUTES."
                "Skipping JWT validation."
            )
        oauth2_scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl=self.__authorization_url,
            tokenUrl=f"{self.__app_domain}/authorization_code",
            refreshUrl=f"{self.__app_domain}/refresh",
        )
        try:
            token = await oauth2_scheme(conn)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
                )
        except Exception as e:
            # We know for suer it does not have a token
            if public_route:
                return AuthCredentials(), UnauthenticatedUser()
            # If not public route stop request.
            logger.exception(e)
            raise AuthenticationError("Unauthorized access") from e

        # At this point we know for sure it has a token
        logger.debug("JWT token found.")
        verify_jwt_signature = not (
            self.__environment == "local"
            and self.__debug
            and not self.__jwt_signature_validation
        )
        if not verify_jwt_signature:
            logger.debug("Token validation off; not verifying signature.")
        try:
            decoded_token = await self.__jwt_validator.decode_jwt(
                token, verify_signature=verify_jwt_signature
            )
        except Exception as e:
            logger.exception(e)
            raise AuthenticationError("Unauthorized access") from e

        return AuthCredentials(decoded_token.get("scope", "").split()), SimpleUser(
            decoded_token["sub"]
        )


def get_current_user_id(request: Request) -> UUID:
    """
    Returns the user id found in the request under the pre-requisite of
    the user being authenticate by the `JWTAuthBackend`

    :param request: Request where the user is supposed to be set.
    :raises HTTPException: If there is a user set but it is not
    authenticated this exception is raised.
    :return: The user id of the authenticated user.
    """
    if not request.user.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    # We use starlette's SimpleUser which only has a username field
    # So the username is actually populated with the user_id
    return UUID(request.user.username)
