from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from wildBg.landmark.forms import LandmarkAddForm
from wildBg.landmark.models import Landmark


class LandmarkAddView(CreateView):
    model = Landmark
    form_class = LandmarkAddForm
    template_name = 'landmark/landmark-create.html'
    success_url = reverse_lazy('test-home')

    def form_valid(self, form):
        landmark = form.save(commit=False)
        landmark.user = self.request.user
        return super().form_valid(form)

