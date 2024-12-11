from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from wildBg.accounts.models import Profile
from wildBg.common.forms import SearchForm, SearchLandmarkForm
from wildBg.landmark.models import Landmark
from wildBg.landmark.serializer import LandmarkSerializer
from wildBg.mixins import SidebarContextMixin
from wildBg.post.forms import PostCommentForm
from wildBg.post.models import Post


UserModel = get_user_model()


class HomePageView(SidebarContextMixin, ListView):
    model = Post
    template_name = 'common/home.html'
    context_object_name = 'all_posts'
    paginate_by = 10

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
    paginate_by = 10

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


class LandmarkListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    async def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query', None)
        queryset = Landmark.objects.all().order_by('-created_at')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(location_name__icontains=search_query)
            ).distinct()

        # Превръщаме queryset в списък асинхронно
        landmarks = await sync_to_async(list)(queryset)
        user = request.user if request.user.is_authenticated else None

        async def get_extra_info(landmark):
            total_reviews = await sync_to_async(lambda: landmark.reviews.count())()
            average_rating_val = await sync_to_async(
                lambda: landmark.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            )()

            has_liked = False
            has_visited = False
            if user:
                has_liked = await sync_to_async(
                    lambda: landmark.likes.filter(user=user).exists()
                )()
                has_visited = await sync_to_async(
                    lambda: landmark.visits.filter(user=user).exists()
                )()

            return {
                'has_liked': has_liked,
                'has_visited': has_visited,
                'total_reviews': total_reviews,
                'average_rating': round(average_rating_val, 1)
            }

        enhanced_landmarks = []
        for lmk in landmarks:
            extra_info = await get_extra_info(lmk)
            serialized = LandmarkSerializer(lmk).data
            serialized.update(extra_info)
            enhanced_landmarks.append(serialized)

        return Response(enhanced_landmarks)


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
