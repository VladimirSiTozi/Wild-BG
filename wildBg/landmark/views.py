from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from wildBg.landmark.forms import LandmarkAddForm, LandmarkEditForm, AdditionalLandmarkInfoCreateForm
from wildBg.landmark.models import Landmark


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

class LandmarkDetailsView(DetailView):
    model = Landmark
    template_name = 'landmark/landmark-details.html'

    # def get_context_data(self, **kwargs):


# class LandmarkEditView(UpdateView):
#     model = Landmark
#     form_class = LandmarkEditForm
#     template_name = 'landmark/landmark-edit.html'
#
#     def get_success_url(self):
#         return reverse_lazy(
#             'land'
#         )
