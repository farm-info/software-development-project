from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=True,
        help_text="Optional but recommended. Used for account recovery.",
    )
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="media/profile_pictures/", null=True, blank=True
    )
