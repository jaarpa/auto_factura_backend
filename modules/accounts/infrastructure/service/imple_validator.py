from fastapi import HTTPException
from jwt import PyJWKClient, decode
from modules.accounts.domain.service.interface_jwt_validator import JWTValidator
import jwt


class ValidateJWT(JWTValidator):
    def __init__(self, region: str, client_id: str, user_pool_id: str):
        
        self.region = region
        self.client_id = client_id
        self.issuer = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
        
        #PyJWKClient instance created once.
        self.jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json" 
        self.jwks_client = PyJWKClient(self.jwks_url)
        
        
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

    async def get_signing_key(self, token: str) -> dict:
        """
        Obtain the public key from the PyJWK client.
        """
        return self.jwks_client.get_signing_key_from_jwt(token)
