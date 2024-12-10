from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from wildBg.accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control wide-input',
                'placeholder': 'Enter your email address',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control wide-input',
                'placeholder': 'Enter your password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control wide-input',
                'placeholder': 'Confirm your password',
            }),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write something about you...'})
        }
