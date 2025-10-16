from django.contrib import admin
from .models import User, OTPHandler

admin.site.register(User)
admin.site.register(OTPHandler)

