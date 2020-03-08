from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from rooms.models import Room

class RoomsInline(admin.TabularInline):
    
    model = Room

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    """ Custom User Admin """
    
    inlines = (RoomsInline, )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birth",
                    "language",
                    "currency",
                    "superhost",
                )
            }
        ),
    )
    
    list_filter = UserAdmin.list_filter + ('superhost',)

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'language',
        'currency',
        'superhost',
        'is_staff',
        'is_superuser',    
    )