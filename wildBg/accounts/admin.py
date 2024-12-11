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

    list_display = ('pk', 'email', 'is_staff', 'is_superuser', 'is_active', 'last_login')
    list_display_links = ('email',)

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        ('Credentials', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ()
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ('last_login',)

    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    form = ProfileEditForm

    list_display = ('pk', 'user', 'first_name', 'last_name', 'level', 'points', 'date_of_birth')
    list_display_links = ('user',)

    list_filter = ('level', 'date_of_birth')

    search_fields = ('user__username', 'user__email', 'first_name', 'last_name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'first_name', 'last_name', 'date_of_birth', 'level')
        }),
        ('Profile Details', {
            'fields': ('profile_picture', 'description', 'background_image')
        }),
        ('Points and Landmarks', {
            'fields': ('points', 'landmarks_visited')
        }),
    )

    filter_horizontal = ('landmarks_visited',)

    readonly_fields = ('user',)

