import os
from typing import Mapping


def get_environ_float(key: str, default_value: float) -> float:
    string_float = os.environ.get(key, None)
    if string_float is None:
        return default_value
    try:
        return float(string_float)
    except Exception as e:
        return default_value


