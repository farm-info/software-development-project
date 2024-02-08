from django.contrib.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

class CustomerUser(User):
    USER_TYPE_CHOICES = [
        ('C', 'Customer'),
    ]

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='C')

    def __str__(self):
        return self.username

class ProfessionalUser(User):
    USER_TYPE_CHOICES = [
        ('P', 'Professional'),
    ]

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='P')

    def __str__(self):
        return self.username

class AdminUser(User):
    USER_TYPE_CHOICES = [
        ('A', 'Admin'),
    ]

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='A')

    def __str__(self):
        return self.username