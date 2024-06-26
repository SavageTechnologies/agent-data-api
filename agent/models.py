from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel


# Create your models here.

class Agent(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    npn = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True, region="US")

    def __str__(self):
        return f"<Agent: {self.id} - {self.name}>"
    class Meta:
        db_table = "agents"


