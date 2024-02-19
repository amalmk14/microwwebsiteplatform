from django.contrib import admin
from .models import Profile,Storedotps,EmailVerificationToken

# Register your models here.

admin.site.register(Profile)
admin.site.register(Storedotps)
admin.site.register(EmailVerificationToken)
