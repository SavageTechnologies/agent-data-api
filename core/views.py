from typing import Optional, Type, TypeVar, Dict

import orjson
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel as PydanticBaseModel, ValidationError

from core.errors import ServerException
from server import settings
from user.models import User

JsonModelT = TypeVar("JsonModelT", bound=PydanticBaseModel)


class BaseView(View):

    __attempted_to_get_user = False
    __user: Optional[User] = None
    __cached_json_request: Optional[Dict] = None

    requires_login = False
    redirect_if_not_logged_in = True

    @property
    def user(self) -> Optional[User]:
        if self.__user is not None or self.__attempted_to_get_user:
            return self.__user
        self.__attempted_to_get_user = True
        if self.request.user.is_authenticated and self.request.user.is_active:
            self.__user = self.request.user
        return self.__user

    @property
    def json_request(self) -> Dict:
        if self.__cached_json_request is not None:
            return self.__cached_json_request
        try:
            self.__cached_json_request = orjson.loads(self.request.body.decode('utf-8'))
        except orjson.JSONDecodeError as de:
            print(de)
            raise ServerException.bad_json()
        return self.__cached_json_request

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            if self.requires_login and self.user is None:
                if self.redirect_if_not_logged_in:
                    return redirect("/user/login/", permanent=False)
                raise ServerException.generic_auth_error()
            return super().dispatch(request, *args, **kwargs)
        except ServerException as se:
            if se.has_info:
                return JsonResponse(status=se.status_code, data=se.to_json())
            return HttpResponse(status=se.status_code)

    def get_validated_json(self, json_model: Type[JsonModelT]) -> JsonModelT:
        try:
            json_request = self.json_request
            parsed_json = json_model.model_validate(json_request)
        except ValidationError as ve:
            if settings.DEBUG:
                print(ve)
            raise ServerException(status_code=400, error_name="JsonParse")   # TODO catch parsing errors here
        return parsed_json

    def login(self, user: User):
        django_login(self.request, user)
        self.__user = user
        self.__attempted_to_get_user = True

    def logout(self):
        if self.user is not None:
            django_logout(self.request)
            self.__user = None

    def check_user(self):
        if self.user is None:
            raise ServerException.generic_auth_error()

