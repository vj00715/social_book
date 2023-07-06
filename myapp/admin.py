from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class MyUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("custom_field", {'fields': ('custom_field',)}),
    )

admin.site.register(CustomUser, MyUserAdmin)
