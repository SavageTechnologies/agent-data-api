import uuid
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import QuerySet

from core.models import BaseModel
from core.random_string import random_255_key
from django.contrib.auth.password_validation import validate_password


class User(AbstractUser):
    username_validator = EmailValidator()
    """
    Override the default Django user model.
    It's almost always a good idea to do this because doing it post-launch is very difficult
    """
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(
        "Username",
        max_length = 255,
        unique = True,
        help_text = ("Required. Must be a valid email address."),
        validators = [username_validator],
        error_messages = {
            'unique': ("A user with that username already exists."),
        },
    )

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    @staticmethod
    def validate_password(password: str) -> bool:
        try:
            validate_password(password)
            return True  ## TODO
        except Exception as e:
            return False
    class Meta:
        db_table = "users"

