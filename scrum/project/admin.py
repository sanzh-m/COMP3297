from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Developer)
admin.site.register(Manager)
admin.site.register(Project)

# Register your models here.
