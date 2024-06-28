from django import forms
from django.contrib import admin
from django.contrib.auth.password_validation import validate_password

from user.models import User


class UserForm(forms.ModelForm):
    set_password = forms.CharField(required=False, validators=[validate_password])

    def clean_set_password(self):
        set_password_to = self.cleaned_data.get("set_password")
        if self.instance._state.adding or (set_password_to is not None and len(set_password_to) > 0):
            validate_password(set_password_to)
        return set_password_to

    def save(self, commit=True):
        instance: User = self.instance
        set_password_to = self.cleaned_data.pop("set_password")
        if self.instance._state.adding or (set_password_to is not None and len(set_password_to) > 0):
            validate_password(set_password_to)  # just double validate for now
            instance.set_password(set_password_to)
        instance.email = instance.username
        return super().save(commit)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "is_staff", "is_superuser", "is_active",
                  "groups", "user_permissions", "set_password",]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    readonly_fields = ["id", "email", "last_login", "date_joined", "updated_at", "created_at"]
    list_display = ["id", "username", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "last_login", "updated_at", "created_at"]
    list_editable = ["first_name", "last_name", "username",]
    search_fields = [
        "username",
    ]
    list_filter = [
        "is_superuser",
    ]



