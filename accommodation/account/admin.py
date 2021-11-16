from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'is_owner')
    search_fields = ('email', 'phone_number')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)
    list_filter = ('is_owner',)
    list_editable = ('is_owner',)

    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, AccountAdmin)

# admin.site.register(User)