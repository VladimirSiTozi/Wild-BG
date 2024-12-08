from django.contrib.auth import get_user_model
from django.db import models

from wildBg.accounts.models import AppUser
from wildBg.landmark.models import Landmark

UserModel = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    location = models.ForeignKey(
        Landmark,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    post_image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
    )

    description = models.TextField()

    tagged_people = models.ManyToManyField(
        AppUser,
        related_name='tagged_posts',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        location_name = self.location.name if self.location else "No Location"
        return f"Post by {self.author.email} at {location_name}"


class PostComment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        # Access the author's profile safely
        profile = getattr(self.author, 'profile', None)
        first_name = profile.first_name if profile and profile.first_name else 'Anonymous'
        return f'Comment by {first_name} on {self.created_at.strftime("%Y-%m-%d")}'


class ReplyPostComment(models.Model):
    comment = models.ForeignKey(
        PostComment,
        on_delete=models.CASCADE,
        related_name='replies',
    )

    author = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        # Access the author's profile safely
        profile = getattr(self.author, 'profile', None)
        first_name = profile.first_name if profile and profile.first_name else 'Anonymous'
        return f'Reply by {first_name} on {self.created_at.strftime("%Y-%m-%d")}'


class PostLike(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        user_email = self.user.email
        post_description = (self.to_post.description[:30] + "...") if len(
            self.to_post.description) > 30 else self.to_post.description
        return f"{user_email} liked: {post_description}"

