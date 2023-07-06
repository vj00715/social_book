from django.contrib import admin
from .models import CustomUser, Book
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class MyUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("custom_field", {'fields': ('public_visibility', 'age')}),
    )

admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Book)