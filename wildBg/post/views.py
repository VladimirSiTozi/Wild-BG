from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.checks import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from wildBg.accounts.models import Profile, AppUser
from wildBg.landmark.models import Like, Landmark
from wildBg.mixins import SidebarContextMixin
from wildBg.post.forms import PostCommentForm, ReplyPostCommentForm, PostAddForm, PostEditForm
from wildBg.post.models import Post, PostLike, PostComment

from django.shortcuts import get_object_or_404


class PostAddView(LoginRequiredMixin, SidebarContextMixin, CreateView):
    model = Post
    form_class = PostAddForm
    template_name = 'post/post-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add landmarks to the context
        context['landmarks'] = Landmark.objects.all()
        context['tagged_people'] = AppUser.objects.all()
        return context

    def form_valid(self, form):
        # Associate the post with the logged-in user
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()  # Save many-to-many relationships, if any
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to a success page, e.g., details view for the created post
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDetailView(SidebarContextMixin, DetailView):
    model = Post
    template_name = 'post/post-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = PostCommentForm()
        context['all_comments'] = True  # To signal the template to show all comments

        post = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            self.object.has_liked = self.object.likes.filter(user=self.request.user).exists()
        else:
            self.object.has_liked = False

        comments = post.comments.all().order_by('-created_at')
        comment_data = []
        for comment in comments:
            replies = comment.replies.all().order_by('-created_at')

            # Collect details for each reply
            reply_data = []
            for reply in replies:
                reply_data.append({
                    'reply': reply,
                    'author_name': f"{reply.author.profile.first_name} {reply.author.profile.last_name}",
                    'author_profile_picture': reply.author.profile.profile_picture if reply.author.profile.profile_picture else None,
                    'created_at': reply.created_at,
                    'content': reply.content,
                })

            # Add detailed comment data
            comment_data.append({
                'comment': comment,
                'author_name': f"{comment.author.profile.first_name} {comment.author.profile.last_name}",
                'author_profile_picture': comment.author.profile.profile_picture if comment.author.profile.profile_picture else None,
                'created_at': comment.created_at,
                'content': comment.content,
                'replies': reply_data
            })

        # Add to the context
        context['comments'] = comment_data
        context['tagged_people'] = post.tagged_people.all()

        return context


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, SidebarContextMixin, UpdateView):
    model = Post
    template_name = 'post/post-edit.html'
    form_class = PostEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['landmarks'] = Landmark.objects.all()
        context['tagged_people'] = [
            {
                'id': person.id,
                'full_name': Profile.objects.get(user=person).get_full_name()
            }
            for person in self.object.tagged_people.all()
        ]
        return context

    def form_valid(self, form):
        # Handle additional logic if necessary
        return super().form_valid(form)

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy(
            'post-detail',
            kwargs={'pk': self.object.pk}
        )


@login_required
def like_post_func(request, pk: int):
    liked_object = PostLike.objects.filter(
        to_post=pk,
        user=request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = PostLike(to_post_id=pk, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER', 'post-detail'))


@login_required
def add_comment(request, pk: int):
    # post = get_object_or_404(Post, pk=post_id)  # This will trigger a 404 if the post doesn't exist

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        comment_form = PostCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect(request.META.get('HTTP_REFERER', f'#{pk}'))


@login_required
def add_reply(request, pk: int):
    if request.method == 'POST':
        comment = PostComment.objects.get(pk=pk)
        reply_form = ReplyPostCommentForm(request.POST)

        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = reply
            reply.author = request.user
            reply.save()

    return redirect(request.META.get('HTTP_REFERER', f'#{pk}'))


@login_required
def search_users(request):
    if 'query' in request.GET:
        query = request.GET.get('query', '').strip()
        users = Profile.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).exclude(
            Q(first_name__isnull=True) & Q(last_name__isnull=True)
        )
        users_data = [
            {'id': user.user.id, 'name': user.get_full_name()}
            for user in users
        ]
        return JsonResponse(users_data, safe=False)
    return JsonResponse([], safe=False)