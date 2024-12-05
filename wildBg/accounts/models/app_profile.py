from django.contrib.auth import get_user_model
from django.db import models

from wildBg.accounts.choices import UserLevelChoices
from wildBg.landmark.models import Landmark

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        # default='images/anonymous_full.jpg',
        blank=True,
        null=True,
    )

    description = models.TextField()

    background_image = models.ImageField(
        upload_to='background_images/',
        # default='images/default_background.jpg',
    )

    points = models.IntegerField(
        default=0
    )

    level = models.CharField(
        max_length=30,
        choices=UserLevelChoices.choices,
        default=UserLevelChoices.BEGINNER
    )

    landmarks_visited = models.ManyToManyField(
        Landmark,
        related_name='visited_by_profiles',
        blank=True,
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.first_name or self.last_name or 'Anonymous'
