from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView

UserModel = get_user_model()


class ProfileDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'


