from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel


# Create your models here.

class Agent(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    npn = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    class Meta:
        db_table = "agents"


