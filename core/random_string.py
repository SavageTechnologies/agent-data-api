import random
import string
from typing import Optional


def random_string(length: int, char_set: Optional[str] = None) -> str:
    if length <= 0:
        return ""
    if char_set is None:
        char_set = string.ascii_letters + string.digits
    return ''.join(random.choice(char_set) for _ in range(length))


def random_asset_folder_id() -> str:
    return random_string(16)


def random_255_key() -> str:
    return random_string(255)


def random_password() -> str:
    return random_string(64)


