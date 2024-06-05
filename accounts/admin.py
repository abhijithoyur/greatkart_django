from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email','username','first_name','last_name','phone_number','date_joined','last_login','is_active')
    list_display_links = ('email', 'username')
    readonly_fields = ('date_joined','last_login','password')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)



