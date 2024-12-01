from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView

from wildBg.accounts.models import Profile
from wildBg.mixins import SidebarContextMixin

UserModel = get_user_model()


class ProfileDetailView(SidebarContextMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     user = self.get_object()
    #
    #     context['posts'] = user.posts.all()
    #
    #     return context





