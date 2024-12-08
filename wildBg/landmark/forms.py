from django import forms

from wildBg.landmark.models import Landmark, AdditionalLandmarkInfo, Review


class LandmarkBaseForm(forms.ModelForm):
    class Meta:
        model = Landmark
        exclude = ('user',)

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter the name of the landmark',
                'maxlength': 100,
                'required': True
            }),
            'location_name': forms.TextInput(attrs={
                'placeholder': 'Enter the location name',
                'maxlength': 100,
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter a brief description of the landmark',
                'rows': 4,
                'cols': 50
            }),
            'image': forms.ClearableFileInput(attrs={
                'placeholder': 'Upload an image of the location'
            }),
            'map_location': forms.Textarea(attrs={
                'placeholder': '<iframe src=...></iframe>',
                'rows': 4,
                'cols': 50
            }),
            'level': forms.Select(attrs={
                'placeholder': 'Select the difficulty or level'
            }),
        }

        labels = {
            'name': 'Landmark Name',
            'location_name': 'Location Name',
            'description': 'Description',
            'image': 'Location Image',
            'map_location': 'Map Embed Code',
            'level': 'Landmark Level',
        }


class LandmarkAddForm(LandmarkBaseForm):
    pass


class LandmarkEditForm(LandmarkBaseForm):
    pass


class AdditionalLandmarkInfoBaseForm(forms.ModelForm):
    class Meta:
        model = AdditionalLandmarkInfo
        exclude = ('landmark',)

        widgets = {
            'duration': forms.TextInput(attrs={
                'placeholder': 'Enter duration in HH:MM:SS format, e.g., 1:30:00 for 1 hour 30 minutes'
            }),
            'distance_km': forms.TextInput(attrs={
                'placeholder': 'Enter distance in kilometers, e.g., 5 or 10'
            }),
            'start_point': forms.TextInput(attrs={
                'placeholder': 'Enter the starting point, e.g., Main Entrance'
            }),
            'end_point': forms.TextInput(attrs={
                'placeholder': 'Enter the ending point, e.g., Summit'
            }),
        }

        labels = {
            'distance_km': 'Distance (kilometers)',
            'is_accessible': 'Easily accessible',
            'duration': 'Estimated Duration',
            'start_point': 'Start Point',
            'end_point': 'End Point',
            'suitable_for_children': 'Suitable for Children',
            'has_eating_places': 'Has Eating Places',
            'is_ennobled': 'Is Ennobled',
            'accessible_by_car': 'Accessible by Car',
            'has_parking': 'Has Parking',
        }


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
