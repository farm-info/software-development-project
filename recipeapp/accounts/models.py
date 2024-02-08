from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("professional", "Professional"),
        ("user", "User"),
    )

    account_type = models.CharField(
        max_length=12,
        choices=ACCOUNT_TYPE_CHOICES,
        default="user",
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        help_text="Optional but recommended. Used for account recovery.",
    )
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="media/profile_pictures/", null=True, blank=True
    )
