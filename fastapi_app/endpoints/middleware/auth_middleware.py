# from fastapi import Request, HTTPException
# from starlette.middleware.base import BaseHTTPMiddleware
# from typing import List
# from fastapi_app.endpoints.utils.validator_class import JWTValidator


# class AuthMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app, jwt_validator: JWTValidator, exclude_paths: List[str]):
#         super().__init__(app)
#         self.jwt_validator = jwt_validator
#         self.exclude_paths = exclude_paths  # Rutas a excluir del middleware

#     async def dispatch(self, request: Request, call_next):
#         # Verificar si la ruta actual está excluida
#         path = request.url.path
#         if path in self.exclude_paths:
#             return await call_next(request)

#         # Verificar si el header Authorization está presente
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             raise HTTPException(
#                 status_code=401, detail="Authorization header missing or invalid"
#             )

#         token = auth_header.split(" ")[1]

#         # Validar el token
#         try:
#             decoded_token = await self.jwt_validator.validate_jwt(token)
#             # Agregar el token decodificado al estado de la request
#             request.state.user = decoded_token
#         except HTTPException as e:
#             raise e
#         except Exception:
#             raise HTTPException(status_code=500, detail="Error validating token")

#         # Llamar al siguiente middleware o endpoint
#         response = await call_next(request)
#         return response
