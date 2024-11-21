from django import forms


class SearchForm(forms.Form):
    user_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search by user name...'},
        )
    )

