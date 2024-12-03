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
        # context['last_comment_only'] = True  # To signal the template to show only the last comment

        posts = self.get_queryset()
        # posts_with_last_comment = []
        # for post in posts:
        #     last_comment = post.comments.order_by('-created_at').filter().first()
        #
        #     if last_comment:
        #         last_comment_data = {
        #             'comment': last_comment,
        #             'author_name': f"{last_comment.author.profile.first_name} {last_comment.author.profile.last_name}",
        #             'author_profile_picture': last_comment.author.profile.profile_picture if last_comment.author.profile.profile_picture else None,
        #             'created_at': last_comment.created_at,
        #             'content': last_comment.content,
        #         }
        #     else:
        #         last_comment_data = None
        #
        #     posts_with_last_comment.append({
        #         'post': post,
        #         'last_comment': last_comment_data  # Detailed last comment data, or None if no comments
        #     })
        #
        # context['posts_with_last_comment'] = posts_with_last_comment

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
