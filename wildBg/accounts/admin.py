from django.contrib import admin
from django.contrib.auth import get_user_model

from wildBg.accounts.forms import AppUserCreationForm, AppUserChangeForm, ProfileEditForm
from wildBg.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(admin.ModelAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser', )
    search_fields = ('email', )
    ordering = ('pk', )

    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ( )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    form = ProfileEditForm

    list_display = ('pk', 'first_name', 'last_name', 'level')
