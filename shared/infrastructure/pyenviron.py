import os
import json
from pathlib import Path
from shared.domain.environ import Environ


class PyEnviron(Environ):
    """
    Implementation of environment manager wich uses the `os` standard
    library and simple casting.
    """

    def get_str_from_path(self, key: str, default: str | None = None) -> str | None:
        file_value = default
        file_path = self.get_path(key)
        if file_path and file_path.exists() and file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as file:
                file_value = file.read().strip()
        return file_value if file_value else default

    def get_str(self, key: str, default: str | None = None) -> str | None:
        return os.environ.get(key, default)

    def get_bool(self, key: str, default: bool | None = None) -> bool | None:
        return bool(os.environ.get(key, default))

    def get_int(self, key: str, default: int | None = None) -> int | None:
        uncasted_value = os.environ.get(key)
        number = default
        if not uncasted_value:
            return default
        try:
            number = int(uncasted_value)
        except ValueError:
            pass
        return number

    def get_float(self, key: str, default: float | None = None) -> float | None:
        uncasted_value = os.environ.get(key)
        number = default
        if not uncasted_value:
            return default
        try:
            number = float(uncasted_value)
        except ValueError:
            pass
        return number

    def get_json(self, key: str, default: dict | None = None) -> dict | None:
        encoded_json = self.get_str(key)
        if not encoded_json:
            return default
        decoded_json = default
        try:
            decoded_json = json.loads(encoded_json)
        except json.JSONDecodeError:
            pass
        return decoded_json

    def get_str_tuple(
        self, key: str, default: tuple[str, ...] | None = None, separator=","
    ) -> tuple[str, ...] | None:
        encoded_tuple = self.get_str(key)
        value = default
        if encoded_tuple:
            value = tuple(encoded_tuple.split(separator))
        return value

    def get_path(self, key: str, default: Path | str | None = None) -> Path | None:
        default_path = Path(default) if default is not None else default
        path_string = self.get_str(key)
        path = default_path
        if not path_string:
            return default_path
        try:
            path = Path(path_string)
        except ValueError:
            pass
        return path
