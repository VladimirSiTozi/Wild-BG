from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from wildBg.landmark.forms import LandmarkAddForm, LandmarkEditForm, AdditionalLandmarkInfoCreateForm, ReviewForm, \
    AdditionalLandmarkInfoEditForm
from wildBg.landmark.models import Landmark, Review, Like, Visit
from wildBg.mixins import SidebarContextMixin


class LandmarkAddView(LoginRequiredMixin, SidebarContextMixin, CreateView):
    model = Landmark
    form_class = LandmarkAddForm
    template_name = 'landmark/landmark-create.html'

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

        return super().form_valid(landmark_form)

    def forms_invalid(self, landmark_form, additional_info_form):
        # If either form is invalid, re-render the page with errors
        return self.render_to_response(self.get_context_data(
            form=landmark_form,
            additional_info_form=additional_info_form
        ))

    def get_success_url(self):
        return reverse_lazy(
            'details-landmark',
            kwargs={'pk': self.object.pk}
        )


class LandmarkDetailsView(SidebarContextMixin, DetailView):
    model = Landmark
    template_name = 'landmark/landmark-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            self.object.has_liked = self.object.likes.filter(user=user).exists()
            self.object.has_visited = self.object.visits.filter(user=user).exists()
        else:
            self.object.has_liked = False
            self.object.has_visited = False

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


class LandmarkEditView(LoginRequiredMixin, UserPassesTestMixin, SidebarContextMixin, UpdateView):
    model = Landmark
    template_name = 'landmark/landmark-edit.html'

    def get(self, request, *args, **kwargs):
        landmark = get_object_or_404(Landmark, pk=self.kwargs['pk'])
        additional_info = landmark.additional_landmark_info

        landmark_form = LandmarkEditForm(instance=landmark)
        additional_info_form = AdditionalLandmarkInfoEditForm(instance=additional_info)

        return render(request, self.template_name, {
            'landmark_form': landmark_form,
            'additional_info_form': additional_info_form,
            'object': landmark,
        })

    def post(self, request, *args, **kwargs):
        landmark = get_object_or_404(Landmark, pk=self.kwargs['pk'])
        additional_info = landmark.additional_landmark_info

        landmark_form = LandmarkEditForm(request.POST, request.FILES, instance=landmark)
        additional_info_form = AdditionalLandmarkInfoEditForm(request.POST, instance=additional_info)

        if landmark_form.is_valid() and additional_info_form.is_valid():
            landmark_form.save()
            additional_info_form.save()
            return redirect('details-landmark', pk=landmark.pk)

        return render(request, self.template_name, {
            'landmark_form': landmark_form,
            'additional_info_form': additional_info_form,
            'object': landmark,
        })

    def test_func(self):
        photo = get_object_or_404(Landmark, pk=self.kwargs['pk'])
        return self.request.user == photo.user

    def get_success_url(self):
        return reverse_lazy(
            'details-landmark',
            kwargs={'pk': self.object.pk}
        )


@login_required
def delete_photo(request, pk: int):
    photo = Landmark.objects.get(pk=pk)

    if request.user == photo.user:
        photo.delete()
    else:
        raise Http404
    return redirect('home')


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