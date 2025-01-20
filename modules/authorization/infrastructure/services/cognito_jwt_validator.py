import jwt

from modules.authorization.domain.services.jwt_validator import JWTValidator


class CognitoJWTValidator(JWTValidator):
    """
    Validation service to validate and decode JWT tokens
    supposedly issued by cognito.
    """

    def __init__(self, client_id: str, issuer_url: str, jwks_url: str):
        self._client_id = client_id
        self._issuer_url = issuer_url
        self._jwks_client = jwt.PyJWKClient(jwks_url)

    async def decode_jwt(self, token: str, **kwargs) -> dict:
        signing_key = self._jwks_client.get_signing_key_from_jwt(token)

        decoding_options = {"verify_aud": False}
        decoding_options.update(kwargs)

        decoded_token = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=self._client_id,
            issuer=self._issuer_url,
            options=decoding_options,
        )

        # If audience was not verified then check that client_id is correct
        if (
            not decoding_options.get("verify_aud")
            and decoded_token.get("client_id") != self._client_id
        ):
            raise jwt.InvalidTokenError("Invalid client_id")

        return decoded_token
