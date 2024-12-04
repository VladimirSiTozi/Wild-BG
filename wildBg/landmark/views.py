from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from wildBg.landmark.forms import LandmarkAddForm, LandmarkEditForm, AdditionalLandmarkInfoCreateForm, ReviewForm
from wildBg.landmark.models import Landmark, Review, Like, Visit
from wildBg.mixins import SidebarContextMixin


class LandmarkAddView(CreateView):
    model = Landmark
    form_class = LandmarkAddForm
    template_name = 'landmark/landmark-create.html'
    success_url = reverse_lazy('test-home')

    def get_context_data(self, **kwargs):
        # Add both forms to the context
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # If the request is a POST, use the submitted form data
            context['additional_info_form'] = AdditionalLandmarkInfoCreateForm(self.request.POST)
        else:
            # If it's a GET request, provide an empty form
            context['additional_info_form'] = AdditionalLandmarkInfoCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        # Handle both forms
        self.object = None
        landmark_form = self.get_form()
        additional_info_form = AdditionalLandmarkInfoCreateForm(self.request.POST)

        if landmark_form.is_valid() and additional_info_form.is_valid():
            return self.forms_valid(landmark_form, additional_info_form)
        else:
            return self.forms_invalid(landmark_form, additional_info_form)

    def forms_valid(self, landmark_form, additional_info_form):
        # Save landmark instance first
        landmark = landmark_form.save(commit=False)
        landmark.user = self.request.user
        landmark.save()

        # Save additional landmark info and link it to the landmark
        additional_info = additional_info_form.save(commit=False)
        additional_info.landmark = landmark
        additional_info.save()

        return redirect(self.success_url)

    def forms_invalid(self, landmark_form, additional_info_form):
        # If either form is invalid, re-render the page with errors
        return self.render_to_response(self.get_context_data(
            form=landmark_form,
            additional_info_form=additional_info_form
        ))


class LandmarkDetailsView(SidebarContextMixin, DetailView):
    model = Landmark
    template_name = 'landmark/landmark-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.has_liked = self.object.likes.filter(user=self.request.user).exists()
        self.object.has_visited = self.object.visits.filter(user=self.request.user).exists()

        context['likes'] = self.object.likes.all()
        context['visits'] = self.object.visits.all()
        context['review_form'] = ReviewForm()

        total_reviews = self.object.reviews.count()
        average_rating = self.object.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        context['total_reviews'] = total_reviews
        context['average_rating'] = round(average_rating, 1)
        context['full_stars'] = range(int(average_rating))
        context['half_star'] = (average_rating % 1) >= 0.5
        context['empty_stars'] = range(5 - int(average_rating) - int((average_rating % 1) >= 0.5))

        reviews_with_star_info = []
        for review in self.object.reviews.all().order_by('-created_at'):
            reviews_with_star_info.append({
                'review': review,
                'user': review.user,
                'created_at': review.created_at,
                'rating': review.rating,
                'comment': review.comment,
                'full_stars': range(int(review.rating)),
                'empty_stars': range(5 - int(review.rating)),

            })

        context['reviews'] = reviews_with_star_info

        return context


@login_required
def add_review(request, pk: int):
    if request.method == 'POST':
        landmark = Landmark.objects.get(pk=pk)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.landmark = landmark
            review.comment = request.POST.get('comment')
            review.rating = request.POST.get('rating')
            review.save()
        else:
            print('kles')

    return redirect(request.META.get('HTTP_REFERER', f'#{pk}'))


@login_required
def like_func(request, pk: int):
    liked_object = Like.objects.filter(
        landmark=pk,
        user=request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(landmark_id=pk, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{pk}')


@login_required
def visit_func(request, pk: int):
    visited_object = Visit.objects.filter(
        landmark=pk,
        user=request.user
    ).first()

    if visited_object:
        visited_object.delete()
    else:
        visit = Visit(landmark_id=pk, user=request.user)
        visit.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{pk}')