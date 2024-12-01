from django import forms

from wildBg.post.models import PostComment, Post


class PostBaseForm(forms.Form):
    class Meta:
        model = Post
        exclude = ('user', )


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