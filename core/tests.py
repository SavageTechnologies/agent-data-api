import json
from typing import Optional, Type

import django
from django.http import HttpResponse
from django.test import TestCase
from django.test import Client
from pydantic import BaseModel, ValidationError
from django.test.runner import DiscoverRunner

from server import settings
from user.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def assert_response_with_code(self, response: HttpResponse, status_code: int):
        self.assertEquals(response.status_code, status_code)

    def assert_response_ok(self, response: HttpResponse, response_json_schema: Optional[Type[BaseModel]] = None):
        if response.status_code < 200 or response.status_code >= 400:
            error_message = "None"
            msg = f"Request failed with status {response.status_code} and message: {error_message}"
            raise self.failureException(msg)

        if response_json_schema is not None:
            return response_json_schema.model_validate_json(response.content)

    def login(self, user: User, client: Optional[Client] = None):
        if client is None:
            client = self.client
        client.force_login(user)


class TestSuiteRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        settings.IS_TEST = True
        super().__init__(*args, **kwargs)

