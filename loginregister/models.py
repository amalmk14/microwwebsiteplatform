from django.db import models
import uuid
# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=50)
    password = models.TextField()
    email = models.EmailField()
    phone = models.TextField(default='123 123 1234')
    country = models.CharField(max_length=100,default='Country')
    cuid = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)
    delete_token = models.TextField()


    def __str__(self):
        return self.name
    

class Storedotps(models.Model):
    email_id=models.EmailField()
    otp=models.CharField(max_length=6)
    otp_active=models.BooleanField(default=True)
    valid_from=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.email_id

from django.db import models
from django.utils import timezone

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Token for {self.user.email}'
    

class DeleteVerificationToken(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Token for {self.user.email}'
