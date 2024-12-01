from django.shortcuts import render
from django.views.generic import ListView, DetailView

from wildBg.mixins import SidebarContextMixin
from wildBg.post.models import Post


class PostDetailView(SidebarContextMixin, DetailView):
    model = Post
    template_name = 'post/post-detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

