from fastapi import HTTPException
from jwt import PyJWKClient, decode


class JWTValidator:
    def __init__(self, jwks_url: str, client_id: str, user_pool_id: str):
        # PyJWKClient instance created once.
        self.jwks_client = PyJWKClient(jwks_url)
        self.client_id = client_id
        self.issuer = f"https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}"

    async def validate_jwt(self, token: str) -> dict:
        try:
            # We use the same instance of jwks_client
            signing_key = await self.get_signing_key(token)

            decoded_token = decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.issuer,
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            print(f"Unexpected error during JWT validation: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_signing_key(self, token: str):
        """
        Obtain the public key from the PyJWK client.
        """
        return self.jwks_client.get_signing_key_from_jwt(token)
