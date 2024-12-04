from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from wildBg.accounts.forms import AppUserCreationForm
from wildBg.accounts.models import Profile
from wildBg.mixins import SidebarContextMixin

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'



class ProfileDetailView(SidebarContextMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        # user = form.save()  # --> self.object
        login(self.request, self.object)

        return response



