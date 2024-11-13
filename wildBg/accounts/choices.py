from django.db import models


class UserLevelChoices(models.TextChoices):
    AMATEUR = 'Amateur', 'Amateur'
    INTERMEDIATE = 'Intermediate', 'Intermediate'
    PROFESSIONAL = 'Professional', 'Professional'

