from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView

from wildBg.accounts.models import Profile
from wildBg.common.forms import SearchForm, SearchLandmarkForm
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

        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(author__profile__first_name__icontains=search_query) |
                Q(author__profile__last_name__icontains=search_query) |
                Q(author__profile__first_name__icontains=search_query) & Q(author__profile__last_name__icontains=search_query) |
                Q(location__name__icontains=search_query) |
                Q(location__location_name__icontains=search_query)
            ). distinct()

        return queryset


class AboutUsPageView(SidebarContextMixin, TemplateView):
    template_name = 'common/about-us.html'


class LandmarksHomePageView(SidebarContextMixin, ListView):
    model = Landmark
    template_name = 'common/landmarks-home.html'
    context_object_name = 'all_landmarks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchLandmarkForm(self.request.GET)

        user = self.request.user
        all_landmarks = context[self.context_object_name]

        # Add `has_liked` and `has_visited` to each post
        if user.is_authenticated:
            for landmark in all_landmarks:
                landmark.has_liked = landmark.likes.filter(user=user).exists()
                landmark.has_visited = landmark.visits.filter(user=user).exists()

                total_reviews = landmark.reviews.count()
                average_rating = landmark.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

                landmark.total_reviews = total_reviews
                landmark.average_rating = round(average_rating, 1)
                landmark.full_stars = range(int(average_rating))
                landmark.half_star = (average_rating % 1) >= 0.5
                landmark.empty_stars = range(5 - int(average_rating) - int((average_rating % 1) >= 0.5))

        context[self.context_object_name] = all_landmarks
        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')

        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(location_name__icontains=search_query)
            ). distinct()

        return queryset


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
