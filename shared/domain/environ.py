from typing import Protocol
from typing import runtime_checkable
from abc import abstractmethod
from pathlib import Path


@runtime_checkable
class Environ(Protocol):
    """
    Manage environement variables an read and convert their contents
    """

    @abstractmethod
    def get_str_from_path(self, key: str, default: str | None = None) -> str | None:
        """
        Reads the file at the location given by the environment variable
        `key` and returns its stripped content as string.
        It is assumed that the file has only one line.

        :param key: Environment variable name. Must contain a path like
        `RDBMS_PASSWORD_FILE=/run/secrets/postgres-passwd`
        :param default: Default value to return if the key does not exists
        or the path it points too does not exists.
        :return: Stripped string with the content of the file.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_str(self, key: str, default: str | None = None) -> str | None:
        """
        Returns the string value in `key` or `default`.

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in
        the environment, defaults to None.
        :return: Value stored by the environment variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_bool(self, key: str, default: bool | None = None) -> bool | None:
        """
        Returns the truthsiness value of value in `key` or `default`.

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in the
        environment, defaults to None.
        :return: Equivalent True or False value of the stored value by the
        environment variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_int(self, key: str, default: int | None = None) -> int | None:
        """
        Returns the value in `key` casted to int or `default`.

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in the
        environment, defaults to None.
        :return: Integer value stored by the environment
        variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_float(self, key: str, default: float | None = None) -> float | None:
        """
        Returns the value in `key` casted to float or `default`.

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in the
        environment, defaults to None.
        :return: Float casted value stored by the environment
        variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_json(self, key: str, default: dict | None = None) -> dict | None:
        """
        Json parsed value in `key` or `default`.

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in the
        environment, defaults to None.
        :return: Json casted value stored by the environment
        variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_str_tuple(
        self, key: str, default: tuple[str, ...] | None = None, separator=","
    ) -> tuple[str, ...] | None:
        """
        Parses a tuple decoded as string in `key` or returns `default`.
        The values in the tuple are not casted and just returned as strings.

        Example:
        FOO=1,B,x,d
        would be read as
        ("1", "B", "x", "d")

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in the
        environment, defaults to None.
        :param separator: Character used to separate each entry in the
        tuple, defaults to ','.
        :return: Tuple casted value stored by the environment
        variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_path(self, key: str, default: Path | None = None) -> Path | None:
        """
        Parses a path from a string stored in `key` or returns `default`.

        :param key: Environment variable name.
        :param default: Value to return if `key` is not in the
        environment, defaults to None.
        :return: Path object from value stored by the environment
        variable `key` or the `default`.
        """
        raise NotImplementedError("Not implemented")
