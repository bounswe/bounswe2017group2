from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import RegisteredUser
# Register your models here.

# we are not using django admin. Uncomment the code below use the admin. Modifications will be needed in RegisteredUser class.

'''
# our customized User model.
admin.site.register(RegisteredUser, UserAdmin)
'''
