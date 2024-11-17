from django import forms

from wildBg.landmark.models import Landmark


class LandmarkBaseForm(forms.ModelForm):
    class Meta:
        model = Landmark
        exclude = ('user', )


class LandmarkAddForm(LandmarkBaseForm):
    pass


class LandmarkEditForm(LandmarkBaseForm):
    pass
