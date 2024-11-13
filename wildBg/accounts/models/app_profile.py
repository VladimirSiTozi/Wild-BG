from django.contrib.auth import get_user_model
from django.db import models

from wildBg.accounts.choices import UserLevelChoices

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

    profile_picture = models.URLField(
        blank=True,
        null=True,
    )

    points = models.IntegerField(
        default=0
    )

    level = models.CharField(
        max_length=30,
        choices=UserLevelChoices.choices,
        default=UserLevelChoices.AMATEUR
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.first_name or self.last_name or 'Anonymous'