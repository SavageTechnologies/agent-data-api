import dataclasses
from typing import Optional, Dict


@dataclasses.dataclass
class ServerException(Exception):
    status_code: int = 400
    error_name: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def safe_error_name(self) -> str:
        if self.error_name is None:
            return ""
        return self.error_name

    @property
    def safe_error_message(self) -> str:
        if self.error_message is None:
            return ""
        return self.error_message

    @property
    def has_info(self) -> bool:
        return self.error_name is not None or self.error_message is not None

    def to_json(self) -> Dict:
        d = {}
        if self.error_name is not None:
            d["error_name"] = self.error_name
        else:
            d["error_name"] = "general"

        if self.error_message is not None:
            d["error_message"] = self.error_message
        return d

    def __str__(self) -> str:
        return f"ServerException: {self.status_code} - {str(self.error_name)} - {str(self.error_message)}"

    @classmethod
    def generic_auth_error(cls) -> "ServerException":
        return ServerException(status_code=401, error_name="AuthError", error_message="You need a user account to do this")

    @classmethod
    def generic_not_found(cls) -> "ServerException":
        return ServerException(status_code=404, error_name="NotFound", error_message="The request or path is not found")

    @classmethod
    def generic_not_found_object(cls, object_name: str, object_id) -> "ServerException":
        return ServerException(status_code=404, error_name="NotFound", error_message=f"The {object_name}:{str(object_id)} is not found")

    @classmethod
    def bad_json(cls) -> "ServerException":
        return ServerException(status_code=400, error_name="BadJson", error_message="Request json was malformed")

    @classmethod
    def bad_api_key(cls) -> "ServerException":
        return ServerException(status_code=401, error_name="AuthError", error_message="You are not authorized to make this call")
