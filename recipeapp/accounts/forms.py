from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime


class FullUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # type: ignore
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")  # type: ignore


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
            "date_of_birth",
        ]
        widgets = {
            "date_of_birth": forms.SelectDateWidget(
                years=range(1900, datetime.now().year)
            ),
        }


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
        ]
        widgets = {
            "date_of_birth": forms.SelectDateWidget(
                years=range(1900, datetime.now().year)
            ),
        }
