from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = (
        "email", "first_name", "last_name", "user_name", "last_login", "date_joined", "is_active"
    )

    list_display_links = (
        "email", "first_name", "last_name"
    )

    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",)

    fieldsets = (
        ("Login Credential", {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_name', 'first_name', 'last_name', 'about')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
    ("Required for new account", {
        'classes': ('wide',),
        'fields': ('email', 'user_name', 'first_name', 'last_name', 'about', 'password1', 'password2'),
    }),
)


    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(Account, AccountAdmin)

admin.site.register(UserProfile)