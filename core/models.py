import uuid

from django.db import models


class BaseModel(models.Model):
    """
    A base upon which all models should inherit.
    This insures all models have a minimum set of fields.
    I also prefer to just start using UUIDs from the get-go, you can base58 encode them to create a very nice
    human-readable ID.
    """
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        abstract = True
