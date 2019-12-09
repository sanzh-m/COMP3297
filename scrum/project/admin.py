from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *


class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'user_type', 'password1', 'password2')}
		 ),
	)
	form = UserChangeForm
	fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'user_type', 'password')}
		 ),
	)
	model = User
	list_display = ['username', 'user_type', ]


admin.site.register(User, UserAdmin)
# admin.site.register(MyUserManager)
admin.site.register(Developer)
admin.site.register(Manager)
admin.site.register(Project)

# Register your models here.
