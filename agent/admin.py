from django.contrib import admin

from agent.models import Agent


# Register your models here.


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    fields = ["id", "name", "email", "npn", "phone_number", "updated_at", "created_at"]
    readonly_fields = ["id", "updated_at", "created_at"]
    list_display = ["id", "name", "email", "npn", "phone_number", "updated_at", "created_at"]
    list_editable = ["name", "email", "npn", "phone_number"]
    search_fields = [
        "name",
        "email",
        "npn",
        "phone_number",
    ]
