from django.contrib.auth.forms import UserCreationForm
from .models import User


class FullUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")  # type: ignore
        help_text = {"email": "Optional, but used for account recovery."}
