from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import RegisteredUser
# Register your models here.

# our customized User model.
admin.site.register(RegisteredUser, UserAdmin)
