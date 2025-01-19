from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class JWTValidator(Protocol):
    """
    Service to determine if a jwt token is valid or not, and decodes it
    if valid.

    More info on jwt tokens
    - https://jwt.io/
    """

    @abstractmethod
    async def decode_jwt(self, token: str, **kwargs) -> dict:
        """
        Tries to decode the provided token. On decoding it validates
        it and if the token is valid returns the decoded token claims.
        If the token is not valid raises an exception.

        kwargs are passed as jwt.decode options.

        :param token: JWT token generated on successful authentication.
        :return: A dictionary containing the decoded JWK token claims.
        """
