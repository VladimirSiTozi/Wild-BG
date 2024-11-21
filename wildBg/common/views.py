from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from wildBg.common.forms import SearchForm
from wildBg.post.forms import PostCommentForm
from wildBg.post.models import Post


class HomePageView(ListView):
    model = Post
    template_name = 'common/home.html'
    context_object_name = 'all_posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = PostCommentForm
        context['search_form'] = SearchForm(self.request.GET)

        user = self.request.user

        for post in context['all_posts']:
            post.has_liked = post.like_set.filter(user=user).exists() if user.is_authenticated else False

        return context

    def get_queryset(self):
        queryset = super().get_queryset()  # get all objects .order_by('-date_of_publication')
        user_name = self.request.GET.get('user_name')

        if user_name:
            queryset = queryset.filter(  # filter the objects
                tagged_people__name__icontains=user_name
            )

        return queryset  # return new queryset


def comment_func(request, post_id: int):
    if request.POST:
        post = Post.objects.get(pk=post_id)
        comment_form = PostCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{post_id}')

