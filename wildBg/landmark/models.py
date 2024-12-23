import re

from django.contrib.auth.decorators import login_required
from django.core.validators import MinLengthValidator
from django.db import models

from wildBg.accounts.models import AppUser
from wildBg.landmark.choices import LandmarkLevelChoices
from multiselectfield import MultiSelectField


class Landmark(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='landmarks'
    )
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3, 'The name of the landmark must be logger than 2 symbols'),
        ],
    )

    location_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3, 'The location name must be logger than 2 symbols'),
        ],
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='landmarks/',
    )

    map_location = models.TextField(
        null=False,
        blank=False,
    )

    level = models.CharField(
        max_length=20,
        choices=LandmarkLevelChoices.choices
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        match = re.search(r'src="([^"]*)"', self.map_location)
        if match:
            self.map_location = match.group(1)

        super().save(*args, **kwargs)


class AdditionalLandmarkInfo(models.Model):
    landmark = models.OneToOneField(
        Landmark,
        on_delete=models.CASCADE,
        related_name='additional_landmark_info'
    )

    is_transition = models.BooleanField(
        default=False
    )

    duration = models.DurationField(
        null=True,
        blank=True,
    )

    is_accessible = models.BooleanField(
        default=False
    )

    distance_km = models.FloatField(
        null=True,
        blank=True,
    )

    suitable_for_children = models.BooleanField(
        default=False,
    )

    has_eating_places = models.BooleanField(
        default=False,
    )

    is_ennobled = models.BooleanField(
        default=False,
    )

    start_point = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(3, 'The start point must be logger than 2 symbols'),
        ],
        null=True,
        blank=True,
    )

    end_point = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(3, 'The end point must be logger than 2 symbols'),
        ],
        null=True,
        blank=True,
    )

    accessible_by_car = models.BooleanField(
        default=False,
    )

    has_parking = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'Additional Landmark Info for "{self.landmark.name}"'


class Review(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    landmark = models.ForeignKey(
        Landmark,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Review by {self.user.email} on {self.landmark.name}"


class Like(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    landmark = models.ForeignKey(
        Landmark,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('user', 'landmark')

    def __str__(self):
        return f"{self.user.email} likes {self.landmark.name}"


class Visit(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    landmark = models.ForeignKey(
        Landmark,
        on_delete=models.CASCADE,
        related_name='visits',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('user', 'landmark')

    def __str__(self):
        return f"{self.user.email} visited {self.landmark.name}"
