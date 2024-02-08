from django.contrib import admin

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('C', 'Customer'),
        ('P', 'Professional'),
        ('A', 'Admin'),
    ]
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='C')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.username