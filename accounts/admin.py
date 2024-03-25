from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, UserOtpCode, Subscription
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["full_name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone_number", "password"]}),
        ("Personal info", {"fields": ["full_name"]}),
        ("Permissions", {"fields": ["is_admin", "is_active"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone_number", "full_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["full_name"]
    ordering = ["full_name"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(UserOtpCode)
admin.site.register(Subscription)