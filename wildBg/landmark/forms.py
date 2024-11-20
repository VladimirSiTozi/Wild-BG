from django import forms

from wildBg.landmark.models import Landmark, AdditionalLandmarkInfo, Review


class LandmarkBaseForm(forms.ModelForm):
    class Meta:
        model = Landmark
        exclude = ('user', )


class LandmarkAddForm(LandmarkBaseForm):
    pass


class LandmarkEditForm(LandmarkBaseForm):
    pass


class AdditionalLandmarkInfoBaseForm(forms.ModelForm):
    class Meta:
        model = AdditionalLandmarkInfo
        exclude = ('landmark', )


class AdditionalLandmarkInfoCreateForm(AdditionalLandmarkInfoBaseForm):
    pass


class AdditionalLandmarkInfoEditForm(AdditionalLandmarkInfoBaseForm):
    pass


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Add review...'}),
            'rating': forms.RadioSelect()
        }