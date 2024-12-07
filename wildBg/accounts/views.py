from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView

from wildBg.accounts.forms import AppUserCreationForm
from wildBg.accounts.models import Profile, AppUser
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


class ProfileDeleteView(SidebarContextMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AppUser
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def delete(self, request, *args, **kwargs):
        # Get the profile object
        profile = self.get_object()

        # Delete the associated user (AppUser model)
        user = profile.user  # Get the associated AppUser instance
        user.delete()  # This will also delete the Profile because of on_delete=models.CASCADE

        # Return the response for the DeleteView
        return super().delete(request, *args, **kwargs)