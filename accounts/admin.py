from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model= CustomUser
    fieldsets=UserAdmin.fieldsets+(("Additional",{"fields":("phone",)}),)
    add_fieldsets=UserAdmin.add_fieldsets+(("Additional",{"fields":("phone",)}),)

# Register your models here.
