from django import forms
from django.contrib.auth import get_user_model

from wildBg.post.models import PostComment, Post, ReplyPostComment


UserModel = get_user_model()


# wildBg/post/forms.py

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', )
        labels = {
            'location': 'Location',
            'post_image': 'Image',
            'description': 'Description',
            'tagged_people': 'Tagged People',
        }
        widgets = {
            'location': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '-- Select a Landmark --'
            }),
            'post_image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter a description of your post...',
                'required': True
            }),
            'tagged_people': forms.MultipleHiddenInput(),
        }

    tagged_people = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        required=False,
        widget=forms.MultipleHiddenInput()
    )


class PostAddForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PhotoDeleteForm(PostBaseForm):
    pass


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add comment...'})
        }


class ReplyPostCommentForm(forms.ModelForm):
    class Meta:
        model = ReplyPostComment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add comment...'})
        }