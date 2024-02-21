from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms


class FullUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # type: ignore
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")  # type: ignore


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']