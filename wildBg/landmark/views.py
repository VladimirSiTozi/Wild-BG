from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from wildBg.landmark.forms import LandmarkAddForm, LandmarkEditForm, AdditionalLandmarkInfoCreateForm, ReviewForm
from wildBg.landmark.models import Landmark, Review
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

        context['likes'] = self.object.likes.all()
        context['visits'] = self.object.visits.all()
        context['review_form'] = ReviewForm

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


def add_review(request, pk):
    landmark = get_object_or_404(Landmark, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.landmark = landmark
            review.rating = request.POST.get('rating')
            review.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    form = ReviewForm()
    context = {
        'landmark': landmark,
        'form': form
    }

    return render(request, 'landmark/landmark-details.html', context)


# class LandmarkEditView(UpdateView):
#     model = Landmark
#     form_class = LandmarkEditForm
#     template_name = 'landmark/landmark-edit.html'
#
#     def get_success_url(self):
#         return reverse_lazy(
#             'land'
#         )
