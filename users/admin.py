from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    
    '''Custom User Admin'''
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields":(
                    "avatar",
                    "gender",
                    "bio",
                    "superorganizer",
                )
            }
        ),
    )
    list_filter = UserAdmin.list_filter + (
        "superorganizer",
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "superorganizer",
        "email_verified",
        "email_secret",
    )