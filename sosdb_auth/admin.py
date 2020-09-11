from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .models import SosdbUser

class SosdbUserAdmin(UserAdmin):
	def __init__(self, *args, **kwargs):
		super(SosdbUserAdmin, self).__init__(*args, **kwargs)

	add_fieldsets = (
		(None, {
			'fields' : ('user_id')}
		),
	)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'user_id')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
			'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_id')
	search_fields = ('email', 'username', 'first_name', 'last_name', 'user_id')

admin.site.register(SosdbUser, SosdbUserAdmin)
