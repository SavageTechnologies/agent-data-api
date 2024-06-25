from django.core.exceptions import ValidationError


class PasswordValidator:
    def __init__(self):
        self.min_length = 8

    def validate(self, password, user=None):
        if password is None or len(password) < self.min_length:
            raise ValidationError(
                f"This password must contain at least {self.min_length} characters.",
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return f"Your password must contain at least {self.min_length} characters."


class DebugPasswordValidator:
    def validate(self, password, user=None):
        pass

    def get_help_text(self):
        return f"DEBUG password can be anything"