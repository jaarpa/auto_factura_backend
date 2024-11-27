# Interfaz

from typing import Protocol
from typing import runtime_checkable
from abc import abstractmethod


@runtime_checkable
class JWTValidator(Protocol):

    @abstractmethod
    async def validate_jwt(self, token: str) -> dict:
        """
        _summary_

        :param token: _description_
        :return: _description_
        """

    @abstractmethod
    async def get_signing_key(self, token: str) -> dict:
        """
        Obtain the public key (JWKs) from the PyJWK client.
        """
