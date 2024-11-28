from fastapi import FastAPI, Request, HTTPException, status
from jwt import PyJWKClient, decode, ExpiredSignatureError, InvalidTokenError

from fastapi import Depends
from dependency_injector.wiring import Provide, inject

#Public routes.
PUBLIC_ROUTES = ["/","/callback","/status","/docs","/openapi.json"]

#@app.middleware("http")
@inject
async def validate_jwt(request:Request,
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
            return await call_next(request)
        # Get the token from the Authorization header
         
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or malformed")
        
        token = auth_header.split(" ")[1]
        
        # We use the same instance of jwks_client
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        decoded_token = decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=client_id,
            issuer=issuer,
        )
        #Stores the decoded token in the request.state
        request.state.user = decoded_token
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        print(f"Unexpected error during JWT validation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return await call_next(request)



