from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from wildBg.accounts.models import Profile
from wildBg.common.forms import SearchForm
from wildBg.landmark.models import Landmark
from wildBg.mixins import SidebarContextMixin
from wildBg.post.forms import PostCommentForm
from wildBg.post.models import Post


UserModel = get_user_model()


class HomePageView(SidebarContextMixin, ListView):
    model = Post
    template_name = 'common/home.html'
    context_object_name = 'all_posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = PostCommentForm
        context['search_form'] = SearchForm(self.request.GET)

        user = self.request.user
        all_posts = context[self.context_object_name]

        # Add `has_liked` to each post
        if user.is_authenticated:
            for post in all_posts:
                post.has_liked = post.likes.filter(user=user).exists()

        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')  # get all objects .order_by('-date_of_publication')

        user_name = self.request.GET.get('user_name')
        if user_name:
            queryset = queryset.filter(  # filter the objects
                tagged_people__name__icontains=user_name
            )

        return queryset  # return new queryset


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
